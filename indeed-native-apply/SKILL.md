---
name: indeed-native-apply
description: Use when applying to Indeed Australia with a saved/native resume, especially through Chrome SmartApply, using private profile defaults, duplicate checks, cover letters, and Marvis records without calling resume-tailoring code.
---

# Indeed Native Apply

## Purpose

Use this skill when an agent needs to apply to Indeed Australia roles with an already prepared or saved resume, without calling the resume-tailoring backend.

This skill is for:

- opening live Indeed Australia job pages
- screening roles before starting SmartApply
- applying with a saved/native resume
- answering common Indeed screening questions from confirmed profile memory
- avoiding duplicate applications
- recording submitted or skipped jobs

It is not for rewriting the resume. Use `tailoring-resume-to-jd` only when the user explicitly wants a tailored resume or generated PDF.

## Preconditions

The host agent should have:

- Chrome browser automation for authenticated Indeed pages
- a known active Indeed account
- an already prepared resume saved in Indeed or available locally
- user authorization to submit applications directly
- a private application profile or answer memory

Optional but useful:

- Gmail or mailbox access for Indeed recommendations and confirmations
- a Marvis job pipeline managed through `managing-job-pipeline-marvis`
- `scripts/indeed_apply_helper.py` for URL identity, default answers, and record JSON

## Helper Script

Use the helper before and during browser work so the browser session stays focused.

Extract a stable job identity:

```bash
python scripts/indeed_apply_helper.py url-info --url "https://au.indeed.com/viewjob?jk=abc123&from=foo"
```

Answer a common question from the private profile:

```bash
python scripts/indeed_apply_helper.py answer --profile job_application_profile.json --question "Earliest start date?" --today YYYY-MM-DD
```

Build a record JSON object for `job_pipeline.py add`:

```bash
python scripts/indeed_apply_helper.py record-json \
  --url "https://au.indeed.com/viewjob?jk=abc123" \
  --company "Example Company" \
  --role "Junior Software Engineer" \
  --source "indeed_search" \
  --status discovered
```

Never commit helper output when it includes private profile answers, account emails, address details, or salary details.

## URL Identity

Use `portal: indeed_au`.

Use Indeed `jk` or `vjk` as the portal job id. Strip tracking parameters before duplicate checks. Prefer canonical URLs from the helper when available.

Before applying:

1. Resolve the final live Indeed job URL.
2. Run a duplicate check with the exact job id and canonical URL.
3. Check the page for already-applied or closed-job text.
4. Treat matching job ids as duplicates even when titles differ slightly.

## Native Resume Mode

When the user says to use the original, native, current, uploaded, or saved resume:

1. Do not call resume-tailoring endpoints.
2. Do not generate a new PDF.
3. Prefer the saved Indeed resume whose filename matches the current resume memory.
4. If the saved resume is missing, upload the current resume only if the user has already identified it.
5. If a saved resume preview has a non-blocking old address and the user already approved that mismatch, do not block solely on that mismatch.
6. Before final submit, verify the selected resume filename or visible resume preview.

## Account Check

Before applying, verify the active Indeed account from the visible page or profile surface.

- The visible account should match the account requested by the user.
- Stop before submitting if the active account is unclear or mismatched.
- Do not inspect cookies, passwords, session stores, or browser profile files to determine the account.

## Screening Rules

Prefer jobs that match early-career software, AI, automation, data, full-stack, intern, graduate, junior, associate, assistant, or technical support roles.

Good signals:

- junior, graduate, intern, entry-level, associate
- Python, JavaScript, TypeScript, AI tools, LLM, RAG, automation, chatbot, data
- no fixed years requirement
- student-compatible part-time, casual, internship, or graduate work
- SmartApply or Apply with Indeed
- employer questions are answerable from confirmed profile memory

Skip or hold when:

- the page says the role is closed
- the role has hard citizen, permanent resident, or clearance requirements the profile does not satisfy
- the role asks for senior, lead, principal, or fixed 3+ years when the profile is junior
- the form asks for unknown sensitive facts
- the form asks for CAPTCHA, identity verification, payment, bank, tax, passport, or password data
- the flow leaves Indeed for a full external ATS profile with unknown legal details

For borderline roles, apply only when hard blockers are absent and the skills overlap is meaningful.

## Common Indeed Answers

Use only confirmed answers from the private profile or user instructions. The helper can classify common questions and return:

- work-rights level
- salary expectation
- physical Sydney/Melbourne location
- LinkedIn profile URL
- earliest start date
- years-of-experience text
- address fields, when already confirmed

If `ready_to_start_now` is true, answer earliest start date with the current run date in `DD/MM/YYYY`, not an old stored date.

Stop and ask the user when a question involves:

- legal identity or background checks
- work rights not covered by confirmed wording
- sponsorship if not already confirmed
- driver licence
- security clearance
- demographic or diversity information
- health, disability, criminal history, or protected attributes
- exact street address if not already confirmed for Indeed

## Browser Flow

For each selected job:

1. Open the live Indeed job page.
2. Confirm the role is open and not already applied.
3. Start `Apply with Indeed`.
4. Confirm the account and saved/native resume.
5. Use the helper for common questions before typing answers.
6. For unknown questions, stop and ask instead of guessing.
7. Continue through SmartApply one page at a time.
8. On the review page, verify:
   - role and company
   - active account
   - selected resume
   - cover letter if requested or present
   - required questions complete
9. Submit only after the review page is checked.
10. Confirm success from the Indeed success page or confirmation email.
11. Close tabs opened for the run when cleanup is requested.

Do not treat a SmartApply form page, generated cover letter, or review page as proof of submission. Submission requires a visible success page or confirmation email.

## Recording Results

After each confirmed submission, create or transition one Marvis task when the pipeline is available. Otherwise append a local record with:

- date
- source
- company
- role
- job id
- canonical URL
- resume filename
- cover letter summary
- status
- employer question count
- confirmation text

Use `scripts/indeed_apply_helper.py record-json` to reduce hand-written records, then use `managing-job-pipeline-marvis/scripts/job_pipeline.py` for deterministic writes.

Keep public repositories sanitized. Do not commit personal details, resumes, raw application logs, account emails, phone numbers, addresses, visa details, salary answers, or generated record JSON containing private values.

## Output Format

Summarize the run with:

- submitted jobs
- skipped duplicates
- skipped hard mismatches
- unknown-question blockers
- confirmation method

Example:

```text
Submitted:
- Company - Role - job id

Skipped:
- Company - reason

Confirmed by:
- Indeed success page
- confirmation email pending
```

## Common Mistakes

- Reusing an old static earliest-start date instead of today's date
- Trusting a noisy Indeed URL without extracting `jk` or `vjk`
- Submitting after an account mismatch
- Guessing years, citizenship, clearance, licence, or protected-attribute answers
- Treating a review page as a submitted application
- Leaving SmartApply tabs open after the run
