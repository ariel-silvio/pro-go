# M4 video production ("12 weeks with Layla")

Production files for Team D's 8-minute M4 video. The human editor does the final cut in Descript.

- Descript project: https://web.descript.com/78aea752-d5b8-476a-9b27-9ca7ecdb292a
- `layla-prompts.md`: five scene prompts for Veo, Runway or Kling (no faces).
- `ai-log.md`: AI disclosure log for the video.
- `scripts/film_prototype.cjs`: films the prototype at 390 × 844 (deviceScaleFactor 2), JPEG q92 frames.
- `scripts/make_fonts.py`: builds `fonts/*.ttf` from @fontsource (Bodoni Moda 500, Jost 400/500, SIL OFL 1.1). The Latin subset has no "→" glyph: draw arrows as shapes.

Setup: `npm ci && pip install pillow fonttools brotli && python3 video/scripts/make_fonts.py`
Film: `npm run build && npx vite preview --port 4173` then `node video/scripts/film_prototype.cjs http://localhost:4173/pro-go/ <outDir> [--stills]`
