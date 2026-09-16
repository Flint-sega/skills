# Verify — blind acceptance, standalone

**Read this only when the verb is `verify`.** This is G4 without the flight: the build already exists — last night's, last week's, someone else's — and the question is whether it does what was asked. Nothing is built here, nothing is fixed here; the output is a verdict.

## What it checks against

A **brief in the user's own words** — a path given with the verb, the open run's brief file, or a program task row quoted verbatim. Never the spec, never the manifest, never the tickets: those are your paraphrase of what was asked, and the whole value of this check is that your paraphrase is not in the room.

## The mechanics — Phase 8's blind acceptance, unchanged

`phases/8-final.md` §1 is the source; what follows is the same check pointed at an arbitrary result.

Spawn one subagent that receives exactly:

- the brief (the whole file, `## Дополнения` included), or the task row quoted verbatim;
- the repo as it stands — checked out at the commit being verified;
- how to run it and how to run the tests.

And **not**: `spec.md`, `manifest.md`, the tickets, `.autopilot/`, or any summary of them. The prohibition is said in the prompt in so many words — «сверяйся только с брифом и с тем, что реально работает» — because the materials are committed and reachable, and only the prompt stops the checker from reading them.

Its brief back to you, verbatim from Phase 8:

- **it runs the project.** «Запусти проект… Чтение кода показывает намерение, запуск показывает результат». A project it could not run is named as such — never passed off as verified by reading;
- a verdict per requirement: реализовано / частично / нет, each with one line of evidence;
- the commands it actually used, verbatim.

## The comparison, and what happens to it

You hold the manifest-equivalent — the brief's requirements as rows — and lay the verdicts against them:

- **agreement everywhere** → the check passed; say so in one line, with what was verified against what.
- **every disagreement goes in the report, unsoftened.** A requirement the verdict calls `нет` is a red row: the result does not do what was asked. You do not explain it away, you do not fix it here — fixing is a ticket like any other (an open run takes it as a дозапрос; a program takes it as a row; no run open, it is the user's to direct).
- if an open run exists, the verdict lands in its `state.js` → `blind`, as Phase 8 would have written it.

## Rules

- **Blind means blind.** The orchestrator does not soften a verdict, does not add context the checker lacked, does not rerun the check «правильнее». A verdict you argue with is a verdict you did not want.
- **You never verify your own sitting.** The agent that built the result does not judge it — the verify verb on work this session just produced is Phase 8's job, and it already runs.
- **A stub is `частично`, not `нет`** — and not `реализовано`. The checker names what works and what is a stub; the row it lands on is the user's call, not the checker's.
- **Unrunnable is a finding**, not a pass and not a failure to execute the verb: the report says «не запустилось: …», and that is the headline finding.
