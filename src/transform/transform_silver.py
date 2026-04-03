import sys
import utils as ut
import pandas as pd
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger_config import get_logger

def main():
    logger = get_logger('TRANSFORM')
    
    try:
        logger.info("Loading raw data from Bronze layer...")
        data = ut.load_data()
        
        logger.info("Generating pre-cleaning report...")
        ut.build_report(data, stage="pre_cleaning")
        
        logger.info("Cleaning and standardizing data...")
        std_dataframe = {f'std_{name.lower()}': ut.snake_case(df) for name, df in data.items()}
        clean_dataframe = {f'clean_{name.replace("std_", "")}': ut.clean_data(df) for name, df in std_dataframe.items()}
        
        clean_tripdata = clean_dataframe['clean_tripdata']
        clean_tripdata['tpep_pickup_datetime'] = pd.to_datetime(clean_tripdata['tpep_pickup_datetime'])
        clean_tripdata['tpep_dropoff_datetime'] = pd.to_datetime(clean_tripdata['tpep_dropoff_datetime'])
        clean_zone = clean_dataframe['clean_zone']
        
        logger.info("Generating post-cleaning report...")
        ut.build_report(clean_dataframe, stage="pos_cleaning")
        
        logger.info("Generating plots and markdown...")
        ut.generate_plots(clean_tripdata, clean_zone)
        ut.build_plot_markdown()
        
        logger.info("Saving processed data to Silver layer (Parquet)...")
        ut.save_as_parquet(clean_tripdata, 'tripdata')
        ut.save_as_parquet(clean_zone, 'zone')
        
        logger.info("Transformation layer completed successfully!")

    except Exception as e:
        logger.error(f"Transformation failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()