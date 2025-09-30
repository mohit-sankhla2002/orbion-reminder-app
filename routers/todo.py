from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import
import enum

app = FastAPI()

# Enumeration portion 
class PeriorityEnum(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class StatusEnum(str, enum.Enum):
    pending = "Pending"
    inPrograss = "In Prograss"
    completed = "Completed"     

class Todos(BaseModel):
    __tablename__ = "todos"
    todo_id = 

class NewTask(BaseModel):
    user_id: str
    title: str
    description: str
    due_date: int
    status: str

@app.post("/todos")
def adding_new_task(newtask: NewTask):
    new_task = newtask.model_drop()
    return new_task