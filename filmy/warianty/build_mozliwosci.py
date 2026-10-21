# Nowe filmy z Dropboxa w nowych miejscach stron ADJ (bez powtarzania wcześniejszych wariantów).
# Wyjście: nowe-baner.html, nowe-karta.html, nowe-intro.html, nowe-formularz.html
import re
from build import BASE, prep, at, ins
from build_nowe import CSS as NCSS, JS as NJS, PLAYB

AD = ('media/reklama-10a.mp4', 'media/reklama-10a.jpg')
AD2 = ('media/reklama-6a.mp4', 'media/reklama-6a.jpg')
TALK = ('media/16-lat.mp4', 'media/16-lat.jpg')

CSS = r'''
/* 1. slajd z filmem w banerze strony głównej */
.adjs-slide{position:relative;overflow:hidden;background:#141414}
.adjs-bg{position:absolute;inset:-40px;background:var(--bg) center/cover;filter:blur(30px) brightness(.5);transform:scale(1.1)}
.adjs-vid{position:absolute;top:0;bottom:0;left:22%;height:100%!important;width:auto!important;max-width:none!important;aspect-ratio:9/16;object-fit:cover;box-shadow:0 0 60px rgba(0,0,0,.5)}
@media (max-width:900px){.adjs-vid{left:50%;transform:translateX(-50%)}}
/* 2. karta „Skuteczność” z filmem w tle */
.adv-card.adjc{position:relative;overflow:hidden;isolation:isolate}
.adjc video{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;z-index:-2}
.adjc::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(254,169,0,.55) 0%,rgba(254,169,0,.92) 62%)}
/* 3. intro strony głównej z filmem obok tekstu */
.adji{display:grid;grid-template-columns:minmax(0,1fr) 220px;gap:56px;align-items:center;max-width:1100px;margin:0 auto;padding:8px 30px 24px}
.adji h1,.adji p{text-align:left!important}.adji .underline-long{margin-left:0!important}
.adji .adjn-vid{box-shadow:0 0 14px 4px rgba(66,66,66,.2);border:0}
@media (max-width:820px){.adji{grid-template-columns:1fr;gap:24px;padding:8px 16px 24px}.adji__m{width:min(240px,70vw);margin:0 auto}}
/* 4. formularz zapisów: film nad formularzem */
.adjf{max-width:732px;margin:28px auto 0;padding:0 30px}
.adjf__card{display:grid;grid-template-columns:96px minmax(0,1fr) auto;gap:24px;align-items:center;padding:16px;background:#fff;border:1px solid #e5e5e5;border-radius:14px}
.adjf__th{position:relative;display:block!important;width:96px!important;aspect-ratio:9/16;border-radius:10px!important;overflow:hidden;background:#1a1a1a}
.adjf__th img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover}
.adjf__th .adjn-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:44px;height:44px}
.adjf__th .adjn-play svg{width:16px;height:16px}
.adjf__t{font:700 18px/1.3 "Work Sans",sans-serif;color:#1a1a1a}
.adjf__d{margin:6px 0 0!important;font:400 15px/1.5 "Work Sans",sans-serif;color:#555}
.adjf__b{display:inline-flex!important;align-items:center;gap:8px;min-height:44px;padding:0 18px!important;border-radius:6px!important;background:#FEA900!important;color:#fff!important;font:600 15px/1 "Work Sans",sans-serif!important;white-space:nowrap}
.adjf__b:hover{background:#e59800!important}.adjf__b:active{transform:scale(.97)}
@media (max-width:700px){.adjf{padding:0 16px}.adjf__card{grid-template-columns:88px minmax(0,1fr);gap:14px}.adjf__th{width:88px!important}.adjf__b{grid-column:1/-1;justify-content:center}}
'''

JS = r'''
(function(){
  document.querySelectorAll('.adjf__open').forEach(function(b){ b.addEventListener('click',function(e){ e.preventDefault();
    var t=document.createElement('button'); t.className='adjnf__c'; t.dataset.kind='mp4'; t.dataset.src=b.dataset.src; t.dataset.title='Film'; t.style.display='none';
    document.body.appendChild(t); t.click(); t.remove(); }); });
  // wideo w pętli startuje także w slajdach karuzeli
  document.querySelectorAll('.adjs-vid,.adjc video').forEach(function(v){ v.muted=true; var p=v.play(); if(p) p.catch(function(){}); });
})();
'''

def page(src, out, edit):
    s = prep((BASE / src).read_text(encoding='utf-8'))
    s = edit(s)
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{NCSS}{CSS}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', f'<script>{NJS}{JS}</script>\n</body>', 1)
    (BASE / out).write_text(s, encoding='utf-8')

def vid(src, poster, cls=''):
    return f'<video class="{cls}" src="{src}" poster="{poster}" muted loop autoplay playsinline aria-hidden="true"></video>'

def baner(s):
    slide = ('<div class="swiper-slide adjs-slide">'
             f'<div class="adjs-bg" style="--bg:url({AD[1]})"></div>{vid(*AD, "adjs-vid")}'
             '<div class="content-wrapper right center"><h2>Kurs prawa jazdy we Wrocławiu</h2>'
             '<p>Jeździsz po trasach, na których zdajesz egzamin</p>'
             '<a href="https://www.naukajazdy.wroc.pl/kursy/prawo-jazdy-kat-b/" class="inside-link-slider-btn">Zobacz kurs kat. B</a></div></div>')
    i = at(s, '<div class="swiper-wrapper">') + len('<div class="swiper-wrapper">')
    return s[:i] + slide + s[i:]

def karta(s):
    i = at(s, '<a class="adv-card orange" href="#vr">')
    s = s[:i] + '<a class="adv-card orange adjc" href="#vr">' + vid(*AD2) + s[i + len('<a class="adv-card orange" href="#vr">'):]
    return s

def intro(s):
    a = at(s, '<section class="main-info container">') + len('<section class="main-info container">')
    e = at(s, 'class="read-more-link">', a); e = s.find('</a>', e) + 4
    inner = s[a:e]
    box = ('<div class="adjn-vid" data-click><video src="' + TALK[0] + '" poster="' + TALK[1] + '" preload="none" playsinline></video>'
           f'<button class="adjn-vid__go" type="button" aria-label="Odtwórz film">{PLAYB}</button></div>')
    return s[:a] + f'<div class="adji"><div>{inner}</div><div class="adji__m">{box}</div></div>' + s[e:]

def formularz(s):
    card = ('<div class="adjn adjf"><div class="adjf__card">'
            f'<button class="adjf__th adjf__open" type="button" data-src="{TALK[0]}" aria-label="Odtwórz film"><img src="{TALK[1]}" alt="">{PLAYB}</button>'
            '<div><div class="adjf__t">Zanim wypełnisz formularz</div><p class="adjf__d">Instruktorka ADJ w 16 sekund mówi, od kiedy możesz zacząć kurs i czego potrzebujesz.</p></div>'
            f'<button class="adjf__b adjf__open" type="button" data-src="{TALK[0]}">Obejrzyj film</button></div></div>')
    return ins(s, at(s, '<form id="formularz-zapisy"'), card)

if __name__ == '__main__':
    page('_home_base.html', 'nowe-baner.html', baner)
    page('_home_base.html', 'nowe-karta.html', karta)
    page('_home_base.html', 'nowe-intro.html', intro)
    page('_form_base.html', 'nowe-formularz.html', formularz)
    print('ok')
