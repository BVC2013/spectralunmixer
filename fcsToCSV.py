import os
import pandas as pd

def fcsToCSV(filepath, csvpath=None):
    """
    Converts an FCS file to CSV format and returns the CSV path.
    Uses the 'FlowCal' package for robust FCS parsing.
    Saves CSVs in data/fluorochromesCSV by default.
    """
    try:
        import FlowCal
    except ImportError:
        raise ImportError("FlowCal is required. Install with 'pip install FlowCal'.")
    # Set default output directory
    output_dir = os.path.join('data', 'fluorochromesCSV')
    os.makedirs(output_dir, exist_ok=True)
    if csvpath is None:
        base = os.path.splitext(os.path.basename(filepath))[0]
        csvpath = os.path.join(output_dir, base + '.csv')
    data = FlowCal.io.FCSData(filepath)
    df = pd.DataFrame(data, columns=data.channels)
    df.to_csv(csvpath, index=False)
    return csvpath