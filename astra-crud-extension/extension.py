import os
import uvicorn
import astrapy

from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Annotated, Any, List, Dict


app = FastAPI()

CALLER_NAME = "vertex-ai-extension"
CALLER_VERSION = "0.1.1"  # TODO: Proper versioning

class ReadParams(BaseModel):
    filter: Dict[str, Any] = {}


class InsertParams(BaseModel):
    data: List[Dict[str, Any]]


class UpdateParams(BaseModel):
    filter: Dict[str, Any]
    fieldUpdate: Dict[str, Any]


class DeleteParams(BaseModel):
    filter: Dict[str, Any]


@app.get("/health")
async def health_check():
    return {"status": "UP"}, 200


@app.post("/readData")
async def read_astra(
    params: ReadParams,
    raw_token: Annotated[str | None, Header(alias="token")] = None,
):
    # Fail if there is no token
    if not raw_token:
        return {"error": "Please provide a token"}

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return {"error": "api_endpoint not provided"}

    # Optional Params for the astra call
    filter = params.filter

    # Attempt to connect to Astra DB
    try:
        my_client = astrapy.DataAPIClient(
            caller_name=CALLER_NAME,
            caller_version=CALLER_VERSION,
        )
        my_database = my_client.get_database(
            api_endpoint=api_endpoint,
            token=token,
        )
        astra_db_collection = my_database.get_collection(table)
    except Exception as e:
        return {"error": str(e)}

    # Perform the find/read operation
    cursor = astra_db_collection.find(
        filter=filter,
    )

    results = []
    for result in cursor:
        results.append(result)

    return results, 200


@app.post("/insertData", status_code=201)
async def insert_astra(
    params: InsertParams,
    raw_token: Annotated[str | None, Header(alias="token")] = None,
):
    # Fail if there is no token
    if not raw_token:
        return {"error": "Please provide a token"}

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return {"error": "api_endpoint not provided"}

    # Optional Params for the astra call
    data = params.data

    # Fail if no data is provided
    if not data:
        return {"error": "Please provide data to insert"}

    # Attempt to connect to Astra DB
    try:
        my_client = astrapy.DataAPIClient(
            caller_name=CALLER_NAME,
            caller_version=CALLER_VERSION,
        )
        my_database = my_client.get_database(
            api_endpoint=api_endpoint,
            token=token,
        )
        astra_db_collection = my_database.get_collection(table)
    except Exception as e:
        return {"error": str(e)}

    # Insert the document(s) into the collection
    result = astra_db_collection.insert_many(data)

    return result


@app.post("/updateData", status_code=200)
async def update_astra(
    params: UpdateParams,
    raw_token: Annotated[str | None, Header(alias="token")] = None,
):
    # Fail if there is no token
    if not raw_token:
        return {"error": "Please provide a token"}

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return {"error": "api_endpoint not provided"}

    # Optional Params for the astra call
    filter = params.filter

    # Fail if no filter is provided
    if not filter:
        return {"error": "Please provide a filter for the update"}

    field_update = {"$set": params.fieldUpdate}

    # Attempt to connect to Astra DB
    try:
        my_client = astrapy.DataAPIClient(
            caller_name=CALLER_NAME,
            caller_version=CALLER_VERSION,
        )
        my_database = my_client.get_database(
            api_endpoint=api_endpoint,
            token=token,
        )
        astra_db_collection = my_database.get_collection(table)
    except Exception as e:
        return {"error": str(e)}

    # Perform the update operation
    result = astra_db_collection.update_many(filter=filter, update=field_update)

    return result


@app.post("/deleteData", status_code=202)
async def delete_astra(
    params: DeleteParams,
    raw_token: Annotated[str | None, Header(alias="token")] = None,
):
    # Fail if there is no token
    if not raw_token:
        return {"error": "Please provide a token"}

    token, api_endpoint, table = raw_token.split(";")

    # Error out if we don't have the token or api_endpoint
    if not api_endpoint:
        return {"error": "api_endpoint not provided"}

    # Optional Params for the astra call
    filter = params.filter

    # Attempt to connect to Astra DB
    try:
        my_client = astrapy.DataAPIClient(
            caller_name=CALLER_NAME,
            caller_version=CALLER_VERSION,
        )
        my_database = my_client.get_database(
            api_endpoint=api_endpoint,
            token=token,
        )
        astra_db_collection = my_database.get_collection(table)
    except Exception as e:
        return {"error": str(e)}

    # Perform the delete operation
    result = astra_db_collection.delete_many(filter=filter)

    return result


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
    )
