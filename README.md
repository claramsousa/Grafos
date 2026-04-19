# Trabalho Prático — Grafos

Implementações em Python da teoria de Grafos e Dígrafos.  
Todas as estruturas de dados e algoritmos são implementados **do zero**, sem uso de bibliotecas externas para as atividades-fim.

---

## 📁 Estrutura do Repositório

```
projeto-grafos/
│
├── dados-trabalho_1/          # Arquivos de entrada (.txt) dos grafos e dígrafos
│   ├── GRAFO_0.txt
│   ├── GRAFO_1.txt
│   ├── GRAFO_2.txt
│   ├── GRAFO_3.txt
│   ├── DIGRAFO_0.txt
│   ├── DIGRAFO1.txt
│   ├── DIGRAFO2.txt
│   └── DIGRAFO3.txt
│
├── src/                       # Módulos base reutilizáveis
│   └── grafo.py               # Classes Grafo e Digrafo + funções de leitura
│   └── main.py 
│
├── implementacoes/            # Uma implementação por arquivo
│   └── lista_adjacencia_grafos.py               # Implementação 1
│   └── implementacao_02.p                       # Implementação 2
│   └── matriz_incidencia_grafos_03.py           # Implementação 3
│   └── conversao_matriz_lista.py                # Implementação 4
│   └── grau_vertice.py                          # Implementação 5
│   └── implementacao_06.py                      # Implementação 6
│   └── implementacao_07.py                      # Implementação 7
│   └── implementacao_08.py                      # Implementação 8
│   └── implementacao_09.py                      # Implementação 9
│   └── implementacao_10.py                      # Implementação 10
│   └── convexo_11.py                            # Implementação 11
│   └── implementacao_12.py                      # Implementação 12
│   └── busca_largura.py                         # Implementação 13
│   └── busca_profundidade_grafos_14.py          # Implementação 14
│   └── implementacao_15.py                      # Implementação 15
│   └── implementacao_16.py                      # Implementação 16
│   └── matriz_incidencia_digrafos_17.py         # Implementação 17
│   └── implementacao_18.py                      # Implementação 18
│   └── implementacao_19.py                      # Implementação 19
│   └── busca_profundidade_digrafos_20.py        # Implementação 20 
│
└── README.md
```

---

## 📄 Formato dos Arquivos de Dados

```
<número de vértices>
<vértice_u>,<vértice_v>
<vértice_u>,<vértice_v>
...
```

- **GRAFOS**: cada aresta é **bidirecional** — `a,b` implica também `b,a`.  
- **DÍGRAFOS**: cada arco é **direcional** — `a,b` significa **DE** `a` **PARA** `b`.

---

## 🗂️ Módulo Base — `src/grafo.py`

Contém as classes e funções utilizadas por todas as implementações:

| Classe / Função       | Descrição                                              |
|-----------------------|--------------------------------------------------------|
| `Grafo`               | Grafo não-dirigido via lista de adjacência             |
| `Digrafo`             | Dígrafo via lista de adjacência                        |
| `ler_grafo(path)`     | Lê arquivo `.txt` e retorna objeto `Grafo`             |
| `ler_digrafo(path)`   | Lê arquivo `.txt` e retorna objeto `Digrafo`           |

---

## 🗂️ Interface de Testes — `src/main.py`

Menu que organiza as implementações e permite testar os métodos desenvolvidos no trabalho.

## ▶️ Como Executar As Implementações

Para testar as funcionalidades do projeto, execute o comando a partir da raiz do projeto:

```bash
python src/main.py
```

> **Requisitos:** Python 3.8+. Nenhuma biblioteca externa é necessária.

---

## 📌 Observações Técnicas

- A estrutura de dados principal é a **lista de adjacência**, implementada com dicionário Python nativo.
- O código está comentado, detalhando entradas, saídas e o funcionamento de cada função.
- Modularidade: Cada funcionalidade foi formulada em arquivos separados 
- Centralização: Embora os scripts sejam independentes, recomendamos utilizar a main.py para a execução do projeto, sendo um menu que integra e gerencia os caminhos de importação para a realização dos testes.
