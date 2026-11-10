import { Check } from 'lucide-react';
import { ColouristCard, Chip, Headline, Label, LinkButton, Screen, Steps } from '../components/ui';

const benefits = [
  "Your salon's colourist comes to you, on your colour cycle.",
  'A hair scan before and after shows what changed.',
  'The next visit is booked before she leaves.',
];

export default function S1Invite() {
  return (
    <Screen>
      <Steps current={1} />
      <div data-tour="invite">
        <Label>Salon Aurora · Downtown Dubai</Label>
        <Headline>Salon Aurora invites you to PRO•GO Colour Plan</Headline>
      </div>
      <p className="t-quote">Hi Layla, your colour, at home, with the colourist you already know.</p>
      <ColouristCard />
      <ul className="flex flex-col gap-3">
        {benefits.map((b) => (
          <li key={b} className="flex gap-3 text-sm leading-relaxed">
            <Check size={18} className="mt-0.5 shrink-0 text-gold-text" aria-hidden />
            <span>{b}</span>
          </li>
        ))}
      </ul>
      <div className="flex flex-wrap gap-2"><Chip kind="fiction">Fictional characters</Chip><Chip>Simulated data</Chip></div>
      <div className="mt-auto"><LinkButton to="/customer/scan">Start my free scan</LinkButton></div>
    </Screen>
  );
}
