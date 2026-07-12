#!/usr/bin/env python3
"""Deterministic Marvis job-record migration, lookup, and status updates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any


HANDLED = {"applying", "submitted", "interview", "offer", "rejected", "withdrawn"}
TERMINAL = {"submitted", "offer", "skipped", "rejected", "withdrawn"}
VALID_STATUSES = {
    "discovered", "screening", "shortlisted", "applying", "submitted",
    "interview", "offer", "skipped", "rejected", "withdrawn", "failed",
}


def scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(json.dumps(str(v), ensure_ascii=False) for v in value) + "]"
    return json.dumps(str(value), ensure_ascii=False)


def parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if not raw:
        return ""
    if raw in {"true", "false"}:
        return raw == "true"
    if raw.startswith(('"', "[", "{")):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass
    if re.fullmatch(r"-?\d+(?:\.\d+)?", raw):
        return float(raw) if "." in raw else int(raw)
    return raw


def split_note(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    fm: dict[str, Any] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        fm[key.strip()] = parse_scalar(raw)
    return fm, text[end + 5 :]


def render_note(fm: dict[str, Any], body: str) -> str:
    preferred = [
        "kind", "project", "status", "priority", "created", "order", "archived", "tags",
        "portal", "portal_job_id", "company", "role", "job_url", "source",
        "source_account_email", "source_message_id", "application_account",
        "resume_filename", "cover_letter", "confirmation_page", "confirmation_email",
    ]
    keys = [k for k in preferred if k in fm] + sorted(k for k in fm if k not in preferred)
    lines = ["---"]
    for key in keys:
        if fm[key] is not None and fm[key] != "":
            lines.append(f"{key}: {scalar(fm[key])}")
    lines.extend(["---", ""])
    clean_body = body.lstrip("\n")
    if clean_body:
        lines.append(clean_body.rstrip())
        lines.append("")
    return "\n".join(lines)


def project_dir(vault: Path) -> Path:
    return vault / "Marvis" / "Job Search"


def ensure_project(vault: Path, dry_run: bool = False) -> Path:
    root = project_dir(vault)
    if dry_run:
        return root
    for name in ("tasks", "archive", "logs", "milestones", "skills"):
        (root / name).mkdir(parents=True, exist_ok=True)
    project = root / "_project.md"
    if not project.exists():
        project.write_text(
            "---\nkind: project\nstatus: active\ncolor: \"#3b82f6\"\n"
            f"created: {date.today().isoformat()}\n---\n\n# Job Search\n\n"
            "## Goal\n\nTrack job discovery, applications, and outcomes.\n",
            encoding="utf-8",
        )
    return root


def task_files(vault: Path) -> list[Path]:
    root = project_dir(vault)
    paths: list[Path] = []
    for folder in (root / "tasks", root / "archive"):
        if folder.exists():
            paths.extend(folder.glob("*.md"))
    return sorted(paths)


def records(vault: Path) -> list[tuple[Path, dict[str, Any], str]]:
    result = []
    for path in task_files(vault):
        fm, body = split_note(path.read_text(encoding="utf-8-sig"))
        if fm.get("kind") == "task":
            result.append((path, fm, body))
    return result


def canonical_url(value: str | None) -> str:
    return (value or "").strip().rstrip("/")


def file_name(record: dict[str, Any]) -> str:
    portal = re.sub(r"[^a-zA-Z0-9_-]+", "-", str(record.get("site") or record.get("portal") or "job"))
    job_id = str(record.get("job_id") or record.get("portal_job_id") or "").strip()
    if not job_id:
        job_id = hashlib.sha1(canonical_url(record.get("url") or record.get("job_url")).encode()).hexdigest()[:12]
    return f"{portal}-{job_id}.md"


def record_to_note(record: dict[str, Any], order: int) -> tuple[dict[str, Any], str]:
    status = str(record.get("status") or "discovered")
    if status not in VALID_STATUSES:
        status = "discovered"
    site = str(record.get("site") or record.get("portal") or "unknown")
    fm: dict[str, Any] = {
        "kind": "task",
        "project": "[[Job Search]]",
        "status": status,
        "created": record.get("date") or date.today().isoformat(),
        "order": order,
        "tags": ["job", site],
        "portal": site,
        "portal_job_id": str(record.get("job_id") or record.get("portal_job_id") or ""),
        "company": record.get("company"),
        "role": record.get("role"),
        "job_url": record.get("url") or record.get("job_url"),
        "source": record.get("source"),
        "source_account_email": record.get("source_account_email"),
        "source_message_id": record.get("source_message_id"),
        "application_account": record.get("account_email"),
        "resume_filename": record.get("resume_filename"),
        "cover_letter": record.get("cover_letter"),
    }
    body = [f"# {record.get('role') or 'Unknown role'} — {record.get('company') or 'Unknown company'}", ""]
    if record.get("notes"):
        body.extend(["## Notes", "", str(record["notes"]), ""])
    if record.get("confirmed_sensitive_answers"):
        body.extend(["## Confirmed application answers", "", "```json", json.dumps(record["confirmed_sensitive_answers"], ensure_ascii=False, indent=2), "```", ""])
    return {k: v for k, v in fm.items() if v not in (None, "")}, "\n".join(body)


def cmd_migrate(args: argparse.Namespace) -> int:
    profile = json.loads(args.legacy_profile.read_text(encoding="utf-8-sig"))
    apps = profile.get("applications", [])
    root = ensure_project(args.vault, args.dry_run)
    created = skipped = 0
    seen: set[tuple[str, str]] = set()
    for idx, record in enumerate(apps, 1):
        identity = (str(record.get("site") or ""), str(record.get("job_id") or ""))
        if identity in seen:
            raise ValueError(f"duplicate legacy identity: {identity}")
        seen.add(identity)
        task_name = file_name(record)
        existing = (root / "tasks" / task_name).exists() or (root / "archive" / task_name).exists()
        if existing:
            skipped += 1
            continue
        created += 1
        if not args.dry_run:
            fm, body = record_to_note(record, idx)
            if fm.get("status") in TERMINAL:
                fm["archived"] = True
            folder = "archive" if fm.get("status") in TERMINAL else "tasks"
            (root / folder / task_name).write_text(render_note(fm, body), encoding="utf-8")
    print(json.dumps({"legacy": len(apps), "created": created, "existing": skipped, "dry_run": args.dry_run}, ensure_ascii=False))
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    matches = []
    for path, fm, _ in records(args.vault):
        same_id = args.job_id and str(fm.get("portal_job_id", "")) == args.job_id
        same_url = args.url and canonical_url(str(fm.get("job_url", ""))) == canonical_url(args.url)
        if same_id or same_url:
            matches.append({"path": str(path), "status": fm.get("status"), "handled": fm.get("status") in HANDLED, "company": fm.get("company"), "role": fm.get("role"), "job_id": fm.get("portal_job_id"), "url": fm.get("job_url")})
    print(json.dumps(matches, ensure_ascii=False, indent=2))
    return 0 if matches else 1


def cmd_add(args: argparse.Namespace) -> int:
    record = json.loads(args.record_json.read_text(encoding="utf-8-sig"))
    ensure_project(args.vault)
    job_id = str(record.get("job_id") or record.get("portal_job_id") or "")
    url = canonical_url(record.get("url") or record.get("job_url"))
    for path, fm, _ in records(args.vault):
        if (job_id and str(fm.get("portal_job_id", "")) == job_id) or (url and canonical_url(str(fm.get("job_url", ""))) == url):
            raise ValueError(f"record already exists: {path}")
    fm, body = record_to_note(record, len(records(args.vault)) + 1)
    if fm.get("status") in TERMINAL:
        fm["archived"] = True
    folder = "archive" if fm.get("status") in TERMINAL else "tasks"
    path = project_dir(args.vault) / folder / file_name(record)
    path.write_text(render_note(fm, body), encoding="utf-8")
    print(path)
    return 0


def cmd_transition(args: argparse.Namespace) -> int:
    if args.status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {args.status}")
    hits = [(p, fm, body) for p, fm, body in records(args.vault) if str(fm.get("portal_job_id", "")) == args.job_id]
    if len(hits) != 1:
        raise ValueError(f"expected one record for {args.job_id}, found {len(hits)}")
    path, fm, body = hits[0]
    if args.status == "submitted" and not args.note:
        raise ValueError("submitted requires --note with portal or email confirmation")
    fm["status"] = args.status
    fm["archived"] = args.status in TERMINAL
    if args.note:
        body = body.rstrip() + f"\n\n## Status update — {date.today().isoformat()}\n\n{args.note}\n"
    path.write_text(render_note(fm, body), encoding="utf-8")
    destination_folder = project_dir(args.vault) / ("archive" if args.status in TERMINAL else "tasks")
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination = destination_folder / path.name
    if destination != path:
        path.replace(destination)
        path = destination
    print(path)
    return 0


def cmd_organize(args: argparse.Namespace) -> int:
    ensure_project(args.vault)
    moved_to_archive = moved_to_tasks = updated = 0
    for path, fm, body in list(records(args.vault)):
        terminal = str(fm.get("status", "")) in TERMINAL
        expected = project_dir(args.vault) / ("archive" if terminal else "tasks") / path.name
        if fm.get("archived") is not terminal:
            fm["archived"] = terminal
            path.write_text(render_note(fm, body), encoding="utf-8")
            updated += 1
        if expected != path:
            expected.parent.mkdir(parents=True, exist_ok=True)
            path.replace(expected)
            if terminal:
                moved_to_archive += 1
            else:
                moved_to_tasks += 1
    print(json.dumps({"moved_to_archive": moved_to_archive, "moved_to_tasks": moved_to_tasks, "frontmatter_updated": updated}, ensure_ascii=False))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    rows = records(args.vault)
    ids = [str(fm.get("portal_job_id", "")) for _, fm, _ in rows if fm.get("portal_job_id")]
    urls = [canonical_url(str(fm.get("job_url", ""))) for _, fm, _ in rows if fm.get("job_url")]
    errors = []
    if len(ids) != len(set(ids)):
        errors.append("duplicate portal_job_id")
    if len(urls) != len(set(urls)):
        errors.append("duplicate job_url")
    for path, fm, _ in rows:
        for key in ("kind", "project", "status", "portal", "company", "role"):
            if not fm.get(key):
                errors.append(f"{path}: missing {key}")
    result: dict[str, Any] = {"records": len(rows), "statuses": Counter(str(fm.get("status")) for _, fm, _ in rows), "errors": errors}
    if args.legacy_profile:
        legacy = json.loads(args.legacy_profile.read_text(encoding="utf-8-sig")).get("applications", [])
        result["legacy_records"] = len(legacy)
        if len(legacy) != len(rows):
            errors.append(f"count mismatch: legacy={len(legacy)} marvis={len(rows)}")
    result["statuses"] = dict(result["statuses"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest="command", required=True)
    migrate = sub.add_parser("migrate")
    migrate.add_argument("--legacy-profile", type=Path, required=True)
    migrate.add_argument("--dry-run", action="store_true")
    migrate.set_defaults(func=cmd_migrate)
    find = sub.add_parser("find")
    find.add_argument("--job-id")
    find.add_argument("--url")
    find.set_defaults(func=cmd_find)
    add = sub.add_parser("add")
    add.add_argument("--record-json", type=Path, required=True)
    add.set_defaults(func=cmd_add)
    transition = sub.add_parser("transition")
    transition.add_argument("--job-id", required=True)
    transition.add_argument("--status", required=True)
    transition.add_argument("--note")
    transition.set_defaults(func=cmd_transition)
    organize = sub.add_parser("organize")
    organize.set_defaults(func=cmd_organize)
    validate = sub.add_parser("validate")
    validate.add_argument("--legacy-profile", type=Path)
    validate.set_defaults(func=cmd_validate)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.vault = args.vault.resolve()
    return args.func(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
