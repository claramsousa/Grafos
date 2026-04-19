import numpy as np
from lista_adjacencia_grafos import construir_lista_adjacencia, exibir_lista_adjacencia
from implementacao_02 import construir_matriz_adjacencia, exibir_matriz_adjacencia

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_grafo, Grafo
except ImportError:
    print("Erro: Nao foi possivel encontrar 'src/grafo.py'. Certifique-se de manter a estrutura de pastas.")

# ==============================================================================
# FUNÇÕES PRNCIPAIS DE CONVERSÃO
# ==============================================================================

"""
Constrói uma matriz de adjacencia a partir de uma lista de adjacencia

Entrada:
    arquivo (str): nome do arquivo de onde pegamos o grafo
    lista_estruturada (dict): lista de adjacencia que será convertida em matriz
Saída:
    matriz_adj (dict): matriz de adjacencia obtida a partir da lista de adjacencia dada
"""
def lista_para_matriz(arquivo, lista_estruturada):
    matriz_adj = Grafo()
    
    # Forma um objeto grafo a partir da lista de adjacência estruturada
    lista_adj = lista_estruturada["lista"]

    for v_origem, vizinhos in lista_adj.items():
        for v_destino in vizinhos:
            # Adiciona a aresta no objeto
            matriz_adj.adicionar_aresta(v_origem, v_destino)
    
    exibir_matriz_adjacencia(arquivo, matriz_adj)
    
    # Retorna a matriz de adjacência
    return construir_matriz_adjacencia(matriz_adj)

"""
Constrói uma lista de adjacencia a partir de uma matriz de adjacencia

Entrada:
    estrutura_matriz (dict): matriz de adjacencia que será convertida em lista
Saída:
    lista_adj (dict): lista de adjacencia obtida a partir da matriz de adjacencia dada
"""

"""Converte Matriz de Incidência para Lista de Adjacência Estruturada."""
def matriz_para_lista(estrutura_matriz):
    
    matriz = estrutura_matriz['matriz']
    vertices = estrutura_matriz['vertices']
    
    # Criamos a lista de adjacência para depois estruturà-la
    lista_adj = Grafo()
    
    # Percorre a matriz de adjacência e adiciona aresta quando o valor for igual a 1
    for i, v_origem in enumerate(vertices):
        for j, v_destino in enumerate(vertices):
            if matriz[i][j] == 1:
                lista_adj.adicionar_aresta(v_origem, v_destino)
    
    # Retorna a lista estruturada
    return construir_lista_adjacencia(lista_adj)

# ==============================================================================
# EXECUÇÃO DE TESTE
# ==============================================================================

if __name__ == '__main__':
    # Caminho para a pasta de dados
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # Arquivos que serão usados no teste
    arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

    for arquivo in arquivos_teste:
        path = os.path.join(base, arquivo)
        
        if os.path.exists(path):
            # Carrega o grafo do arquivo
            g = ler_grafo(path)
            lista_estruturada = construir_lista_adjacencia(g)
            matriz_estruturada = construir_matriz_adjacencia(g)

            # Realiza as conversões
            print("\nConversão de lista para matriz: ")
            matriz_adj = lista_para_matriz(arquivo, lista_estruturada)

            print("\nConversão de matriz para lista: ")
            lista_adj = matriz_para_lista(matriz_estruturada)
            exibir_lista_adjacencia(arquivo, lista_adj)
        else:
            print(f"\nArquivo não encontrado: {path}")

    print(f"\n{'=' * 70}\n")