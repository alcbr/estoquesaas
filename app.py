import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(layout="wide")

# =========================
# 🎨 ESTILO DARK PROFISSIONAL
# =========================
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #111827;
}
.metric-card {
    background: #1f2937;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 🔗 CONEXÃO GOOGLE SHEETS
# =========================
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    produtos = conn.read(worksheet="produtos")
    mov = conn.read(worksheet="movimentacoes")
except:
    st.error("Erro ao conectar com Google Sheets")
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📦 Estoque SaaS")
menu = st.sidebar.radio("Menu", ["Dashboard", "Produtos", "Entrada", "Saída"])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("📊 Dashboard")

    total_produtos = len(produtos)
    estoque_baixo = produtos[produtos["quantidade"] < 10].shape[0]
    valor_total = (produtos["quantidade"] * produtos["preco"]).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown(f'<div class="metric-card">📦 Produtos<br><h2>{total_produtos}</h2></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-card">⚠️ Estoque Baixo<br><h2>{estoque_baixo}</h2></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-card">💰 Valor Total<br><h2>R$ {valor_total:,.2f}</h2></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-card">📊 Movimentações<br><h2>{len(mov)}</h2></div>', unsafe_allow_html=True)

    st.markdown("## 📈 Visão Geral")

    colA, colB = st.columns([3,1])

    fig = px.bar(produtos, x="nome", y="quantidade")
    colA.plotly_chart(fig, use_container_width=True)

    fig2 = px.pie(produtos, names="categoria", values="quantidade")
    colB.plotly_chart(fig2, use_container_width=True)

    st.markdown("## 📦 Produtos")

    def status(q):
        if q < 10:
            return "🔴 Crítico"
        elif q < 20:
            return "🟡 Atenção"
        return "🟢 Estável"

    produtos["status"] = produtos["quantidade"].apply(status)

    st.dataframe(produtos, use_container_width=True)

# =========================
# PRODUTOS
# =========================
elif menu == "Produtos":
    st.title("📦 Cadastro de Produtos")

    nome = st.text_input("Nome")
    categoria = st.text_input("Categoria")
    preco = st.number_input("Preço", min_value=0.0)
    qtd = st.number_input("Quantidade", min_value=0)

    if st.button("Cadastrar"):
        novo = pd.DataFrame([{
            "id": len(produtos)+1,
            "nome": nome,
            "categoria": categoria,
            "preco": preco,
            "quantidade": qtd
        }])

        produtos = pd.concat([produtos, novo], ignore_index=True)
        conn.update("produtos", produtos)

        st.success("Produto cadastrado!")

# =========================
# ENTRADA
# =========================
elif menu == "Entrada":
    st.title("📥 Entrada de Estoque")

    produto = st.selectbox("Produto", produtos["nome"])
    qtd = st.number_input("Quantidade", min_value=1)

    if st.button("Adicionar"):
        idx = produtos[produtos["nome"] == produto].index[0]
        produtos.loc[idx, "quantidade"] += qtd

        nova = pd.DataFrame([{
            "id": len(mov)+1,
            "produto_id": produtos.loc[idx, "id"],
            "tipo": "entrada",
            "quantidade": qtd,
            "data": datetime.now()
        }])

        mov = pd.concat([mov, nova], ignore_index=True)

        conn.update("produtos", produtos)
        conn.update("movimentacoes", mov)

        st.success("Entrada registrada!")

# =========================
# SAÍDA
# =========================
elif menu == "Saída":
    st.title("📤 Saída de Estoque")

    produto = st.selectbox("Produto", produtos["nome"])
    qtd = st.number_input("Quantidade", min_value=1)

    if st.button("Retirar"):
        idx = produtos[produtos["nome"] == produto].index[0]

        if produtos.loc[idx, "quantidade"] >= qtd:
            produtos.loc[idx, "quantidade"] -= qtd

            nova = pd.DataFrame([{
                "id": len(mov)+1,
                "produto_id": produtos.loc[idx, "id"],
                "tipo": "saida",
                "quantidade": qtd,
                "data": datetime.now()
            }])

            mov = pd.concat([mov, nova], ignore_index=True)

            conn.update("produtos", produtos)
            conn.update("movimentacoes", mov)

            st.success("Saída registrada!")
        else:
            st.error("Estoque insuficiente!")
