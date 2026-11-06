"""Cold open v2 (0:00-0:15): morning mirror -> leaving -> horizon, text on a black left third, then the title on the sky.
Usage (from video/): python3 scripts/cold_open.py [music.mp3]  ->  out/edits/cold_open.mp4 (15.0 s; with music if given)
Clip 0a is used 1.6-4.45 s only: before 1.6 s her face shows in the mirror reflection, and from 4.5 s her profile shows."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image, ImageDraw
import render as R

OUT = "out/edits"; TMP = os.path.join(OUT, "cold_parts"); os.makedirs(TMP, exist_ok=True)
ENC = ["-c:v", "libx264", "-crf", "20", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]
def ff(*a): subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)
L = "out/layla/layla_{}.mp4"
DUR, XF, PANEL, SHIFT = 15.0, 0.5, 640, 320
MOVE_AT, MOVE = 11.0, 0.7                     # panel slides out, horizon goes full screen
LINES = [(0.4, 2.6, "Layla. 34. Dubai."), (3.0, 6.9, "Every eight weeks, she colours her hair."),
         (7.4, 10.7, "No one has ever measured what it does to it.")]

# 1) picture: three clips with dissolves (15.0 s)
clips = [(L.format("0a"), 1.6, 4.45), (L.format("0b"), 3.9, 8.55), (L.format("0c"), 1.5, 10.0)]   # 0a from 1.6 s: before that her face shows in the mirror
parts = []
for k, (src, a, b) in enumerate(clips):
    p = os.path.join(TMP, f"c{k}.mp4"); ff("-ss", str(a), "-t", f"{b - a:.3f}", "-i", src, "-an", "-vf", "fps=30,scale=1920:1080", *ENC, p); parts.append(p)
d0, d1 = clips[0][2] - clips[0][1], clips[1][2] - clips[1][1]
base = os.path.join(TMP, "base.mp4")
ff("-i", parts[0], "-i", parts[1], "-i", parts[2], "-filter_complex",
   f"[0:v][1:v]xfade=transition=fade:duration={XF}:offset={d0 - XF:.3f}[x1];"
   f"[x1][2:v]xfade=transition=fade:duration={XF}:offset={d0 + d1 - 2 * XF:.3f}[v]", "-map", "[v]", "-t", str(DUR), *ENC, base)

# 2) overlays: one text line per PNG (white Bodoni on the black third), title on the sky
def line_png(text, n):
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img); f = R.font(R.SERIF, 52)
    rows = R.wrap(d, text, f, PANEL - 160 - 60); y = 540 - len(rows) * 70 // 2
    for i, r in enumerate(rows): d.text((160, y + i * 70), r, font=f, fill=R.WHITE)
    d.rectangle([160, y - 40, 200, y - 38], fill=R.GOLD)
    p = os.path.join(TMP, f"line{n}.png"); img.save(p); return p
def title_png():
    img = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 1920, 1080], fill=R.IVORY + (110,))                 # flat ivory veil for contrast on the sky
    R.spaced(d, (960, 380), "L'ORÉAL GROUPE  ·  TEAM D", R.font(R.SANS_M, 26), R.GOLD_TXT, 7, True)
    d.text((960, 480), "12 weeks with Layla", font=R.font(R.SERIF, 112), fill=R.INK, anchor="mm")
    d.rectangle([850, 575, 1070, 577], fill=R.GOLD)
    d.text((960, 640), "PRO•GO  ·  A proposal to the CEO", font=R.font(R.SANS, 38), fill=R.INK, anchor="mm")
    p = os.path.join(TMP, "title.png"); img.save(p); return p

P = f"(st(0,clip((t-{MOVE_AT})/{MOVE},0,1));ld(0)*ld(0)*(3-2*ld(0)))"   # smoothstep 0..1 during the move
ins = ["-i", base, "-f", "lavfi", "-i", f"color=c=0x111111:s={PANEL}x1080:r=30:d={DUR}"]
fc = [f"color=c=0x111111:s=1920x1080:r=30:d={DUR}[bg]",
      f"[bg][0:v]overlay=x='{SHIFT}*(1-{P})':y=0:eval=frame[m0]",
      f"[m0][1:v]overlay=x='-{PANEL}*{P}':y=0:eval=frame[m1]"]
last, k = "m1", 2
for n, (a, b, text) in enumerate(LINES):
    ins += ["-loop", "1", "-t", str(DUR), "-i", line_png(text, n)]
    fc.append(f"[{k}:v]format=rgba,fade=in:st={a}:d=0.45:alpha=1,fade=out:st={b - 0.45}:d=0.45:alpha=1[l{n}]")
    fc.append(f"[{last}][l{n}]overlay=0:0[m{k}]"); last, k = f"m{k}", k + 1
ins += ["-loop", "1", "-t", str(DUR), "-i", title_png()]
fc.append(f"[{k}:v]format=rgba,fade=in:st={MOVE_AT + MOVE + 0.1}:d=0.9:alpha=1[tt]")
fc.append(f"[{last}][tt]overlay=0:0,format=yuv420p[v]")
pic = os.path.join(OUT, "cold_open_picture.mp4")
ff(*ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-t", str(DUR), *ENC, pic)

# 3) optional music bed for the preview (the animatic mixes its own soundtrack)
final = os.path.join(OUT, "cold_open.mp4")
if len(sys.argv) > 1:
    ff("-i", pic, "-i", sys.argv[1], "-filter_complex",
       f"[1:a]aresample=48000,loudnorm=I=-20:TP=-2,adelay=300|300,afade=t=out:st={DUR - 1.2}:d=1.2[a]",
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-movflags", "+faststart", final)
else:
    os.replace(pic, final)
print("wrote", final)
