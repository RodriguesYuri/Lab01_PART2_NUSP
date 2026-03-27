import time as t
import logging
from logging.handlers import RotatingFileHandler
from zipfile import ZipFile
from pathlib import Path

log_path = Path('data_lake\logs')
log_path.mkdir(exist_ok=True)

log_file = log_path / 'ingest.log'

logger = logging.getLogger('ingestion')
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    log_file,
    maxBytes=5_000_000,
    backupCount=4
)
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

zip_file_path = Path('taxi.zip')
extract_to_path = Path('data_lake/bronze')
files_to_extract = ['yellow_tripdata_2019-03.csv', 'taxi+_zone_lookup.csv']

start = t.time()

try:
    logger.info('Starting ingestion')

    extract_to_path.mkdir(parents=True, exist_ok=True)

    for file in files_to_extract:
        target_file = extract_to_path / file
        if target_file.exists():
            logger.warning('%s already exists. Skipping ingestion', file)
        else:
            with ZipFile(zip_file_path, 'r') as taxi:
                logger.info('Extracting file: %s', file)
                taxi.extract(file, extract_to_path)
            if not target_file.exists():
                raise FileNotFoundError('File extraction failed')    

except Exception as e:
    logger.exception('Error during ingestion: %s', e)

finally:
    elapsed = t.time() - start
    logger.info('Total execution time: %.2fs', elapsed)