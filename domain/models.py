# data models
from dataclasses import dataclass


@dataclass
class GroceryItem:
    name: str
    item_id: int | None = None


@dataclass
class Product:
    product_id: str
    name: str
    brand: str | None = None
    size: str | None = None
    regular_price: float | None = None
    promo_price: float | None = None
    


@dataclass
class TrackedProduct:
    item_id: int
    product_id: str
    is_active: int
    tracked_product_id: int | None = None


@dataclass
class PriceHistory:
    product_id: str
    captured_at: float
    regular_price: float
    promo_price: float
    price_history_id: int | None = None
