import argparse
import os
from mcp.server.fastmcp import FastMCP
from .utils import handle_config

mcp = FastMCP("maths")


@mcp.tool(name="add", description="Add two numbers")
def add(a: float, b: float):
    return handle_config(float(a) + float(b))

@mcp.tool(name="sub", description="Subtract two numbers")
def sub(a: float, b: float):
    return handle_config(float(a) - float(b))

@mcp.tool(name="mul", description="Multiply two numbers")
def mul(a: float, b: float):
    return handle_config(float(a) * float(b))

@mcp.tool(name="div", description="Divide two numbers")
def div(a: float, b: float):
    return handle_config(float(a) / float(b))

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Maths MCP server.")
    parser.add_argument(
        "--rounded",
        type=bool,
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
