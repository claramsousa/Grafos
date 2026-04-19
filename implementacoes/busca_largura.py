"""
busca_largura.py
Módulo de representação de Busca em Largura em grafos não direcionados.
"""

# Importações corrigidas para funcionar dentro do pacote 'implementacoes'
from implementacoes.lista_adjacencia_grafos import construir_lista_adjacencia
from implementacoes.conversao_matriz_lista import matriz_para_lista

def verificacao_lista_ou_matriz(grafo, vertice_inicial):
    """
    Garante que o grafo esteja no formato de lista de adjacência para a busca.
    """
    if isinstance(grafo, dict) and 'matriz' in grafo:
        print("Convertendo a Matriz de Adjacência para Lista de Adjacência...")
        grafo = matriz_para_lista(grafo)
    
    if isinstance(grafo, dict) and 'lista' in grafo:
        if vertice_inicial not in grafo['lista']:
            print(f"\nErro: O vértice inicial '{vertice_inicial}' não pertence ao grafo!")
            return {}
        return grafo
    else:
        raise ValueError("Estrutura de grafo inválida para realizar a busca!")

def mapear_busca_largura(grafo, vertice_inicial):
    """
    Realiza a busca em largura (BFS) e mapeia ordens e predecessores.
    """
    grafo = verificacao_lista_ou_matriz(grafo, vertice_inicial)
    if not grafo:
        return None, None

    lista_adj = grafo['lista']
    ordem_visitas = []
    predecessores = {vertice_inicial: None}
    conhecidos = {vertice_inicial}
    
    # FIFO (Queue) para exploração
    fila = [vertice_inicial]
    topo = 0
    
    while topo < len(fila):
        vertice_atual = fila[topo]
        topo += 1
        ordem_visitas.append(vertice_atual)
        
        for vizinho in lista_adj.get(vertice_atual, []):
            if vizinho not in conhecidos:
                conhecidos.add(vizinho)
                predecessores[vizinho] = vertice_atual
                fila.append(vizinho)
                
    return ordem_visitas, predecessores

def exibir_resultado_bfs(nome_arquivo, vertice_inicial, ordem_visitas, predecessores):
    """
    Exibe os resultados da BFS de forma estruturada.
    """
    if ordem_visitas is None:
        return

    print(f"\n{'='*50}")
    print(f" BUSCA EM LARGURA - ARQUIVO: {nome_arquivo}")
    print(f" Vértice Inicial: {vertice_inicial}")
    print(f"{'='*50}")
    
    print(f"Ordem de Visita: {' -> '.join(map(str, ordem_visitas))}")
    print("\nPredecessores (Árvore de Busca):")
    
    for v in ordem_visitas:
        pai = predecessores[v]
        print(f"  Vértice {v} | Predecessor: {pai if pai is not None else 'Nível Raiz'}")
    
    print(f"{'='*50}\n")