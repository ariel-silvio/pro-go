// Renders the "PG" monogram icons (ink background, gold letters, no L'Oréal marks) into public/icons.
// Local only (uses the Playwright that ships with the dev machine). Run: node scripts/make-icons.cjs
const { chromium } = require('playwright');
const svg = (size, pad) => `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 100 100">
  <rect width="100" height="100" fill="#111111"/>
  <text x="50" y="${50 + 13 * (1 - pad)}" font-family="Didot, 'Bodoni Moda', Georgia, serif" font-size="${40 * (1 - pad)}" fill="#b08d57" text-anchor="middle" letter-spacing="1">PG</text>
</svg>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [name, size, pad] of [['icon-192.png', 192, 0], ['icon-512.png', 512, 0], ['maskable-512.png', 512, 0.25], ['apple-touch-icon.png', 180, 0]]) {
    await p.setViewportSize({ width: size, height: size });
    await p.setContent(`<html><body style="margin:0">${svg(size, pad)}</body></html>`);
    await p.screenshot({ path: `public/icons/${name}` });
    console.log('wrote public/icons/' + name);
  }
  await b.close();
})();
