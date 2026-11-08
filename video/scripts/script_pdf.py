"""Build a branded PDF of the shooting script (Team D Brand Kit v2).

Usage (from video/):  python3 scripts/script_pdf.py out/pdf/script.html
Then:                 node scripts/print_pdf.cjs out/pdf/script.html out/pdf/12-weeks-with-Layla-script.pdf
Stills for the storyboard are read from out/pdf/*.jpg (frames of the rendered clips).
The L'Oréal logo is NOT drawn: the cover uses the kit's text label, as on the video slate.
"""
import os, re, sys, html
import markdown

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                       # video/
FONTS = os.path.join(os.path.dirname(ROOT), "node_modules", "@fontsource")

STILLS = {  # section keyword -> (left still, right still or None, caption)
    "COLD OPEN": ("cold_a", "cold_title", "Morning: the mirror, then the title on the sky"),
    "CHAPTER 1": ("p1", None, "App panel: Hair Health Index 58"),
    "CHAPTER 2": ("layla_2", "p3", "The booking · message from her salon"),
    "CHAPTER 3": ("layla_3", None, "Visit 1 of 2 · her own colourist at home"),
    "CHAPTER 4": ("ch4_salon", "ch4_climax", "Who wins: the salon, ServiceMarket, then the climax on \"L'Oréal learns\""),
    "CHAPTER 5": ("layla_4", None, "Visit 2 of 2 · week 10"),
    "CHAPTER 6": ("layla_5_app", "ch6_rules", "Week 12 · the app shows 58 → 74 (illustrative), then the rules one at a time"),
    "CLOSE": ("closing", None, "Closing card (rendered)"),
}

def font_face(fam, weight, path):
    return f"@font-face{{font-family:'{fam}';font-weight:{weight};src:url('file://{path}') format('woff2');}}"

CSS = "\n".join([
    font_face("Bodoni Moda", 500, f"{FONTS}/bodoni-moda/files/bodoni-moda-latin-500-normal.woff2"),
    font_face("Jost", 400, f"{FONTS}/jost/files/jost-latin-400-normal.woff2"),
    font_face("Jost", 500, f"{FONTS}/jost/files/jost-latin-500-normal.woff2"),
]) + """
:root{--ink:#111111;--paper:#FFFFFF;--ivory:#F7F3EC;--muted:#5F5A54;--hair:#E3DDD3;--gold:#B08D57;--goldtxt:#8A6A3B;--m4:#1B6B63;--note:#F4EAD8}
@page{size:A4;margin:18mm 17mm 20mm 17mm}
@page cover{margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink);font-family:'Jost',sans-serif;font-size:10.2pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
h1,h2,h3{font-family:'Bodoni Moda',serif;font-weight:500;margin:0}
.label{font-family:'Jost';font-weight:500;text-transform:uppercase;letter-spacing:.22em;font-size:8pt;color:var(--goldtxt)}
em{font-style:normal;color:var(--muted)}
strong{font-weight:500}
a{color:var(--goldtxt)}

/* cover */
.cover{page:cover;height:297mm;background:var(--ink);color:#fff;margin:0;padding:30mm 18mm 16mm;display:flex;flex-direction:column;page-break-after:always;position:relative}
.cover .label{color:var(--gold);letter-spacing:.3em}
.cover h1{font-size:46pt;line-height:1.05;margin-top:16mm}
.cover .rule{width:46mm;height:1.2pt;background:var(--gold);margin:9mm 0 7mm}
.cover .sub{font-size:13pt;color:var(--ivory)}
.cover .meta{margin-top:6mm;color:#cfc8bd;font-size:9.5pt}
.strip{display:flex;gap:2.4mm;margin-top:auto}
.strip img{width:20%;aspect-ratio:16/9;object-fit:cover;display:block}
.team{display:grid;grid-template-columns:1fr 1fr;gap:2mm 8mm;margin-top:10mm;font-size:9pt;color:#e9e3d9}
.team b{font-weight:500;color:#fff}
.team span{display:block;color:var(--gold);font-size:7.5pt;letter-spacing:.16em;text-transform:uppercase}
.disc{margin-top:7mm;font-size:7.5pt;color:#9a938a}

/* body */
.intro p,.intro li{max-width:none}
h2{font-size:21pt;line-height:1.15;margin:0 0 3mm;padding-top:5mm;border-top:3pt solid var(--m4);break-after:avoid}
h2.first{break-before:auto}
h2:not(.first){break-before:page}
h2 + .kicker{margin-top:-1mm}
.kicker{margin:0 0 4mm}
h3{font-size:14pt;margin:6mm 0 2mm}
p{margin:0 0 2.6mm}
figure{margin:0 0 4mm;display:flex;gap:2.4mm;break-inside:avoid}
figure img{height:34mm;width:auto;flex:none;display:block;border:.5pt solid var(--hair)}
figure img.tall{width:30mm;object-fit:cover;object-position:top;background:var(--ivory)}
figure .ph{flex:1;aspect-ratio:16/9;background:var(--ivory);border:.5pt dashed var(--gold);display:flex;align-items:center;justify-content:center;color:var(--goldtxt);font-size:8pt;letter-spacing:.18em;text-transform:uppercase}
figcaption{font-size:7.5pt;color:var(--muted);margin:-2.6mm 0 4mm;letter-spacing:.04em}
p.tag{padding:1.5mm 3mm;margin:0 0 1.5mm;font-size:9.2pt;line-height:1.42;background:var(--ivory);border-left:2pt solid var(--gold);break-inside:avoid}
p.tag strong:first-child{font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--goldtxt);margin-right:1.5mm}
p.speaker{margin:5mm 0 2mm;font-size:9pt;letter-spacing:.14em;text-transform:uppercase;color:var(--goldtxt);break-after:avoid}
p.speaker strong{color:var(--ink);font-family:'Bodoni Moda',serif;text-transform:none;letter-spacing:0;font-size:13pt;display:block}
p.speaker em{display:none}
blockquote{margin:0 0 3mm;padding:.5mm 0 .5mm 5mm;border-left:1.2pt solid var(--gold);font-size:10.4pt;line-height:1.48}
blockquote p{margin:0 0 1.6mm}
blockquote strong{font-size:7.5pt;letter-spacing:.18em;color:var(--m4);font-weight:500;padding:.3mm 1.2mm;border:.6pt solid var(--m4);margin-right:1mm;vertical-align:1pt}
blockquote.onscreen{border-left:none;padding-left:0;font-family:'Bodoni Moda',serif;font-size:14pt;line-height:1.35;background:var(--ink);color:#fff;padding:5mm 6mm}
p.note{font-size:8pt;color:var(--muted);background:var(--note);padding:1.6mm 3mm;margin:0 0 2.4mm;break-inside:avoid}
p.note em{color:var(--muted)}
table{border-collapse:collapse;width:100%;margin:2mm 0 5mm;font-size:8.6pt;break-inside:auto}
th{background:var(--ivory);text-align:left;font-weight:500;letter-spacing:.06em}
th,td{border:.5pt solid var(--hair);padding:1.6mm 2.2mm;vertical-align:top}
tr{break-inside:avoid}
hr{display:none}
ul{margin:0 0 3mm;padding-left:5mm}
li{margin:0 0 1.2mm}
"""

def stills_html(key):
    l, r, cap = STILLS.get(key, (None, None, None))
    if cap is None: return ""
    def img(n):
        if n is None: return '<div class="ph">To render</div>'
        cls = ' class="tall"' if n in ("p1", "p3") else ""
        return f'<img{cls} src="file://{ROOT}/out/pdf/{n}.jpg">'
    imgs = img(l) + (img(r) if r else "")
    return f'<figure>{imgs}</figure><figcaption>{html.escape(cap)}</figcaption>'

def prep(md_text):
    """Markdown fixes: own paragraph for each tagged line, hard breaks inside on-screen text, no strikethrough."""
    out, prev = [], ""
    for ln in md_text.splitlines():
        starts_block = re.match(r"\*\*(PICTURE\.|LEFT\.|SOUND\.|ON SCREEN|CARD|CLOSING CARD)|\*(Cut to|Editor|Check|Visit 2|Facts|Team|Go /|Length)", ln)
        if starts_block and prev.strip() and not prev.startswith(">"): out.append("")
        if ln.startswith("> ") and prev.startswith("> ") and prev.strip() != ">" and ln.strip() != ">":
            out[-1] = out[-1] + "  "
        out.append(ln.replace("~~", "")); prev = ln
    return "\n".join(out)

def build(md_text):
    lines = prep(md_text).splitlines()
    body_md = "\n".join(lines[4:])                     # drop title + meta lines (on the cover)
    h = markdown.markdown(body_md, extensions=["tables"])
    # classify paragraphs
    h = re.sub(r"<p><strong>(PICTURE\.|LEFT\.|SOUND\.|CARD|ON SCREEN[^<]*|CLOSING CARD[^<]*)</strong>",
               lambda m: f'<p class="tag"><strong>{m.group(1).rstrip(".:")}</strong>', h)
    h = re.sub(r'<p><strong>([A-ZÉ \'-]+) · ([^<]+)</strong>( · lower third:.*?)</p>',
               lambda m: f'<p class="speaker">{m.group(2)}<strong>{m.group(1).title()}</strong></p>', h)
    h = re.sub(r"<p><em>", '<p class="note"><em>', h)
    # on-screen text blocks (cold open, closing card) = the blockquote right after an ON SCREEN / CLOSING CARD tag
    h = re.sub(r'(<p class="tag"><strong>(?:ON SCREEN|CLOSING CARD)</strong>[^<]*Bodoni[^<]*</p>\s*)<blockquote>',
               r'\1<blockquote class="onscreen">', h)
    # scene headers: kicker + stills
    first = [True]
    def h2(m):
        title = m.group(1)
        key = next((k for k in STILLS if title.upper().startswith(k)), None)
        parts = [p.strip() for p in html.unescape(title).split("·")]
        cls = ' class="first"' if first[0] else ""
        first[0] = False
        if key:
            kicker = " · ".join(parts[:2]) if title.upper().startswith("CHAPTER") else parts[0]
            name = parts[2] if title.upper().startswith("CHAPTER") and len(parts) > 2 else (parts[1] if len(parts) > 1 else "")
            timing = " · ".join(parts[3:]) if title.upper().startswith("CHAPTER") else " · ".join(parts[1:])
            head = f'<h2{cls}>{html.escape(name or parts[0].title())}</h2>'
            return head + f'<p class="kicker label">{html.escape(kicker)}{" · " + html.escape(timing) if timing else ""}</p>' + stills_html(key)
        return f"<h2{cls}>{title}</h2>"
    h = re.sub(r"<h2>(.*?)</h2>", h2, h)
    return h

def cover():
    team = [("Amjad Saad Bensalamah", "Chief Innovation Officer"), ("Ariel De Silvio", "Chief Technology & AI Officer"),
            ("Qhakazile Mathebula", "Chief Operations Officer"), ("Rebecca Fernandes", "Chief Marketing & Creative Officer"),
            ("Saja AlOwayshiq", "Chief Customer Experience Officer"), ("Ignacio Montero Alcantara", "Chief Financial Officer")]
    t = "".join(f"<div><b>{n}</b><span>{r}</span></div>" for n, r in team)
    strip = "".join(f'<img src="file://{ROOT}/out/pdf/layla_{i}.jpg">' for i in range(1, 6))
    return f"""<section class="cover">
<div class="label">L'ORÉAL GROUPE &nbsp;·&nbsp; TEAM D</div>
<h1>12 weeks<br>with Layla</h1>
<div class="rule"></div>
<div class="sub">PRO•GO &nbsp;·&nbsp; M4 open innovation &nbsp;·&nbsp; Shooting script v3</div>
<div class="meta">8:00 video for the CEO &nbsp;·&nbsp; Partner: ServiceMarket (working assumption) &nbsp;·&nbsp; 8 November 2026</div>
<div class="team">{t}</div>
<div class="strip">{strip}</div>
<div class="disc">Student project for IE Business School, Corporate Entrepreneurship. Not affiliated with or endorsed by L'Oréal or ServiceMarket.
Layla is a fictional composite; her scores are illustrative. Layla images generated with Gemini Omni Flash (Google) and listed in the AI log.</div>
</section>"""

if __name__ == "__main__":
    out = sys.argv[1]
    body = build(open(os.path.join(ROOT, "script.md"), encoding="utf-8").read())
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>12 weeks with Layla · script</title>
<style>{CSS}</style></head><body>{cover()}<main class="intro">{body}</main></body></html>"""
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(doc)
    print("wrote", out)
