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

Use before any multi-step workflow.

## Language Config

```http
GET /api/v1/config/language
PUT /api/v1/config/language
Content-Type: application/json
```

Payload:

```json
{
  "ui_language": "en",
  "content_language": "zh"
}
```

Supported by this package:

- `en`
- `zh`
- `ja`

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

Use to find the active language-specific resume id before search or tailoring.

## Upload Job Description

```http
POST /api/v1/jobs/upload
Content-Type: application/json
```

Payload:

```json
{
  "resume_id": "resume-id",
  "job_descriptions": [
    "Responsibilities: build APIs\nRequirements: Python and FastAPI"
  ]
}
```

## Search SEEK

```http
POST /api/v1/jobs/search/seek
Content-Type: application/json
```

Payload:

```json
{
  "resume_id": "resume-id",
  "location": "Sydney NSW"
}
```

## Search doda

```http
POST /api/v1/jobs/search/doda
Content-Type: application/json
```

Payload:

```json
{
  "resume_id": "resume-id",
  "location": "Tokyo"
}
```

## Evaluate Resume vs JD

```http
POST /api/v1/evaluate-job
Content-Type: application/json
```

Payload:

```json
{
  "resume": {
    "summary": "..."
  },
  "job_description": "Responsibilities: ..."
}
```

The `resume` field may be either structured resume JSON or plain text.

## Translate JD to Chinese

```http
POST /api/v1/translate-job-description
Content-Type: application/json
```

Payload:

```json
{
  "job_description": "English or Japanese JD text"
}
```

## Tailor Resume Preview

```http
POST /api/v1/resumes/improve/preview
Content-Type: application/json
```

Payload:

```json
{
  "resume_id": "resume-id",
  "job_id": "job-id",
  "prompt_id": "default"
}
```

Use preview when the user wants review before persistence.

## Tailor Resume And Persist

```http
POST /api/v1/resumes/improve
Content-Type: application/json
```

Payload:

```json
{
  "resume_id": "resume-id",
  "job_id": "job-id",
  "prompt_id": "default"
}
```

## Confirm Previewed Tailored Resume

```http
POST /api/v1/resumes/improve/confirm
Content-Type: application/json
```

Use the preview response to fill:

- `resume_id`
- `job_id`
- `improved_data`
- `improvements`

## Generate Cover Letter

```http
POST /api/v1/resumes/{resume_id}/generate-cover-letter
```

Use only for a tailored resume that already has job context.

## Generate Outreach Message

```http
POST /api/v1/resumes/{resume_id}/generate-outreach
```

## Download Resume PDF

```http
GET /api/v1/resumes/{resume_id}/pdf
```

## Direct Tailored PDF

```http
POST /api/v1/generate-tailored-pdf
Content-Type: application/json
```

Payload:

```json
{
  "resume": {
    "summary": "..."
  },
  "job_description": "Responsibilities: ...",
  "page_size": "A4"
}
```

## Scheduled Scan

```http
GET /api/v1/scheduled-scan/settings
POST /api/v1/scan-jobs
POST /api/v1/scheduled-scan/jobs/status
```

Use scheduled-scan endpoints when the user wants recurring discovery or to mark discovered jobs as `saved`, `ignored`, or `applied`.

For manual Chrome applications that do not have a backend job key, maintain the
workspace Markdown application log described by the skills instead.
