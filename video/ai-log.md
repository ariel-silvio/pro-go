# AI log, M4 video "12 weeks with Layla"

Course rule: GenAI use must be acknowledged. Team D's disclosure lists the tools and prompts used.
The individual 2-page report is out of scope: no AI is used there.

| Date | Tool | What it made | Prompt | Where the output is used |
|---|---|---|---|---|
| ≤ 5 Nov 2026 | Claude (claude.ai, project "Corporate Entrepreneurship") | Storyline options, script drafts, beat sheet, recording setup guide, graphics design, `render.py`, sample clips v1 | Planning chat (see the claude.ai project) | Whole video |
| 5 Nov 2026 | Claude Code (cloud session) | Font setup (`video/fonts/`, converted from @fontsource woff2), prototype filming script `video/scripts/film_prototype.cjs`, test stills of the prototype | Handoff file `handoff-m4-video.md` (Step 0 and Step 3) | Prototype footage, left half of the split screen |
| 5 Nov 2026 | Claude Code (cloud session) | Five Layla scene prompts | Handoff Step 4 (rules: no faces, Dubai daylight, ivory and gold, 5–8 s, 16:9) | `video/layla-prompts.md`; clips made later by a teammate |
| 5 Nov 2026 | Claude Code (cloud session) | `video/render.py` saved from the planning chat; chart right edge moved 1760 → 1720 px for the 160 px margin; 3 sample clips re-rendered and uploaded to Descript as `Graphics/*_v1.mp4` | "Upload the three sample clips" (handoff Step 1) | Descript project, Graphics/ |
| 5 Nov 2026 | Agent Underlord (Descript) | Nothing: asked to remove the failed composition "Graphics sample v1" and 3 empty media items, it replied it has no delete tool (1.9 AI credits) | "Delete the composition 'Graphics sample v1' and the three failed media files …" | Descript project clean-up |
| 5 Nov 2026 | Claude Code (cloud session) | Split-screen format: prototype filmed (p1 scan result 58, p3 booking confirmation) and encoded as 960 × 1080 left-half panels (`scripts/panel.sh`), layout mock (`scripts/mock_split.py`), centre-crop rule added to the Layla prompts; panels uploaded to Descript `Prototype/` | "Let's use 16:9, sometimes split the screen with the app or Layla on one side and us speaking on the other" | Left half of the split screen |
| 5 Nov 2026 | Claude Code (cloud session) | Shooting script v1 (`video/script.md`): cold open, six chapters, closing card, Layla's on-screen lines, picture and sound notes, blanks for the partner | "I would like first to create the script. Take the role of a cinematographic copywriter and producer, avoid AI language, make it very impactful, engaging and beautiful scenes." | Whole video; the team edits the text |
| 5 Nov 2026 | Claude Code (cloud session) | Speaker order by role in `script.md`; six lower-third overlays (`scripts/lower_thirds.py`, RGBA PNG) and one ProRes 4444 test (`LT_S2_Ariel_test.mov`) uploaded to Descript `Graphics/LowerThirds/` | "These are the group members, with respective fictional roles. Use them for the video." (team board screenshots) | Lower thirds, one per speaker |
| 5 Nov 2026 | Claude Code (cloud session) | Name corrected to Qhakazile; remaining five ProRes 4444 lower thirds and all six PNGs uploaded to Descript `Graphics/LowerThirds/` | "Qhakazile" | Lower thirds |
| 5 Nov 2026 | Agent Underlord (Descript) | New composition "Graphics review v1" (25 s): slate, chapter card, two prototype panels, score counter (13.5 AI credits) | "Create a NEW composition named 'Graphics review v1' … in this order …" | Review timeline in Descript |
| 5 Nov 2026 | Agent Underlord (Descript) | Stock search for the five Layla scenes; composition "Layla scenes v1" holds 1 loose match (scene 4); scenes 1, 2, 3, 5 had no clip without faces or off-palette (7.7 AI credits) | "Find stock video clips for a short film about a woman named Layla in Dubai … NO visible faces …" | Test only |
| 5 Nov 2026 | Gemini Omni 1.2 Flash (Google, via Gemini API; replaces Veo, whose preview models were shut down 22 Oct 2026), run by Claude Code | Layla scene 4, week 8: woman from behind brushing her hair by a window (6 s, converted to 1080p30, sound removed) | Prompt 4 in `layla-prompts.md` + centre-framing line + "Avoid: face, eyes, lips, profile, logo, …" | Chapter 5 left half; Descript `Layla/layla_4_week8_brushing.mp4` |

| 5 Nov 2026 | Gemini Omni 1.2 Flash, run by Claude Code | Scene 4 v2 (v1 rejected by Ariel: unnatural elbow). Prompt extended with "Natural human anatomy: realistic, relaxed arm, wrist and elbow movement" and "Avoid: unnatural joints, twisted or hyperextended elbow" | Prompt 4 + anatomy line | Chapter 5; `Layla/layla_4_week8_brushing_v2.mp4` |
| 5 Nov 2026 | Gemini Omni 1.2 Flash, run by Claude Code | Scene 1, week 0, phone by her hair; trimmed to 4.4 s because her lips and chin enter the frame at 4.5 s | Prompt 1 + centre + anatomy lines | Cold open / chapter 1; `Layla/layla_1_week0_scan.mp4` |
| 5 Nov 2026 | Gemini Omni 1.2 Flash, run by Claude Code | Scene 2, week 1, phone on marble counter picked up | Prompt 2 + centre + anatomy lines | Chapter 2; `Layla/layla_2_week1_booking.mp4` |
| 5 Nov 2026 | Gemini Omni 1.2 Flash, run by Claude Code | Scene 3, week 2: original prompt (dye application, "Partner salon" card) failed 6 times with HTTP 502; reworded: gloved hairdresser's hands section and comb her hair, ivory kit box, no text | "Medium close-up … A hairdresser's hand in a thin black glove gently lifts and combs one section of her hair … small neat kit in plain ivory packaging with a thin gold line, no text …" | Chapter 3; `Layla/layla_3_week2_home_visit.mp4` |
| 5 Nov 2026 | Gemini Omni 1.2 Flash, run by Claude Code | Scene 5, week 12: v1 rejected (screen counted 0 to 100, black bars); v2 has a blank ivory screen with a rising gold line | "Close-up … The phone screen is a plain soft ivory glow with a thin gold line slowly rising, no numbers, no letters, no text at all …" | Chapter 6; `Layla/layla_5_week12_rescan.mp4`; score overlay goes on the screen |
| 5 Nov 2026 | Claude Code (cloud session) | Script: visit 2 moved from week 8 to week 10 (8 weeks after visit 1, as in the prototype), "Visit 1 of 2 / 2 of 2" on screen, "twice" in ch. 1, week-12 scan at home; score chart points changed to reach 66 at week 10; `03_score_counter_v2.mp4` uploaded | "We are running a 12 weeks story, but she should be visited only 1 or 2 times in this period. Should we make something longer?" | Script and score graphic |

## Layla scene prompts (full text in `layla-prompts.md`)

Video tool and the person who runs each prompt: **to fill in** when the clips are made.

| # | Beat | Tool used | Run by | Clip file |
|---|---|---|---|---|
| 1 | Week 0, phone scan | Gemini Omni 1.2 Flash | Claude Code (for Ariel) | `layla_1_week0_scan.mp4` |
| 2 | Week 1, booking confirmation | Gemini Omni 1.2 Flash | Claude Code (for Ariel) | `layla_2_week1_booking.mp4` |
| 3 | Week 2, home visit, partner salon | Gemini Omni 1.2 Flash (reworded prompt) | Claude Code (for Ariel) | `layla_3_week2_home_visit.mp4` |
| 4 | Week 8, brushing by the window | Gemini Omni 1.2 Flash | Claude Code (for Ariel) | `layla_4_week8_brushing_v2.mp4` (v1 rejected) |
| 5 | Week 12, score rising | Gemini Omni 1.2 Flash (v2) | Claude Code (for Ariel) | `layla_5_week12_rescan.mp4` |

## To add later
- Graphics renders (Step 2 and Step 5) with the `render.py` version used.
- Agent Underlord edits (Step 6): each instruction and what it changed.
