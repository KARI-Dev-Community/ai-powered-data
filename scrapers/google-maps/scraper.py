from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import httpx
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SCRAPERS_DIR = Path(__file__).resolve().parent.parent
for _p in (str(PROJECT_ROOT), str(SCRAPERS_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from supabase import create_client, Client
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from llm_anomaly_detector import judge_anomaly


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SOURCE_ID = os.getenv("GMAPS_SOURCE_ID", "google-maps-hvac-kuala-lumpur")
VERTICAL = os.getenv("GMAPS_VERTICAL", "hvac")
CITY = os.getenv("GMAPS_CITY", "Kuala Lumpur")
MAX_RESULTS = int(os.getenv("GMAPS_MAX_RESULTS", "200"))

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def ensure_source():
    """Register the source in Supabase if it doesn't exist."""
    existing = (
        supabase.table("sources")
        .select("source_id")
        .eq("source_id", SOURCE_ID)
        .execute()
    )
    if not existing.data:
        supabase.table("sources").insert(
            {
                "source_id": SOURCE_ID,
                "name": f"Google Maps {VERTICAL} {CITY}",
                "url": "https://maps.google.com",
                "selector_json": {
                    "results_selector": "div[role='feed'] > div",
                    "name_selector": "div[class*='qBF1Pd']",
                    "rating_selector": "span[class*='MW4etd']",
                    "reviews_selector": "span[class*='UY7F9']",
                },
                "schema_json": {
                    "business_name": "string",
                    "rating": "float",
                    "review_count": "int",
                    "address": "string",
                    "phone": "string",
                    "website": "string",
                },
                "schedule_cron": "0 3 * * *",
                "status": "active",
            }
        ).execute()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((PlaywrightTimeout, httpx.HTTPError)),
)
def scrape_google_maps() -> list[dict]:
    """Scrape Google Maps for a vertical + city."""
    records = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.set_viewport_size({"width": 1280, "height": 800})

        search_url = f"https://www.google.com/maps/search/{VERTICAL}+{CITY}"
        page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(3)

        # Accept consent if present
        try:
            consent = page.locator("button:has-text('Accept all')").first
            if consent.is_visible(timeout=2000):
                consent.click()
                time.sleep(1)
        except Exception:
            pass

        # Scroll to load results
        results_selector = "div[role='feed'] > div"
        last_height = 0
        for _ in range(20):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(1.5)
            current_height = page.evaluate("document.body.scrollHeight")
            if current_height == last_height:
                break
            last_height = current_height

        result_elements = page.locator(results_selector)
        count = min(result_elements.count(), MAX_RESULTS)

        for i in range(count):
            try:
                el = result_elements.nth(i)
                name = el.locator("div[class*='qBF1Pd']").first.inner_text(timeout=2000)
            except Exception:
                name = None

            if not name:
                continue

            try:
                rating_text = el.locator("span[class*='MW4etd']").first.inner_text(timeout=1000)
                rating = float(rating_text) if rating_text else None
            except Exception:
                rating = None

            try:
                reviews_text = el.locator("span[class*='UY7F9']").first.inner_text(timeout=1000)
                review_count = int("".join(filter(str.isdigit, reviews_text))) if reviews_text else None
            except Exception:
                review_count = None

            records.append(
                {
                    "business_name": name,
                    "rating": rating,
                    "review_count": review_count,
                    "vertical": VERTICAL,
                    "city": CITY,
                    "source_url": search_url,
                }
            )

        browser.close()
    return records


def save_snapshot(records: list[dict]) -> dict:
    """Append snapshot to Supabase; never overwrite history."""
    now = datetime.now(timezone.utc).isoformat()
    provenance = {
        "source": "google-maps",
        "scraper_version": "v1",
        "vertical": VERTICAL,
        "city": CITY,
    }

    snapshot = {
        "source_id": SOURCE_ID,
        "records": records,
        "record_count": len(records),
        "provenance": provenance,
    }

    # We insert via RPC or direct table insert; using raw insert here for clarity
    # In production, use a stored procedure for atomicity
    snapshot_res = supabase.table("snapshots").insert(snapshot).execute()
    snapshot_id = snapshot_res.data[0]["snapshot_id"] if snapshot_res.data else None
    snapshot["snapshot_id"] = snapshot_id

    # Upsert into entity_latest for fast lookups
    for rec in records:
        entity_id = rec.get("business_name", "").lower().replace(" ", "-")
        supabase.table("entity_latest").upsert(
            {
                "source_id": SOURCE_ID,
                "entity_id": entity_id,
                "data": rec,
                "last_seen": now,
                "snapshot_id": snapshot_id,
            },
            on_conflict="source_id,entity_id",
        ).execute()

    return snapshot


def main():
    ensure_source()
    print(f"Scraping {VERTICAL} in {CITY} ...")
    records = scrape_google_maps()
    print(f"Scraped {len(records)} records")
    snapshot = save_snapshot(records)
    print("Snapshot saved")

    history = (
        supabase.table("snapshots")
        .select("*")
        .eq("source_id", SOURCE_ID)
        .order("scraped_at", desc=True)
        .limit(10)
        .execute()
        .data
    )

    report = judge_anomaly(SOURCE_ID, snapshot, history)
    print(f"Anomaly judge: anomaly={report.is_anomaly} confidence={report.confidence}")
    for reason in report.reasons:
        print(f"  - {reason}")

    supabase.table("anomaly_reports").insert(
        {
            "source_id": SOURCE_ID,
            "snapshot_id": snapshot.get("snapshot_id"),
            "is_anomaly": report.is_anomaly,
            "confidence": report.confidence,
            "reasons": report.reasons,
            "suggested_action": report.suggested_action,
            "model": os.getenv("KILO_MODEL", "anthropic/claude-sonnet-4.5") if os.getenv("KILO_API_KEY") else "none",
        }
    ).execute()
    print("Anomaly report saved")


if __name__ == "__main__":
    main()
