from typing import Optional, Any
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


# Request models
class APIRequest(BaseModel):
    user_id: int = Field(..., description="Unique identifier for the user id")
    message: str = Field(..., description="User message to process")

# Response models
class APIResponse(BaseModel):
    success: bool = True
    data: Any = None
    error: Optional[str] = None
