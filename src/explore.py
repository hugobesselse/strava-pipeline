import json
from pathlib import Path
from config import RAW_DATA_PATH

def explore_activities():
    with open (RAW_DATA_PATH / "activities.json","r") as f:
        data = json.load(f)

    print(f"Number of activities:{len(data)}")
    
    # Check datatypes by looking at first activity. 
    # Check: datatype of "id" (unique identifier)
    # Check: datatype of date fields (str) - will be updated in transform.py
    # Check: datatype of speed related fields should be float
    # Check: datatype of duration related fields should be int
    print(f"\nDatatypes first activity:")
    for key, value in data[0].items():
        print(f" {key}: {type(value).__name__} → {value}")
    
if __name__ == "__main__":
    explore_activities()
