"""Six lower thirds as transparent 1920x1080 overlays (speaker sits in the right half).
Usage (from video/): python3 scripts/lower_thirds.py <outdir> [--mov NAME_KEY]
Writes LT_<key>.png (RGBA). With --mov, also a 4 s ProRes 4444 .mov with fades for one speaker."""
import os, sys, subprocess; sys.path.insert(0, '.')
from PIL import Image, ImageDraw
from render import W, H, IVORY, GOLD, GOLD_TXT, INK, font, SANS_M, clamp, ease

TEAM = [  # chapter order
    ("S1_Amjad", "Amjad Saad Bensalamah", "CHIEF INNOVATION OFFICER"),
    ("S2_Ariel", "Ariel De Silvio", "CHIEF TECHNOLOGY & AI OFFICER"),
    ("S3_Qhakazile", "Qhakazile Mathebula", "CHIEF OPERATIONS OFFICER"),
    ("S4_Rebecca", "Rebecca Fernandes", "CHIEF MARKETING & CREATIVE OFFICER"),
    ("S5_Saja", "Saja AlOwayshiq", "CHIEF CUSTOMER EXPERIENCE OFFICER"),
    ("S6_Ignacio", "Ignacio Montero Alcantara", "CHIEF FINANCIAL OFFICER"),
]
X, Y, BH, PAD, TRACK = 1040, 830, 104, 32, 4
FN, FR = font(SANS_M, 36), font(SANS_M, 19)

def caps_width(d, text): return sum(d.textlength(c, font=FR) for c in text) + TRACK * (len(text) - 1)

def frame(name, role, a=1.0, slide=0.0):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    w = max(d.textlength(name, font=FN), caps_width(d, role)) + 2 * PAD
    assert X + w <= W - 160, f"{name}: lower third too wide ({X + w:.0f} px)"
    al = int(255 * a); x = X - 24 * (1 - slide)
    d.rectangle([x, Y, x + w, Y + BH], fill=IVORY + (al,))
    d.rectangle([x, Y, x + 1, Y + BH], fill=GOLD + (al,))          # 2 px gold rule
    d.text((x + PAD, Y + 18), name, font=FN, fill=INK + (al,))
    cx = x + PAD
    for c in role:
        d.text((cx, Y + 68), c, font=FR, fill=GOLD_TXT + (al,)); cx += d.textlength(c, font=FR) + TRACK
    return img

def mov(out, key, name, role, dur=4.0, fps=30):
    tmp = os.path.join(out, f"LT_{key}.part.mov")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}",
        "-r", str(fps), "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", tmp], stdin=subprocess.PIPE)
    for i in range(int(dur * fps)):
        t = i / fps; a = ease(t / 0.4) * (1 - clamp((t - (dur - 0.4)) / 0.4))
        p.stdin.write(frame(name, role, a, ease(t / 0.5)).tobytes())
    p.stdin.close()
    if p.wait() == 0: os.replace(tmp, os.path.join(out, f"LT_{key}.mov"))
    else: raise SystemExit("ffmpeg failed")

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for key, n, r in TEAM:
        frame(n, r).save(os.path.join(out, f"LT_{key}.png")); print("png", key)
    if "--mov" in sys.argv:
        k = sys.argv[sys.argv.index("--mov") + 1]
        key, n, r = next(t for t in TEAM if t[0] == k); mov(out, key, n, r); print("mov", key)
