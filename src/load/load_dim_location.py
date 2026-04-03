import sys
import pandas as pd
import psycopg2
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger_config import get_logger

def main():
    logger = get_logger('LOAD_DIM')
    
    try:
        logger.info("Reading zone.parquet from Silver layer...")
        zone = pd.read_parquet('data_lake/silver/zone.parquet')

        logger.info("Connecting to PostgreSQL database...")
        # Lembrete: 'host' agora é 'db' para funcionar no Docker!
        conn = psycopg2.connect(
            host='db',
            database='nyc_taxi_db',
            user='user_lab',
            password='password_lab',
            port='5432'
        )
        cursor = conn.cursor()

        logger.info(f"Inserting {len(zone)} records into dim_location...")
        for _, row in zone.iterrows():
            cursor.execute("""
                INSERT INTO dim_location (locationid, borough, zone, service_zone)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (locationid) DO NOTHING
            """, tuple(row))

        conn.commit()
        cursor.close()
        conn.close()

        logger.info("dim_location uploaded successfully!")

    except Exception as e:
        logger.error(f"Failed to load dim_location: {repr(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()