"""
busca_profundidade_grafos_14.py
------------------------------
Busca em Profundidade (DFS) em Grafo

Implementação passo-a-passo baseada no pseudocódigo:
BuscaProfundidade(Grafo G, vértice v)
   v.visitado = 1;
   Cria pilha vazia P;
   EMPILHA(P,v);
   Enquanto P.tamanho > 0 faça
      u = CONSULTA(P);
      Se existe uw ∈ E(G) com w.visitado==0 então
         w.visitado = 1;
         w.predecessor = u;
         EMPILHA(P,w);
      Senão 
          DESEMPILHA(P);
"""

import sys
import os

# Adiciona o caminho de src para importação
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    from grafo import ler_grafo
    from matriz_incidencia_grafos_03 import _chave_ordenacao
except ImportError:
    print("Erro: Não foi possível importar os módulos necessários. Verifique a estrutura de pastas.")


# ==============================================================================
# FUNÇÃO PRINCIPAL DA BUSCA (Exportável)
# ==============================================================================

def busca_profundidade(grafo, v_inicial):
    """
    Realiza a Busca em Profundidade (DFS) começando no vértice especificado.

    Entrada:
        grafo (Grafo): objeto Grafo lido (src/grafo.py)
        v_inicial (str|int): o vértice inicial de partida

    Saída:
        dict com as chaves:
            'ordem': lista contendo a ordem em que os vértices foram marcados como visitados
            'predecessor': dicionário apontando quem é o predecessor de cada vértice na árvore
    """
    vertices = sorted(grafo.obter_vertices(), key=_chave_ordenacao)
    
    # Verifica se o vértice inicial realmente existe no grafo
    if str(v_inicial) not in [str(x) for x in vertices]:
        return {"erro": f"Vértice inicial '{v_inicial}' nao existe no grafo."}

    # Assegura o tipo correto com base no dicionário do grafo
    # (por exemplo se passamos '1' mas o vértice internamente é lido como string)
    v_inicial = str(v_inicial)

    # 1. Estruturas para registrar estados: visitado e predecessor
    visitado = {v: 0 for v in vertices}
    predecessor = {v: None for v in vertices}
    ordem_visita = []

    # 2. Inicialização do nó de partida
    visitado[v_inicial] = 1
    ordem_visita.append(v_inicial)
    
    P = []  # Cria pilha vazia P
    P.append(v_inicial) # EMPILHA(P, v_inicial)

    # 3. Laço principal
    while len(P) > 0:
        u = P[-1]  # u = CONSULTA(P)

        vizinho_nao_visitado = None
        
        # Para garantir o mesmo resultado que um teste de mesa,
        # ordenamos a lista de vizinhos e buscamos o PRIMEIRO não-visitado.
        vizinhos_ordenados = sorted(grafo.adjacencia[u], key=_chave_ordenacao)
        
        for w in vizinhos_ordenados:
            if visitado[w] == 0:
                vizinho_nao_visitado = w
                break
        
        # Se existe um vizinho 'w' de 'u' com visitado==0
        if vizinho_nao_visitado is not None:
            w = vizinho_nao_visitado
            visitado[w] = 1          # w.visitado = 1
            ordem_visita.append(w)   # anota a visita
            predecessor[w] = u       # w.predecessor = u
            P.append(w)              # EMPILHA(P, w)
        else:
            P.pop()                  # DESEMPILHA(P)

    return {
        'ordem': ordem_visita,
        'predecessor': predecessor
    }


# ==============================================================================
# FUNÇÃO DE EXIBIÇÃO FORMATADA
# ==============================================================================

def exibir_resultado_dfs(nome_grafo, v_inicial, resultado):
    """
    Exibe a ordem de visita e a tabela com vértices e predecessores.
    """
    print(f"\n{'=' * 60}")
    print(f"  BUSCA EM PROFUNDIDADE: {nome_grafo}")
    print(f"  Vértice Inicial: {v_inicial}")
    print(f"{'=' * 60}")

    if 'erro' in resultado:
        print(f"  [ERRO] {resultado['erro']}\n")
        return

    ordem = resultado['ordem']
    predecessores = resultado['predecessor']
    
    # ── 1. Exibir Ordem de Vértices Visitados ─────────────────────────────────
    print(f"\n  [1] Ordem dos Vértices Visitados:")
    caminho = " -> ".join(str(v) for v in ordem)
    print(f"      {caminho}")
    print(f"      (Total: {len(ordem)} vértices alcançáveis)")

    # ── 2. Exibir Tabelinha de Predecessores ──────────────────────────────────
    print(f"\n  [2] Tabela de Predecessores:")
    print(f"      {'-' * 42}")
    print(f"      | {'Vértice Atual':^16} | {'Predecessor':^17} |")
    print(f"      {'-' * 42}")
    
    for v in ordem:
        pred = predecessores[v]
        txt_v = str(v)
        txt_pred = str(pred) if pred is not None else "--- Raiz ---"
        print(f"      | {txt_v:^16} | {txt_pred:^17} |")
    print(f"      {'-' * 42}\n\n")


# ==============================================================================
# EXECUÇÃO DA DEMONSTRAÇÃO DO SCRIPT
# ==============================================================================

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # ---- TESTE COM O GRAFO_1 ----
    path_g1 = os.path.join(base, 'GRAFO_1.txt')
    if os.path.exists(path_g1):
        g1 = ler_grafo(path_g1)
        # Vamos rodar a busca a partir do vértice 'a' (pode ser o que vc quiser)
        res_g1 = busca_profundidade(g1, v_inicial='d')
        exibir_resultado_dfs("GRAFO_1", 'd', res_g1)

    # ---- TESTE COM O GRAFO_3 ----
    path_g3 = os.path.join(base, 'GRAFO_3.txt')
    if os.path.exists(path_g3):
        g3 = ler_grafo(path_g3)
        # Rodando a partir do vértice '1' caso seja um grafo numérico (se '1' for válido)
        # Pegamos dinamicamente o primeiro vértice
        vertices_g3 = sorted(g3.obter_vertices(), key=_chave_ordenacao)
        if vertices_g3:
            # Pega o vértice raiz, por exemplo '1' ou qual seja o primeiro
            v_ini_3 = vertices_g3[0] 
            res_g3 = busca_profundidade(g3, v_inicial='g')
            exibir_resultado_dfs("GRAFO_3", 'g', res_g3)
