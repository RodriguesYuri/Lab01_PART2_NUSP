import psycopg2
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger_config import get_logger

logger = get_logger('SCHEMA')

def create_schema():
    try:
        logger.info("Connecting to the database...")
        conn = psycopg2.connect(
            host='db',
            database='nyc_taxi_db',
            user='user_lab',
            password='password_lab',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()

        sql_commands = """
        -- 1. Create Dimension Table (Locations)
        CREATE TABLE IF NOT EXISTS dim_location (
            locationid INT PRIMARY KEY,
            borough VARCHAR(255),
            zone VARCHAR(255),
            service_zone VARCHAR(255)
        );

        -- 2. Create Fact Table (Trips)
        CREATE TABLE IF NOT EXISTS fact_trips (
            trip_id SERIAL PRIMARY KEY,
            pickup_datetime TIMESTAMP,
            dropoff_datetime TIMESTAMP,
            passenger_count FLOAT,
            trip_distance FLOAT,
            pulocationid INT,
            dolocationid INT,
            fare_amount FLOAT,
            total_amount FLOAT,
            payment_type INT,
            vendorid INT
        );
        """

        logger.info("Executing table creation in the database...")
        cursor.execute(sql_commands)
        
        logger.info("Schema created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        raise e
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_schema()