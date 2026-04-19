"""
busca_profundidade_digrafos_20.py
Módulo para Busca em Profundidade em Dígrafos com tempos e classificação de arestas.
"""

from implementacoes.matriz_incidencia_grafos_03 import _chave_ordenacao

def busca_profundidade_digrafo(grafo, v_inicial):
    """
    Realiza a DFS calculando tempos de entrada (d) e saída (f).
    Classifica arestas em: Árvore, Retorno, Avanço e Cruzamento.
    """
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    v_inicial = str(v_inicial)
    
    if v_inicial not in [str(x) for x in vertices]:
        return {"erro": f"Vértice inicial '{v_inicial}' não existe no grafo."}

    # Estados: 0: BRANCO, 1: CINZA, 2: PRETO
    cor = {v: 0 for v in vertices}
    d = {v: 0 for v in vertices} # Descoberta
    f = {v: 0 for v in vertices} # Finalização
    predecessor = {v: None for v in vertices}
    ordem_visita = []
    arestas_classificacao = []
    
    adj_ordenada = {v: sorted(grafo.adjacencia[v], key=_chave_ordenacao) for v in vertices}
    proximo_vizinho_idx = {v: 0 for v in vertices}
    tempo = [1] 

    def dfs_visit(inicio):
        cor[inicio] = 1 
        d[inicio] = tempo[0]
        tempo[0] += 1
        ordem_visita.append(inicio)
        
        P = [inicio] # Pilha de recursão simulada
        
        while P:
            u = P[-1]
            if proximo_vizinho_idx[u] < len(adj_ordenada[u]):
                w = adj_ordenada[u][proximo_vizinho_idx[u]]
                proximo_vizinho_idx[u] += 1
                
                if cor[w] == 0: # Vértice não visitado
                    arestas_classificacao.append((u, w, "Árvore"))
                    cor[w] = 1 
                    d[w] = tempo[0]
                    tempo[0] += 1
                    predecessor[w] = u
                    ordem_visita.append(w)
                    P.append(w)
                elif cor[w] == 1: # Vértice na pilha
                    arestas_classificacao.append((u, w, "Retorno"))
                elif cor[w] == 2: # Vértice já finalizado
                    if d[u] < d[w]:
                        arestas_classificacao.append((u, w, "Avanço"))
                    else:
                        arestas_classificacao.append((u, w, "Cruzamento"))
            else:
                P.pop()
                cor[u] = 2 
                f[u] = tempo[0]
                tempo[0] += 1

    # Inicia a busca pelo vértice prioritário
    dfs_visit(v_inicial)
    
    # Cobre os demais vértices (floresta DFS)
    for v in vertices:
        if cor[v] == 0:
            dfs_visit(v)

    return {
        'ordem': ordem_visita,
        'predecessor': predecessor,
        'd': d, 'f': f,
        'arestas': arestas_classificacao
    }

def exibir_dfs_digrafo(nome_grafo, v_inicial, resultado):
    """Exibe o relatório formatado da DFS para Dígrafos."""
    print(f"\n{'=' * 75}\n  DFS EM DÍGRAFO: {nome_grafo} (Início: {v_inicial})\n{'=' * 75}")

    if 'erro' in resultado:
        print(f"  [ERRO] {resultado['erro']}\n"); return

    ordem = resultado['ordem']
    
    print(f"\n  [1] Ordem dos Vértices Visitados:")
    print(f"      {' -> '.join(str(v) for v in ordem)}")
    print(f"      (Total: {len(ordem)} vértices alcançados)\n")

    print(f"  [2] Tabela de Tempos e Predecessores:")
    print(f"      {'-' * 62}")
    print(f"      | {'Vértice':^9} | {'d[v] (Ent)':^12} | {'f[v] (Sai)':^12} | {'Predecessor':^15} |")
    print(f"      {'-' * 62}")
    for v in ordem:
        print(f"      | {str(v):^9} | {str(resultado['d'][v]):^12} | {str(resultado['f'][v]):^12} | {str(resultado['predecessor'][v] or '---'):^15} |")

    print(f"\n  [3] Classificação das Arestas:")
    print(f"      {'-' * 39}")
    print(f"      | {'Aresta (u -> w)':^17} | {'Tipo':^15} |")
    print(f"      {'-' * 39}")
    for u, w, tipo in resultado['arestas']:
        print(f"      | {f'({u}, {w})':^17} | {tipo:^15} |")
    print(f"      {'-' * 39}\n")