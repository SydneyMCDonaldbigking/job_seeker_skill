# Application Records

Use this reference whenever a tailored package enters a live application.

## Local Data Sources

Load `managing-job-pipeline-marvis` and use `Marvis/Job Search/tasks/*.md` plus
`Marvis/Job Search/archive/*.md` as the application system of record. Keep
`job_application_profile.json` for private reusable answers, portal mappings,
account overrides, and resume assets. Treat its legacy applications array and Markdown logs as read-only
migration references after the Marvis project exists.

Never store passwords, one-time codes, tax IDs, identity documents, or secret
tokens in application data.

## Before Applying

1. Run the bundled Marvis pipeline `find` command with the exact job ID and URL.
2. Stop for a match in `applying`, `submitted`, `interview`, `offer`,
   `rejected`, or `withdrawn` unless the user explicitly requests recovery.
3. Summarize `failed` attempts before retrying.
4. For SEEK, read `sites.seek_au.accounts` from the private JSON profile for
   account-specific overrides.

## During Application

Use the JSON `profile` for stable facts and the active site's `form_mappings`
for visible choices. Ask before using mappings marked `requires_confirmation`
unless the current conversation confirms them or authorizes the batch policy.
Transition the Marvis task to `applying` only after the portal job and account
are verified.

## After Submission

Transition the task to `submitted` only after the portal or a success email
clearly confirms submission. Record the account, resume filename, cover-letter
note, and exact confirmation. Store explicitly confirmed application answers
in the task body; do not add new entries to the legacy JSON applications array.

For manual submissions confirmed in portal history, record
`manual_user_submission` and keep uninspected artifacts explicitly unknown.

If the job has a backend scheduled-scan key, also mark backend status `applied`.
