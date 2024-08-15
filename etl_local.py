import pandas as pd
from sqlalchemy import create_engine

# Configuração da conexão com o banco de dados usando SQLAlchemy
engine = create_engine('postgresql+psycopg2://coviduser:covidpass@localhost:5432/postgres')

# Caminhos dos arquivos CSV
dim_localidade_csv = 'csv/dim_localidade_202408141545.csv'
dim_tempo_csv = 'csv/dim_tempo_202408141545.csv'
fato_covid19_csv = 'csv/fato_covid19_202408141544.csv'

# Definir o tamanho do chunk
chunksize = 50000  # número de linhas por chunk

# Função para inserir dados em chunks
def insert_data_in_chunks(csv_file, table_name):
    for chunk in pd.read_csv(csv_file, delimiter=',', chunksize=chunksize):
        chunk.to_sql(table_name, engine, if_exists='append', index=False, method='multi')
        print(f"{len(chunk)} registros inseridos em {table_name}")

# Inserir os dados em chunks
insert_data_in_chunks(dim_tempo_csv, 'dim_tempo')
insert_data_in_chunks(dim_localidade_csv, 'dim_localidade')
insert_data_in_chunks(fato_covid19_csv, 'fato_covid19')

print("Todos os dados foram inseridos com sucesso!")
