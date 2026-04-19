"""
conexo_11.py
Módulo que verifica se um grafo não direcionado é conexo utilizando Busca em Largura (BFS).
"""

# Importação centralizada: quando a main2.py roda, ela encontra este caminho
from implementacoes.busca_largura import mapear_busca_largura

def eh_conexo(grafo_estruturado):
    """
    Verifica se o grafo é conexo.
    
    Entrada:
        grafo_estruturado (dict): dicionário com 'lista' e 'vertices'
    Saída:
        tuple: (conexo (bool), nao_visitados (list))
    """
    vertices = grafo_estruturado['vertices']

    # Verifica se o grafo possui vértices
    if not vertices:
        return True, []

    # Definição do vertice inicial para a busca
    vertice_inicial = vertices[0]
    
    # Realizamos a BFS para conseguir a ordem de visitas
    ordem_visitas, _ = mapear_busca_largura(grafo_estruturado, vertice_inicial)
    
    # Caso a busca retorne erro ou nada
    if ordem_visitas is None:
        return False, vertices

    vertices_visitados = set(ordem_visitas)
    todos_vertices = set(vertices)
    
    # Se a quantidade de visitados for igual ao total de vértices, o grafo é conexo
    conexo = (len(vertices_visitados) == len(todos_vertices))
    nao_visitados = list(todos_vertices - vertices_visitados)
    
    return conexo, nao_visitados