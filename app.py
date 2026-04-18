import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_gsheets import GSheetsConnection

st.set_page_config(layout="wide", page_title="Painel ODM - Combustível", page_icon="⛽")

# --- LINK DA PLANILHA ---
# Use o link que você copiou do botão "Copiar link" da sua última imagem
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1izHisQGFCLdqQ7d2OSGkAM7gDJrlsLxW9FY741lJ_Ao/edit?usp=sharing"

st.title("⛽ Painel de Operações de Combustível")

try:
    # Criando a conexão
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Lendo os dados. 
    # Tentei manter o nome "ODM_MARCO". 
    # IMPORTANTE: Verifique se na sua planilha o nome da aba está exatamente ODM_MARCO
    df = conn.read(spreadsheet=URL_PLANILHA, worksheet="ODM_MARCO", ttl=0)
    
    # Se chegamos aqui, a conexão funcionou!
    st.success("✅ Dados carregados com sucesso!")

    # --- TRATAMENTO DE DADOS (Índices: F=5, P=15, O=14, I=8) ---
    df.iloc[:, 5] = pd.to_numeric(df.iloc[:, 5], errors='coerce').fillna(0)
    df.iloc[:, 15] = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0)
    df.iloc[:, 14] = pd.to_numeric(df.iloc[:, 14], errors='coerce').fillna(0)
    
    # Filtros baseados na Coluna I (índice 8)
    # Supondo que na coluna I o mês apareça como "02", "03", "04"
    df_fechados = df[df.iloc[:, 8].astype(str).str.contains("02|03", na=False)]
    df_atual = df[df.iloc[:, 8].astype(str).str.contains("04", na=False)]

    # --- MÉTRICAS CONSOLIDADAS ---
    st.header("📊 Meses Fechados (Consolidado)")
    m1, m2, m3 = st.columns(3)
    m1.metric("Volume Total", f"{df_fechados.iloc[:, 5].sum():,.0f} L")
    m2.metric("Valor Total", f"R$ {df_fechados.iloc[:, 15].sum():,.2f}")
    m3.metric("Preço Médio", f"R$ {df_fechados.iloc[:, 14].mean():,.2f}")

    st.markdown("---")

    # --- DASHBOARD MÊS VIGENTE ---
    st.header("🚀 Período Vigente (Abril)")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.write("**Volume por Veículo**")
        fig_pie = px.pie(df_atual, values=df_atual.columns[5], names=df_atual.columns[1], hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with c2:
        st.write("**Volume por Pedido**")
        st.bar_chart(df_atual.iloc[:, 5])
        
    with c3:
        st.write("**Média de Preço**")
        media_a = df_atual.iloc[:, 14].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", 
            value=media_a, 
            number={'prefix': "R$ "},
            gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "#f9a825"}}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar: {e}")
    st.info("💡 DICA: Se o erro for 'Worksheet not found', verifique se o nome da aba no Google Sheets é exatamente ODM_MARCO")
