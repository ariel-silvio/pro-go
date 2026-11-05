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

## Layla scene prompts (full text in `layla-prompts.md`)

Video tool and the person who runs each prompt: **to fill in** when the clips are made.

| # | Beat | Tool used | Run by | Clip file |
|---|---|---|---|---|
| 1 | Week 0, phone scan | | | |
| 2 | Week 1, booking confirmation | | | |
| 3 | Week 2, home visit, partner salon | | | |
| 4 | Week 8, brushing by the window | | | |
| 5 | Week 12, score rising | | | |

## To add later
- Graphics renders (Step 2 and Step 5) with the `render.py` version used.
- Agent Underlord edits (Step 6): each instruction and what it changed.
