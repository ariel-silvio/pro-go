import { AlertTriangle, Check, Lock } from 'lucide-react';
import { CONFIG, aed } from '../config';
import { Avatar, Card, Chip, Headline, Label, Note, Screen } from '../components/ui';
import { cannibalisation, colourists, plansFor, priceVariants, salonClients, scenarios } from '../data/mock';
import { useStore } from '../state/store';

function Section({ title, children, chip, tour }: { title: string; children: React.ReactNode; chip?: React.ReactNode; tour?: string }) {
  return (
    <section data-tour={tour} className="flex flex-col gap-3">
      <div className="flex items-center justify-between gap-2 border-b border-hairline pb-2">
        <h2 className="t-label text-gold-text">{title}</h2>{chip}
      </div>
      {children}
    </section>
  );
}

export default function SalonHome() {
  const { state, dispatch } = useStore();
  const variant = priceVariants.find((v) => v.id === state.variantId) ?? priceVariants[0];
  const price = plansFor(variant).find((p) => p.id === state.plan)!.priceAED;
  const share = state.salonShare;
  const sharePct = Math.round(share * 100);

  return (
    <Screen>
      <div>
        <Label>Salon Aurora · Downtown Dubai</Label>
        <Headline>Partner salon dashboard</Headline>
        <p className="t-card-body mt-3 text-muted">Owner: Mrs. Karim (fictional)</p>
      </div>

      <Section title="Alerts">
        {state.alerts.length === 0 ? (
          <p className="t-card-body text-muted">No alerts. Tip: set the customer's scan outcome to Flat or Worse on S7 to see one here.</p>
        ) : state.alerts.map((a) => (
          <div key={a.id} className="flex gap-3 border border-negative p-3" role="status">
            <AlertTriangle size={18} className="mt-0.5 shrink-0 text-negative" aria-hidden />
            <div>
              <p className="t-card-title">{a.text}</p>
              <p className="t-card-body text-muted">Scan outcome: {scenarios[a.scenario].label}. Call her today, ask Dana to adjust the treatment, next scan free.</p>
            </div>
          </div>
        ))}
      </Section>

      <Section title="Clients from salon records" chip={<Chip kind="fiction">Fictional</Chip>}>
        <p className="t-card-body text-muted">Only clients who agreed to be contacted can be invited.</p>
        <div className="border border-hairline">
          <table className="w-full text-left">
            <caption className="sr-only">Salon Aurora clients, consent and PRO•GO status</caption>
            <thead className="t-source bg-ivory uppercase tracking-[0.1em] text-muted">
              <tr><th className="px-2 py-2 font-medium">Client</th><th className="px-2 py-2 font-medium">Cycle</th><th className="px-2 py-2 font-medium">Consent</th><th className="px-2 py-2 font-medium"><span className="sr-only">PRO•GO</span></th></tr>
            </thead>
            <tbody className="t-card-body">
              {salonClients.map((c) => {
                const invited = state.invited.includes(c.id);
                return (
                  <tr key={c.id} className="border-t border-hairline">
                    <td className="px-2 py-1.5"><span className="t-card-title">{c.name}</span><br /><span className="t-source text-muted">Last visit {c.lastVisit}</span></td>
                    <td className="px-2 py-1.5">{c.cycleWeeks} wk</td>
                    <td className="px-2 py-1.5">{c.consent ? 'Yes' : <span className="text-muted">No</span>}</td>
                    <td className="px-2 py-1.5 text-right">
                      {c.active ? <span className="t-source font-medium uppercase tracking-[0.1em] text-positive">Active plan</span>
                        : invited ? <span className="t-source inline-flex items-center gap-1 uppercase tracking-[0.1em]"><Check size={12} aria-hidden />Invited</span>
                        : c.consent ? (
                          <button type="button" onClick={() => dispatch({ type: 'invite', id: c.id })}
                            className="t-source min-h-11 border border-ink px-2 font-medium uppercase tracking-[0.1em]">Invite</button>
                        ) : (
                          <span className="t-source inline-flex items-center gap-1 text-muted" title="No consent to contact"><Lock size={12} aria-hidden />No consent</span>
                        )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p className="t-source text-muted">"Invite" is simulated: no message is sent.</p>
      </Section>

      <Section tour="permits" title="Colourist roster" chip={<Chip kind="low">Permit rule not verified</Chip>}>
        <ul className="flex flex-col gap-2">
          {colourists.map((c) => {
            const ok = !!state.permits[c.id];
            return (
              <li key={c.id} className="border border-hairline p-3">
                <div className="flex items-center gap-3">
                  <Avatar initial={c.initial} size={36} />
                  <span className="t-card-title flex-1">{c.name}</span>
                  <span className={`t-source font-medium uppercase tracking-[0.1em] ${ok ? 'text-positive' : 'text-negative'}`}>{ok ? 'Can be assigned' : 'Cannot be assigned'}</span>
                </div>
                <label className="mt-2 flex min-h-11 cursor-pointer items-center gap-3">
                  <input type="checkbox" checked={ok} onChange={() => dispatch({ type: 'togglePermit', id: c.id })} className="h-5 w-5 accent-[var(--ink)]" />
                  <span className="t-card-body">Home-service permit verified</span>
                </label>
                {!ok && <p className="t-card-body text-negative">Not assigned to home visits until this colourist's named permit is verified.</p>}
              </li>
            );
          })}
        </ul>
        <Note>Dubai asks for a separate home-service permit on top of the salon licence, tied to named staff (BusinessDubai; Gulf News). Not verified with Dubai Municipality.</Note>
      </Section>

      <Section title="Revenue share per visit" chip={<Chip kind="est">Team D proposal</Chip>}>
        <Card>
          <label className="block">
            <span className="flex justify-between text-sm"><span className="t-card-title">Salon share</span><span>{sharePct}%</span></span>
            <input type="range" min={20} max={60} step={1} value={sharePct}
              onChange={(e) => dispatch({ type: 'setShare', value: Number(e.target.value) / 100 })}
              className="mt-2 h-11 w-full accent-[var(--ink)]" aria-valuetext={`${sharePct} percent`} />
          </label>
          <p className="text-sm">On a {aed(price)} visit ({state.plan === 'essential' ? 'Essential' : 'Signature'}, price variant {variant.id}) the salon receives <span className="t-card-title">{aed(Math.round(price * share))}</span>.</p>
          {sharePct !== Math.round(CONFIG.SALON_SHARE_DEFAULT * 100) && <p className="t-source mt-1 text-muted">Default: {Math.round(CONFIG.SALON_SHARE_DEFAULT * 100)}%</p>}
        </Card>
        <Card>
          <p className="t-label text-muted">Partner salon income uplift</p>
          <p className="t-kpi mt-1">+10%</p>
          <p className="t-card-body text-muted">Target per partner salon by 2030. Tracked from the Q2 2027 pilot.</p>
        </Card>
      </Section>

      <Section title="Cannibalisation monitor" chip={<Chip>Simulated</Chip>}>
        <div className="border border-hairline">
          <table className="w-full text-left">
            <caption className="sr-only">Visits moved from the salon chair to home, and new-to-salon customers, per partner salon</caption>
            <thead className="t-source bg-ivory uppercase tracking-[0.1em] text-muted">
              <tr><th className="px-2 py-2 font-medium">Salon</th><th className="px-2 py-2 text-right font-medium">Chair → home</th><th className="px-2 py-2 text-right font-medium">New to salon</th></tr>
            </thead>
            <tbody className="t-card-body">
              {cannibalisation.map((r) => (
                <tr key={r.salon} className="border-t border-hairline">
                  <td className="px-2 py-2 t-card-title">{r.salon}</td>
                  <td className="px-2 py-2 text-right">{r.movedToHome}</td>
                  <td className="px-2 py-2 text-right">{r.newToSalon}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Note>In 2027 we expect new-to-salon near zero; the 30% target is a 2028 review.</Note>
      </Section>
    </Screen>
  );
}
