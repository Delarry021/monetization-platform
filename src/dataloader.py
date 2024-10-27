import pandas as pd

# Carregue o dataframe
df = pd.read_csv("../data/processed/dados_traduzidos.csv",encoding='utf-8')

df.drop(['Número de Telefone'], axis=1, inplace=True)
df.drop(['ID Cliente'], axis=1, inplace=True)

df.to_csv('dados_tratados.csv', index=False)