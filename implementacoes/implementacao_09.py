import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grafo import ler_grafo

def exibir_resultado_detalhado(nome_grafo, grafo, titulo):
    """Exibe o estado do grafo no formato solicitado."""
    vertices = sorted(grafo.obter_vertices(), key=lambda x: (str(x).isnumeric(), str(x)))
    print(f"\n{'=' * 50}")
    print(f"  {titulo}: {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Vértices ({len(vertices)}): {vertices}")
    print(f"  Arestas  ({len(grafo.obter_arestas())})")
    print(f"  Lista de Adjacência:")
    for v in vertices:
        rotulo_fmt = f"{int(v):02}" if str(v).isnumeric() else str(v)
        vizinhos = sorted(grafo.adjacencia[v], key=lambda x: str(x))
        print(f"    {rotulo_fmt}: {vizinhos}")

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    caminho = os.path.join(base, 'GRAFO_1.txt')
    
    if os.path.exists(caminho):
        # 1. Estado Original
        g_inclusao = ler_grafo(caminho)
        exibir_resultado_detalhado('GRAFO_1', g_inclusao, "ESTADO ORIGINAL")

        # 2. Execução da Tarefa 9
        novo_v = "Z"
        print(f"\n[Tarefa 9] Incluindo o vértice '{novo_v}'...")
        g_inclusao.adicionar_vertice(novo_v)
        
        # 3. Estado Final
        exibir_resultado_detalhado('GRAFO_1', g_inclusao, "APÓS INCLUSÃO")
    else:
        print("Arquivo não encontrado.")