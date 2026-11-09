"""Chapter edits for takes recorded in portrait: chapter 4 (Rebecca) and chapter 6 (Ignacio).
Half-half split (960 | 960) like Ariel's chapter: left = Layla, cards, animated type; right = the speaker,
portrait take scaled and cropped to 960x1080. Full-screen footage moments with type dissolve over the split.
All times below are seconds in the RAW take (sentence and word timings checked against the audio envelope).
Usage (from video/): RAW1=... RAW4=... RAW6=... AUD6=... CH=1,4,6 python3 scripts/portrait_edit.py
  -> out/speakers/M4_S4_Rebecca_edit.mp4, out/speakers/M4_S6_Ignacio_edit.mp4 (voice + portrait picture)
  -> out/edits/ch4_edit.mp4, out/edits/ch6_edit.mp4 (1920x1080 picture only, length of the trimmed take)"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

LW = 960; XF = 0.5; FPS = 30
OUT = "out/edits"; TMP = os.path.join(OUT, "portrait_parts"); os.makedirs(TMP, exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "19", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
L = "out/layla/layla_{}.mp4"
INK, IVORY, WHITE, MUTED, GOLDT, GOLD, M4C = R.INK, R.IVORY, R.WHITE, R.MUTED, R.GOLD_TXT, R.GOLD, R.M4
def png(img, n): p = os.path.join(TMP, n); img.save(p); return p
def anim(name, dur, draw, size=(LW, 1080)):
    """Render an animated card: draw(t) -> PIL image."""
    out = os.path.join(TMP, name + ".mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}",
                          "-r", str(FPS), "-i", "-", *ENC, "-an", out], stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))): p.stdin.write(draw(i / FPS).convert("RGB").tobytes())
    p.stdin.close(); p.wait(); return out
def a_in(t, t0, d=0.5): return R.ease((t - t0) / d)

# ---------- static cards (960x1080, ivory) ----------
def card(bg=IVORY): img = Image.new("RGB", (LW, 1080), bg); return img, ImageDraw.Draw(img)
def label(d, xy, t, col=GOLDT, size=24): R.spaced(d, xy, t, R.font(R.SANS_M, size), col, 6)
def big_number(lab, num, line1, line2, src):
    img, d = card(); label(d, (160, 300), lab)
    d.text((150, 340), num, font=R.font(R.SERIF, 240), fill=INK)
    d.rectangle([160, 640, 220, 642], fill=GOLD)
    d.text((160, 670), line1, font=R.font(R.SANS, 40), fill=INK)
    d.text((160, 730), line2, font=R.font(R.SANS, 34), fill=MUTED)
    d.text((160, 960), src, font=R.font(R.SANS, 22), fill=MUTED); return img
def c_salon10(): return big_number("WHO WINS · THE SALON", "+10 %", "more income per partner salon", "by 2030", "")   # sources: on the Miro board
def c_300():     return big_number("PRO•GO · 2027 TARGET", "300", "active care clients in Dubai", "one Layla proves nothing", "")

RULES = [("GO", ["40 % come back", "within 90 days"], "€7m released"),
         ("CHANGE", ["They come back,", "the money doesn't"], "new price or deal"),
         ("FALL BACK", ["Salons say no"], "salon subscription"),
         ("STOP", ["2 missed reviews"], "in a row")]
def c_rule(k):
    """One rule at a time in large type; all four named in a small progress row at the top."""
    img, d = card(); x = 160
    for j, (head, _, _) in enumerate(RULES):          # progress row
        f = R.font(R.SANS_M, 24); col = M4C if j == k else (140, 134, 126)
        R.spaced(d, (x, 170), head, f, col, 5); w = d.textlength(head, font=f) + len(head) * 5
        if j == k: d.rectangle([x, 206, x + w - 5, 208], fill=M4C)
        x += w + 40
    if k is None:
        d.text((150, 330), "The rules", font=R.font(R.SERIF, 150), fill=INK)
        d.rectangle([160, 540, 220, 542], fill=GOLD)
        d.text((160, 575), "written before the test", font=R.font(R.SANS, 44), fill=MUTED)
    else:
        head, lines, then = RULES[k]
        d.text((150, 290), head.title() if head != "FALL BACK" else "Fall back", font=R.font(R.SERIF, 170), fill=INK)
        d.rectangle([160, 520, 220, 522], fill=GOLD)
        for i, ln in enumerate(lines): d.text((160, 555 + i * 64), ln, font=R.font(R.SANS, 50), fill=INK)
        d.text((160, 575 + len(lines) * 64), "→ " + then, font=R.font(R.SANS_M, 40), fill=M4C)
    return img

# ---------- animated cards for Rebecca's climax (ink background) ----------
def learns(dur, t_head, t_sub):
    def draw(t):
        img, d = card(INK); a = a_in(t, t_head, 0.7); b = a_in(t, t_sub, 0.6)
        R.spaced(d, (160, 330), "WHO WINS · L'ORÉAL", R.font(R.SANS_M, 24), R.mix(INK, GOLD, a), 6)
        R.fade_text(img, (160, 380), "L'Oréal", R.font(R.SERIF, 170), WHITE, INK, a, dy=30)
        R.fade_text(img, (160, 560), "learns.", R.font(R.SERIF, 170), WHITE, INK, a_in(t, t_head + 0.25, 0.7), dy=30)
        R.fade_text(img, (165, 790), "in real homes, over 12 weeks", R.font(R.SANS, 44), GOLD, INK, b, dy=12)
        return img
    return draw
def weeks(dur):
    def draw(t):
        img, d = card(INK); n = int(round(12 * R.ease(t / 0.75)))
        R.spaced(d, (160, 330), "OVER", R.font(R.SANS_M, 24), GOLD, 6)
        d.text((150, 360), f"{n}", font=R.font(R.SERIF, 300), fill=WHITE)
        R.fade_text(img, (165, 720), "weeks", R.font(R.SERIF, 90), WHITE, INK, a_in(t, 0.5, 0.4))
        return img
    return draw
def struck(word, dur, t_strike):
    def draw(t):
        img, d = card(INK); a = a_in(t, 0, 0.35)
        R.spaced(d, (160, 400), "NOT IN", R.font(R.SANS_M, 26), R.mix(INK, GOLD, a), 7)
        f = R.font(R.SERIF, 150); R.fade_text(img, (150, 450), word, f, WHITE, INK, a, dy=20)
        w = d.textlength(word, font=f); s = R.ease((t - t_strike) / 0.35)
        if s > 0: d.rectangle([150, 545, 150 + int(w * s), 553], fill=GOLD)
        return img
    return draw
def partners(dur, times, t_sub):
    def draw(t):
        img, d = card();
        for i, (w, t0) in enumerate(zip(["The salon", "ServiceMarket", "L'Oréal"], times)):
            R.fade_text(img, (160, 280 + i * 150), w, R.font(R.SERIF, 104), INK, IVORY, a_in(t, t0, 0.5), dy=16)
        a = a_in(t, t_sub, 0.6); d.rectangle([160, 770, 160 + int(60 * a), 772], fill=GOLD)
        R.fade_text(img, (160, 800), "three reasons to want it to work", R.font(R.SANS, 40), MUTED, IVORY, a, dy=8)
        return img
    return draw


def tick(d, x, y, col=M4C, s=26):
    d.line([(x, y + s * .55), (x + s * .38, y + s * .9), (x + s, y + s * .1)], fill=col, width=5, joint="curve")

# ---------- animated cards for Amjad's chapter (times in edit seconds, relative to the card's start) ----------
def facts(t_items):
    """Layla in three facts: 34 · Dubai · every 8 weeks."""
    items = [("34", "years old"), ("Dubai", "where she lives"), ("8 weeks", "between colours")]
    def draw(t):
        img, d = card()
        R.spaced(d, (160, 250), "LAYLA", R.font(R.SANS_M, 24), GOLDT, 6)
        for i, ((big, small), t0) in enumerate(zip(items, t_items)):
            a = a_in(t, t0, 0.5); y = 310 + i * 210
            R.fade_text(img, (152, y), big, R.font(R.SERIF, 110), INK, IVORY, a, dy=18)
            R.fade_text(img, (160, y + 140), small, R.font(R.SANS, 38), MUTED, IVORY, a, dy=8)
        return img
    return draw
def seesit(t1, t2):
    def draw(t):
        img, d = card(INK)
        R.fade_text(img, (160, 380), "If it didn't work,", R.font(R.SERIF, 84), WHITE, INK, a_in(t, 0.1, 0.5), dy=16)
        R.fade_text(img, (160, 480), "she sees it.", R.font(R.SERIF, 84), WHITE, INK, a_in(t, t1, 0.5), dy=16)
        R.fade_text(img, (160, 640), "So do we.", R.font(R.SERIF, 84), GOLD, INK, a_in(t, t2, 0.5), dy=16)
        return img
    return draw
def capability(t_rows, t_gap, t_subs):
    """What L'Oréal has (ticked) and the gap: the visit at home, with what it takes."""
    rows = ["The science", "The products", "Salons that trust us"]
    subs = ["licensed", "on time", "insured", "permitted"]
    def draw(t):
        img, d = card()
        R.spaced(d, (160, 200), "L'ORÉAL ALREADY HAS", R.font(R.SANS_M, 24), GOLDT, 6)
        for i, (r, t0) in enumerate(zip(rows, t_rows)):
            a = a_in(t, t0, 0.4); y = 255 + i * 88
            if a > 0: tick(d, 162, y + 10, R.mix(IVORY, M4C, a), 34)
            R.fade_text(img, (220, y), r, R.font(R.SANS, 48), INK, IVORY, a)
        g = a_in(t, t_gap, 0.6)
        if g > 0:
            d.rectangle([160, 540, 160 + int(640 * g), 542], fill=GOLD)
            R.fade_text(img, (160, 570), "THE GAP", R.font(R.SANS_M, 24), GOLDT, IVORY, g)
            R.fade_text(img, (152, 610), "The visit at home", R.font(R.SERIF, 80), INK, IVORY, g, dy=14)
            d.rectangle([132, 622, 138, 702], fill=R.mix(IVORY, M4C, g))
        x = 160
        for w, t0 in zip(subs, t_subs):
            a = a_in(t, t0, 0.35); f = R.font(R.SANS_M, 34)
            R.fade_text(img, (x, 750), w, f, M4C, IVORY, a, dy=8); x += d.textlength(w, font=f) + 36
        return img
    return draw
def build_buy_partner(t_words, t_strike1, t_strike2, t_partner):
    """Build, buy or partner: two struck through (with the reason), partner lit."""
    words = ["Build", "Buy", "Partner"]; why = ["takes years", "puts us between the salon and its client"]
    def draw(t):
        img, d = card(INK)
        R.spaced(d, (160, 230), "THREE WAYS TO GET IT", R.font(R.SANS_M, 24), GOLD, 6)
        for i, (w, t0) in enumerate(zip(words, t_words)):
            a = a_in(t, t0, 0.4); y = 270 + i * 240; f = R.font(R.SERIF, 120)
            lit = i == 2 and t >= t_partner
            col = R.mix(WHITE, GOLD, a_in(t, t_partner, 0.6)) if i == 2 else WHITE
            if i < 2 and t >= (t_strike1, t_strike2)[i]: col = R.mix(WHITE, (110, 106, 100), a_in(t, (t_strike1, t_strike2)[i], 0.4))
            R.fade_text(img, (152, y), w, f, col, INK, a, dy=18)
            if i < 2:
                ts = (t_strike1, t_strike2)[i]; sa = R.ease((t - ts) / 0.35); w_px = d.textlength(w, font=f)
                if sa > 0: d.rectangle([152, y + 82, 152 + int(w_px * sa), y + 88], fill=GOLD)
                R.fade_text(img, (165, y + 158), why[i], R.font(R.SANS, 32), (190, 184, 176), INK, a_in(t, ts + 0.2, 0.4))
            if lit: d.rectangle([152, y + 160, 152 + int(220 * a_in(t, t_partner, 0.6)), y + 164], fill=GOLD)
        return img
    return draw


# ---------- Saja's chapter (times in edit seconds, relative to the card's start) ----------
def rows_card(label_txt, rows, t_rows, big=None, t_big=0.0, bg=IVORY, fg=INK, sub=MUTED):
    """A label, an optional big line, then rows that appear one by one (each: (main, small))."""
    def draw(t):
        img, d = card(bg)
        R.spaced(d, (160, 220), label_txt, R.font(R.SANS_M, 26), GOLDT if bg == IVORY else GOLD, 6)
        y = 280
        if big:
            R.fade_text(img, (152, y), big, R.font(R.SERIF, 110), fg, bg, a_in(t, t_big, 0.5), dy=16); y += 170
        for (main, small), t0 in zip(rows, t_rows):
            a = a_in(t, t0, 0.45)
            fs = 72
            while ImageDraw.Draw(img).textlength(main, font=R.font(R.SERIF, fs)) > LW - 200 and fs > 52: fs -= 2
            R.fade_text(img, (160, y), main, R.font(R.SERIF, fs), fg, bg, a, dy=12)
            if small: R.fade_text(img, (162, y + 88), small, R.font(R.SANS, 38), sub, bg, a, dy=6)
            y += 172 if small else 118
        return img
    return draw
def big_type_full(lines, t_lines, dur, name):
    """Full-screen ink card, big serif lines appearing one by one (1920x1080)."""
    def draw(t):
        img = Image.new("RGB", (1920, 1080), INK)
        for i, (ln, t0) in enumerate(zip(lines, t_lines)):
            R.fade_text(img, (960, 430 + i * 170), ln, R.font(R.SERIF, 140), WHITE if i == 0 else GOLD, INK, a_in(t, t0, 0.5), anchor="mm", dy=16)
        return img
    return anim(name, dur, draw, size=(1920, 1080))


def data_full(t_cols, dur, name):
    """Full-screen ink card: the data stays where it is created (two columns appear on her words)."""
    cols = [("Hair results", "L'Oréal and the salon", "with Layla's consent"), ("Booking data", "ServiceMarket", "")]
    def draw(t):
        img = Image.new("RGB", (1920, 1080), INK); d = ImageDraw.Draw(img)
        R.spaced(d, (160, 250), "THE DATA STAYS WHERE IT'S CREATED", R.font(R.SANS_M, 28), R.mix(INK, GOLD, a_in(t, 0, 0.5)), 7)
        for i, ((what, who, note), t0) in enumerate(zip(cols, t_cols)):
            a = a_in(t, t0, 0.5); x = 160 + i * 860
            R.fade_text(img, (x, 360), what, R.font(R.SANS_M, 40), (200, 194, 186), INK, a, dy=10)
            d.rectangle([x, 430, x + int(80 * a), 432], fill=GOLD)
            R.fade_text(img, (x - 6, 470), who, R.font(R.SERIF, 72), WHITE, INK, a, dy=14)
            if note: R.fade_text(img, (x, 600), note, R.font(R.SANS, 36), GOLD, INK, a_in(t, t0 + 0.6, 0.5))
        return img
    return anim(name, dur, draw, size=(1920, 1080))

def price_full(t_big, t_rows, dur, name):
    """Full-screen ink card: the price, then what it covers (1920x1080)."""
    rows = ["2 home visits", "the scans", "her products", "our fee fits inside"]
    def draw(t):
        img = Image.new("RGB", (1920, 1080), INK); d = ImageDraw.Draw(img)
        R.spaced(d, (160, 250), "ONE SUBSCRIPTION · 12 WEEKS · ABOUT", R.font(R.SANS_M, 28), R.mix(INK, GOLD, a_in(t, 0, 0.5)), 7)
        R.fade_text(img, (150, 310), "AED 1,000", R.font(R.SERIF, 200), WHITE, INK, a_in(t, t_big, 0.6), dy=18)
        for i, (r, t0) in enumerate(zip(rows, t_rows)):
            a = a_in(t, t0, 0.45); x = 160 + i * 420
            d.rectangle([x, 640, x + int(60 * a), 642], fill=GOLD)
            R.fade_text(img, (x, 670), r, R.font(R.SANS, 44), GOLD if i == 3 else (236, 230, 220), INK, a, dy=8)
        return img
    return anim(name, dur, draw, size=(1920, 1080))

def ask_card(t_rows, t_final):
    """Chapter 6 climax (left half, ink): the ask builds on his words, then gives way to 'Give us 12 weeks.'"""
    rows = [("90 days in Dubai", "inside the €3m already planned"), ("Proof, not volume", None), ("ServiceMarket at the door", None),
            ("The salon in the room", None), ("And your support", None)]
    def draw(t):
        img, d = card(INK)
        out = 1 - a_in(t, t_final - 0.2, 0.4)
        R.spaced(d, (160, 200), "OUR ASK", R.font(R.SANS_M, 28), R.mix(INK, GOLD, a_in(t, 0, 0.5)), 7)
        y = 260
        for (main, small), t0 in zip(rows, t_rows):
            a = a_in(t, t0, 0.45) * out
            R.fade_text(img, (160, y), main, R.font(R.SERIF, 66), WHITE, INK, a, dy=10)
            if small: R.fade_text(img, (162, y + 84), small, R.font(R.SANS, 38), GOLD, INK, a, dy=6)
            y += 168 if small else 110
        for i, ln in enumerate(("Give us", "12 weeks.")):
            R.fade_text(img, (152, 380 + i * 170), ln, R.font(R.SERIF, 150), WHITE if i == 0 else GOLD, INK, a_in(t, t_final + 0.15 * i, 0.6), dy=18)
        return img
    return draw

# ---------- full-screen footage with type ----------
def type_png(name, lab, big, line):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    R.spaced(d, (160, 600), lab, R.font(R.SANS_M, 26), GOLD, 7)
    d.text((152, 640), big, font=R.font(R.SERIF, 130), fill=WHITE)
    if line: d.text((160, 820), line, font=R.font(R.SANS, 48), fill=(240, 235, 226))
    return png(img, name)
def shade_png():
    """Soft dark gradient from the lower left, so white type reads on bright footage."""
    img = Image.new("RGBA", (1920, 1080)); px = img.load()
    for y in range(0, 1080, 4):
        for x in range(0, 1920, 4):
            a = max(0.0, 1 - (((x - 0) / 1500) ** 2 + ((1080 - y) / 760) ** 2) ** 0.5)
            for dy in range(4):
                for dx in range(4): px[x + dx, y + dy] = (17, 17, 17, int(200 * a))
    return png(img, "shade.png")
def full_seq(name, clips, dur, types):
    """clips: [(src, src_from, length)] joined with dissolves, slow push-in; types: [(t0, t1, png)] relative to the start."""
    parts = []
    for i, (src, a, n) in enumerate(clips):
        p = os.path.join(TMP, f"{name}_c{i}.mp4")
        ff("-ss", f"{a}", "-t", f"{n + XF + 0.1:.3f}", "-i", src, "-an", "-vf", "fps=30,scale=1920:1080", *ENC, p); parts.append(p)
    ins, fc, last, acc = [], [], "0:v", 0.0
    for p in parts: ins += ["-i", p]
    for i in range(1, len(parts)):
        acc += clips[i - 1][2]
        fc.append(f"[{last}][{i}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}[x{i}]"); last = f"x{i}"
    fc.append(f"[{last}]scale=w='trunc(1920*(1+0.06*t/{dur})/2)*2':h=-2:eval=frame,crop=1920:1080,setsar=1[p0]"); last = "p0"
    k = len(parts)
    ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", SHADE]; fc.append(f"[{last}][{k}:v]overlay=0:0[p1]"); last, k = "p1", k + 1
    for t0, t1, pngp in types:
        ins += ["-loop", "1", "-t", f"{dur:.3f}", "-i", pngp]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={t0}:d=0.5:alpha=1,fade=out:st={t1 - 0.4}:d=0.4:alpha=1[t{k}]")
        fc.append(f"[{last}][t{k}]overlay=x=0:y='12*(1-min(1,max(0,(t-{t0})/0.6)))'[p{k}]"); last, k = f"p{k}", k + 1
    out = os.path.join(TMP, f"{name}.mp4")
    ff(*ins, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-t", f"{dur:.3f}", *ENC, "-an", out); return out

# ---------- assembly ----------
GRADES = json.load(open("edits/colour_grades.json"))   # scripts/colour_match.py: one colour standard for all six speakers
FIN = "highpass=f=100,equalizer=f=250:t=q:w=1.2:g=-3,equalizer=f=3200:t=q:w=1.4:g=2,acompressor=threshold=-24dB:ratio=2:attack=15:release=200:makeup=1"   # after Descript Studio Sound
LOOK = "eq=contrast=1.04:saturation=0.94,colorbalance=rs=0.015:bs=-0.015:rm=0.01:bm=-0.01"   # one shared, slightly warm look
def prep_take(raw, a, b, out, mirror=False, denoise=False, loud=-16, audio=None, landscape=False, sp=1.0, look=""):
    """Trim, mirror if needed, speed up (pitch kept), clean voice, shared colour look.
    audio: optional separate voice file with the same timing as raw (e.g. Descript Studio Sound export)."""
    vf = f"setpts=PTS/{sp},fps=30," + ("scale=1920:1080" if landscape else "scale=1080:1920") + (",hflip" if mirror else "") + "," + (look or LOOK)
    if audio:   # already enhanced: only a gentle leveller
        af = "highpass=f=70,acompressor=threshold=-24dB:ratio=2:attack=15:release=200:makeup=1"
    else:
        af = "highpass=f=80" + (",afftdn=nf=-30,equalizer=f=3000:t=q:w=1.2:g=3,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=200:makeup=2" if denoise else "")
    af = (f"atempo={sp}," if sp != 1 else "") + af + f",loudnorm=I={loud}:TP=-1.5:LRA=7"
    ins = ["-ss", f"{a}", "-to", f"{b}", "-i", raw] + (["-ss", f"{a}", "-to", f"{b}", "-i", audio] if audio else [])
    ff(*ins, "-map", "0:v", "-map", f"{1 if audio else 0}:a", "-vf", vf, "-af", af, "-ar", "48000", "-ac", "2",
       *ENC, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    return out

def speaker_full(take, t0, dur, name, push=1.05, z0=1.22, y0=0.42, x0=0.5):
    """The (landscape) speaker full screen for dur seconds from edit time t0, with a slow push-in."""
    out = os.path.join(TMP, name + ".mp4")
    ff("-ss", f"{t0:.3f}", "-t", f"{dur + 0.1:.3f}", "-i", take, "-an", "-vf",
       f"scale=w='trunc(1920*{z0}*(1+{push - 1}*t/{dur})/2)*2':h=-2:eval=frame,crop=1920:1080:(iw-1920)*{x0}:(ih-1080)*{y0},setsar=1,fps=30", *ENC, out)
    return out

def left_clip(src, dur, n, name):
    p = os.path.join(TMP, f"{name}_l{n:02d}.mp4")
    path, _, off = src.partition("@")
    if path.endswith(".png"):
        ff("-loop", "1", "-t", f"{dur:.3f}", "-i", path, "-vf", "fps=30,format=yuv420p", *ENC, "-an", p)
    else:   # 16:9 clip -> centre 960x1080; 960-wide cards pass through; looped if short
        ff("-ss", off or "0", "-stream_loop", "-1", "-i", path, "-t", f"{dur:.3f}", "-an", "-vf", f"fps=30,scale=-2:1080,crop={LW}:1080", *ENC, p)
    return p

def build(name, take, right, lefts, fulls, lt, line, lt_at, off, sp=1.0, map_t=None):
    """right = (scale width, crop x, crop y, zoom (t0, t1, z) or None); lefts: [(t, src, transition)] with
    transition 'fade' or 'cut' into that item; fulls: [(t0, t1, mp4)]. Times in raw seconds; off = trim start."""
    T = length(take)
    M = map_t or (lambda t: (t - off) / sp)   # with map_t, lefts are already in edit seconds; fulls stay in raw seconds
    starts = [max(0.0, s) if map_t else max(0.0, M(s)) for s, _, _ in lefts] + [T]
    trans = [tr for _, _, tr in lefts]
    xd = [XF if tr == "fade" else 1 / FPS for tr in trans]                   # a 'cut' is a 1-frame mix
    parts = [left_clip(src, b - a + (xd[n + 1] if n + 1 < len(lefts) else 0) + 0.1, n, name)   # +0.1: frame rounding
             for n, ((_, src, _), a, b) in enumerate(zip(lefts, starts, starts[1:]))]
    ins, fc, last = [], [], "0:v"
    for p in parts: ins += ["-i", p]
    for n in range(1, len(parts)):
        fc.append(f"[{last}][{n}:v]xfade=transition=fade:duration={xd[n]:.3f}:offset={starts[n]:.3f}[x{n}]"); last = f"x{n}"
    leftv = os.path.join(TMP, f"{name}_left.mp4")
    ff(*ins, "-filter_complex", ";".join(fc) if fc else "[0:v]null[x0]", "-map", f"[{last if fc else 'x0'}]", "-t", f"{T:.3f}", *ENC, "-an", leftv)
    sw, cx, cy, zoom = right
    if zoom:     # slow push-in on the speaker between t0 and t1 (raw seconds), eased, then held; or a ready z(t) expression
        if isinstance(zoom, str): zs = f"({zoom})"
        else:
            t0, t1, z = (zoom[0] - off) / sp, (zoom[1] - off) / sp, zoom[2]
            zs = f"(1+{z - 1}*(st(0,clip((t-{t0})/{t1 - t0},0,1));ld(0)*ld(0)*(3-2*ld(0))))"
        rv = (f"[1:v]scale=w='trunc({sw}*{zs}/2)*2':h=-2:eval=frame,"
              f"crop=960:1080:x='({cx}+480)*iw/{sw}-480':y='({cy}+540)*iw/{sw}-540',setpts=PTS-STARTPTS[r]")
    else:
        rv = f"[1:v]scale={sw}:-2,crop=960:1080:{cx}:{cy},setpts=PTS-STARTPTS[r]"
    ins = ["-i", leftv, "-i", take]
    fc = [rv, "[0:v][r]hstack=inputs=2[s0]"]; last, k = "s0", 2
    json.dump([[round(M(a), 3), round(min(M(b), T), 3)] for a, b, _ in fulls], open(f"edits/fulls_{name}.json", "w"))
    for a, b, mp4 in fulls:
        a, b = M(a), min(M(b), T)
        ins += ["-itsoffset", f"{a:.3f}", "-i", mp4]
        fc.append(f"[{k}:v]format=yuva420p,fade=in:st={a:.3f}:d={XF}:alpha=1,fade=out:st={b - XF:.3f}:d={XF}:alpha=1[f{k}]")
        fc.append(f"[{last}][f{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[s{k}]"); last, k = f"s{k}", k + 1
    for pp, (a, b) in [o for o in ((lt, lt_at), (line, (0.5, 6.5))) if o[0]]:
        ins += ["-loop", "1", "-t", f"{T:.3f}", "-i", pp]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={a}:d=0.4:alpha=1,fade=out:st={b - 0.4}:d=0.4:alpha=1[o{k}]")
        fc.append(f"[{last}][o{k}]overlay=0:0[s{k}]"); last, k = f"s{k}", k + 1
    out = os.path.join(OUT, f"{name}_edit.mp4")
    ff(*ins, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-t", f"{T:.3f}", *ENC, "-an", out)
    print("wrote", out, round(T, 2), "s")

def layla_line(text):   # same Layla line as the animatic
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = R.font(R.SERIF, 40); w = d.textlength(text, font=f)
    d.rectangle([140, 830, 140 + w + 40, 905], fill=R.IVORY + (235,)); d.text((160, 843), text, font=f, fill=R.INK)
    return img

if __name__ == "__main__":
    # inputs by environment: RAW1 (Amjad), RAW4 (Rebecca), RAW6 + AUD6 (Ignacio, Studio Sound voice); CH = chapters to build
    CH = os.environ.get("CH", "1,4,6").split(",")
    SHADE = shade_png()
    if "1" in CH:
        # ===== Chapter 1 · Amjad (raw 86.7 s, landscape; speech 1.7-84.5) =====
        OFF1, SP1 = 1.4, 1.08
        E = lambda t: (t - OFF1) / SP1                       # raw -> edit seconds
        t1 = prep_take(os.environ["RAW1"], OFF1, 85.2, "out/speakers/M4_S1_Amjad_edit.mp4", landscape=True, sp=SP1, look=GRADES["Amjad"])
        T1 = length(t1)
        pro = full_seq("full_progo", [(L.format("6c"), 1.0, E(25.6) - E(21.0))], E(25.6) - E(21.0),
                       [(0.2, E(25.6) - E(21.0), type_png("ty_progo.png", "THAT'S WHAT CHANGES", "PRO•GO", None)),
                        (E(23.4) - E(21.0), E(25.6) - E(21.0), type_png("ty_progo_l.png", "", "", "a 12-week care subscription"))])
        amjad_full = speaker_full(t1, E(80.1), T1 - E(80.1), "amjad_full")
        cap0 = 39.1
        build("ch1", t1, (2160, 580, 130, None),
              lefts=[(0, "out/layla/layla_1_app.mp4", "fade"),                                        # "Layla is made up ..." (the salon's invitation on her phone)
                     (5.8, anim("facts", E(11.9) - E(5.8), facts([E(t) - E(5.8) for t in (5.94, 7.5, 9.04)])), "fade"),
                     (11.9, L.format("3c") + "@2", "fade"), (13.75, L.format("1c"), "cut"),           # "at the salon" / "a box from the pharmacy"
                     (16.25, L.format("1b"), "fade"),                                                   # "neither tells her ..."
                     (25.4, "out/p1_scan_result_58.mp4", "fade"),                                       # "we measure her hair"
                     (27.3, L.format(3), "fade"),                                                       # "a professional from her own salon ... twice"
                     (32.2, "out/layla/layla_5_app.mp4", "fade"),                                       # "12 weeks later, we measure again"
                     (35.0, anim("seesit", E(39.1) - E(35.0), seesit(E(36.7) - E(35.0), E(37.9) - E(35.0))), "fade"),
                     (cap0, anim("capability", E(63.6) - E(cap0),
                                 capability([E(t) - E(cap0) for t in (41.66, 42.84, 43.9)], E(46.4) - E(cap0),
                                            [E(t) - E(cap0) for t in (50.1, 54.3, 55.2, 56.2)])), "fade"),
                     (63.6, "out/layla/layla_3g_slow.mp4", "fade"),                                    # "Layla's living room is not the place to learn"
                     (68.7, anim("bbp", T1 - E(68.7) + 0.2,
                                 build_buy_partner([E(t) - E(68.7) for t in (68.84, 70.3, 71.05)],
                                                   E(72.9) - E(68.7), E(78.4) - E(68.7), E(80.3) - E(68.7))), "fade")],
              fulls=[(21.0, 25.6, pro), (80.1, 999, amjad_full)],                                      # PRO•GO full screen; [LENS] "So we partner"
              lt="out/lower_thirds/LT_S1_Amjad.png", line=png(layla_line("Week 0. Her salon sends a free hair scan."), "line1.png"),
              lt_at=(1, 5), off=OFF1, sp=SP1)
    if "3" in CH:
        # ===== Chapter 3 · Qhakazile (Drive original, landscape; three cuts under full-screen moments; tight frame keeps a logo scarf out of shot) =====
        SP3 = 1.10; KEEP3 = [(2.1, 32.55), (33.45, 45.3), (47.72, 55.9), (58.82, 85.3)]   # cut: "yet", "Data ownership is clearly defined.", "Commercially, the numbers must work."
        def E(t):
            acc = 0.0
            for a, b in KEEP3:
                if t < b: return (acc + max(0.0, t - a)) / SP3
                acc += b - a
            return acc / SP3
        t3 = "out/speakers/M4_S3_Qhakazile_edit.mp4"
        parts = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(KEEP3))
        parts = parts.replace("[0:a]", "[1:a]")             # voice: Descript Studio Sound export, same timing as the raw
        fc3 = parts + "".join(f"[v{i}][a{i}]" for i in range(len(KEEP3))) + f"concat=n={len(KEEP3)}:v=1:a=1[v][a];" \
              f"[v]setpts=PTS/{SP3},fps=30,scale=1920:1080,{GRADES['Qhakazile']},unsharp=5:5:0.35,format=yuv420p[vo];" \
              f"[a]atempo={SP3},{FIN},loudnorm=I=-16:TP=-1.5:LRA=7[ao]"
        ff("-i", os.environ["RAW3"], "-i", "out/voice/qhakazile_studio.m4a", "-filter_complex", fc3, "-map", "[vo]", "-map", "[ao]", "-ar", "48000", "-ac", "2", *ENC, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", t3)
        T3 = length(t3)
        r = lambda t0, ts: [E(x) - E(t0) for x in ts]
        pilot = big_type_full(["A paid pilot.", "Not an acquisition."], [0.15, E(31.75) - E(29.7)], E(33.7) - E(29.7), "paidpilot")
        # she reads most of her lines: about half the chapter goes full screen on Layla or the numbers, she stays for the partners, the deal and the close
        visit1 = full_seq("full_visit1", [(L.format("3h"), 0.0, 2.9), (L.format("3h"), 5.8, E(9.4) - E(4.6) - 2.9)], E(9.4) - E(4.6),
                          [(0.2, E(9.4) - E(4.6), type_png("ty_v1.png", "WEEK 2", "Visit 1 of 2", None)),
                           (1.6, E(9.4) - E(4.6), type_png("ty_v1_l.png", "", "", "Her own colourist. At home. In private."))])
        price = price_full(E(61.0) - E(59.5), r(59.5, (64.0, 65.9, 66.6, 68.2)), E(72.9) - E(59.5), "pricefull")
        uae = full_seq("full_uae", [(L.format("0c"), 3.0, E(81.6) - E(73.1))], E(81.6) - E(73.1),
                       [(0.3, E(81.6) - E(73.1), type_png("ty_uae.png", "IF THE PILOT WORKS", "The UAE", None)),
                        (E(76.0) - E(73.1), E(81.6) - E(73.1), type_png("ty_uae_l.png", "", "", "a longer-term agreement with ServiceMarket"))])
        data = data_full(r(44.6, (47.8, 52.9)), E(59.0) - E(44.6), "datafull")
        build("ch3", t3, (1920, 720, 0, None),                                                # medium framing, scarf as it is
              lefts=[(0, L.format(3), "fade"),                                                   # "Week two. Dana arrives ..."
                     (E(9.5), anim("partners3", E(29.7) - E(9.5), rows_card("THREE PARTNERS MAKE THAT HOUR",
                          [("The salon", "Dana, and the client stays theirs"), ("L'Oréal", "the products and the plan"),
                           ("ServiceMarket", "booking, insurance, payment, permits + setup & clean-up")], r(9.5, (12.3, 15.6, 19.7)))), "fade"),
                     (E(33.5), anim("deal", E(44.6) - E(33.5), rows_card("THE DEAL · A VENTURE-CLIENT PILOT",
                          [("We buy the service", "paid per visit, 90 days. We don't invest."), ("In return", "the only colour subscription on their platform")],
                          r(33.5, (33.6, 38.3)))), "fade"),
                     (E(59.0), anim("price", E(72.9) - E(59.0), rows_card("ONE SUBSCRIPTION · 12 WEEKS · ABOUT",
                          [("2 home visits", None), ("The scans", None), ("Her products", None), ("Our fee fits inside", None)],
                          r(59.0, (64.0, 65.9, 66.6, 68.2)), big="AED 1,000", t_big=E(61.0) - E(59.0))), "fade"),
                     (E(72.9), L.format("0c") + "@5", "fade"),                                  # "longer-term agreement ... across the UAE"
                     (E(81.6), anim("only3", T3 - E(81.6) + 0.2, rows_card("",
                          [("Only when", None), ("the economics", None), ("justify it.", None)], [0.2, 0.5, 0.8], bg=INK, fg=WHITE, sub=GOLD)), "fade")],
              fulls=[(4.6, 9.4, visit1), (29.7, 33.7, pilot), (44.6, 59.0, data), (59.5, 72.9, price), (73.1, 81.6, uae)],
              lt="out/lower_thirds/LT_S3_Qhakazile.png", line=None,
              lt_at=(0.6, 3.9), off=0, sp=1, map_t=E)
    if "5" in CH:
        # ===== Chapter 5 · Saja (IMG_1473 from Drive, landscape; two slips cut: "weeks weeks", "no committee") =====
        SP5 = 1.08; KEEP = [(0.2, 3.68), (4.25, 43.85), (44.95, 81.2)]
        def E(t):                                          # raw -> edit seconds across the two cuts
            acc = 0.0
            for a, b in KEEP:
                if t < b: return (acc + max(0.0, t - a)) / SP5
                acc += b - a
            return acc / SP5
        raw5 = os.environ["RAW5"]; t5 = "out/speakers/M4_S5_Saja_edit.mp4"
        parts = "".join(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{i}];" for i, (a, b) in enumerate(KEEP))
        fc5 = parts + "".join(f"[v{i}][a{i}]" for i in range(len(KEEP))) + f"concat=n={len(KEEP)}:v=1:a=1[v][a];" \
              f"[v]setpts=PTS/{SP5},fps=30,scale=1920:1080,{GRADES['Saja']},format=yuv420p[vo];" \
              f"[a]atempo={SP5},afftdn=nf=-42:nr=14:tn=1,agate=threshold=0.012:ratio=2:range=0.25:attack=8:release=250,{FIN},loudnorm=I=-16:TP=-1.5:LRA=7[ao]"   # extra: room noise about 9 dB lower in her pauses
        ff("-i", raw5, "-i", "out/voice/saja_studio.m4a", "-filter_complex", fc5, "-map", "[vo]", "-map", "[ao]", "-ar", "48000", "-ac", "2", *ENC, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", t5)
        T5 = length(t5)
        visit2 = full_seq("full_visit2", [(L.format(4), 0.0, E(7.0) - E(1.3))], E(7.0) - E(1.3),
                          [(0.2, E(7.0) - E(1.3), type_png("ty_v2.png", "WEEK 10", "Visit 2 of 2", None)),
                           (E(4.6) - E(1.3), E(7.0) - E(1.3), type_png("ty_v2_l.png", "", "", "a second scan, while the colour sets"))])
        leader = big_type_full(["One leader.", "Not a committee."], [0.15, E(45.2) - E(42.6)], E(46.6) - E(42.6), "leader")
        saja_full = speaker_full(t5, E(74.6), T5 - E(74.6), "saja_full", z0=1.5, y0=0.15, x0=0.88)   # she sits right in her frame
        r = lambda t0, ts: [E(x) - E(t0) for x in ts]
        build("ch5", t5, (2160, 980, 0, None),
              lefts=[(0, L.format("5b"), "fade"),
                     (E(7.0), L.format("5b") + "@4", "fade"),                                       # "where a pilot teaches you something ..."
                     (E(12.3), anim("pilot", E(24.3) - E(12.3), rows_card("HERE IS OURS",
                          [("Downtown + Business Bay", "two communities"), ("3–5 partner salons", None), ("90 days", "from Q2 2027")],
                          r(12.3, (16.2, 18.2, 20.3)), big="Dubai", t_big=E(14.1) - E(12.3))), "fade"),
                     (E(24.3), anim("byhand", E(31.8) - E(24.3), rows_card("AT THE START",
                          [("No new app", None), ("Matched by hand", "client to professional, on purpose")], r(24.3, (24.5, 26.7)))), "fade"),
                     (E(31.8), anim("app2028", E(37.7) - E(31.8), rows_card("THE APP",
                          [("after the test", "proves people want this")], r(31.8, (34.3,)), big="2028", t_big=0.1)), "fade"),
                     (E(37.7), anim("owner", E(52.3) - E(37.7), rows_card("WHO OWNS IT",
                          [("One PRO•GO lead", "Professional Products Middle East"), ("Salons and budget", "in one leader's hands"),
                           ("Innovation Board", "reviews it every quarter")], r(37.7, (38.1, 46.7, 49.5)))), "fade"),
                     (E(52.3), anim("numbers", E(66.5) - E(52.3), rows_card("EVERY WEEK, THREE NUMBERS",
                          [("≥ 40 % book visit 2", "within 90 days"), ("> 0 margin per visit", "after the salon and ServiceMarket"),
                           ("+5 points", "on the hair score")], r(52.3, (54.5, 58.9, 63.8)))), "fade"),
                     (E(66.5), "out/p4_rescan_66.mp4", "fade")],                                    # "Layla went from 58 to 66 by week ten"
              fulls=[(1.3, 7.0, visit2), (42.6, 46.6, leader), (74.6, 999, saja_full)],
              lt="out/lower_thirds/LT_S5_Saja.png", line=None, lt_at=(E(7.4), E(11.4)), off=0, sp=1, map_t=E)
    if "4" in CH:
        # ===== Chapter 4 · Rebecca (raw 75.5 s, speech 3.1-72.2) =====
        OFF4 = 2.6
        t4 = prep_take(os.environ["RAW4"], OFF4, 73.5, "out/speakers/M4_S4_Rebecca_edit.mp4", look=GRADES["Rebecca"])
        salon = full_seq("full_salon", [(L.format(3), 0.0, 5.6), (L.format("3g"), 0.0, 5.5), (L.format("3c"), 5.5, 2.8)], 13.9,   # 3g before its 6 s join
                         [(3.5, 13.9, type_png("ty_salon.png", "WHO WINS · 1", "The salon", None)),
                          (3.8, 9.3, type_png("ty_salon_l1.png", "", "", "keeps her client")),
                          (9.2, 13.9, type_png("ty_salon_l2.png", "", "", "earns on a visit it couldn't make alone"))])
        smkt = full_seq("full_smkt", [(L.format("2c"), 0.0, 7.8)], 7.8,
                        [(0.4, 7.8, type_png("ty_sm.png", "WHO WINS · 2", "ServiceMarket", None)),
                         (0.7, 4.7, type_png("ty_sm_l1.png", "", "", "the L'Oréal name behind it")),
                         (4.6, 7.8, type_png("ty_sm_l2.png", "", "", "a door to the salons"))])
        build("ch4", t4, (1260, 0, 450, (47.8, 61.0, 1.08)),   # framed higher: more headroom below, eyes nearer the top third
              lefts=[(0, L.format("4b"), "fade"), (7.1, L.format("4b") + "@5.2", "cut"),     # kit: front view, cut to the side view (the clip jumps angle at 4.7 s)
                     (10.9, L.format("4c"), "fade"),                                          # mask: clean first 2.6 s only (arms bend wrongly after 3 s)
                     (26.2, png(c_salon10(), "c_salon10.png"), "fade"),                      # "Our target is 10 % ..." (in under the dissolve)
                     (32.4, L.format("3c"), "fade"),                                          # "the professional stays theirs"
                     (45.6, anim("learns", 7.35, learns(7.35, 2.2, 4.04)), "fade"),          # pause, then "And L'Oréal learns" (47.8)
                     (52.95, L.format("1b") + "@0.6", "cut"),                                 # "real hair"
                     (54.85, L.format(2) + "@0.3", "cut"),                                    # "in real homes"
                     (56.4, anim("weeks", 1.5, weeks(1.5)), "cut"),                           # "over 12 weeks"
                     (57.9, anim("lab", 1.45, struck("a lab.", 1.45, 0.75)), "cut"),          # "not in a lab"
                     (59.35, anim("survey", 1.6, struck("a survey.", 1.6, 0.9)), "cut"),      # "not in a survey"
                     (60.95, L.format(4), "fade"),                                            # "worth more than the margin"
                     (66.0, anim("partners", 7.6, partners(7.6, (0.2, 0.6, 1.0), 1.64)), "fade")],   # "Three partners ..."
              fulls=[(13.0, 26.9, salon), (37.8, 45.6, smkt)],
              lt="out/lower_thirds/LT_S4_Rebecca.png", line=png(layla_line("Week 4. Nothing to report."), "line4.png"),
              lt_at=(1, 5), off=OFF4)
    if "6" in CH:
        # ===== Chapter 6 · Ignacio (IMG_9977, the original of the same take: sharper picture; voice = Studio Sound export) =====
        OFF6 = 0.0
        END6 = 72.65                                        # "Layla already did." ends 72.2; he reaches for the phone after 72.8
        t6 = prep_take(os.environ["RAW6"], OFF6, END6, "out/speakers/M4_S6_Ignacio_edit.mp4", mirror=True, loud=-15,
                       audio=os.environ.get("AUD6"), look=GRADES["Ignacio"])
        sm = lambda a, d: f"(st(1,clip((t-{a})/{d},0,1))*0+ld(1)*ld(1)*(3-2*ld(1)))"
        Z6 = "+".join(["1"] + [f"{k}*{sm(a, 0.5)}" for a, k in ((18.2, 0.07), (33.0, -0.07), (40.8, 0.07), (48.7, -0.07))]
                      + [f"0.14*{sm(56.4, 13.4)}", f"0.02*{sm(0, 18.0)}"])   # a step in at each rule, back out at the next; slow push through the ask
        prove = big_type_full(["One Layla proves nothing.", "300 could."], [0.1, 10.8 - 8.4], 14.6 - 8.4, "prove300")
        stop = big_type_full(["Stopping early is cheaper", "than being right too late."], [0.1, 53.9 - 51.9], 56.2 - 51.9, "stopearly")
        build("ch6", t6, (1080, 110, 470, Z6),
              lefts=[(0, "out/layla/layla_5_app.mp4", "fade"), (7.6, png(c_rule(None), "rule_0.png"), "fade"),
                     (18.0, png(c_rule(0), "rule_1.png"), "fade"),
                     (32.6, png(c_rule(1), "rule_2.png"), "fade"), (40.5, png(c_rule(2), "rule_3.png"), "fade"),
                     (48.4, png(c_rule(3), "rule_4.png"), "fade"),
                     (56.2, anim("ask", END6 - 56.2 + 0.2, ask_card([58.9 - 56.2, 62.8 - 56.2, 64.7 - 56.2, 66.3 - 56.2, 68.0 - 56.2], 69.8 - 56.2)), "fade")],
              fulls=[(1.5, 7.6, "out/03_score_counter_v2.mp4"), (8.4, 14.6, prove), (51.9, 56.2, stop)],   # 74 lands as he says it (5.4-5.9 s)
              lt="out/lower_thirds/LT_S6_Ignacio.png", line=None, lt_at=(14.8, 18.8), off=OFF6)
        e6 = os.path.join(OUT, "ch6_edit.mp4"); ff("-i", e6, "-vf", f"fade=out:st={END6 - 0.5:.2f}:d=0.5", *ENC, "-an", e6 + ".f.mp4"); os.replace(e6 + ".f.mp4", e6)
