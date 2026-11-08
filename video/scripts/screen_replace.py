"""Put an app screen into a phone in a clip, following tracked corners (scripts/screen_track.py).
Fingers near the screen edges stay in front (colour matte); the original screen's soft shading is kept.
Usage (from video/): python3 scripts/screen_replace.py CLIP.mp4 CORNERS.json SCREEN.png OUT.mp4"""
import json, subprocess, sys, cv2, numpy as np
clip, cj, scr, out = sys.argv[1:5]
C = np.float32(json.load(open(cj))); app = cv2.imread(scr); h, w = app.shape[:2]
src = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
# rounded-corner screen mask in app space
rm = np.zeros((h, w), np.uint8); r = int(w * 0.11)
cv2.rectangle(rm, (r, 0), (w - r, h), 255, -1); cv2.rectangle(rm, (0, r), (w, h - r), 255, -1)
for x, y in ((r, r), (w - r, r), (r, h - r), (w - r, h - r)): cv2.circle(rm, (x, y), r, 255, -1)
# the phone's notch, drawn into the app image (top centre)
nw, nh = int(w * 0.36), int(h * 0.036)
cv2.rectangle(app, ((w - nw) // 2, 0), ((w + nw) // 2, nh), (17, 17, 17), -1)
cv2.circle(app, ((w - nw) // 2, nh // 2), nh // 2, (17, 17, 17), -1); cv2.circle(app, ((w + nw) // 2, nh // 2), nh // 2, (17, 17, 17), -1)
low = np.zeros((h, w), np.uint8); low[int(h * 0.35):] = 255            # fingers only come over the lower part
cap = cv2.VideoCapture(clip); W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                      "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
k = 0
while True:
    ok, f = cap.read()
    if not ok: break
    q = C[min(k, len(C) - 1)]; M = cv2.getPerspectiveTransform(src, q)
    a = cv2.warpPerspective(app, M, (W, H), flags=cv2.INTER_AREA).astype(np.float32)
    m = cv2.warpPerspective(rm, M, (W, H)).astype(np.float32) / 255
    # shading: heavily blurred luminance of the original screen, normalised
    lum = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32)
    inside = m > 0.5; med = np.median(lum[inside]) if inside.any() else 1
    sh = np.clip(cv2.GaussianBlur(lum, (0, 0), 25) / med, 0.86, 1.04)
    a *= sh[..., None]
    # occluders (fingers): saturated and darker than the screen; only trusted near the edges
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV).astype(np.float32)
    occ = ((hsv[..., 1] > 40) & (hsv[..., 2] < 0.95 * med)).astype(np.float32)
    inner = cv2.erode((m > 0.5).astype(np.uint8), np.ones((41, 41), np.uint8)).astype(np.float32)
    occ *= (1 - inner) * (cv2.warpPerspective(low, M, (W, H)) > 0); occ = cv2.GaussianBlur(cv2.dilate(occ, np.ones((3, 3), np.uint8)), (0, 0), 1.5)
    alpha = cv2.GaussianBlur(m, (0, 0), 0.8) * (1 - occ)
    o = f.astype(np.float32) * (1 - alpha[..., None]) + a * alpha[..., None]
    p.stdin.write(np.clip(o, 0, 255).astype(np.uint8).tobytes()); k += 1
p.stdin.close(); p.wait(); print("wrote", out, k, "frames")
