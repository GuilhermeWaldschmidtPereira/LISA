import numpy as np
import os
import glob
import shutil
import subprocess
import time

def delete_file(filepath):
    # pass
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"Deleted file: {filepath}")
    else:
        print(f"File not found: {filepath}")

def delete_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)
        print(f"Deleted directory: {directory}")
    else:
        print(f"Directory not found: {directory}")

def delete_matching(pattern):
    matches = glob.glob(pattern)
    for match in matches:
        if os.path.isfile(match):
            delete_file(match)
        elif os.path.isdir(match):
            delete_directory(match)

# List of files to delete
files_to_delete = [
    "data/cell_params.npy",
    "data/col_split_idxes.npy",
    "data/one_dim_mappings.npy",
]

# Directories and patterns to delete
dirs_to_delete = [
    "data/lattice",  # Delete all files and folders inside /models
    "data/models/*",  # Delete all files and folders matching /lattice*
    "../models/*",  # Delete all files and folders matching /lattice*
    "models/*"
]

# Delete specific files
for file in files_to_delete:
    delete_file(file)

# Delete directories and patterns
for directory in dirs_to_delete:
    delete_matching(directory)

start_time = time.time()
result = subprocess.run(["python3", "../src/main.py"], capture_output=True, text=True)
end_time = time.time()
execution_time = end_time - start_time
print("Saída padrão:", result.stdout)
print("Erro padrão:", result.stderr)
