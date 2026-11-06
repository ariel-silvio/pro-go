import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Pause, Play, X } from 'lucide-react';
import { useStore } from '../state/store';
import { tourSteps } from './steps';

interface TourCtx {
  active: boolean; auto: boolean; index: number; paused: boolean; ended: boolean;
  start: (auto?: boolean) => void; stop: () => void;
  prev: () => void; next: () => void; togglePause: () => void;
}
const Ctx = createContext<TourCtx | null>(null);
export const useTour = () => useContext(Ctx)!;

// ?demo=1 starts the auto-play. Works as https://…/pro-go/?demo=1 and as …/#/customer/invite?demo=1
export function demoRequested() {
  const inSearch = new URLSearchParams(window.location.search).get('demo') === '1';
  const hashQuery = window.location.hash.split('?')[1] ?? '';
  return inSearch || new URLSearchParams(hashQuery).get('demo') === '1';
}

export function TourProvider({ children }: { children: ReactNode }) {
  const { dispatch } = useStore();
  const navigate = useNavigate();
  const [active, setActive] = useState(false);
  const [auto, setAuto] = useState(false);
  const [paused, setPaused] = useState(false);
  const [index, setIndex] = useState(0);
  const [ended, setEnded] = useState(false);

  const go = useCallback((i: number) => {
    const step = tourSteps[i];
    step.enter?.(dispatch);
    navigate(step.path);
    setIndex(i);
  }, [dispatch, navigate]);

  const start = useCallback((a = false) => {
    dispatch({ type: 'demoReset' });
    setAuto(a); setPaused(false); setEnded(false); setActive(true);
    go(0);
  }, [dispatch, go]);
  const stop = useCallback(() => { setActive(false); setEnded(false); }, []);

  // Auto-start from the URL once.
  useEffect(() => { if (demoRequested()) start(true); }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Highlight the step's target and bring it into view.
  useEffect(() => {
    if (!active || ended) return;
    const id = tourSteps[index].target;
    if (!id) return;
    const t = setTimeout(() => {
      const el = document.querySelector<HTMLElement>(`[data-tour="${id}"]`);
      if (!el) return;
      el.setAttribute('data-tour-active', '');
      el.scrollIntoView({ block: 'center', behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
    }, 350);
    return () => {
      clearTimeout(t);
      document.querySelectorAll('[data-tour-active]').forEach((e) => e.removeAttribute('data-tour-active'));
    };
  }, [active, ended, index]);

  // Auto-play timing and in-step actions.
  useEffect(() => {
    if (!active || !auto || paused || ended) return;
    const step = tourSteps[index];
    const cleanup = step.run?.(dispatch);
    const t = setTimeout(() => {
      if (index < tourSteps.length - 1) go(index + 1); else setEnded(true);
    }, step.seconds * 1000);
    return () => { clearTimeout(t); cleanup?.(); };
  }, [active, auto, paused, ended, index, dispatch, go]);

  const prev = useCallback(() => { if (index > 0) go(index - 1); }, [index, go]);
  const next = useCallback(() => { if (index < tourSteps.length - 1) go(index + 1); else setEnded(true); }, [index, go]);
  const togglePause = useCallback(() => setPaused((x) => !x), []);
  const value = useMemo(() => ({ active, auto, index, paused, ended, start, stop, prev, next, togglePause }),
    [active, auto, index, paused, ended, start, stop, prev, next, togglePause]);

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

// The caption bar, placed at the bottom of the phone screen.
export function TourBar() {
  const t = useTour();
  if (!t.active) return null;
  const p = { index: t.index, auto: t.auto, paused: t.paused, ended: t.ended, onPrev: t.prev, onNext: t.next,
    onPause: t.togglePause, onReplay: () => t.start(t.auto), onClose: t.stop };
  const step = tourSteps[p.index];
  const iconBtn = 'flex h-11 w-11 shrink-0 items-center justify-center border border-hairline disabled:opacity-40';
  return (
    <div role="region" aria-label="Guided tour" className="sticky bottom-0 z-30 border-t-2 border-gold bg-ink px-4 pb-3 pt-2 text-paper">
      <div className="flex items-center justify-between">
        <p className="t-label text-gold">{p.ended ? 'End of the tour' : `Guided tour · ${p.index + 1} of ${tourSteps.length}`}</p>
        <button type="button" onClick={p.onClose} aria-label="Close tour" className="flex h-11 w-11 items-center justify-center"><X size={18} aria-hidden /></button>
      </div>
      <p className="text-sm leading-snug" aria-live="polite">
        {p.ended ? 'That was PRO•GO Colour Plan in three minutes. Simulated data, fictional people.' : step.caption}
      </p>
      <div className="mt-2 flex items-center gap-2">
        {p.ended ? (
          <button type="button" onClick={p.onReplay} className="t-label flex min-h-11 flex-1 items-center justify-center gap-2 border border-paper">
            <Play size={14} aria-hidden /> Replay
          </button>
        ) : (
          <>
            <button type="button" onClick={p.onPrev} disabled={p.index === 0} aria-label="Previous step" className={iconBtn}><ChevronLeft size={18} aria-hidden /></button>
            {p.auto && (
              <button type="button" onClick={p.onPause} aria-label={p.paused ? 'Resume' : 'Pause'} className={iconBtn}>
                {p.paused ? <Play size={16} aria-hidden /> : <Pause size={16} aria-hidden />}
              </button>
            )}
            <div className="flex flex-1 gap-0.5" aria-hidden>
              {tourSteps.map((_, i) => <span key={i} className={`h-0.5 flex-1 ${i <= p.index ? 'bg-gold' : 'bg-muted'}`} />)}
            </div>
            <button type="button" onClick={p.onNext} aria-label="Next step" className={iconBtn}><ChevronRight size={18} aria-hidden /></button>
          </>
        )}
      </div>
    </div>
  );
}
