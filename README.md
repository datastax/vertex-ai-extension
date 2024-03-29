 # Astra DB Vertex AI Extension

The Astra DB Vertex AI Extension allows users to perform CRUD operations, using natural language, against their Astra databases. The supported operations are:

- readData
- insertData
- updateData
- deleteData

Follow the steps below to register this extension against your Astra DB instance.

## Installation

### Initial Steps

1. Clone the repository:

    ```bash
    git clone git@github.com:riptano/vertex-ai-extension.git
    ```

2. Download and install the SDK from below, see the Getting Started Info from Google section at the bottom of the README for more details.
3. In the [Google Secrets Manager](https://console.cloud.google.com/security/secret-manager), create a secret for your **Astra DB Credentials**, named `VERTEX_AI_TOKEN`, the format of which is as follows: `<ASTRA_DB_APPLICATION_TOKEN>;<ASTRA_DB_API_ENDPOINT>;<ASTRA_DB_TABLE>`.
4. Next, choose either a UI or Python-based method of registering the extension

### Using the Vertex AI Extension UI

1. Browse to the [Vertex AI Extensions Page](https://console.cloud.google.com/vertex-ai/extensions)
2. Click `Create New Extension`
3. Fill in the fields of the form, choosing `extension.yaml` from the `astra-crud-extension-api` as your OpenAPI spec. See screenshots for example values.

![Example of Registering Astra Extension](images/vertexai1.png)
![Example of Registering Astra Extension](images/vertexai2.png)

### Using the Python SDK

1. Copy the `extension.yaml` file in the `astra-crud-extension-api` folder to the GCS bucket and folder of your choice, such as `gs://{BUCKET_NAME}/{EXTENSION_PATH}/extension.yaml`.
2. Register your extension using the Python SDK, substituting `<BUCKET_NAME>` and `{EXTENSION_PATH}` as appropriate:

    ```python
    from google.cloud.aiplatform.private_preview import llm_extension
  
    PROJECT_ID = "[PROJECT_ID]"  # @param {type:"string"}
    SECRET_ID = "VERTEX_AI_TOKEN"
    BUCKET_NAME = "vai-bucket"
    EXTENSION_PATH = "astra-crud-extension"
    
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

3. Confirm extension has been successfully created at <https://console.cloud.google.com/vertex-ai/extensions>

## Running your Extension

You can now run your extension, either testing from the Vertex AI Extensions UI, or via Python like so, replacing the values provided with the values for our extension:

```python
from google.cloud.aiplatform.private_preview import llm_extension

extension_astra = llm_extension.Extension('projects/[PROJECT_ID_NUM]/locations/us-central1/extensions/[EXTENSION_ID_NUM]')

extension_astra.execute("hello", operation_params={})
extension_astra.execute("readData",
    operation_params = {},  # TODO: Pass in vector or query!
)
```

## For Astra Developers

Use of the extension requires a deployed cloud run container.

1. If you have not already, ensure that you have authenticated with Google Cloud `gcloud auth login`
2. If you have not already, ensure that you have set your project id with `gcloud config set project [PROJECT_ID]`
3. `docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/[PROJECT_ID]/astra-api/astra-crud:20240312 astra-crud-extension`
4. `docker push us-central1-docker.pkg.dev/[PROJECT_ID]/astra-api/astra-crud:20240312`
5. Register the container artifact in [Cloud Run](https://console.cloud.google.com/run/create)
