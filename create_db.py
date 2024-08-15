import psycopg2
import os
from dotenv import load_dotenv

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Conexão com o banco de dados usando variáveis de ambiente
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
cur = conn.cursor()

# Criação das tabelas
cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_tempo (
        data_id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        ano INT,
        mes INT,
        dia INT,
        semanaepi INT,
        CONSTRAINT unique_data UNIQUE (data)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS dim_localidade (
        localidade_id SERIAL PRIMARY KEY,
        regiao VARCHAR(50),
        estado VARCHAR(10),
        municipio VARCHAR(100),
        coduf INT,
        codmun INT,
        populacao INT,
        CONSTRAINT unique_localidade UNIQUE (regiao, estado, municipio)
    );
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS fato_covid19 (
        fato_id SERIAL PRIMARY KEY,
        data_id INT REFERENCES dim_tempo(data_id),
        localidade_id INT REFERENCES dim_localidade(localidade_id),
        casosacumulado INT,
        casosnovos INT,
        obitosacumulado INT,
        obitosnovos INT,
        recuperadosnovos INT,
        emacompanhamentonovos INT
    );
""")

conn.commit()
cur.close()
conn.close()
