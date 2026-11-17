import pandas as pd
import plotly.express as px
import streamlit as st
from src import metrics as m
from src.chat import responder

st.set_page_config(page_title="Data Pilot", page_icon="📊", layout="wide")


@st.cache_data
def dados() -> pd.DataFrame:
    return m.carregar()


df = dados()
menu = st.sidebar.radio("Menu", ["Painel", "Conversa com os dados"])

if menu == "Painel":
    st.title("📊 Data Pilot — Painel de vendas")
    cat = st.selectbox("Categoria", ["Todas"] + sorted(df["category"].unique()))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita total", f"R$ {m.receita_total(df, cat):,.2f}")
    c2.metric("Pedidos", m.total_pedidos(df, cat))
    c3.metric("Ticket médio", f"R$ {m.ticket_medio(df, cat):,.2f}")
    c4.metric("Receita média por cliente", f"R$ {m.receita_media_por_cliente(df, cat):,.2f}")
    st.plotly_chart(px.bar(m.receita_por_mes(df, cat), x="mes", y="receita", title="Receita por mês"),
                    use_container_width=True)
    st.plotly_chart(px.bar(m.top_cidades(df, cat), x="cidade", y="receita", title="Top 5 cidades"),
                    use_container_width=True)
else:
    st.title("💬 Converse com os dados")
    st.caption("O Python calcula; a IA só explica.")
    if "hist" not in st.session_state:
        st.session_state.hist = []
    for papel, texto in st.session_state.hist:
        st.chat_message(papel).write(texto)
    if pergunta := st.chat_input("Ex.: Qual a receita média por cliente em Moda?"):
        st.chat_message("user").write(pergunta)
        with st.spinner("Consultando..."):
            resposta = responder(pergunta, df)
        st.chat_message("assistant").write(resposta)
        st.session_state.hist += [("user", pergunta), ("assistant", resposta)]
