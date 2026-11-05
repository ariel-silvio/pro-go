// Print an HTML file to A4 PDF with Chromium. Usage: node print_pdf.cjs <in.html> <out.pdf>
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [inp, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(inp), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const foot = `<div style="width:100%;font-family:sans-serif;font-size:7px;color:#5F5A54;letter-spacing:.18em;
    padding:0 17mm;display:flex;justify-content:space-between;text-transform:uppercase">
    <span>PRO•GO · 12 weeks with Layla · Team D</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`;
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>', footerTemplate: foot });
  await b.close();
  console.log('wrote', out);
})();
