# COVID-19 Dashboard

Este projeto utiliza dados de COVID-19 para criar um dashboard interativo utilizando Power BI. Os dados são armazenados em um banco de dados PostgreSQL hospedado no Supabase, e o ETL é feito em Python para a ingestão dos dados.

## Visão Geral

O objetivo deste projeto é demonstrar a capacidade de extrair, transformar e carregar dados (ETL) para um banco de dados, e em seguida, visualizar esses dados em um dashboard interativo. O dashboard fornece insights sobre a evolução da pandemia de COVID-19 com base em dados públicos.

## Links Importantes

- **Dashboard Power BI:** [Visualizar Dashboard](https://app.powerbi.com/view?r=eyJrIjoiZTVkNzhhMjgtZDg1YS00MjE5LWE4MWQtZjE2MTRmZjk1YmRlIiwidCI6ImUxN2Q3ZWFlLTQwZGMtNDQ4ZC1hN2VhLTFhOGZhZDk0NDIxMSJ9)
- **Repositório GitHub:** [covid19-dash](https://github.com/carlosandradeds/covid19-dash)

## Requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

- Python 3.8+
- PostgreSQL
- Docker (opcional, para rodar o PostgreSQL localmente)
- Supabase CLI (opcional, se optar por usar o Supabase para hospedar o banco de dados)

## Configuração do Banco de Dados

### Usando Supabase

1. Crie uma conta no [Supabase](https://supabase.io/).
2. Crie um novo projeto e anote as credenciais do banco de dados (host, porta, nome do banco, usuário e senha).
3. Conecte-se ao banco de dados usando uma ferramenta como `pgAdmin` ou `psql` com as credenciais fornecidas.
4. Excute o script create_db.py

### Usando Docker (Banco Local)

1. Clone este repositório:

   ```bash
   git clone https://github.com/carlosandradeds/covid19-dash.git
   cd covid19-dash

2. Suba um container Docker com PostgreSQL:
    
    ```bash
    docker-compose up -d

3. Execute o script python create_db.py
    ```bash
    python create_db.py


3. Execute o script python etl.py
    ```bash
    python etl.py


### Visualização dos Dados
Após a inserção dos dados, você pode visualizar os resultados acessando o dashboard no Power BI através do link fornecido acima.



