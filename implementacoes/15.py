"""
15.py
------------------------------------
IMPLEMENTAÇÃO 15 — Determinação de articulações e blocos (biconectividade), utilizando obrigatoriamente a
função lowpt

Determina, para um grafo não-dirigido:
  - PONTOS DE ARTICULAÇÃO: vértices cuja remoção desconecta o grafo.
  - BLOCOS (componentes biconexas): subgrafos maximais sem ponto de
    articulação, ou seja, entre quaisquer dois vértices do bloco existem
    pelo menos dois caminhos internamente disjuntos.

ALGORITMO: DFS com função lowpt (Tarjan, 1972)
-----------------------------------------------
Durante uma DFS, cada vértice u recebe dois valores:
  - disc[u]  : ordem de descoberta (tempo de entrada na DFS)
  - lowpt[u] : menor disc alcançável a partir da subárvore de u,
               considerando no máximo UMA aresta de retorno.

Definição formal de lowpt[u]:
    lowpt[u] = min(
        disc[u],                          ← o próprio vértice
        disc[w]  para toda aresta de retorno (u, w),
        lowpt[v] para todo filho v de u na árvore DFS
    )

Condição de articulação:
  - u é RAIZ da DFS e tem 2 ou mais filhos na árvore DFS.
  - u NÃO é raiz e tem algum filho v tal que lowpt[v] >= disc[u].
    (significa que v não consegue "escapar" da subárvore de u sem
     passar por u — logo u é indispensável.)

Os blocos são identificados pela pilha de arestas:
  - Toda aresta percorrida é empilhada.
  - Quando uma articulação u é detectada (ou ao final da DFS na raiz),
    todas as arestas no topo da pilha até a aresta (u, v) formam um bloco.

Grafo avaliado: GRAFO_3
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grafo import ler_grafo


# ==============================================================================
# CLASSE AUXILIAR — ESTADO DA DFS
# ==============================================================================

class EstadoDFS:
    """
    Encapsula todas as variáveis de estado da DFS para evitar
    o uso de variáveis globais.

    Atributos:
        tempo      (int):  contador de tempo de descoberta
        disc       (dict): disc[v]  = tempo de descoberta do vértice v
        lowpt      (dict): lowpt[v] = menor disc alcançável a partir de v
        pai        (dict): pai[v]   = vértice que descobriu v na DFS
        pilha      (list): pilha de arestas da DFS (para extração de blocos)
        articulacoes (set): conjunto dos vértices de articulação encontrados
        blocos     (list): lista de blocos, cada bloco é um conjunto de arestas
    """

    def __init__(self):
        self.tempo       = 0
        self.disc        = {}
        self.lowpt       = {}
        self.pai         = {}
        self.pilha       = []   # pilha de arestas: lista de tuplas (u, v)
        self.articulacoes = set()
        self.blocos      = []


# ==============================================================================
# FUNÇÃO LOWPT — CORAÇÃO DO ALGORITMO
# ==============================================================================

def dfs_lowpt(u, estado, adjacencia):
    """
    Executa a DFS recursiva calculando disc e lowpt para cada vértice,
    identificando articulações e extraindo blocos pela pilha de arestas.

    Entrada:
        u          (str/int): vértice atual sendo visitado
        estado     (EstadoDFS): objeto com todo o estado da DFS
        adjacencia (dict): lista de adjacência do grafo

    Saída:
        Nenhuma — modifica 'estado' no lugar (articulacoes, blocos, lowpt)

    Pseudocódigo (Tarjan):
        disc[u] = lowpt[u] = ++tempo
        filhos = 0
        para cada vizinho v de u:
            se v não visitado:
                filhos++
                pai[v] = u
                empilha aresta (u, v)
                dfs_lowpt(v, ...)
                lowpt[u] = min(lowpt[u], lowpt[v])
                se (u é raiz e filhos > 1) OU (u não é raiz e lowpt[v] >= disc[u]):
                    u é articulação → extrai bloco da pilha até (u,v)
            senão se v != pai[u]:          ← aresta de retorno
                lowpt[u] = min(lowpt[u], disc[v])
                empilha aresta (u, v) se disc[v] < disc[u]
    """

    # Marca o vértice como visitado com o tempo atual
    estado.tempo      += 1
    estado.disc[u]     = estado.tempo
    estado.lowpt[u]    = estado.tempo  # inicialmente, lowpt = próprio disc

    filhos_dfs = 0  # conta filhos na árvore DFS (necessário para testar raiz)

    for v in adjacencia[u]:

        if v not in estado.disc:
            # ── Aresta de ÁRVORE: v ainda não foi visitado ──────────────────
            filhos_dfs   += 1
            estado.pai[v] = u

            # Empilha a aresta antes de descer na recursão
            estado.pilha.append((u, v))

            # Desce recursivamente
            dfs_lowpt(v, estado, adjacencia)

            # Após retorno: atualiza lowpt[u] com o que v conseguiu alcançar
            estado.lowpt[u] = min(estado.lowpt[u], estado.lowpt[v])

            # ── Verifica condição de ARTICULAÇÃO ────────────────────────────
            eh_raiz    = estado.pai.get(u) is None
            eh_articulacao = False

            if eh_raiz and filhos_dfs > 1:
                # Raiz com 2+ filhos na DFS → articulação
                eh_articulacao = True

            elif not eh_raiz and estado.lowpt[v] >= estado.disc[u]:
                # Não-raiz: filho v não escapa sem passar por u → articulação
                eh_articulacao = True

            if eh_articulacao:
                estado.articulacoes.add(u)
                # Extrai da pilha todas as arestas até (u, v) → formam um bloco
                _extrair_bloco(estado, u, v)

        elif v != estado.pai.get(u):
            # ── Aresta de RETORNO: v já foi visitado e não é o pai direto ───
            # Só empilha se for uma aresta "para trás" (disc[v] < disc[u])
            if estado.disc[v] < estado.disc[u]:
                estado.pilha.append((u, v))

            # Atualiza lowpt[u] com o disc do ancestral v
            estado.lowpt[u] = min(estado.lowpt[u], estado.disc[v])


def _extrair_bloco(estado, u, v):
    """
    Remove da pilha todas as arestas que pertencem ao bloco atual,
    ou seja, até encontrar (e incluir) a aresta (u, v) ou (v, u).

    Entrada:
        estado (EstadoDFS): estado atual da DFS
        u, v              : aresta que delimita o início do bloco

    Saída:
        Nenhuma — adiciona um frozenset de arestas em estado.blocos
    """
    bloco = set()

    while estado.pilha:
        aresta = estado.pilha.pop()
        bloco.add(aresta)
        # Para quando chegar na aresta que define o limite deste bloco
        if aresta == (u, v) or aresta == (v, u):
            break

    if bloco:
        estado.blocos.append(bloco)


# ==============================================================================
# FUNÇÃO PRINCIPAL DA IMPLEMENTAÇÃO
# ==============================================================================

def biconectividade(grafo):
    """
    Calcula pontos de articulação e blocos de um grafo não-dirigido
    usando DFS com a função lowpt (algoritmo de Tarjan).

    Percorre todos os vértices para garantir o tratamento de grafos
    desconectados (múltiplos componentes).

    Entrada:
        grafo (Grafo): objeto Grafo já lido/construído

    Saída:
        dict com as chaves:
            'articulacoes' (list): vértices de articulação ordenados
            'blocos'       (list): lista de blocos; cada bloco é um conjunto
                                   de tuplas (u, v) representando suas arestas
            'disc'         (dict): tempo de descoberta de cada vértice
            'lowpt'        (dict): valor lowpt de cada vértice
    """
    estado = EstadoDFS()

    for vertice in grafo.adjacencia:
        if vertice not in estado.disc:
            # Inicia DFS a partir de vértice não visitado (trata desconexão)
            estado.pai[vertice] = None  # marca como raiz desta componente
            dfs_lowpt(vertice, estado, grafo.adjacencia)

            # Ao final da DFS de uma componente, arestas restantes
            # na pilha formam o último bloco desta componente
            if estado.pilha:
                _extrair_bloco_final(estado)

    return {
        'articulacoes': sorted(estado.articulacoes, key=str),
        'blocos':       estado.blocos,
        'disc':         estado.disc,
        'lowpt':        estado.lowpt
    }


def _extrair_bloco_final(estado):
    """
    Esvazia a pilha ao final de uma componente DFS, registrando
    todas as arestas restantes como um único bloco.

    Entrada:
        estado (EstadoDFS): estado atual da DFS

    Saída:
        Nenhuma — adiciona o bloco em estado.blocos
    """
    bloco = set()
    while estado.pilha:
        bloco.add(estado.pilha.pop())
    if bloco:
        estado.blocos.append(bloco)


# ==============================================================================
# FUNÇÕES DE EXIBIÇÃO
# ==============================================================================

def exibir_tabela_lowpt(disc, lowpt):
    """
    Exibe a tabela de disc e lowpt de cada vértice, ordenados por
    tempo de descoberta.

    Entrada:
        disc  (dict): disc[v]  = tempo de descoberta
        lowpt (dict): lowpt[v] = valor lowpt
    Saída:
        Impressão no console
    """
    print("\n  Tabela disc / lowpt:")
    print(f"  {'Vértice':>8} | {'disc':>6} | {'lowpt':>6}")
    print(f"  {'-'*8}-+-{'-'*6}-+-{'-'*6}")

    # Ordena pelo tempo de descoberta
    for v in sorted(disc, key=lambda x: disc[x]):
        print(f"  {str(v):>8} | {disc[v]:>6} | {lowpt[v]:>6}")


def exibir_resultado(nome_grafo, resultado):
    """
    Exibe formatado articulações, blocos e a tabela lowpt.

    Entrada:
        nome_grafo (str): rótulo do grafo
        resultado  (dict): dicionário retornado por biconectividade()
    Saída:
        Impressão no console
    """
    print(f"\n{'=' * 60}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 60}")

    # ── Tabela disc/lowpt ────────────────────────────────────────────────────
    exibir_tabela_lowpt(resultado['disc'], resultado['lowpt'])

    # ── Articulações ─────────────────────────────────────────────────────────
    arts = resultado['articulacoes']
    print(f"\n  Pontos de Articulação ({len(arts)} encontrado(s)):")
    if arts:
        print(f"    → {', '.join(str(a) for a in arts)}")
    else:
        print("    → Nenhum (grafo biconexo)")

    # ── Blocos ───────────────────────────────────────────────────────────────
    blocos = resultado['blocos']
    print(f"\n  Blocos / Componentes Biconexas ({len(blocos)} encontrado(s)):")
    for i, bloco in enumerate(blocos, 1):
        # Vértices do bloco = união de todos os endpoints das arestas
        vertices_bloco = set()
        for (u, v) in bloco:
            vertices_bloco.add(u)
            vertices_bloco.add(v)
        arestas_fmt = ', '.join(
            f"({u}-{v})" for (u, v) in sorted(bloco, key=lambda e: (str(e[0]), str(e[1])))
        )
        # Bloco com 1 aresta = ponte (bridge block)
        tipo = "ponte/bridge" if len(bloco) == 1 else "componente biconexa"
        print(f"\n    Bloco {i} [{tipo}]:")
        print(f"      Vértices ({len(vertices_bloco)}): {sorted(vertices_bloco, key=str)}")
        print(f"      Arestas  ({len(bloco)}): {arestas_fmt}")

    # ── Resumo ───────────────────────────────────────────────────────────────
    n_pontes    = sum(1 for b in blocos if len(b) == 1)
    n_biconexas = len(blocos) - n_pontes
    print(f"\n  Resumo:")
    print(f"    Total de blocos         : {len(blocos)}")
    print(f"    Componentes biconexas   : {n_biconexas}")
    print(f"    Pontes (blocos-aresta)  : {n_pontes}")
    print(f"    Pontos de articulação   : {len(resultado['articulacoes'])}")


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    caminho_g3 = os.path.join(base, 'GRAFO_3.txt')
    grafo3     = ler_grafo(caminho_g3)
    resultado3 = biconectividade(grafo3)
    exibir_resultado('GRAFO_3', resultado3)

    print(f"\n{'=' * 60}\n")