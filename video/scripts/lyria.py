"""Generate music with Lyria (Gemini API, Interactions endpoint, background mode; the key comes from the environment proxy).
Usage (from video/): python3 scripts/lyria.py NAME "brief"   ->  out/music/NAME.mp3 and music/NAME_brief.txt"""
import base64, json, sys, time, urllib.request, urllib.error
API = "https://generativelanguage.googleapis.com/v1beta"
def call(m, u, b=None):
    r = urllib.request.Request(u, data=json.dumps(b).encode() if b else None, method=m, headers={"Content-Type": "application/json"})
    try: return json.loads(urllib.request.urlopen(r, timeout=60).read())
    except urllib.error.HTTPError as e: return {"HTTP": e.code, "err": e.read().decode()[:400]}
def generate(name, brief, model="lyria-3-pro-preview", tries=3):
    for attempt in range(tries):
        d = call("POST", API + "/interactions", {"model": model, "input": brief, "background": True}); t = time.time()
        while d.get("status") in ("in_progress", "queued") and time.time() - t < 400:
            time.sleep(8); d = call("GET", API + "/interactions/" + d["id"])
        for s in d.get("steps", []):
            for c in (s.get("content") or []):
                if isinstance(c, dict) and c.get("data") and "audio" in (c.get("mime_type") or ""):
                    open(f"out/music/{name}.mp3", "wb").write(base64.b64decode(c["data"]))
                    open(f"music/{name}_brief.txt", "w").write(brief)
                    print(name, "ok", round(time.time() - t), "s", d.get("model")); return True
        print(name, "attempt", attempt + 1, "->", d.get("status"), d.get("err", "")[:120]); time.sleep(15)
    return False
if __name__ == "__main__": generate(sys.argv[1], sys.argv[2])
