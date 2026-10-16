from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated, Literal
from pydantic import BaseModel, Field
import os
from langgraph.types import interrupt, Command
from dotenv import load_dotenv

load_dotenv()

model = os.getenv('GROQ_MODEL')
api_key = os.getenv('GROQ_API_KEY')

llm = ChatGroq(model=model, api_key=api_key)

class EmailState(BaseModel):
    question: str = ""
    mail_reason: str = ""
    receiver_name: str = ""
    receiver_email: str = ""
    subject: str = ""
    body: str = ""
    feedback: str = ""
    feedback_count: int = 0
    response: str = ""

class UserDetails(BaseModel):
    mail_reason: str = Field("Reason of the email that why user want to send email")
    receiver_name: str = Field("Receiver Name if available else '' ")
    receiver_email: str = Field("Receiver Email Address")

class DraftDetails(BaseModel):
    subject: str = Field("Subject of the Email within 20 words")
    body: str = Field("Body of the Email including proper details, reason and greetings and others")

user_details_llm = llm.with_structured_output(UserDetails)

draft_details_llm = llm.with_structured_output(DraftDetails)

def retrieve_user_details(state: EmailState):
    """Retrieve User Details"""

    res:UserDetails = user_details_llm.invoke(f'Retrieve mail reason, receiver name and receiver email from the question: {state.question}')

    state.mail_reason = res.mail_reason
    state.receiver_name = res.receiver_name
    state.receiver_email = res.receiver_email

    return state

def draft_email(state: EmailState):
    """Draft the Email from User Details"""

    if state.feedback:
        prompt = f"""Revise this email based on the feedback below.
            Current Email: 
            Subject: {state.subject}
            Body: {state.body}

            Feedback: {state.feedback}

            Please write a proper mail body and subject. Without extra text and improvement based on the feedback. 
            Mail body max size will be 200 Words.  """

    else:
        prompt = f"""
        Write a email with these details:
        To: {state.receiver_email}
        Request: {state.mail_reason}
        
        Please write a proper mail body and subject. Without extra text. Mail body
        max size will be 200 Words.  
        """

    res:DraftDetails = draft_details_llm.invoke(prompt)

    state.subject = res.subject
    state.body = res.body

    return state

def review_node(state: EmailState):
    """Review the Drafted Email"""

    print('-'*10)
    print(f'Subject: {state.subject}\n')
    print(f'Body: {state.body}')
    print('-'*10)

    res = interrupt({'question':"Is this Drafted Email is Good or Not(Reply with yes or give the feedback)"})

    if res == "yes":
        state.feedback = ""
    else:
        state.feedback = res
        state.feedback_count += 1

    return state

def router(state: EmailState):
    if state.feedback.strip == "" or not state.feedback:
        return "send"
    if state.feedback_count > 2:
        return "cancel"
    return "draft"

def cancel_node(state:EmailState):
    print("You have reached the feedback limit")

    return state

def send_node(state:EmailState):
    state.response = "Email Send Successfully"
    return state

graph = StateGraph(EmailState)

graph.add_node("retrieve", retrieve_user_details)
graph.add_node("draft", draft_email)
graph.add_node("review", review_node)
graph.add_node("cancel", cancel_node)
graph.add_node("send", send_node)

graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "draft")
graph.add_edge("draft", "review")
graph.add_conditional_edges("review", router)
graph.add_edge("cancel", END)
graph.add_edge("send", END)

app = graph.compile(checkpointer=InMemorySaver())

res = app.invoke({'question':"Write an Email to Aman with email: aman@gmail.com that he have shortlisted for the applied AI Engineering role in Free Data Company"},{'configurable':{'thread_id':'1'}})

# res = app.invoke(Command("Change the name of the Company from Free Data to CoreMacasia Technologies"),{'configurable':{'thread_id':'1'}})
