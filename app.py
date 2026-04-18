import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página para ocupar a tela toda (estilo dashboard)
st.set_page_config(layout="wide", page_title="Dashboard de Combustível")

# --- SIMULAÇÃO DE DADOS ---
data = {
    'Mes': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
    'Investimento': [400, 450, 500, 420, 600, 550],
    'Consumo_L': [100, 110, 130, 105, 150, 140],
    'SLA_Status': [90, 85, 70, 95, 80, 100]
}
df = pd.DataFrame(data)

st.title("⛽ Painel de Controle de Consumo de Combustível")

# --- LINHA 1: MÉTRICAS (KPIs) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Investido", "R$ 4.76k", "+12%")
col2.metric("Total Litros", "5.19k L", "-5%")
col3.metric("KM Médio/L", "12.5 km/l", "0.8%")
col4.metric("Eficiência da Frota", "85%", "SLA OK")

st.markdown("---")

# --- LINHA 2: GRÁFICOS PRINCIPAIS ---
c1, c2, c3 = st.columns([1, 1, 1])

with c1:
    st.subheader("Investimento Mensal")
    # Gráfico de Radar ou Linha para simular o "Monthly Revenues"
    fig_radar = px.line_polar(df, r='Investimento', theta='Mes', line_close=True)
    st.plotly_chart(fig_radar, use_container_width=True)

with c2:
    st.subheader("Distribuição por Veículo")
    fig_pie = px.pie(df, values='Consumo_L', names='Mes', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with c3:
    st.subheader("Satisfação/Eficiência")
    # Indicador Gauge (Igual ao da imagem)
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 71.76,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Projeto 4"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#f9a825"}}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

# --- LINHA 3: BARRAS EMPILHADAS ---
st.subheader("Gastos Detalhados por Categoria")
fig_bar = px.bar(df, x='Mes', y=['Investimento', 'Consumo_L'], barmode='stack')
st.plotly_chart(fig_bar, use_container_width=True)
