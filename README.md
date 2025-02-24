﻿# Cocktail Chatbot API

Цей проєкт – **AI-чатбот**, що використовує **GPT-4 Turbo** та **RAG (Retrieval-Augmented Generation)** на основі FAISS + SQLite для відповіді на питання про коктейлі.  
Чатбот вміє зберігати історію діалогів та покращує відповіді за допомогою **векторного пошуку** по базі коктейлів.  

## **Функціонал**
- ✅ Відповідає на питання про коктейлі, інгредієнти та приготування
- ✅ Використовує **RAG** для пошуку найрелевантніших коктейлів
- ✅ Зберігає **історію чату** для кращої персоналізації
- ✅ API-документація доступна через **Swagger UI**
  
---

## **1. Встановлення і запуск**
Спочатку **клонуємо репозиторій** і встановлюємо залежності:

```bash
git clone https://github.com/your-repo/cocktail-chatbot.git
cd cocktail-chatbot
python -m venv venv  # (Створення віртуального середовища)
```

Активація середовища:
```bash
source venv/bin/activate  # (Linux/macOS) 
```
```bash
venv\Scripts\activate  # (Windows)
```
Встановлення залежностей:
```bash
pip install -r requirements.txt
```

## **2. Налаштування API-ключів**
Потрібно у кореневій папці створити файл .env, який має такий вигляд:
```
OPENAI_API_KEY=your_openai_api_key_here
```
your_openai_api_key_here - це ключ від OPENAI API. Можна тут отримати:
https://platform.openai.com/settings/organization/api-keys

## **3. Запуск**

```bash
python app.py
```

## **4. Перевірка функціональності**"
Тестування через Swagger:
Перейдіть за посиланням: http://localhost:8060/docs

Використовуйте доступні ендпоінти для перевірки функціональності.

Введіть у методі POST user_input(ваше питання по коктелях) та user_id(не має значення який), натисніть Try it out і очікуйте результату.

Тестування через POSTMAN:
Використовуйте посиланням: http://localhost:8060/chat/

Методом POST відправте user_input та user_id та очікуйте відповідь.
