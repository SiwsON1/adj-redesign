# Generator wariantów filmów na kopii strony kursu kat. B (naukajazdy.wroc.pl).
# Wejście: _base.html (świeży HTML strony, poza repo). Wyjście: v01..v11.html + index.html.
# Runda 2: po krytyce (ocena projektowa, detektor impeccable, research). Wszystkie filmy są 16:9.
import re, pathlib

BASE = pathlib.Path(__file__).parent
SITE = 'https://www.naukajazdy.wroc.pl'
FORM = SITE + '/formularz-zapisow/'
TEL = '575 757 408'
CHANNEL = 'https://www.youtube.com/@akademia_szkolen'

# id, tytuł, czas, numer klatki bez napisów (YouTube maxresN/mqN), krótka nazwa miejsca
V = {
    'promo':   ('ZnJegLxixKQ', 'Jak wygląda kurs w ADJ', '1:03', 3, None),
    'fotel':   ('8H4GNjbGqLw', 'Ustawienie fotela przed jazdą', '5:58', 2, None),
    'swiatla': ('8Fu4ivqowfA', 'Sprawdzenie świateł', '4:48', 2, None),
    'plyny':   ('SUTfnCdub4E', 'Sprawdzenie płynów', '4:09', 2, None),
    'jagodno': ('2108OLdnWyE', 'Skręt w lewo na Rondzie Wolnej Ukrainy', '0:58', 2, 'Jagodno'),
    'pionier': ('PqlwPO7q7zE', 'Zawracanie na Rondzie Pionierów', '0:57', 2, 'Rondo Pionierów'),
    'armii':   ('UPOX1k-j9CU', 'Z Armii Krajowej w stronę Krakowskiej', '0:48', 1, 'Krzyki'),
    'mini':    ('kwx0GJi028g', 'Mini rondo: Centralna i Semaforowa', '0:49', 2, 'Mini rondo'),
    'tory':    ('VLkvy_L9fK0', 'Przejazd przez tory', '0:37', 2, 'Tory'),
    'chinska': ('P3ORAULwYMU', 'Skręt w lewo z Chińskiej w Mościckiego', '0:48', 3, 'Chińska'),
}
CITY = ['jagodno', 'pionier', 'armii', 'mini', 'tory', 'chinska']

def img(k, big=False):
    i, _, _, f, _ = V[k]
    return f'https://i.ytimg.com/vi/{i}/{"maxres" if big else "mq"}{f}.jpg'

def yt(k, group=None):
    g = f' data-group="{group}"' if group else ''
    return f'data-yt="{V[k][0]}" data-title="{V[k][1]}"{g}'

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13m-5-6 6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z" fill="currentColor"/></svg>'

def play(cls=''):
    return f'<span class="adjv-play {cls}">{PLAY}</span>'

# ---------- wspólne ----------
COMMON_CSS = r'''
:root{--adj-navy:#1f1f1f;--adj-navy-d:#1f1f1f;--adj-ink:#141414;--adj-gray:#f4f4f4;--adj-brand:#FEA900;--adj-brand-l:#ffbd33;
--adj-sh-1:0 1px 0 rgba(31,31,31,.05),0 12px 28px -18px rgba(31,31,31,.55);--adj-sh-2:0 1px 0 rgba(31,31,31,.06),0 30px 60px -34px rgba(31,31,31,.7);
--adj-out:cubic-bezier(.23,1,.32,1);--adj-in:cubic-bezier(.4,0,1,1)}
.adjv,.adjv *{box-sizing:border-box}
.adjv{font-family:"Work Sans",sans-serif}
:where(.adjv) button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:pointer;text-transform:none;letter-spacing:normal;box-shadow:none;min-height:0;width:auto;height:auto;border-radius:0}
:where(.adjv) img{max-width:none;margin:0;height:auto}
.adjv ul,.adjv ol{list-style:none!important;margin:0!important;padding:0!important}
.adjv li{list-style:none!important;margin:0!important;padding:0!important}.adjv li::marker{content:none}
.adjv p{margin:0}
.adjv a:focus-visible,.adjv button:focus-visible{outline:3px solid var(--adj-brand);outline-offset:3px}
.adjv ::selection{background:var(--adj-brand);color:var(--adj-ink)}
.adjv-media{position:relative;display:block;aspect-ratio:16/9;overflow:hidden;background:var(--adj-ink)}
.adjv-media>img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;transition:transform .5s var(--adj-out)}
.adjv-play{display:grid;place-items:center;width:56px;height:56px;border-radius:50%;background:var(--adj-brand);box-shadow:0 10px 24px -10px rgba(20,20,20,.7);transition:transform .15s var(--adj-out)}
.adjv-play svg{width:22px;height:22px;fill:var(--adj-ink);margin-left:3px}
.adjv-media .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
.adjv-dur{position:absolute;right:10px;bottom:10px;padding:4px 8px;border-radius:6px;background:rgba(20,20,20,.82);color:#fff;font:600 12px/1 "Work Sans",sans-serif;font-variant-numeric:tabular-nums}
@media (hover:hover) and (pointer:fine){[data-yt]:hover .adjv-media>img{transform:scale(1.04)}[data-yt]:hover .adjv-media .adjv-play{transform:translate(-50%,-50%) scale(1.08)}[data-yt]:hover>.adjv-play{transform:scale(1.08)}}
[data-yt]:active .adjv-media .adjv-play{transform:translate(-50%,-50%) scale(.94)}
[data-yt]:active>.adjv-play{transform:scale(.94)}
.adjv-btn{display:inline-flex!important;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 22px!important;border-radius:999px!important;font:700 16px/1 "Work Sans",sans-serif!important;text-decoration:none!important;transition:transform .15s var(--adj-out),background-color .2s var(--adj-out)}
.adjv-btn svg{width:18px;height:18px}
.adjv-btn--primary{background:var(--adj-brand)!important;color:var(--adj-ink)!important;box-shadow:var(--adj-sh-1)}
.adjv-btn--ghost{background:transparent!important;color:#fff!important;box-shadow:inset 0 0 0 2px rgba(255,255,255,.75)!important}
.adjv-btn--ghost .adjv-play{width:30px;height:30px;box-shadow:none}.adjv-btn--ghost .adjv-play svg{width:12px;height:12px;margin-left:2px}
@media (hover:hover) and (pointer:fine){.adjv-btn--primary:hover{background:var(--adj-brand-l)!important}.adjv-btn--ghost:hover{background:rgba(255,255,255,.1)!important}}
.adjv-btn:active{transform:scale(.97)}
/* okno z filmem */
.adjv-modal{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;padding:72px 16px 16px;background:rgba(20,20,20,.9);opacity:0;transition:opacity .22s var(--adj-out)}
.adjv-modal.is-open{opacity:1}.adjv-modal.is-closing{opacity:0;transition:opacity .15s var(--adj-in)}
.adjv-modal__box{position:relative;width:min(1100px,100%);transform:translateY(8px) scale(.98);transition:transform .22s var(--adj-out)}
.adjv-modal.is-open .adjv-modal__box{transform:none}
.adjv-modal__frame{position:relative;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#000;box-shadow:0 40px 80px -30px rgba(0,0,0,.8)}
.adjv-modal iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.adjv-modal__bar{position:absolute;left:0;right:0;bottom:calc(100% + 12px);display:flex;align-items:center;gap:12px;color:#fff}
.adjv-modal__t{flex:1;min-width:0;font:600 16px/1.3 "Work Sans",sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.adjv-modal__b{width:44px;height:44px;flex:0 0 44px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.12)!important;color:#fff!important;border:0;cursor:pointer;transition:transform .15s var(--adj-out),background-color .2s var(--adj-out)}
.adjv-modal__b svg{width:20px;height:20px}
.adjv-modal__b:hover{background:rgba(255,255,255,.22)!important}.adjv-modal__b:active{transform:scale(.94)}
.adjv-modal__b:focus-visible{outline:3px solid var(--adj-brand);outline-offset:2px}
.adjv-modal__b[hidden]{display:none}
/* pasek podglądu wariantów (tylko podgląd) */
.adjv-bar{position:fixed;left:16px;bottom:16px;z-index:2147482000;display:flex;align-items:center;gap:6px;background:var(--adj-ink);color:#fff;border-radius:999px;padding:6px 6px 6px 16px;font:500 13px/1.2 "Work Sans",sans-serif;box-shadow:var(--adj-sh-2)}
.adjv-bar b{color:var(--adj-brand);font-weight:700;margin-right:6px}
.adjv-bar a{color:#fff!important;text-decoration:none!important;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.1)}
.adjv-bar a svg{width:16px;height:16px}
.adjv-bar a:hover{background:rgba(255,255,255,.22)}
@media (max-width:600px){.adjv-bar{left:8px;right:8px;bottom:8px;justify-content:space-between}.adjv-bar span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
@media (prefers-reduced-motion:reduce){.adjv *,.adjv-modal,.adjv-modal__box{transition:opacity .15s linear!important;animation:none!important}}
'''

COMMON_JS = r'''
(function(){
  var X='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>';
  var L='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var R='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var Q='?autoplay=1&rel=0&playsinline=1&cc_load_policy=1&cc_lang_pref=pl&hl=pl';
  function src(id){return 'https://www.youtube-nocookie.com/embed/'+id+Q}
  var warmed=false; function warm(){ if(warmed) return; warmed=true;
    ['https://www.youtube-nocookie.com','https://i.ytimg.com','https://www.google.com'].forEach(function(h){var l=document.createElement('link');l.rel='preconnect';l.href=h;document.head.appendChild(l)}); }
  document.addEventListener('pointerover',function(e){ if(e.target.closest&&e.target.closest('[data-yt]')) warm(); },{passive:true});
  document.addEventListener('focusin',function(e){ if(e.target.closest&&e.target.closest('[data-yt]')) warm(); });
  var y=0;
  function lock(){ y=scrollY; var b=document.body.style; b.position='fixed'; b.top=-y+'px'; b.left='0'; b.right='0'; b.width='100%'; }
  function unlock(){ var b=document.body.style, h=document.documentElement.style, sb=h.scrollBehavior; b.position=b.top=b.left=b.right=b.width=''; h.scrollBehavior='auto'; scrollTo(0,y); requestAnimationFrame(function(){ scrollTo(0,y); h.scrollBehavior=sb; }); }
  function open(trigger){
    var list=[trigger], i=0, g=trigger.dataset.group;
    if(g){ list=[].slice.call(document.querySelectorAll('[data-group="'+g+'"]')); i=list.indexOf(trigger); }
    var m=document.createElement('div'); m.className='adjv-modal'; m.setAttribute('role','dialog'); m.setAttribute('aria-modal','true'); m.setAttribute('aria-label','Film');
    m.innerHTML='<div class="adjv-modal__box"><div class="adjv-modal__bar"><span class="adjv-modal__t"></span>'+
      '<button class="adjv-modal__b" data-prev type="button" aria-label="Poprzedni film">'+L+'</button><button class="adjv-modal__b" data-next type="button" aria-label="Następny film">'+R+'</button>'+
      '<button class="adjv-modal__b" data-close type="button" aria-label="Zamknij film">'+X+'</button></div><div class="adjv-modal__frame"></div></div>';
    var frame=m.querySelector('.adjv-modal__frame'), t=m.querySelector('.adjv-modal__t'), pv=m.querySelector('[data-prev]'), nx=m.querySelector('[data-next]');
    function show(k){ i=(k+list.length)%list.length; var el=list[i];
      frame.innerHTML='<iframe src="'+src(el.dataset.yt)+'" title="'+(el.dataset.title||'Film ADJ')+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
      t.textContent=el.dataset.title||''; pv.hidden=nx.hidden=list.length<2; }
    show(i);
    var last=document.activeElement; document.body.appendChild(m); lock();
    requestAnimationFrame(function(){m.classList.add('is-open')}); m.querySelector('[data-close]').focus();
    function close(){ m.classList.add('is-closing'); document.removeEventListener('keydown',key); setTimeout(function(){ m.remove(); unlock(); if(last&&last.focus) last.focus({preventScroll:true}); },150); }
    function key(e){
      if(e.key==='Escape') close();
      else if(e.key==='ArrowRight'&&list.length>1) show(i+1);
      else if(e.key==='ArrowLeft'&&list.length>1) show(i-1);
      else if(e.key==='Tab'){ var f=[].slice.call(m.querySelectorAll('button:not([hidden]),iframe')); var a=f[0], z=f[f.length-1];
        if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()} else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()} }
    }
    m.addEventListener('click',function(e){ if(e.target===m||e.target.closest('[data-close]')) close(); else if(e.target.closest('[data-prev]')) show(i-1); else if(e.target.closest('[data-next]')) show(i+1); });
    document.addEventListener('keydown',key);
  }
  function inline(t){
    var box=t.closest('[data-inline-box]'); box.style.height=box.offsetHeight+'px';
    box.classList.add('is-playing');
    var f=document.createElement('iframe'); f.src=src(t.dataset.yt); f.title=t.dataset.title||'Film ADJ';
    f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen=true;
    f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0;z-index:5;border-radius:inherit;background:#000';
    box.appendChild(f); t.remove();
  }
  if(window.top!==window.self){ var st=document.createElement('style'); st.textContent='.adjv-bar{display:none!important}'; document.head.appendChild(st); }
  if(location.hash==='#film') addEventListener('load',function(){ setTimeout(function(){
    var el=document.querySelector('.adjv:not(.adjv-bar)'); if(!el) return; el=el.closest('.kurs-img-wrapper')||el;
    var y=el.getBoundingClientRect().top+scrollY-Math.max(90,(innerHeight-el.offsetHeight)/2);
    document.documentElement.style.scrollBehavior='auto'; scrollTo(0,Math.max(0,y)); },300); });
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-yt]'); if(!t) return; e.preventDefault(); warm();
    var small=matchMedia('(max-width:600px)').matches;
    if(t.hasAttribute('data-inline')||(small&&t.hasAttribute('data-inline-mobile'))) inline(t); else open(t);
  });
})();
'''

def card(k, extra='', group=None, big=False, cap=True):
    i, title, dur, _, place = V[k]
    c = f'<span class="adjv-cap"><strong>{title}</strong></span>' if cap else ''
    return (f'<button class="adjv-card {extra}" type="button" {yt(k, group)} aria-label="Odtwórz film: {title}, {dur}">'
            f'<span class="adjv-media"><img src="{img(k, big)}" alt="" loading="lazy" decoding="async">{play()}<span class="adjv-dur">{dur}</span></span>{c}</button>')

CARD_CSS = r'''
.adjv-card{display:flex!important;flex-direction:column;gap:10px;width:100%!important;text-align:left;color:inherit}
.adjv-card .adjv-media{border-radius:12px;box-shadow:var(--adj-sh-1)}
.adjv-cap strong{display:block;font:600 15px/1.35 "Work Sans",sans-serif}
'''

VARS = []
DESC = {'Film w zdjęciu na górze strony': 'Film o kursie w miejscu zdjęcia na górze strony. Gra od razu na stronie, obok przycisku „Zapisz się”.', 'Przycisk na zdjęciu, film w oknie': 'Zdjęcie zostaje bez zmian, na nim przycisk „Obejrzyj film o kursie”. Film otwiera się w oknie.', 'Sekcja kinowa po krokach kursu': 'Osobna sekcja po krokach kursu: duży odtwarzacz, lista filmów o egzaminie i filmy ze skrzyżowań.', 'Filmy przy krokach kursu': 'Przy krokach kursu (jazdy, egzamin wewnętrzny, egzamin DORD) małe przyciski z filmem do danego kroku.', 'Pas z krótkimi filmami pod zdjęciem': 'Pas z okrągłymi miniaturami filmów pod górą strony, jak historyjki na Instagramie.', 'Zakładki przy opisie egzaminu': 'Zakładki z filmami przy opisie egzaminu praktycznego: obsługa auta, światła, płyny, trasy w mieście.', 'Siatka filmów przed FAQ': 'Siatka filmów przed pytaniami (FAQ): duży film o kursie i trzy filmy o egzaminie.', 'Pas z filmem w połowie strony': 'Szeroki pas z kadrem z filmu i dwoma przyciskami: „Obejrzyj film” i „Zapisz się na kurs”.', 'Pytania z jazd w 60 sekund': 'Lista trudnych skrzyżowań z tras egzaminacyjnych we Wrocławiu, każde z krótkim filmem.'}
def var(name, goal, plus, minus, verdict, css, js, kind):
    VARS.append(dict(desc=DESC.get(name, goal), name=name, goal=goal, plus=plus, minus=minus, verdict=verdict, css=css, js=js, kind=kind))

var('Film w zdjęciu na górze strony',
    'Pierwsze wrażenie: kursant widzi, jak wygląda kurs, zanim przewinie stronę.',
    'Film 1:03 gra w miejscu, obok przycisku „Zapisz się”. Najwięcej odtworzeń, bo jest na górze strony.',
    'Zdjęcie auta zamienia się w miniaturę filmu. Na telefonie hero jest niskie, więc zostaje sam przycisk i czas.',
    'Polecany (część zestawu 10)',
    r'''
.adjv1{position:absolute!important;inset:0;z-index:3;display:block!important;border-radius:inherit}
.adjv1::before{content:"";position:absolute;inset:0;border-radius:inherit;background:linear-gradient(180deg,rgba(20,20,20,0) 45%,rgba(20,20,20,.78) 100%)}
.adjv1 .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:80px;height:80px}
.adjv1 .adjv-play svg{width:30px;height:30px}
.adjv1:active .adjv-play{transform:translate(-50%,-50%) scale(.94)}
@media (hover:hover) and (pointer:fine){.adjv1:hover .adjv-play{transform:translate(-50%,-50%) scale(1.08)}}
.adjv1__cap{position:absolute;left:24px;right:24px;bottom:22px;color:#fff;text-align:left;display:flex;align-items:baseline;gap:12px}
.adjv1__cap strong{font:700 clamp(18px,1.7vw,22px)/1.2 "Work Sans",sans-serif}
.adjv1__cap span{font:600 14px/1 "Work Sans",sans-serif;color:rgba(255,255,255,.8);font-variant-numeric:tabular-nums}
.kurs-img-wrapper.is-playing .kurs-info-tags{display:none!important}
@media (max-width:600px){.adjv1::before{background:rgba(20,20,20,.18)}.adjv1 .adjv-play{width:64px;height:64px}.adjv1 .adjv-play svg{width:24px;height:24px}
.adjv1__cap{left:auto;right:10px;top:10px;bottom:auto;background:rgba(20,20,20,.82);padding:6px 12px;border-radius:999px;white-space:nowrap}
.adjv1__cap strong{font-size:13px}.adjv1__cap span{font-size:13px}}
''', '', 'hero1')

var('Przycisk na zdjęciu, film w oknie',
    'Najlżejsza zmiana: zdjęcie zostaje, film jest dla chętnych.',
    'Zdjęcie hero bez zmian, przycisk z czasem filmu. Na telefonie film gra w miejscu, bo okno byłoby za małe.',
    'Przycisk łatwiej przeoczyć niż duży play z wariantu 1.',
    'Do rozważenia',
    r'''
.adjv2{position:absolute;left:16px;bottom:16px;z-index:3;display:inline-flex!important;align-items:center;gap:10px;min-height:48px;padding:6px 18px 6px 6px!important;border-radius:999px!important;background:rgba(20,20,20,.88)!important;color:#fff!important;font:600 15px/1 "Work Sans",sans-serif!important;box-shadow:var(--adj-sh-1)!important;transition:transform .15s var(--adj-out),background-color .2s var(--adj-out)}
.adjv2 .adjv-play{width:36px;height:36px;box-shadow:none}.adjv2 .adjv-play svg{width:14px;height:14px;margin-left:2px}
.adjv2 em{font-style:normal;color:rgba(255,255,255,.7);font-weight:500;font-variant-numeric:tabular-nums}
.adjv2:active{transform:scale(.97)}
@media (hover:hover) and (pointer:fine){.adjv2:hover{background:rgba(20,20,20,.97)!important}}
.kurs-img-wrapper.is-playing .kurs-info-tags{display:none!important}
@media (max-width:600px){.adjv2{left:auto;bottom:auto;right:10px;top:10px;min-height:44px;font-size:14px!important}}
''', '', 'hero2')

var('Sekcja kinowa po krokach kursu',
    'Dla osób, które czytają ofertę dokładnie: wszystkie filmy w jednym miejscu, z zapisem obok.',
    'Jedyny wariant z pełną listą filmów i przyciskiem zapisu przy odtwarzaczu.',
    'Duży blok w połowie strony. Wymaga przewinięcia, żeby go zobaczyć.',
    'Do rozważenia',
    r'''
.adjv3{width:100vw;margin:40px calc(50% - 50vw);padding:56px 16px;background:var(--adj-navy);color:#fff}
.adjv3__in{max-width:1180px;margin:0 auto}
.adjv3 h2{color:#fff!important;margin:0 0 28px!important;text-align:left!important}
.adjv3__stage{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:24px;align-items:start}
.adjv3__player{position:relative;aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#000;box-shadow:var(--adj-sh-2)}
.adjv3__player>button{position:absolute!important;inset:0;display:block!important}
.adjv3__player>button .adjv-media{height:100%;aspect-ratio:auto;border-radius:0;box-shadow:none}
.adjv3__player .adjv-play{width:80px;height:80px}.adjv3__player .adjv-play svg{width:30px;height:30px}
.adjv3__side{display:flex;flex-direction:column;gap:10px}
.adjv3__item{display:grid!important;grid-template-columns:112px 1fr;gap:14px;align-items:center;width:100%!important;min-height:76px;padding:8px!important;border-radius:12px!important;text-align:left;background:rgba(255,255,255,.05)!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.08)!important;transition:background-color .2s var(--adj-out),transform .15s var(--adj-out)}
.adjv3__item img{width:112px!important;aspect-ratio:16/9;object-fit:cover;border-radius:8px;display:block}
.adjv3__item strong{display:block;font:600 15px/1.3 "Work Sans",sans-serif}
.adjv3__item small{display:block;margin-top:6px;font:500 13px/1 "Work Sans",sans-serif;color:rgba(255,255,255,.75);font-variant-numeric:tabular-nums}
.adjv3__item[aria-current="true"]{background:rgba(254,169,0,.14)!important;box-shadow:inset 0 0 0 1px rgba(254,169,0,.6)!important}
.adjv3__item[aria-current="true"] small{color:var(--adj-brand)}
.adjv3__item:hover{background:rgba(255,255,255,.1)!important}.adjv3__item:active{transform:scale(.98)}
.adjv3__side .adjv-btn{margin-top:6px;width:100%}
.adjv3__city{margin-top:48px}
.adjv3__city h3{color:#fff!important;margin:0 0 6px!important}
.adjv3__city p{color:rgba(255,255,255,.78);margin:0 0 20px}
.adjv3__grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.adjv3__more{display:inline-flex;align-items:center;gap:8px;margin-top:20px;min-height:44px;color:var(--adj-brand)!important;font:600 15px/1 "Work Sans",sans-serif;text-decoration:none!important}
.adjv3__more svg{width:18px;height:18px;transition:transform .2s var(--adj-out)}.adjv3__more:hover svg{transform:translateX(4px)}
@media (max-width:900px){.adjv3__stage{grid-template-columns:minmax(0,1fr)}.adjv3__grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
''', r'''
(function(){var s=document.querySelector('.adjv3'); if(!s) return; var p=s.querySelector('.adjv3__player');
 s.querySelectorAll('.adjv3__item').forEach(function(b){ b.addEventListener('click',function(){
  s.querySelectorAll('.adjv3__item').forEach(function(x){x.setAttribute('aria-current','false')}); b.setAttribute('aria-current','true');
  p.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1&rel=0&playsinline=1&cc_load_policy=1&cc_lang_pref=pl&hl=pl" title="'+b.dataset.title+'" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>';
 });});})();
''', 'cinema')

var('Filmy przy krokach kursu',
    'Film odpowiada na pytanie z danego kroku: jak wyglądają jazdy, egzamin wewnętrzny, egzamin DORD.',
    'Najbardziej w kontekście, nie konkuruje z przyciskiem zapisu, nie zmienia wyglądu strony.',
    'Mało widoczne dla kogoś, kto nie czyta kroków.',
    'Polecany (część zestawu 10)',
    r'''
.adjv4{display:inline-flex!important;align-items:center;gap:10px;min-height:44px;margin:10px 8px 2px 0!important;padding:4px 16px 4px 4px!important;border-radius:999px!important;background:#fff!important;color:var(--adj-navy)!important;font:600 14px/1.35 "Work Sans",sans-serif!important;text-align:left;box-shadow:inset 0 0 0 1px rgba(31,31,31,.18),var(--adj-sh-1)!important;transition:transform .15s var(--adj-out),box-shadow .2s var(--adj-out)}
.adjv4 .adjv-play{width:36px;height:36px;flex:0 0 36px;box-shadow:none}.adjv4 .adjv-play svg{width:14px;height:14px;margin-left:2px}
.adjv4 i{font-style:normal;font-weight:500;color:rgba(31,31,31,.75);white-space:nowrap;font-variant-numeric:tabular-nums}
@media (hover:hover) and (pointer:fine){.adjv4:hover{box-shadow:inset 0 0 0 1px var(--adj-brand),var(--adj-sh-1)!important}}
.adjv4:active{transform:scale(.97)}
''', '', 'steps')

var('Pas z krótkimi filmami pod zdjęciem',
    'Szybki przegląd filmów w formie znanej z Instagrama, dla młodszych kursantów.',
    'Wyraźny pas z nagłówkiem tuż pod górą strony, duże kółka z play. Film otwiera się w oknie ze strzałkami do następnego.',
    'Na telefonie pas jest pod terminami i przyciskiem zapisu, więc trzeba trochę przewinąć.',
    'Do rozważenia',
    r"""
.adjv6{width:100vw;margin:28px calc(50% - 50vw) 8px;padding:24px 16px;background:var(--adj-gray)}
.adjv6__in{max-width:1260px;margin:0 auto;display:grid;grid-template-columns:auto minmax(0,1fr);gap:28px;align-items:center}
.adjv6__lead strong{display:block;font:700 20px/1.2 "Work Sans",sans-serif;color:#000}
.adjv6__lead span{display:block;margin-top:6px;font:500 14px/1.35 "Work Sans",sans-serif;color:rgba(31,31,31,.72)}
.adjv6__wrap{position:relative;min-width:0}
.adjv6__row{display:flex;gap:18px;overflow-x:auto;padding:6px 4px 8px!important;scroll-snap-type:x mandatory;scroll-padding-inline:4px;scrollbar-width:none}
.adjv6__row::-webkit-scrollbar{display:none}
.adjv6__s{flex:0 0 auto;width:100px;display:flex!important;flex-direction:column;align-items:center;gap:10px;scroll-snap-align:start;color:#000!important}
.adjv6__ring{position:relative;width:92px;height:92px;border-radius:50%;padding:3px;background:var(--adj-brand);transition:transform .2s var(--adj-out)}
.adjv6__ring img{width:100%!important;height:100%!important;border-radius:50%;object-fit:cover;border:3px solid var(--adj-gray);display:block}
.adjv6__ring .adjv-play{position:absolute;right:-2px;bottom:-2px;width:32px;height:32px;border:3px solid var(--adj-gray);box-shadow:none}
.adjv6__ring .adjv-play svg{width:12px;height:12px;margin-left:2px}
.adjv6__s>span:last-child{font:600 13px/1.35 "Work Sans",sans-serif;text-align:center}
@media (hover:hover) and (pointer:fine){.adjv6__s:hover .adjv6__ring{transform:scale(1.05)}}
.adjv6__s:active .adjv6__ring{transform:scale(.95)}
.adjv6__s:first-child .adjv6__ring::after{content:"";position:absolute;inset:-3px;border-radius:50%;box-shadow:0 0 0 0 rgba(254,169,0,.55);opacity:0}
.adjv6.is-seen li:first-child .adjv6__ring::after{animation:adjv6p 1.6s var(--adj-out) .3s 2}
@keyframes adjv6p{0%{opacity:1;box-shadow:0 0 0 0 rgba(254,169,0,.55)}100%{opacity:0;box-shadow:0 0 0 14px rgba(254,169,0,0)}}
.adjv6__more{position:absolute;right:0;top:0;bottom:0;width:72px;display:flex;align-items:center;justify-content:flex-end;padding-right:4px;background:linear-gradient(90deg,rgba(244,244,244,0),var(--adj-gray) 70%);pointer-events:none;color:#000}
.adjv6__more svg{width:22px;height:22px}
.adjv6.is-end .adjv6__more{display:none}
@media (max-width:900px){.adjv6__in{grid-template-columns:1fr;gap:14px}}
""", r"""
(function(){var s=document.querySelector('.adjv6'); if(!s) return; var r=s.querySelector('.adjv6__row');
 new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){s.classList.add('is-seen');o.disconnect()}})},{threshold:.6}).observe(s);
 function end(){s.classList.toggle('is-end',r.scrollLeft+r.clientWidth>=r.scrollWidth-8)} r.addEventListener('scroll',end,{passive:true}); end();})();
""", 'stories')

var('Zakładki przy opisie egzaminu',
    'Pokazuje, jak wygląda egzamin praktyczny: obsługa auta i trasy po Wrocławiu.',
    'Filmy stoją przy opisie części egzaminu, której dotyczą. Zakładki obsługuje się też strzałkami na klawiaturze.',
    'Dodaje ok. 400 px w środku tekstu o egzaminie.',
    'Do rozważenia',
    r'''
.adjv7{margin:24px 0 32px;padding:12px;border-radius:16px;background:var(--adj-navy);box-shadow:var(--adj-sh-2)}
.adjv7__tabs{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:4px;padding:4px;margin-bottom:12px;border-radius:12px;background:rgba(255,255,255,.07)}
.adjv7__tab{min-height:44px;padding:0 10px!important;border-radius:9px!important;color:rgba(255,255,255,.82)!important;font:600 14px/1.15 "Work Sans",sans-serif!important;text-align:center;transition:background-color .2s var(--adj-out),color .2s var(--adj-out)}
.adjv7__tab[aria-selected="true"]{background:var(--adj-brand)!important;color:var(--adj-ink)!important}
.adjv7__tab:not([aria-selected="true"]):hover{background:rgba(255,255,255,.08)!important}
.adjv7__panel[hidden]{display:none}
.adjv7__panel>.adjv-card .adjv-media{border-radius:10px}
.adjv7__panel>.adjv-card .adjv-cap{color:#fff;padding:2px 4px}
.adjv7__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;color:#fff}
.adjv7__grid .adjv-cap strong{font-size:13px}
@media (max-width:600px){.adjv7__tabs{grid-template-columns:repeat(2,minmax(0,1fr))}.adjv7__grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
''', r'''
(function(){var r=document.querySelector('.adjv7'); if(!r) return; var tabs=[].slice.call(r.querySelectorAll('.adjv7__tab'));
 function sel(t){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1});
  r.querySelectorAll('.adjv7__panel').forEach(function(p){p.hidden=p.id!==t.getAttribute('aria-controls')});}
 tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t)});
  t.addEventListener('keydown',function(e){var k={ArrowRight:1,ArrowLeft:-1}[e.key]; if(!k) return; e.preventDefault(); var n=tabs[(i+k+tabs.length)%tabs.length]; sel(n); n.focus();});});})();
''', 'exam')

var('Siatka filmów przed FAQ',
    'Zebranie filmów w jednym miejscu tuż przed pytaniami, gdzie czytelnik zbiera ostatnie informacje.',
    'Duży film o kursie i trzy filmy o egzaminie, z przyciskiem zapisu w nagłówku sekcji.',
    'Nisko na stronie, więc ogląda go mniej osób. Bez kontekstu tekstu.',
    'Do rozważenia',
    r'''
.adjv8{padding:56px 16px;background:var(--adj-gray)}
.adjv8__in{max-width:1180px;margin:0 auto}
.adjv8__h{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;margin-bottom:24px}
.adjv8__h h2{margin:0!important;text-align:left!important}
.adjv8__g{display:grid;grid-template-columns:2fr 1fr;gap:20px;align-items:start}
.adjv8__g>.adjv-card .adjv-cap strong{font-size:18px}
.adjv8__side{display:grid;gap:16px}
.adjv8__side .adjv-card{display:grid!important;grid-template-columns:minmax(0,1.1fr) 1fr;gap:14px;align-items:center}
.adjv8__side .adjv-play{width:40px;height:40px}.adjv8__side .adjv-play svg{width:16px;height:16px}
@media (max-width:820px){.adjv8__g{grid-template-columns:1fr}}
''', '', 'faq')

var('Pas z filmem w połowie strony',
    'Mocny akcent wizualny między opisem kursu a placem manewrowym.',
    'Kadr z filmu na całą szerokość, obok siebie „Obejrzyj film” i „Zapisz się”.',
    'Zajmuje dużo miejsca dla jednego filmu. Tło lekko się przybliża przy przewijaniu, tylko raz.',
    'Niepolecany',
    r'''
.adjv9{position:relative;width:100vw;margin:40px calc(50% - 50vw);min-height:clamp(340px,38vw,460px);display:grid;align-items:end;padding:48px 16px;overflow:hidden;background:var(--adj-ink);isolation:isolate}
.adjv9__bg{position:absolute;inset:0;z-index:-2;width:100%!important;height:100%!important;object-fit:cover}
@supports (animation-timeline: view()){@media (prefers-reduced-motion:no-preference){.adjv9__bg{animation:adjv9z linear both;animation-timeline:view();animation-range:entry 0% cover 60%}@keyframes adjv9z{from{transform:scale(1.08)}to{transform:scale(1)}}}}
.adjv9::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(20,20,20,.92) 0%,rgba(20,20,20,.55) 45%,rgba(20,20,20,.1) 100%)}
.adjv9__in{max-width:1180px;width:100%;margin:0 auto}
.adjv9 h2{color:#fff!important;margin:0 0 20px!important;max-width:22ch;text-align:left!important;font-size:clamp(28px,3.2vw,42px)!important;line-height:1.1!important}
.adjv9__cta{display:flex;flex-wrap:wrap;gap:12px}
''', '', 'banner')

var('Pytania z jazd w 60 sekund',
    'Odpowiada na obawy przed jazdami po mieście: konkretne skrzyżowania Wrocławia.',
    'Konkretne, lokalne, krótkie filmy. Obok cały czas przycisk zapisu i telefon.',
    'Nisko na stronie, przed FAQ.',
    'Polecany (część zestawu 10)',
    r'''
.adjv10{padding:56px 16px;background:#fff}
.adjv10__in{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:clamp(24px,5vw,72px);align-items:start}
.adjv10__lead{position:sticky;top:100px}
.adjv10__lead h2{margin:0 0 14px!important;text-align:left!important}
.adjv10__lead p{margin:0 0 24px;max-width:40ch}
.adjv10__acts{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center}
.adjv10__tel{display:inline-flex;align-items:center;gap:8px;min-height:48px;color:var(--adj-navy)!important;font:700 16px/1 "Work Sans",sans-serif;text-decoration:none!important;font-variant-numeric:tabular-nums}
.adjv10__tel svg{width:18px;height:18px}
.adjv10__list li+li{border-top:1px solid rgba(31,31,31,.12)!important}
.adjv10__q{display:grid!important;grid-template-columns:128px 1fr;gap:18px;align-items:center;width:100%!important;padding:14px 8px!important;border-radius:12px!important;text-align:left;color:var(--adj-navy)!important;transition:background-color .2s var(--adj-out)}
.adjv10__q .adjv-media{border-radius:8px}
.adjv10__q .adjv-play{width:36px;height:36px}.adjv10__q .adjv-play svg{width:14px;height:14px}
.adjv10__q .adjv-dur{right:6px;bottom:6px;font-size:11px}
.adjv10__q strong{font:600 17px/1.35 "Work Sans",sans-serif}
.adjv10__q small{display:block;margin-top:6px;font:500 13px/1.3 "Roboto",sans-serif;color:rgba(31,31,31,.72)}
@media (hover:hover) and (pointer:fine){.adjv10__q:hover{background:var(--adj-gray)!important}}
.adjv10__q:active{background:#ececec!important}
@media (max-width:820px){.adjv10__in{grid-template-columns:1fr}.adjv10__lead{position:static}.adjv10__q{grid-template-columns:104px 1fr;gap:14px}.adjv10__q strong{font-size:16px}}
''', '', 'qa')




def hero1():
    return (f'<button class="adjv adjv1" type="button" {yt("promo")} data-inline aria-label="Odtwórz film: {V["promo"][1]}, {V["promo"][2]}">'
            f'{play()}<span class="adjv1__cap"><strong>{V["promo"][1]}</strong><span>{V["promo"][2]}</span></span></button>')

def hero2():
    return f'<button class="adjv adjv2" type="button" {yt("promo")} data-inline-mobile>{play()}Obejrzyj film o kursie <em>{V["promo"][2]}</em></button>'

def cinema():
    items = ''.join(
        f'<li><button class="adjv3__item" type="button" data-id="{V[k][0]}" data-title="{V[k][1]}" aria-current="{"true" if n==0 else "false"}">'
        f'<img src="{img(k)}" alt="" loading="lazy"><span><strong>{V[k][1]}</strong><small>{V[k][2]}</small></span></button></li>'
        for n, k in enumerate(['fotel', 'swiatla', 'plyny']))
    grid = ''.join(f'<li>{card(k, group="city3")}</li>' for k in CITY[:4])
    return (f'<section class="adjv adjv3" aria-labelledby="adjv3-h"><div class="adjv3__in"><h2 id="adjv3-h">Zobacz kurs od środka</h2>'
            f'<div class="adjv3__stage"><div class="adjv3__player">{card("fotel", big=True, cap=False)}</div>'
            f'<div class="adjv3__side"><ul role="list" style="display:grid;gap:10px">{items}</ul>'
            f'<a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div></div>'
            f'<div class="adjv3__city"><h3>Trudne skrzyżowania z tras egzaminacyjnych</h3><p>Instruktorzy ADJ pokazują je z drona i zza kierownicy.</p>'
            f'<ul class="adjv3__grid" role="list">{grid}</ul>'
            f'<a class="adjv3__more" href="{CHANNEL}" target="_blank" rel="noopener">Więcej filmów na YouTube {ARROW}</a></div></div></section>')

def chip(k, label=None):
    return f'<button class="adjv adjv4" type="button" {yt(k, "steps")}>{play()}<span>{label or V[k][1]} <i>{V[k][2]}</i></span></button>'

def floating():
    X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
    return f'<aside class="adjv adjv5" aria-label="Film o kursie"><button class="adjv5__x" type="button" aria-label="Ukryj film">{X}</button>{card("promo")}</aside>'

def stories():
    items = ['fotel', 'swiatla', 'plyny'] + CITY
    names = {'fotel': 'Fotel', 'swiatla': 'Światła', 'plyny': 'Płyny'}
    li = ''.join(f'<li><button class="adjv6__s" type="button" {yt(k, "stories")} aria-label="Odtwórz film: {V[k][1]}, {V[k][2]}">'
                 f'<span class="adjv6__ring"><img src="{img(k)}" alt="">{play()}</span><span>{names.get(k) or V[k][4]}</span></button></li>' for k in items)
    return (f'<section class="adjv adjv6" aria-labelledby="adjv6-h"><div class="adjv6__in"><div class="adjv6__lead"><strong id="adjv6-h">Krótkie filmy instruktorów</strong>'
            f'<span>{len(items)} filmów: egzamin i trasy po Wrocławiu</span></div>'
            f'<div class="adjv6__wrap"><ul class="adjv6__row" role="list">{li}</ul><span class="adjv6__more" aria-hidden="true">{ARROW}</span></div></div></section>')

def exam():
    tabs = [('t1', 'Obsługa auta', 'fotel'), ('t2', 'Światła', 'swiatla'), ('t3', 'Płyny', 'plyny'), ('t4', 'Trasy w mieście', 'city')]
    tb = ''.join(f'<button class="adjv7__tab" type="button" role="tab" id="adjv7-tab-{k}" aria-selected="{"true" if n==0 else "false"}" tabindex="{0 if n==0 else -1}" aria-controls="adjv7-{k}">{nm}</button>'
                 for n, (k, nm, _) in enumerate(tabs))
    panels = ''
    for n, (k, nm, v) in enumerate(tabs):
        hid = '' if n == 0 else ' hidden'
        body = ('<ul class="adjv7__grid" role="list">' + ''.join(f'<li>{card(c, group="exam-city")}</li>' for c in CITY[:3]) + '</ul>') if v == 'city' else card(v, big=True)
        panels += f'<div class="adjv7__panel" id="adjv7-{k}" role="tabpanel" aria-labelledby="adjv7-tab-{k}"{hid}>{body}</div>'
    return f'<div class="adjv adjv7"><div class="adjv7__tabs" role="tablist" aria-label="Filmy o egzaminie">{tb}</div>{panels}</div>'

def faq_grid():
    side = ''.join(card(k, group='faq') for k in ['fotel', 'swiatla', 'plyny'])
    return (f'<section class="adjv adjv8" aria-labelledby="adjv8-h"><div class="adjv8__in"><div class="adjv8__h"><h2 id="adjv8-h">Kurs kat. B w filmach</h2>'
            f'<a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div>'
            f'<div class="adjv8__g">{card("promo", group="faq", big=True)}<div class="adjv8__side">{side}</div></div></div></section>')

def banner():
    return (f'<section class="adjv adjv9" aria-labelledby="adjv9-h"><img class="adjv9__bg" src="{img("promo", True)}" alt="" loading="lazy">'
            f'<div class="adjv9__in"><h2 id="adjv9-h">Zobacz, jak wygląda kurs w ADJ</h2><div class="adjv9__cta">'
            f'<button class="adjv-btn adjv-btn--ghost" type="button" {yt("promo")}>{play()}Obejrzyj film {V["promo"][2]}</button>'
            f'<a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div></div></section>')

def qa():
    qs = [('pionier', 'Jak zawracać na Rondzie Pionierów?', 'Rondo Pionierów'), ('jagodno', 'Jak skręcić w lewo na Rondzie Wolnej Ukrainy?', 'Jagodno'),
          ('tory', 'Jak bezpiecznie przejechać przez tory?', 'Przejazd kolejowy'), ('mini', 'Jak przejechać mini rondo?', 'Centralna i Semaforowa'),
          ('armii', 'Jak zjechać z Armii Krajowej w Krakowską?', 'Krzyki')]
    li = ''.join(f'<li><button class="adjv10__q" type="button" {yt(k, "qa")} aria-label="Odtwórz film: {q}, {V[k][2]}">'
                 f'<span class="adjv-media"><img src="{img(k)}" alt="" loading="lazy">{play()}<span class="adjv-dur">{V[k][2]}</span></span>'
                 f'<span><strong>{q}</strong><small>{p}</small></span></button></li>' for k, q, p in qs)
    return (f'<section class="adjv adjv10" aria-labelledby="adjv10-h"><div class="adjv10__in"><div class="adjv10__lead"><h2 id="adjv10-h">Trudne miejsca na trasach egzaminacyjnych</h2>'
            f'<p>Instruktorzy ADJ pokazują, jak przejechać skrzyżowania, na których kursanci mylą się najczęściej.</p>'
            f'<div class="adjv10__acts"><a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a>'
            f'<a class="adjv10__tel" href="tel:+48575757408">{PHONE}{TEL}</a></div></div>'
            f'<ul class="adjv10__list" role="list">{li}</ul></div></section>')


def prep(s):
    s = re.sub(r'<meta name=["\']robots["\'][^>]*>', '', s)
    s = s.replace('href="/', 'href="' + SITE + '/').replace('src="/', 'src="' + SITE + '/')
    s = s.replace('href="' + SITE + '//', 'href="//').replace('src="' + SITE + '//', 'src="//')
    def unlazy(m):
        tag = m.group(0); ds = re.search(r'\sdata-src="([^"]+)"', tag)
        if not ds: return tag
        tag = re.sub(r'\ssrc="[^"]*"', ' src="' + ds.group(1) + '"', tag, count=1)
        return tag.replace(' data-src="', ' data-orig-src="')
    s = re.sub(r'<img[^>]*>', unlazy, s)
    s = re.sub(r'srcset=""\s+data-srcset="([^"]+)"', r'srcset="\1"', s)
    s = re.sub(r'class="lazy\s+', 'class="', s)
    s = s.replace('class="bestseller-title-tag"', 'class="bestseller-title-tag show"')
    s = re.sub(r'(<iframe[^>]*?)\sdata-src="([^"]+)"', lambda m: m.group(1) + ' src="' + m.group(2) + '"', s)
    return s

def at(s, needle, start=0):
    i = s.find(needle, start); assert i > 0, needle; return i

def ins(s, pos, html):
    return s[:pos] + html + s[pos:]

def do_hero(s, html):
    i = at(s, '<div class="kurs-img-wrapper">')
    m = re.compile(r'<img[^>]*>').search(s, i)
    s = s[:m.end()] + html + s[m.end():]
    return s.replace('<div class="kurs-img-wrapper">', '<div class="kurs-img-wrapper" data-inline-box style="position:relative">', 1)

def steps_after(s):
    return at(s, '<div style="height:50px" aria-hidden="true" class="wp-block-spacer"></div><div class="wp-block-columns', at(s, 'Krok 8:'))

def do_steps(s):
    for step, ch in [('Krok 5:', chip('jagodno', 'Trasa egzaminacyjna: skręt w lewo na Rondzie Wolnej Ukrainy')),
                     ('Krok 6:', chip('fotel')), ('Krok 7:', chip('swiatla') + chip('plyny'))]:
        p = at(s, step); e = s.find('</p>', p)
        s = s[:e] + '<br>' + ch + s[e:]
    return s

def faq_pos(s):
    return at(s, '<div class="container"><h2>FAQ')

def drop_inline_promo(s):
    # film o kursie jest już w hero, więc usuwamy jego drugie osadzenie w treści
    a = s.rfind('<figure', 0, at(s, 'ZnJegLxixKQ', at(s, 'Dlaczego kursanci zdają')))
    b = s.find('</figure>', a) + len('</figure>')
    return s[:a] + s[b:]

SVG_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SVG_G = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'

def build(nr, v, base):
    s, css, js, k = base, COMMON_CSS + CARD_CSS + v['css'], COMMON_JS + v['js'], v['kind']
    if k == 'hero1': s = do_hero(s, hero1())
    elif k == 'hero2': s = do_hero(s, hero2())
    elif k == 'cinema': s = ins(s, steps_after(s), cinema())
    elif k == 'steps': s = do_steps(s)
    elif k == 'floating': s = s.replace('</body>', floating() + '</body>', 1)
    elif k == 'stories':
        s = ins(s, at(s, '<div class="kurs-info-kursanta">'), stories())
    elif k == 'exam':
        h = at(s, 'Jak wygląda egzamin na prawo jazdy kat. B'); u1 = s.find('</ul>', h); u2 = s.find('</ul>', u1 + 5) + 5
        s = ins(s, u2, exam())
    elif k == 'faq': s = ins(s, faq_pos(s), faq_grid())
    elif k == 'banner': s = ins(s, steps_after(s), banner())
    elif k == 'qa': s = ins(s, faq_pos(s), qa())
    elif k == 'combo':
        s = do_hero(s, hero1()); s = do_steps(s); s = ins(s, faq_pos(s), qa()); s = drop_inline_promo(s)
        K={v['kind']:v['css'] for v in VARS}; css = COMMON_CSS + CARD_CSS + K['hero1'] + K['steps'] + K['qa']
    n = len(VARS)
    nav = (f'<nav class="adjv-bar" aria-label="Warianty"><span><b>Wariant {nr} z {n}</b>{v["name"]}</span>'
           f'<a href="v{(nr-2)%n+1:02d}.html#film" aria-label="Poprzedni wariant">{SVG_L}</a><a href="index.html" aria-label="Wszystkie warianty">{SVG_G}</a>'
           f'<a href="v{nr%n+1:02d}.html#film" aria-label="Następny wariant">{SVG_R}</a></nav>')
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{css}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', nav + f'<script>{js}</script>\n</body>', 1)
    (BASE / f'v{nr:02d}.html').write_text(s, encoding='utf-8')

def index():
    cards = ''.join(
        f'<li><a class="th" href="v{n:02d}.html#film" aria-label="Wariant {n}: {v["name"]}, na komputerze"><img src="img/v{n:02d}.jpg" alt="" loading="lazy" width="720" height="450"></a>'
        f'<div class="tx"><h2><span>{n}</span>{v["name"]}</h2><p>{v["desc"]}</p>'
        f'<div class="bt"><a class="b1" href="v{n:02d}.html#film">{MON}Na komputerze</a><a class="b2" href="telefon.html?v={n:02d}">{PHN}Na telefonie</a></div></div></li>'
        for n, v in enumerate(VARS, 1))
    return f"""<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Filmy na stronie kursu kat. B: warianty</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>*{{box-sizing:border-box}}body{{margin:0;background:#f4f4f4;color:#1f1f1f;font-family:"Work Sans",sans-serif}}::selection{{background:#FEA900;color:#141414}}
header{{background:#1f1f1f;color:#fff;padding:28px 16px}}header div{{max-width:1180px;margin:0 auto;display:flex;align-items:center;gap:16px}}header img{{height:48px;width:auto}}
main{{max-width:1180px;margin:0 auto;padding:40px 16px 96px}}h1{{font-size:clamp(28px,3.6vw,40px);line-height:1.1;margin:0 0 12px}}.lead{{margin:0 0 32px;font-size:17px;line-height:1.55;max-width:70ch;color:rgba(31,31,31,.8)}}
ul{{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:24px}}
li{{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 1px 0 rgba(31,31,31,.05),0 20px 40px -30px rgba(31,31,31,.5);display:flex;flex-direction:column}}
.th{{display:block;aspect-ratio:16/10;overflow:hidden;background:#1f1f1f}}.th img{{width:100%;height:100%;object-fit:cover;object-position:top;display:block;transition:transform .5s cubic-bezier(.23,1,.32,1)}}
.th:hover img{{transform:scale(1.03)}}.th:focus-visible,.bt a:focus-visible{{outline:3px solid #FEA900;outline-offset:3px}}
.tx{{padding:20px 22px 22px;display:flex;flex-direction:column;flex:1}}h2{{font-size:19px;line-height:1.3;margin:0 0 8px;display:flex;gap:10px;align-items:baseline}}
h2 span{{flex:0 0 auto;display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#FEA900;color:#141414;font-size:15px;font-variant-numeric:tabular-nums;transform:translateY(5px)}}
p{{margin:0 0 20px;font-size:15px;line-height:1.55;color:rgba(31,31,31,.8);flex:1}}.bt{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.bt a{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:0 12px;white-space:nowrap;border-radius:999px;font-weight:600;font-size:14px;text-decoration:none;transition:transform .15s cubic-bezier(.23,1,.32,1),background-color .2s}}
.bt a:active{{transform:scale(.97)}}.bt svg{{width:18px;height:18px}}.b1{{background:#FEA900;color:#141414}}.b1:hover{{background:#ffbd33}}.b2{{background:#f4f4f4;color:#1f1f1f}}.b2:hover{{background:#e9e9e9}}</style></head>
<body><header><div><img src="https://www.naukajazdy.wroc.pl/wp-content/themes/akademia_custom/assets/img/logo_ADJ.png" alt="Akademia Dobrej Jazdy" onerror="this.remove()"></div></header>
<main><h1>Filmy na stronie kursu kat. B</h1>
<p class="lead">Każdy wariant to podgląd obecnej strony kursu kat. B z innym sposobem pokazania filmów z kanału ADJ. Podgląd otwiera się od razu w miejscu z filmem. Na dole strony są strzałki do kolejnych wariantów.</p>
<ul>{cards}</ul></main></body></html>"""

MON = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 20h8M12 16v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
PHN = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="2.5" width="10" height="19" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M11 18h2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

def phone():
    names = [f'"{v["name"]}"' for v in VARS]
    return """<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Podgląd na telefonie</title><link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@500;600;700&display=swap" rel="stylesheet">
<style>*{box-sizing:border-box}html,body{height:100%}body{margin:0;background:#1f1f1f;color:#fff;font-family:"Work Sans",sans-serif;display:grid;grid-template-rows:auto 1fr;overflow:hidden}
.top{display:flex;align-items:center;gap:12px;padding:14px 20px}.top b{color:#FEA900}.top span{flex:1;font-weight:600}
.top a{display:grid;place-items:center;min-width:44px;height:44px;padding:0 14px;border-radius:999px;background:rgba(255,255,255,.1);color:#fff;text-decoration:none;font-weight:600;gap:8px;grid-auto-flow:column}
.top a:hover{background:rgba(255,255,255,.2)}.top svg{width:18px;height:18px}
.stage{display:grid;place-items:center;padding:8px 16px 20px;min-height:0}
.ph{height:min(100%,868px);aspect-ratio:414/868;border-radius:44px;background:#000;padding:12px;box-shadow:0 0 0 2px #3a3a3a,0 40px 80px -30px rgba(0,0,0,.8)}
.sc{width:100%;height:100%;border-radius:32px;overflow:hidden;background:#fff;position:relative}
iframe{position:absolute;left:0;top:0;width:390px;height:844px;border:0;transform-origin:0 0}</style></head>
<body><div class="top"><a href="index.html" aria-label="Wszystkie warianty">""" + SVG_G + """</a><span><b id="n"></b> <span id="t"></span></span>
<a id="pv" aria-label="Poprzedni wariant">""" + SVG_L + """</a><a id="nx" aria-label="Następny wariant">""" + SVG_R + """</a><a id="pc">""" + MON + """Na komputerze</a></div>
<div class="stage"><div class="ph"><div class="sc"><iframe id="f" title="Podgląd strony na telefonie"></iframe></div></div></div>
<script>var N=[""" + ','.join(names) + """],n=N.length,v=parseInt(new URLSearchParams(location.search).get('v')||'1',10);
function p(x){return String(x).padStart(2,'0')}
document.getElementById('n').textContent='Wariant '+v+':';document.getElementById('t').textContent=N[v-1];
document.getElementById('f').src='v'+p(v)+'.html#film';document.getElementById('pc').href='v'+p(v)+'.html#film';
document.getElementById('pv').href='telefon.html?v='+p((v-2+n)%n+1);document.getElementById('nx').href='telefon.html?v='+p(v%n+1);
function fit(){var sc=document.querySelector('.sc'),k=sc.clientWidth/390;var f=document.getElementById('f');f.style.transform='scale('+k+')';f.style.height=(sc.clientHeight/k)+'px'}
addEventListener('resize',fit);fit();</script></body></html>"""

if __name__ == '__main__':
    base = prep((BASE / '_base.html').read_text(encoding='utf-8'))
    for n, v in enumerate(VARS, 1):
        build(n, v, base)
    (BASE / 'index.html').write_text(index(), encoding='utf-8')
    (BASE / 'telefon.html').write_text(phone(), encoding='utf-8')
    print('ok', len(VARS))
