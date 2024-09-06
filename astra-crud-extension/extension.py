import os
import uvicorn
import astrapy

from fastapi import Depends, FastAPI, Header
from pydantic import BaseModel
from typing import Annotated, Any


app = FastAPI()

CALLER_NAME = "vertex-ai-extension"
CALLER_VERSION = "0.1.1"  # TODO: Proper versioning

my_client = astrapy.DataAPIClient(
    caller_name=CALLER_NAME,
    caller_version=CALLER_VERSION,
)

class ReadParams(BaseModel):
    filter: dict[str, Any] = {}


class InsertParams(BaseModel):
    data: list


class UpdateParams(BaseModel):
    filter: dict
    fieldUpdate: dict


class DeleteParams(BaseModel):
    filter: dict


@app.get("/health")
async def health_check():
    return {"status": "UP"}, 200


@app.post("/readData")
async def read_astra(
    params: ReadParams = Depends(),
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
    filter = params.filter.get('filter', {})

    # Attempt to connect to Astra DB
    try:
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
    params: InsertParams = Depends(),
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
    params: UpdateParams = Depends(),
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
    filter = params.filter.get('filter', {})

    # Fail if no filter is provided
    if not filter:
        return {"error": "Please provide a filter for the update"}

    field_update = {"$set": params.fieldUpdate}

    # Attempt to connect to Astra DB
    try:
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
    params: DeleteParams = Depends(),
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
    filter = params.filter.get('filter', {})

    # Attempt to connect to Astra DB
    try:
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
