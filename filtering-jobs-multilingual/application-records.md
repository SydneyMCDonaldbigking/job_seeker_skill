# Application Records

Use this reference whenever screening can lead to a live application.

## Default Local Files

Prefer user-provided paths. If the user has not provided paths, use these files in
the active workspace:

- `applied_jobs_log.md` for submitted, saved, skipped, or duplicate jobs
- `application_personal_info.md` for reusable application answers

Do not store passwords, one-time codes, tax IDs, identity documents, or secret
tokens in either file.

## Before Shortlisting

1. Read `applied_jobs_log.md` if it exists.
2. Treat a job as already handled when any of these match:
   - exact portal job id
   - exact application or job URL
   - same source, company, and role title with `Submitted` status
3. Exclude already-submitted jobs from the main shortlist unless the user asks to
   inspect duplicates.
4. If the match is fuzzy, keep the job but label the duplicate risk.

## Log Table

Use this Markdown table shape for `applied_jobs_log.md`:

```markdown
| Date | Source | Company | Role | Job ID | URL | Resume | Cover Letter | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-19 | SEEK | Example Co | Graduate AI Engineer | 12345678 | https://au.seek.com/job/12345678 | tailored-example.pdf | tailored inline cover letter | Submitted | SEEK confirmed submission. |
```

Recommended status values:

- `Shortlisted`
- `Skipped`
- `Duplicate`
- `Started`
- `Submitted`
- `Failed`

Append new rows only. Do not rewrite or delete earlier rows unless the user asks.

## Backend Status Sync

If the job came from the scheduled-scan backend and includes a backend job key,
also mark the backend status after the user decides:

```http
POST /api/v1/scheduled-scan/jobs/status
```

Use status values supported by the backend, usually `saved`, `ignored`, or
`applied`.

For manual Chrome applications without a backend job key, the Markdown log is the
source of truth.
