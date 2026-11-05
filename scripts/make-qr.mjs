// Writes public/qr.png and docs/qr.png for the live URL. Run: npm run qr
import QRCode from 'qrcode';
const url = 'https://ariel-silvio.github.io/pro-go/';
const opts = { width: 600, margin: 4, errorCorrectionLevel: 'M', color: { dark: '#111111', light: '#ffffff' } };
for (const out of ['public/qr.png', 'docs/qr.png']) {
  await QRCode.toFile(out, url, opts);
  console.log('wrote', out, '->', url);
}
