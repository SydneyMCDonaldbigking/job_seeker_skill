---
name: managing-job-pipeline-marvis
description: Manage a local job-application pipeline stored as Marvis-compatible Markdown tasks. Use when Codex needs to check job IDs or URLs for duplicates, record discovered or skipped roles, move an application through applying/submitted/interview/offer/rejected/withdrawn states, attach resume or confirmation details, migrate legacy job_application_profile.json applications, or validate the local application history before screening or applying.
---

# Managing Job Pipeline in Marvis

Treat Marvis task notes as the application system of record. Keep private profile facts, site mappings, accounts, and resume assets in `job_application_profile.json`; do not write new entries to its legacy `applications` array.

Read `references/schema.md` before creating or editing a record. Run `scripts/job_pipeline.py` for all deterministic reads and writes instead of assembling frontmatter manually.

## Locate the vault

Use the active workspace as `--vault` when it contains `Marvis/Job Search/_project.md`. Otherwise, locate the user's explicitly named Obsidian vault. Never search unrelated personal folders broadly.

## Required workflow

1. Before ranking, tailoring, or opening an application, run `find` with the exact portal job ID and canonical URL.
2. Interpret matches using the duplicate rules in `references/schema.md`.
3. Record a promising unhandled job with `add`; record a deliberate rejection with `add --status skipped` or a record JSON whose `status` is `skipped`.
4. Move a live form to `applying` only after the correct portal job and account are verified.
5. Move a job to `submitted` only after visible portal confirmation or a success email. Include the confirmation in notes or the task body.
6. Run `validate` after migrations or batch updates.

## Commands

Use the bundled script with the available Python runtime:

```text
python scripts/job_pipeline.py --vault <vault> find --job-id <id> --url <url>
python scripts/job_pipeline.py --vault <vault> add --record-json <path> [--status <status>]
python scripts/job_pipeline.py --vault <vault> transition --job-id <id> --status <status> --note <text>
python scripts/job_pipeline.py --vault <vault> organize
python scripts/job_pipeline.py --vault <vault> validate
python scripts/job_pipeline.py --vault <vault> validate --legacy-profile <job_application_profile.json>
python scripts/job_pipeline.py --vault <vault> migrate --legacy-profile <job_application_profile.json>
```

`find` exits with code 1 when no exact match exists; treat `[]` as safe to continue. Use `validate --legacy-profile` only during migration parity checks, because new Marvis-only records intentionally make legacy counts diverge.

Use `--dry-run` on migration first. Migration is idempotent and must not overwrite an existing task unless the user explicitly requests a repair.

## Safety

- Never delete legacy records during migration.
- Never write passwords, tokens, visa identifiers, addresses, or other sensitive profile data into Marvis tasks.
- Preserve unknown frontmatter fields and the existing Markdown body on transition.
- Keep terminal states (`submitted`, `offer`, `skipped`, `rejected`, `withdrawn`) in the Marvis `archive/` folder. Keep active states in `tasks/`.
- Treat company/title similarity as duplicate risk only; exact portal job ID or canonical URL establishes identity.
- Do not mark `submitted` from an application review page, draft, generated cover letter, or browser navigation alone.
