import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection
from urllib.parse import quote

st.set_page_config(layout="wide", page_title="Dashboard ODM", page_icon="⛽")

# ID extraído do seu IMPORTRANGE (Planilha Mãe)
ID_PLANILHA = "14cRIHelvGZDUcQGcaH2ieBVv15t36rCPfU2ulmPto8c"
URL_DIRETA = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # IMPORTANTE: Usei o nome MARCO26 (sem o Ç) para evitar o erro de codec
    # Vá na sua planilha e mude o nome da aba de 'MARÇO26' para 'MARCO26'
    df = conn.read(spreadsheet=URL_DIRETA, worksheet="MARCO26", ttl=0)
    
    st.success("✅ Conectado com sucesso!")

    # --- TRATAMENTO (F=5, P=15, O=14, I=8) ---
    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5].astype(str).str.replace(' L', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15].astype(str).str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14].astype(str).str.replace('R$ ', '').str.replace('.', '').str.replace(',', '.'), errors='coerce').fillna(0)

    # Filtros por Competência (Índice 8)
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]

    # --- MÉTRICAS ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Volume (Fev/Mar)", f"{df_fechados.iloc[:, 5].sum():,.0f} L")
    c2.metric("Total Investido", f"R$ {df_fechados.iloc[:, 15].sum():,.2f}")
    c3.metric("Preço Médio", f"R$ {df_fechados.iloc[:, 14].mean():,.2f}")

    st.markdown("---")
    st.subheader("🚀 Acompanhamento Mês Vigente")
    
    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4, title="Distribuição de Volume")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        st.write("**Resumo Financeiro Atual**")
        st.bar_chart(df_atual.iloc[:, 15])

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
    st.info("👉 SOLUÇÃO: Vá na sua planilha original e mude o nome da aba de 'MARÇO26' para 'MARCO26' (sem o cedilha).")
