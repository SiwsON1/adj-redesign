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

/* strona główna: karta z reklamą */
.adjnr{padding:0 16px 64px}
.adjnr__card{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:minmax(0,560px) 300px;justify-content:space-evenly;gap:56px;align-items:center;padding:40px 48px;background:#fff;border:1px solid #e5e5e5;border-radius:14px}
.adjnr h2{margin:0 0 14px!important;font:800 36px/1.15 "Work Sans",sans-serif!important;color:#1a1a1a!important;text-align:left!important;max-width:18ch}
.adjnr h2 span{color:#FEA900}
.adjnr__lead{margin:0 0 28px!important;padding:0!important;font:400 16px/1.6 "Work Sans",sans-serif;color:#555;text-align:left!important;max-width:48ch}
.adjnr .adjnr__list{display:grid;gap:16px;margin:0 0 32px!important}
.adjnr__list li{display:flex!important;align-items:center;gap:16px;font:700 16px/1.35 "Work Sans",sans-serif}
.adjnr__list small{display:block;font:400 14px/1.4 "Work Sans",sans-serif;color:#666;margin-top:2px}
.adjnr .adjn-vid video{pointer-events:none}
@media (max-width:860px){.adjnr__card{grid-template-columns:1fr;gap:28px;padding:28px 20px}.adjnr h2{font-size:28px!important}.adjnr__media{width:min(280px,100%);margin:0 auto;order:-1}}

/* strona główna: filmy instruktorów */
.adjnf{padding:56px 16px 64px}
.adjnf__in{max-width:1200px;margin:0 auto}
.adjnf h2{margin:0!important;font:700 20px/1.3 "Work Sans",sans-serif!important;color:#000!important;text-align:center!important}
.adjnf__line{display:block;width:40px;height:2px;margin:14px auto 12px;background:#FEA900}
.adjnf__sub{margin:0 auto 32px!important;padding:0!important;max-width:52ch;text-align:center!important;font:400 15px/1.55 "Work Sans",sans-serif;color:#555}
.adjnf__row{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:20px}
.adjnf .adjnf__row>li{display:flex!important}
.adjnf__b{flex:1}
.adjnf__c{display:flex!important;flex-direction:column;width:100%!important;text-align:left;background:#fff;border:1px solid #e5e5e5;border-radius:14px;overflow:hidden;transition:transform .25s cubic-bezier(.23,1,.32,1),box-shadow .25s}
.adjnf__m{position:relative;display:block;aspect-ratio:9/16;background:#1a1a1a}
.adjnf__m img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover}
.adjnf__m .adjn-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:52px;height:52px}
.adjnf__m .adjn-play svg{width:20px;height:20px}
.adjnf__new{position:absolute;left:10px;top:10px;padding:5px 9px;border-radius:6px;background:#FEA900;color:#fff;font:700 12px/1 "Work Sans",sans-serif}
.adjnf__b{display:block;padding:14px 14px 16px}
.adjnf__b strong{display:block;font:700 15px/1.3 "Work Sans",sans-serif;color:#000}
.adjnf__b small{display:block;margin-top:6px;font:500 13px/1.3 "Work Sans",sans-serif;color:#666}
@media (hover:hover) and (pointer:fine){.adjnf__c:hover{transform:translateY(-4px);box-shadow:0 18px 36px -24px rgba(0,0,0,.35)}.adjnf__c:hover .adjn-play{transform:translate(-50%,-50%) scale(1.07)}}
.adjnf__c:active{transform:scale(.98)}
@media (max-width:1000px){.adjnf__row{display:flex;overflow-x:auto;gap:14px;margin:0 -16px;padding:4px 16px 12px;scroll-snap-type:x mandatory;scroll-padding-inline:16px}.adjnf__row>li{flex:0 0 44%;scroll-snap-align:start}}
@media (max-width:560px){.adjnf__row>li{flex:0 0 58%}}

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
  document.querySelectorAll('.adjn-vid[data-loop] video').forEach(function(v){ if(still) return;
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
  document.addEventListener('click',function(e){ var t=e.target.closest('.adjnf__c'); if(!t) return; e.preventDefault(); open(t); });
})();
'''.replace('%X%', repr(X))

def vid_click(src, poster, label, title):
    return (f'<div class="adjn-vid" data-click><video src="{src}" poster="{poster}" preload="none" playsinline></video>'
            f'<button class="adjn-vid__go" type="button" aria-label="{label}">{PLAYB}<span class="adjn-vid__t">{title}</span></button></div>')

def kurs16_media():
    return (f'<div class="adjn adjn16">{vid_click("media/16-lat.mp4", "media/16-lat.jpg", "Odtwórz film: kurs od 16 lat i 9 miesięcy, 0:16", "Kurs od 16 lat i 9 miesięcy")}'
            f'<p class="adjn16__cap">Film 0:16 · Instruktorka ADJ wyjaśnia, jak zacząć kurs przed 17. urodzinami</p></div>')

def reklama():
    pts = [('trophy', '6 lat z rzędu lider zdawalności', 'Ranking zdawalności WORD Wrocław, kategoria B'),
           ('road', 'Ćwiczysz na trasach egzaminacyjnych', 'Skrzyżowania z egzaminu, także w goglach VR'),
           ('pin', '3 lokalizacje i plac egzaminacyjny', 'Wiaduktowa 21, Bierutowska 1A, Wrocławczyka 42/1a')]
    li = ''.join(f'<li>{icon(i)}<span>{a}<small>{b}</small></span></li>' for i, a, b in pts)
    return (f'<section class="adjn adjnr" aria-labelledby="adjnr-h"><div class="adjnr__card"><div>'
            f'<h2 id="adjnr-h">Kurs na prawo jazdy <span>we Wrocławiu</span></h2>'
            f'<p class="adjnr__lead">Uczysz się jeździć pewnie na tych samych skrzyżowaniach, przez które prowadzi trasa egzaminu.</p>'
            f'<ul class="adjnr__list" role="list">{li}</ul><a class="adjn-btn" href="{FORM}">Zapisz się na kurs</a></div>'
            f'<div class="adjnr__media"><div class="adjn-vid" data-loop><video src="media/reklama-10a.mp4" poster="media/reklama-10a.jpg" muted loop playsinline preload="metadata" aria-label="Film: kurs na prawo jazdy we Wrocławiu"></video></div></div>'
            f'</div></section>')

TT = 'https://www.tiktok.com/player/v1/{}?autoplay=1&loop=1&music_info=0&description=0&rel=0&native_context_menu=0'
FILMS = [
    ('mp4', 'media/16-lat.mp4', 'media/16-lat.jpg', 'Kurs od 16 lat i 9 miesięcy', '0:16 · Instruktorka ADJ', True),
    ('tt', TT.format('7543984782145867030'), 'img/tt/7543984782145867030.jpg', 'Witamy w Akademii', 'TikTok ADJ', False),
    ('yt', 'https://www.youtube-nocookie.com/embed/MVWxbNE8Wwk?autoplay=1&rel=0&playsinline=1&cc_load_policy=1&cc_lang_pref=pl', 'https://i.ytimg.com/vi/MVWxbNE8Wwk/hq1.jpg', 'Jak wygląda egzamin praktyczny', '0:51 · Instruktor ADJ', False),
    ('tt', TT.format('7556221278558883094'), 'img/tt/7556221278558883094.jpg', 'Jak nie robić łuku', 'TikTok ADJ', False),
    ('tt', TT.format('7543984156921908502'), 'img/tt/7543984156921908502.jpg', 'Jakich butów nie nosić na motocykl', 'TikTok ADJ', False),
    ('tt', TT.format('7543981236197297430'), 'img/tt/7543981236197297430.jpg', 'Instruktor kontra złamany paznokieć', 'TikTok ADJ', False),
]

def filmy():
    li = ''.join(
        f'<li><button class="adjnf__c" type="button" data-kind="{k}" data-src="{s}" data-title="{t}" aria-label="Odtwórz film: {t}">'
        f'<span class="adjnf__m"><img src="{p}" alt="" loading="lazy">{"<span class=adjnf__new>Nowy</span>" if n else ""}{PLAYB}</span>'
        f'<span class="adjnf__b"><strong>{t}</strong><small>{m}</small></span></button></li>'
        for k, s, p, t, m, n in FILMS)
    return (f'<section class="adjn adjnf" aria-labelledby="adjnf-h"><div class="adjnf__in"><h2 id="adjnf-h">Filmy instruktorów</h2><span class="adjnf__line"></span>'
            f'<p class="adjnf__sub">Krótko i konkretnie: jak zacząć kurs, jak wygląda egzamin i czego unikać na placu.</p>'
            f'<ul class="adjnf__row" role="list">{li}</ul></div></section>')

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
    page('_base.html', 'kurs-16-lat.html', edit_kurs)
    page('_home_base.html', 'glowna-reklama.html', edit_reklama)
    page('_home_base.html', 'glowna.html', edit_filmy)
    print('ok')
