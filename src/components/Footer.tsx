import { FeedbackButton } from './FeedbackButton';

export function Footer() {
  return (
    <footer className="border-t border-hairline bg-ivory px-4 pb-4 pt-4 text-center">
      <FeedbackButton />
      <p className="t-source mt-2 text-muted">Anonymous. Do not enter personal data.</p>
      <p className="t-source mt-2 text-muted">
        Student project for IE Business School. Not affiliated with or endorsed by L'Oréal. Fictional characters and simulated data.
      </p>
    </footer>
  );
}
