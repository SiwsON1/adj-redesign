# Nowe filmy z Dropboxa NETIM (10.2026) w języku wizualnym naukajazdy.wroc.pl:
# karty białe 14px z ramką #e5e5e5, ikony w żółtych kołach 50px, nagłówki Work Sans 800, tło #fafafa.
# Wyjście: kurs-16-lat.html, glowna-reklama.html, glowna.html.
import re
from build import BASE, FORM, PLAY, prep, at, ins

Y = '#FEA900'
ICO = {
 'trophy': '<path d="M8 4h8v4a4 4 0 0 1-8 0zM8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 12v4M9 20h6M10 16h4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
 'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="10" r="2.4" fill="currentColor"/>',
 'road': '<path d="M9 3 6 21M15 3l3 18M12 5v2.5M12 11v2.5M12 17v2" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
}
def icon(k):
    return f'<span class="adjn-ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICO[k]}</svg></span>'
PLAYB = f'<span class="adjn-play">{PLAY}</span>'
X = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'

CSS = r'''
.adjn,.adjn *{box-sizing:border-box}
.adjn{font-family:"Work Sans",sans-serif;color:#000}
:where(.adjn) button{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:pointer}
:where(.adjn) img,:where(.adjn) video{max-width:none;margin:0}
.adjn ul{list-style:none!important;margin:0!important;padding:0!important}.adjn li{margin:0!important;padding:0!important;list-style:none!important}
.adjn :focus-visible{outline:3px solid #FEA900;outline-offset:3px}
.adjn-play{display:grid;place-items:center;width:64px;height:64px;border-radius:50%;background:#FEA900;box-shadow:0 8px 20px -8px rgba(0,0,0,.45);transition:transform .15s cubic-bezier(.23,1,.32,1)}
.adjn-play svg{width:24px;height:24px;fill:#fff;margin-left:3px}
.adjn-ico{flex:0 0 50px;width:50px;height:50px;border-radius:50%;background:#FEA900;color:#fff;display:grid;place-items:center}
.adjn-ico svg{width:24px;height:24px}
.adjn-btn{display:inline-flex!important;align-items:center;justify-content:center;min-height:48px;padding:0 28px!important;border-radius:6px!important;background:#FEA900!important;color:#fff!important;font:600 17px/1 "Work Sans",sans-serif!important;text-decoration:none!important;transition:background-color .2s,transform .15s cubic-bezier(.23,1,.32,1)}
.adjn-btn:hover{background:#e59800!important}.adjn-btn:active{transform:scale(.97)}

/* film pionowy w karcie (gra w miejscu) */
.adjn-vid{position:relative;width:100%;aspect-ratio:9/16;border-radius:14px;overflow:hidden;background:#1a1a1a;border:1px solid #e5e5e5}
.adjn-vid video{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;display:block}
.adjn-vid__go{position:absolute!important;inset:0;z-index:2;display:grid!important;place-items:center;width:100%!important;height:100%!important}
.adjn-vid__go::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)}
.adjn-vid__go .adjn-play{position:relative}
.adjn-vid__t{position:absolute;left:14px;right:14px;bottom:12px;color:#fff;font:600 14px/1.3 "Work Sans",sans-serif;text-align:left}
@media (hover:hover) and (pointer:fine){.adjn-vid__go:hover .adjn-play{transform:scale(1.07)}}
.adjn-vid__go:active .adjn-play{transform:scale(.94)}
.adjn-vid.is-playing .adjn-vid__go{display:none!important}

/* kat. B: film w kolumnie „Wymagania” */
.adjn16{width:min(340px,100%);margin:0 auto}
@media (max-width:780px){.adjn16{width:min(280px,100%);margin:8px auto 24px}}
.adjn16__cap{margin:12px 0 0!important;font:500 14px/1.4 "Work Sans",sans-serif;color:#555;text-align:center}

/* strona główna: pas z zapisem i reklamą w telefonie */
.adjnr{padding:150px 16px 72px}
.adjnr__card{position:relative;max-width:1200px;margin:0 auto;display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:64px;align-items:center;padding:48px 64px;background:#FEA900;border-radius:14px}
.adjnr h2{margin:0 0 12px!important;font:800 36px/1.15 "Work Sans",sans-serif!important;color:#1a1a1a!important;text-align:left!important;max-width:20ch}
.adjnr__lead{margin:0 0 28px!important;padding:0!important;font:500 17px/1.55 "Work Sans",sans-serif;color:#1a1a1a;text-align:left!important;max-width:46ch}
.adjnr__cta{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.adjnr__b1{display:inline-flex!important;align-items:center;min-height:52px;padding:0 28px!important;border-radius:6px!important;background:#1a1a1a!important;color:#fff!important;font:600 17px/1 "Work Sans",sans-serif!important;text-decoration:none!important;transition:background-color .2s,transform .15s cubic-bezier(.23,1,.32,1)}
.adjnr__b1:hover{background:#000!important}.adjnr__b1:active{transform:scale(.97)}
.adjnr__b2{display:inline-flex!important;align-items:center;gap:10px;min-height:52px;padding:0 22px!important;border-radius:6px!important;background:#fff!important;color:#1a1a1a!important;font:600 17px/1 "Work Sans",sans-serif!important;text-decoration:none!important;font-variant-numeric:tabular-nums;transition:transform .15s cubic-bezier(.23,1,.32,1),box-shadow .2s}
.adjnr__b2 svg{width:18px;height:18px}.adjnr__b2:hover{box-shadow:0 8px 20px -10px rgba(0,0,0,.35)}.adjnr__b2:active{transform:scale(.97)}
.adjnr__media{align-self:end;margin:-200px 0 -48px}
.adjnr__ph{position:relative;padding:9px;border-radius:38px;background:#141414;box-shadow:0 30px 60px -28px rgba(0,0,0,.55)}
.adjnr__ph::before{content:"";position:absolute;left:50%;top:16px;z-index:2;width:70px;height:18px;margin-left:-35px;border-radius:12px;background:#141414}
.adjnr__ph video{display:block;width:100%!important;aspect-ratio:9/16;object-fit:cover;border-radius:30px;background:#222}
@media (max-width:900px){.adjnr{padding:40px 16px 56px}.adjnr__card{grid-template-columns:1fr;gap:28px;padding:0 20px 32px}.adjnr__media{order:-1;width:min(220px,62vw);margin:-24px auto 0;align-self:auto}.adjnr h2{font-size:28px!important}}
@media (max-width:900px){.adjnr{padding-top:64px}.adjnr__media{margin-top:-48px}}

/* strona główna: filmy, bliźniak widżetu „Opinie klientów” (te same wymiary i style) */
.adjnf{padding:16px 0}
.adjnf__in{max-width:1320px;margin:0 auto;padding:0 30px}
.adjnf h2{margin:0!important;font:700 20px/1.5 "Work Sans",sans-serif!important;color:#000!important;text-align:center!important}
.adjnf__line{display:block;width:30px;height:1px;margin:12.8px auto 30px;background:#FEA900}
.adjnf__box{display:grid;grid-template-columns:315px minmax(0,1fr);align-items:center}
.adjnf__head{display:flex;gap:12px;align-items:flex-start;padding:16px}
.adjnf__logo{flex:0 0 46px;width:46px;height:46px;border-radius:50%;background:#fff;box-shadow:0 0 2px rgba(0,0,0,.12),0 2px 4px rgba(0,0,0,.24);display:grid;place-items:center;overflow:hidden}
.adjnf__logo img{width:40px!important;height:auto!important}
.adjnf__name{font:700 16px/1.3 "Work Sans",sans-serif;color:#333}
.adjnf__meta{margin:6px 0 10px!important;padding:0!important;font:400 16px/1.4 "Work Sans",sans-serif;color:#777;text-align:left!important}
.adjnf__pill{display:inline-flex!important;align-items:center;gap:6px;padding:5px 12px 6px!important;border-radius:27px!important;background:#FEA900!important;color:#1a1a1a!important;font:600 15px/1.2 "Work Sans",sans-serif!important;text-decoration:none!important;box-shadow:0 0 2px rgba(0,0,0,.12),0 2px 4px rgba(0,0,0,.24);transition:transform .15s cubic-bezier(.23,1,.32,1)}
.adjnf__pill:hover{background:#e59800!important}.adjnf__pill:active{transform:scale(.97)}
.adjnf__wrap{position:relative;min-width:0}
.adjnf__row{display:flex;gap:4px;overflow-x:auto;padding:4px 3px 8px!important;margin:0!important;scroll-snap-type:x mandatory;scroll-behavior:smooth;scrollbar-width:none}
.adjnf__row::-webkit-scrollbar{display:none}
.adjnf .adjnf__row>li{flex:0 0 301px;padding:4px 3px!important;scroll-snap-align:start;display:flex!important}
.adjnf__c{display:block!important;width:100%!important;padding:16px!important;border-radius:8px;background:#f4f4f4!important;box-shadow:0 0 2px rgba(0,0,0,.12),0 2px 4px rgba(0,0,0,.24);text-align:left;transition:box-shadow .2s}
.adjnf__m{position:relative;display:block;aspect-ratio:1/1;border-radius:6px;overflow:hidden;background:#1a1a1a}
.adjnf__m img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;object-position:50% 22%;transition:transform .5s cubic-bezier(.23,1,.32,1)}
.adjnf__m .adjn-play{position:absolute;left:50%;top:50%;z-index:1;transform:translate(-50%,-50%);width:52px;height:52px}
.adjnf__m .adjn-play svg{width:20px;height:20px}
.adjnf__t{display:block;margin-top:12px;font:700 16px/1.35 "Work Sans",sans-serif;color:#154fc1}
.adjnf__d{display:block;margin-top:4px;font:400 13px/1.3 "Work Sans",sans-serif;color:#555}
@media (hover:hover) and (pointer:fine){.adjnf__c:hover{box-shadow:0 0 2px rgba(0,0,0,.12),0 6px 14px rgba(0,0,0,.22)}.adjnf__c:hover img{transform:scale(1.04)}.adjnf__c:hover .adjn-play{transform:translate(-50%,-50%) scale(1.07)}}
.adjnf__c:active{transform:scale(.99)}
.adjnf__arr{position:absolute;top:50%;z-index:2;width:34px!important;height:34px!important;margin-top:-17px;padding:8px!important;border-radius:50%!important;background:#f5f5f5!important;color:#555!important;display:grid!important;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.15);transition:opacity .2s,transform .15s}
.adjnf__arr svg{width:16px;height:16px}.adjnf__arr:active{transform:scale(.92)}
.adjnf__arr[disabled]{opacity:0;pointer-events:none}
.adjnf__prev{left:-17px}.adjnf__next{right:-17px}
@media (max-width:900px){.adjnf__in{padding:0 16px}.adjnf__box{grid-template-columns:1fr}.adjnf__head{padding:0 0 12px}.adjnf .adjnf__row>li{flex:0 0 min(301px,78%)}.adjnf__row{margin:0 -16px!important;padding:4px 13px 8px!important;scroll-padding-inline:16px}.adjnf__arr{display:none!important}}

/* okno z filmem pionowym */
.adjn-modal{position:fixed;inset:0;z-index:2147483000;display:grid;place-items:center;padding:64px 16px 16px;background:rgba(17,17,17,.88);opacity:0;transition:opacity .2s cubic-bezier(.23,1,.32,1)}
.adjn-modal.is-open{opacity:1}
.adjn-modal__box{position:relative;height:min(82dvh,760px);aspect-ratio:9/16;max-width:100%;border-radius:14px;overflow:hidden;background:#000}
.adjn-modal__box video,.adjn-modal__box iframe{position:absolute;inset:0;width:100%;height:100%;border:0;object-fit:contain;background:#000}
.adjn-modal__x{position:absolute;right:max(16px,calc(50% - min(82dvh,760px)*9/32 - 56px));top:12px;width:44px;height:44px;border-radius:50%;display:grid;place-items:center;background:#fff!important;color:#000!important;border:0;cursor:pointer}
.adjn-modal__x svg{width:20px;height:20px}
@media (prefers-reduced-motion:reduce){.adjn *,.adjn-modal{transition:none!important}}
'''

JS = r'''
(function(){
  // film w karcie: start po kliknięciu, z dźwiękiem
  document.querySelectorAll('.adjn-vid[data-click]').forEach(function(box){ var v=box.querySelector('video');
    box.querySelector('.adjn-vid__go').addEventListener('click',function(){ box.classList.add('is-playing'); v.controls=true; v.muted=false; v.play(); }); });
  // reklama: bez dźwięku, w pętli, tylko gdy widoczna
  var still=matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-loop] video').forEach(function(v){ if(still) return;
    new IntersectionObserver(function(es){ es.forEach(function(e){ e.isIntersecting ? v.play().catch(function(){}) : v.pause() }) },{threshold:.3}).observe(v); });
  // okno z filmem pionowym
  var y=0;
  function open(t){
    var m=document.createElement('div'); m.className='adjn-modal'; m.setAttribute('role','dialog'); m.setAttribute('aria-modal','true'); m.setAttribute('aria-label',t.dataset.title||'Film');
    var src=t.dataset.kind==='mp4' ? '<video src="'+t.dataset.src+'" controls autoplay playsinline></video>'
      : '<iframe src="'+t.dataset.src+'" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen title="'+(t.dataset.title||'Film')+'"></iframe>';
    m.innerHTML='<button class="adjn-modal__x" type="button" aria-label="Zamknij film">'+%X%+'</button><div class="adjn-modal__box">'+src+'</div>';
    var last=document.activeElement; y=scrollY; var b=document.body.style; b.position='fixed'; b.top=-y+'px'; b.left=b.right='0'; b.width='100%';
    document.body.appendChild(m); requestAnimationFrame(function(){ m.classList.add('is-open') }); m.querySelector('.adjn-modal__x').focus();
    function close(){ document.removeEventListener('keydown',key); m.remove(); b.position=b.top=b.left=b.right=b.width=''; document.documentElement.style.scrollBehavior='auto'; scrollTo(0,y); if(last) last.focus({preventScroll:true}); }
    function key(e){ if(e.key==='Escape') close(); if(e.key==='Tab'){ e.preventDefault(); m.querySelector('.adjn-modal__x').focus(); } }
    m.addEventListener('click',function(e){ if(e.target===m||e.target.closest('.adjn-modal__x')) close(); });
    document.addEventListener('keydown',key);
  }
  document.querySelectorAll('.adjnf__wrap').forEach(function(w){ var r=w.querySelector('.adjnf__row'), pv=w.querySelector('.adjnf__prev'), nx=w.querySelector('.adjnf__next');
    function st(){ pv.disabled=r.scrollLeft<8; nx.disabled=r.scrollLeft+r.clientWidth>=r.scrollWidth-8; }
    pv.addEventListener('click',function(){ r.scrollBy({left:-r.clientWidth*.8}) }); nx.addEventListener('click',function(){ r.scrollBy({left:r.clientWidth*.8}) });
    r.addEventListener('scroll',st,{passive:true}); st(); });
  document.addEventListener('click',function(e){ var t=e.target.closest('.adjnf__c'); if(!t) return; e.preventDefault(); open(t); });
})();
'''.replace('%X%', repr(X))

def vid_click(src, poster, label, title):
    return (f'<div class="adjn-vid" data-click><video src="{src}" poster="{poster}" preload="none" playsinline></video>'
            f'<button class="adjn-vid__go" type="button" aria-label="{label}">{PLAYB}</button></div>')

def kurs16_media():
    return (f'<div class="adjn adjn16">{vid_click("media/16-lat.mp4", "media/16-lat.jpg", "Odtwórz film", "")}'
            f'</div>')

def reklama():
    phone = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z" fill="currentColor"/></svg>'
    return (f'<section class="adjn adjnr" aria-labelledby="adjnr-h"><div class="adjnr__card"><div>'
            f'<h2 id="adjnr-h">Zacznij kurs prawa jazdy we Wrocławiu</h2>'
            f'<p class="adjnr__lead">Zapisz się online albo zadzwoń. Pomożemy wybrać termin i tryb zajęć.</p>'
            f'<div class="adjnr__cta"><a class="adjnr__b1" href="{FORM}">Zapisz się na kurs</a>'
            f'<a class="adjnr__b2" href="tel:+48575757408">{phone}575 757 408</a></div></div>'
            f'<div class="adjnr__media"><div class="adjnr__ph" data-loop><video src="media/reklama-10a.mp4" poster="media/reklama-10a.jpg" muted loop playsinline preload="metadata" aria-hidden="true"></video></div></div>'
            f'</div></section>')

TT = 'https://www.tiktok.com/player/v1/{}?autoplay=1&loop=1&music_info=0&description=0&rel=0&native_context_menu=0'
FILMS = [
    ('mp4', 'media/16-lat.mp4', 'media/16-lat.jpg', 'Kurs od 16 lat i 9 miesięcy', '0:16 · Instruktorka ADJ', True),
    ('tt', TT.format('7543984782145867030'), 'img/tt/7543984782145867030.jpg', 'Witamy w Akademii', 'TikTok ADJ', False),
    ('yt', 'https://www.youtube-nocookie.com/embed/MVWxbNE8Wwk?autoplay=1&rel=0&playsinline=1&cc_load_policy=1&cc_lang_pref=pl', 'https://i.ytimg.com/vi/MVWxbNE8Wwk/oardefault.jpg', 'Jak wygląda egzamin praktyczny', '0:51 · Instruktor ADJ', False),
    ('tt', TT.format('7556221278558883094'), 'img/tt/7556221278558883094.jpg', 'Jak nie robić łuku', 'TikTok ADJ', False),
    ('tt', TT.format('7543984156921908502'), 'img/tt/7543984156921908502.jpg', 'Jakich butów nie nosić na motocykl', 'TikTok ADJ', False),
    ('tt', TT.format('7543981236197297430'), 'img/tt/7543981236197297430.jpg', 'Instruktor kontra złamany paznokieć', 'TikTok ADJ', False),
]

CHEV_L = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m15 5-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m9 5 7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def filmy():
    li = ''.join(
        f'<li><button class="adjnf__c" type="button" data-kind="{k}" data-src="{s}" data-title="{t}" aria-label="Odtwórz film: {t}">'
        f'<span class="adjnf__m"><img src="{p}" alt="" loading="lazy">{PLAYB}</span>'
        f'<span class="adjnf__t">{t}</span><span class="adjnf__d">{m}</span></button></li>'
        for k, s, p, t, m, n in FILMS)
    logo = 'https://www.naukajazdy.wroc.pl/wp-content/themes/akademia_custom/assets/img/logo_ADJ.png'
    return (f'<section class="adjn adjnf" aria-labelledby="adjnf-h"><div class="adjnf__in"><h2 id="adjnf-h">Filmy instruktorów</h2><span class="adjnf__line"></span>'
            f'<div class="adjnf__box"><div class="adjnf__head"><span class="adjnf__logo"><img src="{logo}" alt=""></span><div>'
            f'<div class="adjnf__name">Akademia Dobrej Jazdy Wrocław</div><p class="adjnf__meta">Krótkie filmy z placu, z trasy i z ośrodka</p>'
            f'<a class="adjnf__pill" href="https://www.tiktok.com/@akademiadobrejjazdy" target="_blank" rel="noopener">Zobacz nasz TikTok</a></div></div>'
            f'<div class="adjnf__wrap"><button class="adjnf__arr adjnf__prev" type="button" aria-label="Poprzednie filmy" disabled>{CHEV_L}</button>'
            f'<ul class="adjnf__row" role="list">{li}</ul>'
            f'<button class="adjnf__arr adjnf__next" type="button" aria-label="Następne filmy">{CHEV_R}</button></div></div></div></section>')

def page(src, out, edit):
    s = prep((BASE / src).read_text(encoding='utf-8'))
    s = edit(s)
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{CSS}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', f'<script>{JS}</script>\n</body>', 1)
    (BASE / out).write_text(s, encoding='utf-8')

def edit_kurs(s):
    w = at(s, 'Wymagania na kurs prawa jazdy kat. B')
    a = s.rfind('<div class="wp-block-columns', 0, w)
    f1 = s.find('<figure', a); f2 = s.find('</figure>', f1) + len('</figure>')
    assert a < f1 < w
    return s[:f1] + kurs16_media() + s[f2:]

def edit_reklama(s):
    sec = s.rfind('<section', 0, at(s, 'Skuteczność, doświadczenie'))
    end = s.find('</section>', sec) + len('</section>')
    return ins(s, end, reklama())

def edit_filmy(s):
    return ins(s, at(s, '<section class="google-reviews"'), filmy())

if __name__ == '__main__':
    page('_base.html', 'kurs-obok-wymagan.html', edit_kurs)
    page('_home_base.html', 'glowna-pod-kartami.html', edit_reklama)
    page('_home_base.html', 'glowna-przed-opiniami.html', edit_filmy)
    print('ok')
