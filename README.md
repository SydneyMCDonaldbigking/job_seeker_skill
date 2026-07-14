# Job Mediator Skills

This folder packages four Codex skills around the local Job Mediator backend
and a Marvis-compatible application pipeline:

- `filtering-jobs-multilingual`
- `indeed-native-apply`
- `tailoring-resume-to-jd`
- `managing-job-pipeline-marvis`

These skills are meant for agents that need to:

- screen roles in English, Chinese, and Japanese
- search SEEK and doda from a local resume
- evaluate JD fit with the A-F scoring backend
- tailor resumes and generate downstream materials
- apply to Indeed Australia with saved/native resumes
- track submitted jobs to avoid duplicate applications
- store application state as local Marvis Markdown tasks
- reuse a local, private application profile for common form answers
- hand off live portal inspection or application steps to the Chrome skill

## Included Files

- `filtering-jobs-multilingual/SKILL.md`
- `filtering-jobs-multilingual/application-records.md`
- `filtering-jobs-multilingual/gmail-seek-recommendations.md`
- `indeed-native-apply/SKILL.md`
- `indeed-native-apply/scripts/indeed_apply_helper.py`
- `tailoring-resume-to-jd/SKILL.md`
- `tailoring-resume-to-jd/application-records.md`
- `tailoring-resume-to-jd/application-personal-info-template.md`
- `managing-job-pipeline-marvis/SKILL.md`
- `managing-job-pipeline-marvis/scripts/job_pipeline.py`
- `managing-job-pipeline-marvis/references/schema.md`
- `references/backend-api-workflows.md`
- `references/seek-quick-apply-runbook.md`
- `references/seek-gmail-application-workflow.md`
- `install-to-codex.ps1`

## Install Into Codex

From this repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-to-codex.ps1
```

The script copies all four skills into:

```text
%USERPROFILE%\.codex\skills\
```

## Runtime Assumptions

- Backend root: `http://127.0.0.1:8001` unless overridden by the local backend config
- Health check: `http://127.0.0.1:8001/api/v1/health`
- Local secret config: keep the private backend config outside this public repository, for example under the local backend `data/config.json`.
- Safe example config: commit only redacted or example config files such as `data/config.example.json`.

## Local Application Memory

Keep reusable application state in the active workspace, not in this public
skill repository. Prefer:

- `Marvis/Job Search/`: current application pipeline and duplicate-check source
- `job_application_profile.json`: private profile facts, portal mappings, account overrides, and resume assets
- legacy Markdown/JSON application logs: read-only migration backups

Agents should load `managing-job-pipeline-marvis` before screening or applying,
transition a task to `submitted` only after confirmation, and avoid storing
passwords or identity-document details.

## Privacy Boundary

Do not commit a real Vault, application records, resumes, account emails,
phone numbers, addresses, visa details, or salary answers. This repository
contains only reusable schemas, deterministic scripts, and redacted examples.

## Chrome Integration

These skills are written to work with the existing Codex Chrome skill.

Use Chrome when the agent needs:

- the user's logged-in browser session
- existing tabs or cookies
- real portal inspection after ranking jobs
- live application flows on SEEK, Indeed, doda, Ashby, Greenhouse, Lever, or company career pages

Do not use generic browsing for those authenticated or profile-dependent steps. The agent should explicitly invoke `@chrome` first, then continue the live browser task there.
