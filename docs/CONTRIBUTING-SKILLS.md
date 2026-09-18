# Contributing Skills

## Skill authoring standard
Each skill lives in its own folder with `SKILL.md` and must include:
- Frontmatter: `name`, `description`, `version`, `tags`
- Headings: Purpose, Use when, Required inputs, Safety/authority, Workflow, Output format, Quality checks, Related skills
- Related skills by exact skill name

## Authoring process
1. Start from an existing skill with similar scope.
2. Keep instructions concise and modular.
3. Require explicit user confirmation before any external action.
4. Use placeholders for unverified company-specific facts.
5. Add/update the entry in `catalog.json`.

## Review checklist
- [ ] No fabricated claims, prices, policies, or integrations
- [ ] Draft-only defaults where external action is possible
- [ ] Web-research safety text included where relevant
- [ ] Output format is structured and reusable
- [ ] Related skills listed
- [ ] `python3 scripts/validate_catalog.py` passes

## Versioning
- Patch (`0.1.x`): wording or minor safety/format improvements
- Minor (`0.x.0`): new skills or major workflow changes

## Attribution boundary
Use upstream repositories only for inspiration of scope/workflow patterns. Do not copy branded content, generated outputs, or scripts.
