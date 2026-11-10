import { useLocation } from 'react-router-dom';
import { feedbackReady } from '../config';
import { FeedbackButton } from './FeedbackButton';
import { personaFromPath } from './PersonaSwitcher';

export function Footer() {
  const { pathname } = useLocation();
  return (
    <footer className="border-t border-hairline bg-ivory px-4 pb-4 pt-4 text-center">
      {feedbackReady() && <>
        <FeedbackButton persona={personaFromPath(pathname)} />
        <p className="t-source mt-2 text-muted">Anonymous. Do not enter personal data.</p>
      </>}
      <p className={`t-source text-muted ${feedbackReady() ? 'mt-2' : ''}`}>
        Student project for IE Business School. Not affiliated with or endorsed by L'Oréal. Fictional characters and simulated data.
      </p>
    </footer>
  );
}
