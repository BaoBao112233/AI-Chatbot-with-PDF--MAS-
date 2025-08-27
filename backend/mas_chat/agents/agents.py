from typing import Any
from mas_chat.configs.environments import get_environment_variables
from dotenv import load_dotenv
import os

from agents import Agent, Runner
from mas_chat.agents.custom_agent_hooks import CustomAgentHooks
from mas_chat.schemas.model import FinalResultSchema as FinalResult
from mas_chat.agents.tools.sample_tools import (
    random_number_tool as random_number,
    multiply_by_two_tool as multiply_by_two
)

from mas_chat.agents.tools.rag_tool import retrieve as retrieve_tool

env = get_environment_variables()

def load_env():
    """Load environment variables from .env file."""
    load_dotenv()
    # You can add validation here if needed
    required_vars = ['OPENAI_API_KEY']
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required environment variable: {var}")


multiply_agent = Agent(
    name="Multiply Agent",
    instructions="Multiply the number by 2 and then return the final result.",
    tools=[multiply_by_two],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Multiply Agent"),
)

chat_pdf_agent = Agent(
    name="Chat PDF Agent",
    instructions="Extract information from a PDF document.",
    tools=[retrieve_tool],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Chat PDF Agent"),
)

start_agent = Agent(
    name="Start Agent",
    instructions="Analyze user requirements and decide which Agent to include.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent, chat_pdf_agent],
    hooks=CustomAgentHooks(display_name="Start Agent"),
)

async def run_agents(input: str) -> Any:
    load_env()
    runner = Runner.run(
        start_agent,
        input=f"Generate a random number between 0 and {input}.",
    )

    result = await runner
    print("Done!")
    return result
