# Astra DB Vertex AI Extension

The Astra DB Vertex AI Extension allows users to perform CRUD operations against their Astra databases using natural language. The supported operations are:

- readData
- insertData
- updateData
- deleteData

## Installation

Follow the steps below to register this extension against your Astra DB instance.

### Prerequisites

The steps on this page assume the following:

- You have an active [Vertex account](https://cloud.google.com/vertex-ai/) account.
- You have an active [Astra account](https://astra.datastax.com/signup) with:
  - An [Astra Serverless (Vector) database](https://docs.datastax.com/en/astra/astra-db-vector/databases/create-database.html#create-vector-database).
  - An [Astra application token](https://docs.datastax.com/en/astra/astra-db-vector/administration/manage-application-tokens.html) with the [database administrator role](https://docs.datastax.com/en/astra/astra-db-vector/administration/manage-database-access.html).
  - Vector data populated in your database. [Sample data sets](https://docs.datastax.com/en/astra/astra-db-vector/databases/load-data.html#load-sample-vector-data) are available.
- You have a Google Cloud project with:
  - The Vertex API enabled. For more, see [Get set up on Google Cloud](https://cloud.google.com/vertex-ai/docs/start/cloud-environment).
  - The Vertex AI Administrator (`roles/aiplatform.admin`) or Vertex AI User (`roles/aiplatform.user`) roles assigned to users or service accounts in your project. For more, see [Vertex AI access control with IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

### Initial Steps

1. Clone the repository:

    ```bash
    git clone git@github.com:datastax/vertex-ai-extension.git
    ```

2. In the [Google Secrets Manager](https://console.cloud.google.com/security/secret-manager), create a secret for your **Astra DB Credentials**, named `DATASTAX_VERTEX_AI_TOKEN`, the format of which is as follows: `[ASTRA_DB_APPLICATION_TOKEN];[ASTRA_DB_API_ENDPOINT];[ASTRA_DB_TABLE]`. **These values can be found in your Astra DB Portal after creating a database. See the above documentation links for more information**
3. Grant the Secrets Manager Secret Accessor permission in GCP to the required principal, i.e., your own account if registering the extension manually or the appropriate service account
4. Next, you must deploy the Docker Container to Cloud Run.

### Deploying your Container

1. If you have not already, ensure that you have authenticated with Google Cloud `gcloud auth login`
2. If you have not already, ensure that you have set your project id with `gcloud config set project [PROJECT_ID]`
3. Set the authentication for the Cloud Run Service, by granting the role Cloud Run Invoker to allAuthenticatedUsers
4. Create a repository for the container by running (more information [here](https://cloud.google.com/artifact-registry/docs/repositories/create-repos#create-gcloud)):

    ```bash
    gcloud artifacts repositories create astra-api \
    --repository-format=docker \
    --location=us-central1 \
    --description="Vertex AI Containers for Astra DB" \
    --async
    ```

5. To build the container, run the following, replacing `[PROJECT_ID]`: `docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/[PROJECT_ID]/astra-api/astra-crud astra-crud-extension`
6. To push the image, run the following, replacing `[PROJECT_ID]`: `docker push us-central1-docker.pkg.dev/[PROJECT_ID]/astra-api/astra-crud`
7. Register the container artifact as a service in [Cloud Run](https://console.cloud.google.com/run/create). Once deployed, you will receive a Cloud Run service URL.
8. Your Cloud Run service URL must be added to `astra-crud-extension-api/extension.yaml`, replacing `[YOUR_CLOUD_RUN_SERVICE_URL]` on line 8.
9. Next, choose either a UI or Python-based method of registering the extension

### Deploying your Vertex AI Extension

#### Using the Vertex AI Extension UI

1. Browse to the [Vertex AI Extensions Page](https://console.cloud.google.com/vertex-ai/extensions)
2. Click `Create Extension`
3. Fill in the fields of the form, choosing `extension.yaml` from the `astra-crud-extension-api` as your OpenAPI spec. See screenshots for example values. Note that you **must specify the API key secret field in the following format: `projects/[PROJECT_ID]/secrets/DATASTAX_VERTEX_AI_TOKEN/versions/latest`**

![Example of Registering Astra Extension](images/vertexai1.png)
![Example of Registering Astra Extension](images/vertexai2.png)

#### Using the Python SDK

1. If you have not already, ensure that you have authenticated with Google Cloud `gcloud auth login`
2. If you have not already, ensure that you have set your project id with `gcloud config set project [PROJECT_ID]`
3. Download and install the Vertex AI Python SDK with `pip install google-cloud-aiplatform`
4. Copy the `extension.yaml` file in the `astra-crud-extension-api` folder to the GCS bucket and folder of your choice, such as `gs://[BUCKET_NAME]/[EXTENSION_PATH]/extension.yaml`.
5. Register your extension using the Python SDK, substituting `[BUCKET_NAME]` and `[EXTENSION_PATH]` as appropriate:

    ```python
    from google.cloud.aiplatform.private_preview import llm_extension
  
    PROJECT_ID = "[PROJECT_ID]"
    SECRET_ID = "DATASTAX_VERTEX_AI_TOKEN"
    BUCKET_NAME = "[BUCKET_NAME]"
    EXTENSION_PATH = "[EXTENSION_PATH]"
    
    extension_astra = llm_extension.Extension.create(
        display_name = "Perform a CRUD Operation on Astra DB",
        description = "Inserts, loads, updates, or deletes data from Astra DB and returns it to the user",
        manifest = {
            "name": "astra_tool",
            "description": "Access and process data from AstraDB",
            "api_spec": {
                "open_api_gcs_uri": f"gs://{BUCKET_NAME}/{EXTENSION_PATH}/extension.yaml"
            },
            "authConfig": {
                "authType": "API_KEY_AUTH",
                "apiKeyConfig": {
                    "name": "token",
                    "apiKeySecret": f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/1",
                    "httpElementLocation": "HTTP_IN_HEADER",
                },
            }
        },
    )
    
    extension_astra
    ```

6. Confirm extension has been successfully created at the [Extensions Page](https://console.cloud.google.com/vertex-ai/extensions)

## Running your Extension

You can now run your extension, either testing from the Vertex AI Extensions UI, or via Python like so:

```python
extension_astra.execute("health", operation_params={})
extension_astra.execute("readData",
    operation_params = {},
)
```
