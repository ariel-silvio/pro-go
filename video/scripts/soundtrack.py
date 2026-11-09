"""Score + sound effects for the 8:00 cut, mixed under the voices already in the animatic.
Usage (from video/): python3 scripts/soundtrack.py out/animatic/animatic_v8_voice.mp4 out/animatic/animatic_v8.mp4 [timeline.json]
All cue times come from the timeline that animatic.py writes, so chapters can change length.
Music: Lyria pieces in out/music (briefs in music/*_brief.txt). SFX: out/sfx (scripts/sfx.py).
Music sits about 17 dB under speech (voice -16 LUFS, music about -33 LUFS after the duck) and comes up on cards, the diagram and the score."""
import os, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import render as R

import json
SRC, DST = sys.argv[1], sys.argv[2]
TL = json.load(open(sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(SRC), "timeline.json")))   # written by animatic.py
SR, DUR = 48000, TL["end"]

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
c = [None] + [TL[f"card{i}"] for i in range(1, 7)]; ch = [None] + [TL[f"ch{i}"] for i in range(1, 7)]
SCORE, ASK, CLOSE = TL["score"], TL["ask"], TL["closing"]
build_at = SCORE - 82.5                                                   # the build's swell peaks about 82 s in
place(music, M("open_dram2"), 0.0,  length=17.5, fout=2.5, gain_db=2)     # cold open, dramatic, drops as chapter 1 starts
place(music, M("bed1"),       c[1], length=c[3] - c[1] + 2.5, fin=2.0, fout=3.0)          # weeks 0-1: sparse warm piano
bed2_len = min(157.0, build_at + 4 - (c[3] - 0.5))
place(music, M("bed2"),       c[3] - 0.5, length=bed2_len, fin=3.0, fout=4.0)            # week 2: strings join; pulse from about week 4
if build_at > c[3] - 0.5 + 157.0 - 4:                                                     # bridge if bed2 runs out first
    place(music, M("bed1"), c[3] + 152.0, src_from=60.0, length=build_at - c[3] - 148.0, fin=2.5, fout=3.0)
place(music, M("build"),      build_at, length=SCORE + 10 - build_at, fin=3.0, fout=5.0)   # weeks 10-12: strings rise, swell on the score
place(music, M("bed1"),       SCORE + 6.0, src_from=20.0, length=ASK - SCORE - 6.0, fin=4.0, fout=4.0, gain_db=-3)   # low pad under the rules
place(music, M("close"),      CLOSE - 0.3, length=DUR - CLOSE + 0.3, fin=0.4, fout=3.0)   # motif returns on the closing card

# gain envelope: duck under speech (chapter bodies), up on cards and the closing; half duck on the score
SPEECH = [(ch[i], c[i + 1] if i < 6 else CLOSE) for i in range(1, 7)]
t = np.arange(len(music)) / SR; g = np.zeros(len(music), np.float32)
for a, b in SPEECH:                    # -15 dB with 0.6 s ramps
    g = np.minimum(g, -15 * np.clip(np.minimum((t - a) / 0.6, (b - t) / 0.6), 0, 1))
# (no lift on the score any more: Ignacio speaks over it, the music stays under him)
g = g + np.interp(t, [SCORE - 1.5, SCORE - 0.5, SCORE + 7.0, SCORE + 8.5], [0, -4, -4, 0])   # the build swells here: keep it under his voice
if "partner" in TL:   # chapter 1: the bed lifts 6 dB on "So we partner", then settles
    P = TL["partner"]; g = g + np.interp(t, [P - 0.3, P + 0.5, P + 3.5, P + 6.0], [0, 6, 6, 0])
CL = TL.get("climax")
if CL:   # chapter 4 climax, "And L'Oréal learns": the bed falls away in her pause, the climax cue takes over, then the bed returns
    dip = np.interp(t, [CL - 2.4, CL - 0.4, CL + 17.5, CL + 20.0], [0, -30, -30, 0])
    g = g + dip
music *= (10 ** (g / 20))[:, None]
if CL:   # climax cue (Lyria): 24.5 s into the cue it is rising; its peak lands on "not in a lab, not in a survey"
    place(music, M("climax_a"), CL - 0.1, src_from=24.5, length=19.5, fin=0.8, fout=3.5, gain_db=-10)
i0, i1 = int((ASK - 2.0) * SR), int(ASK * SR)                              # the ask: music gone by the first word
music[i0:i1] *= np.linspace(1, 0, i1 - i0)[:, None] ** 2; music[i1:int((CLOSE - 0.3) * SR)] = 0
bus += music

# ---- sound effects ----
S = {n: load(f"out/sfx/{n}.wav") for n in ["week_tick", "scan_shimmer", "message_chime", "soft_click", "count_tick",
                                            "reverse_swell", "sub_hit", "winner_tone", "strike"]}
for i in range(1, 7): place(bus, S["week_tick"], c[i] + 0.25, gain_db=-8)                 # chapter cards
place(bus, S["scan_shimmer"], ch[1] + 22.3, gain_db=-14)  # chapter 1: "we measure her hair" (app panel on 58)
place(bus, S["message_chime"], ch[2] + 2.6, gain_db=-14)  # chapter 2: Dana's message (booking panel comes in at 2.4 s)
if "diagram" in TL:
    for i in range(5): place(bus, S["soft_click"], TL["diagram"] + 0.4 + 0.8 * i, gain_db=-12)   # diagram boxes
for k in ("winner1", "winner2"):                          # chapter 4: one soft tone as each winner is named
    if k in TL: place(bus, S["winner_tone"], TL[k], gain_db=-17)
if CL:
    place(bus, S["reverse_swell"], CL - 1.6, gain_db=-12)  # into "And L'Oréal learns"
    place(bus, S["sub_hit"], CL - 0.03, gain_db=-7)
for k in ("progo", "behind", "criteria"):                 # one soft tone on chapter 1's PRO•GO, chapter 2's ServiceMarket and the three ticks
    if k in TL: place(bus, S["winner_tone"], TL[k] + 0.2, gain_db=-18)
for k in ("strike1", "strike2"):                          # chapter 1: build, buy struck through
    if k in TL: place(bus, S["strike"], TL[k] - 0.05, gain_db=-16)
if "partner" in TL:                                       # chapter 1 climax: "So we partner" (Amjad full screen)
    place(bus, S["reverse_swell"], TL["partner"] - 1.6, gain_db=-15)
    place(bus, S["sub_hit"], TL["partner"] - 0.03, gain_db=-11)
if "weeks" in TL:                                         # the 0 -> 12 week counter: one tick per number
    prev = 0
    for f in range(23):
        n = int(round(12 * R.ease(f / 30 / 0.75)))
        if n != prev: place(bus, S["count_tick"], TL["weeks"] + f / 30, gain_db=-14)
        prev = n
place(bus, S["scan_shimmer"], ch[6] + 0.3, gain_db=-14)   # week 12 re-scan
prev = None                                               # count ticks: one per number change, same curve as render.score
for f in range(180):
    wk = 12 * R.ease((f / 30 - 0.6) / 3.6); s = R.PTS[0][1]
    for (x0, y0), (x1, y1) in zip(R.PTS, R.PTS[1:]):
        if x0 <= wk <= x1: s = y0 + (y1 - y0) * (wk - x0) / (x1 - x0)
    s = 74 if wk >= 12 else round(s)
    if prev is not None and s != prev: place(bus, S["count_tick"], SCORE + f / 30, gain_db=-16)
    prev = s

wav = DST.replace(".mp4", "_music.wav")
np.clip(bus, -1, 1).astype("<f4").tofile(wav + ".raw")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", wav + ".raw", wav], check=True); os.remove(wav + ".raw")
# voices (from the animatic) + music bus, gentle limiter
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", SRC, "-i", wav, "-filter_complex",
                "[0:a]aresample=48000[v];[v][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", DST], check=True)
print("wrote", DST, "and", wav)
