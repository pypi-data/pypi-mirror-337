# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Greeting")

# Add a greeting tool
@mcp.tool()
def greet(name: str) -> str:
    """Greet to the person with the given name"""
    return f"你好, {name}!"

def main():
    """Entry point for the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # Initialize and run the server
    main()