import { Navigate } from 'react-router-dom';
import { ColouristCard, Headline, Label, Note, Screen } from '../components/ui';
import { NextVisitActions, ScenarioToggle } from './S7After';
import { useStore } from '../state/store';

export default function S8Adjust() {
  const { state } = useStore();
  if (state.scenario === 'improved') return <Navigate to="/customer/after" replace />;
  return (
    <Screen>
      <div>
        <Label>Plan adjustment</Label>
        <Headline>Your result did not improve as hoped</Headline>
      </div>
      <p className="t-quote">Dana and your salon will adjust your treatment. No extra charge for the next scan.</p>
      <ColouristCard />
      <ul className="flex flex-col gap-2 text-sm leading-relaxed">
        <li><span className="t-card-title">Today:</span> Salon Aurora has been told and will call you.</li>
        <li><span className="t-card-title">Next visit:</span> a different treatment, chosen by Dana.</li>
        <li><span className="t-card-title">Next scan:</span> free of charge.</li>
      </ul>
      <Note>The scan shows a change, not its cause. Simulated result.</Note>
      <ScenarioToggle />
      <div className="mt-auto"><NextVisitActions /></div>
    </Screen>
  );
}
