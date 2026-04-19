import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard ODM - Combustível", page_icon="⛽")

# ID da planilha original (extraído do seu IMPORTRANGE)
ID_PLANILHA = "14cRIHelvGZDUcQGcaH2ieBVv15t36rCPfU2ulmPto8c"
URL_DIRETA = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    # Criando a conexão
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo a aba MARCO26 (certifique-se de que renomeou na planilha!)
    df = conn.read(spreadsheet=URL_DIRETA, worksheet="MARCO26", ttl=0)
    
    # --- TRATAMENTO DOS DADOS ---
    # Limpando as colunas F(5), P(15) e O(14) para virarem números
    def limpar_valor(valor):
        if isinstance(valor, str):
            return valor.replace('L', '').replace('R$', '').replace('.', '').replace(',', '.').strip()
        return valor

    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5].apply(limpar_valor), errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15].apply(limpar_valor), errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14].apply(limpar_valor), errors='coerce').fillna(0)

    # --- FILTROS POR COMPETÊNCIA (Índice 8) ---
    # Separando meses fechados (02, 03) e o mês vigente (04)
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]

    # --- SEÇÃO 1: MÉTRICAS CONSOLIDADAS ---
    st.subheader("📊 Consolidação de Meses Fechados (Fev/Mar)")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        st.metric("Volume Total", f"{df_fechados.iloc[:, 5].sum():,.0f} L")
    with m2:
        st.metric("Investimento Total", f"R$ {df_fechados.iloc[:, 15].sum():,.2f}")
    with m3:
        st.metric("Média de Preço", f"R$ {df_fechados.iloc[:, 14].mean():,.2f}")

    st.markdown("---")

    # --- SEÇÃO 2: DASHBOARD ABRIL (VIGENTE) ---
    st.subheader("🚀 Acompanhamento Mês Vigente (Abril)")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.write("**Volume por Veículo**")
        # Coluna B (índice 1) é o Veículo
        fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.write("**Histórico de Volume**")
        st.bar_chart(df_atual.iloc[:, 5])

    with c3:
        st.write("**Média de Preço Atual**")
        media_a = df_atual.iloc[:, 14].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = media_a,
            number = {'prefix': "R$ ", 'valueformat': ".2f"},
            gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#f9a825"}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.info("Verifique se a aba na planilha foi renomeada para MARCO26 e se o link está público.")
