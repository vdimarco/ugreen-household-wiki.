# Fact rules

## What is a household fact

A household fact is a fact that helps a person run the home. Examples:

- Model numbers, serial numbers, sizes, and parts of appliances, vehicles, and home systems.
- Dates and their meaning: warranty end, renewal, due date, appointment, expiry, service interval, school term.
- Service providers and their contact details.
- Accounts, policies, bills, and subscriptions, with amounts and payment dates.
- Health facts that a document states: medicines and doses on a label, allergies, vaccination dates, the doctor or clinic, and the date of a test result.
- Pet facts: vet, vaccinations, food, microchip number with only the last 4 characters.

These are not household facts. Do not add them to the wiki: opinions, private messages, descriptions of family moments in photos, and facts about people outside the household that are not contact details for a service.

## Extract

- Use only text that the expert returned. Do not add facts from general knowledge.
- Keep the exact value from the source, for example the exact model number or amount.
- Give each fact one source: the file path, plus the page number or the time in the recording.
- If the transcription or the text is marked as low quality, add "(low quality source)" after the fact.

## Mask

- Account, policy, card, and microchip numbers: show only the last 4 characters, for example "Policy number ends in 2291."
- Never copy passwords, PINs, security codes, full card numbers, or full ID numbers. Write "This source contains sensitive data that was not copied." in the Sources line for that file.

## Merge

- One page for each person, pet, item, provider, or policy. Before you create a page, look in index.md for a page with the same item. Use the same page if the name, model, or number matches.
- If a fact is already on the page with the same value, add only the new source to the Sources section.
- If a fact is new, add it at the end of the correct section.
- Add a Related link in both pages when two pages are about connected items, for example a person and their doctor.

## Conflicts

- If a new value is different from the value on the page, do not replace the old value.
- Add a line in Open questions with both values and the source of each value.
- In the change set table, show the conflict so that the user can decide.
- If the user decides in the conversation, move the wrong value to Removed facts with the date and the reason, and keep the correct value in Facts.

## Change set limits

- At most 10 page changes in one change set. index.md and log.md do not count.
- Put the pages with dates in the next 60 days first, then new pages, then changed pages.
- List the changes that do not fit as "for the next run" in the change set and in the log entry.
- A change set never deletes a page and never removes text. Tidy moves a wrong fact to Removed facts only after the user confirms it.

## Change set table

Show the change set to the user in this format before each write:

| Page | New or changed | Facts added | Conflicts |
|---|---|---|---|
| appliances/dishwasher.md | New | 3 | 0 |
| money/car-insurance.md | Changed | 1 | 1 |

Below the table, list:

- Files with no household facts.
- Files that the experts could not read, with the reason.
- Changes for the next run.
