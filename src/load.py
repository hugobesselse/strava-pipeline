import os
import json
from pathlib import Path
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SILVER_CONTAINER = "silver"
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Bronze container is the landing zone for raw data.
BRONZE_CONTAINER = "bronze"

def upload_to_bronze(filename="activities.json"):
    local_file = RAW_DATA_PATH / filename

    if not local_file.exists():
        print("No file found:{local_file}")
        return
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(
        container=BRONZE_CONTAINER,
        blob=filename
    )

    with open(local_file,"rb") as f:
        blob_client.upload_blob(f,overwrite=True)

        print(f"Uploaded:{filename} → Azure bronze container")

def upload_to_silver(filename="activities.parquet"):
    local_file = PROCESSED_DATA_PATH / filename
    if not local_file.exists():
        print(f"File not found:{local_file}")
        return
    
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(
        container=SILVER_CONTAINER,
        blob=filename
    )

    with open (local_file,"rb") as f:
        blob_client.upload_blob(f,overwrite=True)
    
    print(f"Uploaded {filename} to Azure silver container")

if __name__ == "__main__":
    print("Upload started...")
    upload_to_bronze()
    upload_to_silver()

    
  
