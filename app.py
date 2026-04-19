import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide", page_title="Dashboard ODM")

# ESTE É O ID DA PLANILHA MESTRE QUE IDENTIFIQUEI NA SUA FOTO
ID_MESTRE = "14cRIHelvGZDUcQGcaH2ieBVv15t36rCPfU2ulmPto8c"
URL_MESTRE = f"https://docs.google.com/spreadsheets/d/{ID_MESTRE}/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Tentativa de leitura direta
    df = conn.read(spreadsheet=URL_MESTRE, worksheet="MARCO26", ttl=0)
    
    if df is not None:
        st.success("✅ CONECTADO À PLANILHA MESTRE!")
        
        # Tratamento básico para exibir algo
        st.subheader("Dados Recentes")
        st.dataframe(df.head(10))
        
        # Exemplo de gráfico rápido com a coluna de volume (Índice 5)
        if len(df.columns) > 5:
            st.subheader("Volume por Entrada")
            st.line_chart(df.iloc[:, 5])
            
except Exception as e:
    st.error(f"Erro Crítico: {e}")
    st.info("💡 Verifique se a planilha original (ID: 14cRI...) está compartilhada como 'Qualquer pessoa com o link'.")
