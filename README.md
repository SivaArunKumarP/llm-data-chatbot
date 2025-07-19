# LLM‑Powered Data Analysis Chatbot

A simple web application that leverages the OpenAI GPT API to generate clean pandas code for exploring and analyzing any CSV dataset you upload. Built with Flask on the backend and a minimal HTML/CSS/JavaScript frontend.

---

## 🚀 Features

- **Upload CSV files** directly through the browser
- **Ask natural‑language questions** about your data
- **Receive Python pandas code** (and, optionally, matplotlib snippets) that answers your query
- **See results instantly** in the browser (text tables; chart support can be added)
- **Safe execution** via a restricted `exec` sandbox (no arbitrary `eval`)

---

## 📁 Project Structure
llm-data-chatbot/
-├── app.py # Flask server, OpenAI integration, code execution
-├── requirements.txt # Python dependencies
-├── templates/
-│── index.html # Single‑page frontend
-└── README.md # This file

WebPage Design:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c6a9b29c-8910-49db-9fee-c6ee55bcfb0c" />
