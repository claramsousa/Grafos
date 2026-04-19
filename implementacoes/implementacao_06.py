import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grafo import ler_grafo

# ==============================================================================
# FUNÇÃO DE VERIFICAÇÃO 
# ==============================================================================
def sao_adjacentes(grafo, u, v):
    """
    Determina se dois vértices u e v são adjacentes no grafo.
    """
    u, v = str(u), str(v)  
    
    # Verifica se os vértices existem no grafo
    if u not in grafo.adjacencia or v not in grafo.adjacencia:
        return False
        
    # No Grafo não-dirigido, checar se v está na lista de u
    return v in grafo.adjacencia[u]

# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO LOCAL
# ==============================================================================
def testar_e_exibir(nome_grafo, grafo, par_testes):
    """
    Executa testes de adjacência e exibe o resultado formatado.
    """
    print(f"\n{'=' * 60}")
    print(f"  TAREFA (06) — VERIFICAÇÃO DE ADJACÊNCIA: {nome_grafo}")
    print(f"{'=' * 60}")
    
    for u, v in par_testes:
        resultado = sao_adjacentes(grafo, u, v)
        status = "SÃO ADJACENTES" if resultado else "NÃO SÃO ADJACENTES"
        print(f"  Vértices ({u}) e ({v}): {status}")

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    
    # --- TESTES NO GRAFO 1 ---
    caminho_g1 = os.path.join(base, 'GRAFO_1.txt')
    if os.path.exists(caminho_g1):
        g1 = ler_grafo(caminho_g1)
        # Pares para testar: (a,b) existe; (a,c) não existe
        testes_g1 = [('a', 'b'), ('a', 'c'), ('b', 'e'), ('b', 'd'), ('b', 'f'), ('c', 'e'), ('c', 'f'), ('e', 'h'), ('h', 'd')]
        testar_e_exibir('GRAFO_1.txt', g1, testes_g1)

    # --- TESTES NO GRAFO 2 ---
    caminho_g2 = os.path.join(base, 'GRAFO_2.txt')
    if os.path.exists(caminho_g2):
        g2 = ler_grafo(caminho_g2)
        # Pares para testar: (1,2) existe; (1,10) não existe
        testes_g2 = [(1, 2), (1, 10), (10, 11), (8, 9)]
        testar_e_exibir('GRAFO_2.txt', g2, testes_g2)

    print(f"\n{'=' * 60}\n")