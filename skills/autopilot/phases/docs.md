# Docs — the project described from what was built

**Read this only when the verb is `docs`.** The project works; its documentation says something else — or says nothing, or was never written. This verb rewrites the description from the code that exists. The principle is inherited from the memory agent (`phases/9-memory.md`, moment 3): **from the code, never from the plan** — documentation written from a spec describes a project that does not exist, and does it confidently.

## Blind the same way

The docs agent — a subagent, not you (`phases/5-subagents.md` rule 5 holds; at a one-file scale the verb is T0 and you are the crew) — gets the repo and `conventionsFile`, and **not** `spec.md`, the tickets, or the run dir. What the project calls its parts is the conventions file's to say; what it intended is nobody's business here. The one thing being described is what is on disk.

## What gets written, and to where

- **README** — what this is, for whom; install; run; test. Ten honest lines beat a page of aspiration.
- **The memory file**, between the markers, per the rules `phases/9-memory.md` already carries — the docs verb is that agent's job offered standalone, and does not invent a second set of rules. Anything the user wrote outside the markers is untouchable, here as there.
- **A docs/ structure only if one already exists** or `conventionsFile` names a place for one. A docs tree invented by the writing agent is documentation of the writing agent.

## Mechanics

- **Every command is executed before it is documented.** Install, run, test — run them, read the output, write what happened. A command that was not run is not written; a command that fails is a finding about the project, reported — not documented with a «должно сработать».
- **The tree is described as built:** entry points, key files, how the parts talk — from opening them, not from filenames and hope. A structure section that misnames a directory poisons every section after it.
- **No fact about the user is invented**: prices, accounts, addresses, deployment targets stay visibly empty until the user supplies them — the same rule the build flight works under, and for the same reason.
- **Length is a quality, not a virtue:** each file says its one job and stops. Documentation nobody finishes reading documents nothing.

## Gates

- every documented command ran green in this sitting;
- nothing documented that is not on disk — no planned files, no intended behaviour;
- the user's own words outside the markers, byte for byte;
- a reviewer pass over the diff, Craft axis is enough — the finding class here is «написано не про то, что на диске».
