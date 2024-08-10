from openai import OpenAI
from langchain_ollama.llms import OllamaLLM
from config import OPENAI_API_KEY
import os
from google.auth import default, transport
import openai

def get_completion(messages, api="openai", model="gpt-4o-mini", json_format="", temperature=0.7, max_tokens=1000):
    # mode: gpt-4o-mini, gpt-4o, llama3.1, meta/llama3-405b-instruct-maas
    prompt_tokens = 0
    completion_tokens = 0
    if api == "openai":
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=float(temperature),
                max_tokens=max_tokens,
                response_format=json_format,
                strict=True
            )
            result = response.choices[0].message.content
            prompt_tokens= response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            result.parsed.steps
        except Exception as e:
            print(e.json()) # Handle validation errors
            pass
    elif api == "ollama":
        ollama_llm = OllamaLLM(
            model=model,
            temperature=temperature,
            num_ctx=4096,
            num_predict=max_tokens,
        )
        result = ollama_llm.invoke(messages)
    elif api == "vertexai":
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
        #MODEL_ID = "meta/llama3-405b-instruct-maas"

        # Chat
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        result = response.choices[0].message.content
        result = result.replace("\n", "")
        prompt_tokens= response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
    else:
        raise ValueError("Unsupported API specified. Choose 'openai' or 'ollama'.")
    
    return result, prompt_tokens, completion_tokens


# # TEST THE API
# messages = [{"role": "user", "content": "What is the tallest mountain in the world?"}]
# # Call for OpenAI API
# openai_result = get_completion(messages, api="openai", model="gpt-4o-mini")
# print("OpenAI Result:", openai_result)

# print("\n")

# # Call for Ollama API
# ollama_result = get_completion(messages, api="ollama", model="llama3.1")
# print("Ollama Result:", ollama_result)
# # %%
