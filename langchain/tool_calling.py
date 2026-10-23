from langchain_nimble import NimbleSearchTool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain.tools import tool
import os
import requests
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

load_dotenv()

llm = ChatGroq(model=os.getenv('GROQ_MODEL'))

@tool
def search_tool(query:str):
    """
    Search anything on google for real time information.
    Args:
        query - user search query for google search
        
    Return - result from google search
    """

    search = NimbleSearchTool(k=5, deep_search=True, parsing_type="markdown")

    res = search.invoke(query)

    return res

@tool
def get_weather(city:str):
    """
        Get real time weather details like temperature, humidity and others.
        Args:
            city - city name for weather details
        Return -> Weather data from the api response.
    """
    API_URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={os.getenv('WEATHER_API_KEY')}"

    res = requests.get(API_URL)
    if res.status_code == 200:
        return res.json()
    return "Unable to find details for this city"

agent = create_agent(
    model=llm, 
    tools=[search_tool, get_weather],
    system_prompt=(
            "You are a research assistant with google search and weather tools.\n"
            "Use 'google_search' for quick search on google"
            "for deep research that may take several minutes."
            "If user is looking for weather details like temperature, humidity or any other details"
            "then call the 'weather_tool' to get the real time weather data"
        ),
        checkpointer=InMemorySaver()
    )

while True:
    query = input("User: ")
    if query.lower() == "exit":
        break
    res = agent.invoke({'messages':[{'role':'user', 'content':query}]},config={'configurable':{'thread_id':'1'}})
    print(f"AI: {res['messages'][-1].content}")