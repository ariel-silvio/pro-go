"""Measure and match the six speaker takes to one colour standard (face tone and brightness, black level, white balance).
Writes edits/colour_grades.json ({speaker: ffmpeg filter}) and a before/after sheet. Run from video/."""
import json, subprocess, sys, cv2, numpy as np
D = "/tmp/claude-0/-home-user-pro-go/7cbc29c2-b15c-587b-a097-c29f10db4125/scratchpad"
SRC = {  # speaker: (file, sample times, hflip)
 "Amjad": (f"{D}/drive_in3/amjad_raw.mp4", (12, 35, 60), False),
 "Ariel": ("out/speakers/M4_S2_Ariel_take2_edit.mp4", (8, 30, 55), False),
 "Qhakazile": (f"{D}/drive_in4/q_raw.mp4", (10, 40, 70), False),
 "Rebecca": (f"{D}/drive_in/rebecca_raw.mp4", (10, 35, 60), False),
 "Saja": (f"{D}/drive_in3/saja_raw.mp4", (10, 40, 70), False),
 "Ignacio": (f"{D}/drive_in3/ignacio2_raw.mp4", (10, 35, 60), True),
}
# face boxes as fractions of the frame (x0, y0, x1, y1), checked on a contact sheet: cv2 5 has no face detector
BOX = {"Amjad": (.44, .30, .56, .55), "Ariel": (.49, .30, .63, .60), "Qhakazile": (.49, .22, .62, .45),
       "Rebecca": (.33, .34, .46, .43), "Saja": (.63, .20, .76, .42), "Ignacio": (.52, .43, .70, .55)}
CUR = {"name": None}
def frame(f, t, vf=""):
    w = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", (vf + "," if vf else "") + "scale=960:-2", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(w, np.uint8), cv2.IMREAD_COLOR)
def measure(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY); H, W = g.shape; b = BOX[CUR["name"]]
    x, y, w, h = int(b[0] * W), int(b[1] * H), int((b[2] - b[0]) * W), int((b[3] - b[1]) * H)
    skin = img[y + h // 4: y + 3 * h // 4, x + w // 4: x + 3 * w // 4]               # cheeks, nose, forehead centre
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(float); L, A, B = lab[..., 0] * 100 / 255, lab[..., 1] - 128, lab[..., 2] - 128
    sl = cv2.cvtColor(skin, cv2.COLOR_BGR2LAB).astype(float)
    m = np.ones(g.shape, bool); m[max(0, y - h // 2): y + 2 * h, max(0, x - w): x + 2 * w] = False   # away from the person
    chroma = np.hypot(A, B); neutral = m & (chroma < 12) & (L > 35) & (L < 95)
    return dict(face_L=float(np.median(sl[..., 0]) * 100 / 255), face_a=float(np.median(sl[..., 1]) - 128), face_b=float(np.median(sl[..., 2]) - 128),
                black=float(np.percentile(L, 1)), wall_a=float(np.median(A[neutral])) if neutral.sum() > 500 else 0.0,
                wall_b=float(np.median(B[neutral])) if neutral.sum() > 500 else 0.0)
def avg(f, ts, vf):
    ms = [measure(frame(f, t, vf)) for t in ts]; ms = [m for m in ms if m]
    return {k: float(np.mean([m[k] for m in ms])) for k in ms[0]} if ms else None
# Match the camera, not the person: equal white balance, black level, contrast and skin HUE across takes;
# each person keeps their own natural skin lightness (only clear under-exposure is lifted, gently).
TARGET = dict(black=3.0, hue=55.0, chroma=28.0, wall_b=4.0)
def grade_for(m):
    hue = np.degrees(np.arctan2(m["face_b"], m["face_a"])); chroma = np.hypot(m["face_a"], m["face_b"])
    dh = TARGET["hue"] - hue                                      # >0: face too red -> warm-yellow shift; <0: too yellow
    rs = -m["wall_a"] * 0.004 - (m["wall_b"] - TARGET["wall_b"]) * 0.003 - dh * 0.0035
    bs = (m["wall_b"] - TARGET["wall_b"]) * 0.005 + dh * 0.0018
    gs = m["wall_a"] * 0.003
    lift = 1.0 + (0.16 if m["face_L"] < 35 else 0.0)              # only clear under-exposure (dark face against a bright window)
    bp = float(np.clip((m["black"] - TARGET["black"]) / 100 * 1.1, 0.0, 0.09))   # black point: pull lifted blacks back down
    contrast = 1.02
    sat = float(np.clip(TARGET["chroma"] / max(chroma, 1), 0.86, 1.22))
    return (f"colorlevels=rimin={bp:.3f}:gimin={bp:.3f}:bimin={bp:.3f},"
            f"colorbalance=rs={rs:.3f}:gs={gs:.3f}:bs={-bs:.3f}:rm={rs / 2:.3f}:bm={-bs / 2:.3f},"
            f"eq=gamma={lift:.3f}:contrast={contrast:.3f}:saturation={sat:.3f}")
if "--boxes" in sys.argv:   # check sheet of the face boxes
    tiles = []
    for name, (f, ts, flip) in SRC.items():
        img = frame(f, ts[1], "hflip" if flip else ""); H, W = img.shape[:2]; b = BOX[name]
        cv2.rectangle(img, (int(b[0] * W), int(b[1] * H)), (int(b[2] * W), int(b[3] * H)), (0, 0, 255), 3)
        tiles.append(cv2.resize(img, (int(300 * W / H), 300)))
    cv2.imwrite(D + "/boxes.jpg", np.hstack(tiles)); sys.exit()
OVERRIDE = {   # hand-tuned after looking at the sheet
 "Ariel": "colorbalance=rs=-0.015:bs=0.015:rm=-0.01,eq=gamma=1.04:contrast=1.02:saturation=0.92",
 "Saja": "colorlevels=rimin=0.015:gimin=0.015:bimin=0.015,colorchannelmixer=rr=1.045:gg=0.975:bb=0.985,eq=gamma=0.98:contrast=1.06:saturation=1.08",
}
res, grades = {}, {}
for name, (f, ts, flip) in SRC.items():
    CUR["name"] = name; base = "hflip" if flip else ""
    m0 = avg(f, ts, base); g = OVERRIDE.get(name) or grade_for(m0)
    m1 = avg(f, ts, (base + "," if base else "") + g)
    res[name] = (m0, m1); grades[name] = g
    hue = lambda m: np.degrees(np.arctan2(m["face_b"], m["face_a"]))
    print(f"{name:10s} hue {hue(m0):4.0f}->{hue(m1):4.0f}  chroma {np.hypot(m0['face_a'],m0['face_b']):4.0f}->{np.hypot(m1['face_a'],m1['face_b']):4.0f} | before L{m0['face_L']:5.1f} a{m0['face_a']:5.1f} b{m0['face_b']:5.1f} black{m0['black']:5.1f} wall({m0['wall_a']:4.1f},{m0['wall_b']:4.1f})"
          f"  ->  after L{m1['face_L']:5.1f} a{m1['face_a']:5.1f} b{m1['face_b']:5.1f} black{m1['black']:5.1f}")
json.dump(grades, open("edits/colour_grades.json", "w"), indent=1)
rows = []
for name, (f, ts, flip) in SRC.items():
    base = "hflip" if flip else ""
    a = frame(f, ts[1], base); b = frame(f, ts[1], (base + "," if base else "") + grades[name])
    def crop(img):
        H, W = img.shape[:2]; bb = BOX[name]; x, y, w, h = int(bb[0] * W), int(bb[1] * H), int((bb[2] - bb[0]) * W), int((bb[3] - bb[1]) * H)
        cx, cy = x + w // 2, y + h // 2; s = int(h * 1.6)
        x0, y0 = max(0, cx - s // 2), max(0, cy - s // 2); c = img[y0:y0 + s, x0:x0 + s]
        return cv2.resize(c, (300, 300))
    ca, cb = crop(a), crop(b)
    for im, t in ((ca, name + " before"), (cb, "after")): cv2.putText(im, t, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    rows.append((ca, cb))
top = np.hstack([r[0] for r in rows]); bot = np.hstack([r[1] for r in rows])
cv2.imwrite("review/colour_before_after.jpg", np.vstack([top, bot]), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("sheet written")
