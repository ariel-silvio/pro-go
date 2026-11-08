// Phone-screen stills of the PRO•GO prototype for screen replacement in Layla clips (no prototype header or tabs).
// Usage (from video/): node scripts/capture_screens.cjs <baseUrl> <outDir>
const { chromium } = require('playwright');
const [base, out] = process.argv.slice(2);
const seed = { variantId: 'v1', plan: 'essential', scanDone: true, reserved: true, slotId: 's2', checklist: { patch: true }, scenario: 'improved', nextBooked: false, renewed: false, alerts: [] };
const shots = [
  // week 12 re-scan: same screen as week 8, values set to the film's illustrative week-12 score (58 -> 74)
  { name: 'screen_week12_74', route: '#/customer/after', patch: [['AFTER · 9 JUN', 'AFTER · 7 JUL'], ['66', '74'], ['+8', '+16'], ['Wed 9 Jun', 'Wed 4 Aug']] },
];
(async () => {
  const b = await chromium.launch();
  for (const s of shots) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3 });
    await ctx.addInitScript(([k, v]) => localStorage.setItem(k, v), ['progo-demo-v1', JSON.stringify(seed)]);
    const p = await ctx.newPage(); await p.goto(base + s.route); await p.waitForLoadState('networkidle');
    await p.evaluate(() => document.fonts.ready);
    await p.evaluate((patch) => {
      // prototype banner and role tabs: remove the top block that holds the banner text
      const ban = [...document.querySelectorAll('body *')].find((e) => e.children.length === 0 && e.textContent.trim().toUpperCase() === 'PROTOTYPE, SIMULATED DATA');
      let top = ban; while (top && top.parentElement && !top.parentElement.querySelector('main') ) top = top.parentElement;
      (ban?.closest('header, [class*="sticky"], [class*="fixed"]') || ban?.parentElement)?.remove();
      document.querySelectorAll('nav').forEach((n) => n.remove());
      document.querySelectorAll('p').forEach((e) => { if (/demo control/i.test(e.textContent)) e.parentElement.remove(); });   // demo-only switch
      document.body.style.paddingTop = '48px';                            // room for the phone's notch
      const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n; (n = w.nextNode());) for (const [a, z] of patch) {
        const t = n.textContent.replace(/\s+/g, ' ').trim();
        if (t === a || t.toUpperCase() === a) n.textContent = n.textContent.replace(/[\s\S]*/, n.textContent.includes(a) ? n.textContent.replace(a, z) : z);
      }
      for (const [a, z] of patch) if (a.startsWith('+'))                  // deltas are split across nodes ("+", "8")
        document.querySelectorAll('span').forEach((e) => { if (e.textContent.replace(/ up$/, '').trim() === a) {
          const tn = [...e.childNodes].filter((c) => c.nodeType === 3); tn.forEach((c) => (c.textContent = '')); if (tn[0]) tn[0].textContent = z; } });
    }, s.patch || []);
    await p.waitForTimeout(300); await p.screenshot({ path: `${out}/${s.name}.png` }); await ctx.close();
  }
  await b.close();
})();
