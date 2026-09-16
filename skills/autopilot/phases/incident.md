# Incident — something broke

**Read this only when the verb is `incident`** — or when a run mid-flight hits a breakage in the thing being built that is bigger than a red test. Two goals, in strict order: **stop the bleeding, then find out why.** The fix is ordinary work that follows the diagnosis; there is no hotfix lane that skips the rules.

## 1. Stop the bleeding — minutes, read-only first

**Look before touching.** A fixed window of read-only looking: logs, state files, versions, what the users see. The temptation is the mirror of the danger — the first plausible lever, pulled on a live system, is how one incident becomes two.

**The rollback is a question, asked in one line, with the evidence attached.** «Откатываемся до <commit/версия>? Сломано <что>, причина пока не ясна, откат возвращает <что>.» Rolling back is an outward-facing change — the safety gates hold in an incident, which is exactly when they are most tempting to skip. One exception: the system is actively destroying data and the rollback stops it — propose in the same one line and act on any affirmative; silence still does not consent.

**Snapshot the evidence before anything changes** — logs, the state as found, versions and commits, the times. Into the run directory (`.autopilot/<dir>/incident-<time>.md`), or a fresh one if no run is open. An incident whose evidence was fixed away has lost its root cause: the fix lands, the mechanism is gone, and the same incident arrives again from a different door.

## 2. Root cause — before any fix

**A cause is a sentence that predicts the breakage; anything less is a guess.** «Дубли в данных роняют парсер, потому что карта собирается конкатенацией» predicts which users break and which do not. «Что-то с данными» is a guess wearing a diagnosis.

The mechanism is found in the evidence, not in the code alone: the failing input, the code path it takes, the state that made today different from yesterday. Then the check that makes it a cause: **it explains every symptom, not just the first one.** A mechanism that covers one symptom and shrugs at the rest is a symptom, restated.

A cause that cannot be found is said so, plainly — «механизм не установлен, вот что исключено» — and the fix becomes containment plus monitoring, named as such. «Вероятно, и починили» is not a state an incident ends in.

## 3. The fix is ordinary work

- **Red test first:** the mechanism, written as a test that fails on the broken code and passes nowhere else. A fix whose test cannot be made red does not fix the mechanism — it hides the symptom.
- **Then the ticket loop, unskipped:** executor contract, review, green suite, one commit (`phases/5-subagents.md`, `phases/6-review.md`). The fast version of an incident fix is the same loop with the small cut — not the same loop with the steps removed. A red suite at the end of an incident is the incident still running.
- **The fix and the diagnosis travel together:** the commit message names the mechanism in one line; the test name does the same.

## 4. The record

Where the project keeps its history is `conventionsFile`'s to say — a journal directory, `docs/adr/`, the memory file. One entry, written once the fix is green:

- what broke, for whom, and when;
- the mechanism, as the sentence that predicts it;
- the fix commit and the test that guards it;
- the lesson — what would have caught it earlier, stated only if it is true.

A decision falls out of the mechanism (a format was wrong, a boundary was in the wrong place) → an ADR, per the project's numbering (`phases/9-memory.md` knows the format).

The user gets one page, not a log: **что случилось, почему, что изменилось, что не даст повториться.**

## Red flags — start the phase over

- a lever pulled before anything was read;
- a fix committed with no red test behind it;
- a «cause» that does not predict the symptoms it is meant to explain;
- the evidence snapshot skipped «потому что торопились» — the phrase that pays for the second incident;
- the same breakage twice, and no record the first time.
