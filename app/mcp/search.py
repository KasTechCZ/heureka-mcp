import json
from fastmcp import FastMCP
from app.base.requesters import HeaderSearchRequester


def register_search(mcp: FastMCP):
    requester = HeaderSearchRequester()

    @mcp.tool(
        name="search_products",
        description="Search the product catalog on Heureka.cz or Heureka.sk",
        tags={"catalog", "search"},
    )
    def search(query: str, country: str = "cz") -> str:
        """Search products on Heureka.cz/sk"""
        result = requester.search_products(query, country)
        return json.dumps(result, indent=2)


    #@mcp.tool(
    #    name="search_product_offers",
    #    description="Search product offers on Heureka.cz or Heureka.sk",
    #    tags={"catalog", "search"},
    #)
    #def search_offers(query: str, country: str = "cz", product_id: int = None) -> str:
    #    """Search offers on Heureka.cz"""
    #    result = requester.search_offers(query, country, product_id)
    #    return json.dumps(result, indent=2)
