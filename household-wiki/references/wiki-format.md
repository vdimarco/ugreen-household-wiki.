# Wiki format

The wiki is a folder of plain Markdown files. People and other Skills can read it without this Skill.

## Folders

| Folder | One page for each |
|---|---|
| people | family member or person who lives in the home |
| pets | pet |
| home | room, home system (heating, water, power, internet), or the property |
| appliances | appliance or device |
| vehicles | car, bike, or other vehicle |
| money | account, policy, bill, subscription, or loan |
| health | person (health facts only, linked to the person page) |
| school | school, class, or activity |
| contacts | service provider, doctor, vet, school office, or tradesperson |
| trips | trip or event |

Page file names use lowercase words with hyphens, for example `appliances/dishwasher.md` or `money/car-insurance.md`.

## Page template

Each page uses these sections in this order. Leave out a section only if it has no content. Do not use empty headings.

```markdown
# Dishwasher

Type: appliance
Summary: Kitchen dishwasher, bought in March 2024.
Last updated: 2026-11-20

## Facts
- Model: SMS6ZCI42E. Source: Documents/Home/dishwasher-receipt.pdf, page 1
- Serial number ends in 4417. Source: Photos/Home/dishwasher-label.jpg

## Dates
- 2026-03-02: Warranty ends. Source: Documents/Home/dishwasher-receipt.pdf, page 2

## Open questions
- Two warranty end dates found: 2026-03-02 (Documents/Home/dishwasher-receipt.pdf) and 2027-03-02 (Documents/Home/extended-warranty.pdf). The user has not confirmed which one is correct.

## Removed facts
- 2026-12-01: Removed "Colour: white". Reason: the user said that it is wrong.

## Related
- [Kitchen](../home/kitchen.md)
- [Appliance store](../contacts/appliance-store.md)

## Sources
- Documents/Home/dishwasher-receipt.pdf (added 2026-11-20)
- Photos/Home/dishwasher-label.jpg (added 2026-11-20)
```

Rules for pages:

- Each line in Facts and Dates ends with "Source:" and the path of the source file. Add the page number for documents and the time in the recording for voice memos.
- Write dates as YYYY-MM-DD.
- Related links use relative Markdown links to other wiki pages.
- Write "Last updated" as the date of the change set that last changed the page.

## index.md

index.md lists every page, grouped by folder, with a one-line summary.

```markdown
# Household Wiki Index

Last updated: 2026-11-20

## Appliances
- [Dishwasher](appliances/dishwasher.md): Kitchen dishwasher, bought in March 2024.

## Money
- [Car insurance](money/car-insurance.md): Policy for the family car, renews each June.
```

At Setup, index.md has only the heading, the Last updated line, and the line "No pages yet."

## log.md

log.md records the source folders and each change. New entries go at the end. Do not change old entries.

```markdown
# Household Wiki Log

## Source folders
- Documents/Home
- Photos/Receipts
- Voice Memos

## Entries

### 2026-11-20 14:05 Ingest
- Files read: 12. Files with no facts: 2. Files not read: 1 (Documents/Home/scan-03.pdf: file is damaged).
- Pages created: appliances/dishwasher.md, money/car-insurance.md
- Pages changed: people/mia.md
- Open questions added: 1
- Last ingest time: 2026-11-20 14:05
- Next run: 4 files left
```

Each Ingest entry has a "Last ingest time" line. Ingest uses the newest "Last ingest time" to find new files. If files are left for the next run, the "Last ingest time" is the modified time of the newest file that this run added.

At Setup, log.md has the heading, the Source folders section, and one entry named Setup with the date and time.
