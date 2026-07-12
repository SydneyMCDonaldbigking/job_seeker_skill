# Application Records

Use this reference whenever screening can lead to a live application.

## Local Data Sources

Load `managing-job-pipeline-marvis` and use `Marvis/Job Search/tasks/*.md` plus
`Marvis/Job Search/archive/*.md` as the application system of record. Keep
`job_application_profile.json` for private profile facts, site mappings,
account overrides, and resume assets.
Treat its legacy `applications` array and Markdown logs as read-only migration
references after the Marvis project exists.

## Before Shortlisting

1. Run the bundled Marvis pipeline `find` command with the exact portal job ID
   and canonical URL.
2. Treat a match with status `applying`, `submitted`, `interview`, `offer`,
   `rejected`, or `withdrawn` as already handled.
3. Exclude handled jobs from the primary shortlist unless the user asks to
   inspect duplicates.
4. Treat `shortlisted` as an existing candidate and hide `skipped` from normal
   results unless reconsideration was requested.
5. If only company and role look similar, label duplicate risk rather than
   assuming identity.

## Status Records

Create or transition one Marvis task with `managing-job-pipeline-marvis`.
Do not assemble frontmatter manually and do not append to the legacy JSON
applications array. Record Gmail source account or message context when known.

Move a task to `submitted` only after portal or email confirmation. For manual
submissions confirmed in portal history, record `manual_user_submission` and
use unknown artifact values when the resume or cover letter was not inspected.

## Backend Status Sync

For a backend-discovered job with a scheduled-scan key, also update
`POST /api/v1/scheduled-scan/jobs/status` using a backend-supported value such
as `saved`, `ignored`, or `applied`.
