"""
08.py
----------------------------
IMPLEMENTAÇÃO 08 — Função que determina o número total de arestas

Determina o número total de arestas de um Grafo não-dirigido.

Em um grafo não-dirigido, a aresta (u, v) e a aresta (v, u) representam
a MESMA conexão. Por isso, a contagem percorre a lista de adjacência
evitando duplicatas — cada par é contado uma única vez.

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

def contar_arestas(grafo):
    """
    Determina o número total de arestas de um grafo não-dirigido.

    Como a lista de adjacência armazena cada aresta duas vezes
    (u → v e v → u), percorremos todos os pares e usamos um conjunto
    de pares já visitados para evitar contagem duplicada.

    Entrada:
        grafo (Grafo): objeto Grafo já lido/construído

    Saída:
        dict com as chaves:
            'total'   (int):  número total de arestas únicas
            'arestas' (list): lista de tuplas (u, v) de cada aresta
    """
    visitados = set()   # armazena pares já contabilizados (como frozenset)
    arestas_unicas = [] # lista das arestas sem repetição

    for u in grafo.adjacencia:
        for v in grafo.adjacencia[u]:
            # frozenset({u, v}) representa o par sem ordem: {a,b} == {b,a}
            par = frozenset([u, v])

            if par not in visitados:
                visitados.add(par)
                arestas_unicas.append((u, v))  # registra aresta única

    return {
        'total':   len(arestas_unicas),
        'arestas': arestas_unicas
    }


def exibir_resultado(nome_grafo, resultado):
    """
    Exibe formatado o resultado da contagem de arestas.

    Entrada:
        nome_grafo (str): rótulo do grafo (ex.: 'GRAFO_1')
        resultado  (dict): dicionário retornado por contar_arestas()

    Saída:
        Impressão no console (nenhum retorno)
    """
    print(f"\n{'=' * 50}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Total de arestas: {resultado['total']}")
    print(f"  Arestas encontradas:")
    for u, v in resultado['arestas']:
        print(f"    ({u}) ——— ({v})")


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
    resultado1 = contar_arestas(grafo1)
    exibir_resultado('GRAFO_1', resultado1)

    # -------------------------------------------------------
    # GRAFO 2
    # -------------------------------------------------------
    caminho_g2 = os.path.join(base, 'GRAFO_2.txt')
    grafo2 = ler_grafo(caminho_g2)
    resultado2 = contar_arestas(grafo2)
    exibir_resultado('GRAFO_2', resultado2)

    print(f"\n{'=' * 50}\n")