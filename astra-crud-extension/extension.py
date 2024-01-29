from flask import Flask, jsonify, request

from google.cloud import secretmanager

from astrapy.db import AstraDB

import os
import uuid

# Set the path to the service account file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "integrations-379317-480fb9eb65d2.json"

# Provide the GCP Project ID
project_id = os.environ.get("PROJECT_ID", "747469159044")

# Access the secret client
secret_client = secretmanager.SecretManagerServiceClient()

# Next, access the secret for the Astra Token
secret_id = "ASTRA_DB_APPLICATION_TOKEN"
version_id = 1
secret_name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
response = secret_client.access_secret_version(request={"name": secret_name})
DEFAULT_TOKEN = response.payload.data.decode("UTF-8")

# Next, access the secret for the Astra DB Endpoint
secret_id = "ASTRA_DB_API_ENDPOINT"
version_id = 1
secret_name = f'projects/{project_id}/secrets/{secret_id}/versions/{version_id}'
response = secret_client.access_secret_version(request={"name": secret_name})
DEFAULT_API_ENDPOINT = response.payload.data.decode("UTF-8")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    data = {"message": "Hello, World!"}
    
    return jsonify(data)


@app.route("/readData", methods=["POST"])
def read_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token", DEFAULT_TOKEN)
    api_endpoint = params.get("api_endpoint", DEFAULT_API_ENDPOINT)

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", "test")
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.find(filter=filter)

    return jsonify(data)


@app.route("/insertData", methods=["POST"])
def insert_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token", DEFAULT_TOKEN)
    api_endpoint = params.get("api_endpoint", DEFAULT_API_ENDPOINT)

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Some example data
    doc = {
        "_id": str(uuid.uuid4()),
        "name": "Coded Cleats Copy",
        "description": "ChatGPT integrated sneakers that talk to you",
        "$vector": [0.25, 0.25, 0.25, 0.25, 0.25],
    }

    # Optional Params for the astra call
    table = params.get("tableName", "test")
    data = params.get("data", doc)

    # Initialize our vector db
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.create_collection(table, dimension=5)

    # Insert a document into the test collection
    data = astra_db_collection.insert_one(data)

    return jsonify(data)


@app.route("/updateData", methods=["POST"])
def update_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token", DEFAULT_TOKEN)
    api_endpoint = params.get("api_endpoint", DEFAULT_API_ENDPOINT)

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", "test")
    filter = params.get("filter", None)
    field_update = params.get("fieldUpdate", 1)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.find_one_and_update(filter=filter, update=field_update)

    return jsonify(data)


@app.route("/deleteData", methods=["POST"])
def delete_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token", DEFAULT_TOKEN)
    api_endpoint = params.get("api_endpoint", DEFAULT_API_ENDPOINT)

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", "test")
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.delete_many(filter=filter)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
