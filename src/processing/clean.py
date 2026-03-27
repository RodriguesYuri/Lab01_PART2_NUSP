import pandas as pd
from loader import load_data
from profiling import get_info

def standarize_columns(df):
    std = df.copy()

    std.columns = (
        std.columns
        .str.strip()
        .str.lower()
        .str.replace('[^a-z0-9]+', '_', regex=True)
    )

    return std

def clean_data(df):
    clean_df = df.copy()
    
    clean_df = clean_df.dropna()
    clean_df = clean_df.drop_duplicates()

    return clean_df

def time_tipe(df):
    t_df = df.copy()

    t_df['tpep_pickup_datetime'] = pd.to_datetime(t_df['tpep_pickup_datetime'])
    t_df['tpep_dropoff_datetime'] = pd.to_datetime(t_df['tpep_dropoff_datetime'])

    return t_df

data = load_data()

std_dataframe = {
    f'std_{name.lower()}': standarize_columns(df)
    for name, df in data.items()
}

clean_dataframe = {
    f'clean_{name.replace("std_", "")}': clean_data(df)
    for name, df in std_dataframe.items()
}

clean_tripdata = time_tipe(clean_dataframe['clean_tripdata'])

clean_zone = clean_dataframe['clean_zone']