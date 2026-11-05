"""Generate the Layla scenes with Gemini Omni Flash (Gemini API, Interactions endpoint).

Veo preview models were shut down in the Gemini API on 22 Oct 2026; Gemini Omni Flash replaces them.
The API key is NOT in this script or the repo: the cloud environment's network proxy adds the
x-goog-api-key header to requests for generativelanguage.googleapis.com. For a one-off run the key can
instead come from the GEMINI_API_KEY environment variable (never written to disk).

Usage (from video/):
  python3 scripts/veo_generate.py --list-models
  python3 scripts/veo_generate.py --scenes 1,2,3,5 --out out/layla
Prompts are read from layla-prompts.md (the quoted block under each "## N." heading).
Each clip is saved raw (layla_N_raw.mp4) and as the delivery file layla_N.mp4: 1920x1080, 30 fps,
H.264 yuv420p, audio removed.
"""
import argparse, base64, json, os, re, subprocess, sys, time, urllib.request, urllib.error

API = "https://generativelanguage.googleapis.com/v1beta"
MODEL = "gemini-omni-1.2-flash"
CENTRE = (" Subject centred in the frame, main action in the middle third, empty calm space at the sides."
          " Natural human anatomy: realistic, relaxed arm, wrist and elbow movement, small slow gestures.")
NEGATIVE = ("face, eyes, lips, profile, logo, brand name, readable text, watermark, fast motion, "
            "camera shake, neon, cold blue light, cluttered background, extra fingers, distorted hands, "
            "unnatural joints, twisted or hyperextended elbow, bending arms, morphing limbs")

def call(method, url, body=None, timeout=900):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"}
    if os.environ.get("GEMINI_API_KEY"): headers["x-goog-api-key"] = os.environ["GEMINI_API_KEY"]
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} on {url.split('?')[0]}: {e.read().decode()[:600]}")

def prompts(path="layla-prompts.md"):
    text = open(path, encoding="utf-8").read()
    return {int(m.group(1)): m.group(2).strip()
            for m in re.finditer(r"^## (\d)\..*?\n\n> (.+?)\n", text, re.M | re.S)}

def list_models():
    for m in call("GET", f"{API}/models?pageSize=1000").get("models", []):
        if any(k in m["name"] for k in ("omni", "veo")): print(m["name"], m.get("supportedGenerationMethods"))

def to_delivery(raw, out):
    tmp = out[:-4] + ".part.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-an",
                    "-vf", "scale=1920:1080:flags=lanczos,fps=30,format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)

def generate(model, n, prompt, out):
    body = {"model": model, "input": prompt + CENTRE + " Avoid: " + NEGATIVE + ".",
            "response_format": {"type": "video", "aspect_ratio": "16:9"}}
    t = time.time(); d = call("POST", f"{API}/interactions", body)
    vids = [c for s in d.get("steps", []) if s.get("type") == "model_output"
            for c in s.get("content", []) if c.get("type") == "video"]
    if d.get("status") != "completed" or not vids:
        sys.exit(f"scene {n}: no video (status {d.get('status')}): {json.dumps(d)[:400]}")
    raw = os.path.join(out, f"layla_{n}_raw.mp4")
    open(raw, "wb").write(base64.b64decode(vids[0]["data"]))
    to_delivery(raw, os.path.join(out, f"layla_{n}.mp4"))
    print(f"scene {n}: {time.time() - t:.0f}s, {d['usage']['total_output_tokens']} output tokens -> layla_{n}.mp4")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--scenes", default="1,2,3,4,5")
    ap.add_argument("--out", default="out/layla")
    a = ap.parse_args()
    if a.list_models: list_models(); sys.exit()
    os.makedirs(a.out, exist_ok=True); P = prompts()
    for n in [int(x) for x in a.scenes.split(",")]:
        generate(a.model, n, P[n], a.out)
