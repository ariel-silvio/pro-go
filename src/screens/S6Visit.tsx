import { Check } from 'lucide-react';
import { ColouristCard, Headline, Label, LinkButton, Note, Screen, Steps } from '../components/ui';
import { checklistItems, patchTestDay, slots, visitTimeline } from '../data/mock';
import { useStore } from '../state/store';

const segFill = ['bg-gold', 'bg-ink', 'bg-neutral-series', 'bg-gold'];

export default function S6Visit() {
  const { state, dispatch } = useStore();
  const slot = slots.find((s) => s.id === state.slotId) ?? slots[1];
  const total = visitTimeline.reduce((a, b) => a + b.minutes, 0);
  const [h, m] = slot.time.split(':').map(Number);
  const end = `${String(h + Math.floor((m + total) / 60)).padStart(2, '0')}:${String((m + total) % 60).padStart(2, '0')}`;

  return (
    <Screen>
      <Steps current={6} />
      <div>
        <Label>Visit day · {slot.label}</Label>
        <Headline>Before Dana arrives</Headline>
      </div>
      <ul className="flex flex-col gap-2">
        {checklistItems.map((c) => {
          const on = !!state.checklist[c.id];
          return (
            <li key={c.id} data-tour={c.id === 'patch' ? 'patch' : undefined}>
              <button type="button" role="checkbox" aria-checked={on} onClick={() => dispatch({ type: 'toggleCheck', id: c.id })}
                className={`flex min-h-14 w-full items-start gap-3 border p-3 text-left ${c.id === 'patch' ? 'border-ink' : 'border-hairline'}`}>
                <span className={`mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center border ${on ? 'border-ink bg-ink text-paper' : 'border-muted'}`}>
                  {on && <Check size={14} aria-hidden />}
                </span>
                <span>
                  <span className="t-card-title block">{c.label}</span>
                  <span className="t-card-body block text-muted">
                    {c.id === 'patch' ? `By ${patchTestDay(slot)}, 48 h before, with the kit from your salon.` : c.hint}
                  </span>
                </span>
              </button>
            </li>
          );
        })}
      </ul>
      {!state.checklist.patch && (
        <p className="t-card-body text-negative">No patch test, no colour: Dana will only do the treatment and scan.</p>
      )}

      <div>
        <p className="t-label text-muted">The visit, {slot.time} to {end}</p>
        <div className="mt-2 flex h-8 w-full" role="img"
          aria-label={visitTimeline.map((v) => `${v.label} ${v.minutes} minutes`).join(', ')}>
          {visitTimeline.map((v, i) => (
            <div key={v.label} style={{ width: `${(v.minutes / total) * 100}%` }}
              className={`${segFill[i]} ${i ? 'border-l border-paper' : ''}`} />
          ))}
        </div>
        <ul className="mt-2 grid grid-cols-2 gap-x-3 gap-y-1">
          {visitTimeline.map((v, i) => (
            <li key={v.label} className="t-card-body flex items-start gap-2">
              <span className={`mt-1 h-2.5 w-2.5 shrink-0 ${segFill[i]}`} aria-hidden />
              <span><span className="t-card-title">{v.minutes} min</span> {v.label}</span>
            </li>
          ))}
        </ul>
      </div>
      <ColouristCard />
      <Note>Illustrative timings, Team D assumption.</Note>
      <div className="mt-auto"><LinkButton to="/customer/after">After the visit: see my result</LinkButton></div>
    </Screen>
  );
}
