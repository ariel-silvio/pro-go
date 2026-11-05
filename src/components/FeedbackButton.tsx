import { MessageSquare } from 'lucide-react';
import { CONFIG, feedbackReady } from '../config';

export function feedbackUrl(params: Record<string, string> = {}) {
  const url = new URL(CONFIG.FEEDBACK_FORM_URL);
  Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  return url.toString();
}

const base = 't-label inline-flex min-h-11 items-center gap-2 border px-4';

export function FeedbackButton({ persona = 'customer' }: { persona?: string }) {
  if (!feedbackReady()) {
    return <button type="button" disabled className={`${base} border-hairline text-muted`}>Form link coming soon</button>;
  }
  return (
    <a href={feedbackUrl({ persona })} target="_blank" rel="noopener noreferrer" className={`${base} border-ink text-ink`}>
      <MessageSquare size={14} aria-hidden /> Give feedback
    </a>
  );
}
