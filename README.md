# Job Mediator Skills

This folder packages two Codex skills around the local Job Mediator backend:

- `filtering-jobs-multilingual`
- `tailoring-resume-to-jd`

These skills are meant for agents that need to:

- screen roles in English, Chinese, and Japanese
- search SEEK and doda from a local resume
- evaluate JD fit with the A-F scoring backend
- tailor resumes and generate downstream materials
- track submitted jobs to avoid duplicate applications
- reuse a local, private application profile for common form answers
- hand off live portal inspection or application steps to the Chrome skill

## Included Files

- `filtering-jobs-multilingual/SKILL.md`
- `filtering-jobs-multilingual/application-records.md`
- `tailoring-resume-to-jd/SKILL.md`
- `tailoring-resume-to-jd/application-records.md`
- `tailoring-resume-to-jd/application-personal-info-template.md`
- `references/backend-api-workflows.md`
- `install-to-codex.ps1`

## Install Into Codex

From this repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-to-codex.ps1
```

The script copies both skills into:

```text
%USERPROFILE%\.codex\skills\
```

## Runtime Assumptions

- Backend root: `http://127.0.0.1:8001` unless overridden by the local backend config
- Health check: `http://127.0.0.1:8001/api/v1/health`
- Local secret config: `C:\Users\uryuu\Desktop\go_find_a_job\backend\data\config.json`
- Safe example config: `C:\Users\uryuu\Desktop\go_find_a_job\backend\data\config.example.json`

## Local Application Memory

Keep reusable application state in the active workspace, not in this public skill
repository:

- `applied_jobs_log.md`: jobs that were shortlisted, skipped, started, failed, or submitted
- `application_personal_info.md`: private reusable form answers copied from the template

Agents should read these files before applying, append to the log after confirmed
submission, and avoid storing passwords or identity-document details.

## Chrome Integration

These skills are written to work with the existing Codex Chrome skill.

Use Chrome when the agent needs:

- the user's logged-in browser session
- existing tabs or cookies
- real portal inspection after ranking jobs
- live application flows on SEEK, doda, Ashby, Greenhouse, Lever, or company career pages

Do not use generic browsing for those authenticated or profile-dependent steps. The agent should explicitly invoke `@chrome` first, then continue the live browser task there.
