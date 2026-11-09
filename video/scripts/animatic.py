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
    R.spaced(d, (560, 170), "ANIMATIC V12", R.font(R.SANS_M, 18), (150, 144, 136), 4)
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
                           "Fictional characters, simulated data. AI use disclosed (Claude, Gemini Omni Flash, Descript)."]):
        d.text((960, 760 + i * 40), t, font=f, fill=(170, 164, 156), anchor="mm")
    return img

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
TAKES = {1: ("out/speakers/M4_S1_Amjad_edit.mp4", None),   # IMG_4934 trimmed 1.4-85.2 s, 8% faster (scripts/portrait_edit.py)
         2: ("out/speakers/M4_S2_Ariel_take2_graded.mp4", 552),   # take 2 (script v3): trimmed 10.6-92.0 s, 8% faster, pitch kept
         4: ("out/speakers/M4_S4_Rebecca_edit.mp4", None),      # portrait take, edit by scripts/portrait_edit.py
         6: ("out/speakers/M4_S6_Ignacio_edit.mp4", None)}      # portrait, mirrored back, WhatsApp copy (Drive original to come)
def length(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
EDITS = {1: "out/edits/ch1_edit.mp4", 2: "out/edits/ch2_edit.mp4", 4: "out/edits/ch4_edit.mp4", 6: "out/edits/ch6_edit.mp4"}   # synced edits, picture only
# moments inside the edits (seconds from the chapter start) for the soundtrack: diagram, score, the ask
MOMENTS = {1: {"progo": 18.15, "gap": 41.67, "strike1": 66.2, "strike2": 71.3, "partner": 73.06},
           2: {"behind": 5.9, "criteria": 71.0},
           4: {"winner1": 13.9, "winner2": 35.6, "climax": 45.2, "weeks": 53.8}, 6: {"score": 1.5, "ask": 56.4}}
voice = []   # (index in seq, clip) for the soundtrack
CARD_DUR = 2.5   # chapter cards trimmed from 3 s to keep the film under 8:00
CARDS = ["chapter_week0", "chapter_week1", "chapter_week2", "chapter_week4", "chapter_week10", "chapter_week12"]

seq, marks = [], {}
# cold open 0:00-0:15: built by scripts/cold_open.py (mirror, leaving, horizon; text on a black third; title on the sky)
seq.append(full("out/edits/cold_open_picture.mp4", "cold_open", 15.0))

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
marks["closing"] = len(seq); seq.append(full(M4.format("closing_card"), "closing"))
seq.append(still(png(credits(), "credits.png"), "credits", 4))

lst = os.path.join(TMP, "all.txt"); open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in seq))
final = os.path.join(OUT, "animatic_v12_voice.mp4"); part = final.replace(".mp4", ".part.mp4")
starts, t = [], 0.0
for p in seq: starts.append(t); t += length(p)
ins = ["-f", "concat", "-safe", "0", "-i", lst, "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={t:.3f}"]
fc, mix = [], ["[1:a]"]
for k, (idx, clip) in enumerate(voice):
    ins += ["-i", clip]; ms = int(starts[idx] * 1000)
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
