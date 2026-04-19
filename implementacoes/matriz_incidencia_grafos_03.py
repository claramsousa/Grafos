"""
matriz_incidencia_grafos_03.py
Módulo para representação de Grafos por Matriz de Incidência.
"""

def _chave_ordenacao(v):
    """
    Chave de ordenação mista: ordena vértices numéricos como inteiros
    e vértices alfanuméricos como strings.
    """
    try:
        return (0, int(v))
    except (ValueError, TypeError):
        return (1, str(v))

def construir_matriz_incidencia(grafo):
    """
    Constrói a Matriz de Incidência de um grafo não-dirigido.

    Entrada:
        grafo: objeto Grafo
    Saída:
        dict: contendo a matriz, lista de vértices e lista de arestas
    """
    # Ordena para garantir que a matriz seja determinística
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    arestas  = sorted(grafo.obter_arestas(),
                      key=lambda e: (_chave_ordenacao(e[0]),
                                     _chave_ordenacao(e[1])))

    # Cria a matriz zerada (Linhas = Vértices, Colunas = Arestas)
    matriz = [[0] * len(arestas) for _ in range(len(vertices))]

    # Preenche a matriz: cada coluna j tem 1 nas linhas dos seus dois vértices
    for j, (u, v) in enumerate(arestas):
        linha_u = vertices.index(u)
        linha_v = vertices.index(v)
        
        matriz[linha_u][j] = 1
        matriz[linha_v][j] = 1

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arestas':  arestas
    }

def exibir_resultado(nome_grafo, mat_inc):
    """Exibe formatado a Matriz de Incidência com nomes das arestas no cabeçalho."""
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arestas  = mat_inc['arestas']
    
    nomes_arestas = [f"{{{u},{v}}}" for u, v in arestas]
    largura_col = max(max(len(n) for n in nomes_arestas), 5) + 2

    print(f"\n{'=' * 70}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 70}")
    print(f"  Dimensão da matriz: {len(vertices)} vértices x {len(arestas)} arestas\n")

    # Cabeçalho: nomes das arestas
    cabecalho = " " * 9
    for nome in nomes_arestas:
        cabecalho += nome.center(largura_col)
    
    print(cabecalho)
    print(" " * 8 + "-" * (largura_col * len(arestas) + 2))

    # Linhas: cada vértice com seus valores na matriz
    for i, v in enumerate(vertices):
        prefixo = f"  v={str(v):>3} |"
        celulas = ""
        for j in range(len(arestas)):
            valor = str(matriz[i][j])
            celulas += valor.center(largura_col)
        print(f"{prefixo}{celulas}")