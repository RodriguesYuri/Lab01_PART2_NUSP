from pathlib import Path
from clean import clean_tripdata, clean_zone

def save_silver(df, name):
    silver_path = Path('data_lake/silver')
    silver_path.mkdir(parents=True, exist_ok=True)

    file_path = silver_path / f'{name}.parquet'
    df.to_parquet(file_path, index=False)

save_silver(clean_tripdata, 'tripdata')
save_silver(clean_zone, 'zone')