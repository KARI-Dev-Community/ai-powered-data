from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone
from typing import Optional
import os
import time
from dotenv import load_dotenv

load_dotenv()

from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL", "http://localhost:54321")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "anon-key")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="Agentic Income Stack API",
    version="0.1.0",
    description="Public data, price history, and lead endpoints.",
)

# --- Auth middleware ---

async def get_customer(x_api_key: Optional[str] = Header(None)) -> dict:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    res = supabase.table("api_customers").select("*").eq("api_key", x_api_key).eq("active", True).execute()
    if not res.data:
        raise HTTPException(status_code=403, detail="Invalid or inactive API key")
    return res.data[0]


# --- Models ---

class WatchlistItem(BaseModel):
    sku: str
    target_price: float
    user_email: str
    channel: str = "email"


class SourceRegister(BaseModel):
    source_id: str
    name: str
    url: HttpUrl
    selector_json: dict
    schema_json: dict
    schedule_cron: str = "0 3 * * *"


# --- Health ---

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


# --- #36 Data Moat ---

@app.get("/v1/sources")
def list_sources():
    data = supabase.table("sources").select("*").execute()
    return {"sources": data.data}


@app.post("/v1/sources")
def register_source(body: SourceRegister):
    supabase.table("sources").insert(body.dict()).execute()
    return {"status": "registered", "source_id": body.source_id}


@app.get("/v1/timeseries/{source_id}")
def timeseries(source_id: str, entity_id: Optional[str] = None, limit: int = 100):
    query = supabase.table("snapshots").select("*").eq("source_id", source_id).order("scraped_at", desc=True).limit(limit)
    snapshots = query.execute().data
    return {"source_id": source_id, "snapshots": snapshots}


@app.get("/v1/entity/{source_id}/{entity_id}")
def entity_latest(source_id: str, entity_id: str):
    res = supabase.table("entity_latest").select("*").eq("source_id", source_id).eq("entity_id", entity_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Entity not found")
    return res.data[0]


# --- #27 Price Tracking ---

@app.get("/v1/price-history/{sku}")
def price_history(sku: str, limit: int = 50):
    res = (
        supabase.table("price_history")
        .select("*")
        .eq("sku", sku)
        .order("scraped_at", desc=True)
        .limit(limit)
        .execute()
    )
    return {"sku": sku, "history": res.data}


@app.post("/v1/watchlist")
def add_watchlist(item: WatchlistItem, customer: dict = None):
    # In production, link to customer_id
    supabase.table("alert_subscriptions").insert(
        {
            "sku": item.sku,
            "user_email": item.user_email,
            "target_price": item.target_price,
            "channel": item.channel,
        }
    ).execute()
    return {"status": "subscribed", "sku": item.sku}


# --- #11 Public Data API ---

@app.get("/v1/datasets/{dataset_name}/entities")
def list_entities(dataset_name: str, request: Request, customer: dict = None):
    # Rate limit check
    key = customer["api_key"] if customer else None
    if key:
        usage_res = supabase.table("api_usage").select("requests").eq("customer_id", customer["customer_id"]).gte("created_at", datetime.now(timezone.utc).date().isoformat()).execute()
        used = sum(row["requests"] for row in usage_res.data)
        if used >= customer["rate_limit"]:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        supabase.table("api_usage").insert({"customer_id": customer["customer_id"], "endpoint": f"/v1/datasets/{dataset_name}/entities"}).execute()

    # Demo data for first dataset
    if dataset_name == "google-maps-hvac-kl":
        res = supabase.table("entity_latest").select("*").eq("source_id", "google-maps-hvac-kuala-lumpur").limit(100).execute()
        return {"dataset": dataset_name, "data": res.data, "meta": {"count": len(res.data)}}

    raise HTTPException(status_code=404, detail="Dataset not found")


# --- #17 Leads ---

@app.get("/v1/leads")
def list_leads(vertical: Optional[str] = None, min_score: int = 0, limit: int = 50):
    query = supabase.table("prospects").select("*").gte("score", min_score).order("score", desc=True).limit(limit)
    if vertical:
        query = query.eq("vertical", vertical)
    res = query.execute()
    return {"leads": res.data}


# --- #30 Reviews ---

@app.get("/v1/reviews/{client_id}")
def client_reviews(client_id: str, status: Optional[str] = None, limit: int = 50):
    query = supabase.table("reviews").select("*").eq("client_id", client_id).order("posted_at", desc=True).limit(limit)
    if status:
        query = query.eq("status", status)
    res = query.execute()
    return {"client_id": client_id, "reviews": res.data}


# --- #36 Data Moat Anomalies ---

@app.get("/v1/anomalies/{source_id}")
def list_anomalies(source_id: str, limit: int = 50):
    res = (
        supabase.table("anomaly_reports")
        .select("*")
        .eq("source_id", source_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return {"source_id": source_id, "anomalies": res.data}
