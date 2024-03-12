# Vertex AI Extension

## Installation

### Using the GCP Vertex AI Extension GUI

1. Clone the repository:

    ```bash
    git clone git@github.com:riptano/vertex-ai-extension.git
    ```

2. If you have not already, ensure that you have authenticated with Google Cloud `gcloud auth login`
3. If you have not already, ensure that you have set your project id with `gcloud config set project your-project-id`
4. Build the docker container housing the Astra extension:

    ```bash
    docker build -t gcr.io/astra-crud-api/image-name:tag astra-crud-extension
    ```` 

5. Push your docker image to the Google Cloud Registry:

   ```bash
   docker push gcr.io/astra-crud-api/image-name:tag
   ```

5. In the [Google Secrets Manager](https://console.cloud.google.com/security/secret-manager), create a secret for your **Astra DB API Endpoint**, named `ASTRA_DB_API_ENDPOINT`, and for your **Astra DB Application Token**, named `ASTRA_DB_APPLICATION_TOKEN`.
6. Browse to the [Vertex AI Extensions Page](https://console.cloud.google.com/vertex-ai/extensions)
5. Click `Create New Extensions`
6. Fill in the fields of the form. 

### Using the Python SDK

1. Clone the repository:

    ```bash
    git clone git@github.com:riptano/vertex-ai-extension.git
    ```

2. Download your Google Cloud Platform JSON Service Account file to the `astra-crud-extension` directory
3. In your editor of choice, open `astra-crud-extension/extension.py`
4. On line 12 of `extension.py`, et the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the name of the JSON service account file from step 2
5. On line 15 of `extension.py`, set the `PROJECT_ID` environment variable to the ID of the GCP project
6. In the [Google Secrets Manager](https://console.cloud.google.com/security/secret-manager), create a secret for your **Astra DB API Endpoint**, named `ASTRA_DB_API_ENDPOINT`, and for your **Astra DB Application Token**, named `ASTRA_DB_APPLICATION_TOKEN`.
7. Copy the `extension.yaml` file in the `astra-crud-extension-api` folder to the GCS bucket of your choice.
8. Register your extension using the Python SDK, substituting `<YOUR_BUCKET_NAME>` as appropriate:

    ```python
    from google.cloud.aiplatform.private_preview import llm_extension

    llm_extension.Extension.create(
        display_name = "Read Astra",
        description = "Loads data from AstraDB and returns it to the user",
        manifest = {
            "name": "astra_tool",
            "description": "Access and process data from AstraDB",
            "api_spec": {
                "open_api_gcs_uri": f"gs://<YOUR_BUCKET_NAME>/extension.yaml"
            },
            "auth_config": {
                "auth_type": "NO_AUTH",
            },
        },
    )
    ```

9. Confirm extension has been successfully created at <https://console.cloud.google.com/vertex-ai/extensions>

## Getting Started Info from Google

- The following project numbers are allowlisted to Vertex Extensions:
  - Project Number(s): 747469159044 (Integrations Project)
- To get started:
  - First, [download the SDK here](https://console.cloud.google.com/storage/browser/vertex_ai_extensions_sdk_private_releases;tab=objects?forceOnBucketsSortingFiltering=true&project=vertex-sdk-dev&prefix=&forceOnObjectsSortingFiltering=false)
  - Then, access the [Colab notebook here](https://drive.google.com/drive/folders/17GbwWPaOq3GR1GTg_yxQRao6R_gpGplY) (includes tutorial & documentation)
- [Documentation](https://cloud.google.com/vertex-ai/docs/generative-ai/extensions/private/overview)

## For Astra Developers

Use of the extension required a deployed cloud run container.

1. `docker build -t us-central1-docker.pkg.dev/integrations-379317/astra-api/astra-crud:20240312 astra-crud-extension`
2. `docker push us-central1-docker.pkg.dev/integrations-379317/astra-api/astra-crud:20240312`
3. Register the container artifact in [Cloud Run](https://console.cloud.google.com/run/create)
