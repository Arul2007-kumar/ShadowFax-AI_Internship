🤖 Student AI Assistant

A simple AI-powered web application that allows students to ask questions and get answers from an LLM (Large Language Model).

🚀 Features

- Ask questions to AI
- Get real-time AI responses
- Simple chat interface
- Frontend and backend integration
- Gemini LLM integration
- Responsive design

🛠️ Technologies

- HTML
- CSS
- JavaScript
- Python
- FastAPI
- Google Gemini API

📂 Project Structure

student-ai-assistant/
│
├── frontend/
│   ├── index.html
│   ├── indexstyle.css
│   |___output.html
|   └── outputstyle.css
├── backend/
│   ├── main.py
├── .env
└── requirements.txt
│
└── README.md

🔄 Working

User
 ↓
Frontend
 ↓
FastAPI Backend
 ↓
Gemini LLM
 ↓
AI Response
 ↓
Frontend

⚙️ Setup

1. Install Dependencies

pip install -r requirements.txt

2. Add API Key

Create a ".env" file:

GEMINI_API_KEY=your_api_key_here

3. Run Backend

uvicorn main:app --reload

4. Open Frontend

Open:

frontend/index.html

🎯 Purpose

This project was developed to learn Frontend Development, FastAPI, REST API, and LLM Integration.

👨‍💻 Author

Arul Kumar

Project: Student AI Assistant