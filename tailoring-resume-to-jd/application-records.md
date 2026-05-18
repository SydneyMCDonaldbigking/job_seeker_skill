# Application Records

Use this reference whenever a tailored package is used in a live application.

## Default Local Files

Prefer user-provided paths. If the user has not provided paths, use these files in
the active workspace:

- `applied_jobs_log.md` for submitted, saved, skipped, or duplicate jobs
- `application_personal_info.md` for reusable application answers

Do not store passwords, one-time codes, tax IDs, identity documents, or secret
tokens in either file.

## Before Applying

1. Read `applied_jobs_log.md` if it exists.
2. Check the target job against exact job id, exact URL, and source/company/role.
3. If it was already submitted, stop and tell the user before opening the
   application flow.
4. If it was started or failed, summarize the last note and continue only when
   the user wants to retry.

## During Application

Use `application_personal_info.md` for stable form answers, but only when the
form wording clearly matches the stored answer. If a question is ambiguous or
legally sensitive, ask the user instead of guessing.

Common sensitive fields include:

- work rights or visa restrictions
- sponsorship requirements
- years of experience
- education completion
- criminal/background checks
- equal opportunity or demographic questions
- notice period and availability

## After Submission

Append one row to `applied_jobs_log.md` only after the portal clearly confirms
submission. Include the tailored resume file, cover letter type, and any special
question answers in the notes.

Use this Markdown table shape:

```markdown
| Date | Source | Company | Role | Job ID | URL | Resume | Cover Letter | Status | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 2026-05-19 | SEEK | Example Co | Graduate AI Engineer | 12345678 | https://au.seek.com/job/12345678 | tailored-example.pdf | tailored inline cover letter | Submitted | SEEK confirmed submission. |
```

Recommended status values:

- `Started`
- `Submitted`
- `Failed`
- `Withdrawn`
- `Duplicate`

Append new rows only. Do not rewrite or delete earlier rows unless the user asks.

## Backend Status Sync

If the job came from the scheduled-scan backend and includes a backend job key,
also mark the backend status after submission:

```http
POST /api/v1/scheduled-scan/jobs/status
```

Use status `applied` when the portal confirms submission.

For manual Chrome applications without a backend job key, the Markdown log is the
source of truth.
