# Backend API Workflows

Default backend:

```text
http://127.0.0.1:8001
```

If the backend was started on another port, use the active port from the user's
session or local config instead.

API prefix:

```text
/api/v1
```

## Health

```http
GET /api/v1/health
```

## Language Config

```http
GET /api/v1/config/language
PUT /api/v1/config/language
Content-Type: application/json
```

## Upload Master Resume

```http
POST /api/v1/resumes/upload
Content-Type: multipart/form-data
```

Fields:

- `file`: PDF or DOCX
- `resume_language`: `en` or `zh` or `ja`

## List Resumes

```http
GET /api/v1/resumes/list
```

## Upload Job Description

```http
POST /api/v1/jobs/upload
Content-Type: application/json
```

## Search SEEK

```http
POST /api/v1/jobs/search/seek
Content-Type: application/json
```

## Search doda

```http
POST /api/v1/jobs/search/doda
Content-Type: application/json
```

## Evaluate Resume vs JD

```http
POST /api/v1/evaluate-job
Content-Type: application/json
```

## Translate JD to Chinese

```http
POST /api/v1/translate-job-description
Content-Type: application/json
```

## Scheduled Scan

```http
GET /api/v1/scheduled-scan/settings
POST /api/v1/scan-jobs
POST /api/v1/scheduled-scan/jobs/status
```

Use scheduled-scan status only for backend-discovered jobs that have a backend job
key. For manual Chrome applications, update the local Markdown application log.
