# M4 video production ("12 weeks with Layla")

Production files for Team D's 8-minute M4 video. The human editor does the final cut in Descript.

- Descript project: https://web.descript.com/78aea752-d5b8-476a-9b27-9ca7ecdb292a
- `layla-prompts.md`: five scene prompts for Veo, Runway or Kling (no faces).
- `ai-log.md`: AI disclosure log for the video.
- `scripts/film_prototype.cjs`: films the prototype at 390 × 844 (deviceScaleFactor 2), JPEG q92 frames.
- `scripts/panel.sh`: phone frames → 960 × 1080 left-half panel (phone on ivory). Layout: 16:9; left half = app or Layla, right half = speaker, looking screen-left.
- `scripts/mock_split.py`: full-frame layout mock with the lower third.
- `scripts/lower_thirds.py`: the six lower thirds (team, roles, order) as transparent PNGs; `--mov KEY` adds a 4 s ProRes 4444 overlay with fades.
- `render.py out/m4 --m4`: six chapter cards, the service diagram (10 s) and the closing card.
- `12-weeks-with-Layla-script.pdf`: branded script. Rebuild: `python3 scripts/script_pdf.py out/pdf/script.html && node scripts/print_pdf.cjs out/pdf/script.html 12-weeks-with-Layla-script.pdf` (stills in `out/pdf/`).
- `scripts/make_fonts.py`: builds `fonts/*.ttf` from @fontsource (Bodoni Moda 500, Jost 400/500, SIL OFL 1.1). The Latin subset has no "→" glyph: draw arrows as shapes.

Setup: `npm ci && pip install pillow fonttools brotli && python3 video/scripts/make_fonts.py`
Film: `npm run build && npx vite preview --port 4173` then `node video/scripts/film_prototype.cjs http://localhost:4173/pro-go/ <outDir> [--stills]`
