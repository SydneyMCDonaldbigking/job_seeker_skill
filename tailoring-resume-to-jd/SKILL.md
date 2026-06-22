---
name: tailoring-resume-to-jd
description: Use when turning a stored master resume into a JD-specific application package, especially when using preview-vs-save control, multilingual output, cover letters, PDFs, native/original resume mode, or Chrome handoff for live applications.
---

# Tailoring Resume To JD

## Overview

Use the local Job Mediator backend to turn an existing master resume into a JD-specific package. This skill covers JD upload, fit evaluation, previewing changes, persisting a tailored resume, and generating downstream artifacts.

Read `backend-api-workflows.md` when you need exact endpoint or payload details.
Read `application-records.md` before any live application step. Use
`application-profile-template.json` as the shape for the user's private local
`job_application_profile.json` file.

## When to Use

Use this skill when the user wants to:

- adapt a resume to one specific job description
- compare previewed changes before saving
- generate a final tailored resume record
- create a cover letter or outreach message from the tailored result
- export a PDF
- work in English, Chinese, or Japanese content modes

Do not use this skill for broad multi-job discovery. Use `filtering-jobs-multilingual` first, then switch here once a target JD is chosen.

## Preferred Workflow

1. Check backend health.
2. Resolve the working resume id, or upload a language-specific master resume if missing.
3. Set `content_language` for the output language the user wants.
4. Upload the JD with `POST /api/v1/jobs/upload`.
5. Run `POST /api/v1/evaluate-job` first when the user wants fit analysis before rewriting.
6. Choose tailoring mode:
   - `POST /api/v1/resumes/improve/preview` if the user wants to review before save
   - `POST /api/v1/resumes/improve` if the user wants a directly persisted tailored version
7. If preview mode was used and the user approves, call `POST /api/v1/resumes/improve/confirm`.
8. Optionally generate:
   - cover letter
   - outreach message
   - resume PDF
   - direct tailored PDF
9. For live applications, read `job_application_profile.json` and check
   `applications` before opening the form.
10. After the portal confirms submission, append an application object to
   `job_application_profile.json`.

## Native Resume Mode

When the user says to use the original/native resume, says not to modify resume
code, or says the backend is unavailable:

1. Skip backend tailoring and PDF generation.
2. Use the current available master resume from `job_application_profile.json`
   (`resume_assets.master`), or the exact resume file the user named.
3. Still draft a job-specific inline cover letter from the live JD and confirmed
   profile/resume facts.
4. Do not invent unconfirmed tools, certifications, visa facts, demographics, or
   experience.

## Decision Rule

- Use `preview` by default when the user says review, compare, inspect, tweak, or check first.
- Use direct `improve` when the user wants a ready-to-use tailored resume immediately.

## Multilingual Policy

- `en`: good default for Australian and international roles
- `zh`: use when the user wants Chinese-facing explanation or Chinese output content
- `ja`: use when tailoring a Japanese-market resume or aligning to Japanese job ads

Keep the resume language, content language, and JD language mentally separate. They often differ.

## Chrome Handoff

After a tailored resume is ready, explicitly invoke `@chrome` if the user wants to:

- compare the tailored resume against the live job page
- fill or inspect an application form
- use existing account sessions on remote recruiting sites

Before filling forms, read the user's local `job_application_profile.json` when
it exists. Use `profile` for stable facts and `sites.<site_key>` for account
overrides and portal option mappings. Use stored answers only when wording
clearly matches; any mapping marked `requires_confirmation` must be confirmed
before use unless the current conversation explicitly confirms that answer or
authorizes the batch policy.

Before submitting, check `applications` for duplicate job IDs or URLs and verify
the target account, selected resume, cover letter, and required questions on the
review page. If the user has explicitly authorized direct submission for this
batch, submit after those checks pass; otherwise obtain explicit confirmation.
After the portal confirms submission, append one application object according
to `application-records.md`.

For SEEK, the review page is mandatory because saved resume and cover-letter
state can carry over from a previous application.

Do not try to replace the user's authenticated application flow with generic browser automation.

## Output Shape

When reporting results, include:

- chosen resume id
- job id
- whether this was previewed or persisted
- top tailoring priorities
- key changed areas
- generated artifacts available
- application-record status if this entered a live portal
- whether a Chrome handoff is the next best step

## Common Mistakes

- Skipping JD upload and trying to tailor from ad hoc text only
- Saving immediately when the user actually asked to review a preview
- Forgetting to set `content_language` before generating a multilingual result
- Treating a generated cover letter as proof that the tailored resume itself was persisted
- Guessing sensitive form answers instead of reading the JSON profile or asking
- Submitting before checking the review page for a stale cover letter or wrong resume
- Forgetting to record a confirmed live submission in `applications`
