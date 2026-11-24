# Integrity

Regenerated 24 November 2026 while reformatting `journals/02_Research_Log_and_Weekly_Reviews_EN.docx` and `journals/01_Process_Journal_EN.docx` into the course log structure. This file does not audit a live Cursor session.

## What exists in this folder

- Process-journal entries, all `reconstructed: true`: 6 files in `my_work/process_journal/`, dated 12, 14 (two events), 16, 23, and 24 November 2026.
- Decision records, all `reconstructed: true`: DEC-001 through DEC-006. Timestamps are the reconstruction time, 24 November 2026, 13:46 +08:00. Original clock times were not in the source. `refers_to_turn` is NA because no exchange log exists. `disposition` is `unknown` because the source does not say whether an agent suggestion was accepted, modified, or rejected.
- Weekly summaries, all reconstructed: `weekly/WK-12_summary.md`, `WK-13_summary.md`, `WK-14_summary.md`. Student review boxes are unchecked.
- Session file: `sessions/2026-11-24_1346.jsonl`. It has 6 exchange lines and 6 disposition lines, all flagged `reconstructed`, all timestamped 24 November 2026. Each line restates one journal entry. It is not a live chat, and it is not backdated to 12–23 November.

## Checks

- Sessions logged versus git commits: one reconstructed session file, and this folder is not a git repository. No comparison was possible.
- Exchanges with no disposition: none. Turns 1–6 each have a disposition, and every disposition is `unknown`.
- `reconstructed: true`: 6 journal entries, 6 decision records, 3 weekly summaries, and all 12 lines in the session file.
- Gap longer than seven days: everything before 9 November 2026 is absent from the source. The source says not to invent those weeks. 17–22 November has no dated event, only the weekly band.
- Decision records pointing at turns that do not exist: DEC-001 through DEC-006. `refers_to_turn` is NA on each, on purpose.

## Separate from this folder

The course repository `artd8105_zhaijiayu` has another log at `_research_log/`, not in this submission folder: session files `2026-08-26_1250.jsonl`, `2026-08-30_1048.jsonl`, and `2026-10-21_1217.jsonl`, plus DEC-001, DEC-002, and DEC-003. Those DEC numbers are a different series about the early instruction exercise. They were not copied here and are not counted above. There is no `weekly/` directory and no `INTEGRITY.md` in that repository log.

## Not claimed

This reformatting does not verify model names, prompts, masks, RAW files, or a GitHub push.
