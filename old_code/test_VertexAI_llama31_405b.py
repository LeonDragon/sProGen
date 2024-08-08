#%%
# TEST LLAMA 3.1 405B Instruct via Google Vertex AI Model
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel

# Initialize the Vertex AI client
aiplatform.init(project='focal-healer-431902-q6', location='us-central1')

# Load the Llama 3.1 405B Instruct model from Vertex AI Model Garden
model = TextGenerationModel.from_pretrained("llama3-405b-instruct-maas")

# Define your prompt
prompt = "Write a short story about a cat who goes on an adventure."

# Generate text with specific parameters
response = model.predict(
    prompt,
    max_output_tokens=256,  # Limit the generated text length
    temperature=0.7,        # Control the creativity level (higher = more creative)
    top_k=50,              # Limit the number of possible next words considered
    top_p=0.9,             # Limit the probability distribution of next words
)

# Print the generated text
print(response.text)

# %%
