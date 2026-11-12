#!/usr/bin/env python3
"""Fit the hand-timed scenes to the narration in ../narration-natural.

The scenes in compositions/ keep their original cue times, which were set
against the first narration (../narration). This script maps those times to
the new narration with one piecewise-linear time warp per scene, then writes
the scene and audio timing into index.html. Run it once after changing the
narration files:

    python3 demo/video/motion/retime.py
"""
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEAD = 0.4
OLD_SLOTS = [9.6, 12.6, 10.7, 13.7, 9.1, 8.7, 11.6, 9.7, 7.0, 10.5]
# Per scene: (time in the old clip, time in the new clip) at the start of each
# phrase; the last pair is the end of speech. Read from the pauses in the clips.
ANCHORS = [
    [(0.36, 0), (1.87, 1.44), (4.00, 3.23), (5.75, 5.13), (8.43, 7.55)],
    [(0.28, 0), (3.80, 3.21), (8.25, 7.40), (10.58, 9.19), (11.74, 10.28)],
    [(0.51, 0), (2.94, 2.54), (6.41, 5.75), (7.12, 6.29), (9.82, 8.47)],
    [(0.48, 0), (2.95, 2.13), (5.48, 4.18), (12.56, 9.51)],
    [(0.26, 0), (3.17, 2.81), (7.87, 7.24)],
    [(0.49, 0), (3.11, 2.32), (7.40, 5.48)],
    [(0.44, 0), (2.70, 1.47), (4.14, 2.54), (8.00, 4.88), (10.68, 7.08)],
    [(0.47, 0), (2.93, 2.15), (6.63, 4.94), (8.76, 6.69)],
    [(0.28, 0), (1.91, 1.63), (5.64, 4.91)],
    [(0.39, 0), (1.79, 1.43), (3.79, 2.80), (5.12, 3.78), (6.53, 4.69), (8.05, 6.19)],
]


def dur(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


def main():
    slots, warps, clips = [], [], []
    for i, a in enumerate(ANCHORS):
        tail = OLD_SLOTS[i] - LEAD - a[-1][0]
        new_slot = round(LEAD + a[-1][1] + tail, 1)
        w = [(0, 0)] + [(round(LEAD + o, 2), round(LEAD + n, 2)) for o, n in a] + [(OLD_SLOTS[i], new_slot)]
        assert all(x[0] < y[0] and x[1] < y[1] for x, y in zip(w, w[1:])), (i + 1, w)
        slots.append(new_slot)
        warps.append(w)
        src = HERE.parent / "narration-natural" / ("scene%d.m4a" % (i + 1))
        shutil.copy(src, HERE / "assets/audio")
        clips.append(round(dur(src), 2))
    starts = [round(sum(slots[:i]), 1) for i in range(10)]
    total = round(sum(slots), 1)

    for i, w in enumerate(warps):
        sid = "s%d" % (i + 1)
        f = HERE / "compositions" / (sid + ".html")
        t = f.read_text()
        t = re.sub(r"\n      // retime:begin.*?// retime:end\n", "\n", t, flags=re.S)
        reg = '      window.__timelines["%s"] = tl;\n' % sid
        assert t.count(reg) == 1, sid
        block = (
            "      // retime:begin (written by retime.py: old cue time -> new narration time)\n"
            "      const W = %s;\n"
            "      const warped = gsap.timeline({ paused: true });\n"
            "      for (let k = 0; k + 1 < W.length; k++) {\n"
            "        warped.fromTo(tl, { time: W[k][0] }, { time: W[k + 1][0], duration: W[k + 1][1] - W[k][1], ease: \"none\", immediateRender: false }, W[k][1]);\n"
            "      }\n"
            "      // retime:end\n"
            '      window.__timelines["%s"] = warped;\n'
        ) % ([list(x) for x in w], sid)
        f.write_text(t.replace(reg, block))

    ix = HERE / "index.html"
    t = ix.read_text()
    for i in range(10):
        n = i + 1
        t, k = re.subn(r'(<div id="s%d" [^>]*?data-start=")[^"]*(" data-duration=")[^"]*"' % n,
                       lambda m: '%s%s%s%s"' % (m.group(1), starts[i], m.group(2), slots[i]), t)
        assert k == 1
        t, k = re.subn(r'(<audio id="vo%d" [^>]*?data-start=")[^"]*(" data-duration=")[^"]*"' % n,
                       lambda m: '%s%s%s%s"' % (m.group(1), round(starts[i] + LEAD, 2), m.group(2), clips[i]), t)
        assert k == 1
    t, k = re.subn(r'(<div id="root" [^>]*?data-duration=")[^"]*"', lambda m: '%s%s"' % (m.group(1), total), t)
    assert k == 1
    t, k = re.subn(r'(<div id="label" [^>]*?data-duration=")[^"]*"', lambda m: '%s%s"' % (m.group(1), total), t)
    assert k == 1
    ix.write_text(t)
    print("slots", slots, "total", total)


if __name__ == "__main__":
    main()
