#!/usr/bin/env python3
"""Deterministic helpers for Indeed Australia native-resume applications.

The helper keeps browser work small and repeatable:

- extract stable Indeed job identity from noisy URLs
- answer common screening questions from a private local profile
- build Marvis/job-pipeline record JSON without hand-writing frontmatter

It intentionally does not submit applications or inspect browser state.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


QUESTION_RULES = [
    {
        "category": "right_to_work_level",
        "needles": [
            "right to work",
            "work in australia",
            "work authorisation",
            "work authorization",
            "employment visa",
            "resident visa",
        ],
    },
    {
        "category": "salary_expectation",
        "needles": [
            "salary expectation",
            "expected salary",
            "salary expectations",
            "remuneration expectation",
            "desired salary",
        ],
    },
    {
        "category": "physical_based_sydney_melbourne",
        "needles": [
            "physically based",
            "based in sydney",
            "based in melbourne",
            "currently based",
            "currently located",
        ],
    },
    {
        "category": "linkedin_profile_url",
        "needles": ["linkedin"],
    },
    {
        "category": "earliest_start_date",
        "needles": [
            "earliest start",
            "start date",
            "available to start",
            "when can you start",
            "commencement date",
        ],
    },
    {
        "category": "experience_years",
        "needles": [
            "years of experience",
            "year of experience",
            "how many years",
            "professional experience",
        ],
    },
    {
        "category": "address",
        "needles": [
            "street address",
            "current address",
            "postal code",
            "postcode",
            "city/state",
            "city and state",
        ],
    },
]


def load_json(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def dig(data: Any, *keys: str) -> Any:
    cur = data
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def clean_question(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def parse_today(value: str | None) -> date:
    return date.fromisoformat(value) if value else date.today()


def au_date(value: date) -> str:
    return value.strftime("%d/%m/%Y")


def mapping(profile: dict[str, Any], category: str) -> dict[str, Any]:
    found = dig(profile, "sites", "indeed_au", "form_mappings", category)
    return found if isinstance(found, dict) else {}


def direct_answer(data: dict[str, Any]) -> Any:
    for key in (
        "answer",
        "value",
        "default",
        "likely_answer_for_temporary_visa_restricted_hours",
        "likely_answer_for_temporary_visa",
    ):
        if data.get(key) not in (None, ""):
            return data[key]
    return None


def fallback_answer(profile: dict[str, Any], category: str) -> Any:
    if category == "salary_expectation":
        return dig(profile, "profile", "salary", "default_application_text")
    if category == "linkedin_profile_url":
        return dig(profile, "profile", "links", "linkedin_url")
    if category == "right_to_work_level":
        return dig(profile, "profile", "work_rights", "indeed_level")
    return None


def address_answer(profile: dict[str, Any], question: str) -> Any:
    data = mapping(profile, "address")
    answers = data.get("answers") if isinstance(data.get("answers"), dict) else {}
    if not answers:
        answers = dig(profile, "profile", "identity", "address") or {}
    if not isinstance(answers, dict):
        return None

    q = clean_question(question)
    candidates: list[str]
    if "postal" in q or "postcode" in q or "zip" in q:
        candidates = ["postal_code", "postcode", "postalCode", "zip"]
    elif "city/state" in q or "city and state" in q:
        candidates = ["city_state", "cityState"]
    elif "city" in q or "suburb" in q:
        candidates = ["city", "suburb", "city_state", "cityState"]
    elif "state" in q:
        candidates = ["state", "city_state", "cityState"]
    else:
        candidates = ["street_address", "streetAddress", "address", "street"]

    for key in candidates:
        if answers.get(key) not in (None, ""):
            return answers[key]
    return answers or None


def answer_for(profile: dict[str, Any], question: str, today: date) -> dict[str, Any]:
    q = clean_question(question)
    category = "unknown"
    for rule in QUESTION_RULES:
        if any(needle in q for needle in rule["needles"]):
            category = rule["category"]
            break

    data = mapping(profile, category)
    answer: Any = None
    source = f"profile.sites.indeed_au.form_mappings.{category}"

    if category == "earliest_start_date" and dig(profile, "profile", "availability", "ready_to_start_now") is True:
        answer = au_date(today)
        source = "profile.availability.ready_to_start_now"
    elif category == "address":
        answer = address_answer(profile, question)
    elif category != "unknown":
        answer = direct_answer(data)
        if answer in (None, ""):
            answer = fallback_answer(profile, category)

    requires_confirmation = bool(data.get("requires_confirmation", False))
    if answer in (None, ""):
        confidence = "needs_user"
    elif requires_confirmation:
        confidence = "needs_confirmation"
    else:
        confidence = "high"

    return {
        "question": question,
        "category": category,
        "answer": answer,
        "confidence": confidence,
        "requires_confirmation": requires_confirmation,
        "source": source if category != "unknown" else None,
    }


def extract_job_id(url: str) -> str:
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key in ("jk", "vjk", "jobkey", "jobKey", "job_key"):
        if query.get(key):
            return query[key].strip()
    match = re.search(r"(?:jk|vjk|jobkey|job_key)=([A-Za-z0-9_-]+)", url)
    return match.group(1) if match else ""


def canonical_indeed_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        parsed = urlparse("https://" + url.strip())
    host = parsed.netloc.lower()
    job_id = extract_job_id(url)

    if job_id and host.endswith("indeed.com") and "smartapply.indeed" not in host:
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        key = "jk" if query.get("jk") else "vjk"
        path = parsed.path if parsed.path and parsed.path != "/" else "/viewjob"
        return urlunparse((parsed.scheme, parsed.netloc, path, "", urlencode({key: job_id}), ""))

    keep: dict[str, str] = {}
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    for key in ("jk", "vjk", "jobkey", "jobKey", "job_key"):
        if query.get(key):
            keep[key] = query[key]
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", "", urlencode(keep), ""))


def url_info(url: str) -> dict[str, Any]:
    parsed = urlparse(url if "://" in url else "https://" + url)
    return {
        "portal": "indeed_au" if "indeed" in parsed.netloc.lower() else "unknown",
        "portal_job_id": extract_job_id(url),
        "canonical_url": canonical_indeed_url(url),
        "host": parsed.netloc,
        "path": parsed.path or "/",
    }


def compact(record: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in record.items() if v not in (None, "", [], {})}


def build_record(args: argparse.Namespace) -> dict[str, Any]:
    info = url_info(args.url)
    job_id = args.job_id or info["portal_job_id"]
    return compact(
        {
            "date": args.date or date.today().isoformat(),
            "site": "indeed_au",
            "portal": "indeed_au",
            "job_id": job_id,
            "portal_job_id": job_id,
            "url": info["canonical_url"],
            "job_url": info["canonical_url"],
            "company": args.company,
            "role": args.role,
            "source": args.source,
            "status": args.status,
            "account_email": args.account_email,
            "resume_filename": args.resume_filename,
            "cover_letter": args.cover_letter,
            "notes": args.notes,
        }
    )


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_url_info(args: argparse.Namespace) -> int:
    print_json(url_info(args.url))
    return 0


def cmd_answer(args: argparse.Namespace) -> int:
    profile = load_json(args.profile)
    print_json(answer_for(profile, args.question, parse_today(args.today)))
    return 0


def cmd_answers(args: argparse.Namespace) -> int:
    profile = load_json(args.profile)
    today = parse_today(args.today)
    result = [
        answer_for(profile, rule["needles"][0], today)
        for rule in QUESTION_RULES
        if rule["category"] != "unknown"
    ]
    print_json(result)
    return 0


def cmd_record_json(args: argparse.Namespace) -> int:
    print_json(build_record(args))
    return 0


def cmd_self_test(_: argparse.Namespace) -> int:
    mock = {
        "profile": {
            "availability": {"ready_to_start_now": True},
            "salary": {"default_application_text": "AUD 60000/year"},
            "links": {"linkedin_url": "https://www.linkedin.com/in/example"},
        },
        "sites": {
            "indeed_au": {
                "form_mappings": {
                    "right_to_work_level": {"answer": "Employment Visa", "requires_confirmation": False},
                    "physical_based_sydney_melbourne": {"answer": "Yes", "requires_confirmation": False},
                    "experience_years": {"answer": "No experience", "requires_confirmation": False},
                    "address": {
                        "answers": {"postal_code": "2000", "city_state": "Sydney NSW", "street_address": "Example Street"},
                        "requires_confirmation": True,
                    },
                }
            }
        },
    }
    today = date(2026, 7, 14)
    assert extract_job_id("https://au.indeed.com/viewjob?jk=abc123&from=foo") == "abc123"
    assert canonical_indeed_url("https://au.indeed.com/?from=gnav&vjk=abc123") == "https://au.indeed.com/viewjob?vjk=abc123"
    assert answer_for(mock, "Earliest start date?", today)["answer"] == "14/07/2026"
    assert answer_for(mock, "What is your level of right to work in Australia?", today)["answer"] == "Employment Visa"
    assert answer_for(mock, "How many years of Python experience do you have?", today)["answer"] == "No experience"
    assert answer_for(mock, "Postal code", today)["confidence"] == "needs_confirmation"
    print_json({"ok": True})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    url_cmd = sub.add_parser("url-info", help="Extract Indeed job id and canonical URL.")
    url_cmd.add_argument("--url", required=True)
    url_cmd.set_defaults(func=cmd_url_info)

    answer_cmd = sub.add_parser("answer", help="Answer one Indeed screening question from a private profile.")
    answer_cmd.add_argument("--profile", type=Path, required=True)
    answer_cmd.add_argument("--question", required=True)
    answer_cmd.add_argument("--today", help="Override today's date as YYYY-MM-DD for deterministic runs.")
    answer_cmd.set_defaults(func=cmd_answer)

    answers_cmd = sub.add_parser("answers", help="Print common Indeed default answers from a private profile.")
    answers_cmd.add_argument("--profile", type=Path, required=True)
    answers_cmd.add_argument("--today", help="Override today's date as YYYY-MM-DD for deterministic runs.")
    answers_cmd.set_defaults(func=cmd_answers)

    record_cmd = sub.add_parser("record-json", help="Build a job_pipeline.py-compatible record JSON object.")
    record_cmd.add_argument("--url", required=True)
    record_cmd.add_argument("--job-id")
    record_cmd.add_argument("--company", required=True)
    record_cmd.add_argument("--role", required=True)
    record_cmd.add_argument("--source", default="indeed_search")
    record_cmd.add_argument("--status", default="discovered")
    record_cmd.add_argument("--date")
    record_cmd.add_argument("--account-email")
    record_cmd.add_argument("--resume-filename")
    record_cmd.add_argument("--cover-letter")
    record_cmd.add_argument("--notes")
    record_cmd.set_defaults(func=cmd_record_json)

    test_cmd = sub.add_parser("self-test", help="Run deterministic helper tests.")
    test_cmd.set_defaults(func=cmd_self_test)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
