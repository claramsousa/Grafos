"""
implementacao_19.py
Módulo para conversão entre Matriz de Incidência e Estrela Direta (Forward Star).
"""

def construir_matriz_incidencia_fs(digrafo):
    """Constrói a Matriz de Incidência $|V| \times |A|$ de um dígrafo."""
    vertices = sorted(digrafo.obter_vertices(), key=str)
    arcos    = sorted(digrafo.obter_arcos(), key=lambda a: (str(a[0]), str(a[1])))

    idx_v = {v: i for i, v in enumerate(vertices)}
    idx_a = {a: j for j, a in enumerate(arcos)}
    matriz = [[0] * len(arcos) for _ in range(len(vertices))]

    for (u, v) in arcos:
        j = idx_a[(u, v)]
        matriz[idx_v[u]][j] = +1  # Origem
        matriz[idx_v[v]][j] = -1  # Destino

    return {'matriz': matriz, 'vertices': vertices, 'arcos': arcos, 'idx_v': idx_v, 'idx_a': idx_a}

def construir_estrela_direta(digrafo):
    """Constrói a representação Forward Star (APONTA e DEST)."""
    vertices = sorted(digrafo.obter_vertices(), key=str)
    arcos    = sorted(digrafo.obter_arcos(), key=lambda a: (str(a[0]), str(a[1])))
    n, m = len(vertices), len(arcos)

    DEST = [None] + [v for (u, v) in arcos]
    grau_saida = {v: 0 for v in vertices}
    for (u, _) in arcos: grau_saida[u] += 1

    APONTA = [None] * (n + 2)
    APONTA[1] = 1
    for i, v in enumerate(vertices, start=1):
        APONTA[i + 1] = APONTA[i] + grau_saida[v]

    return {'APONTA': APONTA, 'DEST': DEST, 'vertices': vertices, 'arcos': arcos}

def matriz_para_estrela_direta(mat_inc):
    """Converte Matriz de Incidência para Estrela Direta."""
    matriz, vertices, arcos_mi = mat_inc['matriz'], mat_inc['vertices'], mat_inc['arcos']
    n, m = len(vertices), len(arcos_mi)

    arcos_extraidos = []
    for j in range(m):
        origem = destino = None
        for i in range(n):
            if matriz[i][j] == +1: origem = vertices[i]
            elif matriz[i][j] == -1: destino = vertices[i]
        if origem is not None: arcos_extraidos.append((origem, destino))

    arcos_ord = sorted(arcos_extraidos, key=lambda a: (str(a[0]), str(a[1])))
    DEST = [None] + [v for (u, v) in arcos_ord]
    
    grau_saida = {v: 0 for v in vertices}
    for (u, _) in arcos_ord: grau_saida[u] += 1

    APONTA = [None] * (n + 2)
    APONTA[1] = 1
    for i, v in enumerate(vertices, start=1):
        APONTA[i + 1] = APONTA[i] + grau_saida[v]

    return {'APONTA': APONTA, 'DEST': DEST, 'vertices': vertices, 'arcos': arcos_ord}

def estrela_direta_para_matriz(estrela):
    """Converte Estrela Direta de volta para Matriz de Incidência."""
    APONTA, DEST, vertices, arcos = estrela['APONTA'], estrela['DEST'], estrela['vertices'], estrela['arcos']
    n, m = len(vertices), len(arcos)
    
    idx_v = {v: i for i, v in enumerate(vertices)}
    idx_a = {a: j for j, a in enumerate(arcos)}
    matriz = [[0] * m for _ in range(n)]

    for i, u in enumerate(vertices, start=1):
        for k in range(APONTA[i], APONTA[i + 1]):
            v = DEST[k]
            j = idx_a[(u, v)]
            matriz[idx_v[u]][j] = +1
            matriz[idx_v[v]][j] = -1

    return {'matriz': matriz, 'vertices': vertices, 'arcos': arcos}

def exibir_fs_mi_conversao(digrafo, mi_orig, fs_orig, fs_conv, mi_reconst):
    """Exibe o relatório comparativo das conversões."""
    print(f"\n" + "═" * 60)
    print("  RELATÓRIO DE CONVERSÃO: MATRIZ ↔ ESTRELA DIRETA")
    print("═" * 60)

    # Validação lógica
    valid_fs = fs_orig['APONTA'] == fs_conv['APONTA'] and fs_orig['DEST'] == fs_conv['DEST']
    valid_mi = mi_orig['matriz'] == mi_reconst['matriz']

    print(f"\n  [1] Vetores da Estrela Direta (Forward Star):")
    print(f"      APONTA: {fs_orig['APONTA'][1:]}")
    print(f"      DEST:   {fs_orig['DEST'][1:]}")
    print(f"      Status: {'✔ Conversão Íntegra' if valid_fs else '✘ Erro na Conversão'}")

    print(f"\n  [2] Matriz de Incidência Reconstituída:")
    print(f"      Dimensão: {len(mi_reconst['vertices'])} x {len(mi_reconst['arcos'])}")
    print(f"      Status: {'✔ Reconstituição Fiel' if valid_mi else '✘ Divergência Detectada'}")
    
    print("\n  [3] Sucessores (via Forward Star):")
    for i, v in enumerate(fs_orig['vertices'], 1):
        ini, fim = fs_orig['APONTA'][i], fs_orig['APONTA'][i+1] - 1
        sucs = fs_orig['DEST'][ini:fim+1] if ini <= fim else []
        print(f"      Vértice {v:>2}: {sucs}")