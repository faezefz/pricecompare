"""Shop adapters. Each adapter knows how to search one shop."""

from .base import ShopAdapter
from .sample import SampleShop, load_sample_shops

__all__ = ["ShopAdapter", "SampleShop", "load_sample_shops"]