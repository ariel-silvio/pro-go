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
