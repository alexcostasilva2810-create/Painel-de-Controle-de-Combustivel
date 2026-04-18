import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide", page_title="Painel ODM - Combustível", page_icon="⛽")

# --- LINK DA PLANILHA ---
# Certifique-se de que o link abaixo é o da sua planilha e que ela está "Aberta para qualquer pessoa com o link"
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1izHisQGFCLdqQ7d2OSGkAM7gDJrlsLxW9FY741lJ_Ao/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    # Criando a conexão
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo os dados. DICA: Se "ODM_MARCO" ainda der erro, tente ler sem o nome da aba primeiro
    df = conn.read(spreadsheet=URL_PLANILHA, worksheet="ODM_MARCO", ttl=0)
    
    # --- LIMPEZA DE COLUNAS ---
    # F=5, P=15, O=14, I=8
    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14], errors='coerce').fillna(0)
    
    # --- FILTROS ---
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]

    # --- MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Volume Acumulado (Fev/Mar)", f"{df_fechados.iloc[:, 5].sum():,.0f} L")
    m2.metric("Total Investido", f"R$ {df_fechados.iloc[:, 15].sum():,.2f}")
    m3.metric("Média Preço", f"R$ {df_fechados.iloc[:, 14].mean():,.2f}")

    st.markdown("---")
    st.subheader("🚀 Acompanhamento Abril")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        st.bar_chart(df_atual.iloc[:, 5])
    with c3:
        media_a = df_atual.iloc[:, 14].mean()
        fig_gauge = go.Figure(go.Indicator(mode="gauge+number", value=media_a, number={'prefix': "R$ "}))
        st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erro Crítico: {e}")
    st.info("Acesse sua planilha -> Compartilhar -> Mudar para 'Qualquer pessoa com o link' -> Concluído.")
