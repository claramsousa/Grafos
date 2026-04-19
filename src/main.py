import os
import sys

# CONFIGURAÇÃO DE CAMINHOS
# Como a main2.py está na pasta 'src', o dirname(__file__) já é a pasta 'src'
pasta_src = os.path.dirname(__file__)
pasta_raiz = os.path.abspath(os.path.join(pasta_src, '..'))

# Adiciona a raiz e a src ao sys.path para garantir que tudo seja encontrado
if pasta_raiz not in sys.path:
    sys.path.insert(0, pasta_raiz)
if pasta_src not in sys.path:
    sys.path.insert(0, pasta_src)

# Define o caminho da pasta de dados
base = os.path.join(pasta_raiz, 'dados-trabalho_1')

# IMPORTAÇÕES
from grafo import ler_grafo, ler_digrafo

from implementacoes.lista_adjacencia_grafos import construir_lista_adjacencia, exibir_lista_adjacencia
from implementacoes.implementacao_02 import exibir_matriz_adjacencia, construir_matriz_adjacencia
from implementacoes.matriz_incidencia_grafos_03 import (
    construir_matriz_incidencia as construir_mi_grafo,
    exibir_resultado as exibir_mi_grafo
)
from implementacoes.conversao_matriz_lista import matriz_para_lista, lista_para_matriz
from implementacoes.implementacao_06 import sao_adjacentes, testar_e_exibir
from implementacoes.implementacao_07 import contar_vertices, exibir_contagem_vertices
from implementacoes.implementacao_08 import contar_arestas, exibir_contagem_arestas
from implementacoes.implementacao_09 import exibir_resultado_detalhado
from implementacoes.implementacao_10 import exibir_resultado_detalhado
from implementacoes.conexo_11 import eh_conexo
from implementacoes.busca_largura import mapear_busca_largura, exibir_resultado_bfs
from implementacoes.implementacao_12 import verificar_bipartido, exibir_resultado_bipartido
from implementacoes.busca_profundidade_grafos_14 import busca_profundidade, exibir_resultado_dfs
from implementacoes.implementacao_15 import biconectividade, exibir_resultado_biconectividade
from implementacoes.implementacao_16 import exibir_matriz_digrafo
from implementacoes.matriz_incidencia_digrafos_17 import (
    construir_matriz_incidencia as construir_mi_digrafo,
    exibir_incidencia_digrafo as exibir_mi_digrafo
)
from implementacoes.implementacao_18 import obter_grafo_subjacente, analisar_diferenca, verificar_conectividade_fraca, exibir_resultado_subjacente
from implementacoes.implementacao_19 import (
    construir_matriz_incidencia_fs, 
    construir_estrela_direta,
    matriz_para_estrela_direta,
    estrela_direta_para_matriz,
    exibir_fs_mi_conversao
)
from implementacoes.busca_profundidade_digrafos_20 import busca_profundidade_digrafo, exibir_dfs_digrafo
from implementacoes.grau_vertice import calcular_grau_vertices, exibir_grau_vertices

# INTERFACE DO MENU
def menu_principal():
    print("\n|-----------------------------------------|")
    print("|--------Projeto de grafos unidade 1 -----|")
    print("|-----------------------------------------|\n")
    while True:
        print("Digite um numero dos itens obrigatórios solicitados ou 0 para encerrar:")
        opcao = input("Opção: ")

        if opcao == '0':
            break

        elif opcao == '1':
            print("\n --- #1: Representação do Grafo a partir da Lista de Adjacências (GRAFO1, GRAFO2) ---")
            arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

            for arquivo in arquivos_teste:
                path = os.path.join(base, arquivo)
                
                if os.path.exists(path):
                    # Carrega o grafo do arquivo
                    g = ler_grafo(path)
                    
                    # Constrói a estrutura de dados usando o módulo importado
                    dados_lista = construir_lista_adjacencia(g)
                    
                    # Exibe o resultado formatado
                    exibir_lista_adjacencia(arquivo.replace('.txt', ''), dados_lista)
                else:
                    print(f"\nArquivo não encontrado: {path}")

            print(f"\n{'=' * 70}\n")

        elif opcao == '2':
            print("\n--- #02: Representação do Grafo a partir da Matriz de Adjacências(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
                caminho = os.path.join(base, g_nome)
                
                if os.path.exists(caminho):
                    # Carrega o grafo usando a função central de leitura
                    g = ler_grafo(caminho)
                    # Chama a função de exibição do módulo importado
                    exibir_matriz_adjacencia(g_nome, g)
                else:
                    print(f"Arquivo não encontrado: {caminho}")

            print(f"\n{'=' * 65}\n")
    
        elif opcao == '3':
            print("\n--- #3: Representação do Grafo a partir da Matriz de Incidência(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1', 'GRAFO_2']:
                path = os.path.join(base, f'{g_nome}.txt')
                if os.path.exists(path):
                    g = ler_grafo(path)
                    # CORREÇÃO AQUI: Use os nomes com "mi_grafo"
                    dados_mi = construir_mi_grafo(g)
                    exibir_mi_grafo(g_nome, dados_mi)
                else:
                    print(f"\nArquivo não encontrado: {path}")

        elif opcao == '4':
            print("\n--- #4: Conversão de matriz de adjacência para lista de Adjacências e vice-versa.(GRAFO1, GRAFO2) ---")
            arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

            for arquivo in arquivos_teste:
                path = os.path.join(base, arquivo)
        
                if os.path.exists(path):
                    g = ler_grafo(path)
                    lista_estruturada = construir_lista_adjacencia(g)
                    matriz_estruturada = construir_matriz_adjacencia(g)

                    print(f"\n>>> Processando {arquivo}:")
                    print("\n[Conversão: Lista para Matriz]")
                    # Esta função já chama internamente a exibição da matriz
                    matriz_convertida = lista_para_matriz(arquivo, lista_estruturada)

                    print("\n[Conversão: Matriz para Lista]")
                    lista_convertida = matriz_para_lista(matriz_estruturada)
                    # Exibe a lista resultante usando a função do módulo de lista
                    exibir_lista_adjacencia(arquivo, lista_convertida)
                else:
                    print(f"\nArquivo não encontrado: {path}")

            print(f"\n{'=' * 70}\n")

        elif opcao == '5':
            print("\n--- #5: Função que calcula o grau de cada vértice.(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
                path = os.path.join(base, g_nome)
                
                if os.path.exists(path):
                    g = ler_grafo(path)
                    
                    dados_estruturados = construir_lista_adjacencia(g)
                    
                    dados_graus = calcular_grau_vertices(dados_estruturados)
                    exibir_grau_vertices(g_nome.replace('.txt', ''), dados_graus)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 70}\n")

        elif opcao == '6':
            print("\n--- #6: Função que determina se dois vértices são adjacentes.(GRAFO1, GRAFO2 ---")
            path_g1 = os.path.join(base, 'GRAFO_1.txt')
            if os.path.exists(path_g1):
                g1 = ler_grafo(path_g1)
                testes_g1 = [('a', 'b'), ('a', 'c'), ('b', 'e'), ('b', 'd'), ('b', 'f'), ('c', 'e'), ('c', 'f'), ('e', 'h'), ('h', 'd')]
                testar_e_exibir('GRAFO_1.txt', g1, testes_g1)

            path_g2 = os.path.join(base, 'GRAFO_2.txt')
            if os.path.exists(path_g2):
                g2 = ler_grafo(path_g2)
                testes_g2 = [(1, 2), (1, 10), (10, 11), (8, 9)]
                testar_e_exibir('GRAFO_2.txt', g2, testes_g2)

            print(f"\n{'=' * 60}\n")

        elif opcao == '7':
            print("\n--- #7: Função que determina o número total de vértices(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
                path = os.path.join(base, g_nome)
                
                if os.path.exists(path):
                    # Carrega o grafo do arquivo
                    g = ler_grafo(path)
                    # Realiza a contagem e exibe o relatório
                    resultado = contar_vertices(g)
                    exibir_contagem_vertices(g_nome.replace('.txt', ''), resultado)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 50}\n")

        elif opcao == '8':
            print("\n--- #8: Função que determina o número total de arestas(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
                path = os.path.join(base, g_nome)
                
                if os.path.exists(path):
                    # Carrega o grafo do arquivo
                    g = ler_grafo(path)
                    # Realiza a contagem e exibe o resultado
                    resultado = contar_arestas(g)
                    exibir_contagem_arestas(g_nome.replace('.txt', ''), resultado)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 50}\n")

        elif opcao == '9':
            print("\n--- #9: Inclusão de um novo vértice(GRAFO1) ---")
            path = os.path.join(base, 'GRAFO_1.txt')
            
            if os.path.exists(path):
                # 1. Carrega o grafo original
                g = ler_grafo(path)
                exibir_resultado_detalhado('GRAFO_1', g, "ESTADO ORIGINAL")

                # 2. Executa a inclusão
                novo_v = "Z"
                print(f"\n[Tarefa 9] Incluindo o vértice '{novo_v}'...")
                g.adicionar_vertice(novo_v)
                
                # 3. Exibe o resultado final
                exibir_resultado_detalhado('GRAFO_1', g, "APÓS INCLUSÃO")
            else:
                print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 50}\n")

        elif opcao == '10':
            print("\n--- #10: Exclusão de um vértice existente(GRAFO1) ---")
            path = os.path.join(base, 'GRAFO_1.txt')
            
            if os.path.exists(path):
                # 1. Carrega o grafo original (sem as alterações da opção 9)
                g = ler_grafo(path)
                exibir_resultado_detalhado('GRAFO_1', g, "ESTADO ORIGINAL")

                # 2. Executa a exclusão
                v_alvo = "a"
                print(f"\n[Tarefa 10] Removendo o vértice '{v_alvo}'...")
                
                # O método remover_vertice já deve estar na sua classe Grafo em src/grafo.py
                if g.remover_vertice(v_alvo):
                    # 3. Exibe o resultado final
                    exibir_resultado_detalhado('GRAFO_1', g, "APÓS EXCLUSÃO")
                else:
                    print(f"Erro: Vértice '{v_alvo}' não encontrado no grafo.")
            else:
                print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 50}\n")

        elif opcao == '11':
            print("\n--- #11: Função que determina se um grafo é conexo ou não(GRAFO1, GRAFO2) ---")
            arquivos_teste = ['GRAFO_1.txt', 'GRAFO_2.txt']

            for arquivo in arquivos_teste:
                path = os.path.join(base, arquivo)
                if os.path.exists(path):
                    # 1. Carrega o grafo do arquivo
                    g = ler_grafo(path)
                    
                    # 2. Gera a lista estruturada (necessária para a lógica da tarefa 11)
                    dados_lista = construir_lista_adjacencia(g)
                    
                    # 3. Executa a verificação de conectividade
                    conexo, isolados = eh_conexo(dados_lista)
                    
                    print(f"\n{'-'*40}")
                    print(f" Análise de Conectividade: {arquivo}")
                    print(f"{'-'*40}")
                    
                    if conexo:
                        print(" RESULTADO: O grafo é CONEXO.")
                    else:
                        print(" RESULTADO: O grafo é DESCONEXO.")
                        print(f" Vértices não alcançados: {isolados}")
                else:
                    print(f"\nArquivo não encontrado: {path}")

            print(f"\n{'=' * 70}\n")

        elif opcao == '12':
            print("\n--- #12: Determinar se um grafo é bipartido (OPC = 1,0 ponto)(GRAFO1, GRAFO2) ---")
            for g_nome in ['GRAFO_1.txt', 'GRAFO_2.txt']:
                path = os.path.join(base, g_nome)
                
                if os.path.exists(path):
                    # 1. Carrega o grafo do arquivo
                    g = ler_grafo(path)
                    
                    # 2. Executa a lógica de verificação
                    resultado = verificar_bipartido(g)
                    
                    # 3. Exibe o relatório detalhado
                    exibir_resultado_bipartido(g_nome.replace('.txt', ''), resultado, g.adjacencia)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 60}\n")

        elif opcao == '13':
            print("\n--- #13: Busca em Largura, a partir de um vértice específico(GRAFO1, GRAFO3, Vértice inicial) ---")
            arquivos_teste = ['GRAFO_1.txt', 'GRAFO_3.txt']
            
            for arquivo in arquivos_teste:
                path = os.path.join(base, arquivo)
                if os.path.exists(path):
                    g = ler_grafo(path)
                    dados_estruturados = construir_lista_adjacencia(g)
                    
                    vertice_start = dados_estruturados['vertices'][0]
                    
                    ordem, pais = mapear_busca_largura(dados_estruturados, vertice_start)
                    exibir_resultado_bfs(arquivo, vertice_start, ordem, pais)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 70}\n")

        elif opcao == '14':
            print("\n--- #14: Busca em Profundidade, a partir de um vértice em específico(GRAFO1, GRAFO3, Vértice inicial). ---")
            path_g1 = os.path.join(base, 'GRAFO_1.txt')
            if os.path.exists(path_g1):
                g1 = ler_grafo(path_g1)
                res_g1 = busca_profundidade(g1, v_inicial='d')
                exibir_resultado_dfs("GRAFO_1", 'd', res_g1)

            path_g3 = os.path.join(base, 'GRAFO_3.txt')
            if os.path.exists(path_g3):
                g3 = ler_grafo(path_g3)
                res_g3 = busca_profundidade(g3, v_inicial='g')
                exibir_resultado_dfs("GRAFO_3", 'g', res_g3)
            else:
                print(f"Arquivo GRAFO_3.txt não encontrado para teste.")

            print(f"\n{'=' * 60}\n")

        elif opcao == '15':
            print("\n--- #15: Conversão de matriz de adjacência para lista de Adjacências e vice-versa.(GRAFO1, GRAFO2) ---")
            path = os.path.join(base, 'GRAFO_3.txt')
            
            if os.path.exists(path):
                # 1. Carrega o grafo do arquivo
                g = ler_grafo(path)
                
                # 2. Executa o algoritmo de Tarjan para biconectividade
                resultado = biconectividade(g)
                
                # 3. Exibe o relatório detalhado de articulações e blocos
                exibir_resultado_biconectividade('GRAFO_3', resultado)
            else:
                print(f"Arquivo GRAFO_3.txt não encontrado na pasta de dados.")

            print(f"\n{'=' * 60}\n")

        elif opcao == '16':
            print("\n--- #16: Representação do Digrafo a partir da Matriz de Adjacências(DIGRAFO1, DIGRAFO2) ---")
            for d_nome in ['DIGRAFO1.txt', 'DIGRAFO2.txt']:
                path = os.path.join(base, d_nome)
                
                if os.path.exists(path):
                    # Importante: Usa ler_digrafo para manter a direcionalidade
                    d = ler_digrafo(path)
                    exibir_matriz_digrafo(d_nome, d)
                else:
                    print(f"Arquivo não encontrado: {path}")

            print(f"\n{'=' * 65}\n")

        elif opcao == '17':
            print("\n--- #17: Representação do Digrafo a partir da Matriz de Incidência(DIGRAFO1, DIGRAFO2) ---")
            for d_nome in ['DIGRAFO1.txt', 'DIGRAFO2.txt']:
                path = os.path.join(base, d_nome)
                if os.path.exists(path):
                    d = ler_digrafo(path)
                    # CORREÇÃO AQUI: Use os nomes com "mi_digrafo"
                    matriz_estruturada = construir_mi_digrafo(d)
                    exibir_mi_digrafo(d_nome, matriz_estruturada)
                else:
                    print(f"Arquivo não encontrado: {path}")

        elif opcao == '18':
            print("\n--- #18: Determinação do Grafo subjacente (OPC= 0,5 ponto)(DIGRAFO1) ---")
            path = os.path.join(base, 'DIGRAFO1.txt')
            
            if os.path.exists(path):
                d = ler_digrafo(path)

                g_sub = obter_grafo_subjacente(d)

                analise = analisar_diferenca(d, g_sub)
                conect = verificar_conectividade_fraca(g_sub)

                exibir_resultado_subjacente('DIGRAFO1', d, g_sub, analise, conect)
            else:
                print(f"Arquivo DIGRAFO1.txt não encontrado.")

            print(f"\n{'=' * 62}\n")

        elif opcao == '19':
            print("\n--- #19: Conversão de matriz de adjacência para lista de Adjacências e vice-versa.(GRAFO1, GRAFO2) ---")
            path = os.path.join(base, 'DIGRAFO1.txt')
            
            if os.path.exists(path):
                d = ler_digrafo(path)

                mi_original = construir_matriz_incidencia_fs(d)
                fs_original = construir_estrela_direta(d)

                fs_convertida = matriz_para_estrela_direta(mi_original)
                mi_reconstituida = estrela_direta_para_matriz(fs_original)

                exibir_fs_mi_conversao(d, mi_original, fs_original, fs_convertida, mi_reconstituida)
            else:
                print(f"Arquivo DIGRAFO1.txt não encontrado.")

            print(f"\n{'=' * 70}\n")

        elif opcao == '20':
            print("\n--- #20: Busca em profundidade, com determinação de profundidade de entrada e de saída de cada vértice e definição de arestas de árvore, retorno, avanço ou cruzamento.(DIGRAFO2, DIGRAFO3) ---")
            path_d2 = os.path.join(base, 'DIGRAFO2.txt')
            if os.path.exists(path_d2):
                d2 = ler_digrafo(path_d2)
                v_ini_2 = sorted(d2.obter_vertices(), key=lambda x: (str(x).isnumeric(), str(x)))[0]
                res_d2 = busca_profundidade_digrafo(d2, v_inicial=v_ini_2)
                exibir_dfs_digrafo("DIGRAFO2.txt", v_ini_2, res_d2)

            path_d3 = os.path.join(base, 'DIGRAFO3.txt')
            if os.path.exists(path_d3):
                d3 = ler_digrafo(path_d3)
                res_d3 = busca_profundidade_digrafo(d3, v_inicial='g')
                exibir_dfs_digrafo("DIGRAFO3.txt", 'g', res_d3)
            
            print(f"\n{'=' * 75}\n")

        elif opcao == '21':
            print("\n--- #21: Pesquisar e implementar uma aplicação, usando busca em profundidade (OPC= 1,0 ponto). (em exemplo definido pelo grupo, com pelo menos 10 vértices) ---")
            print("O item opcional 21. não  foi implementado")

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()