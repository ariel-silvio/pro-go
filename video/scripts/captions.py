"""Captions for the M4 film (item 7): one line at a time, on the speaker's half only.
None over full-screen type, lower thirds, the cold open or the closing. Over a full-screen speaker shot they sit centred.
Text: the per-chapter sentence transcripts (edits/ch*_sentences*.json), cleaned (names, spelling, slips that were cut).
Times: raw seconds -> edit seconds with each chapter's own cut map (same numbers as scripts/portrait_edit.py),
then + the chapter's start in out/animatic/timeline.json.
Usage (from video/): python3 scripts/captions.py [timeline.json]  ->  out/captions/captions.ass and captions.srt"""
import json, os, re, sys

TL = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "out/animatic/timeline.json"))
OUT = "out/captions"; os.makedirs(OUT, exist_ok=True)
MAXC = 40

def keep_map(keep, sp):
    def E(t):
        acc = 0.0
        for a, b in keep:
            if t < b: return None if t < a - 0.05 and acc > 0 else (acc + max(0.0, t - a)) / sp
            acc += b - a
        return acc / sp
    return E
MAP = {1: lambda t: (t - 1.4) / 1.08,
       2: lambda t: t,                                      # ch2 file is already in edit seconds
       3: keep_map([(2.1, 32.55), (33.45, 45.3), (47.72, 55.9), (58.82, 85.3)], 1.10),
       4: lambda t: t - 2.6,
       5: keep_map([(0.2, 3.68), (4.25, 43.85), (44.95, 81.2)], 1.08),
       6: lambda t: t}
FILES = {i: f"edits/ch{i}_sentences_raw.json" for i in (1, 3, 4, 5, 6)}; FILES[2] = "edits/ch2_take2_sentences.json"
FIX = [(r"\bLaila\b|\bLeila\b", "Layla"), (r"\bDina\b", "Dana"), (r"ProGol?\b", "PRO•GO"), (r"made-up", "made up"),
       (r"colorist", "colourist"), (r"\bcolors\b", "colours"), (r"\bcolor\b", "colour"), (r"service market", "ServiceMarket"),
       (r"need its own", "needs its own"), (r"at first place", "in the first place"), (r"That's why, then\.", "That's why them."),
       (r"Do they make salons stronger or takes its place", "Do they make salons stronger, or take their place"),
       (r"eight weeks weeks", "eight weeks"), (r"one leader, no committee, not a committee", "one leader, not a committee"),
       (r"not an acquisition yet", "not an acquisition"), (r"we match three numbers", "we watch three numbers"),
       (r"from the pilots\.", "from the pilot."), (r"instead cheaper, safer", "instead: cheaper, safer"),
       (r"Week number two", "Week two"), (r"company services", "companies' services")]
DROP = {3: ("Data ownership is clearly defined.", "Commercially, the numbers must work.")}

def clean(s):
    for a, b in FIX: s = re.sub(a, b, s)
    return s

def chunks(text):
    """Split a sentence into lines of at most MAXC characters, preferring breaks after commas."""
    words, out, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > MAXC:
            if "," in cur[:-1] and len(cur) > MAXC * 0.6:           # break at the last comma if the remainder is short
                k = cur.rfind(",") + 1
                if len(cur) - k < 16: out.append(cur[:k].strip()); cur = cur[k:].strip()
            out.append(cur); cur = w
        else: cur = (cur + " " + w).strip()
    return out + [cur] if cur else out

# windows with no captions (film seconds): cold open, cards, full-screen type, lower thirds, the closing
F = lambda i: TL[f"ch{i}"]
quiet = [(0, F(1))] + [(TL[f"card{i}"], F(i)) for i in range(2, 7)] + [(TL["closing"], TL["end"])]
speaker_full = []
for i in (1, 3, 4, 5, 6):
    p = f"edits/fulls_ch{i}.json"
    if not os.path.exists(p): continue
    for a, b in json.load(open(p)):
        if (i, a) in ((1, round((80.1 - 1.4) / 1.08, 3)), (5, round(MAP[5](74.6), 3))): speaker_full.append((F(i) + a, F(i) + b))
        else: quiet.append((F(i) + a, F(i) + b))
LTS = {1: (1, 5), 2: (0.3, 4.2), 3: (0.6, 3.9), 4: (1, 5), 5: (MAP[5](7.4), MAP[5](11.4)), 6: (14.8, 18.8)}
for i, (a, b) in LTS.items(): quiet.append((F(i) + a - 0.2, F(i) + b + 0.2))
if os.path.exists("edits/fulls_ch2.json"):
    for a, b, kind in json.load(open("edits/fulls_ch2.json")):
        (speaker_full if kind == "ariel" else quiet).append((F(2) + a, F(2) + b))

def inside(t, wins): return any(a <= t < b for a, b in wins)
cues = []
for i in range(1, 7):
    S = json.load(open(FILES[i])); end_ch = TL[f"card{i + 1}"] if i < 6 else TL["closing"]
    for n, s in enumerate(S):
        if s["text"] in DROP.get(i, ()): continue
        a, b = MAP[i](s["start"]), MAP[i](s["end"])
        if a is None or b is None: continue
        nxt = MAP[i](S[n + 1]["start"]) if n + 1 < len(S) else None
        b = max(b, a + 0.6); b = min(b + 0.25, nxt) if nxt else b + 0.25
        a, b = F(i) + max(a, 0), min(F(i) + b, end_ch - 0.05)
        parts = chunks(clean(s["text"])); tot = sum(len(p) for p in parts); t = a
        for p in parts:
            d = (b - a) * len(p) / tot; cues.append((t, t + d, p)); t += d

def keep(c):
    a, b, _ = c; mid = (a + b) / 2
    return not inside(mid, quiet)
cues = [c for c in cues if keep(c)]

def ts(t, srt=False):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",") if srt else f"{h}:{m:02d}:{s:05.2f}"
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Half,Jost,38,&H00FFFFFF,&H00FFFFFF,&H00111111,&H8C111111,0,0,0,0,100,100,0,0,3,10,0,2,1000,40,64,1
Style: Full,Jost,40,&H00FFFFFF,&H00FFFFFF,&H00111111,&H8C111111,0,0,0,0,100,100,0,0,3,10,0,2,200,200,64,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev, srt = [], []
for k, (a, b, txt) in enumerate(cues, 1):
    style = "Full" if inside((a + b) / 2, speaker_full) else "Half"
    ev.append(f"Dialogue: 0,{ts(a)},{ts(b)},{style},,0,0,0,,{txt}")
    srt.append(f"{k}\n{ts(a, True)} --> {ts(b, True)}\n{txt}\n")
open(f"{OUT}/captions.ass", "w").write(hdr + "\n".join(ev) + "\n")
open(f"{OUT}/captions.srt", "w").write("\n".join(srt))
print(len(cues), "captions ->", f"{OUT}/captions.ass")
