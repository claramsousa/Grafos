"""
grafo.py
--------
Módulo base para representação e leitura de Grafos e Dígrafos.

Estrutura de dados utilizada: Lista de Adjacência implementada manualmente

Formato do arquivo de entrada:
    - Linha 1: número de vértices (inteiro)
    - Demais linhas: pares "origem,destino" representando arestas

Para GRAFOS: a conexão é bidirecional (a-b implica b-a)
Para DÍGRAFOS: a conexão é direcional (DE -> PARA)
"""


class Grafo:
    """
    Representa um GRAFO NÃO-DIRIGIDO usando lista de adjacência.

    Atributos:
        num_vertices_declarado (int): Número de vértices informado no arquivo.
        adjacencia (dict): Dicionário onde cada chave é um vértice e o valor é uma lista de vizinhos (vértices adjacentes).
    """

    def __init__(self):
        """Inicializa um grafo vazio."""
        self.num_vertices_declarado = 0  # número declarado na linha do arquivo
        self.adjacencia = {}             # lista de adjacência: {vértice: [vizinhos]}

    def adicionar_vertice(self, v):
        """
        Garante que o vértice v existe na lista de adjacência.

        Entrada:
            v: identificador do vértice (str ou int)
        Saída:
            Nenhuma (modifica self.adjacencia no lugar)
        """
        if v not in self.adjacencia:
            self.adjacencia[v] = []

    def adicionar_aresta(self, u, v):
        """
        Adiciona uma aresta bidirecional entre u e v (grafo não-dirigido).

        Entrada:
            u: vértice de origem (str ou int)
            v: vértice de destino (str ou int)
        Saída:
            Nenhuma (modifica self.adjacencia no lugar)
        """
        self.adicionar_vertice(u)
        self.adicionar_vertice(v)

        # Aresta bidirecional: u aparece na lista de v e v na lista de u
        if v not in self.adjacencia[u]:
            self.adjacencia[u].append(v)
        if u not in self.adjacencia[v]:
            self.adjacencia[v].append(u)

    def obter_vertices(self):
        """
        Retorna a lista de todos os vértices do grafo.

        Saída:
            list: lista com todos os vértices presentes na lista de adjacência
        """
        return list(self.adjacencia.keys())

    def obter_arestas(self):
        """
        Retorna a lista de todas as arestas do grafo (sem duplicatas).

        Saída:
            list: lista de tuplas (u, v) representando cada aresta,
                  onde cada par aparece apenas uma vez.
        """
        arestas = []
        visitados = set()

        for u in self.adjacencia:
            for v in self.adjacencia[u]:
                # Usa frozenset para evitar duplicar (u,v) e (v,u)
                par = frozenset([u, v])
                if par not in visitados:
                    visitados.add(par)
                    arestas.append((u, v))

        return arestas

    def __repr__(self):
        """Representação textual do grafo para depuração."""
        return f"Grafo(vértices={self.obter_vertices()}, arestas={self.obter_arestas()})"


class Digrafo:
    """
    Representa um DÍGRAFO (grafo dirigido) usando lista de adjacência.

    Atributos:
        num_vertices_declarado (int): Número de vértices informado no arquivo.
        adjacencia (dict): Dicionário onde cada chave é um vértice e o valor
                           é a lista de vértices para os quais ele aponta (sucessores).
    """

    def __init__(self):
        """Inicializa um dígrafo vazio."""
        self.num_vertices_declarado = 0  # número declarado na 1ª linha do arquivo
        self.adjacencia = {}             # lista de adjacência direcionada

    def adicionar_vertice(self, v):
        """
        Garante que o vértice v existe na lista de adjacência.

        Entrada:
            v: identificador do vértice (str ou int)
        Saída:
            Nenhuma (modifica self.adjacencia no lugar)
        """
        if v not in self.adjacencia:
            self.adjacencia[v] = []

    def adicionar_arco(self, origem, destino):
        """
        Adiciona um arco dirigido de 'origem' para 'destino'.

        Entrada:
            origem:  vértice de partida do arco (str ou int)
            destino: vértice de chegada do arco (str ou int)
        Saída:
            Nenhuma (modifica self.adjacencia no lugar)
        """
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)

        # Arco unidirecional: apenas origem aponta para destino
        if destino not in self.adjacencia[origem]:
            self.adjacencia[origem].append(destino)

    def obter_vertices(self):
        """
        Retorna a lista de todos os vértices do dígrafo.

        Saída:
            list: lista com todos os vértices presentes na lista de adjacência
        """
        return list(self.adjacencia.keys())

    def obter_arcos(self):
        """
        Retorna a lista de todos os arcos do dígrafo.

        Saída:
            list: lista de tuplas (origem, destino) representando cada arco
        """
        arcos = []
        for origem in self.adjacencia:
            for destino in self.adjacencia[origem]:
                arcos.append((origem, destino))
        return arcos

    def __repr__(self):
        """Representação textual do dígrafo para depuração."""
        return f"Digrafo(vértices={self.obter_vertices()}, arcos={self.obter_arcos()})"


# ==============================================================================
# FUNÇÕES DE LEITURA DE ARQUIVOS
# ==============================================================================

def ler_grafo(caminho_arquivo):
    """
    Lê um arquivo de texto e constrói um objeto Grafo.

    Formato esperado do arquivo:
        - Linha 1: número de vértices (inteiro)
        - Demais linhas: "u,v" representando arestas (não-dirigidas)

    Entrada:
        caminho_arquivo (str): caminho para o arquivo .txt do grafo

    Saída:
        Grafo: objeto Grafo preenchido com os dados do arquivo

    Exemplo de arquivo:
        3
        a,b
        b,c
    """
    grafo = Grafo()

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.read().splitlines()  # lê todas as linhas sem '\n'

    # Primeira linha: número de vértices declarado
    grafo.num_vertices_declarado = int(linhas[0].strip())

    # Demais linhas: pares de vértices (arestas)
    for linha in linhas[1:]:
        linha = linha.strip()
        if linha:  # ignora linhas em branco
            partes = linha.split(',')
            u = partes[0].strip()
            v = partes[1].strip()
            grafo.adicionar_aresta(u, v)

    return grafo


def ler_digrafo(caminho_arquivo):
    """
    Lê um arquivo de texto e constrói um objeto Digrafo.

    Formato esperado do arquivo:
        - Linha 1: número de vértices (inteiro)
        - Demais linhas: "origem,destino" representando arcos (dirigidos)

    Entrada:
        caminho_arquivo (str): caminho para o arquivo .txt do dígrafo

    Saída:
        Digrafo: objeto Digrafo preenchido com os dados do arquivo

    Exemplo de arquivo:
        3
        a,b
        b,c
    """
    digrafo = Digrafo()

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.read().splitlines()

    # Primeira linha: número de vértices declarado
    digrafo.num_vertices_declarado = int(linhas[0].strip())

    # Demais linhas: pares origem,destino (arcos dirigidos)
    for linha in linhas[1:]:
        linha = linha.strip()
        if linha:
            partes = linha.split(',')
            origem  = partes[0].strip()
            destino = partes[1].strip()
            digrafo.adicionar_arco(origem, destino)

    return digrafo