
import pandas as pd
import argparse
import requests
from sqlalchemy import create_engine
from time import time
from pathlib import Path


def get_data_in_csv(url):
    table_name = Path(url).stem
    data_source_extension = Path(url).suffix
    data_parquet = f'{table_name}.parquet'
    data_csv = f"{table_name}.csv"

    if data_source_extension == ".parquet":
        r = requests.get(url, allow_redirects=True)
        open(data_parquet, 'wb').write(r.content)
        pd.read_parquet(data_parquet).to_csv(data_csv)
    else:
        r = requests.get(url, allow_redirects=True)
        open(data_csv, 'wb').write(r.content)
    
    return table_name, data_csv

def main(args):
    user = args.user
    password = args.password
    host = args.host
    port = args.port
    db = args.db
    data_source_url = str(args.data_source_url).split(',')

    for url in data_source_url:
        table_name, data_csv = get_data_in_csv(url)

        df = pd.read_csv(data_csv)

        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        engine.connect()

        # Prints the schema
        # print(pd.io.sql.get_schema(df, name="ny_taxi_data", con=engine))

        # Change data type from TEXT to DATETIME
        try:
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        except:
            print("Ignore tpep column error")

        # Create the DB table 
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

        # Upload data 100k at a time
        df_iter = pd.read_csv(data_csv, iterator=True, chunksize=100000)

        while True:
            t_start = time()
            
            try:
                df = next(df_iter)
            except:
                print("No more rows to append")
                break

            try:
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            except:
                print("Ignore tpep column error in while loop")
            
            df.to_sql(name=table_name, con=engine, if_exists='append')
            
            t_end = time()
            print("Insert successful. Took %.3f second(s)" % (t_end - t_start))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--db')
    parser.add_argument('--table_name')
    parser.add_argument('--data_source_url')

    args = parser.parse_args()

    main(args)