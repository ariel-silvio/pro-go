import { Bar, Chip, Headline, Label, LinkButton, Note, Screen, Steps } from '../components/ui';
import { aiNotes, firstScan, metrics } from '../data/mock';

export default function S3Result() {
  const notes = aiNotes(firstScan);
  return (
    <Screen>
      <Steps current={3} />
      <div>
        <Label>Your scan result</Label>
        <Headline>Hair Health Index</Headline>
      </div>
      <div className="flex items-end gap-3">
        <span className="t-display">{firstScan.index}</span>
        <span className="pb-2 text-sm text-muted">/ 100</span>
        <span className="ml-auto pb-2"><Chip kind="est">Illustrative</Chip></span>
      </div>
      <p className="t-card-body -mt-3 text-muted">Not a medical measurement.</p>
      <ul className="flex flex-col gap-4">
        {metrics.map((m) => (
          <li key={m.key}>
            <div className="flex justify-between text-sm"><span className="t-card-title">{m.label}</span><span>{firstScan[m.key]}</span></div>
            <div className="mt-1"><Bar value={firstScan[m.key]} label={`${m.label} ${firstScan[m.key]} out of 100`} /></div>
            <p className="t-card-body mt-1 text-muted">{m.line}</p>
          </li>
        ))}
      </ul>
      <div className="border border-hairline p-4">
        <div className="flex items-center justify-between gap-2"><p className="t-label text-gold-text">AI note</p><Chip>Simulated AI: rules, not a model</Chip></div>
        <ul className="mt-2 flex list-disc flex-col gap-1 pl-4 text-sm leading-relaxed">
          {notes.map((n) => <li key={n}>{n}</li>)}
        </ul>
      </div>
      <Note>Not a medical measurement. See a dermatologist for scalp concerns.</Note>
      <div className="mt-auto"><LinkButton to="/customer/plan">See my plan</LinkButton></div>
    </Screen>
  );
}
