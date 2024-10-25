import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# Carregue o dataframe
df = pd.read_csv("../data/raw/data.csv")

# Defina as colunas categóricas
colunas_categoricas = ['Gender', 'Intl Plan', 'Unlimited Data Plan',
                       'Device Protection & Online Backup', 'Contract Type',
                       'Payment Method', 'Churn Category', 'Churn Reason',
                       'State', 'Under 30', 'Senior']

# Defina as colunas numéricas
colunas_numericas = ['Account Length (in months)', 'Local Calls',
                     'Local Mins', 'Intl Calls', 'Intl Mins',
                     'Customer Service Calls', 'Avg Monthly GB Download',
                     'Extra International Charges', 'Extra Data Charges',
                     'Monthly Charge', 'Total Charges', 'Age']

# Aplique OneHotEncoder nas colunas categóricas
encoder = OneHotEncoder()
df_categorico = encoder.fit_transform(df[colunas_categoricas])

# Aplique MinMaxScaler nas colunas numéricas
scaler = MinMaxScaler()
df_numerico = scaler.fit_transform(df[colunas_numericas])

# Concatene os resultados
df_tratado = pd.concat([pd.DataFrame(df_categorico.toarray()), pd.DataFrame(df_numerico)], axis=1)

