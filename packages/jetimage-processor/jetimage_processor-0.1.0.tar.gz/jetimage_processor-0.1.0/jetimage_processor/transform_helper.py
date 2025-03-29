import numpy as np
"""
Helper functions for jet transformation and histogram generation.
This module provides functions to apply the Gram-Schmidt transformation
to jet constituents and to generate 2D histograms for visualization.
25/03/2025: reviewed and updated for clarity and efficiency.
TODO: investige the effect of the jet selection (top-3 vs all constituents)
"""

def boost_along_axis(p, E, epsilon1, delta_y):
    """
    Boost a single constituent along the jet axis (epsilon1) by a rapidity shift delta_y.
    """
    p_parallel = np.dot(p, epsilon1)
    p_perp = p - p_parallel * epsilon1
    E_boosted = E * np.cosh(delta_y) - p_parallel * np.sinh(delta_y)
    p_parallel_boosted = p_parallel * np.cosh(delta_y) - E * np.sinh(delta_y)
    p_boosted = p_perp + p_parallel_boosted * epsilon1
    return p_boosted, E_boosted

def gram_schmidt_transform(etas, phis, pts, mB=1.0, EB=2.0):
    """
    Transform jet constituents using the procedure from the article.
    
    Steps:
      1. Convert (η, φ, pT) to 3D momenta and energies (E = pT*cosh(η)).
      2. Select the three constituents with highest momentum norm to form the jet.
      3. Rescale the jet four-momentum so that its invariant mass becomes mB.
      4. Apply a Lorentz boost so that the jet energy becomes EB.
         (Boost factor: γ_B = EB/mB; in this project, γ_B is chosen as 2.)
      5. Boost each constituent along the jet axis.
      6. Construct the Gram-Schmidt basis using the boosted top constituents:
             ε̂₁ = boosted jet momentum/|boosted jet momentum|,
             ε̂₂ from boosted p₁, and
             ε̂₃ from boosted p₂.
      7. Compute new coordinates: 
             X = (p_boosted·ε̂₂)/E_boosted, Y = (p_boosted·ε̂₃)/E_boosted,
         and weight ω = E_boosted/EB.
    
    Returns:
      dict: {'x': Xs, 'y': Ys, 'content': weights}
    """
    # Step 1: Convert to 3D momentum and compute energies.
    px = pts * np.cos(phis)
    py = pts * np.sin(phis)
    pz = pts * np.sinh(etas)
    momenta = np.column_stack((px, py, pz))
    energies = pts * np.cosh(etas)  # For massless particles.
    
    # Step 2: Select top-3 constituents by |p|
    p_norms = np.linalg.norm(momenta, axis=1)
    top3_indices = np.argsort(p_norms)[-3:]
    p1, p2, p3 = momenta[top3_indices]
    E1, E2, E3 = energies[top3_indices]
    
    # Compute jet four-momentum (from top 3).
    # jet_momentum = p1 + p2 + p3
    # E_J = E1 + E2 + E3
    # Alternatively, compute jet four-momentum from all constituents.
    jet_momentum = np.sum(momenta, axis=0)
    E_J = np.sum(energies)


    # Step 3: Rescale jet so that its invariant mass is mB.
    m_J2 = E_J**2 - np.linalg.norm(jet_momentum)**2
    m_J = np.sqrt(max(m_J2, 1e-6))
    # print("Original jet mass (before rescaling):", m_J)
    rescale_factor = mB / m_J
    jet_momentum *= rescale_factor
    E_J *= rescale_factor
    # print("After rescaling, jet mass is set to mB =", mB)
    
    # Step 4: Compute jet rapidity.
    B = np.linalg.norm(jet_momentum)
    y_J = np.arctanh(B / E_J)
    
    # Compute desired boost rapidity from EB and mB.
    beta_B = np.sqrt(1 - (mB**2 / EB**2))
    y_B = np.arctanh(beta_B)
    # delta_y = y_B - y_J
    delta_y =  y_J - y_B # 
    # print("Jet rapidity (y_J):", y_J, "Desired boost rapidity (y_B):", y_B, "Delta y:", delta_y)
    
    # Determine the jet axis unit vector from the rescaled jet momentum.
    epsilon1 = jet_momentum / B
    
    # Step 5: Boost each constituent along the jet axis.
    N = len(etas)
    boosted_momenta = np.empty_like(momenta)
    boosted_energies = np.empty_like(energies)
    for i in range(N):
        p = momenta[i]
        E = energies[i]
        p_boosted, E_boosted = boost_along_axis(p, E, epsilon1, delta_y)
        boosted_momenta[i] = p_boosted
        boosted_energies[i] = E_boosted
    
    # Also boost the top-3 constituents to define the basis.
    p1_boost, E1_boost = boost_along_axis(p1, E1, epsilon1, delta_y)
    p2_boost, E2_boost = boost_along_axis(p2, E2, epsilon1, delta_y)
    p3_boost, E3_boost = boost_along_axis(p3, E3, epsilon1, delta_y)
    
    # Compute the boosted jet momentum from the top-3 constituents.
    # boosted_jet_momentum = p1_boost + p2_boost + p3_boost
    # epsilon1_new = boosted_jet_momentum / np.linalg.norm(boosted_jet_momentum)

    # Alternatively, use all boosted constituents for the new jet axis
    boosted_jet_momentum = np.sum(boosted_momenta, axis=0)
    epsilon1_new = boosted_jet_momentum / np.linalg.norm(boosted_jet_momentum)
    
    # Step 6: Construct Gram-Schmidt basis.
    # ε̂₂ from boosted p1.
    proj_p1 = np.dot(p1_boost, epsilon1_new) * epsilon1_new
    temp = p1_boost - proj_p1
    if np.linalg.norm(temp) < 1e-6:
        raise ValueError("Boosted p1 is collinear with ε̂₁; cannot construct ε̂₂.")
    epsilon2 = temp / np.linalg.norm(temp)
    
    # ε̂₃ from boosted p2.
    proj_p2 = np.dot(p2_boost, epsilon1_new) * epsilon1_new + np.dot(p2_boost, epsilon2) * epsilon2
    temp = p2_boost - proj_p2
    if np.linalg.norm(temp) < 1e-6:
        raise ValueError("Boosted p2 lies in the span of ε̂₁ and ε̂₂; cannot construct ε̂₃.")
    epsilon3 = temp / np.linalg.norm(temp)
    
    # Step 7: For each boosted constituent, project onto ε̂₂ and ε̂₃.
    Xs = np.dot(boosted_momenta, epsilon2) / boosted_energies
    Ys = np.dot(boosted_momenta, epsilon3) / boosted_energies
    
    # Weights: fraction of constituent energy.
    weights = boosted_energies / EB
    
    return {"x": Xs, "y": Ys, "content": weights}

# ---------------- Testing Block ----------------

# Generate test data for constituents.
np.random.seed(42)
num_constituents = 10
etas = np.random.uniform(-2.5, 2.5, num_constituents)
phis = np.random.uniform(-np.pi, np.pi, num_constituents)
pts = np.random.uniform(10, 100, num_constituents)

# Set boost parameters as per the thesis.
mB = 1.0        # Target jet mass
gamma_B = 2.0   # Chosen boost factor
EB = gamma_B * mB  # Thus EB = 2.0

result = gram_schmidt_transform(etas, phis, pts, mB, EB)

print("\nTransformed x-coordinates:", result["x"])
print("Transformed y-coordinates:", result["y"])
print("Transformed weights (content):", result["content"])

total_weight = np.sum(result["content"])
print("\nTotal weight (sum of energies/EB):", total_weight)
print("Original total energy/EB:", np.sum(pts * np.cosh(etas)) / EB)

# -------- Testing Block for Boost Parameter Effects --------

# Use same input jet with different boost parameters
np.random.seed(42)
num_constituents = 10
etas = np.random.uniform(-2.5, 2.5, num_constituents)
phis = np.random.uniform(-np.pi, np.pi, num_constituents)
pts = np.random.uniform(10, 100, num_constituents)

# Helper to calculate spread of constituents in image
def calc_spread(xs, ys):
    return np.mean(np.sqrt(xs**2 + ys**2))

# Test with different gamma values
gammas = [1.2, 2.0, 5.0, 10.0]
spreads = []

print("\n----- Testing Effect of Boost Parameter (gamma) -----")
for gamma_B in gammas:
    mB = 1.0
    EB = gamma_B * mB
    
    print(f"\n--- Testing with gamma = {gamma_B} ---")
    result = gram_schmidt_transform(etas, phis, pts, mB, EB)
    
    # Get coordinates and compute spread
    xs, ys = result["x"], result["y"]
    spread = calc_spread(xs, ys)
    spreads.append(spread)
    
    # Print some diagnostic information
    print(f"Mean X coordinate: {np.mean(xs):.6f}, stddev: {np.std(xs):.6f}")
    print(f"Mean Y coordinate: {np.mean(ys):.6f}, stddev: {np.std(ys):.6f}")
    print(f"Mean radial distance from origin: {spread:.6f}")
    
    # Calculate angles between top constituents and axis
    p_norms = np.linalg.norm(result["content"].reshape(-1,1) * np.column_stack((xs, ys)), axis=1)
    top3 = np.argsort(p_norms)[-3:]
    
    print("Top 3 constituent coordinates:")
    for i, idx in enumerate(top3):
        print(f"  Constituent {i+1}: ({xs[idx]:.4f}, {ys[idx]:.4f}), weight={result['content'][idx]:.4f}")
    
# Summarize relationship between gamma and spread
print("\n----- Summary -----")
print("Gamma values:", gammas)
print("Constituent spreads:", spreads)
print("Expected behavior: As gamma increases, spread should DECREASE")
if all(s1 >= s2 for s1, s2 in zip(spreads, spreads[1:])):
    print("✓ Test PASSED: Spread decreases as gamma increases")
else:
    print("✗ Test FAILED: Spread increases or fluctuates as gamma increases")