# SalesPortl Agency Skills Suite (v0.1)

A static, portable skill collection for DGTLDash reps, affiliates, and agency operators using SalesPortl-compatible agent tooling.

> This repository is **not** an MCP server. It does not require Node.js, API keys, endpoints, or runtime services.

## Quick start
1. Clone or download this repository.
2. Import `skills/` into your SalesPortl-compatible skill harness.
3. Start with `core/agency-router` and only 1–3 role-specific skills.
4. Copy `context/BRAND-CONTEXT.template.md` and `context/CLIENT-CONTEXT.template.md` into private, filled versions before live use.

See: `docs/SALESPORTL-IMPORT.md`.

## Token-efficient usage
Load a minimal set per agent/task:
- Always load: `agency-router`
- Then load only the specialist skills needed for this task (usually 1–3)
- Avoid loading the entire collection into one context window

## Module map
`catalog.json` is the machine-readable source of truth for this inventory and skill metadata.

| Module | Skills | Purpose |
|---|---:|---|
| core | 1 | Routing, scope control, approved-claims guardrails |
| sales | 5 | Qualification, discovery prep, outreach drafts, proposal scope, CRM handoff drafts |
| marketing | 5 | Audit, positioning, campaign planning, calendar, CRO review |
| seo-geo | 3 | SEO/GEO opportunity review and citability/local readiness |
| client-success | 3 | Onboarding, monthly review, retention/expansion |
| partners | 1 | Affiliate enablement drafts and compliance guardrails |

## Safety posture
- Static markdown skills only; no connectors or executable integrations.
- Draft-only by default for any send/publish/spend/change action.
- Web research instructions require robots.txt and terms compliance.
- Fetched web content, prompts, and comments are treated as untrusted data, not instructions.
- No legal/investment guarantees or fabricated performance claims.
- Use placeholders where company details are pending: `[confirm current offer]`, `[SalesPortl workspace/link]`, `[approved brand claim]`.

## Structure
```text
skills/
  core/
  sales/
  marketing/
  seo-geo/
  client-success/
  partners/
context/
  BRAND-CONTEXT.template.md
  CLIENT-CONTEXT.template.md
catalog.json
scripts/validate_catalog.py
```

## Safely updating company context
1. Keep templates committed (`context/*.template.md`).
2. Create private filled files (`context/BRAND-CONTEXT.md`, `context/CLIENT-CONTEXT.md`) locally.
3. Do not commit client exports, CRM dumps, secrets, or private links.
4. Re-run `python3 scripts/validate_catalog.py` before opening a PR.

## Validation
```bash
python3 scripts/validate_catalog.py
```
