from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("My App")
def main():
    if len(sys.argv) > 1:
        print(f"Hello, {sys.argv[1]}!")
    else:
        print("Hello, world!")
    mcp.run()

if __name__ == "__main__":
    main()
