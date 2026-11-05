#!/usr/bin/env python3
"""Buduje blok FAQ (wp:html) + JSON-LD FAQPage z pliku z treścią.

Użycie: python3 buduj_blok.py 02_faq-tresc.md
Format wejścia:
  ## Nagłówek: <tekst nagłówka sekcji>
  ### P: <pytanie>
  <odpowiedź, może mieć [anchor](https://...)>
Wyjście: 03_blok-faq.html (do wklejenia jako blok HTML na końcu wpisu).
Styl = kopia .adj-loc-faq ze stron dzielnic (tokeny z /prawo-jazdy-wroclaw-krzyki/).
"""
import html, json, re, sys
from pathlib import Path

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "02_faq-tresc.md")
OUT = Path("03_blok-faq.html")

CSS = """.adj-faq{--g:#fea900;--g-dark:#e59800;--g-text:#a65f00;--ink:#373737;--line:#ececec;--white:#fff;--ease:cubic-bezier(.23,1,.32,1);margin:40px 0 8px;color:var(--ink);line-height:1.6}
.adj-faq *{box-sizing:border-box}
.adj-faq-list{border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--white)}
.adj-faq-list details+details{border-top:1px solid var(--line)}
.adj-faq-list summary{list-style:none;cursor:pointer;padding:18px 20px;font-size:16px;font-weight:600;line-height:1.45;color:var(--ink);display:flex;justify-content:space-between;align-items:center;gap:14px;transition:color .18s var(--ease)}
.adj-faq-list summary::-webkit-details-marker{display:none}
.adj-faq-list summary:hover{color:var(--g-text)}
.adj-faq-list summary:focus-visible{outline:3px solid rgb(254 169 0 / .5);outline-offset:-3px;border-radius:14px}
.adj-faq-list summary:active{color:var(--g-text)}
.adj-faq-list summary .chev{flex:0 0 20px;width:20px;height:20px;color:var(--g);transition:transform .25s var(--ease)}
.adj-faq-list details[open] summary .chev{transform:rotate(180deg)}
.adj-faq-list .ans{padding:0 20px 18px;font-size:15px;color:#4b5563;margin:0}
.adj-faq-list .ans a{color:var(--ink);text-decoration:underline;text-underline-offset:2px}
.adj-faq-list .ans a:hover{color:var(--g-text)}
.adj-faq-list .ans a:focus-visible{outline:2px solid var(--g);outline-offset:2px;border-radius:2px}
@media (prefers-reduced-motion:reduce){.adj-faq-list summary,.adj-faq-list summary .chev{transition:none}}"""

CHEV = ('<svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        '<path d="m6 9 6 6 6-6" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"/></svg>')
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def parse(text):
    heading, items, cur = None, [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## Nagłówek:"):
            heading = s.split(":", 1)[1].strip()
        elif s.startswith("### P:"):
            cur = {"q": s.split(":", 1)[1].strip(), "a": []}
            items.append(cur)
        elif s and cur is not None and not s.startswith("#"):
            cur["a"].append(s)
    for it in items:
        it["a"] = " ".join(it["a"])
    return heading, items


def to_html(answer):
    out, pos = [], 0
    for m in LINK.finditer(answer):
        out.append(html.escape(answer[pos:m.start()], quote=False))
        out.append(f'<a href="{html.escape(m.group(2))}">{html.escape(m.group(1), quote=False)}</a>')
        pos = m.end()
    out.append(html.escape(answer[pos:], quote=False))
    return "".join(out)


def to_text(answer):
    return LINK.sub(r"\1", answer)


def build(heading, items):
    details = "\n".join(
        f'<details>\n<summary>{html.escape(it["q"], quote=False)}{CHEV}</summary>'
        f'<p class="ans">{to_html(it["a"])}</p>\n</details>' for it in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": it["q"],
         "acceptedAnswer": {"@type": "Answer", "text": to_text(it["a"])}} for it in items]}
    return (f'<!-- wp:html -->\n<section class="adj-faq" aria-labelledby="adj-faq-h">\n'
            f'<style>{CSS}</style>\n'
            f'<h2 id="adj-faq-h" class="wp-block-heading">{html.escape(heading, quote=False)}</h2>\n'
            f'<div class="adj-faq-list">\n{details}\n</div>\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n'
            f'</section>\n<!-- /wp:html -->\n')


if __name__ == "__main__":
    heading, items = parse(SRC.read_text(encoding="utf-8"))
    assert heading and items, "brak nagłówka albo pytań"
    OUT.write_text(build(heading, items), encoding="utf-8")
    print(f"{OUT}: {len(items)} pytań")
