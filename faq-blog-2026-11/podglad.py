"""Wstrzykuje 03_blok-faq.html do zapisanej kopii żywego wpisu -> podglad-wpis-310.html (tylko lokalnie)."""
from pathlib import Path
h = Path("zrodla/post-310-live.html").read_text(encoding="utf-8")
blok = Path("03_blok-faq.html").read_text(encoding="utf-8").replace("<!-- wp:html -->", "").replace("<!-- /wp:html -->", "")
anchor = '</div></div><div class="post-sidebar-excerpts">'
assert h.count(anchor) == 1
h = h.replace(anchor, blok + anchor).replace("<head>", '<head><base href="https://www.naukajazdy.wroc.pl/">', 1)
Path("podglad-wpis-310.html").write_text(h, encoding="utf-8")
print("podglad-wpis-310.html")
