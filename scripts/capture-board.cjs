// Board and video assets (handoff §15, Phase 4).
// 1. docs/screens/*.png  — S1, S3, S4, S7 at 1170 x 2532 (390 x 844 at 3x), clean demo state, price variant v1.
// 2. docs/miro-product-image.png — 2400 x 1600 (3:2) composite: S3 and S7 in phone frames on ivory, no logos.
// Needs a running preview:  npm run build && npx vite preview --port 4174
// Then:                     node scripts/capture-board.cjs
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.PROGO_URL || 'http://localhost:4174/pro-go/';
const root = path.resolve(__dirname, '..');
const out = (p) => path.join(root, p);
const demoState = { variantId: 'v1', plan: 'essential', scanDone: true, slotId: 's2', checklist: { patch: true }, scenario: 'improved' };
const shots = [
  ['s1-invite', '#/customer/invite'],
  ['s3-scan-result', '#/customer/result'],
  ['s4-plan', '#/customer/plan'],
  ['s7-before-after', '#/customer/after'],
];

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
  const page = await ctx.newPage();
  await page.goto(BASE + '#/customer/invite');
  await page.evaluate((s) => localStorage.setItem('progo-demo-v1', JSON.stringify(s)), demoState);
  for (const [name, hash] of shots) {
    await page.goto(BASE + hash);
    await page.reload();
    // Board images: hide the dashed demo-only controls (scan-outcome switch). The live prototype keeps them.
    await page.addStyleTag({ content: '.border-dashed { display: none !important; }' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(400);
    await page.screenshot({ path: out(`docs/screens/${name}.png`) });
    console.log('wrote docs/screens/' + name + '.png');
  }
  await ctx.close();

  // Composite
  // Fonts are embedded: a page built with setContent cannot load file:// URLs.
  const font = (f) => 'data:font/woff2;base64,' + fs.readFileSync(path.join(root, 'node_modules/@fontsource', f)).toString('base64');
  const img = (n) => 'data:image/png;base64,' + fs.readFileSync(out(`docs/screens/${n}.png`)).toString('base64');
  const qr = 'data:image/png;base64,' + fs.readFileSync(out('docs/qr.png')).toString('base64');
  const html = `<!doctype html><html><head><meta charset="utf-8"><style>
    @font-face { font-family: 'Bodoni Moda'; font-weight: 500; src: url('${font('bodoni-moda/files/bodoni-moda-latin-500-normal.woff2')}') format('woff2'); }
    @font-face { font-family: 'Jost'; font-weight: 400; src: url('${font('jost/files/jost-latin-400-normal.woff2')}') format('woff2'); }
    @font-face { font-family: 'Jost'; font-weight: 500; src: url('${font('jost/files/jost-latin-500-normal.woff2')}') format('woff2'); }
    * { box-sizing: border-box; margin: 0; }
    body { width: 2400px; height: 1600px; background: #f7f3ec; color: #111; font-family: Jost, sans-serif; display: flex; padding: 120px 140px; gap: 110px; }
    .text { width: 760px; display: flex; flex-direction: column; }
    .label { font-size: 26px; font-weight: 500; letter-spacing: .15em; text-transform: uppercase; color: #8a6a3b; }
    h1 { font-family: 'Bodoni Moda', serif; font-weight: 500; font-size: 112px; line-height: 1.05; margin-top: 28px; }
    .rule { width: 120px; height: 4px; background: #b08d57; margin: 44px 0; }
    .lede { font-size: 38px; line-height: 1.45; }
    ul { list-style: none; padding: 0; margin-top: 40px; font-size: 32px; line-height: 1.45; }
    li { padding-left: 40px; position: relative; margin-bottom: 18px; }
    li::before { content: ''; position: absolute; left: 0; top: 20px; width: 18px; height: 3px; background: #b08d57; }
    .foot { margin-top: auto; display: flex; gap: 28px; align-items: flex-end; }
    .foot img { width: 150px; height: 150px; border: 2px solid #e3ddd3; background: #fff; }
    .foot p { font-size: 22px; line-height: 1.5; color: #5f5a54; }
    .foot b { color: #111; font-weight: 500; }
    .phones { display: flex; gap: 90px; align-items: flex-start; }
    figure { display: flex; flex-direction: column; align-items: center; }
    .phone { width: 600px; height: 1299px; border: 18px solid #111; border-radius: 76px; overflow: hidden; background: #fff; }
    .phone img { width: 100%; height: 100%; display: block; }
    figcaption { margin-top: 0; }
  </style></head><body>
    <div class="text">
      <p class="label">Team D · Product prototype</p>
      <h1>PRO•GO Colour Plan</h1>
      <span class="rule"></span>
      <p class="lede">Your salon's colourist comes to your home, on your colour cycle. A hair scan before and after shows what changed.</p>
      <ul>
        <li>90-day plan: two home visits, scan, colour, treatment</li>
        <li>Booked through the partner salon</li>
        <li>Next visit booked before the colourist leaves</li>
      </ul>
      <div class="foot">
        <img src="${qr}" alt="">
        <p><b>Try it: ariel-silvio.github.io/pro-go</b><br>Prototype, simulated data. Fictional characters.<br>Student project for IE Business School.<br>Not affiliated with or endorsed by L'Oréal.</p>
      </div>
    </div>
    <div class="phones">
      <figure><div class="phone"><img src="${img('s3-scan-result')}" alt=""></div></figure>
      <figure><div class="phone"><img src="${img('s7-before-after')}" alt=""></div></figure>
    </div>
  </body></html>`;
  const p2 = await browser.newPage({ viewport: { width: 2400, height: 1600 } });
  await p2.setContent(html, { waitUntil: 'load' });
  await p2.evaluate(() => document.fonts.ready);
  const loaded = await p2.evaluate(() => ['500 20px "Bodoni Moda"', '400 20px Jost', '500 20px Jost'].map((f) => document.fonts.check(f)));
  if (loaded.includes(false)) throw new Error('Brand fonts did not load in the composite: ' + loaded);
  await p2.waitForTimeout(300);
  await p2.screenshot({ path: out('docs/miro-product-image.png') });
  console.log('wrote docs/miro-product-image.png');
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
