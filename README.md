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
│
├── implementacoes/            # Uma implementação por arquivo
│   └── 01.py                  # Implementação 01 
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

## ▶️ Como Executar As Implementações

A partir da raiz do projeto:

```bash
# Implementação 01
python implementacoes/01.py
```

> **Requisitos:** Python 3.8+. Nenhuma biblioteca externa é necessária.

---

## 📌 Observações Técnicas

- A estrutura de dados principal é a **lista de adjacência**, implementada com dicionário Python nativo.
- O código está comentado, detalhando entradas, saídas e o funcionamento de cada função.
- Cada implementação é **independente** e pode ser executada isoladamente.
