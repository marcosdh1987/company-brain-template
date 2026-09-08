# Local Agent Rules (`local_model_32k`) — Company Brain

> Opt-in mode for small self-hosted models (Qwen 3.x / 3.6, 27B–35B @ 32k) via
> OpenCode / LM Studio / Ollama, used when Claude Code quota runs out. Short on
> purpose — do not expand it. The rules themselves live in `AGENTS.md`; this file
> only tells a small model how to work inside them without losing the task.

## Rules (in priority order)

1. **Edit, never rewrite.** Change only the lines that need changing. Never
   regenerate a whole document — a full rewrite overruns the response limit and
   silently drops status markers, sources, and IDs.
2. **One thing per turn, then stop.** One decision, one action item, one section.
   If asked to "process everything", do the first extraction step from the
   `AGENTS.md` processing workflow, list the rest deferred (one line each), and stop.
3. **Keep output small.** Aim under ~60 lines: a 3-line preamble, the edit, one
   result line. No analysis blocks, no summaries of the repository.
4. **Read whole, in one call.** Read a file with no line range — one call per
   file. Never read in 100-line chunks, and never inventory a folder.
5. **Declare before editing:** `Target file:` / `Expected change:` / `Validation:`
   (always `make validate`; add `make index` when a work unit changed). Then the
   edit. Then the result line.
6. **Never invent facts.** If the source does not say it, write a `_PENDING_`
   placeholder with an owner, or mark the claim `PENDING VALIDATION` / `INFERRED`
   with the reasoning. Never present a guess as `CONFIRMED`.
7. **Do not touch `06-decisions/` by hand.** New decisions go through the
   `record_decision` skill; existing `DEC-XXX` entries are immutable.
8. **Use the edit tool, not a code block.** Apply changes with the edit tool; do
   not paste full documents into chat.
9. **One increment per chat — then start a NEW chat.** End each validated
   increment with one line: `✅ DONE: <what changed>. NEXT: <one line>. Open a
   NEW chat to continue.` Emit `✅ DONE` only after `make validate` ran and passed.

## "Process the whole inbox" → a loop, not one generation

Decompose into the smallest extractions that each leave `make validate` green
(decisions, then requirements, then open questions, then risks, then action
items — the order in `AGENTS.md`), execute only the next one, then stop.
