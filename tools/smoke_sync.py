#!/usr/bin/env python3
"""CI-smoke: sync.py вписывает состояние в дашборд и не ломает state.js.

Воспроизводит минимальный прогон во временной папке: копия шаблона,
копия sync.py, валидный state.js — и оба утверждения, ради которых
скрипт существует: снимок действительно попал между маркеры, а state.js
после автоматики sync.py по-прежнему разбирается как JSON.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "autopilot"
BEGIN, END = "/*STATE-BEGIN*/", "/*STATE-END*/"

STAGES = ["preflight", "manifest", "briefing", "spec", "plan", "build", "review", "final"]


def make_state():
    stamp = "2026-01-01T00:00:00+00:00"
    return {
        "slug": "smoke",
        "dir": "",
        "title": "smoke",
        "mode": "semi",
        "depth": "normal",
        "polish": False,
        "tier": 0,
        "briefFile": "",
        "memoryFile": "",
        "skillDir": str(SKILL),
        "startedAt": stamp,
        "updatedAt": stamp,
        "finishedAt": None,
        "stages": [{"id": s, "status": "done", "startedAt": stamp, "finishedAt": stamp}
                   for s in STAGES],
        "requirements": {"total": 1, "done": 1, "inTicket": 0, "inSpec": 0,
                         "placeholder": 0, "deferred": 0, "dropped": 0},
        "tickets": [],
        "tests": "",
        "debt": {"placeholders": [], "assumptions": [], "emptyEnv": []},
    }


def main():
    with tempfile.TemporaryDirectory() as td:
        run = pathlib.Path(td)
        shutil.copy(SKILL / "phases" / "dashboard-template.html", run / "dashboard.html")
        shutil.copy(SKILL / "tools" / "sync.py", run / "sync.py")
        (run / "state.js").write_text(
            "window.STATE =\n" + json.dumps(make_state(), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

        r = subprocess.run([sys.executable, str(run / "sync.py"), "--no-serve"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout + r.stderr)
            return 1

        page = (run / "dashboard.html").read_text(encoding="utf-8")
        i, j = page.find(BEGIN), page.find(END)
        if i < 0 or j < 0:
            print("маркеры снимка не найдены в dashboard.html")
            return 1
        if '"smoke"' not in page[i:j]:
            print("снимок не попал между маркеры")
            return 1

        raw = (run / "state.js").read_text(encoding="utf-8")
        try:
            state = json.loads(raw.split("=", 1)[1].strip().rstrip(";"))
        except json.JSONDecodeError as e:
            print("state.js не разбирается после sync.py: %s" % e)
            return 1
        if state["slug"] != "smoke":
            print("state.js потерял содержимое после sync.py")
            return 1

    print("smoke: снимок вписан, state.js валиден")
    return 0


if __name__ == "__main__":
    sys.exit(main())
