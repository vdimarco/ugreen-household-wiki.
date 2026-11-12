# Household Wiki

An entry for the [UGREEN Hackathon 2026 on AI NAS](https://ugreenhackathon.devpost.com/), track Open Innovation.

Household Wiki is a UGOS Skill. It turns a family's documents, photos, and voice memos on the NAS into a private, linked Markdown wiki. The wiki answers household questions with sources and shows the dates that are coming up. Source files stay read-only. The Skill writes only after the user confirms a change set.

## Contents

| Path | What it is |
|---|---|
| `household-wiki/` | The Skill package: `SKILL.md` and `references/` |
| `dist/household-wiki.zip` | The Pre-test Skill Package for Round 1 |
| `proposal/` | The Round 1 Project Proposal (Markdown source and PDF) |
| `demo/generate.py` | Makes the fictional demo data set |
| `demo/data/` | The demo data: 12 files for round 1 and 2 edge-case files for round 2 |
| `demo/test-plan.md` | Test cases, expected results, and the demo video plan |
| `demo/video/` | A 110-second concept preview video with narration (clearly labeled, not recorded on a NAS), its builder, and the plan for the Round 2 recording |

## Modes

- **Ingest**: find new files, extract facts, show a change set, and write pages after approval.
- **Ask**: answer from the wiki, with the page and the source file.
- **Tidy**: list due dates, conflicts, old pages, and pages without links.

## Check and build

The static check uses the UGREEN `uliya-skill-kit` 0.7.3 from the [Hackathon Starter Kit](https://ai.ugreen.com/pages/hackathon-starter-kit). The kit is not in this repository.

```bash
node path/to/uliya-skill-kit/scripts/check-skill.mjs household-wiki
```

```bash
rm -f dist/household-wiki.zip && zip -qrX dist/household-wiki.zip household-wiki
```

Last result: `static-pass`, 0 errors, 0 warnings.

## Demo data

```bash
python3 demo/generate.py
```

It needs Python with `reportlab` and `Pillow`, plus `espeak-ng` and `ffmpeg`. All people, companies, and numbers are fictional.
