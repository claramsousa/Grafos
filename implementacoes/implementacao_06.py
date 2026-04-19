"""
implementacao_06.py
Módulo para determinar a adjacência entre vértices.
"""

def sao_adjacentes(grafo, u, v):
    """
    Determina se dois vértices u e v são adjacentes no grafo.
    """
    u, v = str(u), str(v)  # Garante que os identificadores sejam strings
    
    # Verifica se os vértices existem no grafo
    if u not in grafo.adjacencia or v not in grafo.adjacencia:
        return False
        
    # No Grafo não-dirigido, basta checar se v está na lista de adjacência de u
    return v in grafo.adjacencia[u]

def testar_e_exibir(nome_grafo, grafo, par_testes):
    """
    Executa testes de adjacência e exibe o resultado formatado no terminal.
    """
    print(f"\n{'=' * 60}")
    print(f"  TAREFA (06) — VERIFICAÇÃO DE ADJACÊNCIA: {nome_grafo}")
    print(f"{'=' * 60}")
    
    for u, v in par_testes:
        resultado = sao_adjacentes(grafo, u, v)
        status = "SÃO ADJACENTES" if resultado else "NÃO SÃO ADJACENTES"
        print(f"  Vértices ({u}) e ({v}): {status}")