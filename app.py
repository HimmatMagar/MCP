from fastmcp import FastMCP
import random
import json


mcp = FastMCP("Remote MCP")

@mcp.tool
def generate_random_num(min: int = 1, max: int = 100) -> int:
    return random.randint(min, max)


@mcp.resource("info://server")
def server_info() -> str:
    info = {
        "Name": "Simple Remote MCP Server",
        "Version": "0.0.0.1",
        "Descriptions": "A small and simple remote mcp server",
        "tools": ["generate_random_num"]
    }
    return json.dump(info, indent=2)


if __name__ == "__main__":
    mcp.run(transport='http', host="0.0.0.0", port=8000)