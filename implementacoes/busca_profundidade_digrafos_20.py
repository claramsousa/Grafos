"""
busca_profundidade_digrafos_20.py
---------------------------------
Busca em Profundidade (DFS) em Digrafos (Grafos Direcionados)

Implementação com determinação de:
- Profundidade de entrada (descoberta, d[v])
- Profundidade de saída (finalização, f[v])
- Classificação de arestas (Árvore, Retorno, Avanço, Cruzamento)
"""

import sys
import os

# Adiciona o caminho de src para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_digrafo
    from matriz_incidencia_grafos_03 import _chave_ordenacao
except ImportError:
    print("Erro: Não foi possível importar os módulos necessários. Verifique a estrutura de pastas.")


# ==============================================================================
# FUNÇÃO PRINCIPAL DA BUSCA (DFS EM DIGRAFO)
# ==============================================================================

def busca_profundidade_digrafo(grafo, v_inicial):
    """
    Realiza a Busca em Profundidade (DFS) começando no vértice especificado
    e cobrindo os demais vértices do digrafo, caso haja componentes desconectadas.
    """
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    
    if str(v_inicial) not in [str(x) for x in vertices]:
        return {"erro": f"Vértice inicial '{v_inicial}' nao existe no grafo."}

    v_inicial = str(v_inicial)

    # 0: BRANCO (não descoberto), 1: CINZA (em P / pilha), 2: PRETO (totalmente explorado)
    cor = {v: 0 for v in vertices}
    
    # Tempos de descoberta (d) e finalização (f)
    d = {v: 0 for v in vertices}
    f = {v: 0 for v in vertices}
    
    predecessor = {v: None for v in vertices}
    ordem_visita = []
    arestas_classificacao = []
    
    # Para garantir a mesma ordem determinística em cada execução
    adj_ordenada = {v: sorted(grafo.adjacencia[v], key=_chave_ordenacao) for v in vertices}
    
    # Índice para não precisarmos procurar do zero toda vez 
    # (controla a iteração de arestas incidentes)
    proximo_vizinho_idx = {v: 0 for v in vertices}
    
    tempo = [1] # Usando lista simples como referência (pass-by-reference)

    def dfs_visit(inicio):
        cor[inicio] = 1 # CINZA
        d[inicio] = tempo[0]
        tempo[0] += 1
        ordem_visita.append(inicio)
        
        P = [inicio]
        
        while len(P) > 0:
            u = P[-1]
            
            # Enquanto houver vizinhos a explorar para o vértice 'u'
            if proximo_vizinho_idx[u] < len(adj_ordenada[u]):
                w = adj_ordenada[u][proximo_vizinho_idx[u]]
                proximo_vizinho_idx[u] += 1
                
                # Classificação da aresta (u, w)
                if cor[w] == 0:
                    arestas_classificacao.append((u, w, "Árvore"))
                    cor[w] = 1 # CINZA
                    d[w] = tempo[0]
                    tempo[0] += 1
                    predecessor[w] = u
                    ordem_visita.append(w)
                    P.append(w)
                elif cor[w] == 1:
                    arestas_classificacao.append((u, w, "Retorno"))
                elif cor[w] == 2:
                    # Se w já foi totalmente processado
                    if d[u] < d[w]:
                        arestas_classificacao.append((u, w, "Avanço"))
                    else:
                        arestas_classificacao.append((u, w, "Cruzamento"))
            else:
                # Todos os vizinhos explorados, podemos finalizar 'u'
                P.pop()
                cor[u] = 2 # PRETO
                f[u] = tempo[0]
                tempo[0] += 1

    # 1. Iniciar pelo vértice escolhido
    dfs_visit(v_inicial)
    
    # 2. Iterar sobre todos os outros (se desconexo, descobre as demais florestas)
    for v in vertices:
        if cor[v] == 0:
            dfs_visit(v)

    return {
        'ordem': ordem_visita,
        'predecessor': predecessor,
        'd': d,
        'f': f,
        'arestas': arestas_classificacao,
        'cor': cor
    }


# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO FORMATADA
# ==============================================================================

def exibir_resultado_dfs(nome_grafo, v_inicial, resultado):
    """
    Exibe os dados coletados pela DFS em um formato organizado.
    """
    print(f"\n{'=' * 75}")
    print(f"  BUSCA EM PROFUNDIDADE: {nome_grafo}")
    print(f"  Vértice Inicial Priorizado: {v_inicial}")
    print(f"{'=' * 75}")

    if 'erro' in resultado:
        print(f"  [ERRO] {resultado['erro']}\n")
        return

    ordem = resultado['ordem']
    predecessores = resultado['predecessor']
    d = resultado['d']
    f = resultado['f']
    arestas = resultado['arestas']
    cor = resultado['cor']
    
    # ── 1. Exibir Ordem de Vértices Visitados (Descoberta) ────────────────────
    print(f"\n  [1] Ordem Global de Descoberta:")
    caminho = " -> ".join(str(v) for v in ordem)
    print(f"      {caminho}")

    # ── 2. Exibir Tabela de Tempos e Predecessores ────────────────────────────
    print(f"\n  [2] Tabela de Tempos (Entrada / Saída) e Predecessores:")
    print(f"      {'-' * 62}")
    print(f"      | {'Vértice':^9} | {'d[v] (Ent)':^12} | {'f[v] (Sai)':^12} | {'Predecessor':^15} |")
    print(f"      {'-' * 62}")
    
    # Mostrar na ordem de descoberta ou ordenado alfa-numericamente, alfa fica legal.
    # Mas mostrar pela ordem de descoberta ajuda a entender a árvore
    for v in ordem:
        txt_v = str(v)
        txt_d = str(d[v])
        txt_f = str(f[v])
        pred = predecessores[v]
        txt_pred = str(pred) if pred is not None else "---"
        
        print(f"      | {txt_v:^9} | {txt_d:^12} | {txt_f:^12} | {txt_pred:^15} |")
    print(f"      {'-' * 62}")

    # ── 3. Exibir Classificação de Arestas ────────────────────────────────────
    print(f"\n  [3] Classificação das Arestas:")
    print(f"      {'-' * 39}")
    print(f"      | {'Aresta (u -> w)':^17} | {'Tipo':^15} |")
    print(f"      {'-' * 39}")
    
    if len(arestas) == 0:
        print(f"      | {'Nenhuma aresta explorada':^35} |")
    else:
        for u, w, tipo in arestas:
            txt_aresta = f"({u}, {w})"
            print(f"      | {txt_aresta:^17} | {tipo:^15} |")
    print(f"      {'-' * 39}\n\n")


# ==============================================================================
# EXECUÇÃO DA DEMONSTRAÇÃO DO SCRIPT
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # ---- TESTE COM O DIGRAFO_2 ----
    path_d2 = os.path.join(base, 'DIGRAFO2.txt')
    if os.path.exists(path_d2):
        d2 = ler_digrafo(path_d2)
        # Identificar dinamicamente o primeiro vértice
        vertices_d2 = sorted(d2.obter_vertices(), key=_chave_ordenacao)
        if vertices_d2:
            v_ini_2 = vertices_d2[0]
            res_d2 = busca_profundidade_digrafo(d2, v_inicial=v_ini_2)
            exibir_resultado_dfs("DIGRAFO2.txt", v_ini_2, res_d2)
    else:
        print(f"Arquivo não encontrado: {path_d2}")

    # ---- TESTE COM O DIGRAFO_3 ----
    path_d3 = os.path.join(base, 'DIGRAFO3.txt')
    if os.path.exists(path_d3):
        d3 = ler_digrafo(path_d3)
        vertices_d3 = sorted(d3.obter_vertices(), key=_chave_ordenacao)
        if vertices_d3:
            v_ini_3 = vertices_d3[0]
            res_d3 = busca_profundidade_digrafo(d3, v_inicial='g')
            exibir_resultado_dfs("DIGRAFO3.txt", 'g', res_d3)
    else:
        print(f"Arquivo não encontrado: {path_d3}")
