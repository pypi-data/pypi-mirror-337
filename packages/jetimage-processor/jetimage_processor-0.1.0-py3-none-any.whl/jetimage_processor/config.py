import shutil
import os
import yaml
import argparse
import numpy as np
from pathlib import Path
import importlib.resources as pkg_resources
import sys

class Config:
    def __init__(self, config_file='config.yaml'):
        """Load configuration from YAML file and command-line arguments.
        If config_file does not exist, load the default_config.yaml bundled with the package.
        """
        if not Path(config_file).exists():
            # Copy default_config.yaml to example_config.yaml in the current working directory
            example_config_path = Path("example_config.yaml")
            with pkg_resources.open_text(__package__, "default_config.yaml") as default_config:
                with open(example_config_path, 'w') as example_config:
                    shutil.copyfileobj(default_config, example_config)
            
            # Interrupt execution with a clear message
            print("\n" + ("*" * 80))
            print(f"ERROR: Configuration file '{config_file}' not found!")
            print(f"A default example configuration has been created as '{example_config_path}'.")
            print("Please create or modify 'config.yaml' based on 'example_config.yaml' and rerun the program.")
            print("*" * 80 + "\n")
            sys.exit(1)  # Exit the program
        
        # Load the configuration
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        

        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Jet Image Processing')
        parser.add_argument('--dataset', type=str, 
                           default=self.config['input']['default'],
                           choices=list(self.config['input']['files'].keys()),
                           help='Dataset key from config file')
        parser.add_argument('--output-dir', type=str, 
                           help='Custom output directory')
        parser.add_argument('--sample-size', type=int, default=5000,
                           help='Maximum number of jet images to process')
        self.args = parser.parse_args()
        
        # Set current dataset based on argument
        self.current_dataset = self.args.dataset
        
    def get_input_file_paths(self):
        """Get the list of input file paths for the current dataset."""
        dataset_config = self.config['input']['files'][self.current_dataset]
        if 'paths' in dataset_config:
            return [Path(p) for p in dataset_config['paths']]
        else:
            return [Path(dataset_config['path'])]
            
    def get_input_file_path(self):
        """Get the input file path for the current dataset."""
        return self.config['input']['files'][self.current_dataset]['path']
    
    def get_input_file_name(self):
        """Get the input file name (basename) for the current dataset.
        If multiple files are provided, return the basename of the first one.
        """
        file_paths = self.get_input_file_paths()
        return file_paths[0].stem

    def get_h5_file_path(self):
        """Generate the H5 file path based on input file name."""
        input_filename = self.get_input_file_name()
        prefix = self.config['output']['h5_directory_prefix']
        h5_filename = self.config['output']['h5_file_name']
        
        # Create directory name by adding prefix to filename
        directory = f"{prefix}{input_filename}"
        
        # Special case for test dataset - use simplified path
        if self.current_dataset == 'test':
            directory = f"{prefix}test"
            
        return Path(directory) / h5_filename
    
    def get_output_dir(self):
        """Get the output directory path."""
        if self.args.output_dir:
            return Path(self.args.output_dir)
        else:
            h5_path = self.get_h5_file_path()
            return h5_path.parent
    
    def get_histogram_edges(self):
        """Get histogram edges as numpy arrays."""
        cfg = self.config['histogram']
        return {
            'transformed_x_edges': np.linspace(*cfg['transformed_x_edges']),
            'transformed_y_edges': np.linspace(*cfg['transformed_y_edges']),
            'eta_edges': np.linspace(*cfg['eta_edges']),
            'phi_edges': np.linspace(*cfg['phi_edges'])
        }
    
    def get_selection_criteria(self):
        """Get jet selection criteria."""
        return self.config['selection']
    
    def get_transform_params(self):
        """Get transformation parameters."""
        return self.config['transform']
    
    def get_sample_size(self):
        """Get sample size for analysis."""
        return self.args.sample_size
        
    def get_branches(self):
        """Get branch names for the ROOT TTree]."""
        return self.config.get('branches', {})