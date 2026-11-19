# The harness

The harness walks a skill through its steps and checks each step from the
outside: what was read, which commands ran and with what result, which files
were written. It runs as Claude Code hooks shipped with the plugin
(`hooks/hooks.json`), so it works only in Claude Code. In Codex, Cursor and
the other `npx skills` harnesses the skills work without it.

## Where it acts

- **Only in a gm-apprentice vault.** A folder without
  `_meta/vault-state.json` is left alone; the hooks exit before Python
  starts.
- **It only watches until the vault opts in.** Without
  `.claude/harness/modes.json` in the vault, every guard is in observe: it
  adds the current step to the conversation and writes what it would have
  blocked to `.claude/harness/observe.log`, and blocks nothing.
- **Opting in:** copy `harness/modes.example.json` to
  `<vault>/.claude/harness/modes.json`. Opting in blocks for real, even with
  an empty `{}`:
  - the flow guards (`flow.*`) block for a flow marked `mvp` or `validado`
    and watch for one in `rascunho`, unless `modes.json` names them;
  - `confirmacao@_World` and both `forma@` guards block unless `modes.json`
    sets them to `observe` or `off`;
  - the older gates switch on and cannot be set to observe: no vault write
    without a gm-apprentice skill loaded, the per-skill read and command
    gates in `skills.json`, the content check after each note write, and the
    `_midwife/` structure guard.
- **Turning it off:** create `<vault>/.claude/harness/OFF`; delete it to turn
  the harness back on.

## What lives where

| Plugin (`harness/`) | Vault (`.claude/harness/`) |
|---|---|
| `engine/flow.py`: steps, evidence, artifact checks | `modes.json`: which guards block |
| `hooks/*.py`: the hook scripts | `state/`: per-session state, written only by the hooks |
| `flows/<skill>.json`: each skill's steps | `observe.log`, `hook-errors.log` |
| `skills.json`: the older read/command gates | `flows/<skill>.json`, `skills.json`: local versions that win over the plugin's |
| `modes.example.json` | `OFF` |

## Guards

| Guard | What it stops |
|---|---|
| `flow.stop` | ending the turn with a step still open, unless the reply is a short question to the GM that does not claim the work is done |
| `flow.report` | writing a flow's final report before every step has evidence |
| `flow.artifact` | a step file in `_QA/.run/` that fails its check |
| `flow.protect` | editing the harness, the vault's skills, settings or `CLAUDE.md` while a flow runs |
| `confirmacao@_World`, `confirmacao@_midwife` | writing a line the GM was not shown and did not accept (index notes are exempt; "não ..., pode gravar" counts as a yes) |
| `forma@the-midwife`, `forma@ttrpg-expert` | more than one question, or a reply over `forma.max_chars` |

The older gates (`skills.json`, the content check after each note write, the
`_midwife/` structure guard) only block, with no observe mode, so they run
only in a vault that opted in. The `_midwife/` guard lets the shell delete a
single note (no `-r`, no wildcard), since the-midwife drops what was
superseded.

Add `state/`, `observe.log` and `hook-errors.log` under
`.claude/harness/` to the vault's `.gitignore`: `state/` keeps the full text
of each GM turn and proposal for the confirmation guard.

## Moving a vault off its own copy

A vault that ran its own copy of the harness must drop it once the plugin
carries it, or both run. From the vault's `.claude/settings.json` remove the
hooks that call `.claude/harness/hooks/` or `.claude/hooks/midwife-guard.py`.
From `.claude/harness/` delete `engine/`, `hooks/`, `flows/`, `skills.json`
and `tests/`: local `flows/` and `skills.json` win over the plugin's, so an
old copy would hide every later fix. Keep `modes.json`, `state/` and the logs.

## Changing a skill

`tests/test_harness_engine.py` fails when a flow reads a skill file that no
longer exists, or a skill has no flow. Rename a reference file and its flow
in the same change. The harness's own tests live in `harness/tests/` and run
in the same CI step; `test_harness.py` copies a real vault
(`GMA_VAULT=<path>`) and is skipped without one.
