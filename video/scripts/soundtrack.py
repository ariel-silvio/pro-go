"""Score + sound effects for the 8:00 cut, mixed under the voices already in the animatic.
Usage (from video/): python3 scripts/soundtrack.py out/animatic/animatic_v6.mp4 out/animatic/animatic_v7.mp4
Music: Lyria pieces in out/music (briefs in music/*_brief.txt). SFX: out/sfx (scripts/sfx.py).
Music sits about 17 dB under speech (voice -16 LUFS, music about -33 LUFS after the duck) and comes up on cards, the diagram and the score."""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import render as R

SR, DUR = 48000, 480.0
SRC, DST = sys.argv[1], sys.argv[2]

def load(path, target_lufs=None):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
    if target_lufs is not None:
        log = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        i = float([l for l in log.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        a *= 10 ** ((target_lufs - i) / 20)
    return a

def fade(a, fin, fout):
    n = len(a); e = np.ones(n, np.float32)
    if fin:  k = min(n, int(fin * SR));  e[:k] = np.linspace(0, 1, k) ** 2
    if fout: k = min(n, int(fout * SR)); e[n - k:] *= np.linspace(1, 0, k) ** 2
    return a * e[:, None]

bus = np.zeros((int(DUR * SR), 2), np.float32)
def place(buf, a, at, src_from=0.0, length=None, fin=0.0, fout=0.0, gain_db=0.0):
    a = a[int(src_from * SR):]
    if length: a = a[:int(length * SR)]
    a = fade(a, fin, fout) * 10 ** (gain_db / 20)
    s = int(at * SR); e = min(len(buf), s + len(a)); buf[s:e] += a[:e - s]

# ---- score (each piece normalised to -20 LUFS before the envelope) ----
M = lambda n: load(f"out/music/{n}.mp3", -20)
music = np.zeros_like(bus)
place(music, M("open_dram2"), 0.0,  length=17.5, fout=2.5, gain_db=2)     # cold open, dramatic, drops as chapter 1 starts
place(music, M("bed1"),       15.0, length=152.5, fin=2.0, fout=3.0)      # weeks 0-1: sparse warm piano
place(music, M("bed2"),       164.5, length=168.0, fin=3.0, fout=4.0)     # week 2: strings join; pulse from about week 4
place(music, M("bed1"),       318.0, src_from=60.0, length=15.0, fin=2.5, fout=3.0)   # bridge: bed2 ends at 322 s
place(music, M("build"),      330.5, length=110.0, fin=3.0, fout=6.0)     # weeks 10-12: strings rise, swell lands on the score (about 413-419 s)
place(music, M("bed1"),       436.0, src_from=20.0, length=26.0, fin=4.0, fout=5.0, gain_db=-3)   # low pad under the rules
place(music, M("close"),      469.6, length=10.4, fin=0.4, fout=3.0)      # motif returns on the closing card, silence just before

# gain envelope: duck under speech, up on cards / diagram / score / closing
SPEECH = [(18, 90), (93, 165), (168, 240), (253, 315), (318, 390), (393, 413), (419, 470)]
t = np.arange(len(music)) / SR; g = np.zeros(len(music), np.float32)
for a, b in SPEECH:                    # -15 dB with 0.6 s ramps
    g = np.minimum(g, -15 * np.clip(np.minimum((t - a) / 0.6, (b - t) / 0.6), 0, 1))
music *= (10 ** (g / 20))[:, None]
music[int(458 * SR):int(469.6 * SR)] *= np.linspace(1, 0, int(11.6 * SR))[:, None] ** 3   # the ask: let it go quiet
bus += music

# ---- sound effects ----
S = {n: load(f"out/sfx/{n}.wav") for n in ["week_tick", "scan_shimmer", "message_chime", "soft_click", "count_tick"]}
for at in (15, 90, 165, 240, 315, 390): place(bus, S["week_tick"], at + 0.25, gain_db=-8)      # chapter cards
place(bus, S["scan_shimmer"], 37.6, gain_db=-14)          # chapter 1: scan result on the phone
place(bus, S["message_chime"], 96.8, gain_db=-14)         # chapter 2: Dana's message
for i in range(5): place(bus, S["soft_click"], 243.4 + 0.8 * i, gain_db=-12)   # diagram boxes
place(bus, S["scan_shimmer"], 393.3, gain_db=-14)         # week 12 re-scan
prev = None                                               # count ticks: one per number change, same curve as render.score
for f in range(180):
    wk = 12 * R.ease((f / 30 - 0.6) / 3.6); s = R.PTS[0][1]
    for (x0, y0), (x1, y1) in zip(R.PTS, R.PTS[1:]):
        if x0 <= wk <= x1: s = y0 + (y1 - y0) * (wk - x0) / (x1 - x0)
    s = 74 if wk >= 12 else round(s)
    if prev is not None and s != prev: place(bus, S["count_tick"], 413 + f / 30, gain_db=-16)
    prev = s

wav = DST.replace(".mp4", "_music.wav")
np.clip(bus, -1, 1).astype("<f4").tofile(wav + ".raw")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav + ".raw", wav], check=True); os.remove(wav + ".raw")
# voices (from the animatic) + music bus, gentle limiter
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-i", wav, "-filter_complex",
                "[0:a]aresample=48000[v];[v][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", DST], check=True)
print("wrote", DST, "and", wav)
