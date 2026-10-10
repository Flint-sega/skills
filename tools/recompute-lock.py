#!/usr/bin/env python3
"""Пересчёт computedHash в skills-lock.json.

Хеш = sha256 по конкатенации (относительный путь от skills/foreman/ в utf-8 +
байты файла) для всех файлов навыка, отсортированных по пути, без разделителя;
__pycache__ пропускается. Формула верифицирована воспроизведением на деревьях
6adefa5 (df42591e…) и конца прогона редизайна (07468964…).

Файлы собирает `git ls-files`, а не проход по диску: незатреканный мусор под
skills/foreman/ (остатки смока, случайный state.js) не должен молча менять
манифест — на чистом клоне CI тогда отвалился бы на --check.

Режимы:
  (без аргументов)  напечатать хеш
  --check           сравнить с манифестом, код 1 при расхождении (для CI)
  --write           записать хеш в манифест точечной заменой значения
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "foreman"
LOCK = ROOT / "skills-lock.json"


def tracked_files():
    """Пути отслеживаемых файлов навыка; вне git — всё, что на диске без __pycache__."""
    out = subprocess.run(["git", "ls-files", "--", "skills/foreman"],
                         cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        return [p for p in sorted(SKILL.rglob("*"))
                if p.is_file() and "__pycache__" not in p.parts]
    return [ROOT / line for line in out.stdout.splitlines() if line]


def computed_hash():
    digest = hashlib.sha256()
    for path in tracked_files():
        digest.update(path.relative_to(SKILL).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def manifest_hash():
    text = LOCK.read_text(encoding="utf-8")
    found = re.search(r'"computedHash"\s*:\s*"([0-9a-f]{64})"', text)
    return found.group(1) if found else None


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    digest = computed_hash()
    if not mode:
        print(digest)
        return 0
    if mode == "--check":
        current = manifest_hash()
        if current == digest:
            print("computedHash актуален: %s" % digest)
            return 0
        print("РАСХОЖДЕНИЕ: в манифесте %s, по дереву %s" % (current, digest), file=sys.stderr)
        print("запусти: python3 tools/recompute-lock.py --write", file=sys.stderr)
        return 1
    if mode == "--write":
        text = LOCK.read_text(encoding="utf-8")
        updated, count = re.subn(
            r'("computedHash"\s*:\s*")[0-9a-f]{64}(")',
            lambda match: match.group(1) + digest + match.group(2),
            text, count=1)
        if count != 1:
            print("в skills-lock.json не найдено поле computedHash", file=sys.stderr)
            return 1
        LOCK.write_text(updated, encoding="utf-8")
        print("computedHash: %s" % digest)
        return 0
    print("неизвестный режим %r — используй --check или --write" % mode, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
