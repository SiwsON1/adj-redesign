# Generator 10 wariantów filmów na kopii strony kursu kat. B (naukajazdy.wroc.pl).
# Wejście: _base.html (świeży HTML strony). Wyjście: v01.html ... v10.html + index.html.
import re, html as H, pathlib

BASE = pathlib.Path(__file__).parent
SITE = 'https://www.naukajazdy.wroc.pl'
FORM = SITE + '/formularz-zapisow/'

PROMO = ('ZnJegLxixKQ', 'Kurs nauki jazdy w ADJ', '')
FOTEL = ('8H4GNjbGqLw', 'Jak ustawić fotel przed egzaminem', '5:58')
SWIATLA = ('8Fu4ivqowfA', 'Jak sprawdzić światła', '4:48')
PLYNY = ('SUTfnCdub4E', 'Jak sprawdzić płyny', '4:09')
SHORTS = [
    ('2108OLdnWyE', 'Skręt w lewo na Rondzie Wolnej Ukrainy', 'Jagodno', '0:58'),
    ('PqlwPO7q7zE', 'Jak zawracać na Rondzie Pionierów', 'Rondo Pionierów', '0:57'),
    ('UPOX1k-j9CU', 'Z Armii Krajowej w stronę Krakowskiej', 'Krzyki', '0:48'),
    ('kwx0GJi028g', 'Mini rondo: Centralna i Semaforowa', 'Mini rondo', '0:49'),
    ('VLkvy_L9fK0', 'Bezpieczny przejazd przez tory', 'Tory', '0:37'),
    ('P3ORAULwYMU', 'Skręt w lewo z Chińskiej w Mościckiego', 'Chińska', '0:48'),
]

def thumb(i, q='hqdefault'):
    return f'https://i.ytimg.com/vi/{i}/{q}.jpg'

PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>'

def btn_attrs(vid, vertical=False):
    return f'data-yt="{vid}"' + (' data-vertical' if vertical else '')

# ---------- wspólne: style, okno z filmem, pasek wariantu ----------
COMMON_CSS = r'''
:root{--adj-navy:#21314a;--adj-navy-d:#182336;--adj-brand:#FEA900;--adj-brand-l:#ffbd33;--adj-ease:cubic-bezier(.23,1,.32,1)}
.adjv,.adjv *{box-sizing:border-box}
.adjv{font-family:"Work Sans",sans-serif}
.adjv button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:pointer;text-transform:none;letter-spacing:normal;box-shadow:none;min-height:0;width:auto;height:auto}
.adjv img{max-width:none;margin:0}
.adjv ul,.adjv ol{list-style:none!important;margin:0!important;padding:0!important}
.adjv li{list-style:none!important;margin:0!important;padding:0!important}.adjv li::marker{content:none}
.adjv h2,.adjv h3,.adjv p{margin:0}
.adjv :focus-visible{outline:3px solid var(--adj-brand);outline-offset:3px}
.adjv-play{width:64px;height:64px;border-radius:50%;background:var(--adj-brand);display:grid;place-items:center;box-shadow:0 12px 28px -10px rgba(254,169,0,.65);transition:transform .2s var(--adj-ease)}
.adjv-play svg{width:26px;height:26px;fill:var(--adj-navy-d);margin-left:3px}
@media (hover:hover) and (pointer:fine){[data-yt]:hover .adjv-play{transform:scale(1.08)}}
[data-yt]:active .adjv-play{transform:scale(.94)}
/* okno z filmem */
.adjv-modal{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;padding:16px;background:rgba(13,21,34,.86);opacity:0;transition:opacity .2s var(--adj-ease)}
.adjv-modal.is-open{opacity:1}
.adjv-modal__box{position:relative;width:min(1100px,100%);aspect-ratio:16/9;border-radius:14px;overflow:hidden;background:#0d1522;box-shadow:0 40px 80px -30px rgba(0,0,0,.7);transform:scale(.96);transition:transform .22s var(--adj-ease)}
.adjv-modal.is-open .adjv-modal__box{transform:scale(1)}
.adjv-modal--v .adjv-modal__box{width:auto;height:min(86dvh,720px);aspect-ratio:9/16}
.adjv-modal iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.adjv-modal__x{position:absolute;top:14px;right:14px;width:44px;height:44px;border-radius:50%;background:#fff!important;color:var(--adj-navy-d)!important;display:grid;place-items:center;z-index:2;font:600 22px/1 "Work Sans",sans-serif!important;border:0;cursor:pointer;transition:transform .15s var(--adj-ease)}
.adjv-modal__x:active{transform:scale(.94)}
/* pasek wariantu (tylko podgląd) */
.adjv-bar{position:fixed;left:16px;bottom:16px;z-index:2147482000;display:flex;align-items:center;gap:6px;background:var(--adj-navy-d);color:#fff;border-radius:999px;padding:6px 6px 6px 16px;font:500 13px/1.2 "Work Sans",sans-serif;box-shadow:0 12px 30px -12px rgba(0,0,0,.5)}
.adjv-bar b{color:var(--adj-brand);font-weight:700;margin-right:4px}
.adjv-bar a{color:#fff!important;text-decoration:none!important;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:rgba(255,255,255,.1)}
.adjv-bar a:hover{background:rgba(255,255,255,.2)}
@media (max-width:600px){.adjv-bar{left:8px;right:8px;bottom:8px;justify-content:space-between}.adjv-bar span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
@media (prefers-reduced-motion:reduce){.adjv *,.adjv-modal,.adjv-modal__box{transition:none!important;animation:none!important}}
'''

COMMON_JS = r'''
(function(){
  function open(id, vertical){
    var m=document.createElement('div'); m.className='adjv-modal'+(vertical?' adjv-modal--v':''); m.setAttribute('role','dialog'); m.setAttribute('aria-modal','true');
    m.innerHTML='<div class="adjv-modal__box"><button class="adjv-modal__x" type="button" aria-label="Zamknij">×</button><iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1" title="Film ADJ" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe></div>';
    var last=document.activeElement; document.body.appendChild(m); document.documentElement.style.overflow='hidden';
    requestAnimationFrame(function(){m.classList.add('is-open')}); m.querySelector('.adjv-modal__x').focus();
    function close(){ m.classList.remove('is-open'); document.documentElement.style.overflow=''; document.removeEventListener('keydown',key); setTimeout(function(){m.remove(); if(last) last.focus()},180); }
    function key(e){ if(e.key==='Escape') close(); }
    m.addEventListener('click',function(e){ if(e.target===m||e.target.closest('.adjv-modal__x')) close(); });
    document.addEventListener('keydown',key);
  }
  window.adjvOpen=open;
  document.addEventListener('click',function(e){
    var t=e.target.closest('[data-yt]'); if(!t) return; e.preventDefault();
    if(t.hasAttribute('data-inline')){
      var box=t.closest('[data-inline-box]')||t; box.style.height=box.offsetHeight+'px'; box.style.background='#0d1522';
      box.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+t.dataset.yt+'?autoplay=1&rel=0&playsinline=1" title="Film ADJ" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>';
      return;
    }
    open(t.dataset.yt, t.hasAttribute('data-vertical'));
  });
})();
'''

# ---------- warianty ----------
V = []  # (nr, nazwa, opis, css, js, inserts[(kotwica, html, 'before'|'after'|'replace_hero')])

# 1. Film w miejscu zdjęcia w hero
V.append(('Film w miejscu zdjęcia (hero)',
 'Zdjęcie auta w hero dostaje przycisk odtwarzania. Film gra w tym samym miejscu, bez przewijania.',
 r'''
.adjv1{position:absolute!important;inset:0;display:block;border-radius:inherit;overflow:hidden;z-index:2}
.adjv1::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,21,34,0) 45%,rgba(13,21,34,.82) 100%)}
.adjv1 .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:88px;height:88px;z-index:2}
.adjv1 .adjv-play svg{width:34px;height:34px}
@media (hover:hover) and (pointer:fine){.adjv1:hover .adjv-play{transform:translate(-50%,-50%) scale(1.08)}}
.adjv1:active .adjv-play{transform:translate(-50%,-50%) scale(.94)}
.adjv1__cap{position:absolute;left:24px;bottom:22px;right:24px;z-index:2;color:#fff;text-align:left}
.adjv1__cap small{display:block;font:700 12px/1 "Work Sans",sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--adj-brand);margin-bottom:8px}
.adjv1__cap strong{font:700 clamp(18px,1.8vw,24px)/1.2 "Work Sans",sans-serif}
.adjv1 .adjv-play,.adjv1__cap{z-index:3}
[data-inline-box] iframe{border-radius:inherit}
''', '', 'hero'))

# 2. Przycisk w hero -> okno
V.append(('Przycisk w hero, film w oknie',
 'Zdjęcie zostaje bez zmian. W rogu zdjęcia jest przycisk „Obejrzyj film o kursie”, film otwiera się w oknie na środku ekranu.',
 r'''
.adjv2{position:absolute;right:16px;top:16px;z-index:3;display:inline-flex!important;align-items:center;gap:12px;padding:8px 18px 8px 8px!important;border-radius:999px;background:rgba(24,35,54,.88)!important;color:#fff!important;font:600 15px/1 "Work Sans",sans-serif!important;backdrop-filter:blur(6px);box-shadow:0 14px 30px -14px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.12)!important;transition:transform .16s var(--adj-ease)}
.adjv2 .adjv-play{width:40px;height:40px;box-shadow:none}
.adjv2 .adjv-play svg{width:16px;height:16px;margin-left:2px}
.adjv2 em{font-style:normal;color:rgba(255,255,255,.65);font-weight:500;margin-left:2px}
.adjv2:active{transform:scale(.97)}
@media (max-width:600px){.adjv2{top:10px;right:10px;font-size:13px!important;padding:5px 12px 5px 5px!important;gap:8px}.adjv2 .adjv-play{width:30px;height:30px}.adjv2 .adjv-play svg{width:12px;height:12px}}
@media (hover:hover) and (pointer:fine){.adjv2:hover{background:rgba(24,35,54,.96)!important}}
''', '', 'hero'))

# 3. Sekcja kinowa (odtwarzacz + lista + krótkie filmy)
V.append(('Sekcja kinowa po krokach kursu',
 'Osobna ciemna sekcja: duży odtwarzacz, lista filmów o egzaminie, krótkie filmy ze skrzyżowań i przycisk zapisu.',
 '', '', 'steps_after'))

# 4. Filmy przy krokach kursu
V.append(('Filmy przy krokach kursu',
 'Przy krokach „Jazdy”, „Egzamin wewnętrzny” i „Egzamin DORD” pojawia się mały przycisk z filmem do tego kroku.',
 r'''
.adjv4{display:inline-flex!important;align-items:center;gap:10px;margin:8px 8px 4px 0!important;padding:6px 14px 6px 6px!important;border-radius:999px;background:#fff!important;border:1px solid rgba(33,49,74,.16)!important;color:var(--adj-navy)!important;font:600 14px/1.2 "Work Sans",sans-serif!important;box-shadow:0 1px 0 rgba(33,49,74,.04),0 10px 22px -16px rgba(33,49,74,.45)!important;transition:transform .16s var(--adj-ease),border-color .2s var(--adj-ease)}
.adjv4 img{width:52px;height:30px;object-fit:cover;border-radius:999px;display:block}
.adjv4 i{font-style:normal;color:rgba(33,49,74,.55);font-weight:500;white-space:nowrap}
.adjv4{text-align:left;max-width:100%}
@media (max-width:600px){.adjv4{font-size:13px!important}.adjv4 img{width:44px;height:26px}}
.adjv4 .adjv4__p{width:22px;height:22px;border-radius:50%;background:var(--adj-brand);display:grid;place-items:center}
.adjv4 .adjv4__p svg{width:11px;height:11px;fill:var(--adj-navy-d);margin-left:1px}
@media (hover:hover) and (pointer:fine){.adjv4:hover{border-color:var(--adj-brand)!important}}
.adjv4:active{transform:scale(.97)}
''', '', 'steps_chips'))

# 5. Pływający mini-odtwarzacz
V.append(('Pływający mini-odtwarzacz',
 'Po przewinięciu za hero w prawym dolnym rogu pojawia się mała karta z filmem. Można ją zamknąć. Na telefonie to pasek na dole ekranu.',
 r'''
.adjv5{position:fixed;right:20px;bottom:20px;z-index:2147481000;width:320px;border-radius:16px;background:var(--adj-navy-d);color:#fff;box-shadow:0 30px 60px -24px rgba(0,0,0,.65),inset 0 1px 0 rgba(255,255,255,.08);transform:translateY(24px);opacity:0;pointer-events:none;transition:transform .3s var(--adj-ease),opacity .25s var(--adj-ease)}
.adjv5.is-on{transform:none;opacity:1;pointer-events:auto}
.adjv5__open{display:block!important;width:100%!important;text-align:left}
.adjv5__media{position:relative;aspect-ratio:16/9;border-radius:16px 16px 0 0;overflow:hidden}
.adjv5__media img{width:100%;height:100%;object-fit:cover;display:block}
.adjv5__media .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:52px;height:52px}
.adjv5__media .adjv-play svg{width:20px;height:20px}
[data-yt]:active .adjv5__media .adjv-play{transform:translate(-50%,-50%) scale(.94)}
.adjv5__txt{display:block;padding:12px 44px 14px 16px}
.adjv5__txt small{display:block;font:700 11px/1 "Work Sans",sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--adj-brand);margin-bottom:6px}
.adjv5__txt strong{font:700 15px/1.25 "Work Sans",sans-serif}
.adjv5__x{position:absolute!important;top:8px;right:8px;width:32px!important;height:32px!important;border-radius:50%!important;background:rgba(13,21,34,.75)!important;color:#fff!important;font:600 18px/1 "Work Sans",sans-serif!important;display:grid!important;place-items:center;z-index:2}
@media (max-width:600px){.adjv5{left:8px;right:8px;bottom:60px;width:auto}.adjv5__open{display:flex!important;align-items:center}.adjv5__media{width:112px;flex:0 0 112px;border-radius:16px 0 0 16px}.adjv5__media .adjv-play{width:38px;height:38px}}
''', r'''
(function(){var c=document.querySelector('.adjv5'); if(!c) return; var off=false;
 c.querySelector('.adjv5__x').addEventListener('click',function(e){e.stopPropagation();off=true;c.classList.remove('is-on')});
 function f(){ if(!off) c.classList.toggle('is-on', scrollY>700); } addEventListener('scroll',f,{passive:true}); f();})();
''', 'floating'))

# 6. Historyjki pod hero
V.append(('Historyjki pod hero',
 'Pod hero rząd okrągłych miniatur jak na Instagramie. Kliknięcie otwiera pionowy film na cały ekran telefonu.',
 r'''
.adjv6{padding:28px 16px 8px;background:#fff}
.adjv6__in{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:24px}
.adjv6__lead{flex:0 0 auto;font:700 15px/1.3 "Work Sans",sans-serif;color:var(--adj-navy);max-width:150px}
.adjv6__lead small{display:block;font-weight:500;color:rgba(33,49,74,.6);margin-top:4px}
.adjv6__row{display:flex;gap:18px;overflow-x:auto;padding:6px 4px 10px!important;scroll-snap-type:x mandatory;scrollbar-width:none}
.adjv6__row::-webkit-scrollbar{display:none}
.adjv6__s{flex:0 0 auto;width:88px;display:flex!important;flex-direction:column;align-items:center;gap:8px;scroll-snap-align:start}
.adjv6__ring{width:80px;height:80px;border-radius:50%;padding:3px;background:conic-gradient(from 210deg,var(--adj-brand),#fb8e28,var(--adj-brand))!important;transition:transform .2s var(--adj-ease)}
.adjv6__ring img{width:100%;height:100%;border-radius:50%;object-fit:cover;border:3px solid #fff;display:block}
.adjv6__s span{font:600 12px/1.25 "Work Sans",sans-serif;color:var(--adj-navy);text-align:center}
@media (hover:hover) and (pointer:fine){.adjv6__s:hover .adjv6__ring{transform:scale(1.05)}}
.adjv6__s:active .adjv6__ring{transform:scale(.95)}
@media (max-width:700px){.adjv6__in{flex-direction:column;align-items:stretch;gap:10px}.adjv6__lead{max-width:none}}
''', '', 'stories'))

# 7. Zakładki przy egzaminie
V.append(('Zakładki przy opisie egzaminu',
 'Pod nagłówkiem o egzaminie zakładki: przygotowanie auta, światła, płyny, skrzyżowania. Każda zakładka pokazuje swój film.',
 r'''
.adjv7{margin:22px 0 30px;border-radius:16px;background:var(--adj-navy);padding:14px;box-shadow:0 30px 60px -36px rgba(13,21,34,.55)}
.adjv7__tabs{position:relative;display:flex;gap:4px;overflow-x:auto;padding:4px!important;margin-bottom:14px!important;background:rgba(255,255,255,.06);border-radius:12px;scrollbar-width:none}
.adjv7__tab{flex:1 0 auto;padding:10px 16px!important;border-radius:9px!important;color:rgba(255,255,255,.75)!important;font:600 14px/1 "Work Sans",sans-serif!important;white-space:nowrap;transition:background-color .2s var(--adj-ease),color .2s var(--adj-ease)}
.adjv7__tab[aria-selected="true"]{background:var(--adj-brand)!important;color:var(--adj-navy-d)!important}
.adjv7__tab:active{transform:scale(.97)}
.adjv7__panel{position:relative}
.adjv7__panel[hidden]{display:none}
.adjv7__v{position:relative;display:block!important;width:100%!important;aspect-ratio:16/9;border-radius:12px;overflow:hidden}
.adjv7__v img{width:100%;height:100%;object-fit:cover;display:block}
.adjv7__v .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)}
[data-yt].adjv7__v:active .adjv-play{transform:translate(-50%,-50%) scale(.94)}
.adjv7__grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.adjv7__sh{position:relative;display:block!important;aspect-ratio:9/14;border-radius:12px;overflow:hidden}
.adjv7__sh img{width:100%;height:100%;object-fit:cover;transform:scale(1.35);display:block}
.adjv7__sh::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 45%,rgba(13,21,34,.92))}
.adjv7__sh span{position:absolute;left:12px;right:12px;bottom:12px;z-index:1;color:#fff;font:700 14px/1.25 "Work Sans",sans-serif;text-align:left}
''', r'''
(function(){var r=document.querySelector('.adjv7'); if(!r) return; var tabs=r.querySelectorAll('.adjv7__tab');
 tabs.forEach(function(t){t.addEventListener('click',function(){tabs.forEach(function(x){x.setAttribute('aria-selected',x===t)});
  r.querySelectorAll('.adjv7__panel').forEach(function(p){p.hidden=p.id!==t.getAttribute('aria-controls')});});});})();
''', 'exam'))

# 8. Kafle przed FAQ
V.append(('Kafle z filmami przed FAQ',
 'Jeden duży kafel z filmem o kursie i mniejsze kafle o egzaminie i skrzyżowaniach, ułożone w nieregularną siatkę.',
 r'''
.adjv8{padding:clamp(48px,7vw,88px) 16px;background:#f4f6f9}
.adjv8__in{max-width:1180px;margin:0 auto}
.adjv8__h{display:flex;flex-wrap:wrap;align-items:end;justify-content:space-between;gap:12px;margin-bottom:24px}
.adjv8__h h2{font:800 clamp(26px,3vw,38px)/1.1 "Work Sans",sans-serif!important;color:var(--adj-navy)!important;max-width:18ch;text-align:left}
.adjv8__h a{color:var(--adj-navy)!important;font:600 15px/1 "Work Sans",sans-serif;text-decoration:underline;text-underline-offset:4px}
.adjv8__g{display:grid;grid-template-columns:2fr 1fr 1fr;grid-auto-rows:230px;gap:14px}
.adjv8__t{position:relative;display:block!important;width:100%!important;height:100%!important;min-height:180px;border-radius:16px;overflow:hidden;box-shadow:0 1px 0 rgba(33,49,74,.05),0 24px 44px -30px rgba(33,49,74,.55);transition:transform .25s var(--adj-ease)}
.adjv8__t--big{grid-row:span 2}
.adjv8__t--tall{grid-row:span 2}
.adjv8__t img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.adjv8__t--tall img{transform:scale(1.3)}
.adjv8__t::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,rgba(13,21,34,.9))}
.adjv8__t .adjv-play{position:absolute;left:16px;top:16px;width:46px;height:46px;z-index:1}
.adjv8__t .adjv-play svg{width:18px;height:18px}
.adjv8__t--big .adjv-play{width:72px;height:72px;left:24px;top:24px}.adjv8__t--big .adjv-play svg{width:28px;height:28px}
.adjv8__cap{position:absolute;left:16px;right:16px;bottom:14px;z-index:1;color:#fff;text-align:left}
.adjv8__cap strong{display:block;font:700 16px/1.25 "Work Sans",sans-serif}
.adjv8__t--big .adjv8__cap strong{font-size:clamp(20px,2vw,26px)}
.adjv8__cap small{font:500 13px/1 "Roboto",sans-serif;color:rgba(255,255,255,.7)}
@media (hover:hover) and (pointer:fine){.adjv8__t:hover{transform:translateY(-3px)}}
.adjv8__t:active{transform:scale(.98)}
@media (max-width:820px){.adjv8__g{grid-template-columns:1fr 1fr;grid-auto-rows:180px}.adjv8__t--big{grid-column:1/-1;grid-row:span 2}.adjv8__t--tall{grid-row:span 2}}
''', '', 'faq_before'))

# 9. Kinowy baner
V.append(('Kinowy baner na całą szerokość',
 'Pełnoszerokościowy pas z wolno przybliżanym kadrem z filmu i jednym przyciskiem. Mocny akcent w połowie strony.',
 r'''
.adjv9{width:100vw;margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);position:relative;overflow:hidden;min-height:clamp(380px,46vw,560px);display:grid;align-items:center;padding:48px 16px;background:var(--adj-navy-d);isolation:isolate}
.adjv9__bg{position:absolute;inset:-4%;background-size:cover;background-position:center;z-index:-2;animation:adjv9kb 22s var(--adj-ease) infinite alternate}
@keyframes adjv9kb{from{transform:scale(1)}to{transform:scale(1.09) translate(-1.5%,-1%)}}
.adjv9::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(13,21,34,.94) 0%,rgba(13,21,34,.72) 45%,rgba(13,21,34,.25) 100%)}
.adjv9__in{max-width:1180px;width:100%;margin:0 auto;color:#fff}
.adjv9__in small{display:block;font:700 13px/1 "Work Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--adj-brand);margin-bottom:16px}
.adjv9__in h2{font:800 clamp(30px,4.4vw,56px)/1.04 "Work Sans",sans-serif!important;color:#fff!important;max-width:14ch;margin-bottom:28px!important;text-align:left}
.adjv9__cta{display:inline-flex!important;align-items:center;gap:14px;padding:10px 26px 10px 10px!important;border-radius:999px;background:var(--adj-brand)!important;color:var(--adj-navy-d)!important;font:700 17px/1 "Work Sans",sans-serif!important;box-shadow:0 18px 40px -18px rgba(254,169,0,.8)!important;transition:transform .16s var(--adj-ease),background-color .2s var(--adj-ease)}
.adjv9__cta .adjv-play{width:48px;height:48px;background:var(--adj-navy-d);box-shadow:none}
.adjv9__cta .adjv-play svg{fill:var(--adj-brand);width:18px;height:18px}
@media (hover:hover) and (pointer:fine){.adjv9__cta:hover{background:var(--adj-brand-l)!important}}
.adjv9__cta:active{transform:scale(.97)}
''', '', 'steps_after'))

# 10. Pytania w 60 sekund
V.append(('Pytania w 60 sekund',
 'Przed FAQ lista praktycznych pytań, na które odpowiedzią jest krótki film ze skrzyżowania. Działa jak wideo-FAQ.',
 r'''
.adjv10{padding:clamp(48px,7vw,88px) 16px;background:#fff}
.adjv10__in{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,5vw,72px);align-items:start}
.adjv10__lead small{display:block;font:700 13px/1 "Work Sans",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#b87800;margin-bottom:14px}
.adjv10__lead h2{font:800 clamp(28px,3.2vw,42px)/1.08 "Work Sans",sans-serif!important;color:var(--adj-navy)!important;text-align:left;margin-bottom:14px!important}
.adjv10__lead p{font:400 16px/1.6 "Roboto",sans-serif;color:rgba(33,49,74,.75);max-width:38ch}
.adjv10__list{border-top:1px solid rgba(33,49,74,.12)}
.adjv10__q{display:grid!important;grid-template-columns:64px 1fr auto;align-items:center;gap:16px;width:100%!important;padding:16px 4px!important;border-bottom:1px solid rgba(33,49,74,.12)!important;text-align:left;transition:background-color .2s var(--adj-ease)}
.adjv10__q img{width:64px;height:64px;border-radius:12px;object-fit:cover;display:block}
.adjv10__q strong{font:700 17px/1.3 "Work Sans",sans-serif;color:var(--adj-navy)}
.adjv10__q small{display:block;font:500 13px/1 "Roboto",sans-serif;color:rgba(33,49,74,.55);margin-top:6px}
.adjv10__q .adjv-play{width:40px;height:40px;box-shadow:none}
.adjv10__q .adjv-play svg{width:15px;height:15px}
@media (hover:hover) and (pointer:fine){.adjv10__q:hover{background:#f6f8fb}}
.adjv10__q:active{background:#eef2f7}
@media (max-width:820px){.adjv10__in{grid-template-columns:1fr}}
''', '', 'faq_before'))


# ---------- HTML wstawek ----------
def hero_inner(nr, img_tag):
    if nr == 1:
        return (img_tag + f'<button class="adjv adjv1" type="button" {btn_attrs(PROMO[0])} data-inline aria-label="Odtwórz film o kursie">'
                f'<span class="adjv-play">{PLAY}</span>'
                f'<span class="adjv1__cap"><small>Film o kursie</small><strong>Zobacz, jak wygląda nauka jazdy w ADJ</strong></span></button>')
    return img_tag + (f'<button class="adjv adjv2" type="button" {btn_attrs(PROMO[0])}>'
            f'<span class="adjv-play">{PLAY}</span>Obejrzyj film o kursie</button>')

def kino():
    items = ''.join(
        f'<li><button class="vf__item{" is-active" if i==0 else ""}" type="button" data-id="{v[0]}" aria-pressed="{"true" if i==0 else "false"}">'
        f'<img src="{thumb(v[0],"mqdefault")}" alt="" loading="lazy" width="320" height="180">'
        f'<span class="vf__item-txt"><span class="vf__item-title">{v[1]}</span><span class="vf__item-meta">{v[2]}</span></span></button></li>'
        for i, v in enumerate([FOTEL, SWIATLA, PLYNY]))
    shorts = ''.join(
        f'<li><button class="vf__short" type="button" {btn_attrs(s[0], True)}><img src="{thumb(s[0])}" alt="" loading="lazy">'
        f'<span class="vf__chip">{s[2]}</span><span class="vf__short-t">{s[1]}</span><span class="vf__short-d">{s[3]}</span></button></li>' for s in SHORTS)
    return f'''<section id="filmy" class="adjv vf" aria-labelledby="vf-title"><div class="vf__inner">
<div class="vf__head"><p class="vf__eyebrow">Filmy instruktorów ADJ</p><h2 id="vf-title" class="vf__title">Zobacz kurs od środka, zanim się zapiszesz</h2></div>
<div class="vf__stage"><div class="vf__player" data-player><button class="vf__facade" type="button" data-facade aria-label="Odtwórz film">
<img src="{thumb(FOTEL[0])}" alt="" width="480" height="360"><span class="vf__play" aria-hidden="true">{PLAY}</span>
<span class="vf__now"><span class="vf__now-tag">Egzamin kat. B, Hyundai i20</span><span class="vf__now-title">{FOTEL[1]}</span></span></button></div>
<div class="vf__side"><ol class="vf__list" role="list">{items}</ol>
<a class="vf__cta" href="{FORM}"><span class="vf__cta-k">Kurs kat. B</span><span class="vf__cta-t">Zapisz się na kurs</span><span class="vf__cta-arr" aria-hidden="true">→</span></a></div></div>
<div class="vf__city"><div class="vf__city-head"><h3 class="vf__city-title">Miasto za kółkiem</h3><p class="vf__city-sub">Trudne skrzyżowania z tras egzaminacyjnych we Wrocławiu</p></div>
<ul class="vf__rail" role="list">{shorts}</ul>
<a class="vf__channel" href="https://www.youtube.com/@akademia_szkolen" target="_blank" rel="noopener">Wszystkie filmy na kanale YouTube <span aria-hidden="true">→</span></a></div></div></section>'''

def chip(v, vertical=False, label=None):
    t = label or v[1]
    d = v[3] if vertical else v[2]
    return (f'<button class="adjv adjv4" type="button" {btn_attrs(v[0], vertical)}><img src="{thumb(v[0],"mqdefault")}" alt="">'
            f'<span class="adjv4__p">{PLAY}</span>{t} <i>{d}</i></button>')

def floating():
    return (f'<div class="adjv adjv5" role="complementary" aria-label="Film"><button class="adjv5__x" type="button" aria-label="Zamknij">×</button>'
            f'<button class="adjv5__open" type="button" {btn_attrs(FOTEL[0])}><span class="adjv5__media"><img src="{thumb(FOTEL[0],"mqdefault")}" alt=""><span class="adjv-play">{PLAY}</span></span>'
            f'<span class="adjv5__txt"><small>Egzamin kat. B od środka</small><strong>{FOTEL[1]}</strong></span></button></div>')

def stories():
    items = [(FOTEL[0], 'Fotel', False), (SWIATLA[0], 'Światła', False), (PLYNY[0], 'Płyny', False)] + [(s[0], s[2], True) for s in SHORTS]
    li = ''.join(f'<li><button class="adjv6__s" type="button" {btn_attrs(i, v)}><span class="adjv6__ring"><img src="{thumb(i,"mqdefault")}" alt=""></span><span>{n}</span></button></li>' for i, n, v in items)
    return f'<section class="adjv adjv6" aria-label="Krótkie filmy"><div class="adjv6__in"><p class="adjv6__lead">Krótkie filmy<small>egzamin i trasy</small></p><ul class="adjv6__row" role="list">{li}</ul></div></section>'

def exam():
    tabs = [('t1', 'Ustawienie fotela', FOTEL), ('t2', 'Światła', SWIATLA), ('t3', 'Płyny', PLYNY), ('t4', 'Skrzyżowania', None)]
    tb = ''.join(f'<button class="adjv7__tab" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}" aria-controls="adjv7-{k}">{n}</button>' for i, (k, n, _) in enumerate(tabs))
    panels = ''
    for i, (k, n, v) in enumerate(tabs):
        hid = '' if i == 0 else ' hidden'
        if v:
            body = f'<button class="adjv7__v" type="button" {btn_attrs(v[0])} aria-label="Odtwórz: {v[1]}"><img src="{thumb(v[0])}" alt=""><span class="adjv-play">{PLAY}</span></button>'
        else:
            body = '<div class="adjv7__grid">' + ''.join(f'<button class="adjv7__sh" type="button" {btn_attrs(s[0], True)}><img src="{thumb(s[0])}" alt=""><span>{s[1]}</span></button>' for s in SHORTS[:3]) + '</div>'
        panels += f'<div class="adjv7__panel" id="adjv7-{k}" role="tabpanel"{hid}>{body}</div>'
    return f'<div class="adjv adjv7"><div class="adjv7__tabs" role="tablist">{tb}</div>{panels}</div>'

def bento():
    t = lambda cls, i, title, sub, v=False: (f'<button class="adjv8__t {cls}" type="button" {btn_attrs(i, v)}><img src="{thumb(i, "hqdefault")}" alt="" loading="lazy">'
                                             f'<span class="adjv-play">{PLAY}</span><span class="adjv8__cap"><strong>{title}</strong><small>{sub}</small></span></button>')
    g = (t('adjv8__t--big', PROMO[0], 'Zobacz, jak wygląda nauka jazdy w ADJ', 'Film o kursie') +
         t('', FOTEL[0], FOTEL[1], FOTEL[2]) +
         t('adjv8__t--tall', SHORTS[0][0], SHORTS[0][1], SHORTS[0][3], True) +
         t('', SWIATLA[0], SWIATLA[1], SWIATLA[2]))
    return (f'<section class="adjv adjv8"><div class="adjv8__in"><div class="adjv8__h"><h2>Kurs kat. B w filmach</h2>'
            f'<a href="https://www.youtube.com/@akademia_szkolen" target="_blank" rel="noopener">Wszystkie filmy na YouTube</a></div><div class="adjv8__g">{g}</div></div></section>')

def banner():
    return (f'<section class="adjv adjv9"><div class="adjv9__bg" style="background-image:url(https://www.naukajazdy.wroc.pl/wp-content/uploads/2022/04/prawo-jazdy-kat-b-wroclaw.webp)"></div>'
            f'<div class="adjv9__in"><small>Film o kursie</small><h2>Zobacz, jak wygląda nauka jazdy w ADJ</h2>'
            f'<button class="adjv9__cta" type="button" {btn_attrs(PROMO[0])}><span class="adjv-play">{PLAY}</span>Obejrzyj film</button></div></section>')

def qa():
    qs = [(SHORTS[1], 'Jak zawracać na Rondzie Pionierów?'), (SHORTS[0], 'Jak skręcić w lewo na rondzie na Jagodnie?'),
          (SHORTS[4], 'Jak bezpiecznie przejechać przez tory?'), (SHORTS[3], 'Jak przejechać mini rondo?'), (SHORTS[2], 'Jak zjechać z Armii Krajowej w Krakowską?')]
    li = ''.join(f'<li><button class="adjv10__q" type="button" {btn_attrs(s[0], True)}><img src="{thumb(s[0],"mqdefault")}" alt="">'
                 f'<span><strong>{q}</strong><small>Film {s[3]}</small></span><span class="adjv-play">{PLAY}</span></button></li>' for s, q in qs)
    return (f'<section class="adjv adjv10"><div class="adjv10__in"><div class="adjv10__lead"><small>Pytania w 60 sekund</small>'
            f'<h2>Trudne miejsca z tras egzaminacyjnych</h2><p>Instruktorzy ADJ pokazują, jak przejechać skrzyżowania, na których kursanci mylą się najczęściej.</p></div>'
            f'<ul class="adjv10__list" role="list">{li}</ul></div></section>')

KINO_CSS = (BASE.parent / 'vf.css').read_text(encoding='utf-8') + r'''
.vf{width:100vw;margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw)}
.vf__title,.vf__city-title{color:#fff!important;text-align:left}
#filmy .vf__eyebrow,#filmy .vf__channel{color:#FEA900!important}
#filmy .vf__item img{width:120px!important;height:auto!important;aspect-ratio:16/9}
#filmy .vf__facade img,#filmy .vf__short img{height:100%!important}
#filmy .vf__short{all:unset;box-sizing:border-box;position:relative;display:flex;flex-direction:column;justify-content:flex-end;aspect-ratio:9/16;border-radius:14px;overflow:hidden;color:#fff;cursor:pointer;scroll-snap-align:start;background:#0d1522;width:100%}
@media (max-width:900px){#filmy .vf__list{padding:0 16px 6px!important}}
'''
KINO_JS = (BASE.parent / 'vf.js').read_text(encoding='utf-8')


# ---------- składanie ----------
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
    s = re.sub(r'(<iframe[^>]*?)\sdata-src="([^"]+)"', lambda m: m.group(1) + ' src="' + m.group(2) + '"', s)
    return s

def find_after(s, needle, start=0):
    i = s.find(needle, start); assert i > 0, needle; return i

def build(nr, name, desc, css, js, kind, base):
    s = base
    if kind == 'hero':
        i = find_after(s, '<div class="kurs-img-wrapper">')
        m = re.compile(r'<img[^>]*>').search(s, i)
        s = s[:m.start()] + hero_inner(nr, m.group(0)) + s[m.end():]
        s = s.replace('<div class="kurs-img-wrapper">', '<div class="kurs-img-wrapper" data-inline-box style="position:relative">', 1)
    elif kind == 'steps_after':
        k = find_after(s, '<div style="height:50px" aria-hidden="true" class="wp-block-spacer"></div><div class="wp-block-columns', find_after(s, 'Krok 8:'))
        s = s[:k] + (kino() if nr == 3 else banner()) + s[k:]
        if nr == 3: css += KINO_CSS; js += KINO_JS
    elif kind == 'steps_chips':
        for step, ch in [('Krok 5:', chip(SHORTS[0], True, 'Trudne skrzyżowanie na trasie')), ('Krok 6:', chip(FOTEL)), ('Krok 7:', chip(SWIATLA) + chip(PLYNY))]:
            p = find_after(s, step); e = s.find('</p>', p)
            s = s[:e] + '<br>' + ch + s[e:]
    elif kind == 'floating':
        s = s.replace('</body>', floating() + '</body>', 1)
    elif kind == 'stories':
        k = find_after(s, '<div class="opinie-slider container"'); s = s[:k] + stories() + s[k:]
    elif kind == 'exam':
        h = find_after(s, 'Jak wygląda egzamin na prawo jazdy kat. B'); e = s.find('</h2>', h) + 5
        s = s[:e] + exam() + s[e:]
    elif kind == 'faq_before':
        blk = find_after(s, '<div class="container"><h2>FAQ')
        s = s[:blk] + (bento() if nr == 8 else qa()) + s[blk:]
    nav = (f'<div class="adjv-bar"><span><b>Wariant {nr} z 10</b>{name}</span>'
           f'<a href="v{(nr-2)%10+1:02d}.html" aria-label="Poprzedni">‹</a><a href="index.html" aria-label="Lista wariantów">≡</a>'
           f'<a href="v{nr%10+1:02d}.html" aria-label="Następny">›</a></div>')
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{COMMON_CSS}{css}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', nav + f'<script>{COMMON_JS}{js}</script>\n</body>', 1)
    (BASE / f'v{nr:02d}.html').write_text(s, encoding='utf-8')

def index():
    cards = ''.join(f'<li><a href="v{n:02d}.html"><span class="n">{n:02d}</span><span><strong>{nm}</strong><small>{d}</small></span></a></li>'
                    for n, (nm, d, *_ ) in enumerate(V, 1))
    return f'''<!doctype html><html lang="pl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>ADJ, filmy na stronie: 10 wariantów</title><link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>body{{margin:0;background:#f4f6f9;color:#21314a;font-family:"Work Sans",sans-serif}}main{{max-width:880px;margin:0 auto;padding:48px 16px 80px}}
h1{{font-size:clamp(28px,4vw,40px);line-height:1.1;margin:0 0 10px}}p{{margin:0 0 28px;color:rgba(33,49,74,.7);font-size:16px;line-height:1.55}}
ul{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}a{{display:grid;grid-template-columns:56px 1fr;gap:16px;align-items:center;padding:18px 20px;border-radius:14px;background:#fff;color:inherit;text-decoration:none;box-shadow:0 1px 0 rgba(33,49,74,.05),0 18px 34px -28px rgba(33,49,74,.5);transition:transform .2s cubic-bezier(.23,1,.32,1)}}
a:hover{{transform:translateY(-2px)}}a:active{{transform:scale(.99)}}a:focus-visible{{outline:3px solid #FEA900;outline-offset:3px}}.n{{font-weight:800;font-size:26px;color:#FEA900}}strong{{display:block;font-size:18px;margin-bottom:4px}}small{{display:block;font-size:14px;line-height:1.45;color:rgba(33,49,74,.65)}}</style></head>
<body><main><h1>Filmy na stronie kursu kat. B: 10 wariantów</h1><p>Każdy wariant to kopia obecnej strony kursu z innym sposobem pokazania filmów z kanału ADJ. Na dole każdej strony jest pasek do przechodzenia między wariantami.</p><ul>{cards}</ul></main></body></html>'''

if __name__ == '__main__':
    base = prep((BASE / '_base.html').read_text(encoding='utf-8'))
    for n, v in enumerate(V, 1):
        build(n, *v, base)
    (BASE / 'index.html').write_text(index(), encoding='utf-8')
    print('ok', len(V))
