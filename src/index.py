# -*- coding:utf-8 -*-

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Configurações de estilo e cores
BACKGROUND_COLOR = "#092536"
PRIMARY_COLOR = "#FFC65E"
TEXT_COLOR = "#FFFFFF"

# Configurações gerais do Streamlit
st.set_page_config(layout='wide', page_title='Dashboard')
st.markdown(f"""
<style>
    /* Sidebar */
    .stSidebar {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
    }}
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6, .stSidebar p {{
        color: {TEXT_COLOR};
    }}
    /* Inputs e botões */
    .stTextInput, .stSelectbox, .stButton > button, .stTextArea {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_COLOR};
        border-color: {PRIMARY_COLOR};
    }}
    /* Links */
    a, a:visited, a:hover {{
        color: {PRIMARY_COLOR};
    }}
    /* Personalização de botões */
    button, .stButton > button:hover {{
        background-color: {PRIMARY_COLOR};
        color: {BACKGROUND_COLOR};
        border: none;
    }}
    /* Alerta e mensagens */
    .stAlert {{
        background-color: {BACKGROUND_COLOR};
        border-left: 5px solid {PRIMARY_COLOR};
    }}
</style>
""", unsafe_allow_html=True)

# Carregar dados
df = pd.read_csv("data/processed/dados_tratados.csv")

# Sidebar
st.sidebar.image("resources/logo-cora.png")
st.sidebar.write("## Navegação")
menu = st.sidebar.selectbox("Selecione a seção desejada:",
                            ["Análise Geral dos Clientes", "Indicadores de Retenção", "Infraestrutura"])
st.sidebar.write("""
Explore os dados detalhados sobre nossos clientes, retenção e infraestrutura de serviços de telecomunicações. 

---
__Desenvolvido por Guilherme Delarry__
""")

st.title('CORA Analytics')

# Processamentos comuns aos gráficos
df['Faixa_Etaria'] = pd.cut(df['Idade'], bins=[18, 30, 40, 50, 60, 70, 100],
                            labels=['18-30', '30-40', '40-50', '50-60', '60-70', '70+'])

# Menu Análise Geral dos Clientes
if menu == "Análise Geral dos Clientes":
    st.header("Visao Geral do Cliente")
    st.write("Uma visão ampla sobre o perfil e comportamento dos clientes da CORA.")
    st.divider()

    qnt_cli, qnt_estados, med_idade = st.columns(3)
    qnt_cli.metric(label="Quantidade de clientes", value=df.shape[0], delta="-3 Atualizado Hoje")
    qnt_estados.metric(label="Estados Abrangidos", value=df.Estado.nunique(), delta="0 Atualizado Hoje")
    med_idade.metric(label="Média de Idade", value=f"{round(df.Idade.mean())} Anos", delta="+0.3 Atualizado Hoje")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Quantidade de clientes por Idade")
        st.bar_chart(df['Idade'].value_counts().sort_index(), height=250, color="#0597F2", use_container_width=True)
    with col2:
        st.subheader("Quantidade de clientes por Estado")
        st.bar_chart(df['Estado'].value_counts().sort_index(), height=250, color="#0597F2", use_container_width=True)

    col3, col4 = st.columns([2, 1])
    with col3:
        st.subheader("Média de GB de Download por Faixa Etária")
        media_gb_faixa_etaria = df.groupby('Faixa_Etaria')['Media mensal de GB para download'].mean()
        st.bar_chart(media_gb_faixa_etaria)
    with col4:
        st.subheader("Distribuição de Gênero")
        genero_count = df['Genero'].value_counts()
        fig = px.pie(genero_count, values=genero_count.values, names=genero_count.index, height=330)
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5))
        st.plotly_chart(fig)

# Menu Indicadores de Retenção
elif menu == "Indicadores de Retenção":
    st.header("Indicadores de Retenção")
    st.write("Análise detalhada sobre a retenção e rotatividade dos clientes.")
    st.divider()

    sim_count, nao_count = df['Etiqueta de rotatividade'].value_counts().get('Sim', 0), df['Etiqueta de rotatividade'].value_counts().get('Nao', 0)
    total_count = (sim_count / nao_count) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Taxa de Rotatividade", value=f"{round(total_count, 2)}%", delta="-8.32% Atualizado Hoje")
    col2.metric(label="Média de Chamadas Locais", value=f"{round(df['Chamadas locais'].mean(), 2)} Min", delta="+2.53 Atualizado Hoje")
    col3.metric(label="Média de Duração de Conta", value=f"{round(df['Duracao da conta (em meses)'].mean(), 2)} Meses", delta="+0.3 Atualizado Hoje")

    st.divider()

    col4, col5 = st.columns(2)
    with col4:
        st.subheader("Tipo de Contrato por Grupo de Clientes")
        fig1 = px.histogram(df, x='Tipo de Contrato', color='Grupo')
        st.plotly_chart(fig1)
        st.subheader("Duração da Conta x Cobrança Mensal")
        fig2 = px.scatter(df, x="Duracao da conta (em meses)", y="Cobranca Mensal", color="Plano de Dados Ilimitado")
        st.plotly_chart(fig2)
    with col5:
        st.subheader("Motivos de Cancelamento e Rotatividade")
        fig3 = px.histogram(df, y='Motivo da Rotatividade')
        st.plotly_chart(fig3)
        st.subheader("Motivos de Cancelamento por Estado")
        grouped_df = df.groupby(['Motivo da Rotatividade', 'Estado']).size().unstack().fillna(0)
        fig4 = go.Figure(data=go.Heatmap(z=grouped_df.values, x=grouped_df.columns, y=grouped_df.index, colorscale='YlGnBu'))
        st.plotly_chart(fig4)

# Menu Infraestrutura
elif menu == "Infraestrutura":
    st.header("Infraestrutura")
    st.write("Indicadores relacionados à infraestrutura e serviços oferecidos aos clientes.")
    st.divider()

    col1, col2 = st.columns(2)
    col1.metric(label="Média de Minutos Locais", value=f"{round(df['Minutos Local'].mean(), 2)} min", delta="+10.35 Atualizado Hoje")
    col2.metric(label="Média de Minutos Internacionais", value=f"{round(df['Minutos Internacional'].mean(), 2)} min", delta="+60.30 Atualizado Hoje")

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Chamadas de Atendimento ao Cliente por Idade")
        fig1 = px.scatter(df, x='Idade', y='Chamadas de atendimento ao cliente', color='Genero')
        st.plotly_chart(fig1)
        st.subheader("Tarifas Internacionais Extras por Estado")
        fig2 = px.bar(df, x='Estado', y='Tarifas internacionais extras', color='Estado')
        st.plotly_chart(fig2)
    with col4:
        st.subheader("Planos Internacionais por Grupo")
        fig3 = px.histogram(df, x='Plano internacional', color='Grupo', barmode='group')
        st.plotly_chart(fig3)
        st.subheader("Chamadas Internacionais por Estado")
        fig4 = px.bar(df, x='Estado', y='Chamadas internacionais', color='Estado')
        st.plotly_chart(fig4)
