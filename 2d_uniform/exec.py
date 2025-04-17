import numpy as np
import os
import glob
import shutil
import subprocess


# Configuração
num_points = 100
for i in range (0,4):
    latitude_values = np.linspace(1000.0, 20000.0, num_points)  # Valores de latitude (entre 10 e 14000)
    longitude_values = np.linspace(400.0, 8000.5, num_points)  # Valores de longitude (entre 20 e 24000.5)

    # Combinar em um array 2D (cada linha contém [latitude, longitude])
    points_2d = np.column_stack((latitude_values, longitude_values, latitude_values, longitude_values))

    # Caminho para salvar o arquivo .npy
    file_path = f"data/2d_uniform_data_{i}.npy"

    # Salvar o array em um arquivo .npy
    np.save(file_path, points_2d)

    print(f"Arquivo salvo em: {file_path}")


def delete_file(filepath):
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
result = subprocess.run(["python3", "../src/main.py"], capture_output=True, text=True)
print("Saída padrão:", result.stdout)
print("Erro padrão:", result.stderr)
if result.stderr:
    print("Erro encontrado:", result.stderr)