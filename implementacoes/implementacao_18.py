"""
implementacao_18.py
Módulo para conversão de Dígrafos em Grafos Subjacentes e análise de conectividade fraca.
"""

from grafo import Grafo

def obter_grafo_subjacente(digrafo):
    """
    Transforma um Dígrafo em um Grafo não-dirigido.
    Ignora a direção dos arcos e funde arcos opostos em uma única aresta.
    """
    subjacente = Grafo()

    # Preserva todos os vértices
    for v in digrafo.adjacencia:
        subjacente.adicionar_vertice(v)

    # Transforma arcos em arestas (o método adicionar_aresta já lida com duplicatas)
    for u in digrafo.adjacencia:
        for v in digrafo.adjacencia[u]:
            subjacente.adicionar_aresta(u, v)

    subjacente.num_vertices_declarado = digrafo.num_vertices_declarado
    return subjacente

def analisar_diferenca(digrafo, subjacente):
    """Analisa a relação entre arcos originais e arestas resultantes."""
    arcos = digrafo.obter_arcos()
    arestas = subjacente.obter_arestas()
    arcos_set = set(arcos)
    arcos_fundidos = []
    visitados = set()

    for (u, v) in arcos:
        par = frozenset([u, v])
        if (v, u) in arcos_set and par not in visitados:
            arcos_fundidos.append((u, v, v, u))
            visitados.add(par)

    return {
        'arcos_originais': arcos,
        'arestas_subj': arestas,
        'arcos_fundidos': arcos_fundidos,
        'total_arcos': len(arcos),
        'total_arestas': len(arestas)
    }

def verificar_conectividade_fraca(subjacente):
    """Verifica se o subjacente é conexo via busca em largura simplificada."""
    visitados = set()
    componentes = []

    for inicio in subjacente.adjacencia:
        if inicio not in visitados:
            fila = [inicio]
            comp = []
            visitados.add(inicio)
            while fila:
                u = fila.pop(0)
                comp.append(u)
                for v in subjacente.adjacencia[u]:
                    if v not in visitados:
                        visitados.add(v)
                        fila.append(v)
            componentes.append(sorted(comp, key=str))

    return {
        'fracamente_conexo': len(componentes) == 1,
        'componentes': componentes
    }

def exibir_resultado_subjacente(nome, digrafo, subjacente, analise, conect):
    """Exibe o relatório formatado comparando as duas estruturas."""
    print(f"\n{'=' * 62}\n  {nome}  →  Grafo Subjacente\n{'=' * 62}")

    print(f"\n  [ DÍGRAFO ORIGINAL ]")
    print(f"  Arcos ({analise['total_arcos']}): {analise['arcos_originais']}")

    if analise['arcos_fundidos']:
        print(f"\n  Fusões (Arcos Opostos → Aresta Única):")
        for (u, v, vu, vv) in analise['arcos_fundidos']:
            print(f"    ({u}↔{v})")

    print(f"\n  [ GRAFO SUBJACENTE ]")
    print(f"  Arestas ({analise['total_arestas']}): {analise['arestas_subj']}")

    print(f"\n  Conectividade Fraca:")
    if conect['fracamente_conexo']:
        print(f"  ✔  O dígrafo É FRACAMENTE CONEXO.")
    else:
        print(f"  ✘  O dígrafo NÃO É FRACAMENTE CONEXO ({len(conect['componentes'])} componentes).")