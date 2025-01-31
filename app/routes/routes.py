from fastapi import APIRouter, HTTPException, Form
from app.llm.model_openai import ChatBotRAG

chat_router = APIRouter()
chatbot = ChatBotRAG()

@chat_router.post("/chat/")
async def chat_endpoint(user_input: str = Form(...), user_id: str = Form(...)):
    """
    Обробляє повідомлення користувача, виконує RAG-пошук та повертає відповідь GPT-4 Turbo.
    """
    try:
        response = await chatbot.ask(user_input, user_id)
        return {"user_id": user_id, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    """
    Отримує історію чату користувача.
    """
    try:
        history = chatbot.get_history(user_id)
        return {"user_id": user_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@chat_router.delete("/history/{user_id}")
async def clear_chat_history(user_id: str):
    """
    Видаляє історію чату користувача.
    """
    try:
        chatbot.db.clear_chat_history(user_id)
        return {"user_id": user_id, "status": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @chat_router.get('/')
# async def index() -> FileResponse:
#     return FileResponse(INDEX_HTML_PATH, media_type='text/html')
# @chat_router.get("/chat/")
# async def get_chat(user_id: str = Query("default_user")):
#     """Отримує історію чату користувача."""
#     chat_history = sqlite_db.get_chat_history_as_json(user_id)
#     return JSONResponse(content=chat_history)
#
#
# @chat_router.get("/chat_app.ts")
# async def get_chat_ts():
#     """Повертає TypeScript файл."""
#     ts_path = os.path.join(INTERFACE_DIR, "chat_app.ts")
#     if not os.path.exists(ts_path):
#         print("❌ chat_app.ts не знайдено")
#         return {"error": "chat_app.ts not found!"}
#     return FileResponse(ts_path)
#
#
# @chat_router.post("/chat/", summary="Відправити повідомлення в чат")
# async def post_chat(prompt: str = Form(...), user_id: str = "default_user"):
#     """
#     Відправляє повідомлення користувача та отримує відповідь від бота.
#     """
#     history = sqlite_db.load_chat_history(user_id)  # Завантажуємо історію
#
#     response_text = chatbot.ask(prompt, user_id, history)  # Отримуємо відповідь від бота
#
#     # Оновлюємо історію чату
#     new_message = {"role": "user", "content": prompt, "timestamp": datetime.now(timezone.utc).isoformat()}
#     new_response = {"role": "assistant", "content": response_text, "timestamp": datetime.now(timezone.utc).isoformat()}
#     history.extend([new_message, new_response])
#
#     sqlite_db.save_chat_history(user_id, history)
#
#     return JSONResponse(content={"response": response_text})
