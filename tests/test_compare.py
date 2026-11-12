from pricecompare.compare import best_offer, compare, rank
from pricecompare.models import Offer
from pricecompare.shops import SampleShop, load_sample_shops
from pricecompare.shops.sample import matches


def offer(shop, price, shipping=0.0, in_stock=True):
    return Offer(shop, "Thing", "test", price, shipping, in_stock, "")


def test_total_price_includes_shipping():
    assert offer("A", 10.0, 2.5).total_price == 12.5


def test_rank_puts_in_stock_and_cheapest_first():
    offers = [offer("A", 10, in_stock=False), offer("B", 30), offer("C", 20)]
    assert [o.shop for o in rank(offers)] == ["C", "B", "A"]


def test_best_offer_ignores_out_of_stock():
    offers = [offer("A", 5, in_stock=False), offer("B", 15)]
    assert best_offer(offers).shop == "B"


def test_best_offer_none_when_nothing_in_stock():
    assert best_offer([offer("A", 5, in_stock=False)]) is None


def test_matches_needs_every_word():
    assert matches("wireless HEADPHONES", "Wireless Headphones X200")
    assert not matches("wireless mouse", "Wireless Headphones X200")
    assert not matches("   ", "anything")


def test_sample_shop_search():
    shop = SampleShop("Test", [{"product": "Red Mug", "category": "kitchen", "price": 5}])
    assert len(shop.search("mug")) == 1
    assert len(shop.search("kitchen")) == 1
    assert shop.search("plate") == []


def test_compare_with_sample_data():
    result = compare(load_sample_shops(), "headphones")
    assert result["count"] == 3
    # 74.00 + 9.99 = 83.99 vs 79.99 + 4.95 = 84.94 vs 82.00 + 0 = 82.00
    assert result["best"]["shop"] == "QuickShop"
    assert result["best"]["total_price"] == 82.0