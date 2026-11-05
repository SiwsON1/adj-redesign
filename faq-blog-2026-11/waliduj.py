"""Walidacja 03_blok-faq.html: składnia JSON-LD, zgodność z treścią widoczną, reguły treści."""
import html, json, re, sys
h = open("03_blok-faq.html", encoding="utf-8").read()
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))
assert ld["@type"] == "FAQPage"
vis = re.findall(r"<summary>(.*?)<svg.*?</summary><p class=\"ans\">(.*?)</p>", h, re.S)
assert len(vis) == len(ld["mainEntity"]), "liczba pytań się nie zgadza"
bledy = []
for (q, a), e in zip(vis, ld["mainEntity"]):
    qv, av = html.unescape(q), html.unescape(re.sub(r"<[^>]+>", "", a))
    if qv != e["name"]: bledy.append(f"pytanie różne: {qv}")
    if av != e["acceptedAnswer"]["text"]: bledy.append(f"odpowiedź różna: {qv}")
    for zle, opis in [("—", "em-dash"), ("–", "półpauza"), (" zł", "kwota"), ("WORD", "WORD zamiast DORD")]:
        if zle in av or zle in qv: bledy.append(f"{opis}: {qv}")
    n = len(av.split())
    if n > 65: bledy.append(f"{n} słów: {qv}")
    if not re.search(r"[ąćęłńóśźż]", av): bledy.append(f"brak polskich znaków: {qv}")
print(f"JSON-LD OK, {len(vis)} pytań"); print("\n".join(bledy) or "reguły treści: OK")
sys.exit(1 if bledy else 0)
