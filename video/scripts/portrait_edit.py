"""Chapter edits for takes recorded in portrait (chapter 4 Rebecca, chapter 6 Ignacio).
Layout: left 1200 px (Layla, cards), right 720 px (the speaker, portrait take scaled to 720 wide and cropped to 1080 high).
Full-screen moments (service diagram, score) dissolve over the split. Picture follows the sentence timings in
edits/chN_sentences_raw.json (Gemini transcript of the raw take; times relative to the raw file).
Usage (from video/): python3 scripts/portrait_edit.py RAW_REBECCA.mp4 RAW_IGNACIO.mp4
  -> out/speakers/M4_S4_Rebecca_edit.mp4, out/speakers/M4_S6_Ignacio_edit.mp4 (voice + portrait picture)
  -> out/edits/ch4_edit.mp4, out/edits/ch6_edit.mp4 (1920x1080 picture only, length of the trimmed take)"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

LW, RW, XF = 1200, 720, 0.5
OUT = "out/edits"; TMP = os.path.join(OUT, "portrait_parts"); os.makedirs(TMP, exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
L = "out/layla/layla_{}.mp4"

# ---------- cards (1200x1080, ivory, brand kit) ----------
INK, MUTED, GOLDT, GOLD, M4C = R.INK, R.MUTED, R.GOLD_TXT, R.GOLD, R.M4
def card(): img = Image.new("RGB", (LW, 1080), R.IVORY); return img, ImageDraw.Draw(img)
def label(d, y, t, col=GOLDT, x=160): R.spaced(d, (x, y), t, R.font(R.SANS_M, 24), col, 6)
def source(d, t): d.text((160, 960), t, font=R.font(R.SANS, 22), fill=MUTED)
def big_number(label_txt, num, line1, line2, src):
    img, d = card(); label(d, 300, label_txt)
    d.text((150, 340), num, font=R.font(R.SERIF, 240), fill=INK)
    d.rectangle([160, 640, 220, 642], fill=GOLD)
    d.text((160, 670), line1, font=R.font(R.SANS, 40), fill=INK)
    d.text((160, 730), line2, font=R.font(R.SANS, 34), fill=MUTED)
    source(d, src); return img
def c_salon10(): return big_number("PARTNER SALONS · TARGET", "+10 %", "more income per partner salon", "by 2030", "Source: M2 dashboard (Team D target)")
def c_300():     return big_number("PRO•GO · 2027 TARGET", "300", "active care clients in Dubai", "one Layla proves nothing", "Source: M2 dashboard (Team D target)")
RULES = [("GO", "At least 40 % book a second visit within 90 days, and every visit makes money.", "Next €7m released at the Q4 2027 review"),
         ("CHANGE", "They come back, but the money doesn't work.", "New price, new services, or a new deal with ServiceMarket"),
         ("FALL BACK", "Salons won't send their colourists out.", "Test a salon subscription instead"),
         ("STOP", "Two missed reviews in a row.", "Stopping early is cheaper than being right too late")]
def c_rules(active):
    img, d = card(); label(d, 150, "THE RULES · WRITTEN BEFORE THE TEST")
    d.rectangle([160, 200, 220, 202], fill=GOLD)
    for k, (head, cond, then) in enumerate(RULES):
        y = 250 + k * 170; on = k == active; done = active is not None and k < active
        col = INK if on else ((150, 144, 136) if done or active is not None else MUTED)
        if on: d.rectangle([150, y - 14, 156, y + 128], fill=M4C)
        R.spaced(d, (180, y), head, R.font(R.SANS_M, 26), M4C if on else col, 5)
        fs = 32
        while d.textlength(cond, font=R.font(R.SANS, fs)) > LW - 180 - 80: fs -= 1   # keep inside the left panel
        d.text((180, y + 40), cond, font=R.font(R.SANS, fs), fill=col)
        d.text((180, y + 84), "→ " + then, font=R.font(R.SANS, 26), fill=GOLDT if on else col)
    source(d, "Source: M3 frame 4 (after the test we decide); 40 %, €7m, Q4 2027 review: M2 dashboard")
    return img

# ---------- per chapter ----------
def prep_take(raw, a, b, out, mirror=False, denoise=False):
    """Trim, mirror if needed, clean voice, -16 LUFS; picture scaled to 720x1280 (portrait)."""
    vf = "fps=30,scale=720:1280" + (",hflip" if mirror else "")
    af = "highpass=f=80" + (",afftdn=nf=-30" if denoise else "") + ",loudnorm=I=-16:TP=-1.5:LRA=11"
    ff("-ss", f"{a}", "-to", f"{b}", "-i", raw, "-vf", vf, "-af", af, "-ar", "48000", "-ac", "2",
       *ENC, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out)
    return out

def left_clip(src, dur, n, name):
    p = os.path.join(TMP, f"{name}_l{n:02d}.mp4")
    if src.endswith(".png"):
        ff("-loop", "1", "-t", f"{dur:.3f}", "-i", src, "-vf", "fps=30,format=yuv420p", *ENC, "-an", p)
    else:   # 16:9 clip -> centre 1200x1080 window, looped if short
        ff("-stream_loop", "-1", "-i", src, "-t", f"{dur:.3f}", "-an", "-vf", f"fps=30,scale=-2:1080,crop={LW}:1080", *ENC, p)
    return p

def build(name, take, crop_y, lefts, fulls, lt, line, lt_at, off):
    """lefts: [(start, source)] in raw-file seconds; fulls: [(start, end, mp4)]; off = trim start of the take."""
    T = length(take)
    starts = [max(0.0, s - off) for s, _ in lefts] + [T]
    parts = []
    for n, ((_, src), a, b) in enumerate(zip(lefts, starts, starts[1:])):
        parts.append(left_clip(src, b - a + (XF if n < len(lefts) - 1 else 0), n, name))
    # left track with dissolves
    ins, fc, last, acc = [], [], "0:v", 0.0
    for n, p in enumerate(parts): ins += ["-i", p]
    for n in range(1, len(parts)):
        acc += starts[n] - starts[n - 1]
        fc.append(f"[{last}][{n}:v]xfade=transition=fade:duration={XF}:offset={acc:.3f}[x{n}]"); last = f"x{n}"
    left = os.path.join(TMP, f"{name}_left.mp4")
    ff(*ins, "-filter_complex", ";".join(fc) if fc else "[0:v]null[x0]", "-map", f"[{last if fc else 'x0'}]", "-t", f"{T:.3f}", *ENC, "-an", left)
    # split base + full-screen overlays + lower third + Layla line
    ins = ["-i", left, "-i", take]
    fc = [f"[1:v]crop={RW}:1080:0:{crop_y},setpts=PTS-STARTPTS[r]", "[0:v][r]hstack=inputs=2[s0]"]
    last, k = "s0", 2
    for a, b, mp4 in fulls:
        a, b = a - off, b - off
        ins += ["-itsoffset", f"{a:.3f}", "-i", mp4]
        fc.append(f"[{k}:v]format=yuva420p,fade=in:st={a:.3f}:d={XF}:alpha=1,fade=out:st={b - XF:.3f}:d={XF}:alpha=1[f{k}]")
        fc.append(f"[{last}][f{k}]overlay=0:0:eof_action=pass:enable='between(t,{a:.3f},{b:.3f})'[s{k}]"); last, k = f"s{k}", k + 1
    for png, (a, b), x in [o for o in ((lt, lt_at, LW - 960), (line, (0.5, 6.5), 0)) if o[0]]:
        ins += ["-loop", "1", "-t", f"{T:.3f}", "-i", png]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={a}:d=0.4:alpha=1,fade=out:st={b - 0.4}:d=0.4:alpha=1[o{k}]")
        fc.append(f"[{last}][o{k}]overlay={x}:0[s{k}]"); last, k = f"s{k}", k + 1
    out = os.path.join(OUT, f"{name}_edit.mp4")
    ff(*ins, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-t", f"{T:.3f}", *ENC, "-an", out)
    print("wrote", out, round(T, 2), "s")

def png(img, n): p = os.path.join(TMP, n); img.save(p); return p
def layla_line(text):   # same Layla line as the animatic
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = R.font(R.SERIF, 40); w = d.textlength(text, font=f)
    d.rectangle([140, 830, 140 + w + 40, 905], fill=R.IVORY + (235,)); d.text((160, 843), text, font=f, fill=R.INK)
    return img

if __name__ == "__main__":
    raw4, raw6 = sys.argv[1], sys.argv[2]
    # Chapter 4 · Rebecca (raw 75.5 s; speech 3.1-72.8)
    OFF4 = 2.6
    t4 = prep_take(raw4, OFF4, 73.5, "out/speakers/M4_S4_Rebecca_edit.mp4")
    build("ch4", t4, 90,
          lefts=[(0, L.format("4b")), (8.6, L.format("4c")),                       # kit / mask: "Layla uses her kit"
                 (23.0, L.format(3)), (26.6, png(c_salon10(), "c_salon10.png")),    # "earns on a visit" / "+10 % by 2030"
                 (32.0, L.format("3c")), (37.8, L.format("2c")),                    # "the professional stays theirs" / ServiceMarket
                 (47.5, L.format("1b")), (53.8, L.format(4)), (61.0, L.format("6c"))],   # "L'Oréal learns": real hair, real homes
          fulls=[(12.8, 23.0, "out/m4/service_diagram.mp4")],                      # "look at who's winning" -> salon, partner
          lt="out/lower_thirds/LT_S4_Rebecca.png", line=png(layla_line("Week 4. Nothing to report."), "line4.png"),
          lt_at=(1, 5), off=OFF4)
    # Chapter 6 · Ignacio (raw 73.6 s, recorded mirrored, WhatsApp copy 576x1024)
    OFF6 = 0.0
    t6 = prep_take(raw6, OFF6, 73.5, "out/speakers/M4_S6_Ignacio_edit.mp4", mirror=True, denoise=True)
    build("ch6", t6, 130,
          lefts=[(0, L.format(5)), (7.6, png(c_300(), "c_300.png")),
                 (14.5, png(c_rules(None), "rules_0.png")), (18.0, png(c_rules(0), "rules_1.png")),
                 (32.6, png(c_rules(1), "rules_2.png")), (40.5, png(c_rules(2), "rules_3.png")),
                 (48.4, png(c_rules(3), "rules_4.png")),
                 (56.2, L.format("6c")), (65.5, L.format("0c"))],                   # the ask: balcony, then the horizon
          fulls=[(1.5, 7.6, "out/03_score_counter_v2.mp4")],                       # 74 lands as he says it (5.4-5.9 s)
          lt="out/lower_thirds/LT_S6_Ignacio.png", line=None,
          lt_at=(8.5, 12.5), off=OFF6)
