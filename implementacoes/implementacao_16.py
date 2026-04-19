"""
implementacao_16.py
Módulo para exibição da Matriz de Adjacência de Grafos Direcionados (Dígrafos).
"""

def exibir_matriz_digrafo(nome_digrafo, digrafo):
    """
    Constrói e exibe a Matriz de Adjacência para Dígrafos.
    As linhas representam a ORIGEM e as colunas o DESTINO.
    """
    # Ordenação natural (números antes de letras, 10 vem depois de 2)
    vertices = sorted(digrafo.obter_vertices(), key=lambda v: (int(v) if str(v).isdigit() else v))
    n = len(vertices)
    
    print(f"\n{'=' * 65}")
    print(f"   TAREFA (16) — MATRIZ DE ADJACÊNCIA (DÍGRAFO): {nome_digrafo}")
    print(f"{'=' * 65}")
    
    # Cabeçalho com os nomes dos vértices (Destinos)
    header = "      " + " ".join(f"{str(v):>3}" for v in vertices)
    print(header)
    print("     " + "—" * (len(header) - 5))
    
    # Construção das linhas (Origens)
    for u in vertices:
        linha_bits = []
        for v in vertices:
            # No Dígrafo, a adjacência só é 1 se houver arco de u para v
            if v in digrafo.adjacencia[u]:
                linha_bits.append(1)
            else:
                linha_bits.append(0)
        
        rotulo = f" {str(u):>3} |"
        valores = "".join(f"{x:>4}" for x in linha_bits)
        print(f"{rotulo}{valores}   ]")