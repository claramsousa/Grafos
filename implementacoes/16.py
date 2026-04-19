import sys
import os

# Adiciona o caminho de src para importação (Padrão do grupo)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grafo import ler_digrafo

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO DA MATRIZ (Tarefa 16)
# ==============================================================================
def exibir_matriz_digrafo(nome_digrafo, digrafo):
    """
    Constrói e exibe a Matriz de Adjacência para grafos direcionados (Dígrafos).
    """
    # Ordenação natural: garante que '10' venha depois de '2'
    vertices = sorted(digrafo.obter_vertices(), key=lambda v: (int(v) if str(v).isdigit() else v))
    n = len(vertices)
    
    print(f"\n{'=' * 65}")
    print(f"  TAREFA (16) — MATRIZ DE ADJACÊNCIA (DÍGRAFO): {nome_digrafo}")
    print(f"{'=' * 65}")
    
    # 1. Cabeçalho com os nomes dos vértices
    header = "      " + " ".join(f"{str(v):>3}" for v in vertices)
    print(header)
    print("     " + "—" * (len(header) - 5))
    
    # 2. Construção das linhas (De -> Para)
    for u in vertices:
        linha_bits = []
        for v in vertices:
            # No Dígrafo, verificamos se v está na lista de sucessores de u
            if v in digrafo.adjacencia[u]:
                linha_bits.append(1)
            else:
                linha_bits.append(0)
        
        rotulo = f" {str(u):>3} |"
        valores = "".join(f"{x:>4}" for x in linha_bits)
        print(f"{rotulo}{valores}  ]")

# ==============================================================================
# EXECUÇÃO DA TAREFA
# ==============================================================================
if __name__ == '__main__':
    # Define o caminho para os dados
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    
    for d_nome in ['DIGRAFO1.txt', 'DIGRAFO2.txt']:
        caminho = os.path.join(base, d_nome)
        
        if os.path.exists(caminho):
            # Usa a leitura específica para dígrafos do projeto
            d = ler_digrafo(caminho)
            exibir_matriz_digrafo(d_nome, d)
        else:
            print(f"Arquivo não encontrado em: {caminho}")

    print(f"\n{'=' * 65}\n")