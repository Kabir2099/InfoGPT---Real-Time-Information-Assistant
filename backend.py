from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import requests
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict
from langchain_groq import ChatGroq
import yfinance as yf
import logging
from urllib.parse import urlparse, parse_qs

# ------------------- Logging Setup -------------------
log_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8", errors="ignore")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
# -----------------------------------------------------

# Load env
load_dotenv()
groq_api_key = os.getenv('groq_api_key')
weather_api = os.getenv('weather_api_key')
new_api_key = os.getenv('new_api_key')
google_api_key = os.getenv('google_api_key')
os.environ['google_api_key'] = google_api_key

llm = ChatGroq(groq_api_key=groq_api_key, model_name='Gemma2-9b-It')

# FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Tool 1: Weather Fetcher
@tool
def get_weather(location: str) -> str:
    """Fetches real-time weather for a given location using the WeatherAPI."""
    logging.info(f"Tool [get_weather] called with location: {location}")
    api_key = weather_api
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    weather_data = response.json()
    if "current" in weather_data:
        temp = weather_data['current']['temp_c']
        condition = weather_data['current']['condition']['text']
        result = f"Current weather in {location}: {temp}°C, {condition}"
    else:
        result = "Sorry, I couldn't fetch the weather data."
    logging.info(f"Tool [get_weather] result: {result}")
    return result


@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression like addition , substraction, divided or multiplication."""
    logging.info(f"Tool [calculator] called with expression: {expression}")
    try:
        result = str(eval(expression))
    except Exception as e:
        result = f"Error: {e}"
    logging.info(f"Tool [calculator] result: {result}")
    return result


@tool
def get_stock_price(ticker: str) -> str:
    """
    Retrieves the latest stock price for a given ticker symbol (e.g., 'AAPL', 'AMZN', 'TSLA') 
    from Yahoo Finance.

    Always call this tool with the stock's **official ticker symbol**.

    If the user provides a company name (e.g., 'Apple' or 'Tesla'), use the correct ticker symbol.
    """
    logging.info(f"Tool [get_stock_price] called with ticker: {ticker}")
    try:
        stock = yf.Ticker(ticker)
        price = stock.info.get('previousClose')
        if price is None:
            raise ValueError("No price found")
        logging.info(f"Tool [get_stock_price] result: {price}")
        return f"The latest closing price for {ticker.upper()} is ${price:.2f}"
    except Exception as e:
        logging.error(f"Error in get_stock_price: {str(e)}")
        return f"Sorry, I couldn't retrieve the stock price for '{ticker}'. Please check the symbol."


@tool
def get_news(query: str = 'latest') -> str:
    """Fetches the latest news based on the given query. Include all the news data with title and heading"""
    logging.info(f"Tool [get_news] called with query: {query}")
    api_key = new_api_key
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language=en"

    try:
        response = requests.get(url)
        response.raise_for_status()
        new_data = response.json()
        

        if "results" in new_data and new_data["results"]:
            
            if(len(new_data['results'])>5):
                articles = new_data["results"][:5]
            else:
                articles = new_data["results"]

            headlines = "\n".join([
                f"{i+1}. {article['title']}\n   {article['description']}"
                for i, article in enumerate(articles)
            ])
            logging.info(f"answer from Tool [get_news] : \n{headlines}")
            return f"Latest News on {query}:\n {headlines}"
        else:
            result = f"No news found for '{query}'."
    except Exception as e:
        result = f"❌ Error fetching news: {str(e)}"
    logging.info(f"Tool [get_news] result: {result}")
    return result




@tool
def currency_converter(amount: str) -> str:
    """Converts currency given in the format like '100 USD to INR'."""
    logging.info(f"Tool [currency_converter] called with amount: {amount}")
    try:
        parts = amount.strip().upper().split()
        if len(parts) != 4 or parts[2] != "TO":
            raise ValueError("Invalid format")

        amt = float(parts[0])
        base = parts[1]
        target = parts[3]

        url = f"https://open.er-api.com/v6/latest/{base}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data['result'] != "success":
            raise Exception("Currency API error")

        rate = data['rates'].get(target)
        if rate is None:
            raise ValueError(f"Currency '{target}' not found.")

        converted = amt * rate
        result = f"💱 {amt} {base} = {converted:.2f} {target}"
    except Exception as e:
        logging.error(f"Tool [currency_converter] error: {e}")
        result = "❌ Please format input like: '100 USD to INR'"
    logging.info(f"Tool [currency_converter] result: {result}")
    return result






@tool
def ip_lookup(ip: str) -> str:
    """
    Looks up geographical and ISP information for a given IP address.

    This tool uses the IPAPI service to fetch location data based on an IP address.
    It returns information such as country, city, and Internet Service Provider (ISP).

    Input:
        ip (str): The IP address to look up. Example: "8.8.8.8"

    Example usage:
        - "Where is 8.8.8.8 located?"
        - "Tell me about this IP address"
    
    Output example:
        🌍 IP Location:
        Country: United States
        City: Mountain View
        ISP: Google LLC
    """
    logging.info(f"Tool [ip_lookup] called with IP: {ip}")
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/")
        res.raise_for_status()
        data = res.json()
        result = f"🌍 IP Location:\nCountry: {data['country_name']}\nCity: {data['city']}\nISP: {data['org']}"
    except Exception as e:
        result = "❌ Couldn't retrieve IP information."
        logging.error(f"Tool [ip_lookup] error: {e}")
    logging.info(f"Tool [ip_lookup] result: {result}")
    return result


    





prompt = """
        You are an intelligent assistant designed to help users with real-world tasks using tools.

        Your available tools include:
        - Getting the weather
        - Evaluating math expressions
        - Fetching stock prices
        - Fetching the latest news
        - Converting currencies
        - Looking up IP address info

        Your job is to decide which tool(s) to use based on the user's question. Be accurate, clear, and helpful in your responses. Use the tools when appropriate, and return friendly, concise results.

        ⚠️ Special instructions:
        - For the 'get_news' tool: Always return the result exactly as received, without changing it.
        - For the 'currency_converter' tool:
            1. Detect and extract the amount, base currency, and target currency even if user writes casually.
            2. Reformat it into "amount BASE_CURRENCY to TARGET_CURRENCY" format. (Example: "100 USD to INR")
            3. Pass it properly to the tool.

        If the question doesn't require any tools, answer it directly using your own knowledge.

        Examples:
        - "What's the weather in Paris?" → Use get_weather
        - "convert 100usd to inr" → detect amount 100, base USD, target INR → call currency_converter
        - "how much is 50 euros in yen?" → detect 50 EUR to JPY → call currency_converter

        Be helpful, brief, and clear in your communication.
        """




# Memory and agent
memory = InMemorySaver()
agent = create_react_agent(llm, tools=[
    get_weather, calculator, get_stock_price, get_news,
    currency_converter, ip_lookup
], checkpointer=memory, prompt=prompt)


class UserQuery(BaseModel):
    query: str
    config: Dict
    feedback: Optional[str] = None


def agent_response_generator(query: str, config: Dict) -> str:
    logging.info(f"Invoking agent with query: {query}")
    response = agent.invoke({'messages': query}, config=config)
    result = response['messages'][-1].content
    logging.info(f"Agent response: {result}")
    return result


@app.post("/query/")
async def get_agent_response(user_query: UserQuery):
    query = user_query.query
    config = user_query.config
    feedback = user_query.feedback

    logging.info(f"Received query: {query}")
    logging.info(f"Config: {config}")
    logging.info(f"Feedback: {feedback}")
    print(feedback)

    agent_response = agent_response_generator(query, config)


    logging.info(f"Final response: {agent_response}")
    return {"response": agent_response}


@app.get("/")
async def root():
    return {"message": "LangChain Agent with MemorySaver is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
