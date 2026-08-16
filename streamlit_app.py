# =============================================================================
# DESAFIO INDICIUM 2026 — LH NAUTICAL
# Dashboard Executivo (Streamlit + matplotlib)
# Autor: Patrick Wöhrle Guimarães · Agosto 2026
# =============================================================================

import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'DejaVu Sans'
plt.style.use('seaborn-v0_8-whitegrid')

AZUL = '#0E4C92'
VERDE = '#1D9E75'
LARANJA = '#E67E22'
CINZA = '#7F8C8D'

st.set_page_config(page_title="LH Nautical — Indicium 2026", page_icon="⚓", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 2rem;}
    h1 {color:#0E4C92;}
</style>
""", unsafe_allow_html=True)

DATA_DIR = "data_dashboard" if os.path.isdir("data_dashboard") else "."
ORDEM_DIAS = ["Segunda-feira", "Terça-feira", "Quarta-feira",
              "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

# --- Carregamento defensivo (lição do desafio passado) -----------------------
@st.cache_data
def load(nome, cols_esperadas=None, min_rows=1):
    caminho = os.path.join(DATA_DIR, nome)
    if not os.path.exists(caminho):
        return None
    try:
        df = pd.read_csv(caminho)
    except Exception:
        return None
    if cols_esperadas and not all(c in df.columns for c in cols_esperadas):
        return None
    if len(df) < min_rows:
        return None
    return df

def brl(v): return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def num(v): return f"{int(v):,}".replace(",", ".")

def erro_dados():
    st.error("Dados não encontrados ou em formato inesperado. Rode a célula de exportação no Colab e baixe o ZIP novamente.")
    st.stop()

# --- Sidebar -----------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚓ LH Nautical")
    st.markdown("**Desafio Indicium 2026**")
    st.markdown("---")
    pagina = st.radio("Navegação",
        ["🏠 Visão Executiva", "🔍 Qualidade dos Dados (Q1)", "👑 Clientes Fiéis (Q4)",
         "📅 Sazonalidade (Q5)", "📈 Previsão de Demanda (Q6)", "🎯 Recomendação (Q7)",
         "💡 Insights Finais"])
    st.markdown("---")
    st.markdown("**Autor**")
    st.markdown("Patrick Wöhrle Guimarães")
    st.markdown("**Data:** Agosto de 2026")

kpi = load("kpi.csv", ["pedidos", "faturamento", "clientes", "produtos", "inicio", "fim"])

# ============================================================================
if pagina == "🏠 Visão Executiva":
    st.title("⚓ LH Nautical — Painel Executivo")
    st.caption("Análise estratégica de 24 tabelas do ERP · Validação cruzada Python × DuckDB")
    st.markdown("---")
    if kpi is None: erro_dados()
    k = kpi.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Pedidos", num(k["pedidos"]))
    c2.metric("💰 Faturamento", brl(k["faturamento"]))
    c3.metric("🧑‍🤝‍🧑 Clientes", num(k["clientes"]))
    c4.metric("🛍️ Produtos", num(k["produtos"]))
    st.caption(f"📅 Período: **{k['inicio']}** a **{k['fim']}**")

    st.markdown("---")
    st.subheader("🎯 Principais Descobertas")
    cal = load("calendario_dia_semana.csv", ["dia_semana", "media_corrigida"])
    cats = load("categorias_elite.csv", ["categoria", "total_itens"])
    prev = load("previsao_demanda.csv", ["mes", "real", "previsao"])
    rec = load("recomendacao.csv", ["name", "similaridade"])
    d1, d2, d3, d4 = st.columns(4)
    if cal is not None:
        pior = cal.loc[cal["media_corrigida"].idxmin()]
        d1.markdown("**📅 Pior dia de vendas**"); d1.markdown(f"### {pior['dia_semana']}"); d1.markdown(f"{brl(pior['media_corrigida'])}/dia")
    if cats is not None:
        d2.markdown("**👑 Âncora do segmento elite**"); d2.markdown(f"### {cats.iloc[0]['categoria']}"); d2.markdown(f"{int(cats.iloc[0]['total_itens'])} itens no grupo")
    if prev is not None:
        t = prev.dropna(subset=["previsao"])
        d3.markdown("**📈 Precisão do baseline**"); d3.markdown(f"### MAE {(t['real']-t['previsao']).abs().mean():.1f} un."); d3.markdown("Bússola de Bordo 702")
    if rec is not None:
        d4.markdown("**🎯 Top recomendação**"); d4.markdown(f"### {rec.iloc[0]['name']}"); d4.markdown(f"similaridade {rec.iloc[0]['similaridade']:.3f}")

    st.markdown("---")
    st.info("A LH Nautical opera lojas físicas e e-commerce. Este painel responde quem são os clientes mais valiosos, quando a loja física performa menos, quanto venderemos de um produto-chave e o que recomendar junto de cada item — tudo com validação cruzada Python × DuckDB.")

# ============================================================================
elif pagina == "🔍 Qualidade dos Dados (Q1)":
    st.title("🔍 Qualidade e Composição dos Pedidos")
    st.caption("Questão 1 · Análise Exploratória da tabela `orders`")
    eda = load("eda_canal_status.csv", ["channel", "status", "pedidos", "faturamento"])
    if eda is None: erro_dados()

    a, b = st.columns(2)
    with a:
        fig, ax = plt.subplots(figsize=(6, 4))
        eda.groupby("channel")["pedidos"].sum().plot(kind="bar", ax=ax, color=[AZUL, VERDE])
        ax.set_title("Pedidos por Canal"); ax.set_ylabel("Pedidos"); ax.set_xlabel("")
        plt.xticks(rotation=0); plt.tight_layout(); st.pyplot(fig); plt.close(fig)
    with b:
        fig, ax = plt.subplots(figsize=(6, 4))
        eda.groupby("status")["pedidos"].sum().plot(kind="bar", ax=ax, color=LARANJA)
        ax.set_title("Pedidos por Status"); ax.set_ylabel("Pedidos"); ax.set_xlabel("")
        plt.xticks(rotation=0); plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.dataframe(eda, use_container_width=True, hide_index=True)
    st.warning("⚠️ Pedidos `cancelled` e `draft` têm valor preenchido mas **não são receita realizada**. Análises de faturamento devem filtrá-los. Mantivemos todos por fidelidade às premissas, mas o alerta fica registrado.")
    with st.expander("📚 Nota metodológica"):
        st.markdown("- 48.998 linhas · 13 colunas · sem duplicatas completas\n- 452 outliers (0,9%) acima do limite IQR em `total`\n- `salesperson_id` nulo em ~49% (padrão do canal ecommerce)")

# ============================================================================
elif pagina == "👑 Clientes Fiéis (Q4)":
    st.title("👑 Clientes Fiéis — Segmento Elite")
    st.caption("Questão 4 · Ticket médio alto × diversidade ≥ 13 categorias")
    elite = load("clientes_elite.csv", ["customer_id", "ticket_medio", "faturamento_total"])
    cats = load("categorias_elite.csv", ["categoria", "total_itens"])
    if elite is None or cats is None: erro_dados()

    m1, m2, m3 = st.columns(3)
    m1.metric("Clientes no ranking", num(len(elite)))
    m2.metric("Ticket médio (mín)", brl(elite["ticket_medio"].min()))
    m3.metric("Ticket médio (máx)", brl(elite["ticket_medio"].max()))
    st.markdown("---")

    a, b = st.columns([3, 2])
    with a:
        fig, ax = plt.subplots(figsize=(7, 5))
        elite_sorted = elite.sort_values("ticket_medio")
        ax.barh(elite_sorted["customer_id"].astype(str), elite_sorted["ticket_medio"], color=AZUL)
        ax.set_title("Top 10 por Ticket Médio"); ax.set_xlabel("Ticket Médio (R$)")
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)
    with b:
        fig, ax = plt.subplots(figsize=(6, 5))
        top_cats = cats.sort_values("total_itens").tail(8)
        ax.barh(top_cats["categoria"], top_cats["total_itens"], color=VERDE)
        ax.set_title("Categorias do Grupo Elite"); ax.set_xlabel("Itens")
        plt.tight_layout(); st.pyplot(fig); plt.close(fig)
        st.success(f"**Âncora:** {cats.iloc[0]['categoria']} com {int(cats.iloc[0]['total_itens'])} itens")

    st.dataframe(elite, use_container_width=True, hide_index=True)
    st.info(f"💡 Os 10 clientes elite navegam por 14 categorias e gastam em média {brl(elite['ticket_medio'].mean())} por transação. A concentração em {cats.iloc[0]['categoria']} é a âncora ideal para campanhas de cross-sell.")

# ============================================================================
elif pagina == "📅 Sazonalidade (Q5)":
    st.title("📅 Média de Vendas por Dia da Semana")
    st.caption("Questão 5 · Lojas físicas (pos) · Calendário completo com dias sem venda")
    cal = load("calendario_dia_semana.csv", ["dia_semana", "media_corrigida", "media_ingenua"])
    if cal is None: erro_dados()
    cal = cal.copy()
    cal["dia_semana"] = pd.Categorical(cal["dia_semana"], categories=ORDEM_DIAS, ordered=True)
    cal = cal.sort_values("dia_semana")
    pior = cal.loc[cal["media_corrigida"].idxmin()]
    melhor = cal.loc[cal["media_corrigida"].idxmax()]

    m1, m2, m3 = st.columns(3)
    m1.metric("🔻 Pior dia", pior["dia_semana"], brl(pior["media_corrigida"]))
    m2.metric("🔺 Melhor dia", melhor["dia_semana"], brl(melhor["media_corrigida"]))
    m3.metric("Viés do estagiário", brl(pior["media_ingenua"] - pior["media_corrigida"]))

    fig, ax = plt.subplots(figsize=(11, 5))
    x = np.arange(len(cal)); w = 0.4
    ax.bar(x - w/2, cal["media_corrigida"], w, label="Corrigida (com zeros)", color=AZUL)
    ax.bar(x + w/2, cal["media_ingenua"], w, label="Ingênua (erro)", color=LARANJA)
    ax.set_xticks(x); ax.set_xticklabels(cal["dia_semana"], rotation=20, ha="right")
    ax.set_ylabel("Média de Vendas (R$)"); ax.set_title("Média Corrigida vs. Ingênua")
    ax.legend(); plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.dataframe(cal, use_container_width=True, hide_index=True)
    st.warning(f"⚠️ Agrupar direto a tabela de vendas ignora dias sem venda. Na {pior['dia_semana']}, isso inflava a média em {brl(pior['media_ingenua'] - pior['media_corrigida'])}/dia, mascarando que é o pior dia da semana.")
    st.info(f"💡 Recomendação ao Sr. Almir: a {pior['dia_semana']} tem a menor média real ({brl(pior['media_corrigida'])}/dia). Avaliar horário reduzido ou promoção específica antes de decidir fechamento.")

# ============================================================================
elif pagina == "📈 Previsão de Demanda (Q6)":
    st.title("📈 Previsão de Demanda — Bússola de Bordo 702")
    st.caption("Questão 6 · Baseline média móvel 3 meses · Anti data-leakage")
    prev = load("previsao_demanda.csv", ["mes", "real", "previsao"])
    if prev is None: erro_dados()
    prev = prev.copy()
    prev["mes"] = pd.to_datetime(prev["mes"])
    teste = prev[(prev["mes"] >= "2026-01-01") & (prev["mes"] <= "2026-03-31") & prev["previsao"].notna()]
    mae = (teste["real"] - teste["previsao"]).abs().mean()
    soma_prev = round(teste["previsao"].sum()); real_q1 = int(teste["real"].sum())

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("MAE (Q1 2026)", f"{mae:.2f} un.")
    m2.metric("Soma prevista", f"{soma_prev} un.")
    m3.metric("Real vendido", f"{real_q1} un.")
    m4.metric("Subestimativa", f"{real_q1 - soma_prev} un.")

    janela = st.slider("Janela (últimos N meses)", 6, len(prev), 24)
    view = prev.tail(janela)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(view["mes"], view["real"], color=VERDE, linewidth=2, marker="o", markersize=4, label="Real")
    ax.plot(view["mes"], view["previsao"], color=LARANJA, linewidth=2, linestyle="--", marker="x", markersize=6, label="Previsto")
    ax.set_title("Real vs. Previsto — Bússola de Bordo 702")
    ax.set_ylabel("Unidades"); ax.legend(); ax.grid(alpha=0.3)
    plt.xticks(rotation=45); plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    st.dataframe(teste, use_container_width=True, hide_index=True)
    st.warning(f"⚠️ O baseline previu {soma_prev} unidades, real foi {real_q1} — subestimativa de {(real_q1 - soma_prev)/real_q1*100:.0f}%. A média móvel não captura sazonalidade de verão. Para produção, migrar para modelo sazonal (Holt-Winters/Prophet).")

# ============================================================================
elif pagina == "🎯 Recomendação (Q7)":
    st.title("🎯 Vitrine 'Quem comprou isso, também levou…'")
    st.caption("Questão 7 · Referência: Motor de Popa 1949 · Similaridade de cosseno")
    rec = load("recomendacao.csv", ["name", "similaridade"])
    if rec is None: erro_dados()

    st.success(f"**Produto mais similar:** {rec.iloc[0]['name']} (similaridade {rec.iloc[0]['similaridade']:.4f})")

    fig, ax = plt.subplots(figsize=(9, 5))
    rec_sorted = rec.sort_values("similaridade")
    ax.barh(rec_sorted["name"], rec_sorted["similaridade"], color=AZUL)
    ax.set_title("Top 5 Similares ao Motor de Popa 1949"); ax.set_xlabel("Similaridade de Cosseno")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout(); st.pyplot(fig); plt.close(fig)

    rec_show = rec.copy(); rec_show.insert(0, "rank", range(1, len(rec_show) + 1))
    st.dataframe(rec_show, use_container_width=True, hide_index=True)
    st.info("💡 Implementar cross-sell ao lado do Motor de Popa 1949. Topo ser outro motor indica comparação/reposição entre modelos da mesma família; acessórios sustentam vendas complementares. Base: matriz binária 2.000×500, validação cruzada.")
    with st.expander("📚 Nota metodológica"):
        st.markdown("- Cosseno sobre vetores de presença (comprou=1)\n- Quantidade ignorada; produto de referência excluído\n- **Cold start:** produtos novos sem histórico não são recomendados")

# ============================================================================
elif pagina == "💡 Insights Finais":
    st.title("💡 Insights & Recomendações Consolidadas")
    st.markdown("---")
    st.subheader("1. 👑 Clientes Elite (Q4)")
    st.markdown("- 10 clientes gastam entre **R$ 39,5 mil e R$ 41,8 mil** por transação, navegando por 14 categorias.\n- **Hélices** é a âncora de consumo do grupo.")
    st.subheader("2. 📅 Sazonalidade (Q5)")
    st.markdown("- **Quinta-feira** é o pior dia das lojas físicas (R$ 157.154/dia), não o Domingo.\n- Método do estagiário inflava a média em ~R$ 9.084/dia.")
    st.subheader("3. 📈 Previsão de Demanda (Q6)")
    st.markdown("- Baseline subestima o Q1 em ~28% (não captura sazonalidade de verão).\n- Migrar para modelo sazonal antes do próximo verão.")
    st.subheader("4. 🎯 Recomendação (Q7)")
    st.markdown("- **Motor de Popa 5331** é o item ideal para a vitrine junto ao Motor de Popa 1949.")
    st.markdown("---")
    st.subheader("🚀 Próximos Passos")
    st.markdown("1. Vitrine de cross-sell com Hélices e Motores como âncoras.\n2. Reavaliar operação de Quinta-feira nas lojas físicas.\n3. Modelo sazonal de previsão antes do verão.\n4. Campanhas direcionadas ao segmento elite.\n5. Filtrar `cancelled`/`draft` em análises de receita.")