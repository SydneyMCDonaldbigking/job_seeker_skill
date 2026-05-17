---
name: tailoring-resume-to-jd
description: Use when turning a stored master resume into a JD-specific application package, especially when you need preview-vs-save control, multilingual output, cover letters, PDFs, or Chrome handoff for live applications.
---

# Tailoring Resume To JD

## Overview

Use the local Job Mediator backend to turn an existing master resume into a JD-specific package. This skill covers JD upload, fit evaluation, previewing changes, persisting a tailored resume, and generating downstream artifacts.

Read `backend-api-workflows.md` when you need exact endpoint or payload details.

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

Do not try to replace the user's authenticated application flow with generic browser automation.

## Output Shape

When reporting results, include:

- chosen resume id
- job id
- whether this was previewed or persisted
- top tailoring priorities
- key changed areas
- generated artifacts available
- whether a Chrome handoff is the next best step

## Common Mistakes

- Skipping JD upload and trying to tailor from ad hoc text only
- Saving immediately when the user actually asked to review a preview
- Forgetting to set `content_language` before generating a multilingual result
- Treating a generated cover letter as proof that the tailored resume itself was persisted
