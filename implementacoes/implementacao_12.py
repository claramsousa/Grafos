"""
implementacao_12.py
Módulo para verificar se um grafo é bipartido via algoritmo de 2-coloração.
"""

from collections import deque

def _exibir_arestas_coloridas(cores, adjacencia):
    """Exibe exemplos de arestas cruzando os conjuntos U e V."""
    visitados = set()
    exibidos  = 0
    for u in adjacencia:
        for v in adjacencia[u]:
            par = frozenset([u, v])
            if par not in visitados:
                visitados.add(par)
                cu, cv = cores.get(u, '?'), cores.get(v, '?')
                conj_u = "U" if cu == 0 else "V"
                conj_v = "U" if cv == 0 else "V"
                print(f"    ({u})[{conj_u}] ——— ({v})[{conj_v}]")
                exibidos += 1
                if exibidos >= 10:
                    print("    ...")
                    return

def _exibir_tabela_cores(cores):
    """Exibe a tabela de mapeamento vértice -> conjunto."""
    if not cores: return
    print(f"    {'Vértice':>8} | Cor | Conjunto")
    print(f"    {'-'*8}-+-----+---------")
    for v in sorted(cores, key=str):
        cor = cores[v]
        conj = "U" if cor == 0 else "V"
        print(f"    {str(v):>8} |  {cor}  |    {conj}")

def _bfs_coloracao(origem, adjacencia, cores):
    """Algoritmo de 2-coloração por componente conexa."""
    fila = deque([origem])
    cores[origem] = 0
    vertices_componente = [origem]
    conflito = None
    eh_bipartido = True

    while fila:
        u = fila.popleft()
        for v in adjacencia[u]:
            if v not in cores:
                cores[v] = 1 - cores[u]
                fila.append(v)
                vertices_componente.append(v)
            elif cores[v] == cores[u]:
                eh_bipartido = False
                if conflito is None:
                    conflito = (u, v, cores[u])

    return {
        'bipartido': eh_bipartido,
        'vertices': vertices_componente,
        'conflito': conflito,
        'cores_comp': {v: cores[v] for v in vertices_componente}
    }

def verificar_bipartido(grafo):
    """Verifica se o grafo é bipartido tratando todas as componentes."""
    cores = {}
    componentes = []
    eh_bipartido = True

    for vertice_inicial in grafo.adjacencia:
        if vertice_inicial not in cores:
            comp = _bfs_coloracao(vertice_inicial, grafo.adjacencia, cores)
            componentes.append(comp)
            if not comp['bipartido']:
                eh_bipartido = False

    return {
        'bipartido': eh_bipartido,
        'cores': cores,
        'conjunto_U': sorted([v for v, c in cores.items() if c == 0], key=str),
        'conjunto_V': sorted([v for v, c in cores.items() if c == 1], key=str),
        'ciclo_impar': next((c['conflito'] for c in componentes if c['conflito']), None),
        'componentes': componentes
    }

def exibir_resultado_bipartido(nome_grafo, resultado, adjacencia):
    """Interface de exibição para o resultado da bipartição."""
    print(f"\n{'=' * 60}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 60}")

    if resultado['bipartido']:
        print(f"\n  ✔  O grafo É BIPARTIDO\n")
        print(f"  Conjunto U (cor 0): {resultado['conjunto_U']}")
        print(f"  Conjunto V (cor 1): {resultado['conjunto_V']}")
        print(f"\n  Arestas (cruzando U e V):")
        _exibir_arestas_coloridas(resultado['cores'], adjacencia)
    else:
        print(f"\n  ✘  O grafo NÃO É BIPARTIDO\n")
        conflito = resultado['ciclo_impar']
        if conflito:
            u, v, cor = conflito
            nome_conj = "U" if cor == 0 else "V"
            print(f"  Motivo: aresta ({u})—({v}) conecta dois vértices no conjunto {nome_conj}.")
            print(f"  Isso prova a existência de um ciclo ímpar.")
        print(f"\n  Coloração parcial (Diagnóstico):")
        _exibir_tabela_cores(resultado['cores'])