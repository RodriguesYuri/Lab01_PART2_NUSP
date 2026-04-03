import subprocess
import sys

def run_script(script_path):
    """Helper function to run a script and check for errors."""
    print(f"--- Starting: {script_path} ---")
    
    # Executes the script using the current Python interpreter
    result = subprocess.run([sys.executable, script_path])
    
    # returncode 0 means success. Anything else is an error.
    if result.returncode != 0:
        print(f"CRITICAL ERROR: Script {script_path} failed. Halting pipeline.")
        sys.exit(1) # Stops execution
        
    print(f"SUCCESS: {script_path} finished!\n")


if __name__ == "__main__":
    print("=== STARTING END-TO-END DATA PIPELINE ===\n")
    
    # STEP 1: Extraction (Bronze Layer)
    run_script("src/extract/extract_bronze.py") 
    
    # STEP 2: Processing and Parquet (Silver Layer)
    run_script("src/transform/transform_silver.py") 
    
    # STEP 3: Database Load (Gold Layer)
    run_script("src/load/load_dim_location.py")
    run_script("src/load/load_fact_trips.py")
    
    print("=== PIPELINE COMPLETED SUCCESSFULLY ===")