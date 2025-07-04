import numpy as np
import pandas as pd

def creatPoissonCompMatrix(fluorochrome_objs, spillover_matrix):
    """
    Given an array of fluorochrome objects and a spillover matrix,
    compute a Poisson-based compensation matrix.
    Returns a pandas DataFrame with the compensation matrix.
    """
    # Example: Use the mean of each channel for each fluorochrome as the expected value (lambda)
    # and use the spillover matrix to adjust for Poisson noise.
    # This is a placeholder for a more sophisticated Poisson model.
    channel_names = spillover_matrix.columns if hasattr(spillover_matrix, 'columns') else range(spillover_matrix.shape[1])
    n = len(channel_names)
    lambdas = np.zeros((len(fluorochrome_objs), n))
    for i, fc in enumerate(fluorochrome_objs):
        if hasattr(fc, 'preCompedData'):
            data = fc.preCompedData
            if hasattr(data, 'mean'):
                means = np.array(data.mean(axis=0)).flatten()
                if means.shape[0] == n:
                    lambdas[i, :] = means
                else:
                    lambdas[i, :means.shape[0]] = means
    # Poisson compensation: invert the spillover matrix and scale by expected means
    try:
        spillover_inv = np.linalg.pinv(spillover_matrix.values if hasattr(spillover_matrix, 'values') else spillover_matrix)
    except Exception as e:
        raise ValueError(f"Could not invert spillover matrix: {e}")
    poisson_comp = np.dot(lambdas.mean(axis=0), spillover_inv)
    comp_matrix = pd.DataFrame(poisson_comp, index=["poisson_comp"], columns=channel_names)
    return comp_matrix
