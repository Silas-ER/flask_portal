from datetime import datetime
import pandas as pd
import os

def aniversariantes():
    hoje = datetime.now()
    mes_atual = hoje.month

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    ARQUIVO_CSV = os.path.join(BASE_DIR, '..', 'static', 'archives', 'aniversariantes.csv')

    df = pd.read_csv(ARQUIVO_CSV, sep=';')

    # Converte colunas para o tipo correto
    df['Dia'] = pd.to_numeric(df['Dia'], errors='coerce')
    df['Mes'] = pd.to_numeric(df['Mes'], errors='coerce')

    # Remove linhas com valores ausentes (NaN) em 'Dia' ou 'Mes'
    df.dropna(subset=['Dia', 'Mes'], inplace=True)

    # Filtra os aniversariantes do mês
    aniversariantes_mes = df[df['Mes'] == mes_atual]

    # Ordena por dia do mês (opcional)
    aniversariantes_mes = aniversariantes_mes.sort_values('Dia')

    # Cria a lista de aniversariantes
    lista_aniversariantes = []
    for _, row in aniversariantes_mes.iterrows():
        lista_aniversariantes.append({
            'Dia': int(row['Dia']),
            'Nome': row['Nome'],
        })

    return lista_aniversariantes
