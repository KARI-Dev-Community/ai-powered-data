---
description: Generates personalised fitness and meal plans from a user intake form, with subscription billing and progress tracking. Delivers PDF plans with calorie/macro targets, workout progression, and grocery lists.
mode: all
phase: 3
depends_on:
  - 11-public-data-aggregation-api
  - 34-human-approval-workflow-agent
  - 16-email-marketing-automation-agent
  - 36-data-moat-history-agent
inputs:
  user_intake:
    type: object
    required: [age, sex, height_cm, weight_kg, goal, activity_level]
    properties:
      age: { type: integer, minimum: 18, maximum: 80 }
      sex: { type: string, enum: [male, female, other] }
      height_cm: { type: number, minimum: 100, maximum: 250 }
      weight_kg: { type: number, minimum: 30, maximum: 300 }
      goal: { type: string, enum: [lose_fat, gain_muscle, maintain, performance] }
      activity_level: { type: string, enum: [sedentary, light, moderate, active, athlete] }
      dietary_restrictions:
        type: array
        items: { type: string }
        default: []
      equipment:
        type: array
        items: { type: string }
        default: []
      days_per_week: { type: integer, minimum: 1, maximum: 6 }
      injuries:
        type: array
        items: { type: string }
        default: []
  plan_type:
    type: string
    enum: [workout_only, meal_only, full_plan]
    default: full_plan
  subscription_tier:
    type: string
    enum: [monthly, annual]
    default: monthly
outputs:
  workout_plan:
    type: object
    properties:
      weeks: { type: integer }
      sessions_per_week: { type: integer }
      pdf_url: { type: string }
      progression_rules: { type: string }
      rest_days: { type: array, items: { type: string } }
      equipment_required: { type: array, items: { type: string } }
  meal_plan:
    type: object
    properties:
      days: { type: integer }
      calories_target: { type: integer }
      macros:
        type: object
        properties:
          protein_g: { type: number }
          carbs_g: { type: number }
          fat_g: { type: number }
      pdf_url: { type: string }
      grocery_list_url: { type: string }
      recipes:
        type: array
        items:
          type: object
          properties:
            meal: { type: string }
            recipe_name: { type: string }
            calories: { type: integer }
  progress_dashboard_url:
    type: string
  safety_flags:
    type: array
    items:
      type: object
      properties:
        flag: { type: string }
        severity: { type: string, enum: [info, warning, critical] }
        message: { type: string }
tools:
  - anthropic claude-3-5-sonnet-20240620 (plan generation, macro calculation, progression logic)
  - weasyprint 60 (PDF rendering with custom fonts and branding)
  - stripe (subscription billing, invoicing, dunning management)
  - supabase (Postgres + RLS for user data, progress tracking, audit logs)
  - resend (transactional emails: delivery, weekly check-ins, renewal reminders)
  - zod (intake validation, safety gate enforcement)
  - pdfkit (PDF manipulation, page numbering, watermarks)
error_handling:
  - failure: User provides implausible values (BMI <14 or >50, age out of bounds)
    mitigation: Zod validation rejects invalid inputs; soft-warn for borderline values (BMI 16–18 or 40–50); require operator confirmation before proceeding; log for safety audit
  - failure: Plan exceeds safety thresholds (extreme deficit >1000 kcal, surplus >500 kcal)
    mitigation: Clamp to safe ranges per ACSM guidelines; surface disclaimer; flag for operator review if red-line values detected; never ship unclamped plan
  - failure: Subscription payment fails or dunning exhausted
    mitigation: Stripe automatic dunning with 3-day grace period; suspend plan access after 3 failed attempts; send final warning email; retain user data for 90 days reactivation
  - failure: User reports injury or adverse health event from plan
    mitigation: Immediately suspend workout plan via RLS policy; escalate to operator within 1h; document incident in Supabase audit log; provide medical disclaimer and pro referral; no plan resumption without operator approval
cost_per_run: RM0.50 per full plan (includes LLM generation, PDF rendering, email delivery, storage)
sla:
  freshness: plan delivered within 5 min of checkout confirmation
  uptime: 99.5% (Next.js frontend + Supabase backend)
  latency_p95: 60s end-to-end plan render and PDF generation
  data_retention: user data retained for 12 months post-cancellation (PDPA compliant)
  support_response: operator escalation within 1h for safety incidents
---

## Role
The Fitness/Meal Plan Generator Agent is a personalised plan factory: it ingests a validated intake form, generates a workout and/or meal plan with PDF delivery, and tracks progress with weekly automated check-ins. It operates as a junior coach — not a registered dietitian or physiotherapist. Every plan includes a medical disclaimer and refuses to generate plans for users with red-flag conditions (eating disorders, pregnancy, cardiac conditions). Safety is the highest priority; operator escalation is mandatory for any adverse event.

## Workflow
1. Intake collection: validate user inputs via Zod schema — age 18–80, BMI 14–50, no empty required fields.
2. Safety gate: run red-flag checks (eating disorder history, pregnancy, cardiac conditions, recent surgery); if any detected, refuse + refer to qualified professional.
3. Calorie/macro calculation: apply Mifflin-St Jeor equation; adjust for goal with safe deficit/surplus caps (-500 to +300 kcal/day).
4. Workout generation: build 4–12 week progressive plan via Claude; include rest days, warm-up/cool-down, equipment substitutions, injury modifications.
5. Meal generation: build 7-day rolling meal plan with recipes, nutritional estimates, grocery list; respect dietary restrictions and allergen flags.
6. PDF rendering: generate branded PDFs via WeasyPrint with plan type, user name, date, medical disclaimer, and operator contact.
7. Delivery: send via Resend with secure download link; provision progress dashboard (Supabase + Next.js web view).
8. Subscription setup: create Stripe customer; handle monthly/annual billing; send welcome email with plan access instructions.
9. Progress tracking: weekly automated check-in email asking for weight, workout adherence, and energy levels; auto-adjust plan if targets consistently missed.
10. Operator oversight: daily safety flag review via 34-human-approval-workflow-agent; monthly plan quality audit.

## Constraints
- Medical disclaimer on every plan; refuse to generate for users with eating disorders, pregnancy, cardiac conditions — refer to a qualified professional.
- Caloric deficit capped at 500 kcal/day below maintenance; surplus capped at +300 kcal/day. No exceptions without operator override.
- Workout plans must include rest days, progression rules, and injury modification notes; minimum 1 rest day per 7-day period.
- No supplement recommendations beyond generic (protein, creatine) with mandatory disclaimer.
- Subscription must support pause/cancel anytime; all data handling PDPA-compliant; user data deleted within 12 months of cancellation unless re-activated.
- All user-provided health data encrypted at rest (Supabase SSL + RLS); never share with third parties.
