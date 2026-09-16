# Program — a long plan executed task by task

**Read this only when the verb is `program`.** A build flight takes one idea to one landed project; a program is work too big for that — weeks of tasks that live in a file both the user and the agent read, each task landing as its own commit, the file itself recording what is done. The program file is the user's; the flights that execute it are yours.

## The program file

Named by the argument after the verb, else `STATE.md` at the repo root, else any root file with this shape. The shape:

```markdown
# <Название программы>

Обновлено: <дата>. Этап: <где программа сейчас>.

## Следующий шаг

<одна-две строки: что делается следующим>

## Задачи

| # | Задача | Статус | PR |
|---|---|---|---|
| 1 | что сделать | done | #12 |
| 2 | что сделать | doing | — |

## Блокеры

| Что нужно | Статус |
|---|---|
| решение владельца | ждёт |
```

Statuses: `todo` · `doing` · `done` · `blocked`. The «Блокеры» table holds what only the user can give. Three rules hold the file together:

- **A row is a requirement.** It was written by the user, and only the user removes or rewrites one — quoted, like any requirement removal. The agent adds rows only from what the build proved (`D##` in spirit: what was discovered, with the date), never from its own ideas.
- **`done` means it is true on disk** — the change committed, the suite green, the PR merged where the project's discipline uses PRs. An open PR is `doing`, however finished it looks.
- **«Следующий шаг» and «Обновлено» move at the end of every task block**, not continuously. They are the first thing the next session reads; a stale pointer costs a session.

## A session with the program

One sitting = one ordinary flight, named `<date>-program`. Phase 0 runs as always — the sitting gets its own `.autopilot/` run, its own instruments; **step 2 reads the program file alongside `conventionsFile`**. Then, per task:

1. **Pick the frontier task.** «Следующий шаг» names it if it names one; otherwise the top `todo` whose blockers are satisfied. «Блокеры» rows that name the user are questions asked now, in one line each — not silently waited on.
2. **The row is the brief.** Quote it verbatim into a one-row manifest. The dials apply as always: mode decides who closes the gaps in a thin row, depth decides how far past its words the work goes.
3. **Cut to the tier the task deserves** — most program tasks are T0 or T1, and the usual rules decide (`phases/4-plan.md`). A task that cuts to T2+ is a task worth telling the user about before it flies.
4. **Build and review unchanged** — `phases/5-subagents.md`, `phases/6-review.md`, executor contract, green suite, one commit per ticket.
5. **Land, then update the file.** The row flips to `done` only per the rule above; the PR column takes the number; «Следующий шаг» moves to what is now frontier; «Обновлено» takes today. Where the project keeps a journal, one line lands there — where it keeps one is `conventionsFile`'s to say; the sitting invents no files.
6. **One line to the user:** «Задача 3 готова: карты доставлены — 4 из 10 в программе».

## Gates

- **G3 per task:** the row traces to its ticket, the ticket traces to its row. A ticket nobody's row ordered is cut.
- **G4 per block:** at the end of a sitting — or when the user asks — the verify verb runs over the sitting's rows (`phases/verify.md`).
- **A task the build proves wrong** is not quietly rewritten: the finding lands in the row's status (`blocked` + a line under it), the user re-cuts it in their words.

## What a program sitting is not

- **Not a licence to skip the manifest.** A thin row is still quoted; a task «маленькая, соберу сразу» is exactly the task that ships the wrong thing quietly.
- **Not a second memory.** The program file says what is done and what is next; the memory file says what the project is; the run dir holds the sitting's evidence. Three jobs, three files — folding any two into one loses the third.
