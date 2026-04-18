import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide", page_title="Dashboard ODM", page_icon="⛽")

# Este é o ID da planilha original que aparece no seu IMPORTRANGE
ID_PLANILHA_ORIGINAL = "14cRIHelvGZDUcQGcaH2ieBVv15t36rCPfU2ulmPto8c"
URL_DIRETA = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA_ORIGINAL}/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Tente ler a aba original (provavelmente "MARÇO26" ou "ODM MARÇO")
    # Se você renomeou para DADOS como sugerido antes, use "DADOS"
    df = conn.read(spreadsheet=URL_DIRETA, worksheet="MARÇO26", ttl=0)
    
    st.success("✅ Conectado direto na fonte de dados!")
    
    # Exibe os dados para você confirmar que carregou
    st.write(df.head())

except Exception as e:
    st.error(f"Erro ao acessar a planilha original: {e}")
    st.info("Certifique-se de que a planilha 'MARÇO26' também está com acesso 'Qualquer pessoa com o link'.")
