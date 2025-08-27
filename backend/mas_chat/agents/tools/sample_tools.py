import random
from agents import function_tool

@function_tool
def random_number_tool(max: int) -> int:
    """
    Generate a random number up to the provided maximum.
    """
    return random.randint(0, max)

@function_tool
def multiply_by_two_tool(x: int) -> int:
    """
    Multiply the input by two.
    """
    return x * 2

