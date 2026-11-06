"""Chapter 2 edit synced to Ariel's sentences: Layla full screen, Ariel full screen, and split screen with fact cards.
Usage (from video/): python3 scripts/chapter_edit.py   ->  out/edits/ch2_edit.mp4 (picture only, 1920x1080, length of the take)
Sentence timings: edits/ch2_sentences.json (Gemini transcript of the edited take); cuts snap to the quietest point between sentences.
Partner and competitor names are set as type, not logos (handoff rule: no real company logos)."""
import json, math, os, subprocess, sys, array
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

TAKE, CROPX = "out/speakers/M4_S2_Ariel_take1_edit.mp4", 650
OUT = "out/edits"; TMP = os.path.join(OUT, "ch2_parts"); os.makedirs(TMP, exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

# ---------- cut points: quietest 20 ms between the chosen sentences ----------
S = json.load(open("edits/ch2_sentences.json")); T = length(TAKE)
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", TAKE, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True).stdout
pcm = array.array("h", raw); hop = 320
env = [math.sqrt(sum(x * x for x in pcm[i:i + hop]) / hop) for i in range(0, len(pcm) - hop, hop)]
def quiet(a, b):
    i0, i1 = int(max(a, 0) / 0.02), int(min(b, T) / 0.02)
    return min(range(i0, max(i1, i0 + 1)), key=lambda k: env[min(k, len(env) - 1)]) * 0.02
def cut_after(k): return round(quiet(S[k]["end"] - 0.15, S[k + 1]["start"] + 0.15), 2)

# ---------- cards (left half, 960x1080, ivory) ----------
INK, MUTED, GOLDT, GOLD, M4C, HAIR = R.INK, R.MUTED, R.GOLD_TXT, R.GOLD, R.M4, R.HAIR
def card(): img = Image.new("RGB", (960, 1080), R.IVORY); return img, ImageDraw.Draw(img)
def label(d, y, t, col=GOLDT): R.spaced(d, (160, y), t, R.font(R.SANS_M, 24), col, 6)
def tick(d, x, y, col=M4C, s=26):
    d.line([(x, y + s * .55), (x + s * .38, y + s * .9), (x + s, y + s * .1)], fill=col, width=5, joint="curve")
def plus(d, x, y, col=GOLD, s=24):
    d.line([(x + s / 2, y), (x + s / 2, y + s)], fill=col, width=4); d.line([(x, y + s / 2), (x + s, y + s / 2)], fill=col, width=4)
def arrow(d, x, y, w=60, col=GOLD):
    d.line([(x, y), (x + w - 12, y)], fill=col, width=3); d.polygon([(x + w, y), (x + w - 16, y - 8), (x + w - 16, y + 8)], fill=col)
def wordmark(d, xy, size=64, col=INK):   # partner name as type, never a logo
    R.spaced(d, xy, "SERVICEMARKET", R.font(R.SANS_M, size), col, int(size * .12))

def c_behind():
    img, d = card(); label(d, 330, "BEHIND THE SALON'S MESSAGE")
    d.rectangle([160, 400, 220, 402], fill=GOLD); wordmark(d, (160, 450), 58)
    d.text((160, 560), "Booking, routing and payment,\nrun quietly in the background.", font=R.font(R.SANS, 34), fill=MUTED, spacing=12)
    return img
def c_2013():
    img, d = card(); label(d, 300, "SERVICEMARKET · DUBAI")
    d.text((150, 340), "2013", font=R.font(R.SERIF, 240), fill=INK)
    d.rectangle([160, 640, 220, 642], fill=GOLD)
    d.text((160, 670), "Running home services\nin Dubai since then.", font=R.font(R.SANS, 38), fill=MUTED, spacing=12)
    return img
def c_200():
    img, d = card(); label(d, 300, "SERVICEMARKET · PARTNERS")
    d.text((150, 340), "200+", font=R.font(R.SERIF, 240), fill=INK)
    d.rectangle([160, 640, 220, 642], fill=GOLD)
    d.text((160, 670), "vetted partner companies", font=R.font(R.SANS, 40), fill=INK)
    tick(d, 160, 748); d.text((205, 740), "salon at home included", font=R.font(R.SANS, 36), fill=MUTED)
    return img
def c_roles():
    img, d = card(); f = R.font(R.SANS, 40)
    label(d, 250, "ALREADY RUNS")
    for k, t in enumerate(["Booking", "Payment"]): tick(d, 160, 318 + k * 70); d.text((210, 308 + k * 70), t, font=f, fill=INK)
    d.line([(160, 480), (800, 480)], fill=HAIR, width=2)
    label(d, 530, "ADDS IN OUR PILOT")
    for k, t in enumerate(["Insurance", "Each salon's permit paperwork"]): plus(d, 161, 603 + k * 70); d.text((210, 590 + k * 70), t, font=f, fill=INK)
    return img
def c_bigapps():
    img, d = card(); label(d, 280, "THE TWO BIG BEAUTY APPS", MUTED)
    d.text((160, 330), "Urban Company\nJustlife", font=R.font(R.SERIF, 76), fill=MUTED, spacing=16)
    d.text((160, 560), "send their own staff to your door", font=R.font(R.SANS, 34), fill=MUTED)
    arrow(d, 160, 680); d.text((240, 655), "would replace the salon", font=R.font(R.SANS_M, 38), fill=R.INK)
    d.line([(160, 820), (800, 820)], fill=HAIR, width=2)
    return img
def c_other_way():
    img, d = card(); label(d, 280, "THE OTHER WAY")
    wordmark(d, (160, 330), 58)
    d.text((160, 440), "already sells other\ncompanies' services", font=R.font(R.SANS, 40), fill=MUTED, spacing=12)
    arrow(d, 160, 640); d.text((240, 612), "the salon stays", font=R.font(R.SERIF, 54), fill=INK)
    d.text((240, 680), "in front", font=R.font(R.SERIF, 54), fill=INK)
    return img
def c_test():
    img, d = card(); label(d, 280, "THE PARTNER TEST")
    d.text((160, 330), "Does it make\nthe salon stronger?", font=R.font(R.SERIF, 66), fill=INK, spacing=14)
    d.rectangle([160, 540, 220, 542], fill=GOLD)
    tick(d, 160, 598, M4C, 34); wordmark(d, (215, 595), 44, M4C)
    d.text((160, 690), "That's why we chose it.", font=R.font(R.SANS, 36), fill=MUTED)
    return img

def line_overlay(text):   # Layla's on-screen line, same style as the animatic
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = R.font(R.SERIF, 40); w = d.textlength(text, font=f)
    d.rectangle([140, 830, 140 + w + 40, 905], fill=R.IVORY + (235,)); d.text((160, 843), text, font=f, fill=INK)
    return img

# ---------- segments ----------
c = {k: cut_after(k) for k in (0, 1, 2, 3, 5, 6, 8, 10, 13, 15, 17)}
PLAN = [  # (start, end, kind, source)
    (0, c[0], "layla", ("out/layla/layla_2.mp4", "Wednesday, 18:00. Dana, from my salon.")),
    (c[0], c[1], "split", "out/p3_booking_confirmation.mp4"),
    (c[1], c[2], "split", c_behind), (c[2], c[3], "split", c_2013), (c[3], c[5], "split", c_200),
    (c[5], c[6], "ariel", None),
    (c[6], c[8], "split", c_roles), (c[8], c[10], "split", c_bigapps), (c[10], c[13], "split", c_other_way),
    (c[13], c[15], "layla", ("out/layla/layla_3d.mp4", None)),
    (c[15], c[17], "ariel", None),
    (c[17], T, "split", c_test),
]
parts = []
for n, (a, b, kind, src) in enumerate(PLAN):
    d = round(b - a, 3); out = os.path.join(TMP, f"s{n:02d}.mp4"); parts.append(out)
    if kind == "ariel":
        ff("-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", TAKE, "-vf", "fps=30,scale=1920:1080", *ENC, out)
    elif kind == "layla":
        clip, text = src
        ins = ["-stream_loop", "-1", "-i", clip]; vf = "[0:v]fps=30,scale=1920:1080[v0]"; last = "v0"
        if text:
            p = os.path.join(TMP, f"line{n}.png"); line_overlay(text).save(p); ins += ["-loop", "1", "-i", p]
            vf += f";[v0][1:v]overlay=0:0:enable='between(t,0.3,{d - 0.2:.2f})'[v1]"; last = "v1"
        ff(*ins, "-filter_complex", vf, "-map", f"[{last}]", "-t", f"{d:.3f}", *ENC, out)
    else:
        right = ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", TAKE]
        if callable(src):
            p = os.path.join(TMP, f"card{n}.png"); src().save(p)
            left = ["-loop", "1", "-t", f"{d:.3f}", "-i", p]; lf = "[0:v]fps=30,fade=in:st=0:d=0.35:color=0xF7F3EC[l]"
        else:
            left = ["-stream_loop", "-1", "-i", src]; lf = "[0:v]fps=30,scale=960:1080[l]"
        fc = f"{lf};[1:v]fps=30,crop=960:1080:{CROPX}:0[r];[l][r]hstack=inputs=2[v]"
        ins, last = left + right, "v"
        if n == 1:   # first time we see Ariel: lower third
            ins += ["-loop", "1", "-i", "out/lower_thirds/LT_S2_Ariel.png"]
            fc += f";[v][2:v]overlay=0:0:enable='between(t,0.3,{min(d, 4.3) - 0.1:.2f})'[v2]"; last = "v2"
        ff(*ins, "-filter_complex", fc, "-map", f"[{last}]", "-t", f"{d:.3f}", *ENC, out)
    what = src.__name__ if callable(src) else (src if isinstance(src, str) else (src[0] if src else "take"))
    print(f"{n:2d} {a:6.2f}-{b:6.2f} {kind:6s} {what}")
lst = os.path.join(TMP, "list.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
final = os.path.join(OUT, "ch2_edit.mp4"); ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", final)
print("wrote", final, round(length(final), 2), "s (take", round(T, 2), "s)")
