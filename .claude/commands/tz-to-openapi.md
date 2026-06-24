# TZ → OpenAPI

Convert a technical specification file into OpenAPI 3.0.3.

## CRITICAL: Fidelity rules

**Do NOT invent anything. Do NOT lose anything from the original TZ.**

- You are a **transcriber**, not an API designer
- Every output item must trace back to a specific TZ section
- Gaps in TZ → `TODO: not specified in TZ` — never guess
- Before finishing: **Coverage Audit** — walk through original TZ and verify 100% accounted for
- OpenAPI paths/fields must match TZ naming exactly (don't "RESTify" if TZ uses different paths)

Read `AGENTS.md` section «Правила полноты».

## Tooling

**Только Python.** Не запускай ruby, npm, npx, yq и прочие CLI для валидации или проверки yaml.

## Steps (execute in order)

1. Read `AGENTS.md` (including fidelity rules)
2. Identify TZ file from user message (`@input/...`)
3. If input is `.docx`: `python scripts/docx-to-md.py "path"`
4. If input is `.pdf`: `python scripts/pdf-to-md.py "path"`
5. Set `{basename}` = filename without extension
6. **Read the FULL original TZ file** — this is the source of truth

7. **Analyze** as `tz-analyst` (`.claude/agents/tz-analyst.md`):
   - `templates/tz-extraction-checklist.md`
   - Write `output/{basename}-analysis.md`
   - **Must include Coverage Audit section**
   - Re-read TZ and fix any missed items

8. **Generate OpenAPI** as `openapi-architect` (`.claude/agents/openapi-architect.md`):
   - Read analysis + original TZ again
   - `templates/openapi-base.yaml` — минимальный каркас (`info` + `paths`), без `components`
   - Write `output/{basename}-openapi.yaml`
   - **Must NOT add anything not in analysis/TZ**
   - Run OpenAPI Coverage Audit (в ответе пользователю, не через внешние CLI)

9. **Final report** to user (Russian):
   - Output file paths
   - Coverage Audit summary: how many TZ items ✅ / TODO / missed
   - Explicit: «Добавлено от себя: нет» (or list and remove)
   - List all TODOs needing analyst input


Respond in Russian.
