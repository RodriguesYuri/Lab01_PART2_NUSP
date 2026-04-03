import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from io import StringIO
from datetime import datetime

def load_data():
    base_path = Path('data_lake/bronze')

    return {
        'Tripdata' : pd.read_csv(base_path / 'yellow_tripdata_2019-03.csv', sep = ','),
        'Zone' : pd.read_csv(base_path / 'taxi+_zone_lookup.csv', sep = ',')
    }

def snake_case(df):
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

def generate_plots(df, df2):
    plot_path = Path('plots')
    plot_path.mkdir(exist_ok=True)
    
    plt.style.use('seaborn-v0_8-whitegrid')

    # 1. Fare distribution (Box Plot)
    plt.figure(figsize=(10, 4))
    filtered_fare = df[(df['fare_amount'] > 0) & (df['fare_amount'] < df['fare_amount'].quantile(0.99))]
    plt.boxplot(filtered_fare['fare_amount'], vert=False, patch_artist=True)
    plt.title('Fare Amount Boxplot (Positive values up to 99th percentile)')
    plt.xlabel('Fare Amount ($)')
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(plot_path / 'fare_boxplot.png')
    plt.close()

    # 2. Distance distribution (Histogram)
    plt.figure(figsize=(10, 5))
    filtered_dist = df[(df['trip_distance'] > 0) & (df['trip_distance'] <= 50)]
    filtered_dist['trip_distance'].hist(bins=50, color='steelblue', edgecolor='black')
    plt.title('Trip Distance Distribution (up to 50 miles)')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Number of Trips')
    plt.tight_layout()
    plt.savefig(plot_path / 'distance.png')
    plt.close()

    # 3. Trips by hour (Bar)
    plt.figure(figsize=(12, 5))
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    ax = df['hour'].value_counts().sort_index().plot(kind='bar', color='coral')
    plt.title('Trips by Hour of Day')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Trips')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(plot_path / 'hour.png')
    plt.close()

    # 4. Distance vs fare (scatter)
    plt.figure(figsize=(10, 6))
    scatter_df = df[(df['trip_distance'] > 0) & (df['trip_distance'] <= 50) & 
                    (df['fare_amount'] > 0) & (df['fare_amount'] <= 200)]
    plt.scatter(scatter_df['trip_distance'], scatter_df['fare_amount'], alpha=0.1, color='purple')
    plt.title('Distance vs Fare (Cleaned)')
    plt.xlabel('Distance (miles)')
    plt.ylabel('Fare Amount ($)')
    plt.tight_layout()
    plt.savefig(plot_path / 'scatter.png')
    plt.close()

    # 5. Top zones
    top_10 = df['pulocationid'].value_counts().head(10).reset_index()
    top_10.columns = ['pulocationid', 'trip_count'] 
    top_10_named = top_10.merge(df2, 
                                left_on='pulocationid', 
                                right_on='locationid', 
                                how='left')

    top_10_named = top_10_named.sort_values(by='trip_count', ascending=True)

    labels = top_10_named['borough'] + " - " + top_10_named['zone']

    plt.figure(figsize=(10, 6))
    
    plt.barh(labels, top_10_named['trip_count'], color='mediumseagreen')
    
    plt.title('Top 10 Pickup Locations (By Borough and Zone)')
    plt.xlabel('Number of Pickups')
    plt.ylabel('Location')

    plt.tight_layout()
    plt.savefig(plot_path / 'zones.png')
    plt.close()

def build_plot_markdown():
    report_path = Path('plots/plot_markdown.md')
    report_path.parent.mkdir(exist_ok=True)
        
    with open(report_path, 'w', encoding = 'utf-8') as f:
        f.write('# Data Visualization\n\n')

        f.write('## Fare Distribution\n')
        f.write('![fare](../plots/fare.png)\n\n')

        f.write('## Trip Distance\n')
        f.write('![distance](../plots/distance.png)\n\n')

        f.write('## Trips by Hour\n')
        f.write('![hour](../plots/hour.png)\n\n')

        f.write('## Distance vs Fare\n')
        f.write('![scatter](../plots/scatter.png)\n\n')

        f.write('## Top Pickup Locations\n')
        f.write('![zones](../plots/zones.png)\n\n')

def get_info(df):
    buffer = StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def get_nulls(df):
    return df.isnull().sum()

def get_describe(df):
    return df.describe(include='all')

def build_report(data, stage="unknown", base_path="reports"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_path = Path(base_path) / f"{stage}" / f"report_{timestamp}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f'# Report - {stage}\n\n')
        f.write(f'Generated at: {timestamp}\n\n')

        for name, df in data.items():
            f.write(f'## Dataset: {name}\n\n')

            f.write('### Info\n')
            f.write(f'{get_info(df)}\n\n')

            f.write('### Null Count\n')
            f.write(f'{get_nulls(df)}\n\n')

            f.write('### Describe\n')
            f.write(f'{get_describe(df)}\n\n')

    return report_path

def save_as_parquet(df, name):
    silver_path = Path('data_lake/silver')
    silver_path.mkdir(parents=True, exist_ok=True)

    file_path = silver_path / f'{name}.parquet'
    df.to_parquet(file_path, index=False)