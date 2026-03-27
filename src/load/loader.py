import pandas as pd
from pathlib import Path

def load_data():
    base_path = Path('data_lake/bronze')

    return {
        'Tripdata' : pd.read_csv(base_path / 'yellow_tripdata_2019-03.csv', sep = ','),
        'Zone' : pd.read_csv(base_path / 'taxi+_zone_lookup.csv', sep = ',')
    }