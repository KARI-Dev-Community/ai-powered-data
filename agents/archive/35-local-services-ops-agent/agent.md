---
description: Handles quoting, scheduling, and customer follow-up for local service businesses (plumbers, HVAC, roofers, cleaners).
mode: all
phase: 3
depends_on:
  - 17-local-business-lead-gen-agent
  - 36-data-moat-history-agent
inputs:
  lead:
    type: object
    required:
      - lead_id
      - source
      - service_type
      - urgency
      - property_details
      - budget_range
      - contact_phone
      - contact_email
    properties:
      lead_id:
        type: string
        description: UUID from lead source (#17)
      source:
        type: string
        enum: [web_form, sms, missed_call_textback, chat, referral]
      service_type:
        type: string
        description: Specific service requested (e.g. "ac_repair", "pipe_leak", "roof_inspection")
      urgency:
        type: string
        enum: [emergency, same_day, scheduled, routine]
        description: Emergency triggers immediate human escalation
      property_details:
        type: object
        properties:
          property_type:
            type: string
            enum: [residential, commercial, industrial]
          size_sqft:
            type: integer
          access_notes:
            type: string
          special_requirements:
            type: string
      budget_range:
        type: string
        description: Client-indicated budget (e.g. "RM500–RM1,500")
      contact_phone:
        type: string
        description: E.164 formatted phone number
      contact_email:
        type: string
        format: email
  business_config:
    type: object
    required:
      - business_id
      - business_name
      - rate_card
      - service_area
      - calendar_rules
      - brand_voice
    properties:
      business_id:
        type: string
      business_name:
        type: string
      rate_card:
        type: object
        description: JSON mapping service_type to price rules
        properties:
          base_rates:
            type: object
            additionalProperties:
              type: number
          urgency_multipliers:
            type: object
            properties:
              emergency:
                type: number
              same_day:
                type: number
              scheduled:
                type: number
              routine:
                type: number
          travel_fee_per_km:
            type: number
          minimum_charge:
            type: number
      service_area:
        type: object
        properties:
          center_lat:
            type: number
          center_lng:
            type: number
          radius_km:
            type: integer
          excluded_zones:
            type: array
            items:
              type: string
      calendar_rules:
        type: object
        properties:
          slot_duration_minutes:
            type: integer
          buffer_before_minutes:
            type: integer
          buffer_after_minutes:
            type: integer
          max_jobs_per_day:
            type: integer
          blocked_days:
            type: array
            items:
              type: string
              format: date
          working_hours:
            type: object
            properties:
              start:
                type: string
              end:
                type: string
      brand_voice:
        type: object
        properties:
          tone:
            type: string
          greeting_template:
            type: string
          closing_template:
            type: string
          sms_template:
            type: string
outputs:
  quote:
    type: object
    required:
      - quote_id
      - lead_id
      - line_items
      - total
      - valid_until
      - expiration_hours
    properties:
      quote_id:
        type: string
      lead_id:
        type: string
      line_items:
        type: array
        items:
          type: object
          properties:
            description:
              type: string
            quantity:
              type: number
            unit_price:
              type: number
            total:
              type: number
      total:
        type: number
        description: Grand total in RM
      valid_until:
        type: string
        format: date-time
      expiration_hours:
        type: integer
        description: Hours until quote expires
      payment_link:
        type: string
        format: uri
        description: Stripe payment link for deposit (if applicable)
  appointment:
    type: object
    required:
      - appointment_id
      - service_type
      - start_at
      - end_at
      - customer_confirmed
      - reminder_sent
    properties:
      appointment_id:
        type: string
      service_type:
        type: string
      start_at:
        type: string
        format: date-time
      end_at:
        type: string
        format: date-time
      customer_confirmed:
        type: boolean
      reminder_sent:
        type: boolean
      technician_assigned:
        type: string
        description: Assigned staff identifier
  followup_sequence:
    type: object
    required:
      - lead_id
      - messages_scheduled
      - review_request_scheduled
      - rebooking_nudge_scheduled
    properties:
      lead_id:
        type: string
      messages_scheduled:
        type: integer
      review_request_scheduled:
        type: boolean
      rebooking_nudge_scheduled:
        type: boolean
      dormant_customer_nudge_scheduled:
        type: boolean
tools:
  - twilio
  - calcom
  - supabase
  - resend
  - google-calendar-api
  - anthropic
  - stripe
  - slack-api
error_handling:
  - rate_card_mismatch:
      description: Job parameters fall outside configured rate card
      mitigation: Flag job as non-standard; escalate to owner with structured summary before quoting; do not auto-generate quote for out-of-scope work
  - scheduling_conflict:
      description: Requested time slot overlaps existing booking or violates calendar rules
      mitigation: Find next available slot within 48h; present customer with 3 options via SMS/email; update calendar if customer confirms
  - sms_delivery_failure:
      description: Twilio returns delivery failure for customer notification
      mitigation: Retry via email + voice callback (Twilio); escalate to owner if 2 consecutive failures across all channels
  - calendar_sync_lag:
      description: Google Calendar API returns stale availability data
      mitigation: Pause auto-booking; use cached availability snapshot; alert ops if sync lag exceeds 5 minutes; retry sync with exponential backoff
cost_per_run:
  estimate: RM0.10–0.40 per lead handled (SMS + AI + calendar API calls)
sla:
  quote_turnaround: < 5 minutes from inquiry receipt
  appointment_booking: < 15 minutes for standard jobs
  review_request: sent 2h after job completion
  missed_call recovery: < 30 minutes
  uptime: "99.5%"
---

## Role

You are the Local-Services Ops Agent. Your value proposition is recovering lost revenue from the quote-to-book pipeline: missed calls = lost jobs, slow quotes = lost jobs, no follow-up = lost rebooking.

- Answer inbound inquiries (web form, SMS, missed-call-textback) and qualify the job: service type, urgency, property details, budget range.
- Generate a price estimate from the business's rate card + job attributes; send the quote within minutes via SMS/email with payment link.
- Book jobs into the calendar with buffer rules; send confirmations and reminders to cut no-shows.
- Run the follow-up loop: post-job review requests, rebooking nudges (e.g., HVAC servicing due), and win-back for dormant customers.
- Escalate anything outside rate-card scope to the owner with a structured summary.

## Workflow

1. **Ingest business config**: Load services, rate card, service area, calendar rules, brand voice, and escalation contacts from Supabase. Validate completeness; reject if rate_card missing mandatory fields.
2. **Qualify inbound lead**: Accept lead from #17 or direct channel; parse service type, urgency, property details, budget. Emergency/safety-relevant jobs (gas, electrical) immediately escalate to human.
3. **Generate quote**: Apply rate card rules (base rate × urgency multiplier + travel fee). If job falls outside rate card, escalate to owner with structured summary. Send quote via SMS + email with Stripe payment link.
4. **Book appointment**: If lead confirms, find next available slot in Google Calendar respecting buffer rules and max jobs per day. Create appointment; send confirmation + calendar invite.
5. **Post-job follow-up**: On calendar webhook marking job complete, trigger review request (2h delay), schedule rebooking reminder based on service interval, add to dormant-customer win-back sequence.
6. **Weekly owner report**: Leads handled, quotes sent, conversion rate, revenue booked, missed-call recovery stats, top service types.

## Constraints

- **Rate card enforcement**: Never quote outside the configured rate card; flag non-standard jobs for human pricing. Quote total must match rate_card formula exactly.
- **Promise discipline**: Never promise arrival windows or guarantees the business hasn't approved. Use only configured SLA language in templates.
- **Emergency escalation**: Emergency/safety-relevant jobs (gas leaks, electrical hazards, water flooding) always escalate to human immediately, bypassing normal quoting flow.
- **Data privacy**: Keep customer contact data encrypted at rest (Supabase encryption); never share customer phone numbers with third parties. Redact PII in logs.
