---
name: household-wiki
description: A private household wiki on the NAS that the assistant builds and keeps current from the family's own documents, photos, and voice memos. It gives answers with sources and a look-ahead of due dates. Use when the user wants to add new files to the household wiki, asks a question about the home, family, pets, vehicles, bills, policies, warranties, school, or health records, or asks what is coming up or what in the wiki needs attention.
---

# Goal

Keep one private set of linked Markdown pages that describes the household, and keep it current from the files the family already stores on the NAS.

The Skill has three modes:

- **Ingest**: find new files in the source folders, extract household facts, and update the wiki after the user confirms a change set.
- **Ask**: answer a household question from the wiki, with the wiki page and the original source file for each part of the answer.
- **Tidy**: report dates that are coming up or past due, facts that conflict, and pages that are old or not linked.

Each fact in the wiki has a link to its source file. The Skill only reads source files. It never changes, moves, or deletes them. The Skill writes only inside the wiki folder, and only after the user confirms the change set.

Supported sources: PDF, Word, text, and Markdown documents; photos and scans of documents, labels, and notices; and voice memos.

Out of scope: web lookups, email, calendars, reminders sent at a set time, and medical, legal, or financial advice. The wiki records facts and their sources only.

# Required input

Collect only these items. If the request already gives an item, do not ask for it again.

1. **Mode**: Ingest, Ask, or Tidy. Find the mode from the request. "Update the wiki" and "add these files" mean Ingest. A question about the household means Ask. "What is coming up" and "check the wiki" mean Tidy. If the mode is not clear, ask one short question.
2. **Wiki folder**: if the user does not name a folder, use the folder named Household Wiki in the personal folder of the current user.
3. **Source folders** (Ingest only, first run only): one to five folders that the user permits the Skill to read. Later runs read this list from the Source folders section of log.md. The user can change the list at any time.
4. **Question** (Ask only): the question in the words of the user.

Do not ask for passwords, PINs, full card numbers, or full ID numbers. Do not collect data that a child expert collects for itself.

Before you send a delegate command, replace each item in square brackets with the real value from this conversation or from a completed result of an earlier step. If you do not have the real value, stop that step and tell the user what is missing.

# Generation-time capability evidence

- `file-workflow` → `file-agent`
- `ug-filesystem` → `file-agent`
- `ug-document` → `document-agent`
- `ug-photo` → `photo-agent`
- `ug-knowledge` → `knowledge-agent`

| Expert | Work in this Skill | Effect |
|---|---|---|
| `file-agent` | Find the personal folder, find new source files, read wiki pages, create folders and pages, add text to pages, and replace index.md | read; state-change with approval |
| `document-agent` | Extract facts from documents (receipt, invoice, contract, and medical-report schemas), answer questions from source documents, and compare wiki pages for conflicts | read |
| `photo-agent` | Read text in images and describe household facts in images | read |
| `knowledge-agent` | Transcribe voice memos and collect evidence from wiki pages | read |

# Workflow

Read [Wiki format](references/wiki-format.md) before you draft a page, an index, or a log entry. Read [Fact rules](references/fact-rules.md) before you draft a change set in Ingest or Tidy.

## Step 0: Find the wiki (all modes)

`delegate --target file-agent --instruction 'Find the household wiki folder. Use this folder if it exists: [wiki folder named by the user, or the folder named Household Wiki in the personal folder of the current user]. Return the full path of the folder, the full text of index.md, and the full text of log.md. If the folder, index.md, or log.md does not exist, say which one is missing. Do not create, change, or move anything.'`

- If the wiki exists, continue with the mode.
- If the wiki does not exist and the mode is Ingest, go to Setup.
- If the wiki does not exist and the mode is Ask or Tidy, tell the user that the wiki is not set up yet and offer Setup. Stop until the user answers.

## Setup (first Ingest only)

1. Ask the user to confirm the wiki folder and one to five source folders. Ask if there are folders or file types to leave out.
2. When the user confirms, send:

`delegate --target file-agent --instruction 'Create the household wiki in this folder: [confirmed wiki folder]. Create these subfolders in it: people, pets, home, appliances, vehicles, money, health, school, contacts, trips. Create index.md with exactly this content: [index text from the Wiki format reference]. Create log.md with exactly this content: [log text with the Source folders section that lists these folders: confirmed source folders, and one Setup entry with the date of today]. Create files only inside this folder. Return the full path of each folder and file that you created.'`

3. When the result is completed, continue with Ingest step I2. Use the real source folders and an empty last ingest time.

## Ingest

**I1. Get the source folders and the last ingest time.** Read them from the log.md text that Step 0 returned. If log.md has no source folders, ask the user for them and add them to the log entry in step I7.

**I2. Find the new files.**

`delegate --target file-agent --instruction 'Search only in these folders and their subfolders: [source folders]. Find files with a modified time after [last ingest time from log.md, or no time limit on the first run]. Include only these file types: pdf, doc, docx, txt, md, jpg, jpeg, png, heic, m4a, mp3, wav. Leave out all files in this folder: [wiki folder path]. Return at most 30 files, oldest first. For each file, return the full path, the file type, the size, and the modified time. Also return the total number of matching files.'`

- If the result is an empty list, tell the user: "No new files since [last ingest time]." Stop.
- If the total is more than 30, tell the user that this run adds the 30 oldest files and the next run continues.

**I3. Read the new files.** Send only the delegations that have files. Use the real paths from the I2 result.

Documents (pdf, doc, docx, txt, md):

`delegate --target document-agent --instruction 'Read these files: [document paths]. For each file, extract the household facts: people, pets, rooms and home systems, appliances, vehicles, service providers and their contact details, accounts and policies, amounts, and each date with its meaning, for example warranty end, renewal, due date, appointment, or expiry. Use the receipt, invoice, contract, or medical-report schema when a file matches it. Show account, policy, and card numbers with only the last 4 characters. For each fact, return the file path and the page number. Do not guess missing values. Return the files that you could not read as a separate list with the reason.'`

Images (jpg, jpeg, png, heic):

`delegate --target photo-agent --instruction 'For each of these images: [image paths]. Read all text in the image. Then list only household facts that the image shows, for example a product label with model and serial number, a bill, a notice, a school letter, a whiteboard, or a medicine label. Show account and card numbers with only the last 4 characters. For each image, return the path, the text that you found, and the facts. If an image shows no household facts, mark it as no facts and do not describe it.'`

Voice memos (m4a, mp3, wav):

`delegate --target knowledge-agent --instruction 'Transcribe these audio files: [audio paths]. For each file, return the path and the full transcript. Mark the parts where the transcription quality is low. Do not summarize.'`

From each transcript, extract the household facts yourself with the rules in [Fact rules](references/fact-rules.md). Cite the audio file and the time in the recording.

If all three results have no facts, tell the user that the new files have no household facts, list the files, and go to step I7 to record only the log entry.

**I4. Read the related wiki pages.** From index.md, select the pages for the people, items, providers, and policies in the real I3 results.

`delegate --target file-agent --instruction 'In this folder only: [wiki folder path]. Return the full text of each of these pages: [page paths selected from index.md]. If a page does not exist, say so. Do not change any file.'`

**I5. Draft the change set.** Follow [Fact rules](references/fact-rules.md). Use only facts from the real results of I3 and the real page text from I4. A change set has at most 10 page changes. List the other changes as "for the next run".

**I6. Show the change set and get confirmation.** Show a short table with one row for each page: page path, new or changed, facts added, and conflicts found. Below the table, show the files with no facts and the files that the experts could not read. Then ask: "Apply all, apply some, or cancel?"

- If the user cancels, stop. Report that the wiki did not change.
- If the user selects some pages, remove the other pages from the change set.

**I7. Write the change set.**

`delegate --target file-agent --instruction 'Work only inside this folder: [wiki folder path]. Apply this confirmed change set. Create these new pages with exactly this content: [new page paths and their full content]. In these existing pages, add this text at the end of the named section and keep all other text unchanged: [page paths, section names, and the text to add]. Replace index.md with exactly this content: [full new index text]. Add this entry to the end of log.md: [log entry]. Do not delete, move, or rename any file. Do not change files outside this folder. Return each file that you created or changed and the result for each file.'`

**I8. Report.** Show the pages created, the pages changed, the open questions added, and the files left for the next run. Report only changes that the I7 result shows as done.

## Ask

**A1. Find the answer in the wiki.**

`delegate --target knowledge-agent --instruction 'Find evidence that answers this question: [question of the user]. Search only the Markdown files in this folder and its subfolders: [wiki folder path]. Return each passage that helps answer the question, with the file path. If no file answers the question, say that there are no results.'`

If you need the full page to answer, read it with the I4 delegation and the real page paths.

**A2. Answer.** Give a short answer first. Then give the wiki page for each part of the answer and the original source file from the Sources section of that page. If the page has an open question about the same fact, show both values and say that they conflict.

**A3. If the wiki has no answer.** Tell the user: "The wiki has no answer to this question." Ask if the Skill can look in the source folders. Only if the user says yes, send:

`delegate --target document-agent --instruction 'Answer this question: [question of the user]. Use only files in these folders: [source folders from log.md]. Return the answer with the file path and the page number for each part of the answer. If the files do not answer the question, say that there are no results. Do not change any file.'`

If this search finds an answer, give it with its sources and offer to add that file in the next Ingest. If the result is empty, say that the files have no answer. Do not give an answer from general knowledge as a household fact.

## Tidy

**T1. Read the wiki.**

`delegate --target file-agent --instruction 'List all Markdown files in this folder and its subfolders: [wiki folder path]. For each file, return the full path, the modified time, and the full text. If there are more than 40 files, return the text of the 40 files that changed most recently, and return the total number of files. Do not change any file.'`

**T2. Find conflicts.**

`delegate --target document-agent --instruction 'Compare these wiki pages: [page paths from the T1 result]. Find facts that conflict, for example two different dates, amounts, model numbers, or phone numbers for the same person, item, provider, or policy. For each conflict, return both values, the page path of each value, and the source file named on each page. Do not change any file.'`

**T3. Make the household check.** From the real T1 and T2 results, and with the date of today, make these lists:

- **Coming up**: dates in the next 60 days, earliest first.
- **Past due**: dates before today that have no "done" note.
- **Conflicts**: the T2 result and the open questions on the pages.
- **Old pages**: pages with a Last updated date more than 12 months ago.
- **Pages without links**: pages that index.md does not list, or that no other page links to.

If a list is empty, write "None" for that list.

**T4. Offer fixes.** If the user wants fixes, draft a change set with [Fact rules](references/fact-rules.md) and continue with steps I6 and I7. Tidy does not remove facts. A fact that the user marks as wrong goes to the Removed facts section of its page, with the date and the reason.

# Completion and failure

Handle each delegation state as follows:

- `completed`: use only the real result that the expert returned. Pass only that real result to the next step. If the result is an empty result, say so and stop the steps that need it.
- `failed`: tell the user which step failed and the reason that the expert gave. Stop the steps that need that result. Keep the results of other steps. In I3, if one file type fails, continue with the other types and list the failed files in the change set.
- `cancelled`: stop the mode. Tell the user what was done before the cancel. Write nothing more.
- `waiting_user`: give the question of the expert to the user in plain words. Wait for the answer. Then continue the same step.
- `waiting_approval`: tell the user that the NAS asks for approval, and say which files will change. Wait. Do not report the change as done until the step result is `completed`.

Partial writes: if I7 completes only part of the change set, list the files that changed and the files that did not change. Do not try again without the user. If log.md did not change but pages changed, tell the user that the next Ingest will find the same files again, and offer to write only the log entry.

Never invent household data. Never report a fact without its source file. Never report a NAS action as done from local drafts or static checks.

# Safety rules

- Read source files only. Write only inside the wiki folder.
- Get the user's confirmation of the change set before each write.
- Show account, policy, and card numbers with only the last 4 characters. Do not copy passwords, PINs, full card numbers, or full ID numbers into the wiki. If a source contains them, write only "This source contains sensitive data that was not copied."
- Give facts and sources. Do not give medical, legal, or financial advice.
- Send NAS work only as delegations to the four experts in this Skill. Never call cli.invoke from this Skill.
- Reply in the language of the user. Do not translate page paths, file names, expert names, or status values.

# References

- [Wiki format](references/wiki-format.md): folders, page template, index.md, and log.md. Read before you draft any wiki text.
- [Fact rules](references/fact-rules.md): how to extract, merge, cite, and mask facts, how to record conflicts, and the change set limits. Read in Ingest and Tidy.
- [Disclosures](references/disclosures.md): third-party components, work done for the Hackathon, and AI tools used.
