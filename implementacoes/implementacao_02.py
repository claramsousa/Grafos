"""
implementacao_02.py
Módulo para construção e exibição da Matriz de Adjacência.
"""

def construir_matriz_adjacencia(grafo):
    """
    Constrói a matriz de adjacência a partir do objeto Grafo.
    Retorna um dicionário com a matriz (lista de listas) e a lista de vértices ordenados.
    """
    # Lógica de ordenação: prioriza números, depois letras
    chave_ord = lambda v: (0, int(v)) if str(v).isdigit() else (1, str(v))
    vertices_ordenados = sorted(grafo.obter_vertices(), key=chave_ord)
    
    n = len(vertices_ordenados)
    # Mapa de índices para preenchimento rápido da matriz
    indice = {v: i for i, v in enumerate(vertices_ordenados)}
    
    # Inicializa a matriz N x N com zeros
    matriz = [[0 for _ in range(n)] for _ in range(n)]
    
    # Preenche com 1 onde existe adjacência no dicionário do grafo
    for v_origem in vertices_ordenados:
        vizinhos = grafo.adjacencia.get(v_origem, [])
        for v_destino in vizinhos:
            i, j = indice[v_origem], indice[v_destino]
            matriz[i][j] = 1
            
    return {
        "matriz": matriz,
        "vertices": vertices_ordenados
    }

def exibir_matriz_adjacencia(nome_grafo, grafo):
    """
    Constrói e exibe visualmente a Matriz de Adjacência formatada no console.
    """
    # Ordenação para exibição determinística
    vertices = sorted(grafo.obter_vertices(), key=lambda v: (int(v) if str(v).isdigit() else v))
    n = len(vertices)
    
    print(f"\n{'=' * 65}")
    print(f"   TAREFA (02) — MATRIZ DE ADJACÊNCIA: {nome_grafo}")
    print(f"{'=' * 65}")
    
    # Cabeçalho da matriz
    header = "      " + " ".join(f"{str(v):>3}" for v in vertices)
    print(header)
    print("     " + "—" * (len(header) - 5))
    
    # Construção linha por linha
    for v_linha in vertices:
        linha_bits = []
        for v_coluna in vertices:
            # Verifica a existência da conexão na lista de adjacência
            if v_coluna in grafo.adjacencia[v_linha]:
                linha_bits.append(1)
            else:
                linha_bits.append(0)
        
        rotulo = f" {str(v_linha):>3} |"
        valores = "".join(f"{x:>4}" for x in linha_bits)
        print(f"{rotulo}{valores}   ]")