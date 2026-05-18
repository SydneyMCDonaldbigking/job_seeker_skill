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

## Tailor Resume Preview

```http
POST /api/v1/resumes/improve/preview
Content-Type: application/json
```

## Tailor Resume And Persist

```http
POST /api/v1/resumes/improve
Content-Type: application/json
```

## Confirm Previewed Tailored Resume

```http
POST /api/v1/resumes/improve/confirm
Content-Type: application/json
```

## Evaluate Resume vs JD

```http
POST /api/v1/evaluate-job
Content-Type: application/json
```

## Generate Cover Letter

```http
POST /api/v1/resumes/{resume_id}/generate-cover-letter
```

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
