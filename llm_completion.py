from openai import OpenAI
from langchain_ollama.llms import OllamaLLM
from config import OPENAI_API_KEY

def get_completion(messages, api="openai", model="gpt-4o-mini", temperature=0.7, max_tokens=500):
    if api == "openai":
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        result = response.choices[0].message.content
    elif api == "ollama":
        ollama_llm = OllamaLLM(
            model=model,
            temperature=temperature,
            num_ctx=2048,
            num_predict=max_tokens,
        )
        result = ollama_llm.invoke(messages)
    else:
        raise ValueError("Unsupported API specified. Choose 'openai' or 'ollama'.")
    
    return result


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
