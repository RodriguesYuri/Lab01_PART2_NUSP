import os
import sys
import time
from zipfile import ZipFile
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from logger_config import get_logger

os.environ['KAGGLE_CONFIG_DIR'] = str(Path(__file__).resolve().parent.parent.parent)

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except ImportError:
    print("ERROR: 'kaggle' library not found. Please install it using 'uv pip install kaggle'")
    sys.exit(1)

def main():
    logger = get_logger('EXTRACT')
    
    start_time = time.time()
    
    dataset_id = 'microize/newyork-yellow-taxi-trip-data-2020-2019'
    download_path = Path('data_source')
    extract_to_path = Path('data_lake/bronze')
    
    files_to_extract = ['yellow_tripdata_2019-03.csv', 'taxi+_zone_lookup.csv']

    try:
        logger.info('Starting cloud ingestion from Kaggle...')
        
        api = KaggleApi()
        api.authenticate()
        logger.info('Successfully authenticated with Kaggle API.')

        download_path.mkdir(parents=True, exist_ok=True)
        logger.info(f'Downloading dataset {dataset_id} (this may take a while)...')
        
        api.dataset_download_files(dataset_id, path=str(download_path), unzip=False)
        logger.info('Download completed.')

        zip_file_name = dataset_id.split('/')[-1] + '.zip'
        zip_file_path = download_path / zip_file_name

        extract_to_path.mkdir(parents=True, exist_ok=True)
        logger.info('Extracting specific files to Bronze layer...')
        
        with ZipFile(zip_file_path, 'r') as zip_ref:
            available_files = zip_ref.namelist()
            
            for file in files_to_extract:
                target_file = extract_to_path / file
                
                if target_file.exists():
                    logger.warning(f'{file} already exists in Bronze layer. Skipping extraction.')
                elif file in available_files:
                    zip_ref.extract(file, extract_to_path)
                    logger.info(f'Extracted: {file}')
                else:
                    logger.error(f'File {file} not found inside the downloaded Kaggle zip!')

        end_time = time.time()
        logger.info(f'Ingestion completed successfully in {end_time - start_time:.2f} seconds.')

    except Exception as e:
        logger.error(f'Ingestion failed: {str(e)}')
        sys.exit(1)

if __name__ == '__main__':
    main()