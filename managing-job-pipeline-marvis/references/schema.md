# Marvis Job Record Schema

## Layout

```text
Marvis/
  Job Search/
    _project.md
    tasks/
    archive/
    logs/
    milestones/
    skills/
```

Marvis 0.2.4 requires `kind: task`, a project wikilink, and a status. It accepts custom fields and custom status IDs.

## Statuses

- `discovered`: captured but not assessed
- `screening`: assessment in progress
- `shortlisted`: worth applying
- `applying`: form started; do not start a second application
- `submitted`: portal or email confirmed submission
- `interview`: employer interaction or interview underway
- `offer`: offer received
- `skipped`: deliberately not pursued
- `rejected`: employer rejected the application
- `withdrawn`: user withdrew
- `failed`: application attempt failed and may need recovery

Treat `applying`, `submitted`, `interview`, `offer`, `rejected`, and `withdrawn` as already handled for duplicate prevention. Treat `shortlisted` as an existing candidate. Hide `skipped` from ordinary shortlists unless reconsideration was requested.

Store terminal states (`submitted`, `offer`, `skipped`, `rejected`, and `withdrawn`) in `archive/` with `archived: true`. Store active and recoverable states in `tasks/` with `archived: false`.

## Frontmatter

```yaml
---
kind: task
project: "[[Job Search]]"
status: submitted
priority: high
created: 2026-07-11
tags: [job, seek_au]
portal: seek_au
portal_job_id: "12345678"
company: "Example Pty Ltd"
role: "Junior Software Engineer"
job_url: "https://au.seek.com/job/12345678"
source: gmail_seek_recommendations
source_account_email: "account@example.com"
source_message_id: "message-id"
application_account: "account@example.com"
resume_filename: "resume.pdf"
cover_letter: "Tailored inline cover letter"
confirmation_page: true
confirmation_email: true
---
```

Keep long notes, employer questions, cover-letter text, and confirmation details in the Markdown body. Keep atomic searchable values in frontmatter.

## Identity

Use `(portal, portal_job_id)` as the primary identity and canonical URL as the secondary identity. Name files `<portal>-<job_id>.md`. When no portal ID exists, use a stable URL hash.
