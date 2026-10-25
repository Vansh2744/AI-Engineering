from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from langchain.tools import tool
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os
from datetime import datetime
from langchain.agents import create_agent

load_dotenv()

engine = create_engine("sqlite:///crud.db")

LocalSession = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(200))
    completed = Column(Boolean, default=False)

    created_at = Column(String, nullable=False)

    def to_dict(self)->dict:
        return {
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'completed':self.completed,
            'created_at':self.created_at
        }

def init_db():
    Base.metadata.create_all(engine)

init_db()

@tool
def create(title:str, description:str=""):
    """
       Create a new Task
       Args:
         title - Title of the Task
         description - Description of the Task
    """

    with LocalSession() as session:
        task = Task(
            title = title,
            description = description,
            created_at = datetime.now().strftime("%d-%m-%Y %H-%M")
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return f'''
               Task Created!
               Id: {task.id} | Title: {task.title} | Description: {task.description} | Completed: {task.completed}
               '''

@tool
def read(task:str = "all"):
    """
       Read tasks from database
       Args:
         task - title of the task or all to read all tasks
    """

    with LocalSession() as session:
        query = session.query(Task)

        if task != "all":
            query = query.filter(Task.title == task)

        tasks = query.order_by(Task.id).all()

        if not tasks:
            return "No tasks found"

        all_tasks = [task.to_dict() for task in tasks]

        return all_tasks

@tool
def update_task(
    id:int,
    title:str,
    description:str,
    completed:bool
    ):
    """
      Update an existing task by its id
      Args:
         id - id of the task
         title - Updated title of the task if its any
         description - Updated Description of the task if its any
         completed - Updated completed if changed but it can be True or False
    """

    with LocalSession() as session:
        task = session.get(Task, id)
        if not task:
            return f"Task with id {id} not found"
        if title:
            task.title = title
        if description:
            task.description = description
        if completed:
            task.completed = completed

        session.commit()
        session.refresh(task)

        return f"""
                  Task: {task.id} updated
                  {task.to_dict()}
               """

@tool
def delete_task(id:int):
    """
      Permanently Delete the task by its id
      Args:
        id - id of the task to be deleted
    """

    with LocalSession() as session:
        task = session.get(Task, id)

        if not task:
            return f"Task with id: {id} not found"

        title = task.title

        session.delete(task)
        session.commit()

        return f"Task {title} deleted successfully"

llm = ChatGroq(model=os.getenv('GROQ_MODEL'))

agent = create_agent(
    model=llm,
    tools=[create, read, update_task, delete_task],
    system_prompt="""
          You are an Task Management Agent who can create, read, update and delete tasks
          Use the tools that i have provided to perform all these CRUD operations
    """,
    checkpointer=InMemorySaver()
)

while True:
    query = input("User: ")

    if query == "exit":
        break

    res = agent.invoke({'messages':[{'role':'user', 'content':query}]},{'configurable':{'thread_id':'1'}})

    print(f"AI: {res['messages'][-1].content}")