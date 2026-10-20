# Wariant na stronie głównej: pionowe filmy (Shorts) jak na TikToku, instruktor mówi do kamery.
# Wejście: _home_base.html (świeży HTML strony głównej, poza repo). Wyjście: glowna.html.
import re, pathlib
from build import BASE, FORM, PLAY, ARROW, COMMON_CSS, COMMON_JS, prep, at, ins

SHORTS = [  # źródło, id, tytuł, czas/opis, miniatura, etykieta
    ('tt', '7543984782145867030', 'Witamy w Akademii', 'TikTok ADJ', 'img/tt/7543984782145867030.jpg', 'Instruktorka ADJ'),
    ('yt', 'MVWxbNE8Wwk', 'Jak wygląda egzamin praktyczny', '0:51', 'https://i.ytimg.com/vi/MVWxbNE8Wwk/hq1.jpg', 'Instruktor ADJ'),
    ('tt', '7556221278558883094', 'Jak nie robić łuku', 'TikTok ADJ', 'img/tt/7556221278558883094.jpg', 'Plac manewrowy'),
    ('tt', '7543981236197297430', 'Instruktor kontra złamany paznokieć', 'TikTok ADJ', 'img/tt/7543981236197297430.jpg', 'Z przymrużeniem oka'),
    ('tt', '7543984156921908502', 'Jakich butów nie nosić na motocykl', 'TikTok ADJ', 'img/tt/7543984156921908502.jpg', 'Kat. A'),
]

CSS = r'''
.adjvt{padding:56px 16px;background:#1f1f1f;color:#fff}
.adjvt__in{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(28px,5vw,72px);align-items:center}
.adjvt h2{color:#fff!important;text-align:left!important;margin:0 0 14px!important;font-size:clamp(28px,3vw,40px)!important;line-height:1.1!important}
.adjvt__lead p{text-align:left!important;padding:0!important;margin:0 0 24px;color:rgba(255,255,255,.8);font:400 17px/1.6 "Roboto",sans-serif;max-width:42ch}
.adjvt__row{display:flex;gap:14px;overflow-x:auto;padding:4px 2px 10px!important;scroll-snap-type:x mandatory;scrollbar-width:thin}
.adjvt__row>li{flex:0 0 calc((100% - 28px)/3);scroll-snap-align:start}
.adjvt__v{position:relative;display:block!important;width:100%!important;aspect-ratio:9/16;border-radius:18px!important;overflow:hidden;background:#000;box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 30px 60px -30px rgba(0,0,0,.9);text-align:left;transition:transform .25s var(--adj-out)}
.adjvt__v img{position:absolute;inset:0;width:100%!important;height:100%!important;object-fit:cover}
.adjvt__v[data-src=yt] img{transform:scale(1.34)}
.adjvt__v::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,20,20,.35) 0%,rgba(20,20,20,0) 22%,rgba(20,20,20,0) 50%,rgba(20,20,20,.92) 100%)}
.adjvt__tag{position:absolute;left:12px;top:12px;z-index:2;padding:6px 10px;border-radius:999px;background:var(--adj-brand);color:#141414;font:700 12px/1 "Work Sans",sans-serif}
.adjvt__cap{position:absolute;left:14px;right:14px;bottom:14px;z-index:2;color:#fff}
.adjvt__cap strong{display:block;font:700 16px/1.3 "Work Sans",sans-serif;margin-bottom:6px}
.adjvt__cap small{font:600 13px/1 "Work Sans",sans-serif;color:rgba(255,255,255,.78);font-variant-numeric:tabular-nums}
.adjvt__v .adjv-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:2;width:60px;height:60px}
@media (hover:hover) and (pointer:fine){.adjvt__v:hover{transform:translateY(-4px)}.adjvt__v:hover .adjv-play{transform:translate(-50%,-50%) scale(1.08)}}
.adjvt__v:active .adjv-play{transform:translate(-50%,-50%) scale(.94)}
.adjvt__v.is-playing::after,.adjvt__v.is-playing>*:not(iframe){display:none}
@media (max-width:900px){.adjvt__in{grid-template-columns:1fr}.adjvt__row{display:flex;overflow-x:auto;gap:12px;margin:0 -16px;padding:0 16px 8px!important;scroll-snap-type:x mandatory;scroll-padding-inline:16px;scrollbar-width:none}
.adjvt__row>li{flex:0 0 62%}}
'''

JS = r'''
(function(){var s=document.querySelector('.adjvt'); if(!s) return;
 s.addEventListener('click',function(e){var t=e.target.closest('.adjvt__v'); if(!t||t.classList.contains('is-playing')) return; e.preventDefault(); e.stopPropagation();
  s.querySelectorAll('.adjvt__v.is-playing').forEach(function(x){var f=x.querySelector('iframe'); if(f) f.remove(); x.classList.remove('is-playing')});
  var f=document.createElement('iframe'); f.src=t.dataset.src==='tt'?'https://www.tiktok.com/player/v1/'+t.dataset.id+'?autoplay=1&loop=1&music_info=0&description=0&rel=0&native_context_menu=0':'https://www.youtube-nocookie.com/embed/'+t.dataset.id+'?autoplay=1&rel=0&playsinline=1&cc_load_policy=1&cc_lang_pref=pl&hl=pl&loop=1&playlist='+t.dataset.id;
  f.title=t.dataset.title; f.allow='autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen=true;
  f.style.cssText='position:absolute;inset:0;width:100%;height:100%;border:0;z-index:3';
  t.classList.add('is-playing'); t.appendChild(f);},true);})();
'''

def section():
    li = ''.join(
        f'<li><button class="adjvt__v" type="button" data-src="{src}" data-id="{i}" data-title="{t}" aria-label="Odtwórz film: {t}">'
        f'<img src="{f}" alt="" loading="lazy"><span class="adjvt__tag">{tag}</span>'
        f'<span class="adjv-play">{PLAY}</span><span class="adjvt__cap"><strong>{t}</strong><small>{d}</small></span></button></li>'
        for src, i, t, d, f, tag in SHORTS)
    return (f'<section class="adjv adjvt" aria-labelledby="adjvt-h"><div class="adjvt__in"><div class="adjvt__lead">'
            f'<h2 id="adjvt-h">Posłuchaj instruktorów ADJ</h2>'
            f'<p>Krótkie filmy z placu i z ośrodka, takie jak na TikToku ADJ: jak wygląda egzamin, czego unikać na placu i jak wygląda Akademia od środka.</p>'
            f'<a class="adjv-btn adjv-btn--primary" href="{FORM}">Zapisz się na kurs {ARROW}</a></div>'
            f'<ul class="adjvt__row" role="list">{li}</ul></div></section>')

if __name__ == '__main__':
    s = prep((BASE / '_home_base.html').read_text(encoding='utf-8'))
    s = ins(s, s.rfind('<section', 0, at(s, 'Skuteczność, doświadczenie')), section())
    head = f'<meta name="robots" content="noindex, nofollow">\n<style>{COMMON_CSS}{CSS}</style>\n'
    s = re.sub(r'(<head[^>]*>)', lambda m: m.group(1) + '\n' + head, s, count=1)
    s = s.replace('</body>', f'<script>{COMMON_JS}{JS}</script>\n</body>', 1)
    (BASE / 'glowna.html').write_text(s, encoding='utf-8')
    print('ok')
