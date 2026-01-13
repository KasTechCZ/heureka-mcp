import logging
import httpx
from typing import Optional, Dict, Any, List
from gql import Client, gql
from gql.transport.httpx import HTTPXTransport
from gql.transport.exceptions import TransportQueryError
from app.base.config import settings

# Configure logger
logger = logging.getLogger(__name__)
log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
logging.basicConfig(level=log_level)


class GraphqlGatewayRequester:
    def __init__(self, graphql_url: Optional[str] = None):
        self.graphql_url = graphql_url or settings.GRAPHQL_URL

    def _get_client_and_headers(self) -> (Client, Dict[str, str]):
        headers = {}
        transport = HTTPXTransport(url=self.graphql_url, headers=headers)
        client = Client(transport=transport, fetch_schema_from_transport=False)
        return client, headers

    def execute(
        self,
        query_str: str,
        variable_values: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        client, headers = self._get_client_and_headers()
        query = gql(query_str)

        logger.debug(f"Executing GraphQL query: {query_str}")
        if variable_values:
            logger.debug(f"Variables: {variable_values}")

        logger.debug(f"Request headers: {headers}")

        try:
            result = client.execute(query, variable_values=variable_values)
            logger.debug(f"GraphQL response: {result}")
            return result
        except TransportQueryError as e:
            logger.error(f"GraphQL TransportQueryError: {e}")
            raise e
        except Exception as e:
            logger.error(f"GraphQL Error: {e}")
            raise e

    def search_products(
        self,
        query_string: str,
        country: str = "cz",
    ) -> List[Dict[str, Any]]:
        query = """
        query SearchProducts($country: CountryCode!, $body: SerpRequestBody!) {
          serp(country: $country, body: $body) {
            product {
              id
              name
              slug
              categorySlug
              minPrice
              maxPrice
              reviewRating
              reviewCount
              offerCount
            }
          }
        }
        """
        result = self.execute(
            query,
            variable_values={
                "country": country,
                "body": {"query": query_string},
            },
        )
        products = result.get("serp", {}).get("product", [])
        return [
            {
                "id": product.get("id"),
                "name": product.get("name"),
                "minPrice": product.get("minPrice"),
                "maxPrice": product.get("maxPrice"),
                "reviewRating": product.get("reviewRating"),
                "reviewCount": product.get("reviewCount"),
                "offerCount": product.get("offerCount"),
                "url": f"https://{product.get('categorySlug')}.heureka.{country}/{product.get('slug')}/"
            }
            for product in products
        ]

    def search_offers(
        self,
        query_string: str,
        country: str = "cz",
    ) -> List[Dict[str, Any]]:
        query = """
        query SearchOffers($country: CountryCode!, $body: SerpRequestBody!) {
          serp(country: $country, body: $body) {
            offers {
              id
              name
              description
              price
              shopName
              preferredExit {
                url
              }
            }
          }
        }
        """
        result = self.execute(
            query,
            variable_values={
                "country": country,
                "body": {"query": query_string},
            },
        )
        offers = result.get("serp", {}).get("offers", [])
        return [
            {
                "id": offer.get("id"),
                "name": offer.get("name"),
                "description": offer.get("description"),
                "price": offer.get("price"),
                "shopName": offer.get("shopName"),
                "url": offer.get("preferredExit", {}).get("url"),
            }
            for offer in offers
        ]


class HeaderSearchRequester:
    def __init__(self, base_url: str = "https://sa2-p.heu.group/header/v5"):
        self.base_url = base_url

    def search_products(
        self,
        query_string: str,
        country: str = "cz",
    ) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/get_suggester_data/"
        params = {"query": query_string, "country": country}
        
        logger.debug(f"Executing Header Search request: {url} with params {params}")
        
        try:
            response = httpx.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Header Search response: {data}")
            
            products = data.get("products", {}).get("result", [])
            return [
                {
                    "id": product.get("id"),
                    "name": product.get("name"),
                    "minPrice": product.get("min_price"),
                    "maxPrice": product.get("max_price"),
                    "url": f"https:{product.get('url')}" if product.get('url', '').startswith('//') else product.get('url')
                }
                for product in products
            ]
        except Exception as e:
            logger.error(f"Header Search Error: {e}")
            raise e
