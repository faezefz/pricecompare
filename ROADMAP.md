# Roadmap

Planned work. Each item is also an open GitHub issue.

## v0.2 – Better search
- [ ] Filters: category, max price, only in stock
- [ ] Sort options: total price, price, shop name
- [ ] Fuzzy search (small typos still find the product)
- [ ] Group the same product from different shops (by EAN barcode)

## v0.3 – Real shops (official sources only, no scraping)
- [ ] Adapter for the bol.com Marketing Catalog API (affiliate account)
- [ ] Adapter for affiliate product feeds (Daisycon / TradeTracker)
- [ ] Read API keys from .env, config file to choose active shops
- [ ] Search shops in parallel (async) with timeouts
- [ ] Cache results for a few minutes

## v0.4 – Price history
- [ ] Store prices over time in SQLite
- [ ] Simple price-history chart per product
- [ ] Price-drop alert (local, no user accounts)

## v0.5 – Nicer interface
- [ ] Better design and mobile layout
- [ ] Product images and links to the shop

## Quality and deployment
- [ ] More tests (API edge cases, adapters)
- [ ] GitHub Actions: run tests on every push
- [ ] ruff (style) and mypy (types)
- [ ] Dockerfile and docker-compose
- [ ] Deploy a public demo