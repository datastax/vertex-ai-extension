
import os

from flask import Flask, jsonify, request
from astrapy.db import AstraDB


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'UP'}), 200


@app.route("/readData", methods=["POST"])
def read_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    raw_token = params.get("token", request.headers.get("token"))

    # Fail if there is no token
    if not raw_token:
        return jsonify({"error": "Please provide a token"})

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return jsonify({"error": "api_endpoint not provided"})

    # Optional Params for the astra call
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    
    # Get the count of documents from Astra DB
    astra_docs_count = astra_db_collection.count_documents(filter=filter)
    
    # Perform the find operation
    data = list(astra_db_collection.paginated_find(
        filter=filter,
        projection={"$vector": 0},
        options={"limit": astra_docs_count["status"]["count"]}
    ))

    return jsonify(data), 200


@app.route("/insertData", methods=["POST"])
def insert_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    raw_token = params.get("token", request.headers.get("token"))

    # Fail if there is no token
    if not raw_token:
        return jsonify({"error": "Please provide a token"})

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return jsonify({"error": "api_endpoint not provided"})

    # Optional Params for the astra call
    data = params.get("data")

    # Fail if no data is provided
    if not data:
        return jsonify({"error": "Please provide data to insert"})

    # Initialize our vector db
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.create_collection(table, dimension=5)

    # Insert a document into the test collection
    data = astra_db_collection.insert_one(data)

    return jsonify(data), 201


@app.route("/updateData", methods=["POST"])
def update_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    raw_token = params.get("token", request.headers.get("token"))

    # Fail if there is no token
    if not raw_token:
        return jsonify({"error": "Please provide a token"})

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return jsonify({"error": "api_endpoint not provided"})

    # Optional Params for the astra call
    filter = params.get("filter", None)
    field_update = {"$set": params.get("fieldUpdate", 1)}

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.find_one_and_update(filter=filter, update=field_update)

    return jsonify(data), 200


@app.route("/deleteData", methods=["POST"])
def delete_astra():
    params = request.json

    # Grab the Astra token and api endpoint from the environment
    raw_token = params.get("token", request.headers.get("token"))

    # Fail if there is no token
    if not raw_token:
        return jsonify({"error": "Please provide a token"})

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return jsonify({"error": "api_endpoint not provided"})

    # Optional Params for the astra call
    filter = params.get("filter", None)

    # Call the vector find operation
    astra_db = AstraDB(token=token, api_endpoint=api_endpoint)
    astra_db_collection = astra_db.collection(table)
    data = astra_db_collection.delete_many(filter=filter)

    return jsonify(data), 202


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
