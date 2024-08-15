import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Conexão com o banco de dados supabase
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

csvs = os.listdir('data')

for csv in csvs:
    # Carregar o CSV
    df = pd.read_csv(f'data/{csv}', delimiter=';')

    # Tratar valores nulos
    df['estado'].fillna('br', inplace=True)
    df.fillna(0, inplace=True)

    # Listas para armazenar os dados que serão inseridos
    dim_tempo_data = []
    dim_localidade_data = []
    fato_covid19_data = []

    for index, row in df.iterrows():
        print(index)
        # Dados para Dim_Tempo
        dim_tempo_data.append((row['data'], row['data'][:4], row['data'][5:7], row['data'][8:10], row['semanaEpi']))

        # Dados para Dim_Localidade
        dim_localidade_data.append((row['regiao'], row['estado'], row['municipio'], row['coduf'], row['codmun'], row['populacaoTCU2019']))

    # Inserir os dados nas tabelas de dimensão usando executemany
    cur.executemany("""
        INSERT INTO dim_tempo (data, ano, mes, dia, semanaepi)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (data) DO NOTHING;
    """, dim_tempo_data)

    cur.executemany("""
        INSERT INTO dim_localidade (regiao, estado, municipio, coduf, codmun, populacao)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (regiao, estado, municipio) DO NOTHING;
    """, dim_localidade_data)

    # Obter os IDs das tabelas de dimensão para usar na tabela fato
    for index, row in df.iterrows():
        cur.execute("SELECT data_id FROM dim_tempo WHERE data = %s", (row['data'],))
        data_id = cur.fetchone()[0]

        cur.execute("""
            SELECT localidade_id FROM dim_localidade 
            WHERE regiao = %s AND estado = %s AND municipio = %s
        """, (row['regiao'], row['estado'], row['municipio']))
        localidade_id = cur.fetchone()[0]

        # Dados para fato_covid19
        fato_covid19_data.append((data_id, localidade_id, row['casosacumulado'], row['casosnovos'], row['obitosacumulado'], row['obitosnovos'], row['recuperadosnovos'], row['emacompanhamentonovos']))

    # Inserir os dados na tabela fato_covid19 usando executemany
    cur.executemany("""
        INSERT INTO fato_covid19 (data_id, localidade_id, casosacumulado, casosnovos, obitosacumulado, obitosnovos, recuperadosnovos, emacompanhamentonovos)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, fato_covid19_data)

    conn.commit()

# Commit e fechamento da conexão
conn.commit()
cur.close()
conn.close()
