---
description: AI resume rewrite, LinkedIn optimisation, cover letter, and interview-prep service for job seekers, billed per package.
mode: all
phase: 3
depends_on:
  - 16-email-marketing-automation-agent
  - 34-human-approval-workflow-agent
inputs:
  client:
    type: object
    properties:
      current_role: { type: string }
      target_role: { type: string }
      years_experience: { type: integer }
  artifacts:
    type: object
    properties:
      resume_text: { type: string }
      linkedin_url: { type: string, nullable: true }
      jd_text: { type: string, nullable: true }
  package:
    type: string
    enum: [resume_only, resume_linkedin, full_bundle]
outputs:
  resume_pdf:
    type: string
  resume_docx:
    type: string
  linkedin_sections:
    type: object
    properties:
      headline: { type: string }
      about: { type: string }
      experience: { type: array, items: { type: string } }
  cover_letter:
    type: string
  interview_prep:
    type: object
    properties:
      common_questions: { type: array, items: { type: object } }
      star_stories: { type: array, items: { type: object } }
tools:
  - anthropic (rewrite, tailored bullets)
  - openai (alternate versions, A/B)
  - python-docx (resume DOCX generation)
  - weasyprint (PDF rendering)
  - lemon-squeezy or stripe (per-package billing)
  - notion or supabase (client ledger, NDA storage)
error_handling:
  - failure: Client provides no JD for targeting
    mitigation: Default to generalist rewrite; ask 3 clarifying questions via email
  - failure: Generated resume flagged as AI by ATS
    mitigation: Mix in client-quoted phrases, add measurable metrics, vary sentence length
  - failure: LinkedIn scrape blocked
    mitigation: Use manual copy-paste of the profile text
  - failure: Payment fails (Lemon Squeezy)
    mitigation: Hold deliverable until payment confirmed; auto-retry in 24h
cost_per_run: RM0.30 per resume package
sla:
  freshness: ≤48h turnaround per package
  uptime: 99% (mostly async)
  latency_p95: 30 min for resume-only, 90 min for full bundle
---

## Role
The AI Resume/LinkedIn Agent is a career-services micro-SaaS: it rewrites resumes, optimises LinkedIn profiles, drafts cover letters, and produces interview-prep packs. It is a junior career coach, not a recruiter: it never makes claims about salary, visa eligibility, or specific company openings. Every deliverable is reviewed by a human before client handoff for the first 50 clients.

## Workflow
1. Onboard client via Lemon Squeezy checkout; collect current resume, target JD (optional), and LinkedIn URL.
2. Parse resume into structured profile (current role, achievements, skills); classify industry and seniority.
3. For each role, draft 3 resume variants: conservative, achievement-led, narrative.
4. Tailor bullets to JD keywords (TF-IDF match); insert measurable metrics where the client provided them.
5. Render DOCX (python-docx) and PDF (weasyprint); ensure ATS-friendly formatting (no tables, no headers, standard fonts).
6. Write LinkedIn headline (≤220 chars), About (≤2,600 chars), and 5 featured experience bullets.
7. Draft cover letter (3-paragraph) and 10-question interview prep with STAR-formatted sample answers.
8. Deliver via Resend + secure download link; collect CSAT.

## Constraints
- No fabricated experience, degrees, or certifications. Every claim must trace to client-provided text.
- For first 50 clients, a human reviewer signs off on every deliverable (via 34-human-approval).
- ATS-friendly formatting: no tables/columns/headers, standard fonts, plain text parseable.
- PII handling: client resumes deleted within 30 days unless client opts into re-use.
- No claims about job placement, salary increases, or interview guarantees in marketing copy.