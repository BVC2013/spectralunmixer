from CSVToDf import CSVToDf
from createSpilloverMatrix import main as createSpilloverMatrix
from createCompMatrix import createCompMatrix
from applyCompMatrix import applyCompMatrix
from creatPoissonCompMatrix import creatPoissonCompMatrix
import pandas as pd

class concatFile:
    def __init__(self, fluorochromeObjs):
        # Ensure we always have a list of fluorochrome objects
        if fluorochromeObjs is None:
            self.fluorochromes = []
        elif isinstance(fluorochromeObjs, list):
            self.fluorochromes = fluorochromeObjs
        else:
            self.fluorochromes = [fluorochromeObjs]
        self.primary = [f for f in self.fluorochromes if getattr(f, 'isPrimary', False)]
        self.rawMatrix = [f.preCompedData for f in self.fluorochromes]
        # Compute spillover matrix using the files from the fluorochrome objects
        # Save all preCompedData to temp files for compatibility with createSpilloverMatrix
        import tempfile
        import os
        temp_dir = tempfile.mkdtemp()
        temp_files = []
        for idx, f in enumerate(self.fluorochromes):
            temp_path = os.path.join(temp_dir, f"fluorochrome_{idx}.csv")
            f.preCompedData.to_csv(temp_path, index=False)
            temp_files.append(temp_path)
        # Call createSpilloverMatrix with the temp directory
        # This will save the spillover matrix to data/spilloverMatrix.csv
        import sys
        sys_argv_backup = sys.argv
        sys.argv = ['createSpilloverMatrix.py', temp_dir]
        createSpilloverMatrix()
        sys.argv = sys_argv_backup
        # Load the spillover matrix
        self.spilloverMatrix = pd.read_csv('data/spilloverMatrix.csv', index_col=0)
        # Compute and store Poisson compensation matrix
        try:
            self.poissonCompMatrix = creatPoissonCompMatrix(self.fluorochromes, self.spilloverMatrix)
        except Exception as e:
            print(f"Warning: Could not compute Poisson compensation matrix: {e}")
        # Continue with compensation and downstream steps as needed
        # self.compensationMatrix = createCompMatrix(self.spilloverMatrix)
        # self.compVals = applyCompMatrix(self.compensationMatrix)
        # ...
        print("project processed")
