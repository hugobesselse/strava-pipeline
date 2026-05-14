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
        "id","name","sport_type","start_date_local","timezone",
        "distance","moving_time","elapsed_time","total_elevation_gain","average_speed",
        "max_speed","elev_high","elev_low","pr_count","achievement_count",
        "kudos_count","visibility","total_photo_count","manual"
    ]
    return df[columns]

def transform_units(df):
    # Convert meters to kilometers
    df["distance_km"] = (df["distance"]/1000).round(2)
    # Convert seconds to minutes
    df["moving_time_min"] = (df["moving_time"]/60).round(1)
    df["elapsed_time_min"] = (df["elapsed_time"]/60).round(1)
    df["moving_time_hours"] = (df["moving_time_min"]/60).round(0)
    df["elapsed_time_hours"] = (df["elapsed_time_min"]/60).round(0)
    # Convert speed from m/s to km/h
    df["average_speed_kmh"] = (df["average_speed"]*3.6).round(2)
    df["max_speed_kmh"] = (df["max_speed"]*3.6).round(2)
    # Remove original columns
    df = df.drop(columns=["distance","moving_time","elapsed_time","average_speed","max_speed"])
    return df

def transform_dates(df):
    # Convert date column to separate parts for PowerBI
    df["start_date_local"] = pd.to_datetime(df["start_date_local"])
    df["hour"] = df["start_date_local"].dt.hour
    return df

def create_dim_date(df):
    # Create date dimension table based on activities
    dates=pd.date_range(
        start=df["start_date_local"].min(),
        end=df["start_date_local"].max(),
        freq="D"
    )

    dim_date = pd.DataFrame({"date":dates})
    dim_date["Year"] = dim_date["date"].dt.year
    dim_date["Month"] = dim_date["date"].dt.month
    dim_date["Day"] = dim_date["date"].dt.day
    dim_date["Quarter"] = dim_date["date"].dt.quarter
    dim_date["Month_name"] = dim_date["date"].dt.strftime("%B")
    dim_date["Day_name"] = dim_date["date"].dt.strftime("%A")
    dim_date["Day_number"] = dim_date["date"].dt.dayofweek
    
    return dim_date

def save_processed_date(df,dim_date):
    PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

    df.to_parquet(PROCESSED_DATA_PATH / "activities.parquet", index=False)
    dim_date.to_parquet(PROCESSED_DATA_PATH / "dim_date.parquet", index=False)

    print(f"Saved: {len(df)} activities")
    print(f"Saved: {len(dim_date)} date rows in dim_date, ({len(dim_date)/365:.1f} years)")

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
