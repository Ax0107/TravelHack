import pandas as pd
import numpy as np

df = pd.read_excel('data.xlsx')

clients_df = pd.read_excel('clients_df.xlsx')
clients_df.index = clients_df['Unnamed: 0']
clients_df = clients_df.drop(['Unnamed: 0'], axis=1)[1:]
dropped_indexes = clients_df[clients_df['Сумма в $'] == np.inf].index
clients_df2 = clients_df.drop(dropped_indexes)
df_countries = pd.DataFrame(index=['country'], columns=clients_df2.columns)

for country in df['Страна тура'].unique():
    client_ids = df[df['Страна тура'] == country]['ИД клиента']
    client_ids = [i for i in client_ids if i not in dropped_indexes]
    mean_for_country = clients_df2.loc[client_ids].mean()
    df_countries.loc[country] = mean_for_country


def get_info_for_user(user_id, iloc=False):
    if iloc:
        data = clients_df.iloc[user_id]
    else:
        data = clients_df.loc[user_id]
    data = data.drop(data[data == 0.0].index)
    print(data)
    return data


sim_ab = {}
vcols = ['Глубина продаж',
         'Ночей', 'Сумма в $', 'Звездность', 'Планирование поездки']


def predict_for_user(user_id, iloc=False, n='all'):
    print('Информация о клиенте: -------\n')
    info = get_info_for_user(user_id, iloc=iloc)
    print('\n-----------------------------')
    if iloc:
        A = clients_df2.iloc[user_id][vcols].values
    else:
        A = clients_df2.loc[user_id][vcols].values
    for i in range(df_countries.shape[0]):
        B = df_countries.iloc[i][vcols].values
        sim_ab[i] = np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B))

    sims = pd.DataFrame([sim_ab])
    sorted_args = np.nan_to_num(sims.values).argsort()[0][::-1]

    submit = [df_countries.iloc[i].name for i in sorted_args]
    if n != 'all':
        submit = submit[:n]
    print('Направления к рекомендации:\n*', '\n* '.join(submit))
    return {'info': info, 'submit': submit}

