"""Team D video graphics sample: opening slate, chapter card, score counter.
Usage: python3 render.py <outdir> [--stills]
"""
import os, sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
F = os.environ.get("FONT_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")) + "/"
SERIF = F + "bodoni-moda-latin-500-normal.ttf"
SANS = F + "jost-latin-400-normal.ttf"
SANS_M = F + "jost-latin-500-normal.ttf"

INK = (17, 17, 17); IVORY = (247, 243, 236); PAPER = (255, 255, 255)
GOLD = (176, 141, 87); GOLD_TXT = (138, 106, 59); MUTED = (95, 90, 84)
HAIR = (227, 221, 211); WHITE = (255, 255, 255); M4 = (27, 107, 99)

def font(p, s): return ImageFont.truetype(p, s)
def clamp(x): return max(0.0, min(1.0, x))
def ease(x):  # easeOutCubic
    x = clamp(x); return 1 - (1 - x) ** 3
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def spaced(draw, xy, text, fnt, fill, tracking, anchor_center=False):
    """Draw letter-spaced caps (the brand's label style)."""
    widths = [draw.textlength(c, font=fnt) for c in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor_center: x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += w + tracking
    return total

def fade_text(img, xy, text, fnt, color, bg, a, anchor="la", dy=0):
    if a <= 0: return                 # not yet visible: drawing it in the background colour would erase anything underneath
    d = ImageDraw.Draw(img)
    d.text((xy[0], xy[1] + (1 - a) * dy), text, font=fnt, fill=mix(bg, color, a), anchor=anchor)

# ---------- scene 1: opening slate (4 s) ----------
def slate(t):
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    a1 = ease((t - 0.2) / 0.6)
    spaced(d, (W / 2, 330), "L'ORÉAL GROUPE  ·  TEAM D", font(SANS_M, 26), mix(INK, GOLD, a1), 7, True)
    a2 = ease((t - 0.6) / 0.9)
    fade_text(img, (W / 2, 470), "12 weeks with Layla", font(SERIF, 112), WHITE, INK, a2, "mm", 24)
    rw = 220 * ease((t - 1.2) / 0.8)
    d.rectangle([W / 2 - rw / 2, 575, W / 2 + rw / 2, 577], fill=GOLD)
    a3 = ease((t - 1.6) / 0.8)
    fade_text(img, (W / 2, 640), "PRO•GO  ·  A proposal to the CEO", font(SANS, 38), IVORY, INK, a3, "mm", 12)
    out = clamp((t - 3.5) / 0.5)  # fade to black at the end
    if out > 0: img = Image.blend(img, Image.new("RGB", (W, H), INK), out)
    return img

# ---------- scene 2: chapter card (3 s) ----------
def chapter(t, week="Week 0", n="1", title="The problem"):
    img = Image.new("RGB", (W, H), IVORY); d = ImageDraw.Draw(img)
    a0 = ease(t / 0.5)
    d.rectangle([0, 0, W, 10], fill=mix(IVORY, M4, a0))
    a1 = ease((t - 0.1) / 0.5)
    spaced(d, (160, 300), f"CHAPTER {n}", font(SANS_M, 26), mix(IVORY, GOLD_TXT, a1), 7)
    a2 = ease((t - 0.3) / 0.7)
    fade_text(img, (160 - (1 - a2) * 40, 350), week, font(SERIF, 200), INK, IVORY, a2)
    rw = 160 * ease((t - 0.8) / 0.6)
    d.rectangle([160, 610, 160 + rw, 612], fill=GOLD)
    a3 = ease((t - 1.0) / 0.6)
    fade_text(img, (160, 650), title, font(SANS, 56), mix(MUTED, INK, 0.55), IVORY, a3, dy=10)
    out = clamp((t - 2.6) / 0.4)
    if out > 0: img = Image.blend(img, Image.new("RGB", (W, H), IVORY), out)
    return img

# ---------- scene 3: score counter (6 s) ----------
PTS = [(0, 58), (2, 59), (4, 61), (6, 62), (8, 64), (10, 66), (12, 74)]  # visit 1 wk 2, visit 2 wk 10 (66 = prototype re-scan)
def score(t):
    img = Image.new("RGB", (W, H), IVORY); d = ImageDraw.Draw(img)
    a1 = ease(t / 0.5)
    spaced(d, (160, 220), "LAYLA'S HAIR SCORE", font(SANS_M, 26), mix(IVORY, GOLD_TXT, a1), 7)
    p = ease((t - 0.6) / 3.6)                   # progress through the 12 weeks
    wk = 12 * p
    # interpolate score along the points
    s = PTS[0][1]
    for (x0, y0), (x1, y1) in zip(PTS, PTS[1:]):
        if x0 <= wk <= x1: s = y0 + (y1 - y0) * (wk - x0) / (x1 - x0)
    if wk >= 12: s = 74
    d.text((160, 270), f"{round(s)}", font=font(SERIF, 300), fill=mix(IVORY, INK, a1))
    d.text((160, 640), f"Week {int(round(wk))} of 12", font=font(SANS, 44), fill=mix(IVORY, MUTED, a1))
    # chart, right side
    cx0, cx1, cy0, cy1 = 900, 1720, 300, 700  # right end keeps "Wk 12" >= 160 px from the edge
    def X(w): return cx0 + (cx1 - cx0) * w / 12
    def Y(v): return cy1 - (cy1 - cy0) * (v - 50) / 30   # axis 50..80
    for v in (50, 60, 70, 80):
        d.line([cx0, Y(v), cx1, Y(v)], fill=mix(IVORY, HAIR, a1), width=2)
        d.text((cx0 - 20, Y(v)), str(v), font=font(SANS, 26), fill=mix(IVORY, MUTED, a1), anchor="rm")
    for w in (0, 4, 8, 12):
        d.text((X(w), cy1 + 26), f"Wk {w}", font=font(SANS, 26), fill=mix(IVORY, MUTED, a1), anchor="mt")
    line = [(X(x), Y(y)) for x, y in PTS if x <= wk]
    if wk < 12: line.append((X(wk), Y(s)))
    if len(line) > 1: d.line(line, fill=GOLD, width=7, joint="curve")
    r = 13
    ex, ey = X(wk), Y(s)
    d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=GOLD)
    a5 = ease((t - 4.0) / 0.6)                  # what the score stands for
    d.text((160, 730), "colour that lasts  ·  less breakage  ·  shine", font=font(SANS, 34), fill=mix(IVORY, GOLD_TXT, a5))
    a4 = ease((t - 4.4) / 0.6)
    d.text((160, 900), "Illustrative. The pilot will test whether this improvement is real.",
           font=font(SANS, 32), fill=mix(IVORY, MUTED, a4))
    out = clamp((t - 5.9) / 0.4)
    if out > 0: img = Image.blend(img, Image.new("RGB", (W, H), IVORY), out)
    return img


# ---------- service diagram (M3 "How it works", ServiceMarket behind booking and visit) ----------
STEPS = ["Her salon invites her and runs a free scan", "Same colourist booked on WhatsApp",
         "Home visit: scan, colour, treatment", "Re-scan: she sees the result", "Next visit booked before she leaves"]
def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width: cur = t
        else: lines.append(cur); cur = w
    return lines + [cur]
def diagram(t, partner="SERVICEMARKET"):
    img = Image.new("RGB", (W, H), IVORY); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=M4)
    spaced(d, (160, 200), "HOW PRO•GO WORKS", font(SANS_M, 26), GOLD_TXT, 7)
    d.text((160, 245), "One plan, two home visits, one result she can see", font=font(SERIF, 56), fill=INK)
    bw, gap, y0, y1 = 280, 50, 400, 660
    fnum, ftxt = font(SERIF, 54), font(SANS, 29)
    for i, txt in enumerate(STEPS):
        a = ease((t - 0.4 - i * 0.8) / 0.6)
        if a <= 0: continue
        x = 160 + i * (bw + gap); dy = (1 - a) * 16
        d.rectangle([x, y0 + dy, x + bw, y1 + dy], fill=mix(IVORY, PAPER, a), outline=mix(IVORY, HAIR, a), width=2)
        d.text((x + 26, y0 + 22 + dy), str(i + 1), font=fnum, fill=mix(IVORY, GOLD, a))
        for j, line in enumerate(wrap(d, txt, ftxt, bw - 52)):
            d.text((x + 26, y0 + 110 + j * 40 + dy), line, font=ftxt, fill=mix(IVORY, INK, a))
        if i < 4 and ease((t - 0.9 - i * 0.8) / 0.5) > 0:   # arrow to next box, drawn as a shape
            aa = ease((t - 0.9 - i * 0.8) / 0.5); ax = x + bw + 8; ay = (y0 + y1) // 2
            d.line([ax, ay, ax + (gap - 22) * aa, ay], fill=GOLD, width=3)
            if aa > .95: d.polygon([(ax + gap - 16, ay), (ax + gap - 28, ay - 8), (ax + gap - 28, ay + 8)], fill=GOLD)
    a = ease((t - 4.6) / 0.6)                               # partner line under steps 2 and 3
    if a > 0:
        x0 = 160 + (bw + gap); x1 = x0 + 2 * bw + gap
        d.rectangle([x0, y1 + 30, x0 + (x1 - x0) * a, y1 + 33], fill=M4)
        spaced(d, (x0, y1 + 48), f"RUN BY {partner}", font(SANS_M, 22), mix(IVORY, M4, a), 5)
    a = ease((t - 5.6) / 0.6)                               # who wins
    if a > 0:
        spaced(d, (160, 820), "SALON EARNS   ·   " + partner + " GROWS   ·   L'ORÉAL LEARNS", font(SANS_M, 26), mix(IVORY, GOLD_TXT, a), 6)
    a = ease((t - 6.4) / 0.6)
    if a > 0:
        d.text((160, 876), "Her colourist always comes from her own partner salon. Pilot: WhatsApp and salon records; the app comes in 2028.",
               font=font(SANS, 26), fill=mix(IVORY, MUTED, a))
    return img

# ---------- closing card (ink, one sentence in Bodoni) ----------
def closing(t, lines=("Our ask: 90 days in Dubai,", "with ServiceMarket and our partner salons.")):
    img = Image.new("RGB", (W, H), INK); d = ImageDraw.Draw(img)
    a = ease((t - 0.3) / 1.0)
    for i, ln in enumerate(lines):
        fade_text(img, (W / 2, 430 + i * 104), ln, font(SERIF, 76), WHITE, INK, a, "mm", 14)
    rw = 180 * ease((t - 1.2) / 0.8)
    d.rectangle([W / 2 - rw / 2, 640, W / 2 + rw / 2, 642], fill=GOLD)  # below line 2 descenders
    out = clamp((t - 4.4) / 0.6)
    if out > 0: img = Image.blend(img, Image.new("RGB", (W, H), INK), out)
    return img

CARDS = [("0", "Week 0", "The gap"), ("1", "Week 1", "Who, and why them"), ("2", "Week 2", "How we work together"),
         ("3", "Week 4", "Why everyone wins"), ("4", "Week 10", "The pilot"), ("5", "Week 12", "The rules, and our ask")]

SCENES = [("01_opening_slate", slate, 4.0), ("02_chapter_week0", chapter, 3.0), ("03_score_counter", score, 6.0)]

def render(outdir, name, fn, dur):
    tmp = os.path.join(outdir, name + ".part.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(int(dur * FPS)):
        p.stdin.write(fn(i / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(outdir, name + ".mp4"))
    else: raise SystemExit(f"ffmpeg failed on {name}")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    if "--m4" in sys.argv:   # chapter cards, diagram and closing card for the M4 video
        for n, wk, title in CARDS:
            fn = (lambda wk, n, title: lambda t: chapter(t, wk, str(int(n) + 1), title))(wk, n, title)
            render(out, f"chapter_{wk.lower().replace(' ', '')}", fn, 3.0); print("done", wk)
        render(out, "service_diagram", diagram, 10.0); print("done diagram")
        render(out, "closing_card", closing, 5.0); print("done closing")
        diagram(9.0).save(os.path.join(out, "service_diagram.png")); closing(3.0).save(os.path.join(out, "closing_card.png"))
        chapter(2.0, "Week 10", "5", "The pilot").save(os.path.join(out, "chapter_week10.png"))
        sys.exit()
    if "--stills" in sys.argv:
        slate(2.5).save(os.path.join(out, "s1.png")); chapter(2.0).save(os.path.join(out, "s2.png"))
        score(5.0).save(os.path.join(out, "s3.png"))
    else:
        for n, fn, dur in SCENES: render(out, n, fn, dur); print("done", n)

# ---------- text check (v17): every drawn line must fit inside its image and use only characters the font has ----------
import atexit
from fontTools.ttLib import TTFont as _TTF
_CMAPS, TEXT_ISSUES = {}, []
_orig_text = ImageDraw.ImageDraw.text
def _checked_text(self, xy, text, fill=None, font=None, anchor=None, *a, **k):
    if font is not None and isinstance(text, str) and hasattr(font, "path"):
        cm = _CMAPS.get(font.path) or _CMAPS.setdefault(font.path, set(_TTF(font.path).getBestCmap()))
        miss = sorted({c for c in text if c.strip() and ord(c) not in cm})
        if miss: TEXT_ISSUES.append(f"missing glyph {miss} in {os.path.basename(font.path)}: {text!r}")
        try:
            l, t, r, b = self.textbbox(xy, text, font=font, anchor=anchor)
            W, H = self.im.size
            if l < 0 or r > W or b > H: TEXT_ISSUES.append(f"overflow ({l:.0f}-{r:.0f} of {W}): {text!r}")
        except Exception: pass
    return _orig_text(self, xy, text, fill, font, anchor, *a, **k)
ImageDraw.ImageDraw.text = _checked_text
@atexit.register
def _report():
    if TEXT_ISSUES: print("TEXT CHECK:", len(set(TEXT_ISSUES)), "issue(s)\n  " + "\n  ".join(sorted(set(TEXT_ISSUES))))
