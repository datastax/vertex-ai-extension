import os
import uuid

from flask import Flask, jsonify, request

from astrapy.db import AstraDB


app = Flask(__name__)


DEFAULT_TABLE_NAME="test"


@app.route("/", methods=["GET"])
def hello_world():
    data = {"message": "Hello, World!"}
    
    return jsonify(data)


@app.route("/readData", methods=["POST"])
def read_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token")
    api_endpoint = params.get("api_endpoint")

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", DEFAULT_TABLE_NAME)
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.find(filter=filter)

    return jsonify(data)


def insert_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    token = params.get("token")
    api_endpoint = params.get("api_endpoint")

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
    table = params.get("tableName", DEFAULT_TABLE_NAME)
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
    token = params.get("token")
    api_endpoint = params.get("api_endpoint")

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", DEFAULT_TABLE_NAME)
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
    token = params.get("token")
    api_endpoint = params.get("api_endpoint")

    # Error out if we don't have the token or api_endpoint
    if not token or not api_endpoint:
        return jsonify({"error": "token or api_endpoint not provided"})

    # Optional Params for the astra call
    table = params.get("tableName", DEFAULT_TABLE_NAME)
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.delete_many(filter=filter)

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
