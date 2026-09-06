-- Core tables for the agentic income stack
-- Migrations should be idempotent and additive only.

-- Data sources: every scrape target is registered here
CREATE TABLE IF NOT EXISTS sources (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    selector_json JSONB NOT NULL,
    schema_json JSONB NOT NULL,
    schedule_cron TEXT NOT NULL DEFAULT '0 3 * * *',
    status TEXT NOT NULL DEFAULT 'active', -- active, paused, dead
    last_scraped_at TIMESTAMPTZ,
    last_error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Append-only snapshots: never UPDATE or DELETE
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    records JSONB NOT NULL,
    record_count INT NOT NULL,
    schema_version TEXT NOT NULL DEFAULT 'v1',
    provenance JSONB NOT NULL DEFAULT '{}'::jsonb,
    UNIQUE (source_id, scraped_at)
);

-- Index for time-series queries
CREATE INDEX IF NOT EXISTS idx_snapshots_source_time
    ON snapshots (source_id, scraped_at DESC);

-- Entity deduplication / latest state per entity
CREATE TABLE IF NOT EXISTS entity_latest (
    source_id TEXT NOT NULL,
    entity_id TEXT NOT NULL,
    data JSONB NOT NULL,
    first_seen TIMESTAMPTZ NOT NULL DEFAULT now(),
    last_seen TIMESTAMPTZ NOT NULL DEFAULT now(),
    snapshot_id BIGINT NOT NULL REFERENCES snapshots(snapshot_id),
    PRIMARY KEY (source_id, entity_id)
);

-- Derived metrics computed on write
CREATE TABLE IF NOT EXISTS metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    entity_id TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    window_start TIMESTAMPTZ NOT NULL,
    window_end TIMESTAMPTZ NOT NULL,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_id, entity_id, metric_name, window_start)
);

-- API customers / keys for #11
CREATE TABLE IF NOT EXISTS api_customers (
    customer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    company TEXT,
    tier TEXT NOT NULL DEFAULT 'free', -- free, pro, enterprise
    api_key TEXT UNIQUE NOT NULL DEFAULT encode(gen_random_bytes(24), 'hex'),
    rate_limit INT NOT NULL DEFAULT 100,
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- API usage log for billing + rate limiting
CREATE TABLE IF NOT EXISTS api_usage (
    usage_id BIGSERIAL PRIMARY KEY,
    customer_id UUID NOT NULL REFERENCES api_customers(customer_id),
    endpoint TEXT NOT NULL,
    requests INT NOT NULL DEFAULT 1,
    billed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_api_usage_customer_time
    ON api_usage (customer_id, created_at DESC);

-- Prospects for #17 lead-gen
CREATE TABLE IF NOT EXISTS prospects (
    prospect_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name TEXT NOT NULL,
    owner_name TEXT,
    email TEXT,
    phone TEXT,
    website TEXT,
    city TEXT NOT NULL,
    vertical TEXT NOT NULL,
    review_score DOUBLE PRECISION,
    review_count INT,
    tech_stack JSONB DEFAULT '{}'::jsonb,
    problem_signals JSONB DEFAULT '[]'::jsonb,
    score INT NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'new', -- new, contacted, replied, pilot, client, dead
    enrichment_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_prospects_vertical_score
    ON prospects (vertical, score DESC);

-- Outreach sequences for #17
CREATE TABLE IF NOT EXISTS outreach (
    outreach_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prospect_id UUID NOT NULL REFERENCES prospects(prospect_id),
    sequence_step INT NOT NULL DEFAULT 1,
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    personalization_score INT NOT NULL DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'draft', -- draft, sent, opened, replied, bounced, unsubscribed
    sent_at TIMESTAMPTZ,
    replied_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Reviews for #30
CREATE TABLE IF NOT EXISTS reviews (
    review_id TEXT NOT NULL,
    client_id TEXT NOT NULL,
    platform TEXT NOT NULL,
    rating INT NOT NULL,
    text TEXT,
    author TEXT,
    posted_at TIMESTAMPTZ NOT NULL,
    status TEXT NOT NULL DEFAULT 'ingested', -- ingested, drafted, approved, posted, escalated, dead
    response_draft TEXT,
    response_posted_at TIMESTAMPTZ,
    sentiment TEXT,
    priority TEXT DEFAULT 'normal', -- normal, high, p0
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (review_id, client_id, platform)
);

-- Price history for #27 (mirrors #36 snapshots but denormalized for alert queries)
CREATE TABLE IF NOT EXISTS price_history (
    price_history_id BIGSERIAL PRIMARY KEY,
    sku TEXT NOT NULL,
    source_url TEXT NOT NULL,
    price DOUBLE PRECISION NOT NULL,
    currency TEXT NOT NULL DEFAULT 'MYR',
    in_stock BOOLEAN NOT NULL DEFAULT true,
    scraped_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (sku, source_url, scraped_at)
);

CREATE INDEX IF NOT EXISTS idx_price_history_sku_time
    ON price_history (sku, scraped_at DESC);

-- Alert subscriptions for #27
CREATE TABLE IF NOT EXISTS alert_subscriptions (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku TEXT NOT NULL,
    user_email TEXT NOT NULL,
    target_price DOUBLE PRECISION NOT NULL,
    channel TEXT NOT NULL DEFAULT 'email', -- email, sms
    active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Alert log for #27
CREATE TABLE IF NOT EXISTS alert_log (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID NOT NULL REFERENCES alert_subscriptions(subscription_id),
    sku TEXT NOT NULL,
    old_price DOUBLE PRECISION NOT NULL,
    new_price DOUBLE PRECISION NOT NULL,
    discount_pct DOUBLE PRECISION NOT NULL,
    channel TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Row Level Security (enable per table as needed)
-- ALTER TABLE prospects ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE reviews ENABLE ROW LEVEL SECURITY;

-- Anomaly reports from LLM judge for #36
CREATE TABLE IF NOT EXISTS anomaly_reports (
    anomaly_id BIGSERIAL PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES sources(source_id),
    snapshot_id BIGINT NOT NULL REFERENCES snapshots(snapshot_id),
    is_anomaly BOOLEAN NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,
    reasons JSONB NOT NULL DEFAULT '[]'::jsonb,
    suggested_action TEXT,
    model TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_anomaly_reports_source_time
    ON anomaly_reports (source_id, created_at DESC);
