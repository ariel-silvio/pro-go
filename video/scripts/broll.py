"""Generate the extra Layla B-roll clips listed in layla-prompts.md ("Extra clips" table) with Gemini Omni.
Usage (from video/): python3 scripts/broll.py [IDs comma-separated]   e.g.  python3 scripts/broll.py 1b,1c
"""
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veo_generate as V

LOOK = (" Layla: long, glossy, warm-brown hair with soft caramel highlights, an ivory silk blouse; never her face."
        " Warm Dubai daylight, muted ivory and gold tones, calm, cinematic, 16:9, no faces, no readable text, no logos.")
text = open("layla-prompts.md", encoding="utf-8").read().split("## Extra clips", 1)[1]
rows = {m.group(1): m.group(2).strip() for m in re.finditer(r"^\| (\d[a-z]) \| [^|]+ \| (.+?) \|$", text, re.M)}
ids = sys.argv[1].split(",") if len(sys.argv) > 1 else list(rows)
os.makedirs("out/layla", exist_ok=True)
for i in ids:
    if os.path.exists(f"out/layla/layla_{i}.mp4"): print(i, "exists, skipped"); continue
    for attempt in range(3):
        try:
            V.generate(V.MODEL, i, rows[i] + LOOK, "out/layla"); break
        except SystemExit as e:
            print(i, "attempt", attempt + 1, "failed:", str(e)[:90]); time.sleep(25)
