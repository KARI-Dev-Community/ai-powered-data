# Outreach Templates — Phase 2 Lead Engine (#17, #30)

Executable copy for the roadmap's critical path. Send counts and rules first, templates after.

All amounts in RM.

---

## Sending rules (non-negotiable)

| Rule | Value |
|---|---|
| Daily volume (new prospects) | 20 emails + 5 video audits/day max |
| Sending domain | Dedicated domain, NOT your personal one; warm 2–3 weeks before volume |
| Follow-up cap | 3 touches total, then stop |
| Compliance | Real name + business address in footer, working unsubscribe, no misleading subject lines (CAN-SPAM / GDPR / Malaysia PDPA) |
| Personalization floor | Every email references a specific observed problem — if you can't find one, skip the prospect |

## Prospect scoring (who gets contacted)

Score each scraped business; only email 4–5 stars:

| Signal | Points |
|---|---|
| Unanswered Google reviews in last 90 days | +2 |
| No chat widget / no booking system | +2 |
| Website slow (>3s load) or no mobile site | +1 |
| Recently opened (<6 months) | +1 |
| 4.0–4.5 rating (falling, but salvageable) | +1 |

---

## Sequence A — #30 Review Response (entry offer)

### Email 1 — Day 0 (the observed problem)

> **Subject:** 3 unanswered reviews at {{Business Name}}
>
> Hi {{Owner Name}},
>
> I was looking at {{Business Name}} on Google and noticed {{N}} reviews from the last few months with no response — including {{specific example, e.g., "a 2-star from March about wait times"}}.
>
> I run a small service that responds to every customer review for local businesses — in the business owner's voice, within 24 hours, flagging anything sensitive to you first.
>
> Mind if I show you what it would look like? I'll reply to your last 3 reviews free so you can judge the quality.
>
> {{Your Name}}
> {{Business address}} · [Unsubscribe link]

### Email 2 — Day 3 (proof, if no reply)

> **Subject:** Re: 3 unanswered reviews at {{Business Name}}
>
> Hi {{Owner Name}} — went ahead and drafted responses to your 3 most recent reviews (attached). No strings; use them if you like them.
>
> If you want this handled permanently: RM{{X}}/month, cancel anytime, you approve anything sensitive before it posts.
>
> {{Your Name}}

### Email 3 — Day 7 (the close attempt, short)

> **Subject:** Last one from me
>
> {{Owner Name}} — should I keep handling your review responses or leave it with you? One-line reply is fine either way.
>
> {{Your Name}}

## Sequence B — #17 Lead-gen / audit (higher-value targets)

### Email 1 — the audit offer

> **Subject:** Quick question about {{Business Name}}'s booking flow
>
> Hi {{Owner Name}},
>
> I tried to book {{service}} on your site — {{specific friction: "no online booking, and the contact form has no phone field"}}. Most customers give up after ~30 seconds of friction; you're likely losing {{N}} jobs/month to it.
>
> I build small automation tools for {{niche}} businesses. Can I send you a 2-minute video showing exactly where enquiries are leaking and what fixing it looks like? Free, no pitch attached.
>
> {{Your Name}}

### The Loom audit script (2 minutes, not 5)

1. **0:00–0:15** — Their site/Google profile on screen. "This is {{Business Name}} as a customer sees it."
2. **0:15–0:45** — Show ONE leak: the unanswered reviews, the dead contact form, the missing booking. Name the cost: "at your price point, 3 lost enquiries/month ≈ RM{{Y}}."
3. **0:45–1:30** — Show the fix working (your demo agent handling their exact scenario).
4. **1:30–2:00** — The offer: "I'll run this for you free for 30 days. If it earns its keep, RM{{X}}/month. If not, you keep the setup."

### Pilot → retainer conversion (day 25 of free pilot)

> **Subject:** Your 30-day results
>
> Hi {{Owner Name}} — 30 days in. This month I:
> - Responded to {{N}} reviews / handled {{N}} enquiries (avg. response {{T}} minutes)
> - Flagged {{N}} issues to you
> - {{Revenue proxy if known: "3 bookings came through the new flow"}}
>
> Continuing is RM{{X}}/month. If you'd rather take the scripts and run it yourself, that's fine too — want me to write up the process?

## Objection quick-replies

| Objection | Response |
|---|---|
| "I already have someone doing this" | "Great — then this costs you nothing to compare. I'll do month 1 free; keep whoever's better." |
| "Too expensive" | "One recovered job/month covers it. If it doesn't in 60 days, cancel — the risk is mine." |
| "Is this a bot?" | "Partly — the drafts are automated, you approve anything sensitive. That's why it's RM{{X}} and not RM{{Y×4}} for a full-time person." |
| "Send me info" | "Better: 10 minutes on a call, I'll show you on your own listing. {{2 time slots}}." |

## Pricing ladder (log actuals in TRACKER.md)

| Product | Cold quote | Floor |
|---|---|---|
| #30 review response | RM800/mo | RM400/mo |
| #17 leads (per qualified lead) | RM40 | RM20 |
| #7 chatbot | RM1,200/mo | RM600/mo |
| Pilot | Free, 30 days, capped scope | Never exceed 30 days |

## Weekly discipline

- Mon–Fri: 20 new prospects + 5 audits/day (~45 min with the agent doing scraping/drafting)
- Fri: update `TRACKER.md` — emails sent, replies, pilots opened/closed
- Every reply = a call or a pilot, never a price negotiation over email
