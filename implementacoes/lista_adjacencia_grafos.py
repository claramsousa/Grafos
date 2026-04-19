"""
lista_adjacencia_grafos.py

Como a lista de adjacencia já foi implementada como representação padrão na classe Grafos, 
então esse módulo servirá para construir, exibir e testar a lista de adjacência

Este arquivo pode ser:
1. Executado diretamente para ver os testes com GRAFO_1 e GRAFO_2.
2. Importado em outros scripts usando:
    from lista_adjacencia import construir_lista_adjacencia
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_grafo
except ImportError:
    print("Erro: Nao foi possivel encontrar 'src/grafo.py'. Certifique-se de manter a estrutura de pastas.")

# ==============================================================================
# FUNÇÃO DE CONSTRUÇÃO
# ==============================================================================

"""
Extrai a representação da lista de adjacência do objeto Grafo para construi-lo de maneira ordenada

Entrada:
    grafo (dict): dicionário que representa o grafo na estrutura de uma lista de adjacência
Saída:
    representacao_lista (dict): dicionário que armazena a lista de adjacencia e os vértices ordenados
"""
def construir_lista_adjacencia(grafo):
    
    # Ordena as chaves (vértices) do grafo
    chave_ord = lambda v: (0, int(v)) if str(v).isdigit() else (1, str(v))
    vertices_ordenados = sorted(grafo.obter_vertices(), key=chave_ord)
    
    # Monta a lista de adjacencia ordenando os vértices
    lista_pronta = {}
    for v in vertices_ordenados:
        vizinhos = grafo.adjacencia.get(v, [])
        lista_pronta[v] = sorted(vizinhos, key=chave_ord)
        
    representacao_lista = {
        'lista': lista_pronta,
        'vertices': vertices_ordenados
    }
    
    return representacao_lista

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

"""
Exibe a lista de adjacencia com a representação estrutural vista em aula

Entradas:
    nome_grafo (str): nome do arquivo .txt que originou o grafo
    estrutura_lista (dict): dicionário que armazena a lista de adjacencia e os vertices ordenadamente
"""
def exibir_lista_adjacencia(nome_grafo, estrutura_lista):
    lista = estrutura_lista['lista']

    print(f"\n{'=' * 40}")
    print(f" Lista de Adjacência: {nome_grafo}")
    print(f"{'=' * 40}")

    for v in estrutura_lista['vertices']:
        vizinhos = lista[v]
        
        if vizinhos:
            # Formato: V -> V1 -> V2 visto em aula
            str_vizinhos = " -> ".join(map(str, vizinhos))
            print(f"{v} -> {str_vizinhos}")
        else:
            # Vértice isolado (não possui vizinhos)
            print(f"{v}")

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
            
            # Constrói a estrutura de dados
            dados_lista = construir_lista_adjacencia(g)
            
            # Exibe o resultado formatado
            exibir_lista_adjacencia(arquivo.replace('.txt', ''), dados_lista)
        else:
            print(f"\nArquivo não encontrado: {path}")

    print(f"\n{'=' * 70}\n")