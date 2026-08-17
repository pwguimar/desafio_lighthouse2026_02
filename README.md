# ⚓ LH Nautical — Desafio Indicium 2026

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)](https://streamlit.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-1.0+-green.svg)](https://duckdb.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Análise estratégica de 24 tabelas relacionais da LH Nautical: identificação de clientes elite, sazonalidade por calendário, previsão de demanda e sistema de recomendação item-based.

---

**Analista:** Patrick Wöhrle Guimarães  
**Data:** Agosto de 2026  
**Ferramentas:** Python 3 · DuckDB · Pandas · Scikit-learn · Streamlit

---

## Entregáveis

| Produto | Descrição | Link |
|---------|-----------|------|
| **Notebook Analítico** | Análise completa das 7 questões, com validação cruzada Python × DuckDB | [Abrir no GitHub](https://github.com/pwguimar/desafio_lighthouse2026_02/blob/main/2026_02_LIghthouse_Dados%26AI.ipynb) |
| **Dashboard Interativo** | Visualização dos principais resultados em interface amigável | [Abrir no Streamlit Cloud](https://desafiolighthouse202602.streamlit.app/) *ou* executar localmente |
| **Schema SQL** | DDL das 24 tabelas gerado automaticamente | [`schema.sql`](https://github.com/pwguimar/desafio_lighthouse2026_02/blob/main/schema.sql) |
| **Sumário Executivo** | Relatório em PDF com os principais insights para a diretoria | [`Sumário Executivo`](https://github.com/pwguimar/desafio_lighthouse2026_02/blob/main/SumarioExecutivo_LigthhouseDesafio2026.pdf) |

---

## Sobre o Projeto

A LH Nautical é uma rede náutica com lojas físicas e e-commerce. O desafio propôs a construção de um pipeline analítico completo a partir de 24 arquivos CSV do ERP, abordando 7 questões técnicas:

📊 **48.998 pedidos** analisados · **147.320 itens** · **2.000 clientes**  
👑 **10 clientes elite** com ticket médio entre R$ 39,5K e R$ 41,8K  
📅 **Quinta-feira** identificada como pior dia de vendas (R$ 157,2K/dia)  
📈 **Baseline de previsão** com MAE de 19,44 unidades  
🎯 **Sistema de recomendação** com similaridade de cosseno (0,2566)  

---

## Estrutura do Repositório

```
desafio_lighthouse2026_02/
├── 2026_02_LIghthouse_Dados&AI.ipynb    ← Notebook principal com toda a análise
├── 2026_02_LIghthouse_dados&ai.py       ← Notebook principal com toda a análise em Python
├── streamlit_app.py                      ← Dashboard interativo
├── requirements.txt                      ← Dependências do projeto
├── README.md                             ← Este arquivo
├── schema.sql                            ← DDL das 24 tabelas (Questão 02)
├── lh_nautical.duckdb                    ← Banco DuckDB com 24 tabelas carregadas
├── 1-lh_nautical_csv.zip                 ← Dados originais do desafio fornecidos pela Indicium
├── SumarioExecutivo_LigthhouseDesafio2026 ← Sumário Executivo do projeto em .pdf
└── data_dashboard/                       ← CSVs agregados para o dashboard
    ├── kpi.csv
    ├── eda_canal_status.csv
    ├── clientes_elite.csv
    ├── categorias_elite.csv
    ├── calendario_dia_semana.csv
    ├── previsao_demanda.csv
    └── recomendacao.csv
```

---

## Como Executar Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/pwguimar/lh-nautical-indicium-2026.git
cd lh-nautical-indicium-2026
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute o dashboard
```bash
streamlit run streamlit_app.py
```

---

## Questões Respondidas

### Q1 — EDA (Análise Exploratória de Dados)

**Resultados:** 48.998 registros · 13 colunas · Período: 2020-01-01 a 2026-12-31 · Mínimo: R$ 32,62 · Máximo: R$ 127.262,02 · Média: R$ 28.704,99 · Zero duplicatas

**Conclusão:** Dataset com boa integridade estrutural, mas requer tratamento de outliers (452 registros acima do limite IQR) e investigação de nulos em `salesperson_id` (49,2%).

### Q2 — Geração de Schema SQL

**Resultado:** DDL das 24 tabelas gerado automaticamente via Python puro (sem pandas), com inferência de tipos e proteção de overflow para IDs longos.

**Destino:** DuckDB

### Q3 — Carregamento de Dados

**Resultado:** 251.864 linhas carregadas nas 4 tabelas críticas de validação.

| Tabela | Linhas |
| :--- | ---: |
| customers | 2.000 |
| orders | 48.998 |
| order_items | 147.320 |
| payments | 53.546 |
| **Total** | **251.864** |

### Q4 — Análise de Clientes Fiéis

**Resultado:** Top 10 clientes com ticket médio entre R$ 39.532,94 e R$ 41.839,94, todos com 14 categorias distintas.

**Categoria líder:** Hélices (492 itens)

**Metodologia:** Faturamento calculado diretamente sobre `orders` (sem fan-out), diversidade via cadeia `orders → order_items → product_variants → products → categories`, filtro ≥ 13 categorias, ordenação por ticket médio decrescente com desempate por `customer_id`.

**Sensibilidade:** Com filtro `status IN ('confirmed','paid')`, o Top 10 se altera (entram 300, 1527, 1784, 21; saem 929, 1116, 774, 1599).

### Q5 — Dimensão de Calendário

**Resultado:** Pior dia de vendas: **Quinta-feira** (R$ 157.154,32/dia). Melhor dia: Quarta-feira (R$ 173.605,44/dia).

**Metodologia:** `generate_series` + `LEFT JOIN` + `COALESCE` para incluir dias sem venda no cálculo.

**Viés do estagiário:** R$ 9.084,06/dia (média ingênua vs corrigida).

### Q6 — Previsão de Demanda

**Produto:** Bússola de Bordo 702

**Resultado:** Soma prevista Q1 2026: **149 unidades**. MAE: 19,44 unidades. Real: 207 unidades (subestimativa de 58 unidades, ~28%).

**Modelo:** Média móvel simples com janela de 3 meses, regime 1-step-ahead, anti-leakage.

**Limitação:** Não captura sazonalidade nem tendência.

### Q7 — Sistema de Recomendação

**Produto referência:** Motor de Popa 1949 (ID 180)

**Produto mais similar:** Motor de Popa 5331 (similaridade 0,2566)

**Matriz:** 2.000 clientes × 500 produtos · Densidade: 13,6% · 135.508 interações

**Top 5 produtos similares:**

| Rank | Produto | Similaridade |
| :--- | :--- | ---: |
| 1º | Motor de Popa 5331 | 0,2566 |
| 2º | Cabo Náutico 2105 | 0,2562 |
| 3º | Vela Mestra 1913 | 0,2558 |
| 4º | Cabo Náutico 9048 | 0,2393 |
| 5º | GPS Plotter 6249 | 0,2377 |

**Metodologia:** Matriz binária Usuário × Produto, similaridade de cosseno, validação cruzada Python × SQL.

---

## Principais Achados

| Dimensão | Resultado |
|---|---|
| Total de pedidos | 48.998 |
| Total de itens | 147.320 |
| Clientes | 2.000 |
| Ticket médio — clientes elite | R$ 39.532,94 a R$ 41.839,94 |
| Categoria líder — elite | Hélices (492 itens) |
| Pior dia de vendas | Quinta-feira — R$ 157.154,32/dia |
| Viés do estagiário | R$ 9.084,06/dia |
| MAE do modelo baseline | 19,44 unidades |
| Soma prevista Q1 2026 | 149 unidades (real: 207) |
| Produto mais similar | Motor de Popa 5331 (0,2566) |

---

## Dashboard Interativo

O projeto inclui um dashboard desenvolvido em Streamlit com as seguintes seções:

- 📊 Visão Geral — KPIs, composição de pedidos por canal × status
- 👑 Clientes Elite (Q4) — top 10 e categorias preferidas
- 📅 Calendário (Q5) — média por dia da semana com correção de viés
- 📈 Previsão de Demanda (Q6) — real vs previsto
- 🎯 Recomendação (Q7) — top 5 produtos similares ao Motor de Popa 1949

Para executar: `streamlit run streamlit_app.py`

---

## Validação Cruzada (Python vs SQL)

Todas as análises principais foram implementadas em Python e validadas via SQL com DuckDB, garantindo consistência e auditabilidade dos resultados. As queries SQL utilizadas estão documentadas no notebook.

---

## Stack Técnico

| Biblioteca | Papel |
|---|---|
| pandas | Manipulação de dados |
| numpy | Operações numéricas |
| duckdb | SQL sobre DataFrames — validação cruzada |
| scikit-learn | Similaridade de cosseno |
| matplotlib / seaborn | Visualizações no notebook |
| streamlit | Dashboard interativo |

---

## Licença

Este projeto foi desenvolvido para fins de avaliação no Desafio Indicium 2026.
