from fluorochrome import fluorochrome
from concatFile import concatFile
from createCompMatrix import createCompMatrix
from fcsToCSV import fcsToCSV
from dfToCSV import dfToCSV
from applyCompMatrix import applyCompMatrix
import os

# Main file
# Step one: import fluorochromes from directory (files which carry the spectral data for each reagent)
# Step two: convert FCS to CSV if needed, create the fluorochrome class with the CSV filepath
# Step three: create the concatFile class with the fluorochromes
# Step four: create the compensation matrices from the concatFile object
# Step five: save all relevant matrices to CSV
# Step six: apply compensation matrices and save compensated data

fluorochromes = []
fluorochrome_dir = 'data/fluorochromes'
csv_dir = 'data/fluorochromesCSV'
os.makedirs(csv_dir, exist_ok=True)

for filename in os.listdir(fluorochrome_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(fluorochrome_dir, filename)
        fc = fluorochrome(filepath)
        fluorochromes.append(fc)
        print(filename + " loaded as CSV.")
    elif filename.endswith('.fcs'):
        filepath = os.path.join(fluorochrome_dir, filename)
        csvpath = fcsToCSV(filepath)  # This will save to data/fluorochromesCSV
        fc = fluorochrome(csvpath)
        fluorochromes.append(fc)
        print(filename + " converted to CSV and loaded.")

concatfile = concatFile(fluorochromes)
print("Successfully produced concatFile")

# Create and store the linear compensation matrix
comp_matrix = createCompMatrix(concatfile)
concatfile.compensationMatrix = comp_matrix
print("Successfully created linear compensation matrix")

# Save all relevant matrices to CSV
print("Saving all matrices to CSV...")
dfToCSV(concatfile, outdir='data/results', prefix='spectral')
print("All matrices saved to data/results/")

# Apply linear compensation matrix and save compensated data
print("Applying linear compensation matrix...")
applyCompMatrix(concatfile, concatfile.compensationMatrix, outdir='data/results', prefix='comped_linear')
print("Linear compensated data saved.")

# Apply Poisson compensation matrix and save compensated data (if available)
if hasattr(concatfile, 'poissonCompMatrix') and concatfile.poissonCompMatrix is not None:
    print("Applying Poisson compensation matrix...")
    applyCompMatrix(concatfile, concatfile.poissonCompMatrix, outdir='data/results', prefix='comped_poisson')
    print("Poisson compensated data saved.")
else:
    print("No Poisson compensation matrix available.")
