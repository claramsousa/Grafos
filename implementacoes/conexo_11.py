"""
conexo_11.py

Módulo que verifica se um grafo não direcionado é conexo ou não
Utiliza a lógica de Busca em Largura (BFS), verificando se todos os vértices estão em ordem_visitas
"""

import sys
import os
from busca_largura import mapear_busca_largura

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
try:
    from grafo import ler_grafo
except ImportError:
    print("Erro: Nao foi possivel encontrar 'src/grafo.py'. Certifique-se de manter a estrutura de pastas.")

# ==============================================================================
# FUNÇÃO PRINCIPAL
# ==============================================================================

"""
Verifica se o grafo é conexo.

Entrada:
    grafo_estruturado (dict): dicionário com 'lista' e 'vertices'
Saída:
    conexo (bool): True se for conexo, False caso contrário.
    não visitados (list): Lista de vértices que não foram alcançados na busca em largura
"""
def eh_conexo(grafo_estruturado):

    vertices = grafo_estruturado['vertices']

    # Verifica se o grafo possui vértices
    if not vertices:
        return True, []

    # Definição do vertice inicial
    vertice_inicial = vertices[0]
    
    # Realizamos a BFS para conseguir a ordem_visitas
    ordem_visitas, _ = mapear_busca_largura(grafo_estruturado, vertice_inicial)
    
    vertices_visitados = set(ordem_visitas)
    todos_vertices = set(vertices)
    
    # Verifica se há a mesma quantidade de vértices visitados e vértices no grafo
    # Se sim, então é conexo
    conexo = (len(vertices_visitados) == len(todos_vertices))
    nao_visitados = list(todos_vertices - vertices_visitados)
    
    return conexo, nao_visitados

# ==============================================================================
# EXECUÇÃO DE TESTE
# ==============================================================================

if __name__ == '__main__':
    from lista_adjacencia_grafos import construir_lista_adjacencia

    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

    for arquivo in arquivos_teste:
        path = os.path.join(base, arquivo)
        if os.path.exists(path):
            g = ler_grafo(path)
            dados_lista = construir_lista_adjacencia(g)
            
            conexo, isolados = eh_conexo(dados_lista)
            
            print(f"\n{'-'*30}")
            print(f"Análise de Conectividade: {arquivo}")
            print(f"{'-'*30}")
            
            if conexo:
                print("Resultado: O grafo é CONEXO.")
            else:
                print("Resultado: O grafo é DESCONEXO.")
                print(f"Vértices não alcançados: {isolados}")