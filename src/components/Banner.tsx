import { useState } from 'react';
import { Menu, X } from 'lucide-react';
import { resetDemo } from '../state/store';
import { useTour } from '../tour/Tour';
import { PersonaSwitcher } from './PersonaSwitcher';

const item = 'flex min-h-11 w-full items-center px-4 text-left text-sm hover:bg-ivory';

export function Banner() {
  const [open, setOpen] = useState(false);
  const tour = useTour();
  const pick = (fn: () => void) => () => { setOpen(false); fn(); };
  return (
    <div className="sticky top-0 z-20">
      <div className="relative flex items-center justify-between border-b border-gold bg-ink pl-4 text-paper">
        <span className="t-label py-2">Prototype, simulated data</span>
        <button type="button" aria-label={open ? 'Close menu' : 'Open menu'} aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
          className="flex h-11 w-11 items-center justify-center focus-visible:outline-paper">
          {open ? <X size={18} aria-hidden /> : <Menu size={18} aria-hidden />}
        </button>
        {open && (
          <div className="absolute right-2 top-11 w-60 border border-hairline bg-paper py-1 text-ink">
            <button type="button" onClick={pick(() => tour.start(false))} className={item}>Guided tour</button>
            <button type="button" onClick={pick(() => tour.start(true))} className={item}>Play 3-minute demo</button>
            <button type="button" onClick={pick(resetDemo)} className={item}>Reset demo</button>
            <p className="t-source border-t border-hairline px-4 pb-1 pt-2 text-muted">
              Version {__BUILD_SHA__} · {__BUILD_TIME__}
            </p>
          </div>
        )}
      </div>
      <PersonaSwitcher />
    </div>
  );
}
