// Print the one-pager to A4 PDF (no header/footer). Usage: node howto/print_onepager.cjs
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(__dirname, 'record_onepager.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => { const pg = document.querySelector('.page'); return pg.scrollHeight - pg.clientHeight; });
  await p.pdf({ path: path.resolve(__dirname, '..', 'How-to-record-your-part.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  console.log('overflow px:', over); await b.close();
})();
