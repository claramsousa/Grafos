"""
matriz_incidencia_digrafos_17.py
------------------------------
Módulo de representação de Dígrafos por Matriz de Incidência.

Este arquivo pode ser:
1. Executado diretamente para ver os testes com DIGRAFO1 e DIGRAFO2.
2. Importado em outros scripts usando:
   from matriz_incidencia_digrafos_17 import construir_matriz_incidencia
"""

import sys
import os

# Adiciona a pasta 'src' ao caminho de busca para que o módulo encontre 'grafo.py'
# independente de onde seja chamado dentro da estrutura do projeto.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_digrafo
    # Importa a função de ordenação auxiliar do arquivo de grafos para evitar duplicação
    from matriz_incidencia_grafos_03 import _chave_ordenacao
except ImportError:
    print("Erro: Nao foi possivel encontrar os modulos necessarios. Certifique-se de manter a estrutura de pastas.")

# ==============================================================================
# FUNÇÃO PRINCIPAL (Exportável)
# ==============================================================================

def construir_matriz_incidencia(digrafo):
    """
    Constroi a Matriz de Incidencia de um digrafo.

    Entrada:
        digrafo (Digrafo): objeto Digrafo (da classe em src/grafo.py)

    Saída:
        dict: {
            'matriz': list of list,
            'vertices': list,
            'arcos': list
        }
    """
    # Ordena para garantir que a matriz seja deterministica
    vertices = sorted(digrafo.obter_vertices(), key=_chave_ordenacao)
    arcos    = sorted(digrafo.obter_arcos(),
                      key=lambda a: (_chave_ordenacao(a[0]),
                                     _chave_ordenacao(a[1])))

    # Cria a matriz zerada (Linhas = Vertices, Colunas = Arcos)
    matriz = [[0] * len(arcos) for _ in range(len(vertices))]

    # Preenche a matriz: cada coluna j tem +1 na origem e -1 no destino
    for j, (u, v) in enumerate(arcos):
        # Encontra o indice da linha para cada vertice do arco
        linha_u = vertices.index(u)
        linha_v = vertices.index(v)
        
        matriz[linha_u][j] = 1   # u eh origem
        matriz[linha_v][j] = -1  # v eh destino

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arcos':    arcos
    }



# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

def exibir_resultado(nome_digrafo, mat_inc):
    """Exibe formatado a Matriz de Incidencia com nomes dos arcos no cabecalho."""
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arcos    = mat_inc['arcos']
    
    # Prepara os nomes dos arcos para o cabecalho: (u->v)
    nomes_arcos = [f"({u}->{v})" for u, v in arcos]
    
    # Calcula a largura necessaria para cada coluna (baseado no maior nome de arco)
    # No minimo 5 espacos para nao ficar muito apertado
    largura_col = max(max(len(n) for n in nomes_arcos), 5) + 2

    comp_linha = 10 + largura_col * len(arcos)
    comp_linha = comp_linha if comp_linha > 70 else 70

    print(f"\n{'=' * comp_linha}")
    print(f"  {nome_digrafo}")
    print(f"{'=' * comp_linha}")
    print(f"  Dimensao da matriz: {len(vertices)} vertices x {len(arcos)} arcos\n")

    # ── Cabecalho: nomes dos arcos ─────────────────────────────────────────
    cabecalho = " " * 9
    for nome in nomes_arcos:
        cabecalho += nome.center(largura_col)
    
    print(cabecalho)
    print(" " * 8 + "-" * (largura_col * len(arcos) + 2))

    # ── Linhas: cada vertice com seus valores na matriz ───────────────────────
    for i, v in enumerate(vertices):
        prefixo = f"  v={str(v):>3} |"
        celulas = ""
        for j in range(len(arcos)):
            valor = str(matriz[i][j])
            if valor == "1":
                valor = "+1"
            celulas += valor.center(largura_col)
        print(f"{prefixo}{celulas}")



# ==============================================================================
# EXECUÇÃO DE TESTE (Nao roda quando importado)
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # Teste com DIGRAFO1
    path_d1 = os.path.join(base, 'DIGRAFO1.txt')
    if os.path.exists(path_d1):
        d1 = ler_digrafo(path_d1)
        exibir_resultado('DIGRAFO1', construir_matriz_incidencia(d1))

    # Teste com DIGRAFO2
    path_d2 = os.path.join(base, 'DIGRAFO2.txt')
    if os.path.exists(path_d2):
        d2 = ler_digrafo(path_d2)
        exibir_resultado('DIGRAFO2', construir_matriz_incidencia(d2))

    print(f"\n{'=' * 70}\n")