# Nowe filmy z Dropboxa NETIM (10.2026): „16 lat i 9 miesięcy” (instruktorka mówi) i reklamy z drona Jaśka (6/10 s, bez dźwięku).
# Wyjście: kurs-16-lat.html (strona kat. B), glowna-reklama.html (strona główna).
import re
from build import BASE, FORM, PLAY, ARROW, COMMON_CSS, prep, at, ins

CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SOUND = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor"/><path d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

CSS = r'''
/* pionowy film z dźwiękiem, gra po kliknięciu */
.adjvp{position:relative;display:block;width:100%;aspect-ratio:9/16;border-radius:22px;overflow:hidden;background:#141414;box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 34px 70px -34px rgba(20,20,20,.75)}
.adjvp video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.adjvp__go{position:absolute!important;inset:0;z-index:2;display:block!important;width:100%!important;height:100%!important;background:linear-gradient(180deg,rgba(20,20,20,0) 50%,rgba(20,20,20,.75) 100%)!important}
.adjvp__go .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:72px;height:72px}
.adjvp__go .adjv-play svg{width:28px;height:28px}
.adjvp__cap{position:absolute;left:16px;right:16px;bottom:16px;color:#fff;text-align:left;display:flex;align-items:center;gap:8px;font:600 14px/1.2 "Work Sans",sans-serif}
.adjvp__cap svg{width:18px;height:18px;flex:0 0 18px}
@media (hover:hover) and (pointer:fine){.adjvp__go:hover .adjv-play{transform:translate(-50%,-50%) scale(1.08)}}
.adjvp__go:active .adjv-play{transform:translate(-50%,-50%) scale(.94)}
.adjvp.is-playing .adjvp__go{display:none!important}

/* kat. B: 16 lat i 9 miesięcy */
.adj16{margin:48px 0;padding:40px;border-radius:24px;background:#f4f4f4}
.adj16__in{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);gap:48px;align-items:center}
.adj16 h2{margin:0 0 16px!important;text-align:left!important;font-size:clamp(26px,2.6vw,36px)!important;line-height:1.12!important}
.adj16__lead{padding:0!important;text-align:left!important;margin:0 0 22px!important;font:400 17px/1.6 "Roboto",sans-serif;color:rgba(31,31,31,.82);max-width:46ch}
.adj16__list{display:grid;gap:12px;margin:0 0 28px!important}
.adj16__list li{display:grid!important;grid-template-columns:28px 1fr;gap:12px;align-items:start;font:500 16px/1.45 "Roboto",sans-serif;color:#1f1f1f}
.adj16__list svg{width:28px;height:28px;padding:5px;border-radius:50%;background:var(--adj-brand);color:#141414}
@media (max-width:820px){.adj16{padding:24px 16px;margin:32px 0;border-radius:16px}.adj16__in{grid-template-columns:1fr;gap:24px}.adj16__media{max-width:300px;width:100%;margin:0 auto}}

/* strona główna: zapętlona reklama z drona */
.adjrk{padding:56px 16px;background:#1f1f1f;color:#fff;overflow:hidden}
.adjrk__in{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:clamp(32px,6vw,96px);align-items:center}
.adjrk h2{color:#fff!important;text-align:left!important;margin:0 0 16px!important;font-size:clamp(30px,3.6vw,48px)!important;line-height:1.06!important;max-width:16ch}
.adjrk__lead{padding:0!important;text-align:left!important;margin:0 0 28px!important;font:400 18px/1.6 "Roboto",sans-serif;color:rgba(255,255,255,.82);max-width:44ch}
.adjrk__cta{display:flex;flex-wrap:wrap;gap:12px}
.adjrk__ph{position:relative;width:300px;aspect-ratio:9/16;border-radius:36px;padding:10px;background:#0b0b0b;box-shadow:0 0 0 2px #333,0 40px 80px -30px rgba(0,0,0,.9);transform:rotate(3deg)}
.adjrk__ph video,.adjrk__ph img{width:100%;height:100%;object-fit:cover;border-radius:27px;display:block}
.adjrk__sw{position:absolute;left:50%;bottom:-56px;transform:translateX(-50%) rotate(-3deg);display:flex;gap:8px}
.adjrk__sw button{white-space:nowrap;min-width:44px;height:36px!important;padding:0 12px!important;border-radius:999px!important;background:rgba(255,255,255,.12)!important;color:#fff!important;font:600 13px/1 "Work Sans",sans-serif!important;transition:background-color .2s var(--adj-out),transform .15s var(--adj-out)}
.adjrk__sw button[aria-pressed="true"]{background:var(--adj-brand)!important;color:#141414!important}
.adjrk__sw button:active{transform:scale(.96)}
@media (max-width:820px){.adjrk{padding:40px 16px 88px}.adjrk__in{grid-template-columns:1fr}.adjrk__ph{width:min(260px,72vw);margin:0 auto;transform:none}.adjrk__sw{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.adjrk__ph{transform:none}}
'''

JS = r'''
(function(){
  // pionowy film z dźwiękiem: start po kliknięciu, zatrzymanie innych
  document.querySelectorAll('.adjvp').forEach(function(box){
    var v=box.querySelector('video'), go=box.querySelector('.adjvp__go');
    go.addEventListener('click',function(){ document.querySelectorAll('.adjvp video').forEach(function(o){ if(o!==v) o.pause() });
      box.classList.add('is-playing'); v.controls=true; v.muted=false; v.play(); });
  });
  // reklama: autoodtwarzanie bez dźwięku tylko gdy widoczna, bez ruchu przy ograniczeniu animacji
  var rk=document.querySelector('.adjrk'); if(!rk) return;
  var v=rk.querySelector('video'), still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(!still) new IntersectionObserver(function(es){ es.forEach(function(e){ e.isIntersecting ? v.play().catch(function(){}) : v.pause() }) },{threshold:.35}).observe(v);
  rk.querySelectorAll('.adjrk__sw button').forEach(function(b){ b.addEventListener('click',function(){
    rk.querySelectorAll('.adjrk__sw button').forEach(function(x){ x.setAttribute('aria-pressed', x===b) });
    v.poster=b.dataset.poster; v.src=b.dataset.src; if(!still) v.play().catch(function(){}); }); });
})();
'''

def video16():
    return ('<div class="adjvp"><video src="media/16-lat.mp4" poster="media/16-lat.jpg" preload="none" playsinline></video>'
            f'<button class="adjvp__go" type="button" aria-label="Odtwórz film: kurs od 16 lat i 9 miesięcy, 0:16">{PLAY.replace("<svg", "<span class=adjv-play><svg", 1).replace("</svg>", "</svg></span>", 1)}'
            f'<span class="adjvp__cap">{SOUND}Z dźwiękiem · 0:16</span></button></div>')

def kurs16():
    pts = ['Kurs zaczynasz na 3 miesiące przed 17. urodzinami.', 'Teorię i jazdy robisz jeszcze jako szesnastolatek.', 'Potrzebujesz tylko zgody rodzica albo opiekuna.']
    li = ''.join(f'<li>{CHECK}<span>{p}</span></li>' for p in pts)
    return (f'<section class="adjv adj16" aria-labelledby="adj16-h"><div class="adj16__in"><div class="adj16__media">{video16()}</div>'
            f'<div><h2 id="adj16-h">Masz 16 lat i 9 miesięcy? Możesz już zacząć kurs</h2>'
            f'<p class="adj16__lead">Po 17. urodzinach zostaje Ci tylko egzamin. Zobacz w 16 sekund, jak to działa.</p>'
            f'<ul class="adj16__list" role="list">{li}</ul>'
            f'<a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div></div></section>')

def reklama():
    sw = [('10 s A', 'reklama-10a'), ('10 s B', 'reklama-10b'), ('6 s A', 'reklama-6a'), ('6 s B', 'reklama-6b')]
    b = ''.join(f'<button type="button" aria-pressed="{"true" if i==0 else "false"}" data-src="media/{f}.mp4" data-poster="media/{f}.jpg">{n}</button>' for i, (n, f) in enumerate(sw))
    return (f'<section class="adjv adjrk" aria-labelledby="adjrk-h"><div class="adjrk__in"><div>'
            f'<h2 id="adjrk-h">Kurs na prawo jazdy we Wrocławiu</h2>'
            f'<p class="adjrk__lead">Ćwiczysz na skrzyżowaniach, które są na trasach egzaminacyjnych, i zdajesz za pierwszym razem.</p>'
            f'<div class="adjrk__cta"><a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div></div>'
            f'<div class="adjrk__ph"><video src="media/reklama-10a.mp4" poster="media/reklama-10a.jpg" muted loop playsinline preload="metadata" aria-label="Film: kurs na prawo jazdy we Wrocławiu"></video>'
            f'<div class="adjrk__sw" role="group" aria-label="Wersja reklamy (tylko podgląd)">{b}</div></div></div></section>')

def page(src, out, where, html):
    s = prep((BASE / src).read_text(encoding='utf-8'))
    s = ins(s, where(s), html)
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{COMMON_CSS}{CSS}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', f'<script>{JS}</script>\n</body>', 1)
    (BASE / out).write_text(s, encoding='utf-8')

if __name__ == '__main__':
    page('_base.html', 'kurs-16-lat.html',
         lambda s: s.rfind('<div class="wp-block-columns', 0, at(s, 'Wymagania na kurs prawa jazdy kat. B')), kurs16())
    page('_home_base.html', 'glowna-reklama.html',
         lambda s: s.rfind('<section', 0, at(s, 'Skuteczność, doświadczenie')), reklama())
    print('ok')
