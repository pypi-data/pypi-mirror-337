import uproot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from pathlib import Path
import h5py

from .config import Config
from .transform_helper import gram_schmidt_transform


def process_data():
    """
    Main pipeline for processing jet data from ROOT or Parquet files.
    """
    cfg = Config()
    input_file_paths = cfg.get_input_file_paths()
    output_dir = cfg.get_output_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    transform_params = cfg.get_transform_params()
    selection_criteria = cfg.get_selection_criteria()
    edges = cfg.get_histogram_edges()

    # Setup the custom colormap
    cmap = _create_custom_colormap()
    h5_output_path = cfg.get_h5_file_path()

    eta_edges = edges['eta_edges']
    phi_edges = edges['phi_edges']
    transformed_x_edges = edges['transformed_x_edges']
    transformed_y_edges = edges['transformed_y_edges']

    _initialize_hdf5(h5_output_path, transformed_x_edges, transformed_y_edges, cfg, str(input_file_paths))

    # Global accumulators for all histograms.
    global_accumulated_hist = np.zeros((len(eta_edges)-1, len(phi_edges)-1))
    global_accumulated_transformed_hist = np.zeros((len(transformed_x_edges)-1, len(transformed_y_edges)-1))

    for input_file_path in input_file_paths:
        print(f"Processing file: {input_file_path}")
        if input_file_path.suffix == ".parquet":
            print(f"Processing parquet file: {input_file_path}")
            h, ht = _process_events_parquet(input_file_path, selection_criteria, transform_params,
                                            eta_edges, phi_edges,
                                            transformed_x_edges, transformed_y_edges,
                                            h5_output_path, cmap, cfg)
        else:
            print(f"Processing ROOT file: {input_file_path}")
            print(f"Processing dataset: {cfg.current_dataset}")
            print(f"ROOT file: {input_file_path}")
            print(f"Output directory: {output_dir}")
            h, ht = _process_events_root(input_file_path, selection_criteria, transform_params,
                                         eta_edges, phi_edges,
                                         transformed_x_edges, transformed_y_edges,
                                         h5_output_path, cmap, cfg)
        global_accumulated_hist += h
        global_accumulated_transformed_hist += ht

    # Generate one final set of plots with all events.
    _generate_plots(
        eta_edges, phi_edges, global_accumulated_hist, cmap,
        output_dir=cfg.get_output_dir(),
        title=f'Accumulated Constituents Histogram ({cfg.current_dataset})',
        xlabel='Eta', ylabel='Phi', filename='accumulated_constituents_all_events.png'
    )
    _generate_plots(
        transformed_x_edges, transformed_y_edges, global_accumulated_transformed_hist, cmap,
        output_dir=cfg.get_output_dir(),
        title=f'Accumulated Transformed Constituents ({cfg.current_dataset})',
        xlabel='X (Transformed)', ylabel='Y (Transformed)',
        filename='accumulated_transformed_constituents_all_events.png',
        log_scale=True
    )


def _create_custom_colormap():
    viridis = plt.cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    white = np.array([1, 1, 1, 1])
    newcolors[0, :] = white
    return ListedColormap(newcolors)


def _initialize_hdf5(h5_output_path, x_edges, y_edges, cfg, source_file):
    with h5py.File(h5_output_path, 'w') as h5f:
        h5f.create_dataset('jet_images', shape=(0, len(x_edges)-1, len(y_edges)-1), 
                           maxshape=(None, len(x_edges)-1, len(y_edges)-1),
                           dtype=np.float32, chunks=(1, len(x_edges)-1, len(y_edges)-1), 
                           compression='gzip')
        h5f.create_dataset('event_indices', shape=(0,), maxshape=(None,), dtype=np.int32)
        h5f.create_dataset('jet_indices', shape=(0,), maxshape=(None,), dtype=np.int32)
        h5f.create_dataset('x_edges', data=x_edges)
        h5f.create_dataset('y_edges', data=y_edges)
        h5f.attrs['source_file'] = source_file
        h5f.attrs['dataset_name'] = cfg.current_dataset


def _process_events_root(input_file_path, selection_criteria, transform_params,
                         eta_edges, phi_edges, transformed_x_edges, transformed_y_edges,
                         h5_output_path, cmap, cfg):
    # Process events using uproot for ROOT files
    branches = cfg.get_branches()

    try:
        with uproot.open(input_file_path) as file:
            tree = file[branches["tree_name"]]
            pf_IdxFatJet = tree[branches["pf_IdxFatJet"]].array()
            estimated_num_jets = sum(len(np.unique(idx.to_numpy())) for idx in pf_IdxFatJet)
            print(f"Estimated number of jets: {estimated_num_jets}")
    except FileNotFoundError:
        print(f"Error: ROOT file not found at path '{input_file_path}'. Check your configuration.")
        return
    except KeyError as e:
        print(f"Error: Missing expected branch {str(e)} in ROOT file. Verify your configuration.")
        return

    with uproot.open(input_file_path) as file:
        tree = file[branches["tree_name"]]
        pf_pt       = tree[branches["pf_pt"]].array()
        pf_eta      = tree[branches["pf_eta"]].array()
        pf_phi      = tree[branches["pf_phi"]].array()
        pf_IdxFatJet= tree[branches["pf_IdxFatJet"]].array()
        fatjet_pt   = tree[branches["fatjet_pt"]].array()
        fatjet_eta  = tree[branches["fatjet_eta"]].array()
        fatjet_phi  = tree[branches["fatjet_phi"]].array()
        fatjet_mass = tree[branches["fatjet_mass"]].array()

        jet_count = 0
        batch_size = 1000
        batch_images = []
        batch_events = []
        batch_jet_ids = []
        accumulated_hist = np.zeros((len(eta_edges)-1, len(phi_edges)-1))
        accumulated_transformed_hist = np.zeros((len(transformed_x_edges)-1, len(transformed_y_edges)-1))

        # Loop over each event
        for event_idx in range(len(pf_pt)):
            if event_idx % 100 == 0:
                print(f"Processing event {event_idx}/{len(pf_pt)}")
            event_pt    = pf_pt[event_idx].to_numpy()
            event_eta   = pf_eta[event_idx].to_numpy()
            event_phi   = pf_phi[event_idx].to_numpy()
            event_pfIdx = pf_IdxFatJet[event_idx].to_numpy()

            # Apply selection criteria for boosted jets
            fatjet_mask = (
                (fatjet_pt[event_idx] > selection_criteria['pt_min']) & 
                (fatjet_eta[event_idx] < selection_criteria['eta_max']) &
                (fatjet_eta[event_idx] > -selection_criteria['eta_max']) &
                (fatjet_mass[event_idx] > selection_criteria['mass_min'])
            )
            
            if event_idx % 100 == 0:
                print("APPLYING SELECTION ON BOOSTED JETS")
            if not fatjet_mask:
                continue            

            unique_jets = np.unique(event_pfIdx)
            for jet_id in unique_jets:
                mask = event_pfIdx == jet_id
                constituents_eta = event_eta[mask]
                constituents_phi = event_phi[mask]
                constituents_pt  = event_pt[mask]
                # Skip jets with too few constituents
                if len(constituents_pt) < 3:
                    continue

                # Histogram for original jet constituents
                hist, _, _ = np.histogram2d(
                    constituents_eta, constituents_phi,
                    bins=[eta_edges, phi_edges],
                    weights=constituents_pt
                )
                accumulated_hist += hist

                # Apply Gram-Schmidt transformation
                transformed = gram_schmidt_transform(
                    constituents_eta, 
                    constituents_phi, 
                    constituents_pt,
                    mB=transform_params.get('mB', 1.0),
                    EB=transform_params.get('EB', 2.0)
                )
               
                # Histogram for transformed jet image
                hist_transformed, _, _ = np.histogram2d(
                    transformed["x"], transformed["y"],
                    bins=[transformed_x_edges, transformed_y_edges],
                    weights=transformed["content"]
                )
                accumulated_transformed_hist += hist_transformed

                # Collect data for batch
                batch_images.append(hist_transformed)
                batch_events.append(event_idx)
                batch_jet_ids.append(jet_id)

                # Write batch if reached batch_size
                if len(batch_images) >= batch_size:
                    _write_batch(h5_output_path, batch_images, batch_events, batch_jet_ids)
                    jet_count += len(batch_images)
                    print(f"Wrote batch: {jet_count} jets processed so far")
                    batch_images, batch_events, batch_jet_ids = [], [], []

        # Write any remaining jets in a final batch
        if batch_images:
            _write_batch(h5_output_path, batch_images, batch_events, batch_jet_ids)
            jet_count += len(batch_images)

        print(f"Completed processing: {jet_count} total jets saved to {h5_output_path}")
        return accumulated_hist, accumulated_transformed_hist

def _process_events_parquet(input_file_path, selection_criteria, transform_params,
                            eta_edges, phi_edges, transformed_x_edges, transformed_y_edges,
                            h5_output_path, cmap, cfg):
    import awkward as ak
    # Read the parquet file using Awkward Arrays.
    events = ak.from_parquet(input_file_path)
    
    # Optionally filter events by jet label (if defined in config as "parquet_label")
    jet_label = cfg.config.get('parquet_label', None)
    if jet_label is not None:
        events = events[events["jet_label"] == jet_label]
    
    jet_count = 0
    batch_size = 1000
    batch_images = []
    batch_events = []
    batch_jet_ids = []
    
    accumulated_hist = np.zeros((len(eta_edges)-1, len(phi_edges)-1))
    accumulated_transformed_hist = np.zeros((len(transformed_x_edges)-1, len(transformed_y_edges)-1))
    
    # In the new format, each record corresponds to one jet.
    # Use ak.to_list() to loop in pure Python.
    for idx, event in enumerate(ak.to_list(events)):
        # Apply jet-level selection (e.g. jet_pt must pass selection).
        if event["jet_pt"] < selection_criteria["pt_min"]:
            continue
        
        # Convert constituent fields to NumPy arrays to perform element-wise operations.
        constituents_deta = np.array(event["part_deta"])
        constituents_dphi = np.array(event["part_dphi"])
        constituents_pt   = np.array(event["part_energy"])
        
        # Compute absolute η and φ for each constituent.
        constituents_eta = event["jet_eta"] + constituents_deta
        constituents_phi = event["jet_phi"] + constituents_dphi
        
        # Ensure there are enough constituents.
        if len(constituents_pt) < 3:
            continue
        
        # Histogram the original constituent information.
        hist, _, _ = np.histogram2d(
            constituents_eta, constituents_phi,
            bins=[eta_edges, phi_edges],
            weights=constituents_pt
        )
        accumulated_hist += hist
        
        # Apply the Gram-Schmidt transformation.
        transformed = gram_schmidt_transform(
            constituents_eta,
            constituents_phi,
            constituents_pt,
            mB=transform_params.get('mB', 1.0),
            EB=transform_params.get('EB', 2.0)
        )
        # Histogram the transformed coordinates.
        hist_transformed, _, _ = np.histogram2d(
            transformed["x"], transformed["y"],
            bins=[transformed_x_edges, transformed_y_edges],
            weights=transformed["content"]
        )
        accumulated_transformed_hist += hist_transformed
        
        # Accumulate batch information.
        batch_images.append(hist_transformed)
        batch_events.append(idx)
        batch_jet_ids.append(idx)  # Use the event index as the jet id.
        
        if len(batch_images) >= batch_size:
            _write_batch(h5_output_path, batch_images, batch_events, batch_jet_ids)
            jet_count += len(batch_images)
            print(f"Wrote batch: {jet_count} jets processed so far")
            batch_images, batch_events, batch_jet_ids = [], [], []
    
    # Write any remaining batch.
    if batch_images:
        _write_batch(h5_output_path, batch_images, batch_events, batch_jet_ids)
        jet_count += len(batch_images)
    
    print(f"Completed processing: {jet_count} total jets saved to {h5_output_path}")
    return accumulated_hist, accumulated_transformed_hist

def _write_batch(h5_output_path, batch_images, batch_events, batch_jet_ids):
    with h5py.File(h5_output_path, 'a') as h5f:
        current_size = h5f['jet_images'].shape[0]
        new_size = current_size + len(batch_images)
        h5f['jet_images'].resize(new_size, axis=0)
        h5f['event_indices'].resize(new_size, axis=0)
        h5f['jet_indices'].resize(new_size, axis=0)
        h5f['jet_images'][current_size:new_size] = np.array(batch_images, dtype=np.float32)
        h5f['event_indices'][current_size:new_size] = np.array(batch_events, dtype=np.int32)
        h5f['jet_indices'][current_size:new_size] = np.array(batch_jet_ids, dtype=np.int32)
        h5f.attrs['total_jets'] = new_size


def _generate_plots(x_edges, y_edges, hist, cmap, output_dir, title, xlabel, ylabel, filename, log_scale=False):
    plt.figure(figsize=(8, 6))
    im_kwargs = {
        'origin': 'lower',
        'aspect': 'auto',
        'cmap': cmap,
        'extent': [x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]]
    }
    if log_scale:
        im_kwargs['norm'] = 'log'
    plt.imshow(hist.T, **im_kwargs)
    plt.colorbar(label=('Accumulated Transformed pT' if log_scale else 'Accumulated pT'))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.savefig(Path(output_dir) / filename)
    plt.close()


def main():
    process_data()


if __name__ == '__main__':
    main()