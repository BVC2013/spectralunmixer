import os
import pandas as pd

def dfToCSV(concatfile, outdir='data/results', prefix='result'):
    """
    Saves concatFile object's matrices (precomp, spillover, comp, comped) to CSV files in the specified directory.
    """
    os.makedirs(outdir, exist_ok=True)
    # Attempt to extract relevant matrices from concatfile
    matrices = {}
    if hasattr(concatfile, 'preCompedData'):
        matrices['precomp'] = concatfile.preCompedData if isinstance(concatfile.preCompedData, pd.DataFrame) else pd.DataFrame(concatfile.preCompedData)
    if hasattr(concatfile, 'spilloverMatrix'):
        matrices['spillover'] = concatfile.spilloverMatrix if isinstance(concatfile.spilloverMatrix, pd.DataFrame) else pd.DataFrame(concatfile.spilloverMatrix)
    if hasattr(concatfile, 'compensationMatrix'):
        matrices['comp'] = concatfile.compensationMatrix if isinstance(concatfile.compensationMatrix, pd.DataFrame) else pd.DataFrame(concatfile.compensationMatrix)
    if hasattr(concatfile, 'compedData'):
        matrices['comped'] = concatfile.compedData if isinstance(concatfile.compedData, pd.DataFrame) else pd.DataFrame(concatfile.compedData)
    for key, df in matrices.items():
        outpath = os.path.join(outdir, f"{prefix}_{key}.csv")
        df.to_csv(outpath, index=False)