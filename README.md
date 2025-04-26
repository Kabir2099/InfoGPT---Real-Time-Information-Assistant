

# InfoGPT - Real-Time Intelligent Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-orange)
![LangChain](https://img.shields.io/badge/LangChain-Framework-ff69b4)
![License: MIT](https://img.shields.io/badge/License-MIT-green)

---

InfoGPT is a powerful **FastAPI + Streamlit** application built around **LangChain** and **LangGraph**.  
It connects real-world data (Weather, Stocks, Currency, News, IP Lookup) with an LLM-powered conversational agent that **understands flexible user queries** and **uses the correct tool automatically**! 🔥

> **Ask anything** ➡️ **LLM processes** ➡️ **Correct tool called** ➡️ **Real-time answer returned**.

---

## 🚀 Features

- 🔥 **Any-Way Currency Converter** (e.g., "How much is 200 CAD in USD?")
- 🌦️ **Live Weather Updates** for any location.
- 📈 **Get Latest Stock Prices** (by ticker symbol).
- 🌍 **IP Geolocation Lookup**.
- 📰 **Fetch Latest News Headlines** (no paraphrasing).
- ➗ **Built-in Calculator** for math queries.
- 🧠 **Threaded Chat Memory** — separate memory for each conversation.
- 👍👎 **Feedback System**: Like, dislike, and regenerate better answers!
- 📋 **One-click Copy** answers.

---

## 🛠️ Tech Stack

| Backend | Frontend | LLMs & Tools |
| :--- | :--- | :--- |
| FastAPI | Streamlit | LangChain, LangGraph |
| Pydantic | - | Groq LLMs (Gemma-2b, Gemma-9b) |
| Uvicorn | - | WeatherAPI, NewsData.io, ExchangeRate API |
| Logging | - | Yahoo Finance, IPAPI |

---

## 📂 Project Structure

```
├── app.py            # FastAPI backend server
├── frontend.py       # Streamlit frontend
├── requirements.txt  # All dependencies
├── .env              # API keys (Groq, WeatherAPI, etc.)
├── app.log           # Backend logs
├── README.md         # This file
```

---

## ⚙️ Installation Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/InfoGPT.git
cd InfoGPT
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

> ✅ **`requirements.txt`** handles all libraries including FastAPI, Streamlit, LangChain, etc.

### 4. Setup environment variables

Create a `.env` file in the root directory:

```dotenv
weather_api_key = 'Your weather key - weather.com '
google_api_key = 'your google llm key'
groq_api_key = 'groq api key'
news_api_key = 'from https://newsdata.io/api'
```

> 🚨 Make sure to replace with your actual API keys.

---

## 🖥️ Running the App

### Start Backend (FastAPI)

```bash
python app.py
```
✅ Runs at: `http://127.0.0.1:8000`

### Start Frontend (Streamlit)

```bash
streamlit run frontend.py
```
✅ Access app at: `http://localhost:8501`

---

## 💬 How to Use

- Start a **new chat**.
- Type a flexible natural query:
  - `"Convert 300 pounds to rupees"`
  - `"Weather in Paris today"`
  - `"Stock price of Microsoft"`
  - `"IP info of 8.8.8.8"`
  - `"Show latest tech news"`
- Like 👍 / Dislike 👎 the response.
- Provide custom feedback and **regenerate** better answers!
- Erase or delete conversation threads as needed.

---

## 🧠 Key Highlights

- **Flexible Language Input**:  
  User can type currency conversions or other questions *in any format* — no strict templates required.

- **Real-Time External Data**:  
  All tools fetch live, real-world information.

- **Feedback-Driven Improvements**:  
  Regenerate answers based on user feedback, making InfoGPT smarter over time.

---

## 📈 Future Enhancements

- [ ] Add support for PDF/CSV data upload and Q&A
- [ ] Stream backend responses (for faster UX)
- [ ] Full multi-user authentication system
- [ ] Deploy on AWS/GCP and Streamlit Cloud
- [ ] Admin panel for logs and analytics

---

## 🛡 License

Distributed under the **MIT License**.  
Feel free to use, modify, and contribute! 🚀

---

## 👤 Author

Built with ❤️ by [Kabir Sk]

- GitHub: (https://github.com/Kabir2099)
- LinkedIn: (https://linkedin.com/in/kabir-sk-5602141ba)





