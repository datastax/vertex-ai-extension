# Vertex AI Extension

## Installation

### Initial Steps

1. Clone the repository:

    ```bash
    git clone git@github.com:riptano/vertex-ai-extension.git
    ```

2. In the [Google Secrets Manager](https://console.cloud.google.com/security/secret-manager), create a secret for your **Astra DB Credentials**, named `VERTEX_AI_TOKEN`, the format of which is as follows: `<ASTRA_DB_APPLICATION_TOKEN>;<ASTRA_DB_API_ENDPOINT>;<ASTRA_DB_TABLE>`.
3. Next, choose either a UI or Python-based method of registering the extension

### Using the Vertex AI Extension UI

1. Browse to the [Vertex AI Extensions Page](https://console.cloud.google.com/vertex-ai/extensions)
2. Click `Create New Extensions`
3. Fill in the fields of the form. See screenshots for example values.

### Using the Python SDK

1. Copy the `extension.yaml` file in the `astra-crud-extension-api` folder to the GCS bucket and folder of your choice, such as `gs://{BUCKET_NAME}/{EXTENSION_PATH}/extension.yaml`.
2. Register your extension using the Python SDK, substituting `<BUCKET_NAME>` and `{EXTENSION_PATH}` as appropriate:

    ```python
    from google.cloud.aiplatform.private_preview import llm_extension

    SECRET_ID = "VERTEX_AI_TOKEN"

    # Include multiple selection, invocation, and response examples for best results.
    extension_selection_examples = [
        {
          "query": "I want to learn about the products",
          "multi_steps": [{
              "thought": "I should call astra_tool for this",
              "extension_execution": {
                "operation_id": "readData",
                "extension_instruction": "Describe the product that you want to learn about",
                "observation": "Product descriptions come from the description field"
              }
            },
            {
              "thought": "Since the observation was successful, I should respond back to the user with results",
              "respond_to_user": {}
            }],
        },
        {
          "query": "I want to insert a new product",
          "multi_steps": [{
              "thought": "I should call astra_tool for this",
              "extension_execution": {
                "operation_id": "insertData",
                "extension_instruction": "Insert relevant data into Astra DB",
                "observation": "Product descriptions come from the description field"
              }
            },
            {
              "thought": "Since the observation was successful, I should respond back to the user with results",
              "respond_to_user": {}
            }],
        }
    ]
    
    extension_invocation_examples = [{
          "extension_instruction": "Tell me about your product.",
          "operation_id": "readData",
          "thought": "Issue a readData operation request on hello_astra tool",
          "operation_param": "{\"prompt\": \"Tell me about the product.\"}",
          "parameters_mentioned": ["prompt"]
    }]
    
    extension_response_examples = [{
      "operation_id": "readData",
      "response_template": "{{ response }}",
    }]
    
    extension_astra = llm_extension.Extension.create(
        display_name = "Perform a CRUD Operation on Astra DB",
        description = "Inserts, loads, updates, or deletes data from Astra DB and returns it to the user",
        manifest = {
            "name": "Astra CRUD Extension for Vertex AI",
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
            },
            "extension_selection_examples": extension_selection_examples,
            "extension_invocation_examples": extension_invocation_examples,
            "extension_response_examples": extension_response_examples,
        },
    )
    ```

3. Confirm extension has been successfully created at <https://console.cloud.google.com/vertex-ai/extensions>

## Getting Started Info from Google

- The following project numbers are allowlisted to Vertex Extensions:
  - Project Number(s): 747469159044 (Integrations Project)
- To get started:
  - First, [download the SDK here](https://console.cloud.google.com/storage/browser/vertex_ai_extensions_sdk_private_releases;tab=objects?forceOnBucketsSortingFiltering=true&project=vertex-sdk-dev&prefix=&forceOnObjectsSortingFiltering=false)
  - Then, access the [Colab notebook here](https://drive.google.com/drive/folders/17GbwWPaOq3GR1GTg_yxQRao6R_gpGplY) (includes tutorial & documentation)
- [Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/extensions/private/overview)

## For Astra Developers

Use of the extension required a deployed cloud run container.

1. If you have not already, ensure that you have authenticated with Google Cloud `gcloud auth login`
2. If you have not already, ensure that you have set your project id with `gcloud config set project integrations-379317`
3. `docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/integrations-379317/astra-api/astra-crud:20240312 astra-crud-extension`
4. `docker push us-central1-docker.pkg.dev/integrations-379317/astra-api/astra-crud:20240312`
5. Register the container artifact in [Cloud Run](https://console.cloud.google.com/run/create)
