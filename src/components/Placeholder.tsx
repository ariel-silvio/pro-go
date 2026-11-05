import { Link } from 'react-router-dom';
import type { ScreenMeta } from '../screens/registry';

// Phase 0 stub: each screen shows its title and a link to the next one.
export function Placeholder({ screen, next }: { screen: ScreenMeta; next?: ScreenMeta }) {
  return (
    <div className="flex flex-1 flex-col px-6 py-8">
      <p className="t-label text-gold-text">{screen.id}</p>
      <h1 className="t-headline mt-2">{screen.title}</h1>
      <span className="gold-rule mt-3" aria-hidden />
      <p className="mt-4 text-sm leading-relaxed text-muted">{screen.seeing}</p>
      <p className="t-card-body mt-2 text-muted">Screen content arrives in the next phase.</p>
      {next && (
        <Link to={next.path} className="t-label mt-auto flex min-h-12 items-center justify-center bg-ink px-6 text-paper">
          Next: {next.title}
        </Link>
      )}
    </div>
  );
}
