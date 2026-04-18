import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

# Configuração da página para estilo Dashboard
st.set_page_config(layout="wide", page_title="Painel ODM - Combustível", page_icon="⛽")

# --- CONFIGURAÇÃO DA CONEXÃO ---
# Substitua pelo seu link real do Google Sheets
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1izHisQGFCLdqQ7d2OSGkAM7gDJrlsLxW9FY741lJ_Ao/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    # Criando a conexão
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo os dados (IMPORTANTE: Renomeie sua aba no Google para ODM_MARCO)
    df = conn.read(spreadsheet=URL_PLANILHA, worksheet="ODM_MARCO", ttl=0)
    
    # --- TRATAMENTO DE DADOS ---
    # Índices baseados na sua planilha: 
    # F=5 (Volume), P=15 (Total R$), O=14 (Preço Médio), I=8 (Competência)
    
    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14], errors='coerce').fillna(0)
    
    # Filtro de Meses (Coluna I - Índice 8)
    # Ajuste os nomes conforme aparecem exatamente na sua coluna de competência
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]

    # --- SEÇÃO 1: MÉTRICAS CONSOLIDADAS (Meses Fechados) ---
    st.subheader("📊 Consolidação: Fevereiro e Março")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        vol_f = df_fechados.iloc[:, 5].sum()
        st.metric("Volume Total Comprado", f"{vol_f:,.0f} L")
    with m2:
        val_f = df_fechados.iloc[:, 15].sum()
        st.metric("Total Investido", f"R$ {val_f:,.2f}")
    with m3:
        med_f = df_fechados.iloc[:, 14].mean()
        st.metric("Média de Preço", f"R$ {med_f:,.2f}")

    st.markdown("---")

    # --- SEÇÃO 2: DASHBOARD MÊS VIGENTE (Abril) ---
    st.subheader("🚀 Período Vigente: Abril")
    
    col_left, col_mid, col_right = st.columns([1, 1, 1])

    with col_left:
        st.markdown("**Distribuição por Veículo (Volume)**")
        # Coluna B (índice 1) para nomes, F (índice 5) para valores
        fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
        fig_pie.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_mid:
        st.markdown("**Volume por Pedido**")
        st.bar_chart(df_atual.iloc[:, 5])

    with col_right:
        st.markdown("**Preço Médio Atual**")
        media_a = df_atual.iloc[:, 14].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = media_a,
            number = {'prefix': "R$ ", 'valueformat': ".2f"},
            gauge = {
                'axis': {'range': [0, 10]},
                'bar': {'color': "#f9a825"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgray"},
                    {'range': [5, 10], 'color': "gray"}
                ]
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(t=30, b=0, l=10, r=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Tabela detalhada oculta
    with st.expander("Visualizar dados brutos do mês atual"):
        st.dataframe(df_atual)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.info("💡 Verifique se renomeou a aba para ODM_MARCO e se o link tem permissão de leitura.")
