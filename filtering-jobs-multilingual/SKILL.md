---
name: filtering-jobs-multilingual
description: Use when screening or searching jobs in English, Chinese, or Japanese from a local resume, especially when you need SEEK or doda results, JD translation, A-F fit scoring, or browser follow-up in Chrome.
---

# Filtering Jobs Multilingual

## Overview

Use the local Job Mediator backend as the system of record for multilingual job screening. This skill is for English, Chinese, and Japanese role discovery, ranking, and follow-up.

Read `backend-api-workflows.md` before your first run if you need exact payload shapes.

## When to Use

Use this skill when the user wants to:

- search roles from a stored resume
- rank jobs against a resume in `en`, `zh`, or `ja`
- compare multiple JDs quickly with the A-F scoring model
- translate an English or Japanese JD into Chinese before discussing it
- review shortlisted jobs in the user's real browser session

Do not use this skill for final resume rewriting. Use `tailoring-resume-to-jd` for that.

## Core Workflow

1. Check backend health at `GET /api/v1/health`.
2. Confirm the active resume exists for the target language. If needed, upload a fresh resume with `resume_language=en|zh|ja`.
3. Set `content_language` through `PUT /api/v1/config/language` when the user wants outputs in English, Chinese, or Japanese.
4. Choose the search path:
   - `SEEK` for English or Australia-facing searches
   - `doda` for Japanese-market searches
5. Run `POST /api/v1/jobs/search/seek` or `POST /api/v1/jobs/search/doda`.
6. For promising roles, call `POST /api/v1/evaluate-job` to get the structured A-F fit result.
7. If the JD is not easy for the user to read, call `POST /api/v1/translate-job-description` to produce simplified Chinese support text.
8. Summarize jobs by score, key risks, and next action.

## Language Policy

- `en`: keep summaries and action notes in English unless the user asks otherwise
- `zh`: translate or summarize findings in Chinese where helpful, especially for English or Japanese JDs
- `ja`: prefer the Japanese resume for search and ranking, especially with doda

For Chinese support, the backend translation endpoint is JD-to-Chinese, not full bidirectional localization. Keep that boundary explicit.

## Chrome Handoff

If the user wants to inspect live listings, compare real portal pages, or continue into application flows:

1. Explicitly invoke `@chrome`.
2. Reuse the user's logged-in Chrome context.
3. Open the shortlisted job URLs there.
4. Do not switch to generic browsing for cookie-dependent or authenticated steps.

Use Chrome especially for:

- SEEK listing inspection
- doda listing inspection
- Ashby, Greenhouse, Lever, and company career pages
- application steps that depend on the user's session

## Output Shape

Return shortlists in a compact structure:

- role title
- company
- source
- location
- fit score
- why it matches
- why it may fail
- whether Chrome follow-up is worth it

## Common Mistakes

- Searching with the wrong resume language for the market
- Tailoring the resume inside the screening loop instead of first ranking jobs
- Using generic browser tooling for portal/application steps that should move into `@chrome`
- Treating translated Chinese helper text as the original JD source of truth
