"""
implementacao_04_bipartido.py
------------------------------
IMPLEMENTAÇÃO 04 — Verificação de Grafo Bipartido

Um grafo é BIPARTIDO se seus vértices podem ser divididos em dois conjuntos
disjuntos (U e V) de forma que toda aresta conecte um vértice de U a um
vértice de V — ou seja, nenhuma aresta liga dois vértices do mesmo conjunto.

TEOREMA FUNDAMENTAL (König, 1916):
    Um grafo é bipartido se e somente se NÃO possui ciclos de comprimento
    ímpar.

ALGORITMO: 2-COLORAÇÃO POR BFS
---------------------------------
Tentamos colorir o grafo com exatamente 2 cores (0 e 1):
  - Atribuímos a cor 0 ao vértice inicial.
  - Para cada vizinho não colorido, atribuímos a cor oposta (1 - cor_atual).
  - Se encontrarmos um vizinho já colorido com a MESMA cor do vértice atual,
    existe uma aresta dentro do mesmo conjunto → o grafo NÃO é bipartido.

O algoritmo roda sobre todos os vértices para tratar grafos desconectados
(cada componente é testada independentemente).

Complexidade: O(V + E)

Grafos avaliados: GRAFO_1 e GRAFO_2
"""

import sys
import os
from collections import deque  # fila para BFS — uso permitido (estrutura auxiliar)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grafo import ler_grafo


# ==============================================================================
# FUNÇÕES AUXILIARES DE EXIBIÇÃO
# ==============================================================================

def _exibir_arestas_coloridas(cores, adjacencia):
    """
    Exibe até 10 arestas de exemplo mostrando que cada uma cruza os conjuntos.

    Entrada:
        cores      (dict): mapeamento vértice -> cor (0 ou 1)
        adjacencia (dict): lista de adjacência do grafo

    Saída:
        Impressão no console (nenhum retorno)
    """
    visitados = set()
    exibidos  = 0
    for u in adjacencia:
        for v in adjacencia[u]:
            par = frozenset([u, v])
            if par not in visitados:
                visitados.add(par)
                cu     = cores.get(u, '?')
                cv     = cores.get(v, '?')
                conj_u = "U" if cu == 0 else "V"
                conj_v = "U" if cv == 0 else "V"
                print(f"    ({u})[{conj_u}] ——— ({v})[{conj_v}]")
                exibidos += 1
                if exibidos >= 10:
                    print("    ...")
                    return


def _exibir_tabela_cores(cores):
    """
    Exibe tabela vértice -> cor/conjunto para diagnóstico.

    Entrada:
        cores (dict): mapeamento vértice -> cor (0 ou 1)

    Saída:
        Impressão no console (nenhum retorno)
    """
    if not cores:
        return
    print(f"    {'Vértice':>8} | Cor | Conjunto")
    print(f"    {'-'*8}-+-----+---------")
    for v in sorted(cores, key=str):
        cor  = cores[v]
        conj = "U" if cor == 0 else "V"
        print(f"    {str(v):>8} |  {cor}  |    {conj}")


# ==============================================================================
# FUNÇÃO AUXILIAR — coleta cores das componentes (grafo não-bipartido)
# ==============================================================================

def _coletar_cores_parciais(componentes):
    """
    Reconstrói o dicionário de cores a partir das componentes processadas.
    Útil para exibir a coloração parcial quando o grafo não é bipartido.

    Entrada:
        componentes (list): lista de dicts retornados por _bfs_coloracao()

    Saída:
        dict: mapeamento vértice -> cor coletado de todas as componentes
    """
    cores = {}
    for comp in componentes:
        cores.update(comp.get('cores_comp', {}))
    return cores


# ==============================================================================
# FUNÇÃO BFS DE 2-COLORAÇÃO
# ==============================================================================

def _bfs_coloracao(origem, adjacencia, cores):
    """
    Executa a BFS de 2-coloração a partir de 'origem', preenchendo
    o dicionário 'cores' para todos os vértices alcançáveis.

    Entrada:
        origem     (str/int): vértice inicial da BFS
        adjacencia (dict): lista de adjacência do grafo
        cores      (dict): dicionário compartilhado de coloração
                           (modificado no lugar)

    Saída:
        dict com as chaves:
            'bipartido'  (bool): True se esta componente é bipartida
            'vertices'   (list): vértices desta componente
            'conflito'   (tuple | None): (u, v, cor) da aresta conflitante
            'cores_comp' (dict): cópia das cores atribuídas nesta componente
    """
    fila = deque()
    fila.append(origem)
    cores[origem] = 0           # cor inicial: 0 (conjunto U)

    vertices_componente = [origem]
    conflito    = None
    eh_bipartido = True

    while fila:
        u = fila.popleft()      # retira o próximo vértice da fila BFS

        for v in adjacencia[u]:

            if v not in cores:
                # Vértice não colorido: atribui cor oposta à do vértice atual
                cores[v] = 1 - cores[u]   # alterna entre 0 e 1
                fila.append(v)
                vertices_componente.append(v)

            else:
                # Vértice já colorido: verifica conflito de cor
                if cores[v] == cores[u]:
                    # Mesma cor → aresta interna ao conjunto → não bipartido
                    eh_bipartido = False
                    if conflito is None:        # registra apenas o primeiro
                        conflito = (u, v, cores[u])

    # Cópia local das cores desta componente para exibição posterior
    cores_comp = {v: cores[v] for v in vertices_componente}

    return {
        'bipartido':  eh_bipartido,
        'vertices':   vertices_componente,
        'conflito':   conflito,
        'cores_comp': cores_comp
    }


# ==============================================================================
# FUNÇÃO PRINCIPAL DA IMPLEMENTAÇÃO
# ==============================================================================

def verificar_bipartido(grafo):
    """
    Verifica se um grafo não-dirigido é bipartido usando 2-coloração por BFS.

    Percorre todas as componentes do grafo (caso seja desconectado),
    testando cada uma independentemente. O grafo é bipartido somente se
    TODAS as componentes forem bipartidas.

    Entrada:
        grafo (Grafo): objeto Grafo já lido/construído

    Saída:
        dict com as chaves:
            'bipartido'   (bool): True se o grafo é bipartido
            'cores'       (dict): mapeamento vértice -> cor (0 ou 1)
            'conjunto_U'  (list): vértices com cor 0 (se bipartido)
            'conjunto_V'  (list): vértices com cor 1 (se bipartido)
            'ciclo_impar' (tuple | None): (u, v, cor) da aresta conflitante
            'componentes' (list): resultado detalhado por componente
    """
    cores        = {}    # dicionário compartilhado de cores (preenchido pela BFS)
    componentes  = []    # resultado por componente
    eh_bipartido = True  # assume bipartido até encontrar conflito

    for vertice_inicial in grafo.adjacencia:

        if vertice_inicial in cores:
            continue    # vértice já processado em componente anterior

        # Inicia BFS de coloração nesta componente
        comp = _bfs_coloracao(vertice_inicial, grafo.adjacencia, cores)
        componentes.append(comp)

        # Se qualquer componente não for bipartida, o grafo todo não é
        if not comp['bipartido']:
            eh_bipartido = False

    # Monta conjuntos U e V
    conjunto_U = sorted([v for v, c in cores.items() if c == 0], key=str)
    conjunto_V = sorted([v for v, c in cores.items() if c == 1], key=str)

    # Localiza o primeiro conflito encontrado (se houver)
    conflito = None
    for comp in componentes:
        if comp['conflito']:
            conflito = comp['conflito']
            break

    return {
        'bipartido':   eh_bipartido,
        'cores':       cores,
        'conjunto_U':  conjunto_U,
        'conjunto_V':  conjunto_V,
        'ciclo_impar': conflito,
        'componentes': componentes
    }


# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

def exibir_resultado(nome_grafo, resultado, adjacencia):
    """
    Exibe formatado o resultado da verificação de bipartição.

    Entrada:
        nome_grafo (str):  rótulo do grafo
        resultado  (dict): dicionário retornado por verificar_bipartido()
        adjacencia (dict): lista de adjacência do grafo (para exibir arestas)

    Saída:
        Impressão no console (nenhum retorno)
    """
    print(f"\n{'=' * 60}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 60}")

    cores = resultado['cores']

    if resultado['bipartido']:
        # ── GRAFO BIPARTIDO ──────────────────────────────────────────────────
        print(f"\n  ✔  O grafo É BIPARTIDO\n")
        print(f"  Conjunto U (cor 0) [{len(resultado['conjunto_U'])} vértices]: "
              f"{resultado['conjunto_U']}")
        print(f"  Conjunto V (cor 1) [{len(resultado['conjunto_V'])} vértices]: "
              f"{resultado['conjunto_V']}")

        # Exibe componentes se houver mais de uma (grafo desconectado)
        comps = resultado['componentes']
        if len(comps) > 1:
            print(f"\n  Componentes ({len(comps)}):")
            for i, comp in enumerate(comps, 1):
                print(f"    Componente {i}: {sorted(comp['vertices'], key=str)}")

        # Mostra arestas com seus respectivos conjuntos
        print(f"\n  Arestas (confirmando que cruzam os conjuntos U e V):")
        _exibir_arestas_coloridas(cores, adjacencia)

    else:
        # ── GRAFO NÃO-BIPARTIDO ──────────────────────────────────────────────
        print(f"\n  ✘  O grafo NÃO É BIPARTIDO\n")

        conflito = resultado['ciclo_impar']
        if conflito:
            u, v, cor = conflito
            nome_conj = "U" if cor == 0 else "V"
            print(f"  Motivo: aresta ({u})—({v}) conecta dois vértices")
            print(f"          ambos no conjunto {nome_conj} (cor {cor}).")
            print(f"          Isso indica a presença de um ciclo de comprimento ímpar.")

        # Exibe a coloração parcial para diagnóstico
        cores_parciais = _coletar_cores_parciais(resultado['componentes'])
        if cores_parciais:
            print(f"\n  Coloração parcial obtida pela BFS:")
            _exibir_tabela_cores(cores_parciais)


# ==============================================================================
# EXECUÇÃO PRINCIPAL
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # -------------------------------------------------------
    # GRAFO 1
    # -------------------------------------------------------
    caminho_g1 = os.path.join(base, 'GRAFO_1.txt')
    grafo1     = ler_grafo(caminho_g1)
    resultado1 = verificar_bipartido(grafo1)
    exibir_resultado('GRAFO_1', resultado1, grafo1.adjacencia)

    # -------------------------------------------------------
    # GRAFO 2
    # -------------------------------------------------------
    caminho_g2 = os.path.join(base, 'GRAFO_2.txt')
    grafo2     = ler_grafo(caminho_g2)
    resultado2 = verificar_bipartido(grafo2)
    exibir_resultado('GRAFO_2', resultado2, grafo2.adjacencia)

    print(f"\n{'=' * 60}\n")