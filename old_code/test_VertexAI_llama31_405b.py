# %%
#Install Vertex AI SDK for Python and other required packages
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-cloud-aiplatform
# ! pip3 install --upgrade --quiet google-cloud-aiplatform[langchain] openai
# ! pip3 install --upgrade --quiet langchain-openai

import os
from google.auth import default, transport
import openai

# Set environment variable for Google Application Credentials
SERVICE_ACCOUNT_PATH = r"D:\keys\focal-healer-431902-q6-19dcf02385ff.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

PROJECT_ID = "focal-healer-431902-q6"
LOCATION = "us-central1"
BUCKET_NAME = "mybucket"
BUCKET_URI = f"gs://{BUCKET_NAME}"

# Initialize Vertex AI SDK for Python
import vertexai
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=BUCKET_URI)

# Chat completions API
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from vertexai.preview import rag

# Authentication
credentials, project = default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
auth_request = transport.requests.Request()
credentials.refresh(auth_request)

# Configure the OpenAI SDK to point to the Llama 3.1 Chat Completions API endpoint
MODEL_LOCATION = "us-central1"
client = openai.OpenAI(
    base_url=f"https://{MODEL_LOCATION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{MODEL_LOCATION}/endpoints/openapi/chat/completions?",
    api_key=credentials.token,
)

# Configure Llama 3.1 
MODEL_ID = "meta/llama3-405b-instruct-maas"

# Chat
response = client.chat.completions.create(
    model=MODEL_ID, messages=[{"role": "user", "content": "Hello, Llama 3.1!"}]
)

print(response.choices[0].message.content)
print(response.usage.prompt_tokens)
print(response.usage.completion_tokens)


# %%
