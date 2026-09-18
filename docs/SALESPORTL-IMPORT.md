# SalesPortl Import Guide (Static Skill Collection)

This repository ships a static skill library. It does **not** ship an MCP server or API connector.

Exact import steps depend on the SalesPortl workspace and the connected agent harness UI/file format.

## Generic import flow
1. Clone/download this repo.
2. Select a minimal subset of `skills/` for the target agent role.
3. Import folders/files through your harness skill-import mechanism.
4. Confirm imported skill metadata (name, description, tags, version).
5. Test with a low-risk prompt using draft-only output.

## Admin checklist to confirm before go-live
- [ ] Which workspace receives the skill collection: `[SalesPortl workspace/link]`
- [ ] Accepted skill file format and frontmatter requirements
- [ ] How related skills are linked/routed in that workspace
- [ ] Which roles can load/edit skills (rep, manager, affiliate, operator)
- [ ] Approval policy for external actions (send/publish/spend/change)
- [ ] Approved brand claims and prohibited claims loaded from brand context
- [ ] Privacy policy for client data handling and storage
- [ ] Review cadence owner/date for context refresh

## Recommended starter pack (token-efficient)
- `skills/core/agency-router/SKILL.md`
- plus 2–3 specialist skills for the current workflow

## What this repository intentionally does not provide
- No API endpoint setup
- No API keys
- No HTTP or MCP server
- No executable installers
