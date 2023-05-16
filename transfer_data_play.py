import pymongo
import sys
import os
import requests


######################################################
# Code for date-time inclusion:
######################################################
import datetime

now = datetime.datetime.now()
date_time_string = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current date and time:", date_time_string)
######################################################


from dotenv import load_dotenv
load_dotenv()


# MongoDB Atlas connection settings:
mongo_db_username = os.getenv("MONGO_DB_USERNAME")
mongo_db_password = os.getenv("MONGO_DB_PASSWORD")
mongo_cluster_url = os.getenv("MONGO_CLUSTER_URL")

# Django REST variables:
server_root_url = os.getenv("SERVER_ROOT_URL")
api_root = os.getenv("API_ROOT")
first_endpoint_descriptor = os.getenv("FIRST_ENDPOINT_DESCRIPTOR")


# Get the api root response:




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

# Create/use a database named ????
db = client.first_endpoint_descriptor
print(f"db: {db}")

# Create/use a collection named ????
first_endpoint_collection = db["firstEndpointCollection"]

current_collection = first_endpoint_collection.find()

# Print the documents in the collection:
for document in current_collection:
    print(f"\ndocument: {document}")


# Get the current environment:
current_environment = os.getenv("CURRENT_ENVIRONMENT")
print(f"current_environment: {current_environment}")

# Create an environment document to insert into the collection.
current_environment_documents = [
    {
        "current_environment": current_environment,
        "date_time_string": date_time_string,
    },
    {
        "application": os.getenv("APPLICATION_NAME"),
    }
]
print(f"current_environment_documents: {current_environment_documents}")


try:
    print("Dropping collection...")
    first_endpoint_collection.drop()
    print("Collection dropped")
# Throw an exception if `first_endpoint_collection` collection does not exist.
except pymongo.errors.OperationFailure:
    print("Collection does not exist")
    sys.exit(1)
except pymongo.errors.ServerSelectionTimeoutError as e:
    print(f"Server selection error: {e}")
    sys.exit(1)

# Try to insert the documents into the collection.
try:
    print("Inserting documents...")
    result = first_endpoint_collection.insert_many(current_environment_documents)
    print(f"Multiple documents: {result.inserted_ids}")
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
    inserted_count = len(result.inserted_ids)
    print(f"{inserted_count} documents successfully inserted")

print("Done!")