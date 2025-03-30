from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

def main():
    mcp.run()

if __name__ == "__main__":
    main()
