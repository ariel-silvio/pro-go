"""Track a phone screen through a clip (homography from feature points on the phone and hands) and write corner tracks.
Usage (from video/): python3 scripts/screen_track.py CLIP.mp4 "x1,y1 x2,y2 x3,y3 x4,y4" OUT.json [qc_dir]
Corners: the screen's top-left, top-right, bottom-right, bottom-left in the first frame."""
import json, sys, cv2, numpy as np
clip, cs, out = sys.argv[1], sys.argv[2], sys.argv[3]; qc = sys.argv[4] if len(sys.argv) > 4 else None
C0 = np.float32([[float(v) for v in p.split(",")] for p in cs.split()])
cap = cv2.VideoCapture(clip); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
g0 = cv2.cvtColor(frames[0], cv2.COLOR_BGR2GRAY)
# features: a band around the screen (bezel, phone body, fingers), not the screen itself (its light sweep moves)
outer = np.zeros_like(g0); inner = np.zeros_like(g0)
ctr = C0.mean(0)
cv2.fillConvexPoly(outer, np.int32(ctr + (C0 - ctr) * 1.45), 255)
cv2.fillConvexPoly(inner, np.int32(ctr + (C0 - ctr) * 0.94), 255)
band = cv2.subtract(outer, inner)
p0 = cv2.goodFeaturesToTrack(g0, 600, 0.005, 6, mask=band)
pts, ref, prev, corners = p0.copy(), p0.copy(), g0, [C0.tolist()]
for k in range(1, len(frames)):
    g = cv2.cvtColor(frames[k], cv2.COLOR_BGR2GRAY)
    nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev, g, pts, None, winSize=(31, 31), maxLevel=4)
    back, st2, _ = cv2.calcOpticalFlowPyrLK(g, prev, nxt, None, winSize=(31, 31), maxLevel=4)
    good = (st.ravel() == 1) & (st2.ravel() == 1) & (np.linalg.norm((back - pts).reshape(-1, 2), axis=1) < 1.0)
    pts, ref = nxt[good], ref[good]
    H, inl = cv2.findHomography(ref, pts, cv2.RANSAC, 2.0)
    corners.append(cv2.perspectiveTransform(C0[None], H)[0].tolist()); prev = g
c = np.array(corners)                                   # light smoothing (centred 5-frame mean) against jitter
sm = c.copy()
for k in range(len(c)): sm[k] = c[max(0, k - 2):k + 3].mean(0)
json.dump(sm.tolist(), open(out, "w")); print("tracked", len(sm), "frames, points left:", len(pts))
if qc:
    for k in range(0, len(frames), 15):
        v = frames[k].copy(); cv2.polylines(v, [np.int32(sm[k])], True, (0, 0, 255), 2)
        cv2.imwrite(f"{qc}/qc_{k:03d}.jpg", cv2.resize(v, (960, 540)))
