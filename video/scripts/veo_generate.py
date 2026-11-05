"""Generate the Layla scenes with Veo (Gemini API).

The API key is NOT in this script or the repo: the cloud environment's network proxy adds the
x-goog-api-key header to requests for generativelanguage.googleapis.com.

Usage (from video/):
  python3 scripts/veo_generate.py --list-models
  python3 scripts/veo_generate.py --model veo-3.1-fast-generate-preview --scenes 1,2,3,4,5 --out out/layla
Prompts are read from layla-prompts.md (the quoted block under each "## N." heading).
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

API = "https://generativelanguage.googleapis.com/v1beta"
CENTRE = " Subject centred in the frame, main action in the middle third, empty calm space at the sides."
NEGATIVE = ("face, eyes, lips, profile, logo, brand name, readable text, watermark, fast motion, "
            "camera shake, neon, cold blue light, cluttered background, extra fingers, distorted hands")

def call(method, url, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return json.loads(raw) if raw[:1] in (b"{", b"[") else raw
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {url.split('?')[0]}: {e.read().decode()[:600]}")

def prompts(path="layla-prompts.md"):
    text = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"^## (\d)\..*?\n\n> (.+?)\n", text, re.M | re.S):
        out[int(m.group(1))] = m.group(2).strip()
    return out

def list_models():
    res = call("GET", f"{API}/models?pageSize=200")
    for m in res.get("models", []):
        if "veo" in m["name"]:
            print(m["name"], m.get("supportedGenerationMethods"))

def generate(model, n, prompt, out, duration, resolution):
    body = {"instances": [{"prompt": prompt + CENTRE}],
            "parameters": {"aspectRatio": "16:9", "negativePrompt": NEGATIVE,
                           "durationSeconds": duration, "resolution": resolution}}
    op = call("POST", f"{API}/models/{model}:predictLongRunning", body)
    name = op["name"]; print(f"scene {n}: started {name}")
    while not op.get("done"):
        time.sleep(10); op = call("GET", f"{API}/{name}")
    if "error" in op: sys.exit(f"scene {n}: {op['error']}")
    resp = op["response"]
    samples = (resp.get("generateVideoResponse", {}).get("generatedSamples")
               or resp.get("generatedVideos") or [])
    if not samples: sys.exit(f"scene {n}: no video returned (filtered?): {json.dumps(resp)[:400]}")
    uri = samples[0]["video"]["uri"]
    raw = call("GET", uri)
    path = os.path.join(out, f"layla_{n}_raw.mp4")
    open(path + ".part", "wb").write(raw); os.replace(path + ".part", path)
    print(f"scene {n}: saved {path} ({len(raw)} bytes)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--model", default="veo-3.1-fast-generate-preview")
    ap.add_argument("--scenes", default="1,2,3,4,5")
    ap.add_argument("--out", default="out/layla")
    ap.add_argument("--duration", type=int, default=8)
    ap.add_argument("--resolution", default="1080p")
    a = ap.parse_args()
    if a.list_models: list_models(); sys.exit()
    os.makedirs(a.out, exist_ok=True); P = prompts()
    for n in [int(x) for x in a.scenes.split(",")]:
        generate(a.model, n, P[n], a.out, a.duration, a.resolution)
