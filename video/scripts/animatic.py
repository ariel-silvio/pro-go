"""Assemble an 8:00 animatic of the M4 video from the rendered graphics, Layla clips and prototype panels.
Speakers are placeholders (name, role, first line, lower third); no voice or music yet.
Usage (from video/): python3 scripts/animatic.py out/animatic
"""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

OUT = sys.argv[1] if len(sys.argv) > 1 else "out/animatic"
TMP = os.path.join(OUT, "parts"); os.makedirs(TMP, exist_ok=True)
FPS, ENC = 30, ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]
L = "out/layla/layla_{}.mp4"; M4 = "out/m4/{}.mp4"; LT = "out/lower_thirds/LT_{}.png"

def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)

def png(img, name):
    p = os.path.join(TMP, name); img.save(p); return p

# ---------- overlays ----------
def speaker_panel(n, name, role, first):
    img = Image.new("RGB", (960, 1080), (43, 41, 38)); d = ImageDraw.Draw(img)
    R.spaced(d, (80, 200), f"SPEAKER · CHAPTER {n}", R.font(R.SANS_M, 22), R.GOLD, 5)
    d.text((80, 250), name, font=R.font(R.SERIF, 58), fill=R.WHITE)
    R.spaced(d, (80, 340), role.upper(), R.font(R.SANS_M, 18), R.GOLD, 4)
    f = R.font(R.SANS, 30)
    for i, ln in enumerate(R.wrap(d, f"“{first}”", f, 720)[:7]):
        d.text((80, 440 + i * 46), ln, font=f, fill=(231, 225, 216))
    d.text((80, 760), "Recording to come · about 70 s · looking screen-left", font=R.font(R.SANS, 24), fill=(150, 144, 136))
    R.spaced(d, (560, 170), "ANIMATIC V15", R.font(R.SANS_M, 18), (150, 144, 136), 4)
    return img

def layla_line(text):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = R.font(R.SERIF, 40); w = d.textlength(text, font=f)
    d.rectangle([140, 830, 140 + w + 40, 905], fill=R.IVORY + (235,))
    d.text((160, 843), text, font=f, fill=R.INK)
    return img

def centred_line(text):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.text((960, 860), text, font=R.font(R.SERIF, 56), fill=R.WHITE, anchor="mm")
    return img

def credits():
    img = Image.new("RGB", (1920, 1080), R.INK); d = ImageDraw.Draw(img)
    R.spaced(d, (960, 250), "L'ORÉAL GROUPE  ·  TEAM D", R.font(R.SANS_M, 24), R.GOLD, 7, True)
    team = ["Amjad Saad Bensalamah", "Ariel De Silvio", "Qhakazile Mathebula", "Rebecca Fernandes", "Saja AlOwayshiq", "Ignacio Montero Alcantara"]
    for i, t in enumerate(team):
        d.text((960, 360 + i * 56), t, font=R.font(R.SERIF, 40), fill=R.WHITE, anchor="mm")
    f = R.font(R.SANS, 24)
    for i, t in enumerate(["Student project for IE Business School. Not affiliated with L'Oréal or ServiceMarket.",
                           "Fictional characters, simulated data. AI use disclosed (Claude, Gemini Omni Flash, Lyria, Descript). Layla's voice is AI-generated."]):
        d.text((960, 760 + i * 40), t, font=f, fill=(170, 164, 156), anchor="mm")
    return img

def face_tile(take, t, box, size=300, k=1.9):
    """A square crop around the speaker's face from their graded take (box: face as fractions of the frame)."""
    fr = os.path.join(TMP, f"face_{os.path.basename(take)}.png")
    ff("-ss", str(t), "-i", take, "-frames:v", "1", fr)
    im = Image.open(fr).convert("RGB"); W, H = im.size
    cx, cy = (box[0] + box[2]) / 2 * W, (box[1] + box[3]) / 2 * H; side = (box[3] - box[1]) * H * k
    im = im.crop((int(cx - side / 2), int(cy - side * 0.46), int(cx + side / 2), int(cy + side * 0.54)))
    return im.resize((size, size), Image.LANCZOS)

def credits_faces():
    """Six faces, six names: the team behind the proposal."""
    img = Image.new("RGB", (1920, 1080), R.INK); d = ImageDraw.Draw(img)
    R.spaced(d, (960, 120), "L'ORÉAL GROUPE  ·  TEAM D", R.font(R.SANS_M, 24), R.GOLD, 7, True)
    crew = [("Amjad Saad Bensalamah", "out/speakers/M4_S1_Amjad_edit.mp4", 30, (.44, .30, .56, .55)),
            ("Ariel De Silvio", "out/speakers/M4_S2_Ariel_take2_graded.mp4", 30, (.49, .30, .63, .60)),
            ("Qhakazile Mathebula", "out/speakers/M4_S3_Qhakazile_edit.mp4", 2, (.49, .22, .62, .45)),
            ("Rebecca Fernandes", "out/speakers/M4_S4_Rebecca_edit.mp4", 30, (.33, .34, .46, .43), 3.4),
            ("Saja AlOwayshiq", "out/speakers/M4_S5_Saja_edit.mp4", 30, (.63, .20, .76, .42)),
            ("Ignacio Montero Alcantara", "out/speakers/M4_S6_Ignacio_edit.mp4", 30, (.52, .43, .70, .55), 2.7)]
    for i, (name, take, t, box, *k) in enumerate(crew):
        x, y = 960 + (i % 3 - 1) * 520, 200 + (i // 3) * 400
        img.paste(face_tile(take, t, box, 260, *k), (x - 130, y))
        d.text((x, y + 290), name, font=R.font(R.SERIF, 34), fill=R.WHITE, anchor="mm")
    f = R.font(R.SANS, 22)
    for i, t in enumerate(["Student project for IE Business School. Not affiliated with L'Oréal or ServiceMarket.",
                           "Fictional characters, simulated data. Layla's voice is AI-generated. AI use disclosed (Claude, Gemini Omni Flash, Lyria, Descript)."]):
        d.text((960, 990 + i * 34), t, font=f, fill=(170, 164, 156), anchor="mm")
    return img

def closing_title(dur=5.0):
    """Item 36: the ask on the golden-hour sky (clip 0c, warmed), the PRO•GO lockup and a QR code to the live prototype."""
    import qrcode
    lay = []
    def layer(draw_fn, name):
        im = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); draw_fn(im, ImageDraw.Draw(im)); return png(im, name)
    lay.append((0.3, layer(lambda im, d: R.spaced(d, (160, 300), "OUR ASK", R.font(R.SANS_M, 28), R.GOLD, 8), "ct0.png")))
    lay.append((0.5, layer(lambda im, d: d.text((152, 340), "90 days in Dubai.", font=R.font(R.SERIF, 120), fill=R.WHITE), "ct1.png")))
    for k, ln in enumerate(["with ServiceMarket and our partner salons", "inside the €3m already planned", "decision at the Q4 2027 review"]):
        lay.append((1.3 + 0.45 * k, layer(lambda im, d, ln=ln, k=k: d.text((160, 530 + k * 66), ln, font=R.font(R.SANS, 44), fill=(244, 238, 228)), f"ct{2 + k}.png")))
    qr = qrcode.QRCode(border=2, box_size=8); qr.add_data("https://ariel-silvio.github.io/pro-go/"); qr.make(fit=True)
    q = qr.make_image(fill_color=(17, 17, 17), back_color=(247, 243, 236)).convert("RGB").resize((230, 230), Image.NEAREST)
    def lock(im, d):
        d.text((160, 850), "PRO•GO", font=R.font(R.SERIF, 64), fill=R.WHITE)
        d.text((164, 930), "12 weeks of colour care, at home", font=R.font(R.SANS, 28), fill=R.GOLD)
        im.paste(q, (1530, 700)); d.text((1645, 960), "Try PRO•GO", font=R.font(R.SANS_M, 28), fill=R.WHITE, anchor="mm")
    lay.append((2.9, layer(lock, "ct_lock.png")))
    shade = R.Image.new("RGBA", (1920, 1080)); sd = ImageDraw.Draw(shade)
    for x in range(0, 1920, 8): sd.rectangle([x, 0, x + 8, 1080], fill=(17, 17, 17, int(170 * max(0.0, 1 - x / 1500))))
    sh = png(shade, "ct_shade.png")
    out = os.path.join(TMP, "closing_title.mp4")
    ins = ["-ss", "1.0", "-t", f"{dur + 0.1}", "-i", L.format("0c"), "-loop", "1", "-t", f"{dur}", "-i", sh]
    fc = [f"[0:v]fps=30,scale=1920:1080,colorbalance=rs=0.08:gs=0.025:bs=-0.08:rm=0.05:bm=-0.05,eq=saturation=1.12:gamma=0.96,"
          f"scale=w='trunc(1920*(1+0.04*t/{dur})/2)*2':h=-2:eval=frame,crop=1920:1080,setsar=1[b0]", "[b0][1:v]overlay=0:0[b1]"]
    last, k = "b1", 2
    for t0, pp in lay:
        ins += ["-loop", "1", "-t", f"{dur}", "-i", pp]
        fc.append(f"[{k}:v]format=rgba,fade=in:st={t0}:d=0.6:alpha=1[l{k}]")
        fc.append(f"[{last}][l{k}]overlay=x=0:y='10*(1-min(1,max(0,(t-{t0})/0.6)))'[b{k}]"); last, k = f"b{k}", k + 1
    fc.append(f"[{last}]fade=in:st=0:d=0.5,fade=out:st={dur - 0.5}:d=0.5,format=yuv420p[v]")
    ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-t", f"{dur}", *ENC, out); return out

# ---------- building blocks ----------
def norm_left(src, kind, dur=None):
    """Return a 960x1080 clip for the left half."""
    out = os.path.join(TMP, f"left_{os.path.basename(src).split('.')[0]}.mp4")
    if kind == "layla":      # 16:9 → centre crop of the left half
        ff("-i", src, "-an", "-vf", "scale=-2:1080,crop=960:1080,fps=30", *ENC, out)
    elif kind == "panel":    # already 960x1080
        ff("-i", src, "-an", "-vf", "fps=30", *ENC, out)
    elif kind == "still":    # full-frame image letterboxed on ivory
        ff("-loop", "1", "-t", str(dur), "-i", src, "-vf",
           "scale=960:-2,pad=960:1080:0:(oh-ih)/2:color=0xF7F3EC,fps=30", *ENC, out)
    return out

def left_track(name, parts):
    lst = os.path.join(TMP, f"{name}.txt")
    open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
    out = os.path.join(TMP, f"{name}_left.mp4")
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out)
    return out

def split(name, left, dur, panel_png, lt_png=None, line_png=None, take=None):
    """take = (speaker clip, crop x): the speaker's recording fills the right half, cropped around the face."""
    out = os.path.join(TMP, f"{name}.mp4")
    if take:
        inputs = ["-stream_loop", "-1", "-i", left, "-i", take[0]]
        right = f"[1:v]fps=30,crop=960:1080:{take[1]}:0,trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[r]"
    else:
        inputs = ["-stream_loop", "-1", "-i", left, "-loop", "1", "-i", panel_png]
        right = f"[1:v]trim=duration={dur},setpts=PTS-STARTPTS,format=yuv420p[r]"
    fc = f"[0:v]trim=duration={dur},setpts=PTS-STARTPTS[l];{right};[l][r]hstack=inputs=2[v0]"
    k, last = 2, "v0"
    for p, (a, b) in ((lt_png, (1, 5)), (line_png, (0.5, 6.5))):
        if p:
            inputs += ["-loop", "1", "-i", p]
            fc += f";[{last}][{k}:v]overlay=0:0:enable='between(t,{a},{b})'[v{k}]"; last = f"v{k}"; k += 1
    ff(*inputs, "-filter_complex", fc, "-map", f"[{last}]", "-t", str(dur), *ENC, out)
    return out

def full(src, name, dur=None, vf="fps=30"):
    out = os.path.join(TMP, f"{name}.mp4")
    args = ["-i", src, "-an", "-vf", vf] + (["-t", str(dur)] if dur else [])
    ff(*args, *ENC, out); return out

def still(img_path, name, dur):
    out = os.path.join(TMP, f"{name}.mp4")
    ff("-loop", "1", "-t", str(dur), "-i", img_path, "-vf", "fps=30,format=yuv420p", *ENC, out); return out

# ---------- script text ----------
script = open("script.md", encoding="utf-8").read()
def first_line(who):
    sec = script.split(f"**{who} ·", 1)[1]
    q = [l[2:].strip() for l in sec.splitlines() if l.startswith("> ") and l.strip() != ">"]
    s = re.sub(r"\*\*\[[^\]]*\]\*\*\s*", "", " ".join(q[:2]))
    words, out = s.split(), []
    for w in words:                      # whole sentences, up to about 30 words
        out.append(w)
        if len(out) >= 22 and w[-1] in ".!?": break
        if len(out) >= 34: out.append("…"); break
    return " ".join(out)

SPK = [("AMJAD SAAD BENSALAMAH", "Amjad Saad Bensalamah", "Chief Innovation Officer", "S1_Amjad"),
       ("ARIEL DE SILVIO", "Ariel De Silvio", "Chief Technology & AI Officer", "S2_Ariel"),
       ("QHAKAZILE MATHEBULA", "Qhakazile Mathebula", "Chief Operations Officer", "S3_Qhakazile"),
       ("REBECCA FERNANDES", "Rebecca Fernandes", "Chief Marketing & Creative Officer", "S4_Rebecca"),
       ("SAJA ALOWAYSHIQ", "Saja AlOwayshiq", "Chief Customer Experience Officer", "S5_Saja"),
       ("IGNACIO MONTERO ALCANTARA", "Ignacio Montero Alcantara", "Chief Financial Officer", "S6_Ignacio")]
LINES = ["Week 0. Her salon sends a free hair scan.", "Wednesday, 18:00. Dana, from my salon.", "Visit 1 of 2. My colourist. My living room.",
         "Week 4. Nothing to report.", "Week 10. Visit 2 of 2.", "Week 12. 74. She renewed."]
# Recorded takes: chapter -> (trimmed clip, crop x of the 960 px window around the face)
TAKES = {1: ("out/speakers/M4_S1_Amjad_edit.mp4", None),
         3: ("out/speakers/M4_S3_Qhakazile_edit.mp4", None),   # Drive original; three cuts, 10% faster, scarf blurred   # IMG_4934 trimmed 1.4-85.2 s, 8% faster (scripts/portrait_edit.py)
         2: ("out/speakers/M4_S2_Ariel_take2_graded.mp4", 552),
         5: ("out/speakers/M4_S5_Saja_edit.mp4", None),   # Drive original; slips cut, 8% faster   # take 2 (script v3): trimmed 10.6-92.0 s, 8% faster, pitch kept
         4: ("out/speakers/M4_S4_Rebecca_edit.mp4", None),      # portrait take, edit by scripts/portrait_edit.py
         6: ("out/speakers/M4_S6_Ignacio_edit.mp4", None)}      # portrait, mirrored back, WhatsApp copy (Drive original to come)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
EDITS = {1: "out/edits/ch1_edit.mp4", 2: "out/edits/ch2_edit.mp4", 3: "out/edits/ch3_edit.mp4", 5: "out/edits/ch5_edit.mp4", 4: "out/edits/ch4_edit.mp4", 6: "out/edits/ch6_edit.mp4"}   # synced edits, picture only
# moments inside the edits (seconds from the chapter start) for the soundtrack: diagram, score, the ask
MOMENTS = {1: {"progo": 18.15, "gap": 41.67, "strike1": 66.2, "strike2": 71.3, "partner": 73.06},
           2: {"behind": 5.9, "criteria": 71.0},
           3: {"visit1": 2.25, "paidpilot": 25.1, "data": 37.8},
           5: {"visit2": 1.0, "leader": 38.75, "real": 67.3},
           4: {"winner1": 13.9, "winner2": 35.6, "climax": 45.2, "weeks": 53.8}, 6: {"score": 1.5, "prove": 8.4, "stopearly": 51.9, "ask": 56.4, "give": 69.56, "already": 71.2, "end6": 72.65}}
voice = []   # (index in seq, clip) for the soundtrack
CARD_DUR = 2.0   # chapter cards trimmed from 3 s to keep the film under 8:00
CARDS = ["chapter_week0", "chapter_week1", "chapter_week2", "chapter_week4", "chapter_week10", "chapter_week12"]

seq, marks = [], {}
# cold open 0:00-0:15: built by scripts/cold_open.py (mirror, leaving, horizon; text on a black third; title on the sky)
seq.append(full("out/edits/cold_open.mp4", "cold_open", 15.0))

lefts = {1: [norm_left(L.format(1), "layla"), norm_left(L.format("1b"), "layla"), norm_left(L.format("1c"), "layla"),
             norm_left("out/p1_scan_result_58.mp4", "panel")],
         2: [norm_left(L.format(2), "layla"), norm_left(L.format("2c"), "layla"), norm_left("out/p3_booking_confirmation.mp4", "panel")],
         3: [norm_left(L.format(3), "layla"), norm_left(L.format("3c"), "layla"), norm_left(L.format("3g"), "layla")],
         4: [norm_left(L.format("4b"), "layla"), norm_left(L.format("4c"), "layla"), norm_left("out/m4/service_diagram.png", "still", 10)],
         5: [norm_left(L.format(4), "layla"), norm_left(L.format("5b"), "layla"), 
             norm_left("out/p4_rescan_66.mp4", "panel")],
         6: [norm_left(L.format(5), "layla"), norm_left(L.format("6b"), "layla"), norm_left(L.format("6c"), "layla")]}
for i, (key, name, role, lt) in enumerate(SPK, start=1):
    marks[f"card{i}"] = len(seq); seq.append(full(M4.format(CARDS[i - 1]), f"card{i}", CARD_DUR))
    panel = png(speaker_panel(i, name, role, first_line(key)), f"spk{i}.png")
    line = png(layla_line(LINES[i - 1]), f"line{i}.png")
    left = left_track(f"ch{i}", lefts[i])
    if i in EDITS and os.path.exists(EDITS[i]):
        voice.append((len(seq), TAKES[i][0])); marks[f"ch{i}"] = len(seq)
        seq.append(full(EDITS[i], f"ch{i}_edit", round(length(TAKES[i][0]), 3)))
    elif i == 4:      # diagram full screen, then split
        seq.append(full(M4.format("service_diagram"), "diagram_full"))
        seq.append(split(f"ch{i}", left, 62, panel, LT.format(lt), line))
    elif i == 6:    # split, score full screen, split, total 77 s after the card
        seq.append(split("ch6a", left, 20, panel, LT.format(lt), line))
        seq.append(full("out/03_score_counter_v2.mp4", "score"))
        seq.append(split("ch6b", left, 51, panel))
    elif i in TAKES:
        voice.append((len(seq), TAKES[i][0]))
        seq.append(split(f"ch{i}", left, round(length(TAKES[i][0]), 3), panel, LT.format(lt), line, TAKES[i]))
    else:
        seq.append(split(f"ch{i}", left, 66 if i == 3 else 72, panel, LT.format(lt), line))   # ch3 placeholder: aim 65-66 s
# bookend: back to the mirror from the cold open, Layla's voice "Week twelve. Now I know." (AI voice, see ai-log)
marks["closing"] = len(seq)
seq.append(full(L.format("0a"), "mirror_end", None, "trim=start=1.6:end=4.45,setpts=1.3*(PTS-STARTPTS),fps=30,scale=1920:1080,fade=t=in:st=0:d=0.5"))
voice.append((len(seq) - 1, "out/voice/layla_close2_1.wav", 0.3))   # "Week twelve. Now I can see it." (voice A, take 2)
marks["title"] = len(seq); seq.append(closing_title(5.0))
seq.append(still(png(credits_faces(), "credits.png"), "credits", 3))
voice.append((0, "out/voice/layla_open.wav", 3.0))      # cold open: Layla's own line over the mirror

lst = os.path.join(TMP, "all.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in seq))
final = os.path.join(OUT, "animatic_v16_voice.mp4"); part = final.replace(".mp4", ".part.mp4")
starts, t = [], 0.0
for p in seq: starts.append(t); t += length(p)
ins = ["-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={t:.3f}"]
fc, mix = [], ["[1:a]"]
for k, v in enumerate(voice):
    idx, clip, off = v if len(v) == 3 else (*v, 0.0)
    ins += ["-i", clip]; ms = int((starts[idx] + off) * 1000)
    fc.append(f"[{k+2}:a]aresample=48000,adelay={ms}|{ms}[a{k}]"); mix.append(f"[a{k}]")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first[aout]")
ff(*ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", part)
print("chapter starts:", [round(x, 1) for x in starts])
import json
tl = {k: round(starts[v], 3) for k, v in marks.items()}; tl["end"] = round(t, 3)
for i in range(1, 7): tl[f"ch{i}"] = round(starts[marks[f"card{i}"] + 1], 3)
for i, m in MOMENTS.items():
    if i in EDITS and os.path.exists(EDITS[i]): tl.update({k: round(tl[f"ch{i}"] + v, 3) for k, v in m.items()})
if "score" not in tl: tl["score"] = tl["ch6"] + 20
if "ask" not in tl: tl["ask"] = tl["closing"] - 11
json.dump(tl, open(os.path.join(OUT, "timeline.json"), "w"), indent=1); print(tl)
os.replace(part, final); print("wrote", final)
