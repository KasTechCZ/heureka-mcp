import sys
from fastmcp import FastMCP
from app.mcp.search import register_search

mcp = FastMCP("Heureka")

register_search(mcp)

if __name__ == "__main__":
    if "--sse" in sys.argv:
        mcp.run(transport="sse")
    else:
        mcp.run()
