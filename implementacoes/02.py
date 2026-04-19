import sys
import os

# Adiciona o caminho de src para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grafo import ler_grafo

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO DA MATRIZ (Tarefa 02)
# ==============================================================================
def exibir_matriz_adjacencia(nome_grafo, grafo):
    """
    Constrói e exibe a Matriz de Adjacência a partir da lista de adjacência.
    """
    # Ordena os vértices para que a matriz seja determinística (ex: a, b, c...)
    vertices = sorted(grafo.obter_vertices(), key=lambda v: (int(v) if str(v).isdigit() else v))
    n = len(vertices)
    
    print(f"\n{'=' * 65}")
    print(f"  TAREFA (02) — MATRIZ DE ADJACÊNCIA: {nome_grafo}")
    print(f"{'=' * 65}")
    
    # 1. Imprime o cabeçalho com os nomes dos vértices
    header = "      " + " ".join(f"{str(v):>3}" for v in vertices)
    print(header)
    print("     " + "—" * (len(header) - 5))
    
    # 2. Constrói cada linha da matriz
    for v_linha in vertices:
        linha_bits = []
        for v_coluna in vertices:
            # Se v_coluna está na lista de adjacência de v_linha, coloca 1, senão 0
            if v_coluna in grafo.adjacencia[v_linha]:
                linha_bits.append(1)
            else:
                linha_bits.append(0)
        
        # Formata a exibição da linha
        rotulo = f" {str(v_linha):>3} |"
        valores = "".join(f"{x:>4}" for x in linha_bits)
        print(f"{rotulo}{valores}  ]")

# ==============================================================================
# EXECUÇÃO DA TAREFA
# ==============================================================================
if __name__ == '__main__':
    # Define o caminho para a pasta de dados
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    
    # Processa os dois grafos solicitados
    for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
        caminho = os.path.join(base, g_nome)
        
        if os.path.exists(caminho):
            g = ler_grafo(caminho)
            exibir_matriz_adjacencia(g_nome, g)
        else:
            print(f"Arquivo não encontrado: {caminho}")

    print(f"\n{'=' * 65}\n")