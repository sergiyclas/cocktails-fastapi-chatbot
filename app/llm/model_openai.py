import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ChatGPT:
    def __init__(self, model="gpt-4"):
        self.model = model
        openai.api_key = OPENAI_API_KEY

    def ask(self, prompt: str):
        """Відправляє запит до OpenAI GPT-4."""
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {e}"

# Приклад використання:
if __name__ == "__main__":
    chatbot = ChatGPT()
    print(chatbot.ask("What are 5 cocktails containing lemon?"))
