# Demo Video

## Concept preview (this folder)

`household-wiki-concept.mp4`: 1920 x 1080, 30 fps, 110 seconds, English narration.

**This is a concept preview. It is not a recording of the Skill on a UGREEN AI NAS.** Each frame says so in a banner. It shows:

- the fictional demo files from `../data/`,
- the **expected** change set, wiki pages, answers, and household check from `../test-plan.md`, each labeled as expected,
- an illustration of the conversation, labeled as such.

Use it to explain the idea, for example on the Devpost project page or in a pitch. Do not present it as NAS output.

`household-wiki-concept-storyboard.jpg` shows one frame from each of the 10 scenes.

### Scenes and narration

| # | Scene | Narration |
|---|---|---|
| 1 | Title | Household Wiki. A private wiki for your home, on your UGREEN NAS. This is a concept preview with sample data. |
| 2 | The problem | Your household facts hide in hundreds of files. Receipts, policies, school letters, and photos of labels. When does the car insurance renew? Nobody remembers. |
| 3 | Setup | You choose the folders the Skill can read. It makes a wiki folder with one page for each person, pet, appliance, vehicle, and policy. |
| 4 | Ingest | When you say, update the wiki, the Skill finds new files. The NAS experts read documents, text in photos, and voice memos, and pull out the facts. |
| 5 | Change set | Nothing changes until you approve. You see every page it will create or change, and every conflict it found. |
| 6 | A wiki page | Each page is plain Markdown. Every fact links to its source file, so you can always check it. |
| 7 | Ask | Now ask a question. You get the answer, the wiki page, and the source file. And passwords never go into the wiki. |
| 8 | Conflicts | When a new letter says something different, the Skill keeps both values and asks you. It never overwrites a fact. |
| 9 | Tidy | Ask what needs attention, and you get the dates that are coming up and the ones that are past due. |
| 10 | Close | Household Wiki. Your home's knowledge, kept private, kept current, and always with a source. |

The narration is in `narration/` (Higgsfield Seed Audio, preset voice "Helena", about 7 credits).

### Rebuild

```bash
python3 demo/video/build_concept_video.py demo/video/narration demo/video/household-wiki-concept.mp4
```

Needs Python with Pillow, `ffmpeg`, and `pdftoppm`.

## Motion-graphics version (`household-wiki-motion.mp4`)

`household-wiki-motion.mp4`: 1920 x 1080, 30 fps, 103 seconds. It uses the same 10 narration files and the same facts as the concept preview, with animated scenes built in HyperFrames (HTML and GSAP rendered to video). It has no music.

**It is also a concept preview, not a recording of the Skill on a UGREEN AI NAS.** A label at the top of every frame says: "Concept preview. Fictional sample data. Expected results shown. Not a recording on a UGREEN AI NAS."

The project is in `motion/`: `index.html` holds the scene order, the label, and the narration; `compositions/s1.html` to `s10.html` hold one scene each.

```bash
cd demo/video/motion && npx hyperframes check
```

```bash
cd demo/video/motion && npx hyperframes render -o ../household-wiki-motion.mp4
```

Needs Node.js and `ffmpeg`. The first run downloads the HyperFrames CLI.

A clickable walkthrough with the same content is in `../interactive/index.html`. Open the file in a browser.

## Final Round 2 video (to record on the test day)

The rules require a public YouTube video of no more than 3 minutes, with English narration or English subtitles, that shows the Skill running on **your assigned UGREEN AI NAS** during your assigned testing day.

Plan for the recording:

1. Start a screen recording before the first request. Record Tests 1 to 4 in `../test-plan.md`.
2. Keep the NAS address bar or the device name visible in at least one shot.
3. Show the new wiki folder in the file manager, and open one page, for example `appliances/dishwasher.md`.
4. After the test day, cut the recording to the same 10 scenes. Replace scenes 4 to 9 with the real screen recording. Keep scenes 1 to 3 and 10 if you like.
5. Change the banner text and the title pill. Remove "Concept preview" and "Expected results shown", because the new footage is real. Keep "Fictional sample data".
