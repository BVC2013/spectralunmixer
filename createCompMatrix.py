import numpy as np
import pandas as pd

def createCompMatrix(concatfile):
    """
    Takes a concatFile object, inverts its spillover matrix, stores the compensation matrix in the object, and returns it as a DataFrame.
    """
    spill = concatfile.spilloverMatrix
    if not isinstance(spill, pd.DataFrame):
        raise ValueError("Spillover matrix must be a pandas DataFrame.")
    comp_matrix = pd.DataFrame(np.linalg.pinv(spill.values), index=spill.columns, columns=spill.index)
    concatfile.compensationMatrix = comp_matrix
    return comp_matrix
