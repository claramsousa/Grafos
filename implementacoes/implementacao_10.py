"""
implementacao_10.py
Módulo focado na exibição detalhada do estado do grafo após a exclusão de vértices.
"""

def exibir_resultado_detalhado(nome_grafo, grafo, titulo):
    """
    Exibe o estado completo do grafo (Vértices, Arestas e Lista de Adjacência).
    Formatado para mostrar o impacto de inclusões ou exclusões.
    """
    # Ordenação mista (números antes de letras)
    vertices = sorted(grafo.obter_vertices(), key=lambda x: (str(x).isnumeric(), str(x)))
    
    print(f"\n{'=' * 50}")
    print(f"  {titulo}: {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Vértices ({len(vertices)}): {vertices}")
    print(f"  Arestas  ({len(grafo.obter_arestas())})")
    print(f"  Lista de Adjacência:")
    
    for v in vertices:
        # Formata vértices numéricos com zero à esquerda para alinhamento
        rotulo_fmt = f"{int(v):02}" if str(v).isnumeric() else str(v)
        vizinhos = sorted(grafo.adjacencia[v], key=lambda x: str(x))
        print(f"    {rotulo_fmt}: {vizinhos}")