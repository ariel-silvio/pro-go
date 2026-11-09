"""Synthesise the film's designed sound effects (original, license-free). Usage (from video/): python3 scripts/sfx.py
Writes out/sfx/*.wav at 48 kHz: week_tick, scan_shimmer, message_chime, soft_click, count_tick, reverse_swell, sub_hit, winner_tone, strike."""
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

# scan read (replaces the first "shimmer", whose rising, wobbling partials sounded like a cat):
# a soft unpitched light sweep (band-passed air moving upward), then a short warm confirm, D5 then A5, no glide, no vibrato
x = t(1.25); n = len(x); sh = np.zeros(n)
noise = rng.standard_normal(n); sweep = np.zeros(n); win = 1024; hop = 256
for i0 in range(0, int(0.62 * SR) - win, hop):                 # band-pass the noise along a rising centre frequency
    fc = 900 + 3400 * (i0 / (0.62 * SR)) ** 1.3
    seg = np.fft.rfft(noise[i0:i0 + win] * np.hanning(win)); f = np.fft.rfftfreq(win, 1 / SR)
    seg *= np.exp(-0.5 * ((f - fc) / (fc * 0.18)) ** 2)
    sweep[i0:i0 + win] += np.fft.irfft(seg, win)
sweep *= np.sin(np.pi * np.clip(x / 0.62, 0, 1)) ** 2 * 0.9
def soft(freq, at, d=0.55):
    y = np.zeros(n); k = int(at * SR); m = min(n - k, int(d * SR)); xx = np.arange(m) / SR
    y[k:k + m] = (np.sin(2 * np.pi * freq * xx) + 0.12 * np.sin(2 * np.pi * 2 * freq * xx)) * np.minimum(xx / 0.012, 1) * np.exp(-xx / 0.22)
    return y
sh = sweep + 0.55 * soft(587.33, 0.52) + 0.5 * soft(880.0, 0.66)
save("scan_shimmer", sh, 0.06)

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

# count tick: a soft, rounded tick under the 58 -> 74 count (lower and gentler than before), then the scan's confirm note
x = t(0.06); n = len(x)
save("count_tick", (np.sin(2 * np.pi * 1500 * x) + 0.3 * np.sin(2 * np.pi * 750 * x)) * env(n, 0.0015, 0.01))
n = int(SR * 0.9); x = np.arange(n) / SR
save("confirm", 0.55 * soft(587.33, 0.0, 0.8)[:n] + 0.5 * soft(880.0, 0.14, 0.7)[:n], 0.05)

# room tone for the cold open: quiet, low, brownish air that fades out by about 7 s
d = 8.0; n = int(SR * d); x = np.arange(n) / SR
br = np.cumsum(rng.standard_normal(n)); br -= np.convolve(br, np.ones(4800) / 4800, mode="same")   # brown noise, no DC drift
br = np.convolve(br, np.ones(40) / 40, mode="same") * np.minimum(x / 0.8, 1) * np.clip((7.0 - x) / 2.5, 0, 1)
save("room_tone", br, 0.2)

# one piano-like note for the mirror bookend (D4, struck, slow decay, a little hammer)
d = 4.0; n = int(SR * d); x = np.arange(n) / SR; f0 = 293.66
pn = sum(a_ * np.sin(2 * np.pi * f0 * k_ * x * (1 + 0.0004 * k_ * k_)) * np.exp(-x / (1.6 / k_ ** 0.7))
         for k_, a_ in ((1, 1.0), (2, 0.45), (3, 0.22), (4, 0.12), (5, 0.06)))
pn = pn * np.minimum(x / 0.004, 1) + 0.05 * rng.standard_normal(n) * np.exp(-x / 0.01)
save("piano_note", pn, 0.1)

# climax (chapter 4, "And L'Oréal learns"): reverse swell into a deep, soft hit
rng = np.random.default_rng(7)
d = 1.6; x = t(d); n = len(x)
noise = rng.standard_normal(n)
k = np.exp(-np.arange(0, 0.05, 1 / SR) / 0.01); k /= k.sum()               # gentle low-pass
sw = np.convolve(noise, k, mode="same") * (x / d) ** 3                         # rises into the hit
sw += 0.5 * np.sin(2 * np.pi * (110 + 110 * x / d) * x) * (x / d) ** 4
save("reverse_swell", sw / np.max(np.abs(sw)) * 0.5, 0.15)
d = 2.4; x = t(d); n = len(x)
hit = np.sin(2 * np.pi * 48 * x) * env(n, 0.004, 0.9) + 0.35 * np.sin(2 * np.pi * 96 * x) * env(n, 0.004, 0.35)
hit += 0.15 * np.convolve(rng.standard_normal(n), k, mode="same") * env(n, 0.002, 0.08)
save("sub_hit", hit / np.max(np.abs(hit)) * 0.8)
# winner tone (chapter 4: the salon, ServiceMarket): one soft bell, warm
save("winner_tone", bell(659.25, 1.6) * 0.6 + np.pad(bell(987.77, 1.2), (0, int(SR * 0.4))) * 0.25, 0.05)
# strike (chapter 1, "build" and "buy" struck through): a short, soft swish, like a pen across paper
d = 0.32; x = t(d); n = len(x)
sw2 = np.convolve(rng.standard_normal(n), np.ones(24) / 24, mode="same") * np.sin(np.pi * x / d) ** 2
sw2 = sw2 - np.convolve(sw2, np.ones(200) / 200, mode="same")           # thin it: no low rumble
save("strike", sw2, 0.1)
