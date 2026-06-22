# Application Records

Use this reference whenever screening can lead to a live application.

## Default Local Data Source

Read `job_application_profile.json` in the active workspace when it exists.
For manual SEEK work, its `applications` array is the local source of truth.
Legacy Markdown logs are read-only migration references when JSON exists.

## Before Shortlisting

1. Read `applications`.
2. Treat a job as already handled when its exact portal job ID or exact URL
   matches a record whose status is `submitted`.
3. Exclude already-submitted jobs from the primary shortlist unless the user
   asks to inspect duplicates.
4. If only company and role look similar, keep the result but label duplicate
   risk rather than assuming it is the same job.

## Status Records

When a screening decision needs to be recorded, append an application entry
with a status such as `shortlisted`, `skipped`, `duplicate`, `started`,
`submitted`, or `failed`. Do not rewrite historical entries unless requested.

For Gmail-sourced SEEK work, include the source account or message context when
known. If the user manually submitted a job and SEEK Applied jobs confirms it,
record `manual_user_submission`; use unknown resume/cover-letter values when
those artifacts were not inspected.

## Backend Status Sync

For jobs with a scheduled-scan backend key, also update:

```http
POST /api/v1/scheduled-scan/jobs/status
```

Use backend-supported values such as `saved`, `ignored`, or `applied`.
