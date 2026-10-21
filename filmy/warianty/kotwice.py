# Dopisuje przewijanie do miejsca z filmem, gdy w adresie jest #film (strony spoza build.py).
import pathlib
BASE = pathlib.Path(__file__).parent
PAGES = {'glowna.html': '.adjnf', 'glowna-opinie.html': '.adjnf', 'kurs-obok-wymagan.html': '.adjn16', 'nowe-formularz.html': '.adjf', 'nowe-intro.html': '.adji'}
JS = '''<script>(function(){if(location.hash!=='#film')return;addEventListener('load',function(){setTimeout(function(){
var e=document.querySelector('%s');if(!e)return;var c=e.closest('.wp-block-columns')||e;var h=c.offsetHeight;
var y=c.getBoundingClientRect().top+scrollY-Math.max(90,(innerHeight-h)/2);document.documentElement.style.scrollBehavior='auto';scrollTo(0,Math.max(0,y));},400)});})();</script>'''
for f, sel in PAGES.items():
    p = BASE / f; s = p.read_text(encoding='utf-8')
    if 'location.hash!==\'#film\'' in s: continue
    s = s.replace('</body>', JS % sel + '</body>', 1); p.write_text(s, encoding='utf-8'); print('ok', f)
