from dotenv import load_dotenv
from anthropic import Anthropic 

load_dotenv()

client = Anthropic()

usage_log = []
    
def ask_llm(prompt, model="claude-haiku-5-5", system=None):
    """
    Makes an API request to the LLM and returns the text content of the reply.
    """
    try:
        params = {
            "model": model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }
        
        if system:
            params["system"] = system
            
        response = client.messages.create(**params)
        usage_log.append({
            "model": model,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens, 
            })
        print(f"[ask_llm] model={model} stop_reason={response.stop_reason} output_tokens={response.usage.output_tokens}")
        
        texts = [block.text for block in response.content if block.type == "text"]
        if texts:
            return "".join(texts)
        return "No answer came back."
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred while processing your request: {e}"

if __name__ == "__main__":
    print(ask_llm("Reply with the single word: ready"))