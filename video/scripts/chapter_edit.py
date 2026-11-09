"""Chapter 2 edit synced to Ariel's sentences: Layla full screen, Ariel full screen, and split screen with fact cards.
Usage (from video/): python3 scripts/chapter_edit.py   ->  out/edits/ch2_edit.mp4 (picture only, 1920x1080, length of the take)
Sentence timings: edits/ch2_sentences.json (Gemini transcript of the edited take); cuts snap to the quietest point between sentences.
Partner and competitor names are set as type, not logos (handoff rule: no real company logos)."""
import json, math, os, subprocess, sys, array
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

TAKE, CROPX = "out/speakers/M4_S2_Ariel_take2_graded.mp4", 552   # take 2 (8 Nov, script v3): IMG_2880 trimmed 10.6-92.0 s, 8% faster, pitch kept
OUT = "out/edits"; TMP = os.path.join(OUT, "ch2_parts"); os.makedirs(TMP, exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", "-an"]
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

# ---------- cut points: quietest 20 ms between the chosen sentences ----------
S = json.load(open("edits/ch2_take2_sentences.json")); T = length(TAKE)
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
    d.text((160, 560), "their own brand at your door", font=R.font(R.SANS, 40), fill=MUTED)
    arrow(d, 160, 680); d.text((240, 655), "the client moves to the app", font=R.font(R.SANS_M, 38), fill=R.INK)
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

CRITERIA = ["Runs home visits in Dubai today", "Works through salons, not around them", "Makes the salon stronger"]
def c_crit(k):
    """The three partner-selection criteria: k = 0 all listed, 1-3 the one he is asking, 4 all three ticked."""
    def draw():
        img, d = card(); label(d, 250, "OUR PARTNER CRITERIA")
        for i, t in enumerate(CRITERIA):
            y = 330 + i * 130; on = k == i + 1 or k == 4
            col = INK if on else (140, 134, 126)
            if k == 4: tick(d, 162, y + 16, M4C, 38)                   # ticked: the tick takes the number's place
            else: d.text((160, y), f"{i + 1}", font=R.font(R.SERIF, 64), fill=GOLD if on else col)
            d.text((230, y + 10), t, font=R.font(R.SANS_M if i == 2 else R.SANS, 41), fill=col)
        if k == 4:
            d.rectangle([160, 740, 220, 742], fill=GOLD); wordmark(d, (160, 775), 44, M4C)
            d.text((160, 845), "passes all three", font=R.font(R.SANS, 40), fill=MUTED)
        return img
    draw.__name__ = f"c_crit{k}"; return draw

def line_overlay(text):   # Layla's on-screen line, same style as the animatic
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = R.font(R.SERIF, 40); w = d.textlength(text, font=f)
    d.rectangle([140, 830, 140 + w + 40, 905], fill=R.IVORY + (235,)); d.text((160, 843), text, font=f, fill=INK)
    return img

# ---------- full-screen moment: "behind that message sits ServiceMarket ... since 2013" ----------
import portrait_edit as PE
PE.SHADE = PE.shade_png()
def full_behind(dur, t_line):
    return PE.full_seq("full_behind", [(PE.L.format("2c"), 0.0, dur)], dur,
                       [(0.2, dur, PE.type_png("ty_behind.png", "BEHIND THE MESSAGE", "ServiceMarket", None)),
                        (t_line, dur, PE.type_png("ty_behind_l.png", "", "", "home services in Dubai since 2013"))])

# ---------- segments ----------
c = {k: cut_after(k) for k in (0, 2, 3, 4, 6, 8, 9, 12, 14, 16, 17, 18, 19, 21)}
BEHIND = full_behind(round(c[4] - c[2] + 1.0, 2), round(c[3] - c[2], 2))
PLAN = [  # (start, end, kind, source); sentence numbers in edits/ch2_take2_sentences.json
    (0, c[0], "layla", ("out/layla/layla_2.mp4", "Wednesday, 18:00. Dana, from my salon.")),
    (c[0], c[2], "split", "out/p3_booking_confirmation.mp4"),          # "she thinks she's talking to her salon, and she is"
    (c[2], c[4], "layla", (BEHIND, None)),                              # full screen with type, same style as chapter 4
    (c[4], c[6], "split", c_200),
    (c[6], c[8], "split", c_roles),                                     # booking, payment; adds insurance and permits
    (c[8], c[9], "ariel", None),                                        # "That's the capability we're missing."
    (c[9], c[12], "split", c_bigapps), (c[12], c[14], "split", c_other_way),
    (c[14], c[16], "layla", ("out/layla/layla_3g_slow.mp4", None)),     # "if Layla ever feels ..." (3g at 93 % speed: fills the 9.6 s)
    (c[16], c[17], "split", c_crit(0)), (c[17], c[18], "split", c_crit(1)), (c[18], c[19], "split", c_crit(2)),
    (c[19], c[21], "ariel", None),                                      # [LENS] "and the one that decides it: ..."
    (c[21], T, "split", c_crit(4)),                                     # "ServiceMarket passes all three. That's why them."
]
XF = 0.6                      # transition length (s)
FPS = 30
def fr(t): return round(t * FPS) / FPS          # snap times to whole frames
PLAN = [(fr(a), fr(b), k, src) for a, b, k, src in PLAN]
json.dump([[a, b, k] for a, b, k, _ in PLAN if k in ("layla", "ariel")], open("edits/fulls_ch2.json", "w"))   # for captions
SHIFT = 960 - CROPX                             # in the split, take pixel x appears at x + SHIFT

def vis(n, t0, dur, out):
    """Render segment n's look for take time [t0, t0+dur] (picture only)."""
    a, b, kind, src = PLAN[n]; rel = t0 - a
    if kind == "ariel":
        ff("-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", TAKE, "-vf", "fps=30,scale=1920:1080", *ENC, out); return
    if kind == "layla":
        clip, text = src
        ins = ["-stream_loop", "-1", "-ss", f"{rel:.3f}", "-i", clip]; vf = "[0:v]fps=30,scale=1920:1080,setpts=PTS-STARTPTS[v0]"; last = "v0"
        if text:
            p = os.path.join(TMP, f"line{n}.png"); line_overlay(text).save(p); ins += ["-loop", "1", "-i", p]
            vf += f";[v0][1:v]overlay=0:0:enable='between(t,{0.3 - rel:.2f},{(b - a) - 0.2 - rel:.2f})'[v1]"; last = "v1"
        ff(*ins, "-filter_complex", vf, "-map", f"[{last}]", "-t", f"{dur:.3f}", *ENC, out); return
    right = ["-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", TAKE]
    if callable(src):
        p = os.path.join(TMP, f"card{n}.png")
        if not os.path.exists(p): src().save(p)
        left = ["-loop", "1", "-t", f"{dur:.3f}", "-i", p]; lf = "[0:v]fps=30[l]"
    else:
        left = ["-stream_loop", "-1", "-ss", f"{rel:.3f}", "-i", src]; lf = "[0:v]fps=30,scale=960:1080,setpts=PTS-STARTPTS[l]"
    fc = f"{lf};[1:v]fps=30,crop=960:1080:{CROPX}:0[r];[l][r]hstack=inputs=2[v]"; ins, last = left + right, "v"
    if n == 1:   # first time we see Ariel: lower third
        ins += ["-loop", "1", "-i", "out/lower_thirds/LT_S2_Ariel.png"]
        fc += f";[v][2:v]overlay=0:0:enable='between(t,{0.3 - rel:.2f},{4.2 - rel:.2f})'[v2]"; last = "v2"
    ff(*ins, "-filter_complex", fc, "-map", f"[{last}]", "-t", f"{dur:.3f}", *ENC, out)

def card_png(n):
    p = os.path.join(TMP, f"card{n}.png")
    if not os.path.exists(p): PLAN[n][3]().save(p)
    return p

def push(split_n, to_full, c, out):
    """Fluid move between a split (card + Ariel's half) and Ariel full screen: the card slides out (or in) on the left
    while the take glides between its split position (x+SHIFT) and full frame (x)."""
    P = f"(st(0,clip(t/{XF},0,1));ld(0)*ld(0)*(3-2*ld(0)))"          # smoothstep 0..1
    prog = P if to_full else f"(1-{P})"
    fc = (f"color=c=0xF7F3EC:s=1920x1080:r=30:d={XF}[bg];"
          f"[0:v]fps=30,setpts=PTS-STARTPTS[take];[1:v]fps=30,format=rgba[card];"
          f"[bg][take]overlay=x='{SHIFT}*(1-{prog})':y=0:eval=frame[m];"
          f"[m][card]overlay=x='-960*{prog}':y=0:eval=frame,format=yuv420p[v]")
    ff("-ss", f"{c:.3f}", "-t", f"{XF:.3f}", "-i", TAKE, "-loop", "1", "-t", f"{XF:.3f}", "-i", card_png(split_n),
       "-filter_complex", fc, "-map", "[v]", "-t", f"{XF:.3f}", *ENC, out)

def dissolve(n_from, n_to, c, out):
    A, B = out + ".a.mp4", out + ".b.mp4"; vis(n_from, c, XF, A); vis(n_to, c, XF, B)
    ff("-i", A, "-i", B, "-filter_complex", f"[0:v][1:v]xfade=transition=fade:duration={XF - 1 / FPS:.3f}:offset=0[v]", "-map", "[v]", "-t", f"{XF:.3f}", *ENC, out)

parts = []
for n, (a, b, kind, src) in enumerate(PLAN):
    if n > 0:                                   # transition at the cut, then the rest of the segment
        prev = PLAN[n - 1][2]; tr = os.path.join(TMP, f"t{n:02d}.mp4")
        if prev == "split" and kind == "ariel" and callable(PLAN[n - 1][3]): push(n - 1, True, a, tr); how = "move"
        elif prev == "ariel" and kind == "split" and callable(src): push(n, False, a, tr); how = "move"
        else: dissolve(n - 1, n, a, tr); how = "dissolve"
        parts.append(tr); t0 = a + XF
    else:
        t0, how = a, "start"
    core = os.path.join(TMP, f"s{n:02d}.mp4"); vis(n, t0, round(b - t0, 3), core); parts.append(core)
    what = src.__name__ if callable(src) else (src if isinstance(src, str) else (src[0] if src else "take"))
    print(f"{n:2d} {a:6.2f}-{b:6.2f} {kind:6s} {what:32s} in: {how}")
lst = os.path.join(TMP, "list.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
final = os.path.join(OUT, "ch2_edit.mp4"); ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", final)
print("wrote", final, round(length(final), 2), "s (take", round(T, 2), "s)")
