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

## Layla scene prompts (full text in `layla-prompts.md`)

Video tool and the person who runs each prompt: **to fill in** when the clips are made.

| # | Beat | Tool used | Run by | Clip file |
|---|---|---|---|---|
| 1 | Week 0, phone scan | | | |
| 2 | Week 1, booking confirmation | | | |
| 3 | Week 2, home visit, partner salon | | | |
| 4 | Week 8, brushing by the window | Gemini Omni 1.2 Flash | Claude Code (for Ariel) | `layla_4_week8_brushing.mp4` |
| 5 | Week 12, score rising | | | |

## To add later
- Graphics renders (Step 2 and Step 5) with the `render.py` version used.
- Agent Underlord edits (Step 6): each instruction and what it changed.
