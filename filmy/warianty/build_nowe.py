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

/* strona główna: filmy 9:16 (tokeny strony: nagłówek 20/700 + kreska 30x1, karta grid-card r10 cień 0 0 14px 4px) */
.adjnf{padding:24px 0 40px}
.adjnf__in{max-width:1200px;margin:0 auto;padding:0 30px}
.adjnf h2{margin:0!important;font:700 20px/1.5 "Work Sans",sans-serif!important;color:#000!important;text-align:center!important}
.adjnf__line{display:block;width:30px;height:1px;margin:12.8px auto 32px;background:#FEA900}
.adjnf__wrap{position:relative}
.adjnf__row{display:grid;grid-auto-flow:column;grid-auto-columns:calc((100% - 80px)/5);gap:20px;overflow-x:auto;padding:16px 16px 24px!important;margin:-16px -16px 0!important;scroll-snap-type:x mandatory;scroll-padding-inline:16px;scroll-behavior:smooth;scrollbar-width:none}
.adjnf__row::-webkit-scrollbar{display:none}
.adjnf .adjnf__row>li{scroll-snap-align:start;display:block!important}
.adjnf__c{position:relative;display:block!important;width:100%!important;aspect-ratio:9/16;border-radius:10px!important;overflow:hidden;background:#1a1a1a!important;box-shadow:0 0 14px 4px rgba(66,66,66,.2);text-align:left;transition:transform .3s cubic-bezier(.23,1,.32,1),box-shadow .3s cubic-bezier(.23,1,.32,1)}
.adjnf__c img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover;transition:transform .6s cubic-bezier(.23,1,.32,1)}
.adjnf__c::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 55%,rgba(0,0,0,.72) 100%)}
.adjnf__c .adjn-play{position:absolute;left:50%;top:50%;z-index:2;transform:translate(-50%,-50%);width:52px;height:52px}
.adjnf__c .adjn-play svg{width:20px;height:20px}
.adjnf__t{position:absolute;left:14px;right:14px;bottom:14px;z-index:2;font:700 15px/1.3 "Work Sans",sans-serif;color:#fff}
@media (hover:hover) and (pointer:fine){.adjnf__c:hover{transform:translateY(-6px);box-shadow:0 0 14px 4px rgba(66,66,66,.2),0 24px 40px -24px rgba(0,0,0,.45)}.adjnf__c:hover img{transform:scale(1.04)}.adjnf__c:hover .adjn-play{transform:translate(-50%,-50%) scale(1.08)}}
.adjnf__c:active{transform:scale(.98)}
.adjnf__arr{position:absolute;top:50%;z-index:3;width:34px!important;height:34px!important;margin-top:-17px;border-radius:50%!important;background:#f5f5f5!important;color:#444!important;display:grid!important;place-items:center;box-shadow:0 2px 6px rgba(0,0,0,.15);transition:opacity .2s,transform .15s}
.adjnf__arr svg{width:16px;height:16px}.adjnf__arr:active{transform:scale(.92)}
.adjnf__arr[disabled]{opacity:0;pointer-events:none}
.adjnf__prev{left:-17px}.adjnf__next{right:-17px}
.adjnf__more{display:flex;justify-content:center;margin-top:28px}
.adjnf__more a{display:inline-flex!important;align-items:center;min-height:44px;padding:0 20px!important;border-radius:6px!important;background:#FEA900!important;color:#fff!important;font:600 16px/1 "Work Sans",sans-serif!important;text-decoration:none!important;transition:background-color .2s,transform .15s}
.adjnf__more a:hover{background:#e59800!important}.adjnf__more a:active{transform:scale(.97)}
@media (max-width:1100px){.adjnf__row{grid-auto-columns:calc((100% - 60px)/4)}}
@media (max-width:860px){.adjnf__row{grid-auto-columns:calc((100% - 40px)/3)}}
@media (max-width:640px){.adjnf__in{padding:0 16px}.adjnf__row{grid-auto-columns:62%;gap:14px}.adjnf__arr{display:none!important}.adjnf__t{font-size:15px}}

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
    ('mp4', 'media/16-lat.mp4', 'media/16-lat.jpg', 'Zacznij kurs przed 17. urodzinami', '0:16 · Instruktorka ADJ', True),
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
        f'<img src="{p}" alt="" loading="lazy">{PLAYB}<span class="adjnf__t">{t}</span></button></li>'
        for k, s, p, t, m, n in FILMS)
    return (f'<section class="adjn adjnf" aria-labelledby="adjnf-h"><div class="adjnf__in"><h2 id="adjnf-h">Filmy instruktorów</h2><span class="adjnf__line"></span>'
            f'<div class="adjnf__wrap"><button class="adjnf__arr adjnf__prev" type="button" aria-label="Poprzednie filmy" disabled>{CHEV_L}</button>'
            f'<ul class="adjnf__row" role="list">{li}</ul>'
            f'<button class="adjnf__arr adjnf__next" type="button" aria-label="Następne filmy">{CHEV_R}</button></div>'
            f'<div class="adjnf__more"><a href="https://www.youtube.com/@akademia_szkolen" target="_blank" rel="noopener">Pokaż więcej filmów</a></div></div></section>')

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
    return ins(s, at(s, '<section class="blog-excerpts container">'), filmy())

if __name__ == '__main__':
    page('_base.html', 'kurs-obok-wymagan.html', edit_kurs)
    page('_home_base.html', 'glowna-pod-kartami.html', edit_reklama)
    page('_home_base.html', 'glowna-przed-opiniami.html', edit_filmy)
    print('ok')


# ---------- razem-nowe: nowe filmy z Dropboxa w trzech miejscach strony kursu, z oznaczeniami ----------
SPOT_CSS = r'''
[data-spot]{position:relative;outline:3px dashed #FEA900;outline-offset:10px;border-radius:12px;scroll-margin-top:240px}
[data-spot]::before{content:attr(data-spot);position:absolute;z-index:20;left:14px;top:-34px;padding:7px 12px;border-radius:999px;background:#1a1a1a;color:#FEA900;font:700 13px/1 "Work Sans",sans-serif;white-space:nowrap;pointer-events:none}
#miejsce-1::before{top:14px}
body.spots-off [data-spot]{outline:0}body.spots-off [data-spot]::before{display:none}
.spotnav{position:fixed;left:50%;bottom:16px;z-index:2147482000;transform:translateX(-50%);display:flex;align-items:center;gap:6px;padding:6px;border-radius:999px;background:#1a1a1a;box-shadow:0 18px 40px -16px rgba(0,0,0,.6);font:600 14px/1 "Work Sans",sans-serif;max-width:calc(100vw - 16px);overflow-x:auto;scrollbar-width:none}
.spotnav span{color:#fff;padding:0 8px 0 10px;white-space:nowrap}
.spotnav a,.spotnav button{display:inline-flex;align-items:center;gap:8px;min-height:40px;padding:0 14px;border-radius:999px;background:rgba(255,255,255,.1);color:#fff!important;text-decoration:none!important;white-space:nowrap;border:0;font:inherit;cursor:pointer;transition:background-color .2s,transform .15s}
.spotnav a b{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#FEA900;color:#1a1a1a;font-size:12px}
.spotnav a:hover,.spotnav button:hover{background:rgba(255,255,255,.2)}.spotnav a:active,.spotnav button:active{transform:scale(.96)}
.spotnav :focus-visible{outline:3px solid #FEA900;outline-offset:2px}
@media (max-width:700px){.spotnav span,.spotnav a i{display:none}}
/* 1: film w miejscu zdjęcia na górze (pętla bez dźwięku) */
.adjh-box{position:absolute;inset:0;z-index:1;border-radius:inherit;overflow:hidden;display:grid;place-items:center;background:#1a1a1a}
.adjh-box::before{content:"";position:absolute;inset:-40px;background:var(--bg) center/cover;filter:blur(28px) brightness(.55);transform:scale(1.1)}
.adjh-box video.adjh-loop{position:absolute!important;top:0;bottom:0;left:50%;transform:translateX(-50%);height:100%!important;width:auto!important;max-width:none!important;aspect-ratio:9/16;object-fit:cover;box-shadow:0 0 40px rgba(0,0,0,.45)}
/* 3: film pionowy w miejscu filmu YouTube w „Dlaczego kursanci zdają” */
.adjn-slot{display:grid;place-items:center;padding:24px 0}
.adjn-slot .adjn-vid{width:min(300px,100%);box-shadow:0 0 14px 4px rgba(66,66,66,.2);border:0}
'''

def nav(items):
    a = ''.join(f'<a href="#miejsce-{i}"><b>{i}</b><i style="font-style:normal">{t}</i></a>' for i, t in items)
    return ('<nav class="spotnav" aria-label="Miejsca na filmy"><span>Filmy na tej stronie:</span>' + a +
            '<button type="button" onclick="document.body.classList.toggle(\'spots-off\');this.textContent=document.body.classList.contains(\'spots-off\')?\'Pokaż oznaczenia\':\'Ukryj oznaczenia\'">Ukryj oznaczenia</button></nav>')

def edit_razem_nowe(s):
    # 1. góra strony: reklama z drona zamiast zdjęcia, gra sama bez dźwięku
    i = at(s, '<div class="kurs-img-wrapper">')
    m = re.compile(r'<img[^>]*>').search(s, i)
    s = s[:m.end()] + '<div class="adjh-box" data-loop style="--bg:url(media/reklama-10a.jpg)"><video class="adjh-loop" src="media/reklama-10a.mp4" poster="media/reklama-10a.jpg" muted loop autoplay playsinline aria-hidden="true"></video></div>' + s[m.end():]
    s = s.replace('<div class="kurs-img-wrapper">', '<div id="miejsce-1" data-spot="1 · Film na górze strony" class="kurs-img-wrapper" style="position:relative">', 1)
    # 2. obok wymagań: instruktorka, z dźwiękiem po kliknięciu
    w = at(s, 'Wymagania na kurs prawa jazdy kat. B'); a = s.rfind('<div class="wp-block-columns', 0, w)
    f1 = s.find('<figure', a); f2 = s.find('</figure>', f1) + len('</figure>')
    s = s[:f1] + '<div id="miejsce-2" data-spot="2 · Film przy wymaganiach">' + kurs16_media() + '</div>' + s[f2:]
    # 3. „Dlaczego kursanci zdają”: druga wersja reklamy w miejscu obecnego filmu YouTube
    d = at(s, 'Dlaczego kursanci zdają'); y = at(s, 'ZnJegLxixKQ', d)
    a = s.rfind('<figure', 0, y); b = s.find('</figure>', a) + len('</figure>')
    slot = ('<div id="miejsce-3" data-spot="3 · Film w sekcji o zdawalności" class="adjn adjn-slot">'
            '<div class="adjn-vid" data-loop><video src="media/reklama-10b.mp4" poster="media/reklama-10b.jpg" muted loop playsinline preload="metadata" aria-hidden="true"></video></div></div>')
    s = s[:a] + slot + s[b:]
    s = s.replace('</head>', f'<style>{SPOT_CSS}</style></head>', 1)
    s = s.replace('</body>', nav([(1, 'Góra strony'), (2, 'Przy wymaganiach'), (3, 'Sekcja o zdawalności')]) + '</body>', 1)
    return s

if __name__ == '__main__':
    page('_base.html', 'razem-nowe.html', edit_razem_nowe)
    print('ok razem-nowe')
