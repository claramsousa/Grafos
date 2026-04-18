"""
18.py
--------------------------------------
IMPLEMENTAÇÃO 18 — Determinação do Grafo subjacente

O GRAFO SUBJACENTE (ou grafo subjacente não-dirigido) de um dígrafo D é
obtido ignorando-se a direção de todos os arcos, transformando cada arco
(u → v) em uma aresta não-dirigida {u, v}.

Regras de construção:
  - Cada arco (u → v) do dígrafo gera uma aresta {u, v} no grafo subjacente.
  - Se existirem arcos opostos (u → v) E (v → u), eles geram UMA ÚNICA
    aresta {u, v} — sem aresta paralela (grafo simples).
  - Todos os vértices do dígrafo são preservados, mesmo os isolados.

Aplicações práticas:
  - Verificar conectividade fraca de um dígrafo (um dígrafo é fracamente
    conexo se e somente se seu grafo subjacente for conexo).
  - Servir de base para algoritmos que não dependem de orientação.

Dígrafo avaliado: DIGRAFO1
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grafo import ler_digrafo, Grafo


# ==============================================================================
# FUNÇÃO PRINCIPAL DA IMPLEMENTAÇÃO
# ==============================================================================

def obter_grafo_subjacente(digrafo):
    """
    Constrói o grafo subjacente (não-dirigido) a partir de um dígrafo.

    Para cada arco (u → v) do dígrafo, adiciona a aresta bidirecional
    {u, v} no grafo resultante. Arcos opostos (u→v e v→u) geram apenas
    uma aresta, pois a classe Grafo já evita duplicatas na adjacência.

    Entrada:
        digrafo (Digrafo): objeto Digrafo já lido/construído

    Saída:
        Grafo: novo objeto Grafo não-dirigido (o grafo subjacente),
               com os mesmos vértices e arestas derivadas dos arcos
    """
    subjacente = Grafo()

    # Garante que todos os vértices do dígrafo existam no subjacente,
    # inclusive aqueles que possam ser apenas destino (sem arcos de saída)
    for v in digrafo.adjacencia:
        subjacente.adicionar_vertice(v)

    # Para cada arco (u → v), adiciona a aresta bidirecional {u, v}
    # O método adicionar_aresta já trata duplicatas internamente
    for u in digrafo.adjacencia:
        for v in digrafo.adjacencia[u]:
            subjacente.adicionar_aresta(u, v)

    # Copia o número de vértices declarado do dígrafo original
    subjacente.num_vertices_declarado = digrafo.num_vertices_declarado

    return subjacente


def analisar_diferenca(digrafo, subjacente):
    """
    Compara arcos do dígrafo com arestas do grafo subjacente, identificando
    quais arcos opostos foram fundidos em uma única aresta.

    Entrada:
        digrafo    (Digrafo): dígrafo original
        subjacente (Grafo):   grafo subjacente construído

    Saída:
        dict com as chaves:
            'arcos_originais'  (list): lista de tuplas (u, v) — arcos do dígrafo
            'arestas_subj'     (list): lista de tuplas (u, v) — arestas do subjacente
            'arcos_fundidos'   (list): pares de arcos opostos fundidos em 1 aresta
            'total_arcos'      (int):  número de arcos no dígrafo
            'total_arestas'    (int):  número de arestas no grafo subjacente
    """
    arcos     = digrafo.obter_arcos()
    arestas   = subjacente.obter_arestas()

    # Detecta pares de arcos opostos: (u→v) e (v→u) existem simultaneamente
    arcos_set    = set(arcos)
    arcos_fundidos = []
    visitados_fund = set()

    for (u, v) in arcos:
        par = frozenset([u, v])
        if (v, u) in arcos_set and par not in visitados_fund:
            arcos_fundidos.append((u, v, v, u))   # ((u→v) e (v→u) → {u,v})
            visitados_fund.add(par)

    return {
        'arcos_originais': arcos,
        'arestas_subj':    arestas,
        'arcos_fundidos':  arcos_fundidos,
        'total_arcos':     len(arcos),
        'total_arestas':   len(arestas)
    }


def verificar_conectividade_fraca(subjacente):
    """
    Verifica se o dígrafo original é FRACAMENTE CONEXO, ou seja, se seu
    grafo subjacente é conexo (existe caminho entre todo par de vértices
    ignorando a direção dos arcos).

    Utiliza BFS sobre o grafo subjacente.

    Entrada:
        subjacente (Grafo): grafo subjacente já construído

    Saída:
        dict com as chaves:
            'fracamente_conexo' (bool): True se o subjacente for conexo
            'componentes'       (list): lista de componentes (conjuntos de vértices)
    """
    visitados  = set()
    componentes = []

    for inicio in subjacente.adjacencia:
        if inicio in visitados:
            continue

        # BFS a partir de 'inicio'
        fila       = [inicio]
        componente = []
        visitados.add(inicio)

        while fila:
            u = fila.pop(0)
            componente.append(u)

            for v in subjacente.adjacencia[u]:
                if v not in visitados:
                    visitados.add(v)
                    fila.append(v)

        componentes.append(sorted(componente, key=str))

    return {
        'fracamente_conexo': len(componentes) == 1,
        'componentes':       componentes
    }


# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

def exibir_resultado(nome_digrafo, digrafo, subjacente, analise, conectividade):
    """
    Exibe formatado o dígrafo original, o grafo subjacente e a análise.

    Entrada:
        nome_digrafo  (str):    rótulo do dígrafo
        digrafo       (Digrafo): dígrafo original
        subjacente    (Grafo):  grafo subjacente construído
        analise       (dict):   resultado de analisar_diferenca()
        conectividade (dict):   resultado de verificar_conectividade_fraca()

    Saída:
        Impressão no console (nenhum retorno)
    """
    print(f"\n{'=' * 62}")
    print(f"  {nome_digrafo}  →  Grafo Subjacente")
    print(f"{'=' * 62}")

    # ── Dígrafo original ──────────────────────────────────────────────────────
    print(f"\n  [ DÍGRAFO ORIGINAL ]")
    print(f"  Vértices : {sorted(digrafo.obter_vertices(), key=str)}")
    print(f"  Arcos ({analise['total_arcos']}):")
    for (u, v) in analise['arcos_originais']:
        print(f"    ({u}) ──► ({v})")

    # ── Arcos fundidos ────────────────────────────────────────────────────────
    if analise['arcos_fundidos']:
        print(f"\n  Arcos OPOSTOS fundidos em aresta única ({len(analise['arcos_fundidos'])}):")
        for (u, v, vu, vv) in analise['arcos_fundidos']:
            print(f"    ({u}→{v})  +  ({vu}→{vv})  →  aresta {{{u},{v}}}")

    # ── Grafo subjacente ──────────────────────────────────────────────────────
    print(f"\n  [ GRAFO SUBJACENTE ]")
    print(f"  Vértices : {sorted(subjacente.obter_vertices(), key=str)}")
    print(f"  Arestas ({analise['total_arestas']}):")
    for (u, v) in sorted(analise['arestas_subj'], key=lambda e: (str(e[0]), str(e[1]))):
        print(f"    ({u}) ——— ({v})")

    # ── Lista de adjacência do grafo subjacente ───────────────────────────────
    print(f"\n  Lista de Adjacência do Grafo Subjacente:")
    print(f"  {'Vértice':>8} | Vizinhos")
    print(f"  {'-'*8}-+-{'—'*35}")
    for v in sorted(subjacente.adjacencia, key=str):
        vizinhos = sorted(subjacente.adjacencia[v], key=str)
        print(f"  {str(v):>8} | {vizinhos}")

    # ── Conectividade fraca ───────────────────────────────────────────────────
    print(f"\n  Conectividade Fraca do Dígrafo:")
    if conectividade['fracamente_conexo']:
        print(f"  ✔  O dígrafo É FRACAMENTE CONEXO")
        print(f"     (seu grafo subjacente é conexo)")
    else:
        comps = conectividade['componentes']
        print(f"  ✘  O dígrafo NÃO É FRACAMENTE CONEXO")
        print(f"     {len(comps)} componentes fracamente conexas:")
        for i, comp in enumerate(comps, 1):
            print(f"     Componente {i}: {comp}")

    # ── Resumo comparativo ────────────────────────────────────────────────────
    print(f"\n  Resumo comparativo:")
    print(f"  {'Propriedade':<30} {'Dígrafo':>10} {'Subjacente':>12}")
    print(f"  {'-'*30}-{'-'*10}-{'-'*12}")
    print(f"  {'Vértices':<30} {len(digrafo.obter_vertices()):>10} "
          f"{len(subjacente.obter_vertices()):>12}")
    print(f"  {'Arestas/Arcos':<30} {analise['total_arcos']:>10} "
          f"{analise['total_arestas']:>12}")
    print(f"  {'Arcos opostos fundidos':<30} {len(analise['arcos_fundidos']):>10} "
          f"{'—':>12}")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # -------------------------------------------------------
    # DIGRAFO 1
    # -------------------------------------------------------
    caminho_d1 = os.path.join(base, 'DIGRAFO1.txt')
    digrafo1   = ler_digrafo(caminho_d1)

    # Constrói o grafo subjacente
    subjacente1 = obter_grafo_subjacente(digrafo1)

    # Analisa diferenças e verifica conectividade fraca
    analise1       = analisar_diferenca(digrafo1, subjacente1)
    conectividade1 = verificar_conectividade_fraca(subjacente1)

    exibir_resultado('DIGRAFO1', digrafo1, subjacente1, analise1, conectividade1)

    print(f"\n{'=' * 62}\n")