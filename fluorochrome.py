from fcsToCSV import fcsToCSV
from CSVToDf import CSVToDf
import os
import pandas as pd

class fluorochrome:
    def __init__(self, filepath):
        self.filepath = filepath
        self.isPrimary = False
        self.uncompData = pd.DataFrame()
        self.preCompedData = pd.DataFrame()
        self.metadata = pd.DataFrame()
        self.instruCompData = pd.DataFrame()
        self.load_data()

    def load_data(self):
        # If FCS file, convert to CSV first
        if self.filepath.lower().endswith('.fcs'):
            csv_path = self.filepath.replace('.fcs', '.csv')
            fcsToCSV(self.filepath, csv_path)
            df = CSVToDf(csv_path)
        elif self.filepath.lower().endswith('.csv'):
            df = CSVToDf(self.filepath)
        else:
            raise ValueError('Unsupported file type for fluorochrome')
        # Assume df is a DataFrame or convertible to one
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame(df)
        # preCompedData is all the CSV data
        self.preCompedData = df.copy()
        # Metadata: columns with 'meta', 'info', 'fsc', 'ssc', or 'time' in the name
        meta_cols = [col for col in df.columns if any(x in col.lower() for x in ['meta', 'info', 'fsc', 'ssc', 'time'])]
        self.metadata = df[meta_cols] if meta_cols else pd.DataFrame()
        # Instrument compensation data: columns with 'spectral' in the name
        instru_cols = [col for col in df.columns if 'spectral' in col.lower()]
        self.instruCompData = df[instru_cols] if instru_cols else pd.DataFrame()
        # Remove instruCompData columns from preCompedData
        if instru_cols:
            self.preCompedData.drop(columns=instru_cols, inplace=True)
        # uncompData is always empty, to be set later
        self.uncompData = pd.DataFrame()
