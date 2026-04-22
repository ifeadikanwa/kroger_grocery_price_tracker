# data models
from dataclasses import dataclass

@dataclass
class GroceryItem:
    item_id: int = 0
    name: str
    
@dataclass
class Product:
    product_id: str = ""
    name: str
    brand: str
    size: str
    
@dataclass
class TrackedProduct:
    tracked_product_id: int = 0
    item_id: int
    product_id: str
    is_active: int

@dataclass
class PriceHistory:
    price_history_id: int = 0
    product_id: str
    captured_at: float
    regular_price: float
    promo_price: float
        
    