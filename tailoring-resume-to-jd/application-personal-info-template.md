# Application Personal Info Template

Copy this template to a local file named `application_personal_info.md` in the
active workspace. Fill the copied file with the user's real answers. Do not commit
the filled file to a public repository.

Use stored answers only when the application form wording clearly matches. Ask
the user when a question is new, ambiguous, legally sensitive, or could change by
job.

## Identity

```yaml
preferred_name:
legal_name:
preferred_email:
preferred_phone:
current_location:
linkedin:
github:
portfolio:
preferred_job_board_account:
```

## Work Rights And Availability

```yaml
country:
work_rights_answer:
visa_status_answer:
sponsorship_required_answer:
available_start_date:
notice_period_answer:
relocation_answer:
remote_hybrid_onsite_preference:
```

## Education

```yaml
highest_degree:
computer_science_qualification_answer:
graduation_status_answer:
university:
graduation_date:
```

## Experience Answers

Store wording that can be pasted or selected directly when the form asks the same
question.

```yaml
ai_engineer_experience_answer:
data_engineer_experience_answer:
software_engineer_experience_answer:
machine_learning_experience_answer:
python_experience_answer:
javascript_experience_answer:
cloud_experience_answer:
```

## Skills And Tools

Only select skills that are confirmed by the resume or by the user.

```yaml
confirmed_programming_languages:
confirmed_frameworks:
confirmed_cloud_tools:
confirmed_databases:
confirmed_ml_tools:
```

## Common Free-Text Answers

Keep these concise and honest. Rewrite them for the specific JD before submitting.

```yaml
why_this_role:
why_this_company:
ai_project_summary:
backend_project_summary:
teamwork_example:
challenge_example:
availability_note:
```

## Guardrails

- Never store passwords, one-time codes, secret tokens, tax IDs, or identity
  document numbers.
- Do not invent credentials or years of experience.
- If a form requires an explanation for work rights, sponsorship, education, or
  experience, adapt the stored answer to the exact question and show the user
  when the risk is non-trivial.
- When the user gives a new answer during an application, ask whether to append it
  to the local personal info file for reuse.
