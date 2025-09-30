from pydantic import BaseModel
from fastapi import FastAPI

class coloumns(BaseModel):
    Date : int
    month : int
    year : int
    
    