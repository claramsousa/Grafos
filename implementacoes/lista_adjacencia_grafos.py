"""
lista_adjacencia_grafos.py
Módulo para construir e exibir a lista de adjacência de um grafo.
"""

def construir_lista_adjacencia(grafo):
    """
    Extrai a representação da lista de adjacência do objeto Grafo para construí-lo de maneira ordenada.

    Entrada:
        grafo: objeto Grafo
    Saída:
        dict: dicionário que armazena a lista de adjacência e os vértices ordenados
    """
    # Ordena as chaves (vértices) do grafo
    chave_ord = lambda v: (0, int(v)) if str(v).isdigit() else (1, str(v))
    vertices_ordenados = sorted(grafo.obter_vertices(), key=chave_ord)
    
    # Monta a lista de adjacência ordenando os vizinhos de cada vértice
    lista_pronta = {}
    for v in vertices_ordenados:
        vizinhos = grafo.adjacencia.get(v, [])
        lista_pronta[v] = sorted(vizinhos, key=chave_ord)
        
    return {
        'lista': lista_pronta,
        'vertices': vertices_ordenados
    }

def exibir_lista_adjacencia(nome_grafo, estrutura_lista):
    """
    Exibe a lista de adjacência com a representação estrutural V -> V1 -> V2.

    Entradas:
        nome_grafo (str): nome para identificação no console
        estrutura_lista (dict): retorno da função construir_lista_adjacencia
    """
    lista = estrutura_lista['lista']

    print(f"\n{'=' * 40}")
    print(f" Lista de Adjacência: {nome_grafo}")
    print(f"{'=' * 40}")

    for v in estrutura_lista['vertices']:
        vizinhos = lista[v]
        
        if vizinhos:
            str_vizinhos = " -> ".join(map(str, vizinhos))
            print(f"{v} -> {str_vizinhos}")
        else:
            # Vértice isolado
            print(f"{v}")