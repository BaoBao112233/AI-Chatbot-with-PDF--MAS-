from fastapi import APIRouter, Depends
from cachetools import TTLCache
from mas_template.agents.agents import Agent
from mas_template.schemas.model import ChatRequest, ChatResponse


Router = APIRouter(
    prefix="/ai", tags=["Chating with Multi Agents System "]
)

cache = TTLCache(maxsize=500, ttl=300)
@Router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, agent: Agent = Depends()) -> ChatResponse:
    response = agent.chat(request)
    return response