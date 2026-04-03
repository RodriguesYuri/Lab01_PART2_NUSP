import os
import sys
import pandas as pd
import psycopg2
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger_config import get_logger

def main():
    logger = get_logger('LOAD_FACT')
    
    try:
        logger.info("Reading tripdata.parquet from Silver layer...")
        tripdata = pd.read_parquet('data_lake/silver/tripdata.parquet')

        logger.info("Formatting columns for fact_trips...")
        tripdata = tripdata[[
            'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
            'trip_distance', 'fare_amount', 'total_amount', 'pulocationid',
            'dolocationid', 'payment_type'
        ]]

        tripdata.columns = [
            'pickup_datetime', 'dropoff_datetime', 'passenger_count',
            'trip_distance', 'fare_amount', 'total_amount', 'pulocationid',
            'dolocationid', 'payment_type'
        ]

        logger.info("Creating temporary CSV for bulk insert...")
        csv_path = 'tripdata_temp.csv'
        tripdata.to_csv(csv_path, index=False)

        logger.info("Connecting to PostgreSQL database...")
        conn = psycopg2.connect(
            host='db',
            database='nyc_taxi_db',
            user='user_lab',
            password='password_lab',
            port='5432'
        )
        cursor = conn.cursor()

        logger.info("Executing COPY command for ultra-fast ingestion...")
        with open(csv_path, 'r') as f:
            cursor.copy_expert("""
                COPY fact_trips(
                    pickup_datetime, dropoff_datetime, passenger_count,
                    trip_distance, fare_amount, total_amount,
                    pulocationid, dolocationid, payment_type
                ) FROM STDIN WITH CSV HEADER
            """, f)

        conn.commit()
        cursor.close()
        conn.close()
        
        # Boa prática: apagar o arquivo temporário após o uso
        if os.path.exists(csv_path):
            os.remove(csv_path)

        logger.info("fact_trips uploaded successfully!")

    except Exception as e:
        logger.error(f"Failed to load fact_trips: {repr(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()