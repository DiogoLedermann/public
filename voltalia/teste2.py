import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('voltalia/PLDh_2021.xlsx', sheet_name='Sheet1', index_col='Hora')
df = df.loc[df['Submercado'] == 'NORDESTE']

new_df = pd.DataFrame()

for i in range(12):
    cols = [col for col in df.columns if f'/{i+1:02}/' in col]

    new_df[f'mean{i+1:02}'] = df[cols].mean(axis=1)

data = new_df.to_numpy()
data = data.transpose()

for i, prices in enumerate(data):
    plt.figure()
    plt.grid()
    plt.title(f'Perfil do PLD horário (Mês {i+1})')
    plt.xlabel('Hora')
    plt.ylabel('PLD - R$/MWh')
    plt.plot([j for j in range(24)], prices)
    plt.savefig(f'voltaliaImgs/Perfil do PLD horário (Mês {i+1})t.png')
