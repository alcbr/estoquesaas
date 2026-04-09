import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# 🎨 TEMA DARK PROFISSIONAL
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
}

h1, h2, h3 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 Sistema")
menu = st.sidebar.radio("Menu", ["Dashboard", "Produtos"])

# =========================
# DADOS MOCK (depois liga no Sheets)
# =========================
df = pd.DataFrame({
    "produto": ["Teclado", "Mouse", "Monitor", "Notebook"],
    "categoria": ["Eletrônicos", "Eletrônicos", "Eletrônicos", "Informática"],
    "quantidade": [50, 15, 8, 25]
})

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.title("Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.markdown('<div class="metric-card">📦 Produtos<br><h2>1248</h2></div>', unsafe_allow_html=True)
    col2.markdown('<div class="metric-card">⚠️ Estoque Baixo<br><h2>47</h2></div>', unsafe_allow_html=True)
    col3.markdown('<div class="metric-card">💰 Valor Total<br><h2>R$ 12.8K</h2></div>', unsafe_allow_html=True)
    col4.markdown('<div class="metric-card">🏭 Fornecedores<br><h2>32</h2></div>', unsafe_allow_html=True)

    st.markdown("## 📈 Visão Geral")

    colA, colB = st.columns([3,1])

    # gráfico linha
    fig = px.line(df, x="produto", y="quantidade")
    colA.plotly_chart(fig, use_container_width=True)

    # gráfico pizza
    fig2 = px.pie(df, names="categoria", values="quantidade")
    colB.plotly_chart(fig2, use_container_width=True)

    st.markdown("## 📦 Produtos")

    def status(q):
        if q < 10:
            return "🔴 Crítico"
        elif q < 20:
            return "🟡 Atenção"
        return "🟢 Estável"

    df["status"] = df["quantidade"].apply(status)

    st.dataframe(df, use_container_width=True)

# =========================
# PRODUTOS
# =========================
elif menu == "Produtos":
    st.title("Cadastro de Produtos")

    nome = st.text_input("Nome")
    categoria = st.text_input("Categoria")
    qtd = st.number_input("Quantidade")

    if st.button("Salvar"):
        st.success("Produto cadastrado (simulação)")
