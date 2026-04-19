"""
grau_vertice.py
Módulo para cálculo do grau de vértices em grafos não-dirigidos.
"""

from implementacoes.lista_adjacencia_grafos import construir_lista_adjacencia
from implementacoes.conversao_matriz_lista import matriz_para_lista

def verificacao_lista_ou_matriz(grafo):
    """
    Verifica se a entrada é lista ou matriz
    Se for matriz, ela é convertida para uma lista de adjacência para então realizar o cálculo
    Pois é mais eficiente utilizando a lista de adjacência
    
    Entradas:
        grafo (dict): dicionário que armazena a estrutura de matriz ou de lista
    
    Saída:
        grafo (dict): lista de adjacência estruturada com a lista e os vértices ordenados
    """
    if isinstance(grafo, dict) and 'matriz' in grafo:
        print("Convertendo a Matriz de Adjacência para Lista para cálculo de graus...")
        grafo = matriz_para_lista(grafo)
    
    if isinstance(grafo, dict) and 'lista' in grafo:        
        return grafo
    else:
        raise ValueError("Estrutura de grafo inválida para o cálculo de graus!")

def calcular_grau_vertices(grafo):
    """
    Calcula o grau de cada vértice a partir do grafo
    
    Entrada:
        grafo (dict): grafo que pode estar representado como lista ou matriz de adjacência
    Saída:
        representacao_grau (dict): Dicionário contendo a lista de graus e os vértices ordenados
    """
    grafo = verificacao_lista_ou_matriz(grafo)
    graus = {}

    lista_adj = grafo['lista']
    vertices_ordenados = grafo['vertices']
    
    # O grau é a contagem de vizinhos na lista
    for vertice in vertices_ordenados:
        vizinhos = lista_adj.get(vertice, [])
        graus[vertice] = len(vizinhos)
        
    return {
        'graus': graus,
        'vertices': vertices_ordenados
    }

def exibir_grau_vertices(nome_grafo, estrutura_graus):
    """
    Exibe a quantidade de graus que cada vértice possui
    
    Entradas:
        nome_grafo (str): nome do arquivo .txt que originou o grafo
        estrutura_graus (dict): dicionário que armazena o valor dos graus e os vertices ordenados
    """
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
