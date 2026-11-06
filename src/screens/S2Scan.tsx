import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Analysing, ScanEnds, ScanLengths, ScanRoots } from '../components/Illustrations';
import { Chip, Headline, Label, Note, Screen, Steps, btnPrimary } from '../components/ui';
import { useStore } from '../state/store';

const steps = [
  { title: 'Roots at the crown', text: 'Your colourist holds the scanner over your parting.', Art: ScanRoots },
  { title: 'Lengths', text: 'Then over the middle of a strand.', Art: ScanLengths },
  { title: 'Ends', text: 'Then over the ends, where hair is often driest.', Art: ScanEnds },
];

export default function S2Scan() {
  const [step, setStep] = useState(0);
  const [analysing, setAnalysing] = useState(false);
  const { dispatch } = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!analysing) return;
    const t = setTimeout(() => { dispatch({ type: 'scanDone' }); navigate('/customer/result'); }, 1500);
    return () => clearTimeout(t);
  }, [analysing, dispatch, navigate]);

  const current = steps[step];
  return (
    <Screen>
      <Steps current={2} />
      <div>
        <Label>Free hair scan</Label>
        <Headline>{analysing ? 'Analysing…' : `Step ${step + 1} of 3: ${current.title}`}</Headline>
      </div>
      <Chip>Simulated scan</Chip>
      <div data-tour="scan">{analysing ? <Analysing /> : <current.Art />}</div>
      <p className="text-sm leading-relaxed" aria-live="polite">
        {analysing ? 'Reading the three captures.' : current.text}
      </p>
      <Note>Simulated scan. No camera is used. Not a medical or scientific measurement.</Note>
      <div className="mt-auto">
        <button type="button" disabled={analysing} className={`${btnPrimary} disabled:opacity-60`}
          onClick={() => (step < 2 ? setStep(step + 1) : setAnalysing(true))}>
          {analysing ? 'Analysing…' : step < 2 ? 'Capture (simulated)' : 'Capture and analyse'}
        </button>
      </div>
    </Screen>
  );
}
