#!/usr/bin/env python3
"""Build the Household Wiki concept preview video.

This video is a concept preview. It shows the demo files in demo/data and the
expected results from demo/test-plan.md. It is not a recording of the Skill on a
UGREEN AI NAS. The Round 2 video must be recorded on the assigned NAS; see
demo/video/README.md.

Usage:
    python3 demo/video/build_concept_video.py NARRATION_DIR OUT.mp4

NARRATION_DIR holds scene1 ... scene10 audio files (wav, mp3, or m4a).
Needs Pillow, ffmpeg, and pdftoppm.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DEMO = Path(__file__).resolve().parents[1]
R1, R2 = DEMO / "data/round1", DEMO / "data/round2"
W, H = 1920, 1080
BG, PANEL, FG, MUTED = (16, 34, 32), (28, 52, 49), (244, 247, 246), (156, 178, 172)
MINT, AMBER, RED, BLUE = (140, 215, 190), (236, 182, 62), (222, 96, 90), (150, 190, 240)
BANNER = "CONCEPT PREVIEW  ·  Fictional sample data  ·  Expected results shown  ·  Not recorded on a UGREEN NAS"


def font(size, bold=False, mono=False):
    name = ("DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf") if mono else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    for p in Path("/usr/share/fonts").rglob(name):
        return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def canvas():
    im = Image.new("RGB", (W, H), BG)
    return im, ImageDraw.Draw(im)


def banner_strip():
    im = Image.new("RGB", (W, 46), (8, 18, 17))
    d = ImageDraw.Draw(im)
    f = font(20, True)
    d.text(((W - d.textlength(BANNER, font=f)) / 2, 10), BANNER, fill=(255, 210, 120), font=f)
    return im


def fit(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((int(im.width * r), int(im.height * r)))


def cover(path, w, h):
    im = Image.open(path).convert("RGB")
    r = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1))
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def pdf_page(pdf, tmp, page=1, res=80):
    out = Path(tmp) / f"{pdf.stem}-{page}"
    subprocess.run(["pdftoppm", "-r", str(res), "-png", "-f", str(page), "-l", str(page), "-singlefile", str(pdf), str(out)], check=True)
    return Image.open(str(out) + ".png").convert("RGB")


def title(d, text, sub=None):
    d.text((90, 50), text, fill=FG, font=font(54, True))
    if sub:
        d.text((92, 125), sub, fill=MUTED, font=font(28))


def pill(d, x, y, text, color, size=28):
    f = font(size, True)
    tw = d.textlength(text, font=f)
    d.rounded_rectangle((x, y, x + tw + 40, y + size + 22), (size + 22) // 2, fill=color)
    d.text((x + 20, y + 10), text, fill=(18, 22, 22), font=f)
    return tw + 40


def wrap(d, text, f, width):
    out, cur = [], ""
    for w_ in text.split():
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=f) > width and cur:
            out.append(cur)
            cur = w_
        else:
            cur = t
    return out + [cur]


def bubble(d, x, y, w, text, who, color, size=30):
    f = font(size)
    lines = []
    for para in text.split("\n"):
        lines += wrap(d, para, f, w - 60)
    h = 52 + int(size * 1.4) * len(lines) + 26
    d.rounded_rectangle((x, y, x + w, y + h), 26, fill=color)
    d.text((x + 30, y + 14), who, fill=MUTED, font=font(22, True))
    for i, ln in enumerate(lines):
        d.text((x + 30, y + 50 + i * int(size * 1.4)), ln, fill=FG, font=f)
    return y + h + 24


def md_panel(d, x, y, w, lines, size=26):
    """Draw Markdown text in a panel. Lines starting with # are headings."""
    lh = int(size * 1.45)
    h = 40 + lh * len(lines)
    d.rounded_rectangle((x, y, x + w, y + h), 18, fill=(250, 250, 247))
    for i, ln in enumerate(lines):
        bold = ln.startswith("#")
        color = (20, 70, 60) if bold else (35, 38, 40)
        if "Source:" in ln:
            a, b = ln.split("Source:", 1)
            d.text((x + 28, y + 20 + i * lh), a, fill=color, font=font(size, mono=True))
            d.text((x + 28 + d.textlength(a, font=font(size, mono=True)), y + 20 + i * lh), "Source:" + b, fill=(30, 110, 160), font=font(size, mono=True))
        else:
            d.text((x + 28, y + 20 + i * lh), ln, fill=color, font=font(size, bold, mono=True))
    return y + h


# ---------- Scenes ----------

def s1():
    im, d = canvas()
    nodes = [(1180, 180, "people"), (1520, 140, "appliances"), (1760, 300, "money"), (1260, 380, "pets"), (1560, 450, "home"), (1220, 600, "school"), (1640, 660, "health")]
    for a, b in [(0, 1), (1, 2), (0, 3), (3, 4), (4, 2), (3, 5), (5, 6), (4, 6), (1, 4)]:
        d.line((nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1]), fill=(80, 150, 130), width=5)
    for x, y, t in nodes:
        t += ".md"
        w = d.textlength(t, font=font(28, True)) / 2 + 24
        d.rounded_rectangle((x - w, y - 36, x + w, y + 36), 14, fill=(245, 248, 246), outline=(80, 150, 130), width=4)
        d.text((x - w + 24, y - 18), t, fill=(25, 70, 60), font=font(28, True))
    d.text((90, 300), "Household Wiki", fill=FG, font=font(104, True))
    d.text((94, 440), "A private wiki for your home,", fill=MUTED, font=font(44))
    d.text((94, 500), "on your UGREEN AI NAS", fill=MUTED, font=font(44))
    pill(d, 94, 620, "Concept preview with sample data", AMBER, 30)
    d.text((94, 900), "UGREEN Hackathon 2026 on AI NAS  ·  Track: Open Innovation", fill=MUTED, font=font(28))
    return im


def s2(tmp):
    im, d = canvas()
    docs = sorted((R1 / "Documents/Home").glob("*.pdf"))
    pics = sorted((R1 / "Photos/Home").glob("*"))
    x, y = 90, 60
    for p in docs:
        pg = fit(pdf_page(p, tmp, res=50), 270, 350)
        im.paste(pg, (x, y))
        x += 300
    x, y = 90, 450
    for p in pics:
        im.paste(cover(p, 330, 230), (x, y))
        x += 350
    d.text((90, 740), "14 files  ·  3 folders  ·  receipts, policies, letters, labels, a voice memo", fill=FG, font=font(40, True))
    d.text((90, 820), "\"When does the car insurance renew?\"", fill=(255, 210, 120), font=font(46, True))
    d.text((90, 895), "The answer is in there. Finding it takes 20 minutes.", fill=MUTED, font=font(34))
    return im


def s3():
    im, d = canvas()
    title(d, "Setup", "You choose the source folders. The Skill only reads them.")
    y = 240
    for name, n in (("Documents/Home", 6), ("Photos/Home", 5), ("Voice Memos", 1)):
        d.rounded_rectangle((90, y, 760, y + 110), 18, fill=PANEL)
        d.text((130, y + 22), name, fill=FG, font=font(38, True))
        d.text((130, y + 70), f"{n} file{'s' if n > 1 else ''}  ·  read-only", fill=MUTED, font=font(24))
        y += 140
    d.line((800, 420, 960, 420), fill=MINT, width=8)
    d.polygon([(960, 400), (1000, 420), (960, 440)], fill=MINT)
    d.rounded_rectangle((1040, 200, 1830, 900), 20, fill=PANEL)
    d.text((1080, 230), "Household Wiki/", fill=MINT, font=font(38, True, mono=True))
    items = ["index.md", "log.md", "people/", "pets/", "home/", "appliances/", "vehicles/", "money/", "health/", "school/", "contacts/", "trips/"]
    for i, it in enumerate(items):
        d.text((1120, 300 + i * 48), ("├── " if i < len(items) - 1 else "└── ") + it, fill=FG if it.endswith(".md") else BLUE, font=font(30, mono=True))
    return im


def s4():
    im, d = canvas()
    title(d, "Ingest: \"Update the household wiki.\"", "The Skill finds new files and sends each one to a NAS expert")
    cols = [("Documents", "document-agent", "receipt · invoice · contract\nmedical-report schemas", R1 / "Documents/Home/dishwasher-receipt.pdf"),
            ("Photos", "photo-agent", "reads text in photos\nlabels, notices, whiteboards", R1 / "Photos/Home/furnace-label.jpg"),
            ("Voice memos", "knowledge-agent", "transcribes speech\nthen facts are extracted", None)]
    for k, (name, agent, what, _) in enumerate(cols):
        x = 90 + k * 600
        d.rounded_rectangle((x, 200, x + 560, 470), 20, fill=PANEL)
        d.text((x + 30, 225), name, fill=FG, font=font(40, True))
        d.text((x + 30, 285), agent, fill=MINT, font=font(32, True, mono=True))
        for i, ln in enumerate(what.split("\n")):
            d.text((x + 30, 345 + i * 42), ln, fill=MUTED, font=font(28))
    d.text((90, 520), "Example facts, each with its source", fill=FG, font=font(36, True))
    facts = [("Furnace filter: 16 x 25 x 1", "furnace-label.jpg"),
             ("Car insurance renews 2026-12-15, $1,284.00 per year", "car-insurance-renewal-2026.pdf, page 1"),
             ("Plumber Ray, Lakeview Plumbing: 555-0199", "plumber-visit-2026-11-02.m4a"),
             ("Mia: allergic to penicillin", "pediatric-visit-mia-2026-10.pdf, page 1")]
    for i, (f_, s) in enumerate(facts):
        y = 590 + i * 88
        d.rounded_rectangle((90, y, 1830, y + 72), 14, fill=(250, 250, 247))
        d.text((120, y + 18), f_, fill=(30, 35, 38), font=font(30, True))
        d.text((1100, y + 22), "Source: " + s, fill=(30, 110, 160), font=font(26))
    return im


def s5():
    im, d = canvas()
    title(d, "The change set", "Example of the expected change set for the first run. Nothing is written before you approve.")
    rows = [("money/car-insurance.md", "New", 6, 0), ("pets/pepper.md", "New", 6, 0), ("school/maple-grove-elementary.md", "New", 7, 0),
            ("money/internet.md", "New", 5, 0), ("people/mia.md", "New", 3, 0), ("health/mia.md", "New", 5, 0),
            ("appliances/dishwasher.md", "New", 6, 0), ("home/furnace.md", "New", 5, 0), ("home/water-heater.md", "New", 5, 0),
            ("contacts/lakeview-plumbing.md", "New", 3, 0)]
    x0, y0 = 90, 200
    head = ("Page", "New or changed", "Facts added", "Conflicts")
    cx = (x0, x0 + 820, x0 + 1150, x0 + 1450)
    d.rounded_rectangle((x0 - 10, y0 - 10, 1840, y0 + 52), 10, fill=PANEL)
    for c, h in zip(cx, head):
        d.text((c + 10, y0), h, fill=MINT, font=font(28, True))
    for i, (p, s, n, c) in enumerate(rows):
        y = y0 + 64 + i * 50
        d.text((cx[0] + 10, y), p, fill=FG, font=font(28, mono=True))
        d.text((cx[1] + 10, y), s, fill=FG, font=font(28))
        d.text((cx[2] + 10, y), str(n), fill=FG, font=font(28))
        d.text((cx[3] + 10, y), str(c), fill=FG, font=font(28))
    y = y0 + 64 + len(rows) * 50 + 20
    d.text((x0, y), "No household facts:  beach-day-2026-07.jpg", fill=MUTED, font=font(26))
    d.text((x0, y + 40), "For the next run:  vehicles/tessera-wagon.md, contacts/cedar-pediatrics.md, contacts/oakview-vet.md", fill=MUTED, font=font(26))
    pill(d, x0, y + 100, "Apply all, apply some, or cancel?", AMBER, 30)
    return im


def s6(tmp):
    im, d = canvas()
    title(d, "A wiki page", "Expected page appliances/dishwasher.md, made from the receipt")
    lines = ["# Dishwasher", "", "Type: appliance", "Summary: Aster DW-450 dishwasher, bought 2024-03-02.", "",
             "## Facts", "- Model: DW450SS. Source: dishwasher-receipt.pdf, p1",
             "- Serial number ends in 4417. Source: dishwasher-receipt.pdf, p1",
             "- Price: $849.00. Source: dishwasher-receipt.pdf, p1", "", "## Dates",
             "- 2026-03-02: Warranty ends. Source: dishwasher-receipt.pdf, p2", "", "## Related",
             "- [Kitchen](../home/kitchen.md)", "- [Brightwater Appliances](../contacts/brightwater.md)"]
    md_panel(d, 90, 190, 1150, lines, 25)
    pg = fit(pdf_page(R1 / "Documents/Home/dishwasher-receipt.pdf", tmp, page=2, res=90), 560, 760)
    im.paste(pg, (1290, 190))
    s = pg.height / 792.0  # pixels per PDF point; line 2 of the Warranty text sits at 139-148 pt
    d.rectangle((1290 + int(46 * s), 190 + int(134.5 * s), 1290 + int(240 * s), 190 + int(151.5 * s)), outline=AMBER, width=3)
    d.text((1290, 965), "Source: dishwasher-receipt.pdf, page 2", fill=MUTED, font=font(24))
    return im


def s7():
    im, d = canvas()
    title(d, "Ask", "Illustration of the conversation, with the expected answers")
    y = 190
    y = bubble(d, 760, y, 1080, "When does the car insurance renew, and what does it cost?", "YOU", (40, 70, 110))
    y = bubble(d, 90, y, 1300, "It renews on 2026-12-15. The premium is $1,284.00 per year.\nPage: money/car-insurance.md\nSource: Documents/Home/car-insurance-renewal-2026.pdf, page 1", "HOUSEHOLD WIKI", PANEL)
    y = bubble(d, 760, y, 1080, "What is the Wi-Fi password?", "YOU", (40, 70, 110))
    bubble(d, 90, y, 1300, "The wiki does not store passwords. A photo of the fridge whiteboard has one, and the Skill did not copy it.", "HOUSEHOLD WIKI", PANEL)
    return im


def s8(tmp):
    im, d = canvas()
    title(d, "Conflicts and sensitive data", "Expected result of the second run with 2 new files")
    pg = fit(pdf_page(R2 / "Documents/Home/car-insurance-change-notice.pdf", tmp, res=80), 520, 620)
    im.paste(pg, (90, 190))
    d.text((90, 830), "New: car-insurance-change-notice.pdf", fill=MUTED, font=font(24))
    lines = ["# Car insurance", "", "## Dates",
             "- 2026-12-15: Renewal. Source: car-insurance-renewal-2026.pdf, p1", "",
             "## Open questions",
             "- Two renewal dates found:", "  2026-12-15 (car-insurance-renewal-2026.pdf)", "  2027-01-15 (car-insurance-change-notice.pdf)",
             "  The user has not confirmed which one is correct."]
    yy = md_panel(d, 660, 190, 1180, lines, 25)
    d.rounded_rectangle((660, yy + 30, 1840, yy + 200), 18, fill=PANEL)
    d.text((690, yy + 50), "money/card.md", fill=MINT, font=font(26, True, mono=True))
    d.text((690, yy + 95), "Card number ends in 1111.", fill=FG, font=font(30))
    d.text((690, yy + 140), "The full card number and the PIN were not copied.", fill=AMBER, font=font(28, True))
    return im


def s9():
    im, d = canvas()
    title(d, "Tidy: \"What needs attention?\"", "Expected household check for a test day of 2026-11-25")
    d.rounded_rectangle((90, 190, 1100, 960), 20, fill=PANEL)
    d.text((130, 215), "Coming up", fill=MINT, font=font(38, True))
    up = [("2026-11-30", "Field trip form due (Mia)"), ("2026-12-03", "Picture day (Mia)"), ("2026-12-08", "Card payment due, $412.37"),
          ("2026-12-15", "Car insurance renewal (open question)"), ("2026-12-17", "Winter concert, 6:00 pm"), ("2026-12-20", "Pepper: rabies vaccine due"),
          ("2026-12-21", "Winter break starts")]
    for i, (dt, t) in enumerate(up):
        d.text((130, 290 + i * 88), dt, fill=FG, font=font(30, True, mono=True))
        d.text((380, 290 + i * 88), t, fill=FG, font=font(30))
    d.rounded_rectangle((1150, 190, 1840, 560), 20, fill=(70, 34, 34))
    d.text((1190, 215), "Past due", fill=(255, 170, 160), font=font(38, True))
    for i, (dt, t) in enumerate((("2026-11-18", "Internet bill, $65.00"), ("2026-03-02", "Dishwasher warranty ended"))):
        d.text((1190, 300 + i * 110), dt, fill=FG, font=font(30, True, mono=True))
        d.text((1190, 345 + i * 110), t, fill=FG, font=font(30))
    d.rounded_rectangle((1150, 600, 1840, 960), 20, fill=PANEL)
    d.text((1190, 625), "Conflicts", fill=AMBER, font=font(34, True))
    d.text((1190, 680), "Car insurance renewal date", fill=FG, font=font(28))
    d.text((1190, 760), "Old pages", fill=MINT, font=font(34, True))
    d.text((1190, 815), "None", fill=FG, font=font(28))
    d.text((1190, 880), "No change without your approval.", fill=MUTED, font=font(24))
    return im


def s10():
    im, d = canvas()
    d.text((90, 250), "Household Wiki", fill=FG, font=font(100, True))
    for i, t in enumerate(["Private: your files and the wiki stay on your NAS.", "Current: each run adds only the new files.",
                           "Checkable: every fact has a source file.", "Safe: no write without your approval, and no passwords."]):
        d.text((94, 410 + i * 66), t, fill=FG, font=font(38))
    d.text((94, 720), "github.com/vdimarco/ugreen-household-wiki.", fill=BLUE, font=font(34, True))
    d.text((94, 790), "Final demo: recorded on a UGREEN AI NAS in Round 2.", fill=MUTED, font=font(30))
    return im


# ---------- Assembly ----------

def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    narr, out = Path(sys.argv[1]), Path(sys.argv[2])
    with tempfile.TemporaryDirectory() as tmp:
        scenes = [s1(), s2(tmp), s3(), s4(), s5(), s6(tmp), s7(), s8(tmp), s9(), s10()]
        strip = Path(tmp) / "banner.png"
        banner_strip().save(strip)
        parts = []
        for i, im in enumerate(scenes, start=1):
            png = Path(tmp) / f"scene{i}.png"
            im.save(png)
            audio = next(narr.glob(f"scene{i}.*"))
            dur = duration(audio) + 1.6
            frames = int(dur * 30)
            vf = (f"scale=2880:-1,zoompan=z='min(zoom+0.00025,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                  f":d={frames}:s={W}x{H}:fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st={dur - 0.4:.2f}:d=0.4")
            part = Path(tmp) / f"part{i}.mp4"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(png), "-i", str(audio),
                            "-loop", "1", "-i", str(strip),
                            "-filter_complex", f"[0:v]{vf}[z];[z][2:v]overlay=0:{H - 46}:shortest=1,format=yuv420p[v];"
                                               f"[1:a]adelay=600|600,apad,aresample=48000[a]",
                            "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}", "-r", "30",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "160k", str(part)],
                           check=True)
            parts.append(part)
        lst = Path(tmp) / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                        "-movflags", "+faststart", str(out)], check=True)
        sheet = Image.new("RGB", (960 * 3, 540 * 4), BG)
        for i, im in enumerate(scenes):
            frame = im.copy()
            frame.paste(Image.open(strip), (0, H - 46))
            sheet.paste(frame.resize((960, 540)), ((i % 3) * 960, (i // 3) * 540))
        sheet.save(out.with_name(out.stem + "-storyboard.jpg"), quality=80)
    print(f"{out}  {duration(out):.1f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
