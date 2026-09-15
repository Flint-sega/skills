#!/usr/bin/env python3
"""Сканер секретов для CI: репо публичное, утечка необратима.

Формы — зеркало редаксионного гейта навыка (phases/1-manifest.md):
тот же набор классов ключей, что навык вычищает из брифов. Сканер
грубее гейта и намеренно таков: здесь лучше ложная тревога, которую
разберёт человек, чем пропущенный токен в публичной истории.

Ложные попадания подавляются строкой-маркером в той же строке файла:
    что-то_похожее_на_ключ  # scan-secrets: allow
"""

import argparse
import pathlib
import re
import subprocess
import sys

ALLOW_MARKER = "scan-secrets: allow"

PATTERNS = [
    ("openai-ключ", re.compile(r"sk-[A-Za-z0-9_-]{20,}")),
    ("github-pat", re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}")),
    ("aws-ключ", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("google-ключ", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("slack-токен", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("telegram-токен", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{35}\b")),
    ("jwt", re.compile(r"eyJ[A-Za-z0-9_-]{15,}\.eyJ[A-Za-z0-9_-]{15,}\.[A-Za-z0-9_-]{10,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("connection-string", re.compile(
        r"(postgres(ql)?|mysql|mongodb(\+srv)?|redis|amqp)://[^\s\"'`]+:[^\s\"'`]+@")),
    ("присвоение-пароля", re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|access[_-]?token)\b['\"]?\s*[:=]\s*['\"][^'\"]{12,}['\"]")),
]


def iter_files(repo: pathlib.Path, paths):
    if paths:
        for arg in paths:
            p = repo / arg
            if p.is_file():
                yield p.relative_to(repo), p
            else:
                for q in sorted(p.rglob("*")):
                    if q.is_file():
                        yield q.relative_to(repo), q
    else:
        out = subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True)
        for name in out.stdout.splitlines():
            p = repo / name
            if p.is_file():
                yield pathlib.Path(name), p


def scan(files):
    findings = []
    for name, path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if ALLOW_MARKER in line:
                continue
            for label, rx in PATTERNS:
                m = rx.search(line)
                if m:
                    findings.append("%s:%d %s %s" % (name, lineno, label, m.group(0)[:12] + "…"))
    return findings


def main():
    ap = argparse.ArgumentParser(description="сканер секретов для публичного репо")
    ap.add_argument("paths", nargs="*", help="сканировать эти пути вместо git ls-files")
    args = ap.parse_args()
    repo = pathlib.Path(__file__).resolve().parent.parent

    findings = scan(iter_files(repo, args.paths))
    for f in findings:
        print(f)
    if findings:
        print("найдено %d подозрительных строк — разберись или пометь «%s»" %
              (len(findings), ALLOW_MARKER))
        return 1
    print("секретов не найдено")
    return 0


if __name__ == "__main__":
    sys.exit(main())
