
import errno
import os
import sys
sys.path.append("../../../")
from src.utils import FileViewer


class Config(object):

    class __Singleton(object):

        def __init__(self):

            self.data_dim = 4  # The dimension of spatial data   
            self.sigma = 1
            self.max_value = 0.8  # Valor máximo
            self.T_each_dim = 1  # Número de partições por dimensão
            self.n_piecewise_models = 1  # Número de modelos de regressão por partes
            self.eta = 0.01  # Taxa de aprendizado para otimização
            self.page_size = 1   # Tamanho da página (elementos por página)
            self.min_value = -0.8  # Valor mínimo
            self.lr = 1e-1  # Taxa de aprendizado
            self.tau = 1   # Número de nós em cada dimensão

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

                    