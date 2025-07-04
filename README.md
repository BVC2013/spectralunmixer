# SpectralUnmixer: Spectral Flow Cytometry Data Processing Pipeline

## Overview
A robust, modular workflow for spectral flow cytometry data: import FCS/CSV, create fluorochrome objects, generate spillover and compensation matrices (linear, Poisson, WLS), and batch export results. Designed for reproducibility and compatibility with standard cytometry analysis practices.

---

## 🚀 Step-by-Step Usage

### 1️⃣ Prepare Your Data
- Place all single-stained FCS or CSV files in: `data/fluorochromes/`
- Each file should represent a single fluorochrome/reagent.

### 2️⃣ Install Required Python Packages
```sh
pip install pandas numpy FlowCal
```

### 3️⃣ Run the Main Pipeline
From the project root, run:
```sh
python project.py
```
The script will:
- Convert FCS files to CSV (`data/fluorochromesCSV/`)
- Create fluorochrome objects for each file
- Concatenate and process all fluorochromes
- Generate spillover, linear, Poisson, and WLS compensation matrices
- Save all matrices and compensated data to `data/results/`

### 4️⃣ Output Files
All results are saved in `data/results/`:
- `spectral_precomp.csv` — Pre-compensated data matrix
- `spectral_spillover.csv` — Spillover matrix
- `spectral_comp.csv` — Linear compensation matrix
- `spectral_comped_linear_fluorochrome_X.csv` — Linear compensated data (per fluorochrome)
- `spectral_comped_poisson_fluorochrome_X.csv` — Poisson compensated data (per fluorochrome, if available)
- `spectral_comped_wls_fluorochrome_X.csv` — WLS compensated data (if WLS is integrated)

### 5️⃣ Customization & Advanced Usage
- Use different compensation strategies by importing and calling the relevant matrix creation functions (e.g., `CreateWlsCompMatrix`, `creatPoissonCompMatrix`) in your workflow.
- Add new compensation methods by creating a new script (see `creatPoissonCompMatrix.py` or `CreateWlsCompMatrix.py` for structure).
- For batch processing or integration with other analysis, modify `project.py` as needed.

### 6️⃣ Troubleshooting
- Ensure all dependencies are installed.
- Check that your input files are correctly formatted and placed in `data/fluorochromes/`.
- Review console output for error messages.

---

## 📁 File Structure
| File                        | Purpose                                 |
|-----------------------------|-----------------------------------------|
| `project.py`                | Main workflow script                    |
| `fluorochrome.py`           | Fluorochrome object definition          |
| `concatFile.py`             | Concatenation and matrix storage        |
| `fcsToCSV.py`               | FCS to CSV conversion                   |
| `createSpilloverMatrix.py`  | Spillover matrix generation             |
| `createCompMatrix.py`       | Linear compensation matrix              |
| `creatPoissonCompMatrix.py` | Poisson compensation matrix             |
| `CreateWlsCompMatrix.py`    | WLS compensation matrix                 |
| `applyCompMatrix.py`        | Applies compensation matrices           |
| `dfToCSV.py`                | Exports matrices/dataframes to CSV      |
| `CSVToDf.py`                | Loads CSVs as DataFrames                |

---

## 🧩 Example: Adding a New Compensation Method
1. Create a new script (e.g., `createNewCompMatrix.py`) following the structure of existing matrix scripts.
2. Import and call your function in `project.py` after the `concatFile` object is created.
3. Use `applyCompMatrix` to apply and export the new compensation results.

---

## 📬 Contact
For questions or contributions, please open an issue or pull request on the project repository.
