from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from langchain.tools import tool
from pydantic import Field, BaseModel

load_dotenv()

llm = ChatGroq(model=os.getenv('GROQ_MODEL'))

def send_email(to:str, subject:str, body:str):
    smtp_server = "smtp.gmail.com"
    port = 587 
    sender_email = os.getenv('EMAIL_ADDRESS')
    password = os.getenv('EMAIL_APP_PASSWORD')
    receiver_email = to

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
        server.quit()

class SendEmailInput(BaseModel):
    to: str = Field(description="The recipient's email address")
    subject: str = Field(description="The email subject line")
    body: str = Field(description="The complete plain-text email body")

@tool(args_schema=SendEmailInput)
def send_email_tool(to:str, subject:str, body:str):
    """
     Send Email to any email address by providing the correct email address, subject and body.
     Args:
        to - email address
        subject - email subject in one line
        body - email body in plane text
    """
    send_email(to, subject, body)

    return f"Email Sent to email: {to} Successfully"

SYSTEM_PROMPT = """
You are an email drafting assistant.

Your Job is to take user query or input and generate 
receiver email address, subject of email and body of 
email from that input and send email to the receiver email address
"""

agent = create_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT,
    tools=[send_email_tool],
    checkpointer=InMemorySaver()
)

while True:
    query = input("User: ")
    if query.lower() == "exit":
        break
    res = agent.invoke({'messages':[{'role':'user', 'content':query}]},config={'configurable':{'thread_id':'1'}})
    print(f"AI: {res['messages'][-1].content}")