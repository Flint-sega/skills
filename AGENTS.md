<!-- autopilot:start -->
# skills — репозиторий навыка foreman (Flint-sega/skills)

Вырос из nick-vels/skills (autopilot) и развивается самостоятельно: конвейеры сборки навыков (foreman и другие) с тестами и CI. Пайплайны лежат в `skills/<имя>/` (SKILL.md + phases/ + prompts/ + tools/), проверяются `tests/` и GitHub Actions.

## Команды

| Команда | Что делает |
|---------|------------|
| `python3 -m py_compile tools/*.py skills/foreman/tools/ap.py tests/*.py` | Синтаксис всех Python-файлов |
| `python3 tools/check_frontmatter.py` | Frontmatter всех SKILL.md (нужен `pyyaml`) |
| `python3 -m unittest discover -s tests` | Тесты (41); один файл: `python3 -m unittest tests.test_ap -v` |
| `python3 tools/scan_secrets.py` | Скан секретов |
| `python3 tools/recompute-lock.py --check` | computedHash манифеста актуален (шестой шаг CI); `--write` — записать |
| `node -e "const fs=require('fs');const html=fs.readFileSync('skills/foreman/phases/dashboard-template.html','utf8');new Function(html.match(/<script>([\s\S]*?)<\/script>/g).map(s=>s.replace(/<\/?script>/g,'')).join('\n'));console.log('template JS: parses');"` | JS шаблона дашборда парсится (тот же шаг в CI) |
| `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"` | CI-файл — валидный YAML |

## Где что

- `skills/foreman/` — единственный навык репо: SKILL.md, `phases/` (регламент конвейера + `dashboard-template.html` — шаблон дашборда прогона), `prompts/`, `tools/ap.py` — движок прогона.
- `tests/test_ap.py`, `tests/test_custom_stages.py` — unittest поверх ap.py; гоняют шаблон+ap.py во временной папке.
- `tools/` — `check_frontmatter.py`, `scan_secrets.py`, `measure-run.py`, `recompute-lock.py`.
- `skills-lock.json` — манифест хэшей; из него правится только поле `computedHash` (инструментом `tools/recompute-lock.py --write`).
- `.github/workflows/ci.yml` — шесть шагов, те же команды, что в таблице выше.
- `CHANGELOG.md` — журнал изменений навыка.

## Подводные камни

- `skills-lock.json` `computedHash` = sha256 по путям ОТНОСИТЕЛЬНО `skills/foreman/` (например `"SKILL.md"`, `"phases/..."`) + байтам файлов, отсортированным по пути, без разделителя и без `__pycache__` — формула верифицирована воспроизведением на деревьях 6adefa5 (df42591e…) и редизайна (07468964…). Правка любого файла навыка обязана обновлять это поле: `python3 tools/recompute-lock.py --write`, проверка — `--check`.
- Апстрим nick-vels/skills с 2.1.0 (326c6ea) самостоятельно разошёлся: НЕ мержим. Шаблон дашборда foreman — свой контент; изменения `ap.py` апстрима переносим выборочно по его чейнджлогу, при реальной нужде.
- Mimosa-хук: пишет исходники только через Write/Edit (Bash-запись режет); git-коммиты может блокировать при высоких находках в существующем коде (не в твоём diff) — тогда работа идёт без коммитов, а вопрос решает владелец.
- Шаблон дашборда `skills/foreman/phases/dashboard-template.html` — контракт с живыми прогонами: маркеры `/*STATE-BEGIN*/…/*STATE-END*/` и формат `window.STATE={…};`, порядок тегов (снапшот → state.js → рантайм), `POLL_MS=10000`, ключи localStorage `autopilot-theme/lang/beats:<slug>:<startedAt>`, `#link` вне `#app`, две пары `<script>` без атрибутов (снапшот-заглушка и рантайм; CI-регэксп склеивает их в один блок).
- Локальный смоук дашборда — только во временной папке (/tmp): скопировать туда шаблон и ap.py, там init; в корне репо живой прогон, `ap.py init` в нём откажется.

## Как здесь работает Foreman

Сборка ведётся навыком `/foreman`. Требования, спецификация и таски — в `.autopilot/`.
Прогресс — `.autopilot/dashboard.html`. Требование из `manifest.md` может снять
только пользователь. Прерванную сборку продолжает «продолжи прогон».
<!-- autopilot:end -->
