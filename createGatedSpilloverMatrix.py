"""
createGatedSpilloverMatrix.py

Usage:
    python createGatedSpilloverMatrix.py <input_dir> <group1> [<group2> ...]

Arguments:
    <input_dir>   Directory containing single-stained and unstained control CSV or FCS files.
    <group1> ...  (Optional) Substrings to group files by sample type (e.g., 'Bead', 'PBMC').
                  If no groups are provided, groups are auto-detected from filename prefixes before the first underscore.

Output:
    The spillover matrix is saved as 'data/spilloverMatrix.csv'.
    The script prints the name of the autofluorescence control automatically selected.

Each file should have columns for all channels (including FSC/SSC/Time if present).
The script performs gating, grouping, negative control subtraction, normalization, and outputs a FlowSpecs-compatible spillover matrix.
"""

import sys
import os
import pandas as pd
import numpy as np
import re
from concatFile import concatFile

def main():
    if len(sys.argv) < 2:
        print("Usage: python createGatedSpilloverMatrix.py <input_dir> <group1> [<group2> ...]")
        sys.exit(1)
    input_dir = sys.argv[1]
    output_csv = os.path.join('data', 'spilloverMatrix.csv')

    # Create a concatFile object from the input directory
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv') or f.endswith('.fcs')]
    if not files:
        print(f"No CSV or FCS files found in {input_dir}")
        sys.exit(1)
    from fluorochrome import fluorochrome
    fluorochromeObjs = [fluorochrome(f) for f in files]
    concat_obj = concatFile(fluorochromeObjs)
    # Save the spillover matrix
    concat_obj.spilloverMatrix.to_csv(output_csv)
    print(f"Spillover matrix saved to {output_csv}")

if __name__ == "__main__":
    main()
