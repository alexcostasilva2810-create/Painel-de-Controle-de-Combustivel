import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Dashboard ODM - Combustível")

# --- CONEXÃO COM O GOOGLE SHEETS ---
url = "SUA_URL_DA_PLANILHA_AQUI"
conn = st.connection("gsheets", type=GSheetsConnection)

# Lendo a aba específica
df = conn.read(spreadsheet=url, worksheet="ODM MARÇO")

# --- TRATAMENTO DOS DADOS (Baseado nos índices que você passou) ---
# F=Volume(5), P=Total(15), O=Média(14), I=Competência(8)
df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0)
df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14], errors='coerce').fillna(0)

# Definindo quem é o mês atual (Vigente) e quem são os anteriores (Fechados)
# Exemplo: Se estivermos em Abril, meses 02 e 03 são fechados.
mes_vigente = "04" 
df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
df_atual = df[df.iloc[:, 8].astype(str).str.contains(mes_vigente, na=False)]

st.title("⛽ Painel de Operações de Combustível")

# --- SEÇÃO 1: MESES CONSOLIDADOS (FECHADOS) ---
st.subheader("📊 Consolidação de Meses Fechados (Fev/Mar)")
c1, c2, c3 = st.columns(3)

with c1:
    vol_fechado = df_fechados.iloc[:, 5].sum()
    st.metric("Total Volume Comprado", f"{vol_fechado:,.0f} L")
with c2:
    valor_fechado = df_fechados.iloc[:, 15].sum()
    st.metric("Total em Reais (R$)", f"R$ {valor_fechado:,.2f}")
with c3:
    media_fechada = df_fechados.iloc[:, 14].mean()
    st.metric("Média do Período", f"R$ {media_fechada:,.2f}")

st.markdown("---")

# --- SEÇÃO 2: MÊS VIGENTE (ABRIL) - ESTILO DASHBOARD ---
st.subheader(f"📅 Acompanhamento Mês Vigente (Mês {mes_vigente})")

col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

# KPI 1: Gráfico de Pizza (Volume por Veículo ou Motorista - Coluna B/C)
with col_kpi1:
    st.write("**Distribuição de Volume**")
    fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
    fig_pie.update_layout(showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# KPI 2: Gráfico de Barras Empilhadas (Volume Diário/Pedido)
with col_kpi2:
    st.write("**Histórico de Compras no Mês**")
    st.bar_chart(df_atual.iloc[:, 5])

# KPI 3: Gauge de Média de Preço (Comparando com a meta ou média anterior)
with col_kpi3:
    media_atual = df_atual.iloc[:, 14].mean()
    st.write("**Média de Preço Atual**")
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = media_atual,
        gauge = {'axis': {'range': [0, 10]}, 'bar': {'color': "#f9a825"}},
        number = {'prefix': "R$ "}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# TABELA DE DETALHES DO MÊS ATUAL
with st.expander("Visualizar listagem detalhada do mês vigente"):
    st.dataframe(df_atual)
