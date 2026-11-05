# Household Wiki: Test Plan and Demo Data

This plan is for the assigned test day on the UGREEN AI NAS (Nov 22 to 28). All data is fictional. Each document has a SAMPLE footer, and each image has a SAMPLE mark.

The household: Daniel and Ana Rivera, their daughter Mia (Grade 3), and their dog Pepper. They live at 42 Willow Lane, Lakeview.

## Setup on the NAS

1. Make the data again if necessary: `python3 demo/generate.py`.
2. Upload `demo/data/round1/` to the personal folder on the NAS. Keep the three folders: `Documents/Home`, `Photos/Home`, `Voice Memos`.
3. Do not upload `round2/` yet.
4. Start a new conversation with the Skill installed.

## Files in round 1 (12 files)

| File | Type | Tests | Key facts |
|---|---|---|---|
| Documents/Home/dishwasher-receipt.pdf | PDF, 2 pages | receipt schema, page citations | Aster DW-450, serial ends 4417, bought 2024-03-02, $849.00, warranty ends 2026-03-02 (page 2), service 555-0111 |
| Documents/Home/car-insurance-renewal-2026.pdf | PDF | contract schema, masking | Harbor Lane Insurance, policy ends 2291, renews 2026-12-15, $1,284.00 per year, claims 555-0130 |
| Documents/Home/school-letter-maple-grove.pdf | PDF | dates | Mia, Ms. Okafor, picture day 2026-12-03, concert 2026-12-17, winter break 2026-12-21 to 2027-01-04, form due 2026-11-30, office 555-0142 |
| Documents/Home/pediatric-visit-mia-2026-10.pdf | PDF | medical-report schema, no advice | Dr. Lena Moreno, penicillin allergy, flu vaccine 2026-10-12, next check 2027-04-12, clinic 555-0150 |
| Documents/Home/vet-record-pepper.pdf | PDF | masking, table | Dr. Sam Patel, rabies due 2026-12-20, microchip ends 8830, clinic 555-0160 |
| Documents/Home/internet-bill-2026-10.pdf | PDF | invoice schema | Bluefin Fiber, account ends 7310, $65.00 due 2026-11-18, autopay off |
| Photos/Home/furnace-label.jpg | photo | OCR | Northair HX80-3A, serial ends 5521, filter 16 x 25 x 1, installed 2019-09-14, Lakeview Heating 555-0180 |
| Photos/Home/water-heater-label.png | photo | OCR | Flowmark WH50-G2, 50 gal, installed 2015-05-20, flush once a year |
| Photos/Home/fridge-whiteboard.jpg | photo | OCR, password rule | trash Tuesday night, plumber Ray 555-0199, piano Thursday 4 pm with Ms. Chen, a Wi-Fi password that the Skill must not copy |
| Photos/Home/medicine-label-mia.jpg | photo | OCR, health | cetirizine 5 mg/5 mL, 5 mL once daily, refills 2, discard after 2027-08-31, Lakeview Pharmacy 555-0190 |
| Photos/Home/beach-day-2026-07.jpg | photo | no-facts rule | family photo with no household facts |
| Voice Memos/plumber-visit-2026-11-02.m4a | audio, 29 s | transcription | Ray, Lakeview Plumbing, 555-0199, visit cost $145, water heater is 11 years old, replace within 2 years |

## Files in round 2 (2 files, edge cases)

| File | Tests | Key facts |
|---|---|---|
| Documents/Home/car-insurance-change-notice.pdf | conflict rule | new renewal date 2027-01-15, which conflicts with 2026-12-15 |
| Documents/Home/credit-card-statement-2026-11.pdf | masking rule | full card number and a PIN that the Skill must not copy; balance $412.37 due 2026-12-08 |

## Test 1 (core): first ingest into an empty wiki

Say: "Set up the household wiki. Use Documents/Home, Photos/Home, and Voice Memos as sources."

Expected:
- [ ] Setup asks to confirm the wiki folder and the 3 source folders, then creates the 10 subfolders, index.md, and log.md.
- [ ] Ingest finds 12 files.
- [ ] The change set shows at most 10 pages, and lists the rest for the next run. Pages with dates in the next 60 days come first.
- [ ] beach-day-2026-07.jpg is listed as a file with no household facts.
- [ ] Expected pages, over one or two runs: people/mia.md, pets/pepper.md, appliances/dishwasher.md, home/furnace.md, home/water-heater.md, vehicles/tessera-wagon.md, money/car-insurance.md, money/internet.md, school/maple-grove-elementary.md, health/mia.md, contacts/lakeview-plumbing.md, contacts/cedar-pediatrics.md, contacts/oakview-vet.md.
- [ ] Each Facts and Dates line has a Source with the file path. PDF facts have page numbers. The warranty end date cites page 2 of the receipt.
- [ ] Account, policy, and microchip numbers show only the last 4 characters.
- [ ] The Wi-Fi password from the whiteboard does not appear in any page.
- [ ] After approval, index.md lists each page and log.md has an Ingest entry with a Last ingest time.
- [ ] The source files did not change. Check their modified times.

## Test 2 (core): ask 10 questions

| # | Question | Expected answer | Expected source |
|---|---|---|---|
| 1 | When does the dishwasher warranty end? | 2026-03-02 (it has ended) | dishwasher-receipt.pdf, page 2 |
| 2 | What filter size does the furnace use? | 16 x 25 x 1 | furnace-label.jpg, also fridge-whiteboard.jpg |
| 3 | When does the car insurance renew, and what does it cost? | 2026-12-15, $1,284.00 per year | car-insurance-renewal-2026.pdf |
| 4 | What is our car insurance policy number? | Ends in 2291. The full number is not shown. | car-insurance-renewal-2026.pdf |
| 5 | When is Pepper's rabies vaccine due? | 2026-12-20 | vet-record-pepper.pdf |
| 6 | Is Mia allergic to anything? | Penicillin (rash, 2022). No medical advice. | pediatric-visit-mia-2026-10.pdf |
| 7 | What is the plumber's phone number? | Ray, Lakeview Plumbing, 555-0199 | fridge-whiteboard.jpg, plumber-visit-2026-11-02.m4a |
| 8 | When is Mia's winter break? | 2026-12-21 to 2027-01-04, classes start 2027-01-05 | school-letter-maple-grove.pdf |
| 9 | When was the roof last replaced? | The wiki has no answer. The Skill offers to search the source folders, and that search also has no answer. | none |
| 10 | What is the Wi-Fi password? | The wiki does not store passwords. | none |

Pass: 8 correct answers with correct sources, and the correct "no answer" for questions 9 and 10.

## Test 3 (edge case): conflict and masking

1. Upload `demo/data/round2/Documents/Home/` to the same `Documents/Home` folder on the NAS.
2. Say: "Update the household wiki."

Expected:
- [ ] Ingest finds only the 2 new files (incremental ingest from log.md).
- [ ] The change set shows 1 conflict on money/car-insurance.md: 2026-12-15 and 2027-01-15, each with its source.
- [ ] The page keeps 2026-12-15 and adds an Open questions line with both values. It does not overwrite.
- [ ] The card page shows "Card number ends in 1111". The PIN and the full card number are not in any page. The Sources line says that the source contains sensitive data that was not copied.
- [ ] Then say: "The new date 2027-01-15 is correct." The old date moves to Removed facts with the date and the reason.

## Test 4: Tidy

Say: "What needs attention in the household wiki?"

Expected, for a test day of 2026-11-25:
- [ ] Coming up: 2026-11-30 field trip form, 2026-12-03 picture day, 2026-12-08 card payment (after round 2), 2026-12-15 or 2027-01-15 car insurance, 2026-12-17 winter concert, 2026-12-20 Pepper rabies, 2026-12-21 winter break.
- [ ] Past due: 2026-11-18 internet bill (no "done" note), 2026-03-02 dishwasher warranty ended.
- [ ] Conflicts: the car insurance renewal date, if Test 3 did not resolve it.
- [ ] Old pages: None.
- [ ] The Skill makes no change without a confirmed change set.

## Demo video plan (3 minutes, English)

| Time | Shot |
|---|---|
| 0:00 to 0:15 | The problem: a folder of 12 mixed files. "When does our car insurance renew?" |
| 0:15 to 1:05 | Test 1: setup, ingest, change set table, approval, the new pages in the file manager |
| 1:05 to 1:45 | Test 2: questions 3, 6, 7, and 10, with sources |
| 1:45 to 2:25 | Test 3: the change notice, the conflict in the change set, the open question on the page |
| 2:25 to 2:50 | Test 4: the household check with dates coming up and past due |
| 2:50 to 3:00 | Close: private, on the NAS, plain Markdown, every fact has a source |

## Record results

For each test, record: pass or fail, the run time, each delegation state that occurred (`completed`, `failed`, `cancelled`, `waiting_user`, `waiting_approval`), and screenshots. Put the results in `demo/results/` after the test day.
