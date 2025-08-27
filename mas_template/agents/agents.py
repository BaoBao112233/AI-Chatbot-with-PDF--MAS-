from typing import Any
from mas_template.configs.environments import get_environment_variables
from dotenv import load_dotenv
import os

from agents import Agent, Runner
from mas_template.agents.custom_agent_hooks import CustomAgentHooks
from mas_template.schemas.model import FinalResultSchema as FinalResult
from mas_template.agents.tools.sample_tools import (
    random_number_tool as random_number,
    multiply_by_two_tool as multiply_by_two
)

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

start_agent = Agent(
    name="Start Agent",
    instructions="Generate a random number. If it's even, stop. If it's odd, hand off to the multiply agent.",
    tools=[random_number],
    output_type=FinalResult,
    handoffs=[multiply_agent],
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
