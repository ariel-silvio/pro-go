import { CONFIG, aed, eur } from '../config';
import { Card, Chip, Headline, Label, Note, Screen, btnSecondary } from '../components/ui';
import { calcDefaults, firstThreeMillion, kpis } from '../data/mock';
import { useStore } from '../state/store';

type CalcKey = keyof typeof calcDefaults;
const inputs: { key: CalcKey; label: string; min: number; max: number; step: number; unit: 'aed' | 'n' }[] = [
  { key: 'price', label: 'Price per visit', min: 350, max: 700, step: 10, unit: 'aed' },
  { key: 'salonPay', label: 'Pay to partner salon (professional time and salon share)', min: 100, max: 400, step: 5, unit: 'aed' },
  { key: 'travel', label: 'Travel', min: 0, max: 150, step: 5, unit: 'aed' },
  { key: 'products', label: 'Products', min: 0, max: 200, step: 5, unit: 'aed' },
  { key: 'visitsPerDay', label: 'Visits per day per colourist', min: 1.5, max: 4, step: 0.5, unit: 'n' },
];

function MarginCalculator() {
  const { state, dispatch } = useStore();
  const c = state.calc;
  const cost = c.salonPay + c.travel + c.products;
  const margin = c.price - cost;
  const pct = c.price ? Math.round((margin / c.price) * 100) : 0;
  const positive = margin > 0;

  return (
    <section className="flex flex-col gap-3" aria-labelledby="calc-h">
      <div className="flex items-center justify-between gap-2 border-b border-hairline pb-2">
        <h2 id="calc-h" className="t-label text-gold-text">Margin per visit calculator</h2>
        <Chip kind="low">Team D estimates, LOW</Chip>
      </div>
      <p className="t-card-body text-muted">The riskiest number. Move the price and the costs to see where a visit stops paying for itself.</p>
      <Card className="flex flex-col gap-4">
        {inputs.map((i) => (
          <label key={i.key} className="block">
            <span className="flex items-baseline justify-between gap-2 text-sm">
              <span className="t-card-body">{i.label}</span>
              <span className="t-card-title whitespace-nowrap">
                {i.unit === 'aed' ? aed(c[i.key]) : c[i.key]}
                {i.unit === 'aed' && CONFIG.SHOW_EUR && <span className="t-source ml-1 font-normal text-muted">{eur(c[i.key])}</span>}
              </span>
            </span>
            <input type="range" min={i.min} max={i.max} step={i.step} value={c[i.key]}
              onChange={(e) => dispatch({ type: 'setCalc', key: i.key, value: Number(e.target.value) })}
              className="h-11 w-full accent-[var(--ink)]"
              aria-valuetext={i.unit === 'aed' ? `${c[i.key]} dirhams` : String(c[i.key])} />
            {i.key === 'price' && (
              <span className="t-source block text-muted">Break-even on variable cost: {aed(cost)}</span>
            )}
          </label>
        ))}
        <p className="t-source text-muted">Exchange rate: {CONFIG.AED_PER_EUR} AED per euro.</p>
      </Card>

      <div data-tour="calc" className={`border-2 p-4 ${positive ? 'border-positive' : 'border-negative'}`} aria-live="polite">
        <p className={`t-label ${positive ? 'text-positive' : 'text-negative'}`}>{positive ? '▲ Positive margin' : '▼ Negative margin'} at {aed(c.price)}</p>
        <dl className="mt-3 grid grid-cols-3 gap-2">
          <div><dt className="t-source text-muted">Variable cost</dt><dd className="t-card-title">{aed(cost)}</dd></div>
          <div><dt className="t-source text-muted">Margin per visit</dt><dd className={`t-card-title ${positive ? 'text-positive' : 'text-negative'}`}>{margin >= 0 ? '+' : '−'}{aed(Math.abs(margin))}</dd></div>
          <div><dt className="t-source text-muted">Margin</dt><dd className="t-card-title">{pct}%</dd></div>
        </dl>
        <p className="t-card-body mt-3">Per colourist day ({c.visitsPerDay} visits): <span className="t-card-title">{margin >= 0 ? '+' : '−'}{aed(Math.round(Math.abs(margin * c.visitsPerDay)))}</span></p>
      </div>
      <Note>Roots-only visits at AED 150 to 420 in salons would not cover this. That is why the pilot bundles colour with a treatment and a scan. Team D break-even estimate: about AED 420 to 500 or more per visit (LOW).</Note>
      <button type="button" className={btnSecondary} onClick={() => dispatch({ type: 'resetCalc' })}>Reset to Team D defaults</button>
    </section>
  );
}

export default function CeoScoreboard() {
  const { state, dispatch } = useStore();
  const total = firstThreeMillion.reduce((a, b) => a + b.k, 0);

  return (
    <Screen>
      <div>
        <Label>CEO scoreboard · PRO•GO pilot, Dubai</Label>
        <Headline>Are we on track for the Q4 2027 review?</Headline>
        <p className="t-card-body mt-3 text-muted">EUR 10m staged: EUR 3m now, EUR 7m held until the Q4 2027 review (repeat bookings, positive margin per visit).</p>
      </div>

      <label className="flex min-h-11 cursor-pointer items-center justify-between gap-3 border border-dashed border-muted px-3">
        <span className="t-label text-muted">Show simulated demo data</span>
        <input type="checkbox" checked={state.showSim} onChange={() => dispatch({ type: 'toggleSim' })} className="h-5 w-5 accent-[var(--ink)]" />
      </label>

      <div className="relative">
        {state.showSim && (
          <div aria-hidden className="pointer-events-none absolute inset-0 z-10 flex items-center justify-center overflow-hidden">
            <span className="-rotate-[24deg] font-serif text-[44px] tracking-[0.12em] text-negative/25">SIMULATED</span>
          </div>
        )}
        <ul className="grid grid-cols-1 gap-3">
          {kpis.map((k) => (
            <li key={k.id} className="border border-hairline bg-paper p-4">
              <div className="flex items-start justify-between gap-2">
                <h2 className="t-card-title">{k.name}</h2>
                <Chip kind="est">Team D proposal</Chip>
              </div>
              {state.showSim ? (
                <div className="mt-2 flex flex-wrap items-baseline gap-x-3 gap-y-1">
                  <span className="t-kpi whitespace-nowrap">{k.sim}</span>
                  <span className={`t-source font-medium uppercase tracking-[0.1em] ${k.simOnTrack ? 'text-positive' : 'text-negative'}`}>
                    {k.simOnTrack ? '▲ On or above target' : '▼ Below target'}
                  </span>
                </div>
              ) : null}
              <p className="mt-2 text-sm"><span className="t-label text-muted">Target </span>{k.target}</p>
              {k.later && <p className="t-card-body text-muted">{k.later}</p>}
              <p className="t-card-body mt-2 text-muted">{k.definition}</p>
            </li>
          ))}
        </ul>
        {state.showSim && <p className="t-card-body mt-2 text-negative">Simulated values, invented for the demo. Not results.</p>}
      </div>
      <p className="t-source -mt-2 text-muted">Targets: Team D M2 dashboard. Default view shows targets only.</p>

      <MarginCalculator />

      <details className="border border-hairline">
        <summary className="t-label flex min-h-11 cursor-pointer items-center px-3 text-gold-text">Where the first EUR 3m goes</summary>
        <div className="border-t border-hairline">
          <table className="w-full text-left">
            <caption className="sr-only">Use of the first EUR 3 million, EUR thousands</caption>
            <thead className="t-source bg-ivory uppercase tracking-[0.1em] text-muted"><tr><th className="px-3 py-2 font-medium">Line</th><th className="px-3 py-2 text-right font-medium">EUR k</th></tr></thead>
            <tbody className="t-card-body">
              {firstThreeMillion.map((r) => (
                <tr key={r.line} className="border-t border-hairline"><td className="px-3 py-1.5">{r.line}</td><td className="px-3 py-1.5 text-right">{r.k}</td></tr>
              ))}
              <tr className="border-t border-ink"><td className="t-card-title px-3 py-2">Total</td><td className="t-card-title px-3 py-2 text-right">{total.toLocaleString('en-GB')}</td></tr>
            </tbody>
          </table>
          <p className="t-source px-3 pb-3 text-muted">Team D assumptions, LOW confidence.</p>
        </div>
      </details>
    </Screen>
  );
}
