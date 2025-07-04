import numpy as np
import pandas as pd

def CreateWlsCompMatrix(fluorochrome_objs, spillover_matrix):
    """
    Given an array of fluorochrome objects and a spillover matrix,
    compute a Weighted Least Squares (WLS) compensation matrix.
    Returns a pandas DataFrame with the compensation matrix.
    """
    # Use the mean and variance of each channel for each fluorochrome as weights
    channel_names = spillover_matrix.columns if hasattr(spillover_matrix, 'columns') else range(spillover_matrix.shape[1])
    n = len(channel_names)
    means = np.zeros((len(fluorochrome_objs), n))
    variances = np.zeros((len(fluorochrome_objs), n))
    for i, fc in enumerate(fluorochrome_objs):
        if hasattr(fc, 'preCompedData'):
            data = fc.preCompedData
            if hasattr(data, 'mean') and hasattr(data, 'var'):
                m = np.array(data.mean(axis=0)).flatten()
                v = np.array(data.var(axis=0)).flatten()
                means[i, :m.shape[0]] = m
                variances[i, :v.shape[0]] = v
    # Avoid division by zero in weights
    weights = 1.0 / (variances + 1e-8)
    # WLS solution: (X^T W X)^-1 X^T W Y
    # Here, X = spillover_matrix, Y = means, W = diag(weights)
    try:
        X = spillover_matrix.values if hasattr(spillover_matrix, 'values') else np.array(spillover_matrix)
        Y = means.mean(axis=0)
        W = np.diag(weights.mean(axis=0))
        XtWX = X.T @ W @ X
        XtWY = X.T @ W @ Y
        wls_comp = np.linalg.solve(XtWX, XtWY)
        comp_matrix = pd.DataFrame([wls_comp], columns=channel_names, index=["wls_comp"])
    except Exception as e:
        raise ValueError(f"Could not compute WLS compensation matrix: {e}")
    return comp_matrix
