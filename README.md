# Job Mediator Skills

This folder packages two Codex skills around the local Job Mediator backend:

- `filtering-jobs-multilingual`
- `tailoring-resume-to-jd`

These skills are meant for agents that need to:

- screen roles in English, Chinese, and Japanese
- search SEEK and doda from a local resume
- evaluate JD fit with the A-F scoring backend
- tailor resumes and generate downstream materials
- hand off live portal inspection or application steps to the Chrome skill

## Included Files

- `filtering-jobs-multilingual/SKILL.md`
- `tailoring-resume-to-jd/SKILL.md`
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

- Backend root: `http://127.0.0.1:8000`
- Health check: `http://127.0.0.1:8000/api/v1/health`
- Local secret config: `C:\Users\uryuu\Desktop\go_find_a_job\backend\data\config.json`
- Safe example config: `C:\Users\uryuu\Desktop\go_find_a_job\backend\data\config.example.json`

## Chrome Integration

These skills are written to work with the existing Codex Chrome skill.

Use Chrome when the agent needs:

- the user's logged-in browser session
- existing tabs or cookies
- real portal inspection after ranking jobs
- live application flows on SEEK, doda, Ashby, Greenhouse, Lever, or company career pages

Do not use generic browsing for those authenticated or profile-dependent steps. The agent should explicitly invoke `@chrome` first, then continue the live browser task there.
