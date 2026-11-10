import { MessageSquare } from 'lucide-react';
import { feedbackReady, feedbackUrl } from '../config';

const base = 't-label inline-flex min-h-11 items-center gap-2 border px-4';

export function FeedbackButton({ persona = 'customer' }: { persona?: string }) {
  if (!feedbackReady()) {
    return null;   // no form yet: show nothing rather than a disabled "coming soon" button
  }
  return (
    <a href={feedbackUrl({ persona })} target="_blank" rel="noopener noreferrer" className={`${base} border-ink text-ink`}>
      <MessageSquare size={14} aria-hidden /> Give feedback
    </a>
  );
}
