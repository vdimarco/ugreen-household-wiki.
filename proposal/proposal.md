# Household Wiki: Project Proposal

**Skill name:** household-wiki · **Track:** Open Innovation · **Entrant:** Vaughn DiMarco

<!-- answers-start -->

## 1. What does your Skill do?

It turns a family's documents, photos, and voice memos on the NAS into a private wiki that answers household questions with sources and shows coming dates.

## 2. Who is your target user, and what is their problem?

The person who runs a home. Facts are spread across hundreds of files: receipts, warranties, policies, school letters, lab results, and photos of labels. "When does the car insurance renew?" takes 20 minutes of search. Search finds files. It does not keep knowledge.

## 3. What is your solution?

The LLM Wiki pattern on the NAS. Source files stay read-only. The Skill puts facts into linked Markdown pages, one for each person, pet, appliance, vehicle, provider, and policy. Each fact cites its source. Answers come from the pages.

## 4. What is the main user flow?

Setup: confirm the wiki folder and up to five source folders. Ingest: "Update the wiki." The Skill finds new files, extracts facts, and shows a change set. After approval, it writes the pages, index, and log. Ask: the user gets the answer, the page, and the source file. Tidy: due dates, conflicts, and old pages.

## 5. How is your idea different from existing tools or common AI solutions?

Chat assistants forget and use the cloud. File search returns files, not answers. Note apps need people to type every fact. This wiki maintains itself, logs each change, shows conflicts, and stays at home in plain Markdown that other Skills can read.

## 6. Which UGREEN AI NAS features does your Skill use, and at which step?

- file-agent (ug-filesystem, file-workflow): find new files; read and write pages, index, and log.
- document-agent (ug-document): extract with receipt, invoice, contract, and medical-report schemas (Ingest); answer from sources (Ask); reconcile pages (Tidy).
- photo-agent (ug-photo): OCR and vision on photos of labels and notices (Ingest).
- knowledge-agent (ug-knowledge): transcribe voice memos (Ingest); collect evidence (Ask).

## 7. What is your technical approach?

One SKILL.md with three modes that delegates self-contained tasks to registered experts. log.md stores the source folders and the last ingest time, so each run is incremental: up to 30 files and 10 page changes. All writes go in one confirmed change set, inside the wiki folder only, and add text without removing it. Account numbers keep only the last 4 characters. Passwords are never copied. Only NAS models are used. All five delegation states are handled.

## 8. What have you built so far? What is not built yet? What still needs testing on a NAS?

Built: SKILL.md, wiki format, and fact rules. They pass the uliya-skill-kit static check with 0 errors. Not built: optional tags on files that were read. NAS tests: real expert output, patch writes, approval prompts, run time, and OCR on phone photos.

## 9. How will you test your Skill if you become a Finalist?

Core 1: ingest 12 sample files into an empty wiki. Expect correct pages, a source for each fact, and an updated index and log. Core 2: ask 10 questions. Expect correct answers with sources, and "no answer" when the files have none. Edge: a letter with a conflicting renewal date. Expect an open question with both values and no overwrite.

## 10. What are the known limits, risks, or outside dependencies of your Skill?

Quality depends on NAS OCR, extraction, and transcription. A large first ingest needs several runs. The wiki changes only when asked. Writes can need NAS approval. No medical, legal, or financial advice. It depends only on UGOS experts.

<!-- answers-end -->

## Third-party components and licenses

None. The Skill contains only Markdown. It uses no third-party library, service, or model. It was built and checked with the UGREEN uliya-skill-kit 0.7.3 from the Hackathon Starter Kit, which is not part of the package. AI tool: Claude (Anthropic), used to research, draft, and review the files.
