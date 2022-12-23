import base64
import os
from google.cloud import bigquery
import requests
import pandas as pd
import datetime

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    api_key=os.environ.get("api_key")
    endpoint="https://api.shipmonk.com/v1/products"

    shipmonk_params={
        "page":1,
        "pageSize":50,
        "status":"active"
            
    }
    headers={
        'Api-Key':api_key
    }
    # Initialize the data list
    data = []

    # Set the maximum number of pages to retrieve
    max_pages = 5

    # Loop through the pages
    for page in range(1, max_pages + 1):
        # Update the page number in the parameters
        shipmonk_params['page'] = page
        
        # Make the GET request
        response = requests.get(endpoint, params=shipmonk_params, headers=headers)
        
        # Check the status code of the response
        if response.status_code == 200:
            # If the request was successful, append the data to the list
            data.extend(response.json()['data'])
            
        else:
            # If the request was not successful, print an error message
            print(f'An error occurred on page {page}: {response.status_code}')


    # print(data)
    # Convert the JSON data into a well-formatted and readable string
    # formatted_json = json.dumps(data, indent=2)

    #   # Print the formatted JSON string
    # print(formatted_json)

    # Extract the 'sku', 'name', and 'quantity_total_on_hand' fields from the dictionaries in the data list
    skus = [d['sku'] for d in data]
    names = [d['name'] for d in data]
    quantities_on_hand = [d['inventory']['quantity_total_on_hand'] for d in data]
    quantities_available = [d['inventory']['quantity_total_available'] for d in data]
    Quarantined_Inventory=[d['inventory']['quantity_total_quarantined']for d in data]
    allocated_inventory=[d['inventory']['quantity_total_unavailable']for d in data]


    # Extract the 'replacement_cost', 'custom_data', 'width', 'length', 'height', 'weight', 'packaging_type_identifier', 'packaging_type', 'barcodes', 'country_code', 'hs_code', 'created_at', 'updated_at', 'stock_out_days', 'product_type', 'is_fragile' fields from the dictionaries in the data list
    replacement_costs = [d.get('replacement_cost') for d in data]
    custom_data = [d.get('custom_data') for d in data]
    barcodes = [d.get('barcodes') for d in data]
    country_codes = [d.get('country_code') for d in data]
    hs_codes = [d.get('hs_code') for d in data]
    created_ats = [d.get('created_at') for d in data]
    Modified = [d.get('updated_at') for d in data]
    stock_out_days = [d.get('stock_out_days') for d in data]
    product_types = [d.get('product_type') for d in data]



    # Create a dataframe from the extracted data
    df = pd.DataFrame({'SKU': skus, 'Name': names, 'Inventory_on_Hand': quantities_on_hand, 'Available_Inventory': quantities_available,"Quarantined_Inventory":
    Quarantined_Inventory,"allocated_inventory":allocated_inventory,
                    'Replacement_Value': replacement_costs, 'Customs_Value': custom_data,   'Barcode': barcodes, 'CountryId': country_codes, 'HsCode': hs_codes, 'Created': created_ats, 'Modified': Modified, 'Stockout_days': stock_out_days, 'Product_Type': product_types})




    df['Barcode'] = df['Barcode'].apply(lambda x: ','.join(map(str, x)))
    df['Customs_Value'] = df['Customs_Value'].apply(lambda x: ' '.join(map(str, x)))
    # Define a custom function to remove everything after the "T" character
    def remove_after_t(x):
        return x.split('T')[0]
    df['Created']=df['Created'].apply(remove_after_t)
    df['Modified']=df['Modified'].apply(remove_after_t)


    df['Created']=pd.to_datetime(df.Created, format='%Y-%m-%d')
    df['Modified']=pd.to_datetime(df.Modified, format='%Y-%m-%d')

    

    table_id=os.environ.get("table_id")
    project_id=os.environ.get("project_id")


    credentials_path="./abiding-hull-369419-f341cdc14ada.json"
    job_location='US'
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credentials_path
    df.to_gbq(table_id,project_id=project_id,if_exists="replace",location=job_location,progress_bar=True)    
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
