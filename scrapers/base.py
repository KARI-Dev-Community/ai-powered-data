from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import time


class RetailerScraper:
    """Base class for retailer price scrapers."""

    def __init__(self, source_id: str, selectors: dict, currency: str = "MYR"):
        self.source_id = source_id
        self.selectors = selectors
        self.currency = currency

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((PlaywrightTimeout, Exception)),
    )
    def fetch(self, url: str) -> dict:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)

            result = {
                "url": url,
                "title": page.title(),
                "price": None,
                "in_stock": False,
                "currency": self.currency,
            }

            price_sel = self.selectors.get("price")
            if price_sel:
                try:
                    price_text = page.locator(price_sel).first.inner_text(timeout=5000)
                    result["price"] = float(
                        "".join(c for c in price_text if c.isdigit() or c == ".")
                    )
                    result["in_stock"] = True
                except Exception:
                    result["in_stock"] = False

            stock_sel = self.selectors.get("stock")
            if stock_sel:
                try:
                    stock_text = page.locator(stock_sel).first.inner_text(timeout=3000).lower()
                    result["in_stock"] = "out of stock" not in stock_text and "unavailable" not in stock_text
                except Exception:
                    pass

            browser.close()
            return result
