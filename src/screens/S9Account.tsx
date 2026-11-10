import { Package, CalendarDays, RefreshCw } from 'lucide-react';
import { CONFIG, aed, eur } from '../config';
import { Card, Chip, ColouristCard, Headline, Label, LinkButton, Note, Screen } from '../components/ui';
import { firstScan, nextVisit, plansFor, priceVariants, secondScan, slots, weekTwelveScan } from '../data/mock';
import { useStore } from '../state/store';

export default function S9Account() {
  const { state } = useStore();
  const variant = priceVariants.find((v) => v.id === state.variantId) ?? priceVariants[0];
  const plan = plansFor(variant).find((p) => p.id === state.plan)!;
  const first = slots.find((s) => s.id === state.slotId) ?? slots[1];
  const after = secondScan(state.scenario);
  const planPrice = plan.priceAED * plan.visits;

  const row = 'flex items-start gap-3 border-t border-hairline py-3 first:border-t-0';
  return (
    <Screen>
      <div>
        <Label>My PRO•GO</Label>
        <Headline>Your Colour Plan</Headline>
      </div>
      <Card>
        <div className="flex items-baseline justify-between">
          <span className="font-serif text-2xl">{plan.name}</span>
          <span className="t-source font-medium uppercase tracking-[0.1em] text-positive">Active</span>
        </div>
        <p className="t-card-title mt-2">{aed(planPrice)} <span className="font-normal text-muted">per 90-day plan</span></p>
        {CONFIG.SHOW_EUR && <p className="t-source text-muted">about {eur(planPrice)} · {plan.visits} home visits included</p>}
      </Card>

      <div className="border border-hairline px-4">
        <div className={row}>
          <CalendarDays size={18} className="mt-0.5 shrink-0 text-gold-text" aria-hidden />
          <div>
            <p className="t-card-title">Next visit</p>
            <p className="t-card-body">{state.nextBooked ? `${nextVisit.label} 2027, ${nextVisit.time}, with Dana` : 'Not booked yet: book it from your result.'}</p>
          </div>
        </div>
        <div className={row}>
          <Package size={18} className="mt-0.5 shrink-0 text-gold-text" aria-hidden />
          <div>
            <p className="t-card-title">Colour-care kit</p>
            <p className="t-card-body">Salon-grade kit sent after your first visit ({first.label}). Next kit before your second visit.</p>
          </div>
        </div>
        <div className={row}>
          <RefreshCw size={18} className="mt-0.5 shrink-0 text-gold-text" aria-hidden />
          <div>
            <p className="t-card-title">Renewal</p>
            <p className="t-card-body">{state.renewed ? 'Renewal noted for' : 'Plan renews on'} 13 Jul 2027 (90 days after your first visit). Cancel any time before.</p>
          </div>
        </div>
      </div>

      <div>
        <p className="t-label text-muted">Your scans</p>
        <p className="mt-1 text-sm">Hair Health Index {firstScan.index} on 14 Apr → {after.index} on 9 Jun{state.scenario === 'improved' && <> → {weekTwelveScan.index} on {weekTwelveScan.label}</>} <Chip kind="est">Illustrative</Chip></p>
        {state.scenario === 'improved' && <p className="t-card-body text-muted">Week 12: scanned at home with the app, no visit needed.</p>}
        <p className="t-card-body text-muted">Not a medical measurement.</p>
      </div>
      <ColouristCard subtitle="Your colourist, Salon Aurora" />
      <Note>Prototype: no payment, no real booking, no delivery.</Note>
      <div className="mt-auto"><LinkButton to="/customer/after" secondary>Back to my result</LinkButton></div>
    </Screen>
  );
}
