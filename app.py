st.set_page_config(layout="wide")

# CSS customizado
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Produtos", "1.248", "+12%")
col2.metric("Estoque Baixo", "47", "-5%")
col3.metric("Valor Total", "R$ 1.284", "+8%")
col4.metric("Fornecedores", "32", "+12")
import pandas as pd

data = pd.DataFrame({
    "mes": ["Jan","Fev","Mar","Abr","Mai"],
    "estoque": [30,28,40,42,45]
})

st.line_chart(data.set_index("mes"))
def status(qtd):
    if qtd < 10:
        return "🔴 Crítico"
    elif qtd < 20:
        return "🟡 Atenção"
    else:
        return "🟢 Estável"

produtos["status"] = produtos["quantidade"].apply(status)

st.dataframe(produtos)
st.bar_chart(produtos.groupby("categoria")["quantidade"].sum())
