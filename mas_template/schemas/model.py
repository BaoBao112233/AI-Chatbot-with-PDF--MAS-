from typing import Optional
from pydantic import BaseModel, Field


"""
Group Schema Input and Output each Agent

"""

class FinalResultSchema(BaseModel):
    number: int 


class ChatRequest(BaseModel):
    user_id: int
    message: str

class ChatResponse(BaseModel):
    response: str
    error_status: str = "success"