import { ArrowDown, ArrowRight, ArrowUp } from 'lucide-react';
import { Bar, Chip, Headline, Label, LinkButton, Note, Screen, Steps, btnPrimary, btnSecondary } from '../components/ui';
import { firstScan, metrics, nextVisit, scenarios, secondScan, type Scenario } from '../data/mock';
import { useStore } from '../state/store';

export function Delta({ d }: { d: number }) {
  if (d > 0) return <span className="inline-flex items-center gap-0.5 text-positive"><ArrowUp size={12} aria-hidden />+{d}<span className="sr-only"> up</span></span>;
  if (d < 0) return <span className="inline-flex items-center gap-0.5 text-negative"><ArrowDown size={12} aria-hidden />{d}<span className="sr-only"> down</span></span>;
  return <span className="inline-flex items-center gap-0.5 text-muted"><ArrowRight size={12} aria-hidden />0<span className="sr-only"> no change</span></span>;
}

export function ScenarioToggle() {
  const { state, dispatch } = useStore();
  return (
    <div className="border border-dashed border-muted p-3">
      <p className="t-label text-muted">Demo control: scan outcome</p>
      <div className="mt-2 grid grid-cols-3 gap-1" role="radiogroup" aria-label="Scan outcome">
        {(Object.keys(scenarios) as Scenario[]).map((s) => (
          <button key={s} type="button" role="radio" aria-checked={state.scenario === s}
            onClick={() => dispatch({ type: 'setScenario', scenario: s })}
            className={`t-label min-h-11 border ${state.scenario === s ? 'border-ink bg-ink text-paper' : 'border-hairline'}`}>
            {scenarios[s].label}
          </button>
        ))}
      </div>
    </div>
  );
}

export function NextVisitActions() {
  const { state, dispatch } = useStore();
  return (
    <div className="flex flex-col gap-2">
      {state.nextBooked
        ? <Note>Next visit booked: {nextVisit.label}, {nextVisit.time}, with Dana. (Simulated, no real booking.)</Note>
        : <button type="button" className={btnPrimary} onClick={() => dispatch({ type: 'bookNext' })}>Book my next visit · {nextVisit.label}</button>}
      {state.renewed
        ? <Note>Plan renewal noted. No payment in this prototype.</Note>
        : <button type="button" className={btnSecondary} onClick={() => dispatch({ type: 'renew' })}>Renew my 90-day plan</button>}
      {(state.nextBooked || state.renewed) && <LinkButton to="/customer/account" secondary>See my plan summary</LinkButton>}
    </div>
  );
}

export default function S7After() {
  const { state } = useStore();
  const after = secondScan(state.scenario);
  const notImproved = state.scenario !== 'improved';

  return (
    <Screen>
      <Steps current={7} />
      <div>
        <Label>Before and after</Label>
        <Headline>Your scan shows a change since your first visit</Headline>
      </div>
      <div data-tour="before-after" className="grid grid-cols-2 border border-hairline">
        <div className="p-4"><p className="t-label text-muted">Before · 14 Apr</p><p className="t-kpi mt-1">{firstScan.index}</p></div>
        <div className="border-l border-hairline bg-ivory p-4">
          <p className="t-label text-muted">After · 9 Jun</p>
          <p className="t-kpi mt-1">{after.index}</p>
          <p className="t-card-title"><Delta d={after.index - firstScan.index} /></p>
        </div>
      </div>
      <div className="-mt-3 flex items-center justify-between"><p className="t-card-body text-muted">Hair Health Index. Not a medical measurement.</p><Chip kind="est">Illustrative</Chip></div>

      <ul className="flex flex-col gap-3">
        {metrics.map((m) => (
          <li key={m.key}>
            <div className="flex justify-between text-sm">
              <span className="t-card-title">{m.label}</span>
              <span className="t-card-body">{firstScan[m.key]} → {after[m.key]} <Delta d={after[m.key] - firstScan[m.key]} /></span>
            </div>
            <div className="mt-1 flex flex-col gap-0.5">
              <Bar value={firstScan[m.key]} tone="muted" label={`${m.label} before ${firstScan[m.key]}`} />
              <Bar value={after[m.key]} label={`${m.label} after ${after[m.key]}`} />
            </div>
          </li>
        ))}
      </ul>
      <p className="t-source -mt-2 text-muted"><span className="inline-block h-2 w-3 bg-neutral-series align-middle" /> Before <span className="ml-3 inline-block h-2 w-3 bg-ink align-middle" /> After</p>

      <ScenarioToggle />

      <div className="mt-auto flex flex-col gap-2">
        {notImproved ? <LinkButton to="/customer/adjust">What happens now</LinkButton> : <NextVisitActions />}
      </div>
    </Screen>
  );
}
