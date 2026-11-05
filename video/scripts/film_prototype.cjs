// Films the PRO•GO prototype at a phone viewport for the M4 video.
// Usage: node film_prototype.js <baseUrl> <outDir> [--stills]
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const [base, out, mode] = process.argv.slice(2);
const KEY = 'progo-demo-v1';
const seed = { variantId: 'v1', plan: 'essential', scanDone: true, reserved: true, slotId: 's2',
  checklist: { patch: true }, scenario: 'improved', nextBooked: false, renewed: false, alerts: [] };
const shots = [
  { name: 'p1_scan_result_58', route: '#/customer/result', state: seed },
  { name: 'p2_professional_partner_salon', route: '#/customer/slot', state: { ...seed, slotId: null } },
  { name: 'p3_booking_confirmation', route: '#/customer/slot', state: seed },
  { name: 'p4_rescan', route: '#/customer/after', state: seed },
];
const only = (process.env.ONLY || '').split(',').filter(Boolean);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  for (const s of shots.filter((x) => !only.length || only.includes(x.name))) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
    await ctx.addInitScript(([k, v]) => localStorage.setItem(k, v), [KEY, JSON.stringify(s.state)]);
    const page = await ctx.newPage();
    await page.goto(base + s.route); await page.waitForLoadState('networkidle');
    await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(400);
    if (mode === '--stills') {
      await page.screenshot({ path: path.join(out, s.name + '.jpg'), type: 'jpeg', quality: 92, fullPage: true });
    } else {
      // 6 s at 30 fps: hold 1.5 s, slow scroll to bottom, hold.
      const dir = path.join(out, s.name); fs.mkdirSync(dir, { recursive: true });
      const max = await page.evaluate(() => Math.max(0, document.documentElement.scrollHeight - innerHeight));
      const N = 180;
      for (let i = 0; i < N; i++) {
        const t = Math.min(1, Math.max(0, (i - 45) / 90)); const e = t < .5 ? 2*t*t : 1 - Math.pow(-2*t+2, 2)/2;
        await page.evaluate((y) => window.scrollTo(0, y), Math.round(e * max));
        await page.screenshot({ path: path.join(dir, String(i).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 92 });
      }
    }
    await ctx.close();
  }
  await browser.close();
})();
