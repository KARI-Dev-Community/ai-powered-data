from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


@dataclass
class AnomalyReport:
    source_id: str
    snapshot_id: int | None
    is_anomaly: bool
    confidence: float
    reasons: list[str]
    suggested_action: str | None = None


def get_kilo_client() -> OpenAI | None:
    api_key = os.getenv("KILO_API_KEY")
    if not api_key or api_key.startswith("kilo-xxx"):
        return None
    return OpenAI(
        base_url="https://api.kilo.ai/api/gateway",
        api_key=api_key,
    )


def build_prompt(source_id: str, current: dict, historical: list[dict]) -> str:
    hist_summary = []
    for snap in historical[-5:]:
        hist_summary.append(
            {
                "scraped_at": snap.get("scraped_at"),
                "record_count": snap.get("record_count"),
                "sample_fields": list(snap.get("records", [{}])[0].keys()) if snap.get("records") else [],
            }
        )

    return f"""You are a data-quality judge for a scraping pipeline.
Source: {source_id}

Current snapshot:
- record_count: {current.get('record_count')}
- scraped_at: {current.get('scraped_at')}
- sample_record_keys: {list(current.get('records', [{}])[0].keys()) if current.get('records') else []}

Recent history:
{json.dumps(hist_summary, indent=2)}

Task:
1) Detect anomalies vs recent history: sudden record-count drop/gain, missing fields, schema drift.
2) Return JSON only with keys: is_anomaly (bool), confidence (0-1 float), reasons (list of strings), suggested_action (string or null).
3) confidence should be higher when there is clear evidence of a problem.

Return ONLY valid JSON. Do not include markdown fences, code blocks, or any text outside the JSON object.
"""


def judge_anomaly(source_id: str, current: dict, historical: list[dict]) -> AnomalyReport:
    client = get_kilo_client()

    if not client:
        return AnomalyReport(
            source_id=source_id,
            snapshot_id=current.get("snapshot_id"),
            is_anomaly=False,
            confidence=0.0,
            reasons=["No valid Kilo Gateway API key configured; anomaly detection skipped."],
            suggested_action="Configure KILO_API_KEY.",
        )

    model = os.getenv("KILO_MODEL", "anthropic/claude-sonnet-4.5")
    prompt = build_prompt(source_id, current, historical)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        text = response.choices[0].message.content or "{}"
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        data = json.loads(text)
        return AnomalyReport(
            source_id=source_id,
            snapshot_id=current.get("snapshot_id"),
            is_anomaly=bool(data.get("is_anomaly")),
            confidence=float(data.get("confidence", 0.0)),
            reasons=list(data.get("reasons", [])),
            suggested_action=data.get("suggested_action"),
        )
    except Exception as e:
        return AnomalyReport(
            source_id=source_id,
            snapshot_id=current.get("snapshot_id"),
            is_anomaly=True,
            confidence=0.6,
            reasons=[f"Kilo Gateway judge failed: {e}"],
            suggested_action="Investigate Kilo Gateway integration.",
        )
