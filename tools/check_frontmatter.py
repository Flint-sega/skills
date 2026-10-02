#!/usr/bin/env python3
"""Frontmatter каждого SKILL.md разбирается как YAML и согласован с каталогом.

Смоук 02.10 поймал: `:` внутри description рвёт YAML — навык не
регистрируется в харнессе, а текстовые ревью этого не видят.
Проверяем: YAML валиден; name совпадает с именем каталога навыка;
description и argument-hint не пусты; metadata.version есть.
"""

import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent

for skill_md in sorted(REPO.glob("skills/*/SKILL.md")):
    raw = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    if not m:
        print("%s: нет frontmatter" % skill_md)
        sys.exit(1)
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        print("%s: YAML не разбирается — %s" % (skill_md, str(e).splitlines()[0]))
        sys.exit(1)
    name = meta.get("name")
    if name != skill_md.parent.name:
        print("%s: name=%r не совпадает с каталогом %r" %
              (skill_md, name, skill_md.parent.name))
        sys.exit(1)
    for field in ("description", "argument-hint"):
        if not meta.get(field):
            print("%s: пусто поле %s" % (skill_md, field))
            sys.exit(1)
    version = (meta.get("metadata") or {}).get("version")
    if not version:
        print("%s: нет metadata.version" % skill_md)
        sys.exit(1)
    print("%s: ok (name=%s, version=%s)" % (skill_md.relative_to(REPO), name, version))
