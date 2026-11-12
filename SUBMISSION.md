# Devpost Submission: Household Wiki

Copy each field into the Devpost project form. Round 1 closes Sunday, Nov 15, 2026, at 11:45 PM PT.

## Files to upload

| Devpost item | File | Size | Limit |
|---|---|---|---|
| Project Proposal (PDF) | `proposal/household-wiki-proposal.pdf` | 36 KB, 2 pages, about 475 words | 1 MB, 500 words |
| Pre-test Skill Package (ZIP) | `dist/household-wiki.zip` | 10 KB, 4 files | 10 MB, 100 files, 1 MB per file |
| Cover image (gallery) | `media/cover.png` | 3:2 | none |
| Video demo link (optional) | `demo/video/household-wiki-concept.mp4` | 110 s, 14 MB, 1080p | YouTube, Vimeo, or Youku link only |

## Project name

Household Wiki

## Elevator pitch

A private wiki for your home, built on your NAS from the family's own documents, photos, and voice memos. It answers household questions with sources and shows the dates that are coming up.

## Track

Open Innovation

## About the project

### Inspiration

Each household has hundreds of files with facts that matter: receipts, warranties, insurance policies, school letters, lab results, and photos of labels. When a question comes up, such as "When does the car insurance renew?" or "Which filter does the furnace use?", someone searches for 20 minutes or does not find the answer. Search finds files. It does not keep knowledge. We wanted a home that remembers what its files say.

### What it does

Household Wiki applies the LLM Wiki pattern on the UGREEN AI NAS. The source files stay read-only. The Skill puts the facts into linked Markdown pages: one page for each person, pet, appliance, vehicle, provider, and policy. Each fact cites its source file.

- **Ingest**: finds new files, extracts facts, and shows a change set. It writes pages only after the user approves.
- **Ask**: answers from the wiki, and gives the page and the source file for each part of the answer.
- **Tidy**: lists the dates that are coming up or past due, the facts that conflict, and the pages that are old or have no links.

### How we built it

The Skill is one SKILL.md with two reference files, built with the UGREEN Skill Developer Package (uliya-skill-kit 0.7.3). It delegates self-contained tasks to four registered NAS experts:

- `file-agent`: finds new files, and reads and writes the wiki pages, the index, and the log.
- `document-agent`: extracts facts with the receipt, invoice, contract, and medical-report schemas, and compares pages for conflicts.
- `photo-agent`: reads text in photos of labels and notices.
- `knowledge-agent`: transcribes voice memos and collects evidence for answers.

log.md stores the source folders and the last ingest time, so each run reads only new files.

### Challenges we ran into

- Each write on the NAS can need approval. We put all page changes in one change set, so the user approves once for each run.
- Conflicting facts must not disappear. A new value never replaces an old value. Both go to an "Open questions" section with their sources.
- Sensitive numbers must stay out of the wiki. Account and policy numbers keep only the last 4 characters. Passwords and PINs are never copied.

### Accomplishments that we're proud of

- The package passes the kit's static check with 0 errors and 0 warnings.
- Each fact in the wiki has a source, and the user can check every answer.
- The wiki is plain Markdown. People and other Skills can read it without this Skill.

### What we learned

A household needs knowledge that is compiled once and kept current, more than a better search. A local NAS is the right place for that knowledge, because it is always on, it holds the family's files, and the data stays at home.

### What's next

- Test the Skill on a real UGREEN AI NAS with our 14-file demo set and 10 test questions.
- Optional tags on files that the Skill has read.
- More page types, for example for home maintenance schedules.

## Built with

ugos, ugreen-ai-nas, uliya-skill-kit, markdown, claude

## Try it out

- https://github.com/vdimarco/ugreen-household-wiki.

## Video demo link

Round 1 does not require a video. This concept preview is optional. It explains the idea with fictional sample files and the expected results. It is not a recording on a UGREEN NAS, and every frame says so. Round 2 needs a new video recorded on your assigned NAS (see `demo/video/README.md`).

Devpost does not accept a video file. Upload the video first, then paste the link:

1. Upload `demo/video/household-wiki-concept.mp4` to YouTube. Set it to Public or Unlisted.
2. Use the title and description below.
3. Paste the YouTube link into the Devpost field "Video demo link".

**YouTube title**

Household Wiki: concept preview (UGREEN Hackathon 2026 on AI NAS)

**YouTube description**

Household Wiki is a UGOS Skill that turns a family's documents, photos, and voice memos on a UGREEN AI NAS into a private, linked Markdown wiki. It answers household questions with sources and shows the dates that are coming up.

This video is a concept preview. All files and people are fictional. The change set, pages, answers, and household check on screen are the expected results for the demo files. It is not a recording of the Skill on a UGREEN NAS. The final demo will be recorded on a UGREEN AI NAS in Round 2.

Code and demo files: https://github.com/vdimarco/ugreen-household-wiki.
Entry for the UGREEN Hackathon 2026 on AI NAS, track Open Innovation.

## Before you submit

- [ ] Check the entrant name in the proposal PDF ("Vaughn DiMarco"). Add teammates and their consent if you have any.
- [ ] Confirm on the Devpost Rules tab that a team can enter more than one Skill, if you also submit Shot List Coverage.
- [ ] Upload the PDF and the ZIP above.
- [ ] Optional: upload the concept video to YouTube and paste the link into "Video demo link".
- [ ] Do not add a video or a repo as required items. Round 1 does not need them.
