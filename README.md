## Project overview
I created this pipeline to extract data from Strava via API and transform the data. The pipeline runs local but is build with Azure in mind; raw and processed data are stored in Azure Data Lake Storage. For visualisations I use PowerBI.   

## Architecture
Extract.py retrieves data from Strava by looping a GET API call. The "last_extract" section updates to create an incremental data extraction. The result is stored without transformations as .json in Azure as the bronze layer.  

Transform.py updates the data by making changes to data types, conversions in data (e.g. m/s to km/h) and selecting columns for data analysis. The result is stored as .parquet in Azure as the silver layer. 

Load.py uploads the .json and .parquet files into Azure Data Lake Storage. PowerBI connects to the silver layer to visualise the data in an interactive dashboard. 

Explore.py is a supporting script to inspect the data types and column values. 

## Installation
Check and update Python version if necessary, create virtual environment in Visual Studio Code. 
Install packages by executing requirements.txt: pip install -r requirements.txt
Create Strava Developer App to retrieve STRAVA credentials. 
Create .env file for variables not pulled from GitHub. These include:
STRAVA_CLIENT_ID=
STRAVA_CLIENT_SECRET=
STRAVA_REDIRECT_URI=
STRAVA_ACCESS_TOKEN=
STRAVA_REFRESH_TOKEN=
STRAVA_TOKEN_EXPIRES_AT=
AZURE_STORAGE_CONNECTION_STRING=
Create Azure account, configure containers bronze and silver for data storage.

## Usage
The pipeline runs end-to-end with one bash command:
python pipeline.py. 
This executes all functions defined in extract.py, transform.py and load.py. Each script can be run individually via: 
python src/extract.py
python src/transform.py
python src/load.py

Auth.py must be run manually once to retrieve STRAVA API tokens: store these tokens in .env file.
 
## Project structure
These are the folders: 
```
strava-pipeline/
├── data/
│   ├── raw/          # .json data extracted from Strava
│   └── processed/    # .parquet transformed data 
├── src/
│   ├── auth.py       # one-off authorisation
│   ├── config.py     # sets configuration variables
│   ├── explore.py    # supporting script to investigate the data
│   ├── extract.py    # script to extract data from Strava
│   ├── transform.py  # script to transform data
│   └── load.py       # script to load raw and processed data into Azure bronze and silver layer. 
├── sql/
│   └── queries.sql   # file for SQL queries
├── pipeline.py       # script to run complete pipeline
├── .env              # environment variables
├── .gitignore        # defines what should not be committed to GitHub
├── requirements.txt  # Python dependencies 
└── README.md         # project description
```

## Technical considerations
Extract-Load-Transform: this pipeline assumes an Azure Data Lake as storage, allowing semi-structured data such as JSON. Although the source data remains available in Strava, this approach can handle transformation-logic changes without having to extract the raw data again. Finally, having transform as the final stage allows flexible data marts for various analytical purposes. 

Incremental extraction: after a first full data extraction, the pipeline can run on an interval to extract only new activities. This reduces API calls, Azure storage and processing time, and potential cloud-usage costs.

Parquet: parquet preserves data types and reduces file size compared to CSV or JSON.  

Medallion: separating raw data storage and transformation ensures traceability and auditability of the pipeline. 

## Scope considerations
The pipeline is limited to Azure's free tier. Several changes would be possible with a production environment: 
- Using Azure Data Factory for orchestration
- Using Azure Key Vault for credentials
- Using Azure SQL for the gold layer
- Using Azure Databricks for large-scale data transformations
