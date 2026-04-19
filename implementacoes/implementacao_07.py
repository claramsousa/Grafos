"""
implementacao_07.py
Módulo para determinar e validar o número total de vértices de um grafo.
"""

def contar_vertices(grafo):
    """
    Determina o número total de vértices.
    Retorna o valor declarado no arquivo e a contagem real na estrutura de dados.
    """
    vertices_reais = grafo.obter_vertices()
    
    return {
        'declarado': grafo.num_vertices_declarado,
        'real':      len(vertices_reais),
        'vertices':  sorted(vertices_reais, key=str)
    }

def exibir_contagem_vertices(nome_grafo, resultado):
    """
    Exibe formatado o resultado da contagem e alerta sobre divergências.
    """
    print(f"\n{'=' * 50}")
    print(f"  {nome_grafo}")
    print(f"{'=' * 50}")
    print(f"  Vértices declarados (1ª linha do arquivo): {resultado['declarado']}")
    print(f"  Vértices encontrados nas arestas:          {resultado['real']}")
    print(f"  Lista de vértices: {resultado['vertices']}")

    # Lógica de validação de integridade
    if resultado['declarado'] != resultado['real']:
        diff = resultado['declarado'] - resultado['real']
        if diff > 0:
            print(f"  ⚠ ATENÇÃO: {diff} vértice(s) declarado(s) sem arestas (isolado(s)).")
        else:
            print(f"  ⚠ ATENÇÃO: {abs(diff)} vértice(s) extra(s) nas arestas além do declarado.")
    else:
        print(f"  ✔ Declarado e contagem real coincidem.")