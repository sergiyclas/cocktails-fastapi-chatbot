import tiktoken
import asyncio
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from app.database.orm_query import SQLiteDB
from app.llm.rag import CocktailRAG
from config import SQLITE_DB_PATH

MODEL_NAME = "gpt-4-turbo"
MODEL_CONTEXT_SIZE = 8000
RESERVED_TOKENS_COUNT = 2000
MAX_MESSAGES_TOKENS_COUNT = MODEL_CONTEXT_SIZE - RESERVED_TOKENS_COUNT


class ChatBotRAG:
    def __init__(self):
        self.chat = ChatOpenAI(model_name=MODEL_NAME)
        self.db = SQLiteDB(SQLITE_DB_PATH)
        self.rag = CocktailRAG()

    async def ask(self, user_input: str, user_id: str):
        history = self.get_history(user_id)
        history.append(HumanMessage(content=user_input))

        relevant_cocktails = await self.rag.get_relevant_cocktails(user_input)

        cocktail_knowledge = "\n".join([
            f"- {cocktail['name']} (Category: {cocktail['category']})\n"
            f"  Glass Type: {cocktail['glassType']}\n"
            f"  Alcoholic: {cocktail['alcoholic']}\n"
            f"  Instructions: {cocktail['instructions']}\n"
            f"  Ingredients: {', '.join(cocktail['ingredients'])}\n"
            for cocktail in relevant_cocktails
        ]) or "No relevant cocktails found."

        prompt = f"""
        You are Cocktail Expert, who knows everything about cocktails. Give only precise and short answers.
        User Input: {user_input}
        User's Chat History: {self.format_history(history)}
        Relevant Cocktail Knowledge:
        {cocktail_knowledge}

        Based on the user's query and Relevant Cocktail Knowledge, generate an accurate response.
        """
        print(cocktail_knowledge)

        messages_to_send = self.truncate_messages([HumanMessage(content=prompt)])

        response = self.chat.invoke(messages_to_send)

        self.save_message(user_id, "user", user_input)
        self.save_message(user_id, "assistant", response.content)

        return response.content

    def get_history(self, user_id: str):
        history = self.db.get_chat_history(user_id)
        return self.convert_messages(history)

    def save_message(self, user_id: str, role: str, content: str):
        self.db.add_chat_message(user_id, role, content)

    @staticmethod
    def convert_messages(messages):
        chat_messages = []
        for message in messages:
            if message["role"] == "assistant":
                chat_messages.append(AIMessage(content=message["content"]))
            elif message["role"] == "user":
                chat_messages.append(HumanMessage(content=message["content"]))
            elif message["role"] == "tool":
                chat_messages.append(ToolMessage(tool_call_id=message["tool_call_id"], content=message["content"]))
            elif message["role"] == "system":
                chat_messages.append(SystemMessage(content=message["content"]))
        return chat_messages

    @staticmethod
    def format_history(messages):
        return "\n".join([f"{msg.type}: {msg.content}" for msg in messages])

    @staticmethod
    def truncate_messages(messages):
        enc = tiktoken.get_encoding("cl100k_base")
        tokens_used = 0
        truncated_messages = []

        for msg in reversed(messages):
            msg_tokens = len(enc.encode(msg.content))
            if tokens_used + msg_tokens > MAX_MESSAGES_TOKENS_COUNT:
                break
            truncated_messages.append(msg)
            tokens_used += msg_tokens

        return list(reversed(truncated_messages))


if __name__ == "__main__":
    chatbot = ChatBotRAG()
    response = asyncio.run(chatbot.ask("What are the 5 non-alcoholic cocktails containing sugar?", "1"))
    print(f"{response}")
