"""
matriz_incidencia_digrafos_17.py
Módulo para representação de Dígrafos por Matriz de Incidência.
"""

# Importa a função de ordenação auxiliar da Tarefa 03 para manter o padrão
from implementacoes.matriz_incidencia_grafos_03 import _chave_ordenacao

def construir_matriz_incidencia(digrafo):
    """
    Constrói a Matriz de Incidência de um dígrafo.
    Origem = +1, Destino = -1.
    """
    # Ordenação determinística
    vertices = sorted(digrafo.obter_vertices(), key=_chave_ordenacao)
    arcos    = sorted(digrafo.obter_arcos(),
                      key=lambda a: (_chave_ordenacao(a[0]),
                                     _chave_ordenacao(a[1])))

    # Cria a matriz zerada (Linhas = Vértices, Colunas = Arcos)
    matriz = [[0] * len(arcos) for _ in range(len(vertices))]

    # Preenche a matriz: +1 na origem (u) e -1 no destino (v)
    for j, (u, v) in enumerate(arcos):
        linha_u = vertices.index(u)
        linha_v = vertices.index(v)
        
        matriz[linha_u][j] = 1   # Origem
        matriz[linha_v][j] = -1  # Destino

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arcos':    arcos
    }

def exibir_incidencia_digrafo(nome_digrafo, mat_inc):
    """Exibe formatada a Matriz de Incidência do Dígrafo."""
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arcos    = mat_inc['arcos']
    
    # Nomes dos arcos para o cabeçalho
    nomes_arcos = [f"({u}->{v})" for u, v in arcos]
    largura_col = max(max(len(n) for n in nomes_arcos), 5) + 2
    comp_linha = max(10 + largura_col * len(arcos), 70)

    print(f"\n{'=' * comp_linha}")
    print(f"  {nome_digrafo}")
    print(f"{'=' * comp_linha}")
    print(f"  Dimensão: {len(vertices)} vértices x {len(arcos)} arcos\n")

    # Cabeçalho
    cabecalho = " " * 9
    for nome in nomes_arcos:
        cabecalho += nome.center(largura_col)
    print(cabecalho)
    print(" " * 8 + "-" * (largura_col * len(arcos) + 2))

    # Linhas
    for i, v in enumerate(vertices):
        prefixo = f"  v={str(v):>3} |"
        celulas = ""
        for j in range(len(arcos)):
            valor = str(matriz[i][j])
            if valor == "1":
                valor = "+1"
            celulas += valor.center(largura_col)
        print(f"{prefixo}{celulas}")