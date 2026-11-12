"""A shop adapter that reads made-up products from a JSON file.

Used for development and tests. The shops and prices are fictional.
"""

import json
from pathlib import Path

from ..models import Offer

DEFAULT_DATA = Path(__file__).resolve().parents[2] / "data" / "sample_shops.json"


def matches(query: str, text: str) -> bool:
    """True if every word of the query appears in the text (any case)."""
    words = query.lower().split()
    text = text.lower()
    return bool(words) and all(word in text for word in words)


class SampleShop:
    def __init__(self, name: str, products: list[dict]):
        self.name = name
        self._products = products

    def search(self, query: str) -> list[Offer]:
        offers = []
        for p in self._products:
            if matches(query, f"{p['product']} {p['category']}"):
                offers.append(
                    Offer(
                        shop=self.name,
                        product=p["product"],
                        category=p["category"],
                        price=float(p["price"]),
                        shipping=float(p.get("shipping", 0)),
                        in_stock=bool(p.get("in_stock", True)),
                        url=p.get("url", ""),
                    )
                )
        return offers


def load_sample_shops(path: Path = DEFAULT_DATA) -> list[SampleShop]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [SampleShop(shop["name"], shop["products"]) for shop in data["shops"]]