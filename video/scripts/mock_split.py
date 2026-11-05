"""Layout mock for the 16:9 split screen: left panel (app or Layla), right speaker, lower third.
Usage: python3 scripts/mock_split.py <left_panel.png> <out.png>   (run from video/)"""
import sys; sys.path.insert(0, '.')
from PIL import Image, ImageDraw
from render import W, H, INK, IVORY, GOLD, GOLD_TXT, MUTED, HAIR, WHITE, font, spaced, SANS, SANS_M

def lower_third(img, name, role_city, x=1040, y=830):
    d = ImageDraw.Draw(img)
    fn, fr = font(SANS_M, 36), font(SANS_M, 20)
    w = max(d.textlength(name, font=fn), sum(d.textlength(c, font=fr) + 5 for c in role_city)) + 64
    d.rectangle([x, y, x + w, y + 104], fill=IVORY)
    d.rectangle([x, y, x + 1, y + 104], fill=GOLD)            # 2 px gold rule on the left
    d.text((x + 32, y + 18), name, font=fn, fill=INK)
    spaced(d, (x + 32, y + 66), role_city, fr, GOLD_TXT, 5)

if __name__ == '__main__':
    img = Image.new('RGB', (W, H), INK)
    img.paste(Image.open(sys.argv[1]).convert('RGB'), (0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([960, 0, W, H], fill=(58, 55, 52))           # speaker placeholder
    d.ellipse([1340, 300, 1540, 500], fill=(84, 80, 76)); d.rectangle([1260, 520, 1620, 1080], fill=(84, 80, 76))
    d.text((1440, 200), "Speaker, centred, looking screen-left", font=font(SANS, 30), fill=(170, 165, 158), anchor="mm")
    d.line([1300, 250, 1120, 250], fill=(170, 165, 158), width=3); d.polygon([(1100, 250), (1124, 238), (1124, 262)], fill=(170, 165, 158))
    lower_third(img, "Ariel", "ROLE  ·  AARHUS")
    img.save(sys.argv[2])
