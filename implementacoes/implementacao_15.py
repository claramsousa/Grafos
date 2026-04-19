"""
implementacao_15.py
Módulo para determinação de articulações e blocos utilizando a função lowpt.
"""

class EstadoDFS:
    """Encapsula o estado da busca em profundidade para o cálculo de biconectividade."""
    def __init__(self):
        self.tempo = 0
        self.disc = {}
        self.lowpt = {}
        self.pai = {}
        self.pilha = []
        self.articulacoes = set()
        self.blocos = []

def _extrair_bloco(estado, u, v):
    """Extrai as arestas da pilha que formam um bloco (componente biconexa)."""
    bloco = set()
    while estado.pilha:
        aresta = estado.pilha.pop()
        bloco.add(aresta)
        if aresta == (u, v) or aresta == (v, u):
            break
    if bloco:
        estado.blocos.append(bloco)

def _extrair_bloco_final(estado):
    """Extrai as arestas restantes da pilha ao fim de uma componente."""
    bloco = set()
    while estado.pilha:
        bloco.add(estado.pilha.pop())
    if bloco:
        estado.blocos.append(bloco)

def dfs_lowpt(u, estado, adjacencia):
    """DFS recursiva que calcula disc e lowpt para identificar articulações."""
    estado.tempo += 1
    estado.disc[u] = estado.lowpt[u] = estado.tempo
    filhos_dfs = 0

    for v in adjacencia[u]:
        if v not in estado.disc:
            filhos_dfs += 1
            estado.pai[v] = u
            estado.pilha.append((u, v))
            
            dfs_lowpt(v, estado, adjacencia)

            # Após o retorno da recursão, atualiza o lowpt do pai
            estado.lowpt[u] = min(estado.lowpt[u], estado.lowpt[v])

            # Condição de Articulação
            eh_raiz = estado.pai.get(u) is None
            if (eh_raiz and filhos_dfs > 1) or (not eh_raiz and estado.lowpt[v] >= estado.disc[u]):
                estado.articulacoes.add(u)
                _extrair_bloco(estado, u, v)

        elif v != estado.pai.get(u):
            # Aresta de retorno
            if estado.disc[v] < estado.disc[u]:
                estado.pilha.append((u, v))
            estado.lowpt[u] = min(estado.lowpt[u], estado.disc[v])

def biconectividade(grafo):
    """Função principal que orquestra o algoritmo de Tarjan."""
    estado = EstadoDFS()
    for vertice in grafo.adjacencia:
        if vertice not in estado.disc:
            estado.pai[vertice] = None
            dfs_lowpt(vertice, estado, grafo.adjacencia)
            if estado.pilha:
                _extrair_bloco_final(estado)

    return {
        'articulacoes': sorted(estado.articulacoes, key=str),
        'blocos': estado.blocos,
        'disc': estado.disc,
        'lowpt': estado.lowpt
    }

def exibir_resultado_biconectividade(nome_grafo, resultado):
    """Exibe o diagnóstico completo de articulações e blocos."""
    print(f"\n{'=' * 60}")
    print(f"  RESULTADO BICONECTIVIDADE: {nome_grafo}")
    print(f"{'=' * 60}")

    # Tabela disc/lowpt
    print("\n  Tabela disc / lowpt:")
    print(f"  {'Vértice':>8} | {'disc':>6} | {'lowpt':>6}")
    print(f"  {'-'*8}-+-{'-'*6}-+-{'-'*6}")
    for v in sorted(resultado['disc'], key=lambda x: resultado['disc'][x]):
        print(f"  {str(v):>8} | {resultado['disc'][v]:>6} | {resultado['lowpt'][v]:>6}")

    # Articulações
    print(f"\n  Pontos de Articulação encontrados: {resultado['articulacoes'] if resultado['articulacoes'] else 'Nenhum'}")

    # Blocos
    print(f"\n  Blocos / Componentes Biconexas ({len(resultado['blocos'])}):")
    for i, bloco in enumerate(resultado['blocos'], 1):
        v_bloco = set()
        for u, v in bloco:
            v_bloco.update([u, v])
        tipo = "ponte" if len(bloco) == 1 else "biconexo"
        print(f"    Bloco {i} [{tipo}]: {sorted(v_bloco, key=str)}")