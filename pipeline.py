import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from extract import extract_all_activities
from transform import transform
from load import upload_to_bronze, upload_to_silver

def run_pipeline():
    print("=== Pipeline started ===\n")
    
    print("Step 1: extracting...")
    extract_all_activities()

    print("\nStep 2: transforming...")
    transform()

    print("\nStep 3: loading to Azure...")
    upload_to_bronze()
    upload_to_silver()

    print("\n === Pipeline completed ===")

if __name__ == "__main__":
    run_pipeline()
