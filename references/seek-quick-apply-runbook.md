# SEEK Quick Apply Runbook

Last sanitized: 2026-06-10

This runbook summarizes a successful end-to-end workflow for submitting SEEK Quick Apply applications with a logged-in Chrome session and local resume tailoring. It is generic by design and contains no personal application data.

## High-Level Flow

1. Read private local state before doing anything:
   - Candidate profile
   - Application log
   - Upload memory
   - Personal answer memory
2. Deduplicate:
   - Never apply to a job whose job ID or URL is already recorded as submitted.
3. Test the Chrome control bridge:
   - Use the working unsandboxed Node REPL bridge.
   - A minimal smoke test should return `ok`.
4. Check the local backend:
   - Verify the health endpoint before relying on tailoring or PDF generation.
5. For each target job:
   - Fetch or inspect the live job description.
   - Generate one job-specific tailored PDF.
   - Draft one job-specific inline cover letter.
   - Open the SEEK `/apply` page in logged-in Chrome.
   - Upload the job-specific PDF.
   - Replace any stale cover letter text.
   - Answer employer questions from confirmed local profile data only.
   - Stop at the review page.
6. Submit only after the batch is confirmed.
7. Confirm success page per job.
8. Record successful submissions only after the portal confirms success.
9. Clean up automation-created browser tabs.

## Backend Notes

Run the backend from the backend package directory, not necessarily the repository root. If the app imports a top-level package such as `app`, the working directory must make that package importable.

Common issues:

- `ModuleNotFoundError` for the app package:
  - Usually caused by running from the wrong directory.
- Missing Python dependencies:
  - Usually caused by using the wrong Python environment.
  - Prefer the project's package manager/runtime wrapper.
- Degraded LLM health:
  - Can happen because of upstream rate limits.
  - If the user approved fallback behavior, continue with a conservative resume and manually drafted cover letter.

## Tailored PDF Generation

If an HTTP PDF endpoint hangs on Windows, check whether it launches a visible browser from a background service. A reliable workaround is:

- Run a small local script in the backend environment.
- Import the same PDF generation function.
- Force headless rendering.
- Write PDF bytes into the private workspace.

Keep generated PDFs private. Do not commit them.

## Chrome Bridge Notes

Use the known-working Chrome automation bridge for the environment. If the JavaScript kernel resets:

1. Re-run Chrome bootstrap.
2. List open Chrome tabs.
3. Claim tabs from the returned tab objects.
4. Avoid guessed tab IDs.

Do not inspect cookies, session stores, passwords, or browser profile internals.

## SEEK Upload Notes

SEEK may render both resume and cover-letter file inputs. Avoid broad file selectors.

Reliable resume upload pattern:

```js
await tab.playwright.getByLabel("Upload resume", { exact: true }).check({ force: true });

const uploadButton = tab.playwright
  .getByTestId("resumeFileInput")
  .getByTestId("upload-button");

const chooserPromise = tab.playwright.waitForEvent("filechooser", { timeoutMs: 10000 });
await uploadButton.click({ timeoutMs: 10000 });
const chooser = await chooserPromise;
await chooser.setFiles(["C:/absolute/path/to/job-specific-resume.pdf"]);
```

Then verify the uploaded filename appears before continuing.

Avoid:

- Clicking hidden `input[type="file"]` controls directly if they have no clickable bounding box.
- Using broad `input[type="file"]` when there are multiple file inputs.
- Reusing stale application tabs after a failed upload attempt.

## Cover Letter Notes

Google Translate or browser translation overlays can duplicate labels. If label lookup becomes ambiguous, filling the single `textarea` on the documents step can be more reliable.

Always replace stale cover letter text from previous applications.

## Employer Question Policy

Use only confirmed local profile data. If a question is ambiguous, legally sensitive, or not covered by confirmed data, pause and ask.

Examples of answers that often require special care:

- Work rights
- Sponsorship
- Salary
- Notice period
- Medical, demographic, legal, or background-check questions
- Experience duration
- Programming languages and tools

When in doubt, answer conservatively or ask.

## SEEK Profile Page

SEEK may show a profile update step after employer questions.

Default behavior:

- Do not add imported resume entries to the SEEK profile unless explicitly requested.
- Continue to review without modifying the public profile.

## Review Page Checklist

Before submit:

- Correct account is displayed.
- Correct company and role are displayed.
- Correct job-specific PDF is listed.
- Cover letter is present.
- Employer questions show complete.
- Optional promotional checkboxes are left untouched unless requested.

## Success Signals

Treat a submission as successful only if the page confirms it.

Useful signals:

- URL contains `/apply/success`.
- Title contains `Application sent`.
- Body text says the application has been sent to the employer.

Only then write the local application record.

## Browser Tab Cleanup

After each confirmed success:

- Close automation-created SEEK job, apply, search, and success tabs.
- Do not close tabs that existed before automation started.
- Prefer per-job cleanup over one large final cleanup call.
- If cleanup fails, report which tabs remain open rather than blocking the workflow.

## Do Not Commit

Keep all private artifacts out of Git:

- Candidate profile JSON
- Application log
- Personal info memory
- Resume PDFs
- Tailored PDFs
- Raw job descriptions
- Local executable copies
- Browser bridge repair binaries

