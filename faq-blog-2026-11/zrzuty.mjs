import { chromium } from '/Users/marcinsiwonia/projekty/agent-lab/node_modules/playwright/index.mjs';
const file = 'file://' + process.cwd() + '/podglad-wpis-310.html';
const tag = process.argv[2] || 'r1';
const b = await chromium.launch();
const clean = p => p.evaluate(() => { for (const e of [...document.querySelectorAll('body *')]) { const s = getComputedStyle(e); if ((s.position === 'fixed' || s.position === 'sticky') && (/cookie/i.test(e.innerText || '') || e.getBoundingClientRect().width >= innerWidth * 0.95 && e.getBoundingClientRect().height >= innerHeight * 0.9)) e.remove(); } document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto'; });
for (const [name, vp] of [['desktop', {width: 1440, height: 900}], ['mobile', {width: 390, height: 844}]]) {
  const p = await b.newPage({viewport: vp, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/130 Safari/537.36'});
  await p.goto(file, {waitUntil: 'load', timeout: 60000}).catch(e => console.log('goto', e.message));
  await p.waitForTimeout(3000);
  await p.evaluate(() => { for (const e of [...document.querySelectorAll('body *')]) { const s = getComputedStyle(e); if ((s.position === 'fixed' || s.position === 'sticky') && (/cookie/i.test(e.innerText || '') || e.getBoundingClientRect().width >= innerWidth * 0.95 && e.getBoundingClientRect().height >= innerHeight * 0.9)) e.remove(); } document.documentElement.style.overflow = 'auto'; document.body.style.overflow = 'auto'; });
  const sec = p.locator('section.adj-faq');
  await sec.scrollIntoViewIfNeeded(); await p.waitForTimeout(2500);
  await clean(p); await sec.screenshot({path: `zrzuty/${tag}-${name}-zamkniete.png`});
  await p.locator('section.adj-faq summary').first().click(); await p.waitForTimeout(500);
  // kontekst: koniec wpisu + blok
  const box = await sec.evaluate(e => { const r = e.getBoundingClientRect(); return {y: r.top + scrollY, height: r.height}; });
  await clean(p); await p.screenshot({path: `zrzuty/${tag}-${name}-kontekst.png`, clip: {x: 0, y: Math.max(0, box.y - 350), width: vp.width, height: Math.min(box.height + 450, 2400)}, fullPage: true});
  await p.keyboard.press('Tab'); // focus test
  await p.locator('section.adj-faq summary').nth(1).focus(); await p.waitForTimeout(300);
  await clean(p); await sec.screenshot({path: `zrzuty/${tag}-${name}-otwarte-focus.png`});
  const st = await p.evaluate(() => { const s = document.querySelector('.adj-faq summary'), a = document.querySelector('.adj-faq .ans'), h = document.querySelector('#adj-faq-h'), bp = document.querySelector('.wp-block-paragraph');
    const g = e => e && getComputedStyle(e); return {summary: [g(s).fontSize, g(s).fontFamily.slice(0,40), s.getBoundingClientRect().height], ans: g(a).fontSize, h2: [g(h).fontSize, g(h).fontWeight, g(h).marginTop], ctH2: (()=>{const x=[...document.querySelectorAll('h2.wp-block-heading')][0]; return [g(x).fontSize,g(x).textAlign,g(x).marginTop,g(x).marginBottom]})(), postP: bp && [g(bp).fontSize, g(bp).color, g(bp).lineHeight], width: document.querySelector('.adj-faq').getBoundingClientRect().width}; });
  console.log(name, JSON.stringify(st));
  await p.close();
}
await b.close();
