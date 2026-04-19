"""
grau_vertice.py

Módulo que calcula o grau de todos os vértices do grafo não direcionado

Este arquivo pode ser:
1. Executado diretamente para ver os testes com GRAFO_1 e GRAFO_2.
2. Importado em outros scripts usando:
    from grau_vertice import calcular_grau_vertices
"""
from lista_adjacencia_grafos import construir_lista_adjacencia, exibir_lista_adjacencia
from conversao_matriz_lista import matriz_para_lista

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_grafo
except ImportError:
    print("Erro: Nao foi possivel encontrar 'src/grafo.py'. Certifique-se de manter a estrutura de pastas.")

# ==============================================================================
# FUNÇÃO AUXILIAR
# ==============================================================================

"""
Verifica se a entrada é lista ou matriz
Se for matriz, ela é convertida para uma lista de adjacência para então realizar o cálculo
Pois é mais eficiente utilizando a lista de adjacência

Entradas:
    grafo (dict): dicionário que armazena a estrutura de matriz ou de lista

Saída:
    grafo (dict): lista de adjacência estruturada com a lista e os vértices ordenados
"""
def verificacao_lista_ou_matriz(grafo):
    # Verifica se é Matriz de Adjacencia procurando a chave 'matriz' no dicionário
    if isinstance(grafo, dict) and 'matriz' in grafo:
        print("Convertendo a Matriz de Adjacência para Lista de Adjacência e realizando a busca em largura...")
        grafo = matriz_para_lista(grafo)
    
    # Verifica se é uma Lista de Adjacência Estruturada procurando a chave 'lista' no dicionário
    if isinstance(grafo, dict) and 'lista' in grafo:        
        return grafo
        
    else:
        raise ValueError("Estrutura de grafo inválida, a busca não poderá ser realizada!")
    
    return {}

# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

"""
Calcula o grau de cada vértice a partir do grafo

Entrada:
    grafo (dict): grafo que pode estar representado como lista ou matriz de adjacência
Saída:
    representacao_grau (dict): Dicionário contendo a lista de graus e os vértices ordenados
"""
def calcular_grau_vertices(grafo):
    grafo = verificacao_lista_ou_matriz(grafo)
    graus = {}

    lista_adj = grafo['lista']  # Acessa o dicionário de adjacência real
    vertices_ordenados = grafo['vertices']
    
    # Cálcula a quantidade de vizinhos que o vértice possui e coloca na lista de graus
    for vertice in vertices_ordenados:
        vizinhos = lista_adj.get(vertice, [])
        graus[vertice] = len(vizinhos)
        
    representacao_grau = {
        'graus': graus,
        'vertices': vertices_ordenados
    }
    
    return representacao_grau

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

"""
Exibe a quantidade de graus que cada vértice possui

Entradas:
    nome_grafo (str): nome do arquivo .txt que originou o grafo
    estrutura_graus (dict): dicionário que armazena o valor dos graus e os vertices ordenados
"""
def exibir_grau_vertices(nome_grafo, estrutura_graus):
    graus = estrutura_graus['graus']
    vertices = estrutura_graus['vertices']

    print(f"\n{'=' * 40}")
    print(f" Grau dos Vértices: {nome_grafo}")
    print(f"{'=' * 40}")
    print(f"{'Vértice':<15} | {'Grau':<10}")
    print("-" * 40)

    for v in vertices:
        print(f"{v:<15} | {graus[v]:<10}")
    
    print(f"{'=' * 40}")

# ==============================================================================
# EXECUÇÃO DE TESTE
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

    for arquivo in arquivos_teste:
        path = os.path.join(base, arquivo)
        
        if os.path.exists(path):
            # Carrega o grafo
            grafo = ler_grafo(path)

            dados_estruturados = construir_lista_adjacencia(grafo)
            
            # Calcula os graus usando a função de calcular os graus
            dados_graus = calcular_grau_vertices(dados_estruturados)
            
            # Exibe formatado
            exibir_grau_vertices(arquivo.replace('.txt', ''), dados_graus)
        else:
            print(f"\nArquivo não encontrado: {path}")

    print(f"\n{'=' * 70}\n")