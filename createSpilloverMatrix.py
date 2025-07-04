import sys
import os
import pandas as pd
import numpy as np
import re

# Usage: python createSpilloverMatrix.py <input_dir> OR call main(fluorochromeObjs=...)
def main(input_dir=None, fluorochromeObjs=None):
    output_csv = os.path.join('data', 'spilloverMatrix.csv')
    if fluorochromeObjs is not None:
        # Use the provided array of fluorochrome objects
        fluorochromes = list(fluorochromeObjs)
        files = [getattr(f, 'filepath', f"fluorochrome_{i}") for i, f in enumerate(fluorochromes)]
    else:
        if input_dir is None and len(sys.argv) >= 2:
            input_dir = sys.argv[1]
        if not input_dir:
            print("Usage: python createSpilloverMatrix.py <input_dir>")
            sys.exit(1)
        files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.csv') or f.endswith('.fcs')]
        if not files:
            print(f"No CSV or FCS files found in {input_dir}")
            sys.exit(1)
        from fluorochrome import fluorochrome
        fluorochromes = [fluorochrome(f) for f in files]
    # Use preCompedData for spillover calculation
    spec_calc_mat = {}
    for fc, f in zip(fluorochromes, files):
        df = fc.preCompedData
        if df.empty:
            continue
        medians = df.median(axis=0)
        spec_calc_mat[f] = medians
    if not spec_calc_mat:
        print("No valid data found in fluorochrome objects.")
        sys.exit(1)
    spec_calc_df = pd.DataFrame.from_dict(spec_calc_mat, orient='index')
    single_stain_groups = [spec_calc_df]
    if single_stain_groups[0].shape[0] < 3:
        print("It seems like unmixing of one color is attempted, which is not meaningful.")
        sys.exit(1)
    neg_ctrl_rows = [single_stain_groups[0].index[single_stain_groups[0].sum(axis=1).argmin()]]
    raw_spec_mat_list = []
    for group, neg_row in zip(single_stain_groups, neg_ctrl_rows):
        neg_ctrl = group.loc[neg_row]
        subtracted = group.subtract(neg_ctrl, axis=1)
        raw_spec_mat_list.append(subtracted)
    raw_spec_mat = pd.concat(raw_spec_mat_list, axis=0)
    spec_mat_no_unstain = raw_spec_mat.loc[:, (raw_spec_mat != 0).any(axis=0)]
    def clean_col(col):
        col = re.sub(r'\.csv$', '', col, flags=re.IGNORECASE)
        col = re.sub(r'\.fcs$', '', col, flags=re.IGNORECASE)
        return col.strip('_')
    spec_mat_no_unstain.columns = [clean_col(c) for c in spec_mat_no_unstain.columns]
    autofluo_name = spec_calc_df.sum(axis=1).idxmin()
    print(f"Autofluorescence control automatically selected: {autofluo_name}")
    spec_mat = pd.concat([spec_mat_no_unstain, spec_calc_df.loc[[autofluo_name]].rename(index={autofluo_name: 'Autofluo'})])
    spec_mat_frac = spec_mat.apply(lambda x: x / x.max(), axis=0)
    spec_mat_frac[spec_mat_frac < 0] = 0
    spec_mat_frac.to_csv(output_csv)
    print(f"Spillover matrix saved to {output_csv}")

if __name__ == "__main__":
    main()