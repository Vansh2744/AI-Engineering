from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

llm = ChatGroq(model=os.getenv('GROQ_MODEL'), api_key=os.getenv('GROQ_API_KEY'))

# hist = []

# while True:
#     query = input("User: ")
#     if query == "exit":
#         break
#     hist.append({'role':'user','content':query})
#     res = llm.invoke(hist)
#     hist.append({'role':'ai','content':res.content})
#     print(f"AI: {res.content}")
