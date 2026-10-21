from dotenv import load_dotenv
from anthropic import Anthropic 

load_dotenv()

client = Anthropic()

def ask_llm(prompt, model="claude-haiku-5-5"):
    """
    Makes an API request to the LLM and returns the text content of the reply.
    """
    try:
        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        for block in response.content:
            if block.type == "text":
                return block.text
        return "No answer came back."  
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred while processing your request: {e}"

if __name__ == "__main__":
    print(ask_llm("Reply with the single word: ready"))