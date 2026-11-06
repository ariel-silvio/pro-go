"""Synthesise the film's designed sound effects (original, license-free). Usage (from video/): python3 scripts/sfx.py
Writes out/sfx/*.wav at 48 kHz: week_tick, scan_shimmer, message_chime, soft_click, count_tick."""
import os, subprocess
import numpy as np
SR = 48000; OUT = "out/sfx"; os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)
def t(d): return np.arange(int(SR * d)) / SR
def env(n, a, d):           # attack then exponential decay (seconds)
    x = np.arange(n) / SR; return np.minimum(x / max(a, 1e-4), 1) * np.exp(-x / d)
def save(name, x, stereo_spread=0.0):
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.5                       # peak about -6 dBFS; levels are set in the mix
    l, r = x * (1 - stereo_spread), np.roll(x, int(SR * 0.0007)) * (1 + stereo_spread)
    st = np.stack([l, r], 1).astype(np.float32).tobytes()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-af", "afade=t=out:st=%.3f:d=0.02" % (len(x) / SR - 0.02), "-c:a", "pcm_s24le", f"{OUT}/{name}.wav"], input=st, check=True)
    print("wrote", f"{OUT}/{name}.wav", f"{len(x) / SR:.2f}s")

# week tick: a soft, dry wooden tick (like a quiet clock), same on every chapter card
x = t(0.12); n = len(x)
tick = (np.sin(2 * np.pi * 1850 * x) + 0.45 * np.sin(2 * np.pi * 3720 * x) + 0.2 * np.sin(2 * np.pi * 920 * x)) * env(n, 0.0006, 0.018)
tick += rng.normal(0, 1, n) * env(n, 0.0002, 0.004) * 0.35
save("week_tick", tick)

# scan shimmer: rising glassy partials with a breath of air, 1.6 s (cold open and week 12, so the loop closes)
x = t(1.6); n = len(x); sh = np.zeros(n)
for k, (f0, f1) in enumerate([(1200, 2100), (1800, 3150), (2400, 4200), (3000, 5250)]):
    f = f0 + (f1 - f0) * (x / x[-1]) ** 1.5; ph = 2 * np.pi * np.cumsum(f) / SR
    sh += np.sin(ph + k) * (0.6 ** k) * (1 + 0.25 * np.sin(2 * np.pi * (5 + k) * x))
air = np.convolve(rng.normal(0, 1, n), np.ones(24) / 24, "same")
sh = (sh + 0.25 * air) * np.sin(np.pi * np.clip(x / x[-1], 0, 1)) ** 1.6
save("scan_shimmer", sh, 0.08)

# message chime: two soft bell notes, generic (not any app's sound)
def bell(freq, d=0.9):
    x = t(d); n = len(x)
    return (np.sin(2 * np.pi * freq * x) + 0.35 * np.sin(2 * np.pi * freq * 2.76 * x) * np.exp(-x / 0.12)
            + 0.18 * np.sin(2 * np.pi * freq * 5.4 * x) * np.exp(-x / 0.05)) * env(n, 0.003, 0.32)
c = np.zeros(int(SR * 1.1)); a = bell(1318.5); b = bell(1975.5)      # E6 then B6
c[:len(a)] += a; o = int(SR * 0.13); c[o:o + len(b)] += 0.8 * b[:len(c) - o]
save("message_chime", c, 0.05)

# soft click: felt, not digital (diagram steps appearing)
x = t(0.08); n = len(x)
cl = np.sin(2 * np.pi * 520 * x) * env(n, 0.0005, 0.012) + np.convolve(rng.normal(0, 1, n), np.ones(6) / 6, "same") * env(n, 0.0002, 0.003) * 0.6
save("soft_click", cl)

# count tick: very small high tick under the 58 -> 74 count
x = t(0.05); n = len(x)
save("count_tick", np.sin(2 * np.pi * 2600 * x) * env(n, 0.0004, 0.007))
