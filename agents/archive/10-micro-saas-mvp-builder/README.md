# Micro-SaaS MVP Builder

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Medium-High |
| Capital | RM 0–RM 500 (deploy + LLM) |
| Success Probability | 15–30% (depends on idea quality) |
| Time to First RM | 2–8 weeks (first paying user) |
| Skills Needed | Full-stack dev, product sense, Stripe integration |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | Next.js 14 App Router | SEO, SSR, built-in API routes; largest ecosystem |
| Backend | FastAPI (optionally Hono) | Async Python; easy auth + DB wiring |
| DB / Auth | Supabase | Managed Postgres + Auth + RLS in one; free tier viable |
| Billing | Stripe + Lemon Squeezy | Stripe for subscriptions; Lemon Squeezy for simpler onboarding |
| Deploy | Vercel (primary) / Render / Fly | Vercel for Next.js; Render/Fly as fallback |
| Code Gen | Anthropic Claude (Opus/Sonnet) | Strongest for multi-file scaffolding |
| Smoke Tests | Playwright | End-to-end signup + checkout |
| CI | GitHub Actions (implied via repo) | Build + lint + smoke on every push |

## Execution Plan

| Week | Task |
|------|------|
| 1 | Build idea validator: pull prior MVPs from 36-data-moat-history-agent. Define scaffold template (file-tree contract). |
| 2 | Implement Claude scaffold prompt with strict file boundaries. Test on 3 known-good ideas. |
| 3 | Add CI loop: sandbox → pnpm build → iterate on error → max 3 retries. |
| 4 | Wire Supabase (auth + DB schema + RLS). Add sign-up smoke test. |
| 5 | Wire Stripe billing (subscriptions + webhook). Add checkout smoke test. |
| 6 | Add core-feature smoke test. Deploy to Vercel. Validate p95 latency target. |
| 7–8 | Test 5 edge-case ideas (bad prompt, large schema, Stripe webhook edge cases). Log failures. |
| 9–12 | Package as reusable agent. Document operator runbook. Target 1 deploy/week. |

## Unit Economics

| Item | Cost | Revenue |
|------|------|---------|
| LLM generation (scaffold) | RM 3–RM 8 | — |
| Vercel deploy minutes | RM 0–RM 2 | — |
| Supabase free tier | RM 0 | — |
| Stripe fees (per transaction) | — | 2.9% + RM 0.10 |
| Lemon Squeezy fees | — | 5% + RM 0.25 |
| Human review (first 10 MVPs) | RM 200–RM 500 | — |

**Break-even:** First MVP with 10 subscribers at RM 30/mo = RM 300/mo gross.

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| Generated code does not build | Self-debug loop (max 3 retries); surface persistent errors to operator |
| Stripe webhook signature fails | Re-fetch endpoint secret with exponential backoff; alert operator |
| Vercel deploy quota exceeded | Auto-fallback to Render or Fly; log migration cost |
| Repo secrets leak to git | Git-secrets + GitHub secret scanning on every push; rotate leaked keys immediately |
| LLM hallucinates API surface | Pin to exact library versions in scaffold template; smoke-test enforces correctness |
| Deploy URL public before approval | Operator approval gate; agent never auto-announces |

## First Milestone

**Day 7:** First end-to-end scaffold → deploy → smoke test completed for a known-good idea. Target: by Day 30, 5 MVPs deployed with 1 smoke test each passing.
