import json
import pandas as pd
from pathlib import Path
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH

def load_raw_activities():
    # Load raw JSON from bronze layer.
    with open (RAW_DATA_PATH / "activities.json","r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def select_columns(df):
    # Select only columns of choice
    columns = [
        "id","name","type","sport_type","start_date_local","timezone",
        "distance","moving_time","elapsed_time","total_elevation_gain","average_speed",
        "max_speed","elev_high","elev_low","has_heartrate","pr_count","achievement_count",
        "kudos_count","commute","photo_count","visibility","total_photo_count","manual","athlete_count"
    ]
    return df[columns]

def transform_units(df):
    # Convert meters to kilometers
    df["distance_km"] = (df["distance"]/1000).round(2)
    # Convert seconds to minutes
    df["moving_time_min"] = (df["moving_time"]/60).round(1)
    df["elapsed_time_min"] = (df["elapsed_time"]/60).round(1)
    # Convert speed from m/s to km/h
    df["average_speed_kmh"] = (df["average_speed"]*3.6).round(2)
    df["max_speed_kmh"] = (df["max_speed"]*3.6).round(2)
    # Remove original columns
    df = df.drop(columns=["distance","moving_time","elapsed_time","average_speed","max_speed"])
    return df

def transform_dates(df):
    # Convert date column to separate parts for PowerBI
    df["start_date_local"] = pd.to_datetime(df["start_date_local"])
    df["year"] = df["start_date_local"].dt.year
    df["month"] = df["start_date_local"].dt.month
    df["month_name"] = df["start_date_local"].dt.strftime("%B")
    df["day"] = df["start_date_local"].dt.day
    df["day_of_week"] = df["start_date_local"].dt.strftime("%A")
    df["hour"] = df["start_date_local"].dt.hour

    return df

def deduplicate(df):
    # Remove duplicates based on unique Strava ID
    before = len(df)
    df = df.drop_duplicates(subset="id")
    after = len(df)

    if before != after:
        print(f"Deduplicate: {before-after} duplicates removed")
    return df

def save_processed(df):
    # Save transformed data in Silver layer
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)
    output_file = PROCESSED_DATA_PATH / "activities.parquet"
    df.to_parquet(output_file,index=False)
    print(f"Saved: {len(df)} activities in {output_file}")

def transform():
    print("Transformation started...")

    df = load_raw_activities()
    print(f"Loaded:{len(df)} activities, {len(df.columns)} columns")

    df = select_columns(df)
    df = deduplicate(df)
    df = transform_units(df)
    df = transform_dates(df)

    print(f"Transformed: {len(df.columns)} columns")
    save_processed(df)

if __name__ == "__main__":
    transform()
