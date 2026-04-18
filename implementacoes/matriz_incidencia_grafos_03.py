"""
matriz_incidencia_3.py
------------------------------
Módulo de representação de Grafos por Matriz de Incidência.

Este arquivo pode ser:
1. Executado diretamente para ver os testes com GRAFO_1 e GRAFO_2.
2. Importado em outros scripts usando:
   from matriz_incidencia_3 import construir_matriz_incidencia
"""

import sys
import os

# Adiciona a pasta 'src' ao caminho de busca para que o módulo encontre 'grafo.py'
# independente de onde seja chamado dentro da estrutura do projeto.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_grafo
except ImportError:
    print("Erro: Nao foi possivel encontrar 'src/grafo.py'. Certifique-se de manter a estrutura de pastas.")


# ==============================================================================
# FUNÇÃO AUXILIAR DE ORDENAÇÃO
# ==============================================================================

def _chave_ordenacao(v):
    """
    Chave de ordenacao mista: ordena vertices numericos como inteiros
    e vertices alfanumericos como strings.
    """
    try:
        return (0, int(v))
    except (ValueError, TypeError):
        return (1, str(v))


# ==============================================================================
# FUNÇÃO PRINCIPAL (Exportável)
# ==============================================================================

def construir_matriz_incidencia(grafo):
    """
    Constroi a Matriz de Incidencia de um grafo nao-dirigido.

    Entrada:
        grafo (Grafo): objeto Grafo (da classe em src/grafo.py)

    Saída:
        dict: {
            'matriz': list of list,
            'vertices': list,
            'arestas': list
        }
    """
    # Ordena para garantir que a matriz seja deterministica
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    arestas  = sorted(grafo.obter_arestas(),
                      key=lambda e: (_chave_ordenacao(e[0]),
                                     _chave_ordenacao(e[1])))

    # Cria a matriz zerada (Linhas = Vertices, Colunas = Arestas)
    matriz = [[0] * len(arestas) for _ in range(len(vertices))]

    # Preenche a matriz: cada coluna j tem 1 nas linhas dos seus dois vertices
    for j, (u, v) in enumerate(arestas):
        # Encontra o indice da linha para cada vertice da aresta
        linha_u = vertices.index(u)
        linha_v = vertices.index(v)
        
        matriz[linha_u][j] = 1
        matriz[linha_v][j] = 1

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arestas':  arestas
    }



# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO
# ==============================================================================

def exibir_resultado(nome_grafo, mat_inc):
    """Exibe formatado a Matriz de Incidencia com nomes das arestas no cabecalho."""
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arestas  = mat_inc['arestas']
    
    # Prepara os nomes das arestas para o cabecalho: {u,v}
    nomes_arestas = [f"{{{u},{v}}}" for u, v in arestas]
    
    # Calcula a largura necessaria para cada coluna (baseado no maior nome de aresta)
    # No minimo 5 espacos para nao ficar muito apertado
    largura_col = max(max(len(n) for n in nomes_arestas), 5) + 2

    print(f"\n{'=' * 70}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 70}")
    print(f"  Dimensao da matriz: {len(vertices)} vertices x {len(arestas)} arestas\n")

    # ── Cabecalho: nomes das arestas ─────────────────────────────────────────
    cabecalho = " " * 9
    for nome in nomes_arestas:
        cabecalho += nome.center(largura_col)
    
    print(cabecalho)
    print(" " * 8 + "-" * (largura_col * len(arestas) + 2))

    # ── Linhas: cada vertice com seus valores na matriz ───────────────────────
    for i, v in enumerate(vertices):
        prefixo = f"  v={str(v):>3} |"
        celulas = ""
        for j in range(len(arestas)):
            valor = str(matriz[i][j])
            celulas += valor.center(largura_col)
        print(f"{prefixo}{celulas}")



# ==============================================================================
# EXECUÇÃO DE TESTE (Nao roda quando importado)
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # Teste com GRAFO_1
    path_g1 = os.path.join(base, 'GRAFO_1.txt')
    if os.path.exists(path_g1):
        g1 = ler_grafo(path_g1)
        exibir_resultado('GRAFO_1', construir_matriz_incidencia(g1))

    # Teste com GRAFO_2
    path_g2 = os.path.join(base, 'GRAFO_2.txt')
    if os.path.exists(path_g2):
        g2 = ler_grafo(path_g2)
        exibir_resultado('GRAFO_2', construir_matriz_incidencia(g2))

    print(f"\n{'=' * 62}\n")
