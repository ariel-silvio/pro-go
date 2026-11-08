"""Chapter edits for takes recorded in portrait: chapter 4 (Rebecca) and chapter 6 (Ignacio).
Half-half split (960 | 960) like Ariel's chapter: left = Layla, cards, animated type; right = the speaker,
portrait take scaled and cropped to 960x1080. Full-screen footage moments with type dissolve over the split.
All times below are seconds in the RAW take (sentence and word timings checked against the audio envelope).
Usage (from video/): python3 scripts/portrait_edit.py RAW_REBECCA.mp4 RAW_IGNACIO.mp4
  -> out/speakers/M4_S4_Rebecca_edit.mp4, out/speakers/M4_S6_Ignacio_edit.mp4 (voice + portrait picture)
  -> out/edits/ch4_edit.mp4, out/edits/ch6_edit.mp4 (1920x1080 picture only, length of the trimmed take)"""
import os, subprocess, sys
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
def c_salon10(): return big_number("WHO WINS · THE SALON", "+10 %", "more income per partner salon", "by 2030", "Source: M2 dashboard (Team D target)")
def c_300():     return big_number("PRO•GO · 2027 TARGET", "300", "active care clients in Dubai", "one Layla proves nothing", "Source: M2 dashboard (Team D target)")

RULES = [("GO", ["40 % come back", "within 90 days"], "€7m released"),
         ("CHANGE", ["They come back,", "the money doesn't"], "new price or deal"),
         ("FALL BACK", ["Salons say no"], "salon subscription"),
         ("STOP", ["2 missed reviews"], "in a row")]
def c_rule(k):
    """One rule at a time in large type; all four named in a small progress row at the top."""
    img, d = card(); x = 160
    for j, (head, _, _) in enumerate(RULES):          # progress row
        f = R.font(R.SANS_M, 22); col = M4C if j == k else (176, 170, 160)
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
    d.text((160, 960), "Source: M3 frame 4; 40 %, €7m, Q4 2027 review: M2 dashboard", font=R.font(R.SANS, 22), fill=MUTED)
    return img

# ---------- animated cards for Rebecca's climax (ink background) ----------
def learns(dur, t_head, t_sub):
    def draw(t):
        img, d = card(INK); a = a_in(t, t_head, 0.7); b = a_in(t, t_sub, 0.6)
        R.spaced(d, (160, 330), "WHO WINS · L'ORÉAL", R.font(R.SANS_M, 24), R.mix(INK, GOLD, a), 6)
        R.fade_text(img, (160, 380), "L'Oréal", R.font(R.SERIF, 170), WHITE, INK, a, dy=30)
        R.fade_text(img, (160, 560), "learns.", R.font(R.SERIF, 170), WHITE, INK, a_in(t, t_head + 0.25, 0.7), dy=30)
        R.fade_text(img, (165, 790), "for the first time", R.font(R.SANS, 44), GOLD, INK, b, dy=12)
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
def prep_take(raw, a, b, out, mirror=False, denoise=False, loud=-16):
    """Trim, mirror if needed, clean voice; picture kept portrait (1080x1920)."""
    vf = "fps=30,scale=1080:1920" + (",hflip" if mirror else "")
    af = "highpass=f=80" + (",afftdn=nf=-30,equalizer=f=3000:t=q:w=1.2:g=3,acompressor=threshold=-24dB:ratio=2.5:attack=15:release=200:makeup=2" if denoise else "") \
         + f",loudnorm=I={loud}:TP=-1.5:LRA=7"
    ff("-ss", f"{a}", "-to", f"{b}", "-i", raw, "-vf", vf, "-af", af, "-ar", "48000", "-ac", "2",
       *ENC, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    return out

def left_clip(src, dur, n, name):
    p = os.path.join(TMP, f"{name}_l{n:02d}.mp4")
    path, _, off = src.partition("@")
    if path.endswith(".png"):
        ff("-loop", "1", "-t", f"{dur:.3f}", "-i", path, "-vf", "fps=30,format=yuv420p", *ENC, "-an", p)
    else:   # 16:9 clip -> centre 960x1080; 960-wide cards pass through; looped if short
        ff("-ss", off or "0", "-stream_loop", "-1", "-i", path, "-t", f"{dur:.3f}", "-an", "-vf", f"fps=30,scale=-2:1080,crop={LW}:1080", *ENC, p)
    return p

def build(name, take, right, lefts, fulls, lt, line, lt_at, off):
    """right = (scale width, crop x, crop y, zoom (t0, t1, z) or None); lefts: [(t, src, transition)] with
    transition 'fade' or 'cut' into that item; fulls: [(t0, t1, mp4)]. Times in raw seconds; off = trim start."""
    T = length(take)
    starts = [max(0.0, s - off) for s, _, _ in lefts] + [T]
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
    if zoom:     # slow push-in on the speaker between t0 and t1 (raw seconds), eased, then held
        t0, t1, z = zoom[0] - off, zoom[1] - off, zoom[2]
        zs = f"(1+{z - 1}*(st(0,clip((t-{t0})/{t1 - t0},0,1));ld(0)*ld(0)*(3-2*ld(0))))"
        rv = (f"[1:v]scale=w='trunc({sw}*{zs}/2)*2':h=-2:eval=frame,"
              f"crop=960:1080:x='({cx}+480)*iw/{sw}-480':y='({cy}+540)*iw/{sw}-540',setpts=PTS-STARTPTS[r]")
    else:
        rv = f"[1:v]scale={sw}:-2,crop=960:1080:{cx}:{cy},setpts=PTS-STARTPTS[r]"
    ins = ["-i", leftv, "-i", take]
    fc = [rv, "[0:v][r]hstack=inputs=2[s0]"]; last, k = "s0", 2
    for a, b, mp4 in fulls:
        a, b = a - off, b - off
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
    raw4, raw6 = sys.argv[1], sys.argv[2]
    SHADE = shade_png()
    # ===== Chapter 4 · Rebecca (raw 75.5 s, speech 3.1-72.2) =====
    OFF4 = 2.6
    t4 = prep_take(raw4, OFF4, 73.5, "out/speakers/M4_S4_Rebecca_edit.mp4")
    salon = full_seq("full_salon", [(L.format(3), 0.0, 5.6), (L.format("3g"), 0.0, 5.5), (L.format("3c"), 5.5, 2.8)], 13.9,   # 3g before its 6 s join
                     [(3.5, 13.9, type_png("ty_salon.png", "WHO WINS · 1", "The salon", None)),
                      (3.8, 9.3, type_png("ty_salon_l1.png", "", "", "keeps her client")),
                      (9.2, 13.9, type_png("ty_salon_l2.png", "", "", "earns on a visit it couldn't make alone"))])
    smkt = full_seq("full_smkt", [(L.format("2c"), 0.0, 7.8)], 7.8,
                    [(0.4, 7.8, type_png("ty_sm.png", "WHO WINS · 2", "ServiceMarket", None)),
                     (0.7, 4.7, type_png("ty_sm_l1.png", "", "", "the L'Oréal name behind it")),
                     (4.6, 7.8, type_png("ty_sm_l2.png", "", "", "a door to the salons"))])
    build("ch4", t4, (1260, 0, 250, (47.8, 61.0, 1.08)),
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
    # ===== Chapter 6 · Ignacio (raw 73.6 s, recorded mirrored, WhatsApp copy) =====
    OFF6 = 0.0
    t6 = prep_take(raw6, OFF6, 73.5, "out/speakers/M4_S6_Ignacio_edit.mp4", mirror=True, denoise=True, loud=-15)
    build("ch6", t6, (1080, 60, 470, None),
          lefts=[(0, "out/layla/layla_5_app.mp4", "fade"), (7.6, png(c_300(), "c_300.png"), "fade"),
                 (14.5, png(c_rule(None), "rule_0.png"), "fade"), (18.0, png(c_rule(0), "rule_1.png"), "fade"),
                 (32.6, png(c_rule(1), "rule_2.png"), "fade"), (40.5, png(c_rule(2), "rule_3.png"), "fade"),
                 (48.4, png(c_rule(3), "rule_4.png"), "fade"),
                 (56.2, L.format("6c"), "fade"), (65.5, L.format("0c"), "fade")],        # the ask: balcony, then the horizon
          fulls=[(1.5, 7.6, "out/03_score_counter_v2.mp4")],                             # 74 lands as he says it (5.4-5.9 s)
          lt="out/lower_thirds/LT_S6_Ignacio.png", line=None, lt_at=(8.5, 12.5), off=OFF6)
