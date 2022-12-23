# ShipmonkAPI_list_of_products-to-GCP
This Project is a Python automation project  using Shipmonk API
we are pulling the list of products and number of inventory available using a shipmonk API end point and loading the data into big query table
the whole program is automated by creating a google cloud function in GCP and automating the program to run daily, hourly using Pub/Sub topic and  cloud scheduler service in googlle cloud
The following are pre_requisites to  automate the process
  1. Have a Google cloud project with Big query upgraded and ofcourse a billing account
  2. Have accesss to google cloud  Credentials.json file here is a link for more details:https://developers.google.com/workspace/guides/create-credentials#create_credentials_for_a_service_account
  3. Create a cloud function and add the runtime environment variables these are credentials that you need to secure eg API KEYS
  4. Dont forget to add library version of any python library you use
