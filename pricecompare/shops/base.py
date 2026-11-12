"""The interface every shop adapter must follow.

To add a new shop (for example one with an official API), write a class
with a `name` and a `search(query)` method that returns a list of Offers.
"""

from typing import Protocol

from ..models import Offer


class ShopAdapter(Protocol):
    name: str

    def search(self, query: str) -> list[Offer]:
        ...