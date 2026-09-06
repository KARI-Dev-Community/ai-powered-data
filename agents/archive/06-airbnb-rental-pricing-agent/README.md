# 06-airbnb-rental-pricing-agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low–Medium (OTA dependency, PMS reliability) |
| Capital | RM200–RM600/month (PMS API, proxy scraping, SMS/email) |
| Success Probability | 70% (immediate revenue uplift for managed properties) |
| Time to First RM | 14–30 days (increased ADR or occupancy on first listing) |
| Skills Needed | Property management basics, Python, API integrations, forecasting |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Pricing Model | Prophet / StatsForecast | Demand forecasting, event-aware, easy retrain |
| Scraping | Playwright + residential proxies | Competitor rate + availability capture |
| PMS | Guesty / Hostaway API | Channel manager sync, multi-OTA push |
| Messaging | Anthropic Claude + Twilio + Resend | Guest intent classification, SMS/email escalation |
| Storage | Supabase | Booking history, message log, price audit trail |
| Scheduling | Celery + Redis | Nightly price recompute (01:00 local) |
| Events | Google Calendar API + 36-data-moat calendar | Local events, school holidays, conferences |

## Execution Plan

| Week | Steps |
|------|-------|
| 1 | Onboard listing; export last 365 days of bookings from PMS. Set up Supabase tables. Configure Playwright for competitor scrape. |
| 2 | Run first Prophet model manually; validate against last 30 days. Calibrate ±30% clamp. Test Twilio SMS escalation with mock emergency. |
| 3 | Automate nightly Celery price recompute (01:00–01:10). Test PMS push; verify no double-bookings. Enable guest message triage. |
| 4 | Deliver first daily morning digest (revenue, occupancy, ADR, response time). Calibrate message-policy escalation keywords with host. |
| 5–8 | Monitor price-drift vs competitors weekly. Introduce local events uplift from 36-data-moat calendar. Track message-response time SLA. |
| 9–12 | Add second listing. Test multi-property dashboard. Introduce dynamic min_stay based on occupancy probability. |

## Unit Economics

| Cost Item | RM/month | Revenue Item | RM/month |
|-----------|----------|--------------|----------|
| PMS API (Guesty/Hostaway) | 100–250 | ADR uplift (+10–25%) on 1 listing | 300–1,500 |
| Twilio SMS + Resend email | 50–100 | Occupancy uplift (+5–15%) | 200–1,000 |
| Playwright + proxies | 100–200 | | |
| VPS + Celery + Supabase | 80–150 | | |
| **Total** | **330–700** | **Total** | **500–2,500** |

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Airbnb API auth expires | Refresh token cron; alert via monitoring |
| PMS sync conflict (channel manager) | Last-write-wins with audit log; surface to operator |
| Guest message contains escalation keyword | Hold reply; notify host via SMS+email; log context |
| Pricing model suggests implausibly high price | Clamp to ±30% of base; surface clamp to operator |

## First Milestone

**Day 14:** Nightly price recompute live for 1 listing, first guest message auto-replied, daily digest delivered to host, and ADR uplift of ≥10% observed vs prior 30-day baseline.
