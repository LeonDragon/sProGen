# %%
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
#from langchain_core.messages import AIMessage
#from langchain_core.messages import HumanMessage
#from langchain_core.messages import SystemMessage

# template = """Question: {question}
# Answer: Let's think step by step."""
# prompt = ChatPromptTemplate.from_template(template)
# model = OllamaLLM(model="llama3")
# chain = prompt | model
# chain.invoke({"question": "What is LangChain?"})

# %%%
delimiter = "####"
system_message = f"""
Follow these steps to answer the customer queries.
The customer query will be delimited with four hashtags,\
i.e. {delimiter}. 

Step 1:{delimiter} First decide whether the user is \
asking a question about a specific product or products. \
Product cateogry doesn't count. 

Step 2:{delimiter} If the user is asking about \
specific products, identify whether \
the products are in the following list.
All available products: 
1. Product: TechPro Ultrabook
   Category: Computers and Laptops
   Brand: TechPro
   Model Number: TP-UB100
   Warranty: 1 year
   Rating: 4.5
   Features: 13.3-inch display, 8GB RAM, 256GB SSD, Intel Core i5 processor
   Description: A sleek and lightweight ultrabook for everyday use.
   Price: $799.99

2. Product: BlueWave Gaming Laptop
   Category: Computers and Laptops
   Brand: BlueWave
   Model Number: BW-GL200
   Warranty: 2 years
   Rating: 4.7
   Features: 15.6-inch display, 16GB RAM, 512GB SSD, NVIDIA GeForce RTX 3060
   Description: A high-performance gaming laptop for an immersive experience.
   Price: $1199.99

3. Product: PowerLite Convertible
   Category: Computers and Laptops
   Brand: PowerLite
   Model Number: PL-CV300
   Warranty: 1 year
   Rating: 4.3
   Features: 14-inch touchscreen, 8GB RAM, 256GB SSD, 360-degree hinge
   Description: A versatile convertible laptop with a responsive touchscreen.
   Price: $699.99

4. Product: TechPro Desktop
   Category: Computers and Laptops
   Brand: TechPro
   Model Number: TP-DT500
   Warranty: 1 year
   Rating: 4.4
   Features: Intel Core i7 processor, 16GB RAM, 1TB HDD, NVIDIA GeForce GTX 1660
   Description: A powerful desktop computer for work and play.
   Price: $999.99

5. Product: BlueWave Chromebook
   Category: Computers and Laptops
   Brand: BlueWave
   Model Number: BW-CB100
   Warranty: 1 year
   Rating: 4.1
   Features: 11.6-inch display, 4GB RAM, 32GB eMMC, Chrome OS
   Description: A compact and affordable Chromebook for everyday tasks.
   Price: $249.99

Step 3:{delimiter} If the message contains products \
in the list above, list any assumptions that the \
user is making in their \
message e.g. that Laptop X is bigger than \
Laptop Y, or that Laptop Z has a 2 year warranty.

Step 4:{delimiter}: If the user made any assumptions, \
figure out whether the assumption is true based on your \
product information. 

Step 5:{delimiter}: First, politely correct the \
customer's incorrect assumptions if applicable. \
Only mention or reference products in the list of \
5 available products, as these are the only 5 \
products that the store sells. \
Answer the customer in a friendly tone.

Use the following format:
Step 1:{delimiter} <step 1 reasoning>
Step 2:{delimiter} <step 2 reasoning>
Step 3:{delimiter} <step 3 reasoning>
Step 4:{delimiter} <step 4 reasoning>
Response to user:{delimiter} <response to customer>

Make sure to include {delimiter} to separate every step.
"""

user_message = f"""
by how much is the BlueWave Chromebook more expensive \
than the TechPro Desktop"""

# %%
# Define roles and placeholders
chat_template = ChatPromptTemplate.from_messages(
  [
    ("system", "You are a historian assistant, answer the question in short and concise manner"),
    ("user", "What is the tallest mountain in the world?"),
    ("ai", "Mount Everest"),
    ("user", "What is the largest ocean on Earth?"),
    ("ai", "Pacific Ocean"),
    ("user", "In which year did the first airplane fly?"),
    ("ai", "1903"),
    ("user", "{user_input}"),
    ("ai", ""),
   ]
)

messages = chat_template.format_messages(name="Alice", user_input="The answer Pacific Ocean is from who? ai or user, and from what question")

print(messages)

model = OllamaLLM(
        model="llama3.1",     # Model name (must be specified)
        temperature=0.0,      # Adjust the temperature for creativity
        num_ctx=2048,         # Default context window size
        num_predict=200,      # Maximum number of tokens to generate
)

prompt_value = model.invoke(messages)
print(prompt_value)
# %%
# model="llama3",       # Model name (must be specified)
# cache=None,           # No caching by default
# temperature=0.8,      # Default temperature
# num_ctx=2048,         # Default context window size
# num_gpu=None,         # Use default GPU configuration
# num_predict=128,      # Default number of tokens to predict
# num_thread=None,      # Auto-detect optimal number of threads
# repeat_last_n=64,     # Default for preventing repetition
# repeat_penalty=1.1,   # Default penalty for repetition
# stop=None,            # No default stop tokens
# tags=None,            # No default tags
# mirostat=0,           # Mirostat sampling disabled by default
# mirostat_eta=0.1,     # Default learning rate for Mirostat
# mirostat_tau=5.0,     # Default balance control for Mirostat
# keep_alive=None,      # No default keep-alive duration
# verbose=False,        # Default verbose setting is False
# top_k=40,             # Default top-k sampling
# top_p=0.9,            # Default top-p sampling
# tfs_z=1.0             # Tail free sampling disabled by default


# Explanation of Configurations:
# model: Specifies the model name, e.g., "llama3".
# cache: Determines whether to use caching for responses. It can be set to True, False, or a specific cache instance.
# temperature: Controls the randomness of the output. Lower values make the output more deterministic, while higher values increase randomness.
# num_ctx: Sets the context window size, i.e., the number of tokens the model can consider when generating the next token.
# num_gpu: Specifies the number of GPUs to use for inference.
# num_predict: Sets the maximum number of tokens to predict. It can be set to a specific number or special values like -1 for infinite generation.
# num_thread: The number of CPU threads to use for computation.
# repeat_last_n: Controls how far back the model looks to prevent repetition.
# repeat_penalty: Penalty applied to repeated tokens to reduce redundancy.
# stop: A list of stop tokens to cut off the model's output when encountered.
# tags: Tags to add to the run trace for tracking and organization.
# mirostat, mirostat_eta, mirostat_tau: Parameters for Mirostat sampling, controlling perplexity and response to feedback.
# keep_alive: Duration in seconds to keep the model loaded in memory.
# verbose: If True, prints out additional information such as response text.
# top_k: Controls the diversity of the output by limiting the number of top tokens considered.
# top_p: Cumulative probability threshold for nucleus sampling, which includes tokens with a cumulative probability above this threshold.
# tfs_z: Tail free sampling, reducing the impact of less probable tokens.




# %%
