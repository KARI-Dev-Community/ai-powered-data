# 21. Online course generator

## Metrics

| Metric | Value |
| --- | --- |
| Risk | Medium |
| Capital Required | RM400–RM2,000 |
| Success Probability | Low–Medium (40–65% with validated topic + 50+ students in month 3) |
| Time to First RM | 4–8 months |
| Skills Needed | Instructional design, video/slide creation, Teachable/Thinkific setup, copywriting, ElevenLabs voice tuning |

## Stack

| Layer | Choice | Why |
| --- | --- | --- |
| Outline / scripts | Anthropic Claude Sonnet 4 | Strongest at structured long-form, learning objectives |
| Slide deck | python-pptx + master template + SDXL art | Editable, brandable, batch-generatable |
| Voiceover | ElevenLabs (SSML-tuned) | Natural, multilingual, pronunciation hints |
| Video | ffmpeg 6 + movit + whisper large-v3 | Slide-to-video, captions, motion scenes |
| Platform | Teachable (creators) / Thinkific (cohort) | Each has its audience; both have REST API |
| Checkout fallback | Stripe CLI + API | Direct checkout if platform fees >3% |
| Email nurture | 16-email-marketing-agent | Post-launch 4-week drip |
| Catalog | Supabase postgrest | Course catalog, sales ledger, completion tracking |

## Execution Plan

| Week | Step |
| --- | --- |
| 1 | Pick niche + 1 course topic; set up Teachable/Thinkific school; build outline manually |
| 2 | SME review of outline; lock module → lesson → objective tree; approve script sample |
| 3 | Build agent pipeline: outline → script → slides → voiceover → video → quiz |
| 4 | Record first 3 lessons as seed content; ship $49 mini-course to beta list |
| 5 | Add quiz generation + completion-tracking email sequence; integrate 16-email-marketing-agent |
| 6–10 | Launch 1 new course per month; validate price ladder ($49 → $199 → $499); A/B test thumbnails |
| 11–12 | Add 36-data-moat-history-agent for course-topic selection + competitor gap analysis |

## Unit Economics

| Item | Cost (RM) | Revenue (RM) |
| --- | --- |
| Claude Sonnet outline + scripts + quizzes | 35/course | – |
| ElevenLabs voiceover (10 lessons) | 20/course | – |
| SDXL slide art | 8/course | – |
| ffmpeg render + storage | 7/course | – |
| Supabase catalog + API | 5/course | – |
| Platform API calls | 5/course | – |
| **Variable cost per course** | **80/course** | – |
| Teachable Pro / Thinkific | 100–200/mo | – |
| Avg sale price | – | 100–500 |
| Completion-driven upsell | – | 50–200 |
| Break-even | 5–10 sales per month | – |
| Gross margin | – | ~70–80% |

## Known Failure Modes

| Failure | Mitigation |
| --- | --- |
| SME sign-off missing before render | Block render pipeline until sme_reviewed=true on all scripts; operator escalation after 48h |
| Quizzes too easy (high completion, low retention) | Mix 30% distractors; 1 application-level case-study per module; A/B test difficulty per cohort |
| Low completion rate post-launch | Add 1 progress email per module; surface drop-off analytics; unlock micro-certificate at 80% completion |
| Platform upload format rejection | Validate against Teachable/Thinkific spec pre-export; re-encode to H.264 1080p; surface platform error code |
| AI voiceover sounds robotic | SSML pauses, sentence rewrite for natural cadence, pronunciation hints; ElevenLabs voice clone fallback |

## First Milestone

**Day 90:** First course live, 50 paid students, RM5,000 revenue, second course in production with SME-approved outline.
