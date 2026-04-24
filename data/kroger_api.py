# kroger api operations
import os
import base64
import requests
from dotenv import load_dotenv

from domain.models import Product

load_dotenv()

class KrogerAPI:

    def __init__(self):
        
        self.client_id = os.getenv("KROGER_CLIENT_ID")
        self.client_secret = os.getenv("KROGER_CLIENT_SECRET")
        self.location_id = os.getenv("KROGER_LOCATION_ID")

        self.token_url = "https://api.kroger.com/v1/connect/oauth2/token"
        self.products_url = "https://api.kroger.com/v1/products"

    # login to kroger API and get our access token
    def get_access_token(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "product.compact",
        }

        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()

        token_data = response.json()
        return token_data["access_token"]

    def search_products(self, query: str) -> list[Product]:
        # get access token
        token = self.get_access_token()

        # build request
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }

        params = {
            "filter.term": query,
            # "filter.locationId": self.location_id,
            "filter.limit": 10,
        }

        # make request
        response = requests.get(self.products_url, headers=headers, params=params)
        response.raise_for_status()

        # get data from the response
        data = response.json()

        products = []

        # got through the raw json and extract what we need
        for raw_product in data.get("data", []):
            product_id = raw_product.get("productId")
            name = raw_product.get("description")
            brand = raw_product.get("brand")

            items = raw_product.get("items", [])
            size = None

            if items:
                size = items[0].get("size")

            if product_id and name:
                products.append(
                    Product(
                        product_id=product_id,
                        name=name,
                        brand=brand,
                        size=size,
                    )
                )
                
        print(f"Fetched {len(products)} products for query: {query}")
        
        return products
