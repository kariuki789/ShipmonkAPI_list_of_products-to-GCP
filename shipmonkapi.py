import requests
import pandas as pd
api_key="eCRCo7pgxBBrHaUeVeYPXKNbCxGR7k8u7ZtvpDYPEHQGBP0E6k"
endpoint="https://api.shipmonk.com/v1/products"

shipmonk_params={
    "page":1,
    "pageSize":50,
    "status":"active"
        
}
headers={
    'Api-Key':api_key
}

response=requests.get(endpoint, params=shipmonk_params,headers=headers)
print(response.status_code)

data= response.json()

# print(data['data'])
dataFrame= data['data']
df=pd.DataFrame(dataFrame)
del df['inventory']
del df['barcodes']
# print(df)

from google.cloud import bigquery

table_id="abiding-hull-369419.Portfolio.Shipmonk"
project_id="abiding-hull-369419"
import os
credentials_path="C:/Users/Morris/OneDrive/Desktop/Python/API/abiding-hull-369419-f341cdc14ada.json"
job_location='US'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
df.to_gbq(table_id,project_id=project_id,if_exists="replace",location=job_location,progress_bar=True)