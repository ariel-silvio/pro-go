import { useNavigate } from 'react-router-dom';
import { Check } from 'lucide-react';
import { CONFIG, aed, eur, feedbackReady, feedbackUrl } from '../config';
import { Chip, Headline, Label, Note, Screen, Steps, btnPrimary } from '../components/ui';
import { plansFor, priceVariants } from '../data/mock';
import { useStore } from '../state/store';

export default function S4Plan() {
  const { state, dispatch } = useStore();
  const navigate = useNavigate();
  const variant = priceVariants.find((v) => v.id === state.variantId) ?? priceVariants[0];
  const plans = plansFor(variant);

  const reserve = () => {
    dispatch({ type: 'reserve' });
    if (feedbackReady()) {
      window.open(feedbackUrl({ variant: variant.id, persona: 'customer', plan: state.plan }), '_blank', 'noopener,noreferrer');
    }
    navigate('/customer/slot');
  };

  return (
    <Screen>
      <Steps current={4} />
      <div>
        <Label>Your 90-day plan</Label>
        <Headline>Two home visits, one result you can see</Headline>
      </div>
      <ol className="flex flex-col gap-2 text-sm leading-relaxed">
        <li><span className="t-card-title">Day 0:</span> home visit with scan, colour, treatment and re-scan.</li>
        <li><span className="t-card-title">Between visits:</span> a salon-grade colour-care kit arrives at home.</li>
        <li><span className="t-card-title">Day 56 to 70:</span> second home visit, with a before-and-after scan.</li>
      </ol>

      <fieldset data-tour="plans" className="flex flex-col gap-3">
        <legend className="t-label mb-2 text-muted">Choose a plan</legend>
        {plans.map((p) => {
          const selected = state.plan === p.id;
          return (
            <label key={p.id}
              className={`block cursor-pointer border p-4 ${selected ? 'border-ink outline outline-1 outline-ink' : 'border-hairline'}`}>
              <input type="radio" name="plan" value={p.id} checked={selected} className="sr-only"
                onChange={() => dispatch({ type: 'choosePlan', plan: p.id })} />
              <div className="flex items-baseline justify-between gap-2">
                <span className="font-serif text-2xl">{p.name}</span>
                <span className={`h-4 w-4 shrink-0 border ${selected ? 'border-ink bg-ink' : 'border-muted'}`} aria-hidden />
              </div>
              <ul className="mt-3 flex flex-col gap-1">
                {p.includes.map((i) => (
                  <li key={i} className="t-card-body flex gap-2"><Check size={14} className="mt-0.5 shrink-0 text-gold-text" aria-hidden />{i}</li>
                ))}
              </ul>
              <div className="mt-4 border-t border-hairline pt-3">
                <p className="t-card-title">
                  {aed(p.priceAED * p.visits)} <span className="font-normal text-muted">per 90-day plan</span>
                </p>
                {CONFIG.SHOW_EUR && <p className="t-source text-muted">about {eur(p.priceAED * p.visits)}</p>}
                <p className="t-source mt-1 text-muted">
                  Subscription, renews every 90 days. Includes {p.visits} home visits <span className="whitespace-nowrap">(about {aed(p.priceAED)} each)</span>.
                </p>
              </div>
              <p className="t-source mt-2 text-right text-muted"><span className="sr-only">Price variant </span>{variant.id}</p>
            </label>
          );
        })}
      </fieldset>

      <Note>{feedbackReady() ? 'This is a prototype. No payment, no booking. "Reserve my place" opens a short anonymous form.' : 'This is a prototype. No payment, no booking.'}</Note>
      <div className="mt-auto flex flex-col gap-2">
        <button type="button" onClick={reserve} className={btnPrimary}>Reserve my place</button>
        <div className="flex justify-center"><Chip kind="low">Price: Team D assumption, LOW confidence</Chip></div>
      </div>
    </Screen>
  );
}
