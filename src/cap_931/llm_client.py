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
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error occurred: {e}")
        return f"An error occurred while processing your request.: {e}"

if __name__ == "__main__":
    print(ask_llm("Reply with the single word: ready"))