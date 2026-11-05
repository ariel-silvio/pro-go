"""Convert the @fontsource woff2 files (installed by `npm ci`) to TTF for render.py. Run from the repo root."""
from pathlib import Path
from fontTools.ttLib import TTFont
src, out = Path('node_modules/@fontsource'), Path('video/fonts')
out.mkdir(parents=True, exist_ok=True)
for woff, ttf in [('bodoni-moda/files/bodoni-moda-latin-500-normal.woff2', 'BodoniModa-500.ttf'),
                  ('jost/files/jost-latin-400-normal.woff2', 'Jost-400.ttf'),
                  ('jost/files/jost-latin-500-normal.woff2', 'Jost-500.ttf')]:
    f = TTFont(src / woff); f.flavor = None; f.save(out / ttf); print('wrote', out / ttf)
