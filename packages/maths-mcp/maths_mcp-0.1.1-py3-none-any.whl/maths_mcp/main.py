import argparse
import os
from mcp.server.fastmcp import FastMCP
from .utils import handle_config

mcp = FastMCP("maths")


@mcp.tool(name="add", description="Add two numbers")
def add(a, b):
    return handle_config(a + b)

@mcp.tool(name="sub", description="Subtract two numbers")
def sub(a, b):
    return handle_config(a - b)

@mcp.tool(name="mul", description="Multiply two numbers")
def mul(a, b):
    return handle_config(a * b)

@mcp.tool(name="div", description="Divide two numbers")
def div(a, b):
    return handle_config(a / b)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Maths MCP server.")
    parser.add_argument(
        "--rounded",
        type=bool,
        required=True,
        help="Should the output be rounded to the nearest whole number?",
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    if args.rounded:
        os.environ["MCP_ROUND"] = "true"

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
