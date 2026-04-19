"""
conversao_matriz_lista.py
Módulo para conversão cruzada entre representações de Matriz e Lista de Adjacência.
"""

from implementacoes.lista_adjacencia_grafos import construir_lista_adjacencia
from implementacoes.implementacao_02 import construir_matriz_adjacencia, exibir_matriz_adjacencia
from grafo import Grafo

def lista_para_matriz(arquivo, lista_estruturada):
    """
    Constrói uma matriz de adjacência a partir de uma estrutura de lista.
    
    Entrada:
        arquivo (str): nome do arquivo para identificação na exibição
        lista_estruturada (dict): dicionário contendo a lista e vértices
    Saída:
        dict: estrutura de matriz de adjacência
    """
    matriz_adj = Grafo()
    lista_adj = lista_estruturada["lista"]

    # Reconstrói as arestas no novo objeto Grafo
    for v_origem, vizinhos in lista_adj.items():
        for v_destino in vizinhos:
            matriz_adj.adicionar_aresta(v_origem, v_destino)
    
    # Exibe a matriz resultante
    exibir_matriz_adjacencia(arquivo, matriz_adj)
    
    return construir_matriz_adjacencia(matriz_adj)


def matriz_para_lista(estrutura_matriz):
    """
    Converte uma estrutura de Matriz de Adjacência para Lista de Adjacência.
    
    Entrada:
        estrutura_matriz (dict): dicionário contendo matriz e vértices
    Saída:
        dict: estrutura de lista de adjacência
    """
    matriz = estrutura_matriz['matriz']
    vertices = estrutura_matriz['vertices']
    lista_adj = Grafo()
    
    # Percorre a matriz e adiciona arestas onde o valor é 1
    for i, v_origem in enumerate(vertices):
        for j, v_destino in enumerate(vertices):
            if matriz[i][j] == 1:
                lista_adj.adicionar_aresta(v_origem, v_destino)
    
    # Retorna a lista estruturada para ser exibida pela main
    return construir_lista_adjacencia(lista_adj)