# Application Records

Use this reference whenever a tailored package is used in a live application.

## Default Local Data Source

Prefer a user-provided path. Otherwise, read `job_application_profile.json` in
the active workspace. It is the source of truth for reusable answers, portal
settings, resume references, and application outcomes.

Legacy `application_personal_info.md` and `applied_jobs_log.md` files are
read-only migration references when JSON exists.

Do not store passwords, one-time codes, tax IDs, identity documents, or secret
tokens in application data.

## Before Applying

1. Read `applications`.
2. Treat an exact matching `job_id` or `url` with status `submitted` as already
   submitted and stop before opening the application flow.
3. If an earlier record is `started` or `failed`, summarize it and continue only
   when the user wants to retry.
4. For SEEK, read `sites.seek_au.accounts` for account-specific overrides.

## During Application

Use `profile` for stable facts and the active site's `form_mappings` for visible
portal choices. Ask before using a mapping marked `requires_confirmation` unless
the current conversation has explicitly confirmed that answer or direct-submit
batch policy.

Sensitive fields include work rights, visa restrictions, sponsorship,
experience, qualifications, medical or background checks, demographic
questions, notice period, and availability.

## After Submission

Append one application object only after the portal clearly confirms
submission. Store the site key, company, role, job ID, URL, account used,
resume filename, cover-letter note, status `submitted`, and confirmation note.
When a sensitive answer was explicitly confirmed and used, store it under
`confirmed_sensitive_answers`.

For manually submitted jobs later confirmed in a portal history page, record
`source: manual_user_submission`. If the resume or cover letter was not
inspected, store an explicit unknown value rather than guessing.

## Backend Status Sync

If the job came from the scheduled-scan backend and includes a backend job key,
also mark backend status using:

```http
POST /api/v1/scheduled-scan/jobs/status
```

Use status `applied` after portal confirmation. For manual browser applications,
the JSON application entry is the local source of truth.
