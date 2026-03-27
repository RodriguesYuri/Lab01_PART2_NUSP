import matplotlib.pyplot as plt
from pathlib import Path
from clean import clean_tripdata

def generate_plots(df):
    plot_path = Path('data_lake/silver/plots')
    plot_path.mkdir(exist_ok = True)

    print(plot_path.resolve())

    # 1. Fare distribution (Box Plot)
    plt.figure()
    filtered = df[df['fare_amount'] < df['fare_amount'].quantile(0.99)]
    plt.boxplot(filtered['fare_amount'], vert=False)
    plt.title('Fare Amount Boxplot (until 99º percentil)')
    plt.savefig(plot_path / 'fare_boxplot.png')
    plt.close()

    # 2. Distance distribution (Histogram)
    plt.figure()
    df['trip_distance'].hist(bins=50)
    plt.title('Trip Distance Distribution')
    plt.savefig(plot_path / 'distance.png')
    plt.close()

    # 3. Trips by hour (Bar)
    plt.figure()
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    df['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title('Trips by Hour')
    plt.savefig(plot_path / 'hour.png')
    plt.close()

    # 4. Distance vs fare (scatter)
    plt.figure()
    plt.scatter(df['trip_distance'], df['fare_amount'], alpha=0.1)
    plt.title('Distance vs Fare')
    plt.savefig(plot_path / 'scatter.png')
    plt.close()

    # 5. Top zones
    plt.figure()
    df['pulocationid'].value_counts().head(10).plot(kind='barh')
    plt.title('Top Pickup Locations')
    plt.savefig(plot_path / 'zones.png')
    plt.close()

generate_plots(clean_tripdata)