import os
import shutil
from pathlib import Path
import pkg_resources

# Default download location (Desktop)
DEFAULT_DOWNLOAD_LOCATION = Path.home() / "Desktop"

# Mapping of files and their dependent "complete" files
DEPENDENT_FILES = {
    "admission.py": "admission.csv",
    "cluster_algoritm.py": "Daily_minimum_temps.csv",
    "dendogram.py": "iris.csv",
    "k_means.py":"Mall_Customers.csv",
    "LinearRegression.py":"Salary_dataset.csv",
    "spam detection.py":"spam.csv",
    "SVM.py":"Wholesale_customers_data.csv",
}

def list_files():
    """Lists all available files in the package."""
    files_path = pkg_resources.resource_filename(__name__, "files")
    return [f for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, f))]

def download_file(file_name: str, location: str = None):
    """Downloads the specified file and its dependent file (if applicable)."""
    
    # Get the file path inside the package
    source_file_path = pkg_resources.resource_filename(__name__, f"files/{file_name}")

    # Check if file exists
    if not os.path.exists(source_file_path):
        raise FileNotFoundError(f"❌ File '{file_name}' not found in the package.")

    # Set default download location (Desktop)
    destination_path = Path(location) if location else DEFAULT_DOWNLOAD_LOCATION

    # Ensure the directory exists
    os.makedirs(destination_path, exist_ok=True)

    # Copy the main file
    shutil.copy(source_file_path, destination_path / file_name)
    print(f"✅ File '{file_name}' downloaded to: {destination_path}")

    # Check for dependent file
    if file_name in DEPENDENT_FILES:
        dependent_file = DEPENDENT_FILES[file_name]
        dependent_file_path = pkg_resources.resource_filename(__name__, f"files/{dependent_file}")

        if os.path.exists(dependent_file_path):
            shutil.copy(dependent_file_path, destination_path / dependent_file)
            print(f"✅ Dependent file '{dependent_file}' also downloaded.")

