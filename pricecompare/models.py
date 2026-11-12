"""Data models."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Offer:
    """One shop selling one product at one price."""

    shop: str
    product: str
    category: str
    price: float  # in euros
    shipping: float  # in euros
    in_stock: bool
    url: str

    @property
    def total_price(self) -> float:
        return round(self.price + self.shipping, 2)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["total_price"] = self.total_price
        return data