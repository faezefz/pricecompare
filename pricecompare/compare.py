"""Search all shops and rank the offers."""

from .models import Offer
from .shops import ShopAdapter


def search_all(shops: list[ShopAdapter], query: str) -> list[Offer]:
    """Ask every shop and collect all offers."""
    offers: list[Offer] = []
    for shop in shops:
        offers.extend(shop.search(query))
    return offers


def rank(offers: list[Offer]) -> list[Offer]:
    """Best first: in-stock offers before out-of-stock, then cheapest total price."""
    return sorted(offers, key=lambda o: (not o.in_stock, o.total_price, o.shop))


def best_offer(offers: list[Offer]) -> Offer | None:
    """The cheapest offer that is in stock, or None."""
    in_stock = [o for o in offers if o.in_stock]
    return rank(in_stock)[0] if in_stock else None


def compare(shops: list[ShopAdapter], query: str) -> dict:
    """Full result for one search, ready to send as JSON."""
    offers = rank(search_all(shops, query))
    best = best_offer(offers)
    return {
        "query": query,
        "count": len(offers),
        "best": best.to_dict() if best else None,
        "offers": [o.to_dict() for o in offers],
    }