# 16. Email marketing automation agent

## Metrics

| Risk | Capital | Success Probability | Time to First RM | Skills Needed |
| --- | --- | --- | --- | --- |
| Medium | RM400–RM2,000 | Medium | 3–6 months | Copywriting, ESP tools (Mailchimp/Klaviyo), list-building |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| ESP | ConvertKit (creators) / Klaviyo (ecom) / Brevo (budget) | Right tool per business model |
| Transactional | Resend | Dev-friendly, reliable |
| Copy | Anthropic Claude Sonnet 4 | Brand voice, A/B variants |
| Tracking | Posthog + UTM | Open/click attribution |
| Revenue | Stripe + unique discount codes | Per-campaign attribution |
| Schedule | Celery | Per-segment timing, retries |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Pick ESP, set up list, install double opt-in, physical-address footer |
| 2 | Build 3 core drips: welcome, abandoned cart, win-back |
| 3 | Connect Stripe + unique discount codes for attribution |
| 4 | First 1,000 subscribers via lead magnet (PDF, quiz, free tool) |
| 5 | Add broadcast workflow + A/B subject-line test |
| 6-10 | Compound: 5 drips, weekly broadcast, monthly re-engagement |
| 11-12 | Add 36-data-moat-history-agent for content-angle selection |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- | --- |
| ESP up to 10k subs | 100/mo | – |
| Resend transactional | 20/mo | – |
| LLM per campaign | 0.05 | – |
| Avg revenue per send (ecom) | – | 0.10–0.50 per recipient |
| Per-campaign service fee (if B2B) | – | 500–2,000/campaign |
| Break-even | ~5,000 active subscribers on ecom | – |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| ESP outage | Round-robin across 2 ESPs, queue messages |
| Open-rate collapse | Throttle frequency, refresh subject-line style |
| Spam complaints | Pause affected segment, audit content |
| List fatigue | Re-engagement campaign, sunset unengaged |

## First Milestone
Day 60: 2,000 active subscribers, 3 drips live, RM500 attributed revenue, first paid B2B client.