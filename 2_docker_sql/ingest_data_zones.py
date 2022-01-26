#!/usr/bin/env python
# coding: utf-8

import os
import sys
import argparse

from time import time

import pandas as pd
from sqlalchemy import create_engine

def download_csv(url, filename):
    try:
        print(f'Downloading {filename}, if not exist')
        if os.path.isfile(filename):
            print (f"{filename} already exist")
        else:
            print ("Downloading ....")
            os.system(f"curl  {url} -# --output {filename}")
            print (f"Downloaded {filename}")
        
        print("\n----Printing the first 10 lines of {filename}----")
        os.system(f"head -10 {filename}")
        print("-------------------------------------------------")
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

def load_data(csv_name,user,password,host,port,db,table_name):
    print(f"Loading {csv_name} into table {table_name} - postgresql://{user}:{password}@{host}:{port}/{db}")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    numOfLines = int(os.popen(f'wc -l < {csv_name}').read()[:-1])
    if numOfLines > 100000:
        try: 
            df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
            df.to_sql(name=table_name, con=engine, if_exists='append')
            while True: 
                t_start = time()
                df = next(df_iter)
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
                df.to_sql(name=table_name, con=engine, if_exists='append')
                t_end = time()
                print('inserted another chunk, took %.3f second' % (t_end - t_start))
        except StopIteration as err:
                print('Batch Processing is Completed!!')
    else:
        try: 
            df =pd.read_csv(csv_name)
            df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
            df.to_sql(name=table_name, con=engine, if_exists='append')
            print('Finished inserting zones to database')
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    trip_url = params.trip_url
    zone_url = params.zone_url
    try:
        download_csv(trip_url,'trips.csv')
        load_data('trips.csv',user,password,host,port,db,'trips')
        download_csv(zone_url,'zones.csv')
        load_data('zones.csv',user,password,host,port,db,'zones')
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--trip_url', help='trip url of the csv file')
    parser.add_argument('--zone_url', help='zone url of the csv file')
    args = parser.parse_args()

    main(args)