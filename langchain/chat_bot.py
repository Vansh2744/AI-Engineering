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


if 'messages' not in st.session_state:
    st.session_state.messages = []

st.header("CHAT BOT")

for msg in st.session_state.messages:
    st.chat_message(msg.get('role')).markdown(msg.get('content'))

query = st.chat_input("Enter.....")

if query:
    st.session_state.messages.append({'role':'user','content':query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(st.session_state.messages)
    st.session_state.messages.append({'role':'ai', 'content':res.content})
    st.chat_message("ai").markdown(res.content)