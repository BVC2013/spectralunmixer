import os
import pandas as pd
import numpy as np

def applyCompMatrix(concatfile, comp_matrix, outdir='data/results', prefix='comped'):
    """
    Applies the given compensation matrix (poisson, linear, wls, etc) to all fluorochromes in the concatFile object.
    Saves the compensated data as CSV files in the specified directory.
    """
    os.makedirs(outdir, exist_ok=True)
    comped_data_list = []
    for idx, fc in enumerate(concatfile.fluorochromes):
        data = fc.preCompedData if hasattr(fc, 'preCompedData') else None
        if data is not None:
            # Ensure data and comp_matrix are DataFrames and have matching columns
            if not isinstance(data, pd.DataFrame):
                data = pd.DataFrame(data)
            if hasattr(comp_matrix, 'values'):
                comp = comp_matrix.values
            else:
                comp = np.array(comp_matrix)
            try:
                # Apply compensation: matrix multiplication
                comped = np.dot(data.values, comp.T) if comp.shape[0] == data.shape[1] else np.dot(data.values, comp)
                comped_df = pd.DataFrame(comped, columns=comp_matrix.index if comp_matrix.shape[0] == data.shape[1] else comp_matrix.columns)
                comped_data_list.append(comped_df)
                # Save each compensated fluorochrome to CSV
                outpath = os.path.join(outdir, f"{prefix}_fluorochrome_{idx}.csv")
                comped_df.to_csv(outpath, index=False)
            except Exception as e:
                print(f"Warning: Could not apply compensation to fluorochrome {idx}: {e}")
    return comped_data_list