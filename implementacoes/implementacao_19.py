"""
19.py
------------------------------------
IMPLEMENTAÇÃO 19 — Conversão de matriz de incidência para estrela direta e vice versa

═══════════════════════════════════════════════════════════════════
 ESTRUTURAS DE DADOS PARA DÍGRAFOS
═══════════════════════════════════════════════════════════════════

1. MATRIZ DE INCIDÊNCIA (M)
   ─────────────────────────
   Matriz de dimensão |V| × |A|  (vértices × arcos).
   Para cada arco a = (u → v):
       M[u][a] = +1   (u é ORIGEM do arco)
       M[v][a] = -1   (v é DESTINO do arco)
       M[w][a] =  0   (w não participa do arco)

   Propriedades:
     - Cada coluna tem exatamente um +1 e um -1 (e o restante 0).
     - Permite identificar grau de entrada e saída de cada vértice.

2. ESTRELA DIRETA (Forward Star)
   ─────────────────────────────
   Representação compacta orientada para travessia dos SUCESSORES.
   Composta por dois vetores:
     • APONTA[v]  : índice no vetor DEST onde começam os arcos que
                    SAEM do vértice v  (sentinela: APONTA[|V|+1] = |A|+1)
     • DEST[k]    : destino do k-ésimo arco (arcos ordenados por origem)

   Para listar todos os arcos que saem de v:
       para k de APONTA[v] até APONTA[v+1]-1:
           destino = DEST[k]

   Ordenação: arcos agrupados por vértice de ORIGEM, e dentro de cada
   grupo, ordenados pelo vértice de DESTINO (para determinismo).

3. ESTRELA INVERSA (Reverse Star)  — bônus, derivada da Estrela Direta
   ─────────────────────────────────────────────────────────────────────
   Mesma ideia, mas orientada para travessia dos PREDECESSORES.
     • APONTA_INV[v]: índice onde começam os arcos que CHEGAM em v
     • ORIG[k]      : origem do k-ésimo arco (arcos ordenados por destino)

═══════════════════════════════════════════════════════════════════
 CONVERSÕES IMPLEMENTADAS
═══════════════════════════════════════════════════════════════════
  (A) Dígrafo (lista de arcos)  →  Matriz de Incidência
  (B) Dígrafo (lista de arcos)  →  Estrela Direta
  (C) Matriz de Incidência      →  Estrela Direta
  (D) Estrela Direta            →  Matriz de Incidência

Dígrafo avaliado: DIGRAFO1
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from grafo import ler_digrafo


# ══════════════════════════════════════════════════════════════════
# (A) DÍGRAFO → MATRIZ DE INCIDÊNCIA
# ══════════════════════════════════════════════════════════════════

def construir_matriz_incidencia(digrafo):
    """
    Constrói a Matriz de Incidência de um dígrafo.

    A matriz tem dimensão |V| × |A|.
    Para cada arco a = (u → v):
        M[u][a] = +1  (vértice de origem)
        M[v][a] = -1  (vértice de destino)
        demais  =  0

    Entrada:
        digrafo (Digrafo): objeto Digrafo já lido/construído

    Saída:
        dict com as chaves:
            'matriz'    (list of list): matriz |V|×|A| com valores -1, 0, +1
            'vertices'  (list): vértices ordenados (índices das linhas)
            'arcos'     (list): arcos ordenados como tuplas (u,v)
                                (índices das colunas)
            'idx_v'     (dict): mapeamento vértice → índice de linha
            'idx_a'     (dict): mapeamento arco(tupla) → índice de coluna
    """
    # Ordena vértices e arcos para indexação determinística
    vertices = sorted(digrafo.obter_vertices(), key=str)
    arcos    = sorted(digrafo.obter_arcos(),
                      key=lambda a: (str(a[0]), str(a[1])))

    n = len(vertices)   # número de vértices
    m = len(arcos)      # número de arcos

    # Mapas de índice para acesso direto
    idx_v = {v: i for i, v in enumerate(vertices)}  # vértice → linha
    idx_a = {a: j for j, a in enumerate(arcos)}     # arco    → coluna

    # Inicializa matriz com zeros
    matriz = [[0] * m for _ in range(n)]

    # Preenche +1 (origem) e -1 (destino) para cada arco
    for (u, v) in arcos:
        j = idx_a[(u, v)]
        matriz[idx_v[u]][j] = +1   # u é origem → +1
        matriz[idx_v[v]][j] = -1   # v é destino → -1

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arcos':    arcos,
        'idx_v':    idx_v,
        'idx_a':    idx_a
    }


# ══════════════════════════════════════════════════════════════════
# (B) DÍGRAFO → ESTRELA DIRETA
# ══════════════════════════════════════════════════════════════════

def construir_estrela_direta(digrafo):
    """
    Constrói a representação em Estrela Direta (Forward Star) do dígrafo.

    Os arcos são ordenados primeiramente pelo vértice de ORIGEM e,
    dentro de cada grupo, pelo vértice de DESTINO.

    APONTA[i] indica o índice (base 1) no vetor DEST onde começam
    os arcos que saem do vértice vertices[i-1].
    Sentinela: APONTA[|V|+1] = |A| + 1  (facilita o cálculo do intervalo).

    Entrada:
        digrafo (Digrafo): objeto Digrafo já lido/construído

    Saída:
        dict com as chaves:
            'APONTA'   (list): vetor de ponteiros, indexado de 1 a |V|+1
            'DEST'     (list): vetor de destinos, indexado de 1 a |A|
            'vertices' (list): vértices ordenados (posição i → APONTA[i])
            'arcos'    (list): arcos ordenados (posição k → DEST[k])
    """
    vertices = sorted(digrafo.obter_vertices(), key=str)
    n = len(vertices)

    # Ordena arcos por (origem, destino)
    arcos_ordenados = sorted(
        digrafo.obter_arcos(),
        key=lambda a: (str(a[0]), str(a[1]))
    )
    m = len(arcos_ordenados)

    # Mapeia vértice → posição (1-indexado) na lista de vértices
    pos_v = {v: i + 1 for i, v in enumerate(vertices)}

    # ── Constrói DEST (base 1) ──────────────────────────────────────────────
    # DEST[k] = destino do k-ésimo arco  (k de 1 a m)
    DEST = [None] + [v for (u, v) in arcos_ordenados]   # índice 0 não usado

    # ── Constrói APONTA (base 1) ────────────────────────────────────────────
    # APONTA[i] = posição em DEST do primeiro arco que sai do vértice i
    # APONTA[n+1] = m + 1  (sentinela)

    # Conta quantos arcos saem de cada vértice
    grau_saida = {v: 0 for v in vertices}
    for (u, _) in arcos_ordenados:
        grau_saida[u] += 1

    # Preenche APONTA acumulando posições
    APONTA = [None] * (n + 2)   # índices 0..n+1  (0 não usado)
    APONTA[1] = 1               # primeiro arco começa na posição 1
    for i, v in enumerate(vertices, start=1):
        APONTA[i + 1] = APONTA[i] + grau_saida[v]
    # APONTA[n+1] == m+1  (sentinela automática pela acumulação)

    return {
        'APONTA':   APONTA,
        'DEST':     DEST,
        'vertices': vertices,
        'arcos':    arcos_ordenados
    }


# ══════════════════════════════════════════════════════════════════
# (C) MATRIZ DE INCIDÊNCIA → ESTRELA DIRETA
# ══════════════════════════════════════════════════════════════════

def matriz_para_estrela_direta(mat_inc):
    """
    Converte uma Matriz de Incidência para a representação em Estrela Direta.

    Percorre cada coluna da matriz (cada arco):
      - A linha com valor +1 indica a ORIGEM do arco.
      - A linha com valor -1 indica o DESTINO do arco.
    Em seguida, aplica a mesma lógica de construção da Estrela Direta.

    Entrada:
        mat_inc (dict): dicionário retornado por construir_matriz_incidencia()

    Saída:
        dict: mesmo formato de construir_estrela_direta()
              (com chaves APONTA, DEST, vertices, arcos)
    """
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arcos_mi = mat_inc['arcos']

    n = len(vertices)
    m = len(arcos_mi)

    # ── Passo 1: extrai arcos da matriz (coluna por coluna) ─────────────────
    arcos_extraidos = []
    for j in range(m):
        origem  = None
        destino = None
        for i in range(n):
            if matriz[i][j] == +1:
                origem  = vertices[i]
            elif matriz[i][j] == -1:
                destino = vertices[i]
        if origem is not None and destino is not None:
            arcos_extraidos.append((origem, destino))

    # ── Passo 2: ordena arcos por (origem, destino) ─────────────────────────
    arcos_ordenados = sorted(arcos_extraidos,
                             key=lambda a: (str(a[0]), str(a[1])))

    # ── Passo 3: constrói DEST e APONTA (idêntico à função (B)) ────────────
    DEST = [None] + [v for (u, v) in arcos_ordenados]

    grau_saida = {v: 0 for v in vertices}
    for (u, _) in arcos_ordenados:
        grau_saida[u] += 1

    APONTA = [None] * (n + 2)
    APONTA[1] = 1
    for i, v in enumerate(vertices, start=1):
        APONTA[i + 1] = APONTA[i] + grau_saida[v]

    return {
        'APONTA':   APONTA,
        'DEST':     DEST,
        'vertices': vertices,
        'arcos':    arcos_ordenados
    }


# ══════════════════════════════════════════════════════════════════
# (D) ESTRELA DIRETA → MATRIZ DE INCIDÊNCIA
# ══════════════════════════════════════════════════════════════════

def estrela_direta_para_matriz(estrela):
    """
    Converte uma Estrela Direta de volta para a Matriz de Incidência.

    Percorre o vetor APONTA para identificar, para cada vértice i,
    quais arcos partem dele (posições APONTA[i] até APONTA[i+1]-1 em DEST).
    Cada arco (origem, destino) gera +1 na linha da origem e -1 na do destino.

    Entrada:
        estrela (dict): dicionário retornado por construir_estrela_direta()
                        (chaves: APONTA, DEST, vertices, arcos)

    Saída:
        dict: mesmo formato de construir_matriz_incidencia()
              (com chaves matriz, vertices, arcos, idx_v, idx_a)
    """
    APONTA   = estrela['APONTA']
    DEST     = estrela['DEST']
    vertices = estrela['vertices']
    arcos    = estrela['arcos']      # arcos já na ordem da estrela

    n = len(vertices)
    m = len(arcos)

    # Índices para acesso direto à matriz
    idx_v = {v: i for i, v in enumerate(vertices)}
    idx_a = {a: j for j, a in enumerate(arcos)}

    # ── Inicializa matriz zerada ─────────────────────────────────────────────
    matriz = [[0] * m for _ in range(n)]

    # ── Reconstrói arcos a partir de APONTA e DEST ──────────────────────────
    for i, u in enumerate(vertices, start=1):
        # Arcos que saem de u: posições APONTA[i] até APONTA[i+1]-1
        for k in range(APONTA[i], APONTA[i + 1]):
            v = DEST[k]             # destino do arco
            arco = (u, v)
            j = idx_a[arco]         # coluna correspondente ao arco

            matriz[idx_v[u]][j] = +1   # origem: +1
            matriz[idx_v[v]][j] = -1   # destino: -1

    return {
        'matriz':   matriz,
        'vertices': vertices,
        'arcos':    arcos,
        'idx_v':    idx_v,
        'idx_a':    idx_a
    }


# ══════════════════════════════════════════════════════════════════
# VERIFICAÇÃO DE EQUIVALÊNCIA
# ══════════════════════════════════════════════════════════════════

def matrizes_iguais(mat_a, mat_b):
    """
    Verifica se duas matrizes de incidência são idênticas (mesma estrutura
    e mesmos valores), comparando vértice a vértice e arco a arco.

    Entrada:
        mat_a, mat_b (dict): dicionários no formato de construir_matriz_incidencia()

    Saída:
        bool: True se as matrizes forem estruturalmente idênticas
    """
    if mat_a['vertices'] != mat_b['vertices']:
        return False
    if mat_a['arcos'] != mat_b['arcos']:
        return False
    for linha_a, linha_b in zip(mat_a['matriz'], mat_b['matriz']):
        if linha_a != linha_b:
            return False
    return True


# ══════════════════════════════════════════════════════════════════
# FUNÇÕES DE EXIBIÇÃO
# ══════════════════════════════════════════════════════════════════

def exibir_matriz_incidencia(mat_inc, titulo="Matriz de Incidência"):
    """
    Exibe a Matriz de Incidência formatada no console.

    Entrada:
        mat_inc (dict): dicionário retornado por construir_matriz_incidencia()
        titulo  (str):  título para a seção

    Saída:
        Impressão no console (nenhum retorno)
    """
    matriz   = mat_inc['matriz']
    vertices = mat_inc['vertices']
    arcos    = mat_inc['arcos']
    m        = len(arcos)

    print(f"\n  {titulo}")
    print(f"  Dimensão: {len(vertices)} vértices × {m} arcos")

    # Cabeçalho: rótulos dos arcos (a1, a2, ...)
    cab = "  " + " " * 6 + "".join(f"  a{j+1:02d}" for j in range(m))
    print(cab)

    # Sublinha do cabeçalho
    print("  " + " " * 6 + "─" * (m * 5))

    # Linhas: cada vértice com seus valores na matriz
    for i, v in enumerate(vertices):
        linha_vals = "".join(
            f"  {matriz[i][j]:+d} " if matriz[i][j] != 0 else "   0 "
            for j in range(m)
        )
        print(f"  v={str(v):>3} │{linha_vals}")

    # Rodapé: legenda dos arcos
    print(f"\n  Legenda dos arcos:")
    for j, (u, v) in enumerate(arcos):
        print(f"    a{j+1:02d} = ({u} → {v})")


def exibir_estrela_direta(estrela, titulo="Estrela Direta (Forward Star)"):
    """
    Exibe a representação em Estrela Direta no console.

    Entrada:
        estrela (dict): dicionário retornado por construir_estrela_direta()
        titulo  (str):  título para a seção

    Saída:
        Impressão no console (nenhum retorno)
    """
    APONTA   = estrela['APONTA']
    DEST     = estrela['DEST']
    vertices = estrela['vertices']
    n        = len(vertices)
    m        = len(estrela['arcos'])

    print(f"\n  {titulo}")

    # ── Vetor APONTA ──────────────────────────────────────────────────────────
    print(f"\n  Vetor APONTA  (índice 1 a {n+1}, sentinela em {n+1}):")
    cab_ap  = "  Índice  : " + "".join(f"  {i:3d}" for i in range(1, n + 2))
    val_ap  = "  APONTA  : " + "".join(f"  {APONTA[i]:3d}" for i in range(1, n + 2))
    vert_ap = "  Vértice : " + "".join(f"  {str(v):>3}" for v in vertices) + "   *"
    print(cab_ap)
    print(val_ap)
    print(vert_ap)

    # ── Vetor DEST ────────────────────────────────────────────────────────────
    print(f"\n  Vetor DEST  (índice 1 a {m}):")
    cab_d  = "  Índice  : " + "".join(f"  {k:3d}" for k in range(1, m + 1))
    val_d  = "  DEST    : " + "".join(f"  {str(DEST[k]):>3}" for k in range(1, m + 1))
    print(cab_d)
    print(val_d)

    # ── Interpretação: sucessores de cada vértice ─────────────────────────────
    print(f"\n  Interpretação — sucessores de cada vértice:")
    print(f"  {'Vértice':>8} | APONTA[i] | APONTA[i+1]-1 | Sucessores (DEST)")
    print(f"  {'-'*8}-+{'-'*10}+{'-'*14}+-{'-'*25}")
    for i, v in enumerate(vertices, start=1):
        ini  = APONTA[i]
        fim  = APONTA[i + 1] - 1
        sucs = [str(DEST[k]) for k in range(ini, fim + 1)] if ini <= fim else []
        print(f"  {str(v):>8} | {ini:^9} | {fim:^13} | {sucs}")


# ══════════════════════════════════════════════════════════════════
# EXECUÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    base = os.path.join(os.path.dirname(__file__), '..', 'dados-trabalho_1')

    # Lê o dígrafo do arquivo
    digrafo = ler_digrafo(os.path.join(base, 'DIGRAFO1.txt'))

    print("\n" + "═" * 70)
    print("  IMPLEMENTAÇÃO 06 — Matriz de Incidência ↔ Estrela Direta")
    print("  Dígrafo: DIGRAFO1  │  Vértices: 13  │  Arcos: 16")
    print("═" * 70)

    # ──────────────────────────────────────────────────────────────────────────
    # (A) Dígrafo → Matriz de Incidência (fonte original)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n\n" + "─" * 70)
    print("  (A)  DÍGRAFO  →  MATRIZ DE INCIDÊNCIA")
    print("─" * 70)
    mat_original = construir_matriz_incidencia(digrafo)
    exibir_matriz_incidencia(mat_original, "Matriz de Incidência (construída diretamente do dígrafo)")

    # ──────────────────────────────────────────────────────────────────────────
    # (B) Dígrafo → Estrela Direta (fonte original)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n\n" + "─" * 70)
    print("  (B)  DÍGRAFO  →  ESTRELA DIRETA")
    print("─" * 70)
    estrela_original = construir_estrela_direta(digrafo)
    exibir_estrela_direta(estrela_original, "Estrela Direta (construída diretamente do dígrafo)")

    # ──────────────────────────────────────────────────────────────────────────
    # (C) Matriz de Incidência → Estrela Direta
    # ──────────────────────────────────────────────────────────────────────────
    print("\n\n" + "─" * 70)
    print("  (C)  MATRIZ DE INCIDÊNCIA  →  ESTRELA DIRETA")
    print("─" * 70)
    estrela_de_matriz = matriz_para_estrela_direta(mat_original)
    exibir_estrela_direta(estrela_de_matriz, "Estrela Direta (convertida a partir da Matriz de Incidência)")

    # Verifica se o resultado de (C) é igual ao de (B)
    ok_c = (estrela_de_matriz['APONTA'] == estrela_original['APONTA'] and
            estrela_de_matriz['DEST']   == estrela_original['DEST'])
    print(f"\n  Validação (C) ≡ (B): {'✔ IDÊNTICAS' if ok_c else '✘ DIVERGENTES'}")

    # ──────────────────────────────────────────────────────────────────────────
    # (D) Estrela Direta → Matriz de Incidência
    # ──────────────────────────────────────────────────────────────────────────
    print("\n\n" + "─" * 70)
    print("  (D)  ESTRELA DIRETA  →  MATRIZ DE INCIDÊNCIA")
    print("─" * 70)
    mat_de_estrela = estrela_direta_para_matriz(estrela_original)
    exibir_matriz_incidencia(mat_de_estrela, "Matriz de Incidência (reconstruída a partir da Estrela Direta)")

    # Verifica se o resultado de (D) é igual ao de (A)
    ok_d = matrizes_iguais(mat_de_estrela, mat_original)
    print(f"\n  Validação (D) ≡ (A): {'✔ IDÊNTICAS' if ok_d else '✘ DIVERGENTES'}")

    print("\n\n" + "═" * 70 + "\n")