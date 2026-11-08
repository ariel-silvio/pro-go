# Layla scene prompts (M4 video, "12 weeks with Layla")

Generated with Gemini Omni Flash via `scripts/veo_generate.py` (Veo preview models were shut down in the Gemini API on 22 Oct 2026). Can also be run by hand in Gemini, Runway or Kling.
Every prompt is logged in `ai-log.md` for the course AI disclosure.

**Split-screen framing (decided 5 Nov):** the video is 16:9 and these clips mostly play in the **left half (960 × 1080)**, beside the speaker. Generate at 16:9, but keep the subject and the action in the **centre third** of the frame, so a centre crop still works. The same clip can then also run full screen.

Add to every prompt: `subject centred in the frame, main action in the middle third, empty calm space at the sides`.

**Rules for every clip:** no faces; hands, phone, hair from behind, interiors only; warm Dubai daylight; muted ivory and gold tones; 5 to 8 seconds; 16:9 (1920 × 1080); calm, slow camera, no fast cuts; no real logos or brand names; no readable text on screens (prototype footage replaces screen content in the edit).

Negative prompt to add where the tool supports it:
`face, eyes, lips, profile, logo, brand name, readable text, watermark, fast motion, camera shake, neon, cold blue light, cluttered background`

---

## 1. Week 0, Opening and S1 (phone scan)

> Close-up, 16:9, 6 seconds. A woman's hand holds a smartphone a few centimetres from the lengths of her long dark coloured hair, seen from behind and slightly to the side, no face visible. Bright modern Dubai apartment, soft warm morning daylight through sheer ivory curtains, gentle out-of-focus city skyline. The phone screen glows with a soft abstract light sweep suggesting a hair scan, no readable text. Muted ivory, sand and soft gold palette. Slow push-in, shallow depth of field, calm, cinematic, natural skin tones.

Use: left half, 0:00–0:15 and the start of S1. Screen content is replaced by `p1_scan_result_58`.

## 2. Week 1, S2 (booking confirmation)

> Static top-down-angled shot, 16:9, 6 seconds. A smartphone lies on a white marble kitchen counter beside a small ceramic cup and a sprig of greenery. The screen shows a simple light-coloured confirmation layout with no readable text. Behind, an out-of-focus floor-to-ceiling window with a warm hazy Dubai city view in late afternoon light. A woman's hand enters the frame and gently picks up the phone, no face visible. Ivory, marble white and soft gold palette, calm, minimal, slow.

Use: left half, S2. Screen content is replaced by `p3_booking_confirmation`.

## 3. Week 2, S3 (first home visit, professional from her partner salon)

> Medium close-up, 16:9, 7 seconds. A professional colourist's gloved hands apply hair colour with a brush to a section of a seated woman's hair, filmed from behind at shoulder height, no faces visible. Bright Dubai living room in warm daylight. On the side table, a neat small kit in plain ivory packaging with a thin gold line, and a folded ivory card on a stand that reads only "Partner salon" in simple serif type. No logos, no brand names. Calm, careful movements, slow lateral camera drift, muted ivory and gold tones.

Use: left half, S3. The "Partner salon" card keeps the baseline rule visible: the professional comes from her own salon. If the tool garbles the text, remove the card from the prompt and let the editor add a lower-third tag "From her partner salon".

## 4. Week 8, S5 (mid-plan check)

> Medium shot, 16:9, 6 seconds. A woman seen from behind sits by a large window and slowly brushes her long glossy coloured hair; the brush glides smoothly, light catches the shine. Warm Dubai late-afternoon sun, sheer ivory curtains moving slightly, soft bokeh city view. No face, no mirror reflection of the face. Muted ivory, honey and soft gold palette, calm, slow, cinematic.

Use: left half, S5. Pairs with `p4_rescan` if the team keeps the week-8 re-scan in the prototype.

## 5. Week 12, S6 (re-scan, she renews)

> Close-up, 16:9, 6 seconds. Two hands hold a smartphone in portrait at chest height, a woman's glossy coloured hair falling over one shoulder in soft focus, no face visible. The screen shows a simple light layout with a single large number gently counting up and a thin gold line rising, no other readable text. Warm Dubai daylight in a calm ivory interior. Slow push-in, shallow depth of field, calm and quietly satisfied mood.

Use: left half, S6. Screen content is replaced by the score graphic (58 to 74, marked "Illustrative") or by prototype footage.

---

## Extra clips (B-roll, v2): two or three per chapter so the left half changes every 6–8 s

Continuity line added to every prompt: *"Layla: long, glossy, warm-brown hair with soft caramel highlights, an ivory silk blouse; never her face."* Generated with Gemini Omni 1.2 Flash via `scripts/broll.py`, same centre-framing, anatomy and avoid lines as above.

| ID | Chapter | Prompt |
|---|---|---|
| 1b | Week 0 | Extreme close-up: her fingers lift the coloured ends of her hair to the window light; the ends look a little dry. Bright Dubai apartment, morning. Slow push-in. |
| 1c | Week 0 | A bathroom shelf in soft daylight: her hand picks up a plain, unbranded box of home hair colour, looks at it, and puts it back. No text, no logo. Static shot. |
| 2b | Week 1 | Over the shoulder from behind: she sits on a cream sofa and types a short message on her phone; the screen is a soft blur, not readable. Late afternoon light. |
| 2c | Week 1 | A phone lies on a light wooden side table; its screen lights up softly with a new message; a cup and a small plant beside it. Shallow focus, warm evening light. |
| 3b | Week 2 | Seen from inside the apartment: the front door opens; only a professional's hand and a small ivory case with a thin gold line come into frame. No faces. |
| 3c | Week 2 | Gloved hands mix hair colour in a small black bowl with a tint brush, on a white table by a window. Close-up, slow and careful. |
| 3d | Week 2 | ~~From behind: gloved hands divide her hair into neat sections with a tail comb and clip them.~~ Replaced by 3g: hair clips appeared and moved on their own. |
| 3g | Week 2 | Seen from behind at shoulder height: a professional colourist's hands in thin black gloves slowly comb through one section of her long hair with a fine black comb, from the roots to the ends, in one smooth continuous movement, then gently lift the section to look at the colour. No hair clips, no other tools, nothing appears or disappears. Calm living room, soft daylight, slow and careful, steady camera. (two takes, 3e and 3f, joined before their artefacts) |
| 4b | Week 4 | Her hands open a plain ivory parcel on a hallway console: a small colour-care kit inside, thin gold line, no text. |
| 4c | Week 4 | From behind in a bright bathroom: she smooths a hair mask through her lengths with both hands. Steam-soft light, slow. |
| 5b | Week 10 | From behind: she walks slowly down a bright corridor towards a window; her glossy hair moves as she walks. |
| 5c | Week 10 | Close-up: gloved hands rinse her hair over a portable basin; water and light, calm. From behind and above, no face. |
| 6b | Week 12 | Close-up: her finger taps once on a phone screen; the screen is plain ivory with a thin gold line, no text. |
| 6c | Week 12 | Wide, from behind: she stands on a balcony at golden hour, the Dubai skyline soft in the distance, her hair moving in the breeze. Slow, final shot. |

---

## Cold open v2 (6 Nov 2026): morning, mirror, leaving, horizon

| ID | Prompt |
|---|---|
| 0a | Medium shot from behind and slightly to one side, at shoulder height: early morning in her bright Dubai apartment hallway, dressed for work in an ivory silk blouse and a camel blazer. She stops in front of a tall mirror, lifts a strand of her coloured hair between her fingers, looks at it and pauses, thoughtful. The camera stays behind her; the mirror reflection is soft and out of focus and cropped at her shoulders, so her face is never visible. Warm low morning sun. |
| 0b | From inside the apartment, behind her at waist height: she picks up her bag and phone from a pale console table, walks to the front door and out into a bright corridor; the door slowly closes behind her. Static camera, calm. |
| 0c | Slow upward tilt and gentle push from a sunlit apartment window towards the hazy morning Dubai skyline and the horizon, golden light, calm, no people, no text. The shot ends on wide open sky above the city. |
