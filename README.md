## Project overview
This pipeline extracts data from Strava via API, transforms the data and uses PowerBI to create visualisations. This project demonstrates practise in Visual Studio Code, Python, REST API's and PowerBI. The pipeline runs local but is build with Azure in mind; raw and processed data are stored in Azure Data Lake Storage. 

## Architecture
Extract.py retrieves data from Strava by looping a GET API call. The "last_extract" section updates to create an incremental data extraction. The result is stored without transformations as .json in Azure as the bronze layer.  

Transform.py updates the data by making changes to data types, conversions in data numbers and selections columns for data analysis. The result is stored as .parquet in Azure as the silver layer. 

Load.py uploads the .json and .parquet files into Azure Data Lake Storage.

PowerBI connects to the silver layer to visualise the data in an interactive dashboard. 

-- explore.py is a supporting script to inspect the data types and column values. 

## Installation
Check and update Python version if necessary, create virtual environment in Visual Studio Code. 
Install packages by executing requirements.txt: pip install -r requirements.txt
Create Strava Developer App to retrieve STRAVA credentials. 
Create .env file for variables not pulled from GitHub. These include:
# STRAVA_CLIENT_ID=
# STRAVA_CLIENT_SECRET=
# STRAVA_REDIRECT_URI=
# STRAVA_ACCESS_TOKEN=
# STRAVA_REFRESH_TOKEN=
# STRAVA_TOKEN_EXPIRES_AT=
# AZURE_STORAGE_CONNECTION_STRING=
Create Azure account, configure containers bronze and silver for data storage.

## Usage
The pipeline runs end-to-end with one bash command:
# python pipeline.py. 
This executes all functions defined in extract.py, transform.py and load.py. Each script can be run individually via: 
# python src/extract.py
# python src/transform.py
# python src/load.py

Auth.py must be run manually once to retrieve STRAVA API tokens: store these tokens in .env file.
 

