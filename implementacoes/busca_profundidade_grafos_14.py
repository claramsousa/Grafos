"""
busca_profundidade_grafos_14.py
Módulo de implementação da Busca em Profundidade (DFS) com Backtracking.
"""

from implementacoes.matriz_incidencia_grafos_03 import _chave_ordenacao

def busca_profundidade(grafo, v_inicial):
    """
    Realiza a Busca em Profundidade (DFS) começando no vértice especificado.
    """
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    v_inicial = str(v_inicial)
    
    if v_inicial not in [str(x) for x in vertices]:
        return {"erro": f"Vértice inicial '{v_inicial}' não existe no grafo."}

    # Estruturas de estado
    visitado = {v: 0 for v in vertices}
    predecessor = {v: None for v in vertices}
    ordem_visita = []

    # Inicialização
    visitado[v_inicial] = 1
    ordem_visita.append(v_inicial)
    
    P = [v_inicial]  # Pilha (Stack) para o Backtracking

    while P:
        u = P[-1]  # Consulta o topo da pilha
        vizinho_nao_visitado = None
        
        # Busca o primeiro vizinho não visitado em ordem determinística
        vizinhos_ordenados = sorted(grafo.adjacencia[u], key=_chave_ordenacao)
        for w in vizinhos_ordenados:
            if visitado[w] == 0:
                vizinho_nao_visitado = w
                break
        
        if vizinho_nao_visitado is not None:
            w = vizinho_nao_visitado
            visitado[w] = 1
            ordem_visita.append(w)
            predecessor[w] = u
            P.append(w) # Mergulha na profundidade
        else:
            P.pop() # Backtracking: retorna ao pai para procurar outros caminhos

    return {
        'ordem': ordem_visita,
        'predecessor': predecessor
    }

def exibir_resultado_dfs(nome_grafo, v_inicial, resultado):
    """Exibe a ordem de visita e a tabela de predecessores da DFS."""
    print(f"\n{'=' * 60}")
    print(f"  BUSCA EM PROFUNDIDADE: {nome_grafo}")
    print(f"  Vértice Inicial: {v_inicial}")
    print(f"{'=' * 60}")

    if 'erro' in resultado:
        print(f"  [ERRO] {resultado['erro']}\n")
        return

    ordem = resultado['ordem']
    predecessores = resultado['predecessor']
    
    print(f"\n  [1] Ordem dos Vértices Visitados:")
    print(f"      {' -> '.join(str(v) for v in ordem)}")
    print(f"      (Total: {len(ordem)} vértices alcançáveis)")

    print(f"\n  [2] Tabela de Predecessores:")
    print(f"      {'-' * 42}")
    print(f"      | {'Vértice Atual':^16} | {'Predecessor':^17} |")
    print(f"      {'-' * 42}")
    
    for v in ordem:
        pred = predecessores[v]
        txt_v = str(v)
        txt_pred = str(pred) if pred is not None else "--- Raiz ---"
        print(f"      | {txt_v:^16} | {txt_pred:^17} |")
    print(f"      {'-' * 42}\n")