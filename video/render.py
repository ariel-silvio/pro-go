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
    fade_text(img, (160, 650), title, font(SANS, 56), MUTED, IVORY, a3, dy=10)
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
    a4 = ease((t - 4.4) / 0.6)
    d.text((160, 900), "Illustrative. The pilot will test whether this improvement is real.",
           font=font(SANS, 32), fill=mix(IVORY, MUTED, a4))
    out = clamp((t - 5.6) / 0.4)
    if out > 0: img = Image.blend(img, Image.new("RGB", (W, H), IVORY), out)
    return img

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
    if "--stills" in sys.argv:
        slate(2.5).save(os.path.join(out, "s1.png")); chapter(2.0).save(os.path.join(out, "s2.png"))
        score(5.0).save(os.path.join(out, "s3.png"))
    else:
        for n, fn, dur in SCENES: render(out, n, fn, dur); print("done", n)
