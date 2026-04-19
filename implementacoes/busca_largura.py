"""
busca_largura.py

Módulo de representação de Busca em Largura em grafos não direcionados.

Este arquivo pode ser:
1. Executado diretamente para ver os testes com GRAFO_1 e GRAFO_2.
2. Importado em outros scripts usando:
    from busca_largura import mapear_busca_largura
"""

import sys
import os
from lista_adjacencia_grafos import construir_lista_adjacencia
from conversao_matriz_lista import matriz_para_lista

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
Se for matriz, ela é convertida para uma lista de adjacência para então realizar a busca
Pois a busca em largura utilizando lista de adjacência é mais eficiente

Entradas:
    grafo (dict): dicionário que armazena as estruturas de matriz ou de lista
    vertice_inicial (str): vértice de onde a busca em largura partirá

Saída:
    grafo (dict): lista de adjacência estruturada com a lista e os vértices ordenados
"""
def verificacao_lista_ou_matriz(grafo, vertice_inicial):
    # Verifica se é Matriz de Adjacencia procurando a chave 'matriz' no dicionário e transforma em lista de adjacência
    if isinstance(grafo, dict) and 'matriz' in grafo:
        print("Convertendo a Matriz de Adjacência para Lista de Adjacência e realizando a busca em largura...")
        grafo = matriz_para_lista(grafo)
    
    # Verifica se é uma Lista de Adjacência Estruturada procurando a chave 'lista' no dicionário
    if isinstance(grafo, dict) and 'lista' in grafo:

        # Verifica se o vértice inicial pertence ao grafo
        if vertice_inicial not in grafo['lista']:
            print(f"\nErro: O vértice inicial '{vertice_inicial}' não pertence ao grafo!")
            return {}
        
        return grafo
        
    else:
        raise ValueError("Estrutura de grafo inválida, a busca não poderá ser realizada!")
    
    return {}

# ==============================================================================
# FUNÇÃO PRINCIPAL 
# ==============================================================================

"""
Realiza a busca em largura no grafo não direcionado

Atributos:
    lista_adj (dict): armazena o dicionário com a lista de adjacência, as chaves são os vértices e os valores seus vizinhos
    conhecidos

Entradas:
    grafo: grafo não direcionado que pode estar representado como lista ou matriz
    vertice_inicial (str): vértice onde a busca inicia

Saída:
    ordem_visitas (list): lista de todos os vértices visitados na BSF
    predecessores (list): lista de predecessores na busca em largura
"""   
def mapear_busca_largura(grafo, vertice_inicial):

    grafo = verificacao_lista_ou_matriz(grafo, vertice_inicial)

    lista_adj = grafo['lista']
    ordem_visitas = []
    predecessores = {vertice_inicial: None}
    conhecidos = {vertice_inicial}
    
    # FIFO que será usado para mapear os vértices já explorados ou não
    fila = [vertice_inicial]
    topo = 0
    
    # Loop feito até explorar todos os vértices possíveis
    while topo < len(fila):
        vertice_atual = fila[topo]
        topo += 1
        ordem_visitas.append(vertice_atual)
        
        # Adiciona cada vizinho ainda não visitado à fila, à lista de conhecidos e marca o vértice atual como predecessor dele
        for vizinho in lista_adj.get(vertice_atual, []):
            if vizinho not in conhecidos:
                conhecidos.add(vizinho)
                predecessores[vizinho] = vertice_atual
                fila.append(vizinho)
                
    return ordem_visitas, predecessores

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================
"""
Exibe o vértice inicial, a ordem de visitas e os predecessores da busca em largura

Entradas:
    nome_arquivo (str): nome do arquivo .txt que originou o grafo
    vertice_inicial (str): vértice onde a busca inicia
    ordem_visitas (list): lista de todos os vértices visitados na BSF em ordem de visita
    predecessores (list): lista de predecessores na busca em largura na ordem da ordem de visitas
"""  
def exibir_resultado_bfs(nome_arquivo, vertice_inicial, ordem_visitas, predecessores):
    if ordem_visitas is None:
        print(f"\n{'!'*50}")
        print(f"Não foi possível exibir a BFS do arquivo {nome_arquivo}, pois a busca retornou vazia!")
        print(f"{'!'*50}\n")
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

# ==============================================================================
# EXECUÇÃO DE TESTE
# ==============================================================================

if __name__ == '__main__':
    base_dados = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    arquivos_para_teste = ['GRAFO_1.txt', 'GRAFO_3.txt']
    
    # Vamos testar iniciando sempre pelo primeiro vértice que aparecer no arquivo
    for arquivo in arquivos_para_teste:
        caminho = os.path.join(base_dados, arquivo)
        
        if os.path.exists(caminho):
            grafo = ler_grafo(caminho)
            
            dados_estruturados = construir_lista_adjacencia(grafo)
            
            # Definição do vértice inicial, pode alterar o vértice inicial mudando o índice
            vertice_start = dados_estruturados['vertices'][0]
            
            # Execução da BFS
            ordem, pais = mapear_busca_largura(dados_estruturados, vertice_start)
            
            # Exibição
            exibir_resultado_bfs(arquivo, vertice_start, ordem, pais)
        else:
            print(f"Arquivo não encontrado: {caminho}")