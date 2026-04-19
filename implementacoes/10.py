import sys
import os

# Adiciona o caminho de src para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from grafo import ler_grafo

def exibir_resultado_detalhado(nome_grafo, grafo, titulo):
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
    # CORREÇÃO AQUI: 'dados-trabalho_1'
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')
    caminho = os.path.join(base, 'GRAFO_1.txt')
    
    if os.path.exists(caminho):
        g_exclusao = ler_grafo(caminho)
        exibir_resultado_detalhado('GRAFO_1', g_exclusao, "ESTADO ORIGINAL")

        v_alvo = "a"
        print(f"\n[Tarefa 10] Removendo o vértice '{v_alvo}'...")
        if g_exclusao.remover_vertice(v_alvo):
            exibir_resultado_detalhado('GRAFO_1', g_exclusao, "APÓS EXCLUSÃO")
        else:
            print(f"Erro: Vértice '{v_alvo}' não encontrado.")
    else:
        print(f"Arquivo não encontrado em: {caminho}")