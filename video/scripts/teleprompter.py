"""Build the teleprompter page from script.md. Usage (from video/): python3 scripts/teleprompter.py
Writes video/teleprompter.html (all six spoken parts, [LENS] markers kept)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
t = open(os.path.join(ROOT, "script.md"), encoding="utf-8").read()
WEEKS = ["Week 0", "Week 1", "Week 2", "Week 4", "Week 10", "Week 12"]
NAMES = {"SAJA ALOWAYSHIQ": "Saja AlOwayshiq", "ARIEL DE SILVIO": "Ariel De Silvio"}
parts, chunks = [], re.split(r"\*\*([A-Z ]+) · (Chief[^*]+)\*\*[^\n]*\n", t)[1:]
for k in range(0, len(chunks), 3):
    name, role, body = chunks[k], chunks[k + 1].strip(), chunks[k + 2].split("\n---")[0]
    paras, cur = [], []
    for ln in body.splitlines():
        if ln.startswith("> ") and ln.strip() != ">": cur.append(ln[2:].strip())
        elif ln.strip() == ">" and cur: paras.append(" ".join(cur)); cur = []
    if cur: paras.append(" ".join(cur))
    paras = [p for p in (re.sub(r"\*\(Music[^)]*\)\*", "", p).strip() for p in paras) if p]
    parts.append({"name": NAMES.get(name, name.title()), "role": role, "week": WEEKS[len(parts)], "paras": paras})
html = open(os.path.join(HERE, "teleprompter_template.html"), encoding="utf-8").read()
html = html.replace("__PARTS__", json.dumps(parts, ensure_ascii=False))
open(os.path.join(ROOT, "teleprompter.html"), "w", encoding="utf-8").write(html)
print("wrote teleprompter.html with", len(parts), "parts")
