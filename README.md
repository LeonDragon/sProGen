# sProGen - Automatic Sound Process Model Generation from Textual Description

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
      ```sh
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```

4. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **(Optional) Set up Google Cloud Authentication**:
   
    - Install the Google Cloud client library:
      ```sh
      pip install --upgrade google-cloud-aiplatform
      ```

    - Ensure you have the Google Cloud SDK installed. If not, you can download and install it from [here](https://cloud.google.com/sdk/docs/install).

    - Authenticate with Google Cloud:
      ```sh
      gcloud auth login
      ```

    - Set your Google Cloud project ID:
      ```sh
      gcloud config set project YOUR_PROJECT_ID
      ```
      Replace `YOUR_PROJECT_ID` with your actual Google Cloud project ID.

    - Create a service account and download its JSON key file. Follow these steps:
      1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
      2. Navigate to "IAM & Admin" > "Service Accounts".
      3. Click "Create Service Account".
      4. Provide a name and description for the service account and click "Create".
      5. Assign the necessary roles (e.g., "Vertex AI Admin") and click "Continue".
      6. Click "Done", then "Manage keys" for the service account.
      7. Click "Add Key" > "Create new key" and choose "JSON". Download the key file.

    - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to the downloaded JSON key file:
      - On Windows:
        ```sh
        set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-file.json"
        ```
      - On macOS/Linux:
        ```sh
        export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"
        ```
      Make sure to replace `/path/to/your/service-account-file.json` with the actual path to your service account key file.

6. **Run your project**:
    ```sh
    python Sample.py
    ```

## Using Llama 3.1 in Vertex AI

Here is an example of how to use the Llama 3.1 model in Vertex AI:

```python
import os
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-file.json"

# Initialize the Vertex AI client
aiplatform.init(project='your-project-id', location='us-central1')

# Load the Llama 3.1 405B Instruct model from Vertex AI Model Garden
model = TextGenerationModel.from_pretrained("llama3-405b-instruct-maas")

# Define your prompt
prompt = "Write a short story about a cat who goes on an adventure."

# Generate text using the model
response = model.predict(prompt)
print('Generated text:', response)
