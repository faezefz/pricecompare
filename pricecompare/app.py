"""Web app: a search page and a JSON API.

Run with:  uvicorn pricecompare.app:app --reload
"""

from html import escape

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from .compare import compare
from .shops import load_sample_shops

app = FastAPI(title="PriceCompare", version="0.1.0")
SHOPS = load_sample_shops()

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PriceCompare</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 760px; margin: 40px auto; padding: 0 16px; }}
    form {{ display: flex; gap: 8px; }}
    input {{ flex: 1; padding: 10px; font-size: 16px; }}
    button {{ padding: 10px 18px; font-size: 16px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
    th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
    .best {{ background: #e8f7ec; padding: 12px; border-radius: 8px; margin-top: 16px; }}
    .out {{ color: #999; }}
  </style>
</head>
<body>
  <h1>PriceCompare</h1>
  <p>Search for a product and find the best shop to buy it.</p>
  <form action="/" method="get">
    <input name="q" value="{query}" placeholder="e.g. headphones, coffee maker" autofocus>
    <button type="submit">Search</button>
  </form>
  {results}
</body>
</html>"""


def render_results(result: dict) -> str:
    if not result["query"]:
        return ""
    if result["count"] == 0:
        return f"<p>No offers found for <b>{escape(result['query'])}</b>.</p>"

    parts = []
    best = result["best"]
    if best:
        parts.append(
            f'<div class="best">Best choice: <b>{escape(best["product"])}</b> at '
            f'<b>{escape(best["shop"])}</b> for <b>€{best["total_price"]:.2f}</b> '
            f"(incl. shipping)</div>"
        )
    rows = []
    for o in result["offers"]:
        css = "" if o["in_stock"] else ' class="out"'
        stock = "yes" if o["in_stock"] else "no"
        rows.append(
            f"<tr{css}><td>{escape(o['shop'])}</td><td>{escape(o['product'])}</td>"
            f"<td>€{o['price']:.2f}</td><td>€{o['shipping']:.2f}</td>"
            f"<td><b>€{o['total_price']:.2f}</b></td><td>{stock}</td></tr>"
        )
    parts.append(
        "<table><tr><th>Shop</th><th>Product</th><th>Price</th><th>Shipping</th>"
        "<th>Total</th><th>In stock</th></tr>" + "".join(rows) + "</table>"
    )
    return "".join(parts)


@app.get("/", response_class=HTMLResponse)
def home(q: str = "") -> str:
    result = compare(SHOPS, q) if q.strip() else {"query": "", "count": 0}
    return PAGE.format(query=escape(q), results=render_results(result))


@app.get("/api/search")
def api_search(q: str = Query(..., min_length=1, description="What to search for")) -> dict:
    return compare(SHOPS, q)