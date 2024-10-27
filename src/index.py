#-*- coding:utf-8 -*-

import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt

st.markdown("""
<style>
    [data-testid=stApp], [data-testid=stApp] h1, [data-testid=stApp] h2 {

        color: black;
    }
    [data-testid=stSidebar], [data-testid=stSidebar] h1, [data-testid=stSidebar] h2 {
        background-color: #0597F2;
        color: #F2F2F2  ;
        text-align: justify;
    }
    
    hr{
        border-color: #3EB1F9;
    }
    [data-testid=stSidebar] a,[data-testid=stSidebar] p{
        color: #F2F2F2;
    }
    div[data-baseweb="select"] > div {
        background-color: #27A4F2;
        border: none;
        color: #F2F2F2;
    }
</style>
""", unsafe_allow_html=True)

#carregar dados
df = pd.read_csv("data/processed/dados_tratados.csv")

### Main
st.title('CORA Analytics')

st.sidebar.image("resources/logo-cora.png")
st.sidebar.write("## Submenu")
menu = st.sidebar.selectbox("Escolha uma opcao:",
["Visao Geral do Cliente", "Dados de Retencao", "Infraestrutura"])
st.sidebar.write("""
ECharts demos are extracted from https://echarts.apache.org/examples/en/index.html, by copying/formattting the 'option' json object into st_echarts. Definitely check the echarts example page, convert the JSON specs to Python Dicts and you should get a nice viz.

---
__Made by Delarry__
""")

if menu == "Visao Geral do Cliente":
    st.header("Visao Geral do Cliente")
    st.write("Aqui estao os dados gerais sobre os clientes.")

    st.bar_chart(df['Idade'].value_counts().sort_index(),color="#0597F2")
    st.bar_chart(df['Estado'].value_counts().sort_index(),color="#0597F2")

    fig, ax = plt.subplots()
    ax.pie(df['Genero'].value_counts(),colors=["#0597F2","#F59CA9","#FE9920"] ,labels=df['Genero'].value_counts().index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Garantir que o gráfico de pizza seja um círculo
    st.pyplot(fig)

    grouped_df = df.groupby(['Motivo da Rotatividade','Estado']).size().unstack().fillna(0)
    plt.figure(figsize=(16, 8))  # Aumentar o tamanho da figura
    sns.heatmap(grouped_df, cmap="YlGnBu", annot=True, fmt="g", linewidths=.5)
    plt.title("Mapa de Calor - Quantidade de Clientes por Estado e Motivo de Cancelamento")
    plt.xlabel("Estado")
    plt.ylabel("Motivo da Rotatividade")

    st.pyplot(plt)

elif menu == "Dados de Retencao":
    st.header("Dados de Retencao")
    st.write("Aqui estao os dados de retencao dos clientes.")

    st.scatter_chart(
        pd.DataFrame(df, columns=["Duracao da conta (em meses)", "Cobranca Mensal", "Plano de Dados Ilimitado"]),
        y="Cobranca Mensal", x="Duracao da conta (em meses)", color="Plano de Dados Ilimitado", size=25, height=350)




    plt.figure(figsize=(10, 6))
    df['Total_Minutos'] = df['Minutos Local'] + df['Minutos Internacional']
    df_grouped = df.groupby('Grupo').agg({
        'Minutos Local': 'sum',
        'Minutos Internacional': 'sum'
    }).reset_index()

    df_grouped_melted = pd.melt(df_grouped, id_vars='Grupo', value_vars=['Minutos Local', 'Minutos Internacional'],
                                var_name='Tipo de Minuto', value_name='Total Minutos')

    sns.barplot(x='Grupo', y='Total Minutos', hue='Tipo de Minuto', data=df_grouped_melted)
    plt.title('Comparacao de Minutos Locais e Internacionais por Grupo')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)

elif menu == "Infraestrutura":
    st.header("Infraestrutura")
    st.write("Aqui estao os dados sobre a infraestrutura.")










