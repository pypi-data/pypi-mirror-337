"""MCP Greeting package"""

from .server import mcp

def main():
    """Entry point for the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    # Initialize and run the server
    main()
