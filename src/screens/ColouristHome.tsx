import { useState } from 'react';
import { AlertTriangle, Check } from 'lucide-react';
import { Avatar, Chip, Headline, Label, Note, Screen, btnPrimary, btnSecondary } from '../components/ui';
import { plansFor, priceVariants, todaysVisits, visitSteps } from '../data/mock';
import { useStore } from '../state/store';

export default function ColouristHome() {
  const { state, dispatch } = useStore();
  const [open, setOpen] = useState<string | null>(null);
  const variant = priceVariants.find((v) => v.id === state.variantId) ?? priceVariants[0];
  const mayaPlan = plansFor(variant).find((p) => p.id === state.plan)!;
  const mayaAlert = state.alerts.find((a) => a.customer === 'Maya');

  return (
    <Screen>
      <div className="flex items-center gap-3">
        <Avatar initial="D" />
        <div>
          <Label>Dana · Salon Aurora</Label>
          <p className="t-card-body text-muted">Certified colourist · Home-service permit verified</p>
        </div>
      </div>
      <Headline>Today's home visits</Headline>
      <p className="t-card-body -mt-2 text-muted">Wed 14 Apr 2027 · first names only, as shared by the salon</p>

      <ul className="flex flex-col gap-3">
        {todaysVisits.map((v) => {
          const isMaya = v.id === 'v-maya';
          const service = isMaya ? `${mayaPlan.name}: ${mayaPlan.includes[0].toLowerCase()} + treatment` : v.service;
          const done = state.stepsDone[v.id] ?? 0;
          const patchOk = isMaya ? !!state.checklist.patch : true;
          return (
            <li key={v.id} className="border border-hairline bg-paper">
              <div className="flex items-start gap-3 p-4">
                <span className="t-kpi w-16 shrink-0 text-[22px] leading-7">{v.time}</span>
                <div className="min-w-0 flex-1">
                  <p className="t-card-title">{v.customer} <span className="font-normal text-muted">· {v.area}</span></p>
                  <p className="t-card-body">{service}</p>
                  <p className="t-card-body mt-1 text-muted">Last scan: Hair Health Index {v.scan} (illustrative)</p>
                  {!patchOk && <p className="t-card-body mt-1 text-negative">Patch test not confirmed yet: no colour until it is.</p>}
                  {isMaya && mayaAlert && (
                    <p className="t-card-body mt-1 flex items-center gap-1 text-negative"><AlertTriangle size={12} aria-hidden /> Result did not improve: adjust treatment</p>
                  )}
                  {done === visitSteps.length && <p className="t-card-body mt-1 text-positive"><Check size={12} className="inline" aria-hidden /> Visit complete</p>}
                </div>
              </div>
              <label className="block border-t border-hairline px-4 py-2">
                <span className="t-source text-muted">Notes (saved on this device only)</span>
                <textarea rows={2} value={state.notes[v.id] ?? v.note}
                  onChange={(e) => dispatch({ type: 'setNote', id: v.id, text: e.target.value })}
                  className="t-card-body mt-1 block w-full resize-none border border-hairline bg-ivory p-2 focus:outline-none focus-visible:border-ink" />
              </label>
              <div className="border-t border-hairline p-3">
                {open === v.id ? (
                  <div>
                    <p className="t-label text-muted">Visit checklist</p>
                    <ol className="mt-2 flex flex-col gap-1">
                      {visitSteps.map((s, i) => {
                        const isDone = i < done;
                        const isNext = i === done;
                        return (
                          <li key={s}>
                            <button type="button" disabled={!isNext}
                              onClick={() => dispatch({ type: 'stepDone', id: v.id, step: i + 1 })}
                              className={`flex min-h-11 w-full items-center gap-3 border px-3 text-left text-sm ${isNext ? 'border-ink' : 'border-hairline'} ${isDone ? 'text-muted' : ''}`}>
                              <span className={`flex h-5 w-5 shrink-0 items-center justify-center border ${isDone ? 'border-ink bg-ink text-paper' : 'border-muted'}`}>
                                {isDone && <Check size={14} aria-hidden />}
                              </span>
                              {i + 1}. {s}{isNext && <span className="t-source ml-auto text-muted">Tap when done</span>}
                            </button>
                          </li>
                        );
                      })}
                    </ol>
                    <button type="button" onClick={() => setOpen(null)} className={`${btnSecondary} mt-2`}>Close checklist</button>
                  </div>
                ) : (
                  <button type="button" onClick={() => setOpen(v.id)} className={btnPrimary}>
                    {done === 0 ? 'Start visit' : done === visitSteps.length ? 'View checklist' : 'Continue visit'}
                  </button>
                )}
              </div>
            </li>
          );
        })}
      </ul>
      <div className="flex flex-wrap gap-2"><Chip kind="fiction">Fictional customers</Chip><Chip>Simulated data</Chip></div>
      <Note>Notes stay in this browser. Nothing is sent anywhere.</Note>
    </Screen>
  );
}
