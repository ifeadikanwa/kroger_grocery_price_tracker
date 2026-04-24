# middle man - providing functions for the ui to fulfill user interactions

from data.database import Database
from data.kroger_api import KrogerAPI
from domain import models


class GroceryService:

    def __init__(self):
        # initialize db instance
        self.db = Database()
        
        #initialize kroger api
        self.kroger_api = KrogerAPI()
        
    def add_grocery_item(self, name):
        return self.db.insert_grocery_item(name=name)

    def get_grocery_items(self):
        rows = self.db.get_grocery_items()

        # if there no data in db, return empty list
        if not rows:
            return []

        #if there is data in db, convert it to groceryItem
        grocery_items = [
            models.GroceryItem(item_id=row[0], name=row[1]) for row in rows
        ]

        return grocery_items
    
    def delete_grocery_item(self, item_id):
        self.db.delete_grocery_item(item_id)
        
    def search_products(self, query: str):
        return self.kroger_api.search_products(query=query)
    
    def track_product(self, item_id: int, product):
        self.db.insert_product(product)
        return self.db.insert_tracked_product(
            item_id=item_id,
            product_id=product.product_id,
        )
        
    def get_tracked_products_for_item(self, item_id: int):
        rows = self.db.get_tracked_products_for_item(item_id)

        return [
            {
                "tracked_product_id": row[0],
                "product_id": row[1],
                "name": row[2],
                "brand": row[3],
                "size": row[4],
                "regular_price": row[5],
                "promo_price": row[6],
            }
            for row in rows
        ]


    def remove_tracked_product(self, tracked_product_id: int):
        self.db.remove_tracked_product(tracked_product_id)
