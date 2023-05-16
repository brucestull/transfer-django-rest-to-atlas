import os
import sys
import requests
import pymongo
from dotenv import load_dotenv


######################################################
# Code for date-time inclusion:
######################################################
import datetime

now = datetime.datetime.now()
date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current date and time:", date_time_string)
######################################################


# Load environment variables from .env file
load_dotenv()

# Define the url for the request, using environment variables for the url fragments:
url = f"{os.getenv('SERVER_ROOT_URL')}{os.getenv('API_ROOT')}{os.getenv('FIRST_ENDPOINT')}"


# Get the API response:
response = requests.get(url)
print("response.url: ", response.url)
# `response.text` contains a string returned by the API:
# print("response.text: ", response.text)
data = response.json()

# Get MongoDB Atlas connection settings:
mongo_db_username = os.getenv("MONGO_DB_USERNAME")
mongo_db_password = os.getenv("MONGO_DB_PASSWORD")
mongo_cluster_url = os.getenv("MONGO_CLUSTER_URL")

# Try to create a new client instance of `pymongo.MongoClient`:
try:
    client = pymongo.MongoClient(
        f"mongodb+srv://{mongo_db_username}:{mongo_db_password}@{mongo_cluster_url}/?retryWrites=true&w=majority"
    )
    print("Connected successfully!!!")

# return a friendly error if a URI error is thrown
except pymongo.errors.ConfigurationError:
    print(
        "An Invalid URI host error was received. Is your Atlas host name correct in your connection string?"
    )
    sys.exit(1)

db = client.transferDataDatabase
transfer_data_collection = db["transferDataCollection"]
current_collection = transfer_data_collection.find()
if current_collection:
    for document in current_collection:
        print(f"document: {document}")

documents_to_insert = [
    {
        "current_environment": os.getenv("CURRENT_ENVIRONMENT"),
        "date_time_string": date_time_string,
    },
    {
        "application": "transfer_data",
    },
    {
        "the_stuff_im_trying_to_transfer": data,
    }
]

try:
    print("Attempting to drop the collection...")
    transfer_data_collection.drop()
    print("Collection dropped successfully!")
except pymongo.errors.OperationFailure:
    print("The collection could not be dropped.")
    sys.exit(1)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Server selection error: {e}")
    sys.exit(1)

try:
    print("Attempting to insert the documents...")
    database_insert_result = transfer_data_collection.insert_many(documents_to_insert)
    print("Documents inserted successfully!")
# Throw an exception on a BulkWriteError.
except pymongo.errors.BulkWriteError as e:
    print(e.details["writeErrors"][0]["errmsg"])
    sys.exit(1)
# Throw an exception if an `OperationFailure` is raised.
except pymongo.errors.OperationFailure as e:
    print(f"Invalid insert operation: {e}")
    sys.exit(1)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Server selection error: {e}")
    sys.exit(1)
# If the documents are successfully inserted, print out the number of documents inserted.
else:
    inserted_count = len(database_insert_result.inserted_ids)
    print(f"{inserted_count} documents successfully inserted")

print("Done!")