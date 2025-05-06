import numpy as np
import matplotlib.pyplot as plt

# Função para carregar os dados do txt
def carregar_dados(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        linhas = f.readlines()
    dados = np.array([list(map(float, linha.strip().split(','))) for linha in linhas])
    return dados

# Implementação simples do algoritmo K-Means
def kmeans(dados, k, max_iter=100, tol=1e-4):
    n_amostras, n_features = dados.shape
    indices = np.random.choice(n_amostras, k, replace=False)
    centroides = dados[indices]

    for iteracao in range(max_iter):
        # Atribuir cada ponto ao centróide mais próximo
        distancias = np.linalg.norm(dados[:, np.newaxis] - centroides, axis=2)
        grupos = np.argmin(distancias, axis=1)

        # Atualizar os centróides
        novo_centroides = np.array([dados[grupos == i].mean(axis=0) if np.any(grupos == i) else centroides[i] for i in range(k)])
        
        # Verificar convergência
        if np.all(np.linalg.norm(centroides - novo_centroides, axis=1) < tol):
            break

        centroides = novo_centroides

    return centroides, grupos

# Função para calcular a inércia (soma dos quadrados das distâncias)
def compute_inertia(dados, centroides, grupos):
    inertia = 0.0
    for i, centroide in enumerate(centroides):
        diff = dados[grupos == i] - centroide
        inertia += np.sum(diff ** 2)
    return inertia

# Carregar os dados
caminho = "768d_uniform\data_0.txt"  # Substitua pelo caminho do seu arquivo
dados = carregar_dados(caminho)

# Variação de k para o método do joelho
K_values = range(1, 30)
inertia_values = []

for k in K_values:
    centroides, grupos = kmeans(dados, k)
    inertia = compute_inertia(dados, centroides, grupos)
    inertia_values.append(inertia)
    print(f"k = {k} -> Inércia: {inertia:.4f}")

# Plot do método do joelho
plt.figure()
plt.plot(K_values, inertia_values, marker='o')
plt.xlabel('Número de clusters (k)')
plt.ylabel('Inércia')
plt.title('Método do Joelho para determinar o k ótimo')
plt.grid(True)
plt.show()
