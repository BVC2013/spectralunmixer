import pandas as pd

def CSVToDf(rpath):
    """
    Reads a CSV file from the given path and returns a pandas DataFrame.
    """
    return pd.read_csv(rpath)