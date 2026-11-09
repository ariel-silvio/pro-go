"""v16 generations, run once in the background (from video/): new Omni clips 3h/3i, Lyria opening and finale cues,
Layla's new closing line (Gemini TTS, voice Aoede). Prompts are logged in ai-log.md."""
import base64, json, os, subprocess, sys, threading, urllib.request
sys.path.insert(0, "scripts")
import veo_generate as V, lyria as Ly
LAYLA = " Layla: long, glossy, warm-brown hair with soft caramel highlights, an ivory silk blouse; never her face."
CLIPS = {
 "3h": ("From behind, at shoulder height, in a bright, calm Dubai living room in soft daylight: a professional colourist's hands in thin black gloves "
        "gently place an ivory protective cape over a seated woman's shoulders and smooth it; a neat ivory floor mat lies under the chair and a small "
        "ivory kit case with a thin gold line stands on a side table. Slow, careful movements, steady camera, no faces." + LAYLA),
 "3i": ("Seen from inside a bright Dubai apartment hallway: the front door opens and a professional's hand carrying a small ivory case with a thin "
        "gold line comes into frame, followed by a second small bag; the person steps in and the door closes softly. Only hands, arms and the cases "
        "are visible, never a face. Warm morning light, calm, slow, steady camera."),
}
def clip(name, prompt):
    try:
        V.generate(V.MODEL, name, prompt, "out/layla"); print("clip", name, "done", flush=True)
    except Exception as e: print("clip", name, "FAILED", e, flush=True)
STYLE = " No drums kit, no synth, no vocals. Warm felt piano theme in D major, the same three-note motif as the rest of the film, cinematic, restrained."
CUES = {
 "open_v16a": ("Instrumental film score, 18 seconds. It begins almost silent: one single soft felt-piano note, then sparse low piano notes; "
               "from about 3 seconds strings creep in quietly and build steadily; a full, dramatic, emotional swell lands at exactly 11 seconds "
               "and holds to 14 seconds, then settles softly." + STYLE),
 "open_v16b": ("Instrumental film score, 18 seconds. Opens with a single quiet piano note and a breath of air, then a slow, intimate piano line; "
               "low strings enter at 4 seconds, a gentle pulse from 7 seconds, rising tension, a powerful cinematic peak at 11 seconds with full "
               "strings and piano, sustained until 14 seconds, then a soft fall." + STYLE),
 "open_v16c": ("Instrumental film score, 18 seconds. Starts very softly with two single piano notes far apart, then a hopeful piano phrase; "
               "a cello line joins at 5 seconds and the music rises continuously, reaching a bright, majestic, emotional climax at 11 seconds, "
               "held until 14 seconds, then resolving quietly." + STYLE),
 "finale_v16": ("Instrumental film score, 26 seconds. Starts with the soft solo piano theme; warm strings join at 5 seconds and rise steadily "
                "with growing confidence; a full, warm, uplifting orchestral peak at about 17 seconds, held for two seconds, then everything "
                "stops abruptly to silence at 19.5 seconds; after one second of silence, a single soft piano note at 21 seconds and a gentle "
                "resolving chord that fades out by 26 seconds." + STYLE),
}
def cues():
    for n, b in CUES.items(): Ly.generate(n, b)
def tts():
    API = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent"
    style = ("Read as Layla: a 34-year-old professional woman in Dubai, warm, quiet and reflective, speaking to herself in the morning. "
             "Natural, unhurried, intimate, not theatrical, not a narrator. Soft international English accent. Say: ")
    for k in range(2):
        b = {"contents": [{"parts": [{"text": style + "Week twelve. Now I can see it."}]}],
             "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Aoede"}}}}}
        r = urllib.request.Request(API, data=json.dumps(b).encode(), headers={"Content-Type": "application/json"})
        d = json.loads(urllib.request.urlopen(r, timeout=120).read())
        raw = f"out/voice/layla_close2_{k}.pcm"; open(raw, "wb").write(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw, f"out/voice/layla_close2_{k}.wav"], check=True)
    print("tts done", flush=True)
ts = [threading.Thread(target=clip, args=(n, p)) for n, p in CLIPS.items()] + [threading.Thread(target=cues), threading.Thread(target=tts)]
for t in ts: t.start()
for t in ts: t.join()
print("ALL DONE", flush=True)
