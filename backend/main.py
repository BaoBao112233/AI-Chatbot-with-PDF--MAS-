import os
import uvicorn
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Any
import logging
from mas_chat.configs.environments import env
from mas_chat.agents.agents import run_agents
from mas_chat.schemas.model import ChatRequest, ChatResponse, APIRequest, APIResponse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Initialize the FastAPI app
app = FastAPI(
    title="Template Multi-Agents System (MAS) API",
    description="API for interacting with the Template Multi-Agents System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Routes
@app.post("/ai/chat", response_model=ChatResponse)
async def chat(request: APIRequest):
    """Process a chat message and return a response"""
    try:
        # Convert to internal ChatRequest
        chat_request = ChatRequest(
            user_id=request.user_id,
            message=request.message
        )

        print(f'user_id: {request.user_id} | message: {request.message}')

        # Process the request
        result = await run_agents(chat_request)
        # Đảm bảo trả về đúng schema ChatResponse
        if isinstance(result, ChatResponse):
            return result
        return APIResponse(response=str(result), error_status="success")
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}", exc_info=True)
        return APIResponse(
            response="",
            error_status="Error processing request"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5555, reload=True)