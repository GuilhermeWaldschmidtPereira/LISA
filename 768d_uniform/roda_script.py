import numpy as np
import os
import glob
import shutil
import subprocess
import pandas as pd

dict_ = {
    'sigma': [],
    'T_each_dim': [],
    'n_picewise_models': [],
    'page_size': [],
    'tau': [],
    'status': [],
}

for sigma in range (1, 1024):
    for T_each_dim in range (1, 1024):
        for n_picewise_models in range(1,1024):
            for page_size in range(1, 1024):
                for tau in range(1, 1024):
                    dict_['sigma'].append(sigma)
                    dict_['T_each_dim'].append(T_each_dim)
                    dict_['n_picewise_models'].append(n_picewise_models)
                    dict_['page_size'].append(page_size)
                    dict_['tau'].append(tau)

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
                        
                        

                    string_config = f"""
import errno
import os
import sys
sys.path.append("../../../")
from src.utils import FileViewer


class Config(object):

    class __Singleton(object):

        def __init__(self):

            self.data_dim = 768  # The dimension of spatial data   
            self.sigma = {sigma}
            self.max_value = 10000  # Valor máximo
            self.T_each_dim = {T_each_dim}  # Número de partições por dimensão
            self.n_piecewise_models = {n_picewise_models}  # Número de modelos de regressão por partes
            self.eta = 0.01  # Taxa de aprendizado para otimização
            self.page_size = {page_size}   # Tamanho da página (elementos por página)
            self.min_value = 0  # Valor mínimo
            self.lr = 1e-1  # Taxa de aprendizado
            self.tau = {tau}   # Número de nós em cada dimensão

            data_name = str(self.data_dim) + 'd_uniform'
            self.home_dir = os.path.join(os.path.expanduser("~"), os.path.join('workspace/LISA', data_name))
            self.models_dir = os.path.join(self.home_dir, 'models')
            self.data_dir = os.path.join(self.home_dir, 'data')
            # self.logs_dir = os.path.join(self.home_dir, logs_dir)
            FileViewer.detect_and_create_dir(self.home_dir)
            FileViewer.detect_and_create_dir(self.models_dir)
            FileViewer.detect_and_create_dir(self.data_dir)
            # FileViewer.detect_and_create_dir(self.logs_dir)


            self.query_range_path = os.path.join(self.data_dir, data_name + "_query_ranges.qr")
            self.static_data_name = data_name + "_data_0.npy"  # static data path
            self.data_to_insert_name = data_name + "_data_2.npy"  # data to insert
            self.data_to_delete_name = data_name + "_data_3.npy"  # data to delete
            self.cell_params_path = "cell_params.npy"

            # print '---------Config is initilized----------'

    instance = None

    def __new__(cls):
        if not Config.instance:
            Config.instance = Config.__Singleton()
        return Config.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)

                    """

                    with open('../src/utils/core/config.py', 'w', encoding='utf-8') as file:
                        file.write(string_config)
                    print("Arquivo salvo com sucesso!")


                    result = subprocess.run(["python3", "../src/main.py"], capture_output=True, text=True)
                    print("Saída padrão:", result.stdout)
                    print("Erro padrão:", result.stderr)
                    
                    if result.stderr:
                        dict_['status'].append("Erro")

                    else:   
                        print("Execução concluída com sucesso!")
                        dict_['status'].append("Sucesso")
                        

                    df = pd.DataFrame(dict_)
                    df.to_csv('results.csv', index=False)