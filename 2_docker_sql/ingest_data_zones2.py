import os
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name_1 = params.table_name_1
    table_name_2 = params.table_name_2
    url_1 = params.url_1
    url_2 = params.url_2
    
    csv_name_1 = 'output.csv'
    csv_name_2 = 'output2.csv'

    os.system(f"wget {url_1} -O {csv_name_1}")
    os.system(f"wget {url_2} -O {csv_name_2}")


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter_1 = pd.read_csv(csv_name_1, iterator=True, chunksize=100000)
    df_iter_2 = pd.read_csv(csv_name_2, iterator=True, chunksize=100000)

    df_1 = next(df_iter_1)
    df_2 = next(df_iter_2)

    df_1.tpep_pickup_datetime = pd.to_datetime(df_1.tpep_pickup_datetime)
    df_1.tpep_dropoff_datetime = pd.to_datetime(df_1.tpep_dropoff_datetime)

    df_1.head(n=0).to_sql(name=table_name_1, con=engine, if_exists='replace')
    df_2.head(n=0).to_sql(name=table_name_2, con=engine, if_exists='replace')

    df_1.to_sql(name=table_name_1, con=engine, if_exists='append')
    df_2.to_sql(name=table_name_2, con=engine, if_exists='append')


    while True: 
        t_start = time()

        df_1 = next(df_iter_1)
        df_2 = next(df_iter_2)

        df_1.tpep_pickup_datetime = pd.to_datetime(df_1.tpep_pickup_datetime)
        df_1.tpep_dropoff_datetime = pd.to_datetime(df_1.tpep_dropoff_datetime)

        df_1.to_sql(name=table_name_1, con=engine, if_exists='append')
        df_2.to_sql(name=table_name_2, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name_1', required=True, help='name of the table1 where we will write the results to')
    parser.add_argument('--table_name_2', required=True, help='name of the table2 where we will write the results to')
    parser.add_argument('--url_1', required=True, help='url_1 of the csv file')
    parser.add_argument('--url_2', required=True, help='url_2 of the csv file')

    args = parser.parse_args()

    main(args)