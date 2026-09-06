# Kindle Self-Publishing Agent

## Metrics

| Metric | Value |
|--------|-------|
| Risk | Low-Medium |
| Capital | RM 0–RM 100 (cover art + ads) |
| Success Probability | 30–50% per title (genre-dependent) |
| Time to First RM | 24–72h after KDP publish |
| Skills Needed | Copywriting, KDP metadata, basic design taste |

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Manuscript Gen | Anthropic Claude | Strong long-form coherence; enforces reading-level constraints |
| Cover Art | DALL-E 3 / SDXL | Genre-appropriate covers; SDXL cheaper for batch |
| Manuscript Render | Pandoc | EPUB + PDF from Markdown; KDP-accepted format |
| Validation | Kindle Previewer CLI | Pre-flight check before upload |
| Ads | Amazon Ads API | KDP-native attribution; low-funnel retargeting |
| Data Ledger | Supabase | Track ASIN, sales, royalties per title |
| Topic Validation | Google Trends + KDP Search | Identify rising keywords before writing |

## Execution Plan

| Week | Task |
|------|------|
| 1 | Build topic-validating prompt for 36-data-moat-history-agent. Pull 10 candidate topics. |
| 2 | Test manuscript generation + pandoc render on 3 nonfiction niches. Validate via Kindle Previewer. |
| 3 | Build cover-generation prompt library per genre. Human-blind test 5 covers. |
| 4 | Build KDP metadata prompt (title, subtitle, 7 keywords, 2 categories, blurb). |
| 5 | Set up Amazon Ads account + API credentials. Write campaign prompt templates. |
| 6 | Publish first 5 books via KDP (manual upload). Record time from idea to live. |
| 7–8 | Automate metadata + cover selection. Add plagiarism gate against internal corpus. |
| 9–12 | Scale to 2–4 books/week. Monthly kill list: delist <5 copies in 60 days. |

## Unit Economics

| Item | Cost | Revenue |
|------|------|---------|
| Manuscript generation | RM 0.50 | — |
| Cover art (DALL-E 3) | RM 0.10–RM 0.30 | — |
| Amazon Ads spend | RM 50–RM 200/mo | — |
| KDP royalty (70% tier) | — | ~65% of list price |
| Nonfiction list price | — | RM 14.90–RM 24.90 |
| Low-content list price | — | RM 9.90–RM 14.90 |
| Holding cost (none) | RM 0 | — |

**Break-even:** 5–10 nonfiction sales/month per title covers ad spend.

## Known Failure Modes

| Failure | Mitigation |
|---------|-----------|
| KDP rejects manuscript format | Validate via Kindle Previewer CLI before upload; re-render with pandoc fixes |
| Cover rejected (trademark or content) | Trademark pre-check; regenerate with sanitised prompt |
| Amazon Ads account suspended | Manual review request; pause all campaigns; surface to operator |
| Topic competition too high | 36-data-moat-history-agent validation gate; flag and rotate |
| Plagiarism flag from KDP | Check against internal corpus (top 1000 KDP titles); rewrite flagged passages |
| Low discoverability (no sales in 60d) | Delist and reallocate keywords to winner; rotate topic faster |

## First Milestone

**Day 14:** First nonfiction book from idea to live on KDP with 7 keywords and Amazon Ads campaign active. Target: by Day 30, first book sells ≥5 copies and earns ≥RM 50 royalties.
