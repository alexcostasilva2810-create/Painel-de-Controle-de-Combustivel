import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard ODM - Combustível")

# --- CONEXÃO COM O GOOGLE SHEETS ---
# Certifique-se de que a URL da sua planilha esteja correta abaixo
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1izHisQGFCLdqQ7d2OSGkAM7gDJrIsLxW9FY741lJ_Ao/edit?gid=0#gid=0"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Lendo a aba específica
    df = conn.read(spreadsheet=URL_PLANILHA, worksheet="ODM MARÇO")
except Exception as e:
    st.error(f"Erro na conexão: {e}")
    st.stop()

# --- TRATAMENTO DOS DADOS ---
# Índices confirmados: F=5 (Volume), P=15 (Total R$), O=14 (Média R$), I=8 (Competência)
try:
    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14], errors='coerce').fillna(0)
    
    # Lógica de Meses (Baseado na coluna de índice 8)
    # Filtramos meses fechados (Ex: 02 e 03) e o vigente (04)
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]
except Exception as e:
    st.warning("Verifique se as colunas da planilha estão na ordem correta.")

# --- INTERFACE ---
st.title("⛽ Painel de Operações de Combustível")

# --- SEÇÃO 1: MESES CONSOLIDADOS (FECHADOS) ---
st.header("📊 Consolidação de Meses Fechados")
c1, c2, c3 = st.columns(3)

with c1:
    vol_fechado = df_fechados.iloc[:, 5].sum()
    st.metric("Volume Total Comprado", f"{vol_fechado:,.0f} L")
with c2:
    valor_fechado = df_fechados.iloc[:, 15].sum()
    st.metric("Total em Reais", f"R$ {valor_fechado:,.2f}")
with c3:
    media_fechada = df_fechados.iloc[:, 14].mean()
    st.metric("Média do Período", f"R$ {media_fechada:,.2f}")

st.markdown("---")

# --- SEÇÃO 2: MÊS VIGENTE (ABRIL) ---
st.header("🚀 Acompanhamento Mês Vigente")
col_left, col_mid, col_right = st.columns(3)

with col_left:
    st.write("**Volume por Veículo**")
    # Coluna B (índice 1) como nome do veículo
    fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_mid:
    st.write("**Evolução de Compras**")
    st.bar_chart(df_atual.iloc[:, 5])

with col_right:
    st.write("**Preço Médio Atual**")
    media_atual = df_atual.iloc[:, 14].mean()
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = media_atual,
        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#f9a825"}},
        number = {'prefix': "R$ "}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# Tabela detalhada
with st.expander("Ver lista completa do mês atual"):
    st.dataframe(df_atual)
