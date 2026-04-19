"""
implementacao_08.py
Módulo para determinar o número total de arestas de um grafo não-dirigido.
"""

def contar_arestas(grafo):
    """
    Determina o número total de arestas de um grafo não-dirigido.

    Como a lista de adjacência armazena cada aresta duas vezes (u-v e v-u),
    filtramos as duplicatas para contar cada conexão apenas uma vez.
    """
    visitados = set()   # Conjunto para evitar contagem dupla
    arestas_unicas = [] # Lista das arestas para exibição

    for u in grafo.adjacencia:
        for v in grafo.adjacencia[u]:
            # Usamos frozenset para que {a,b} seja igual a {b,a}
            par = frozenset([u, v])

            if par not in visitados:
                visitados.add(par)
                arestas_unicas.append((u, v))

    return {
        'total':   len(arestas_unicas),
        'arestas': arestas_unicas
    }

def exibir_contagem_arestas(nome_grafo, resultado):
    """
    Exibe formatado o resultado da contagem de arestas.
    """
    print(f"\n{'=' * 50}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Total de arestas: {resultado['total']}")
    print(f"  Arestas encontradas:")
    for u, v in resultado['arestas']:
        print(f"    ({u}) ——— ({v})")