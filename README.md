# ShipmonkAPI_list_of_products-to-GCP
This Project is a Python automation project  using Shipmonk API
we are pulling the list of products and number of inventory available using a shipmonk API end point using a Cloud Function written in Python that is triggered by a message on a Cloud Pub/Sub topic. When the function is triggered, it makes an HTTP GET request to the ShipMonk API with the specified API key and parameters. The function then retrieves data from the API and stores it in a list. The function then filters the data and stores it in a Pandas DataFrame. Finally, the function writes the DataFrame to a BigQuery table.

Here is a breakdown of the code:

1.  The function imports the required libraries and sets up some constants and variables.
2.  The function makes an HTTP GET request to the ShipMonk API using the requests library. The API key and parameters are specified in the request headers and query   string, respectively. The function stores the response data in a list.
3.  The function loops through the data in the list and extracts specific fields from the dictionaries. The extracted data is stored in separate lists.
4.  The function creates a Pandas DataFrame from the extracted data and writes it to a BigQuery table using the bigquery library.


The following are pre_requisites to  automate the process
  1. Have a Google cloud project with Big query upgraded and ofcourse a billing account
  2. Have accesss to google cloud  Credentials.json file here is a link for more details:https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account
  3. Create a cloud function and add the runtime environment variables these are credentials that you need to secure eg API KEYS
  4. Dont forget to add library version of any python library you use in the requirements.text file
