import puppeteer from "puppeteer";
import { mkdir, readdir } from "node:fs/promises";
import { join } from "node:path";

const DIR = "./temporary-screenshots";
const URL = "http://localhost:3001";
const WIDTHS = [390, 768, 1440];

await mkdir(DIR, { recursive: true });

const existing = await readdir(DIR);
const nums = existing
  .map((f) => f.match(/screenshot-(\d+)/)?.[1])
  .filter(Boolean)
  .map(Number);
const next = nums.length ? Math.max(...nums) + 1 : 1;

const browser = await puppeteer.launch({ headless: true });

for (const w of WIDTHS) {
  const page = await browser.newPage();
  await page.setViewport({ width: w, height: 900, deviceScaleFactor: 2 });
  await page.goto(URL, { waitUntil: "networkidle2", timeout: 60000 });
  // Force all reveal elements to visible (screenshot mode)
  await page.evaluate(() => {
    document.querySelectorAll('.reveal').forEach(el => {
      el.classList.add('is-visible');
    });
    // Trigger counter animations
    document.querySelectorAll('[data-counter]').forEach(el => {
      el.dataset.counted = 'true';
      el.textContent = (el.dataset.prefix || '') + el.dataset.counter.replace('.', ',') + (el.dataset.suffix || '');
    });
    // Trigger stat bars
    document.querySelectorAll('.stats-bar__fill').forEach(el => {
      el.style.width = el.dataset.width;
    });
  });
  await new Promise((r) => setTimeout(r, 800));
  const file = join(DIR, `screenshot-${next}-${w}w.png`);
  await page.screenshot({ path: file, fullPage: true });
  console.log(`✓ ${file}`);
  await page.close();
}

await browser.close();
console.log(`\nDone – round ${next}`);
