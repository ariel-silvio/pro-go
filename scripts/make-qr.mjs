// Writes public/qr.png and docs/qr.png for the live URL. Run: npm run qr
import QRCode from 'qrcode';
const url = 'https://ariel-silvio.github.io/pro-go/';
const opts = { width: 600, margin: 4, errorCorrectionLevel: 'M', color: { dark: '#111111', light: '#ffffff' } };
for (const out of ['public/qr.png', 'docs/qr.png']) {
  await QRCode.toFile(out, url, opts);
  console.log('wrote', out, '->', url);
}

// The M4 video (Team D, 12 weeks with Layla), shown in the desktop side panel.
await QRCode.toFile('public/qr-video.png', 'https://youtu.be/T2k37jMMXo4', { width: 384, margin: 2, color: { dark: '#111111', light: '#F7F3EC' } });
