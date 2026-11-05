import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { CONFIG } from '../config';

export function Banner() {
  const [open, setOpen] = useState(false);
  const reset = () => {
    try { localStorage.removeItem(CONFIG.STORAGE_KEY); } catch { /* storage blocked */ }
    window.location.hash = '#/customer/invite';
    window.location.reload();
  };
  return (
    <div className="sticky top-0 z-20 flex items-center justify-between border-b border-gold bg-ink pl-4 text-paper">
      <span className="t-label py-2">Prototype, simulated data</span>
      <button type="button" aria-label={open ? 'Close menu' : 'Open menu'} aria-expanded={open}
        onClick={() => setOpen((o) => !o)}
        className="flex h-11 w-11 items-center justify-center focus-visible:outline-paper">
        {open ? <X size={18} aria-hidden /> : <Menu size={18} aria-hidden />}
      </button>
      {open && (
        <div className="absolute right-2 top-11 w-48 border border-hairline bg-paper text-ink">
          <button type="button" onClick={reset} className="min-h-11 w-full px-4 text-left text-sm hover:bg-ivory">
            Reset demo
          </button>
        </div>
      )}
    </div>
  );
}
