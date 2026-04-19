"""
07.py
-----------------------------
IMPLEMENTAÇÃO 07 — Função que determina o número total de vértices

Determina o número total de vértices de um Grafo ou Dígrafo a partir:
  1. Do valor declarado na primeira linha do arquivo, E
  2. Da contagem real dos vértices presentes nas arestas/arcos.

Ambos os valores são exibidos, pois podem divergir (ex.: vértice isolado
declarado mas sem nenhuma aresta listada, ou vértice extra aparecendo
nas arestas mas não contado na primeira linha).

Grafos avaliados nesta implementação: GRAFO_1 e GRAFO_2
"""

import sys
import os

# Adiciona a pasta 'src' ao caminho de busca de módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grafo import ler_grafo


# ==============================================================================
# FUNÇÃO PRINCIPAL DA IMPLEMENTAÇÃO
# ==============================================================================

def contar_vertices(grafo):
    """
    Determina o número total de vértices de um grafo.

    A contagem real é feita sobre os vértices efetivamente presentes
    na lista de adjacência (construída a partir das arestas do arquivo).
    O número declarado na primeira linha do arquivo também é retornado
    para fins de comparação e validação.

    Entrada:
        grafo (Grafo | Digrafo): objeto de grafo já lido/construído

    Saída:
        dict com as chaves:
            'declarado' (int): número informado na 1ª linha do arquivo
            'real'      (int): número de vértices encontrados nas arestas
            'vertices'  (list): lista dos vértices reais
    """
    vertices_reais = grafo.obter_vertices()   # lista de vértices da adjacência
    quantidade_real = len(vertices_reais)     # contagem dos vértices reais

    return {
        'declarado': grafo.num_vertices_declarado,
        'real':      quantidade_real,
        'vertices':  sorted(vertices_reais, key=str)  # ordenados para legibilidade
    }


def exibir_resultado(nome_grafo, resultado):
    """
    Exibe formatado o resultado da contagem de vértices.

    Entrada:
        nome_grafo (str): rótulo do grafo (ex.: 'GRAFO_1')
        resultado  (dict): dicionário retornado por contar_vertices()

    Saída:
        Impressão no console (nenhum retorno)
    """
    print(f"\n{'=' * 50}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Vértices declarados (1ª linha do arquivo): {resultado['declarado']}")
    print(f"  Vértices encontrados nas arestas:          {resultado['real']}")
    print(f"  Lista de vértices: {resultado['vertices']}")

    # Alerta se houver divergência entre declarado e real
    if resultado['declarado'] != resultado['real']:
        diff = resultado['declarado'] - resultado['real']
        if diff > 0:
            print(f"  ⚠ ATENÇÃO: {diff} vértice(s) declarado(s) sem arestas (isolado(s)).")
        else:
            print(f"  ⚠ ATENÇÃO: {abs(diff)} vértice(s) extra(s) nas arestas além do declarado.")
    else:
        print(f"  ✔ Declarado e contagem real coincidem.")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

if __name__ == '__main__':
    # Caminho base para os arquivos de dados
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # -------------------------------------------------------
    # GRAFO 1
    # -------------------------------------------------------
    caminho_g1 = os.path.join(base, 'GRAFO_1.txt')
    grafo1 = ler_grafo(caminho_g1)
    resultado1 = contar_vertices(grafo1)
    exibir_resultado('GRAFO_1', resultado1)

    # -------------------------------------------------------
    # GRAFO 2
    # -------------------------------------------------------
    caminho_g2 = os.path.join(base, 'GRAFO_2.txt')
    grafo2 = ler_grafo(caminho_g2)
    resultado2 = contar_vertices(grafo2)
    exibir_resultado('GRAFO_2', resultado2)

    print(f"\n{'=' * 50}\n")