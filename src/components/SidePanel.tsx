import type { ScreenMeta } from '../screens/registry';

export function SidePanel({ screen }: { screen?: ScreenMeta }) {
  return (
    <aside className="w-80 shrink-0 self-center" aria-label="What you are seeing">
      <p className="t-label text-gold-text">What you are seeing</p>
      {screen ? (
        <>
          <h2 className="t-headline mt-2">{screen.id}. {screen.title}</h2>
          <span className="gold-rule mt-3" aria-hidden />
          <p className="mt-4 text-sm leading-relaxed">{screen.seeing}</p>
          <p className="t-label mt-6 text-muted">Assumption it tests</p>
          <p className="mt-1 text-sm leading-relaxed">{screen.tests}</p>
        </>
      ) : (
        <p className="mt-2 text-sm">Pick a screen.</p>
      )}
      <p className="t-card-body mt-8 border border-hairline bg-source-note p-4 text-ink">
        Honesty note: classmates are not Dubai women who colour their hair. Their answers are a rehearsal and a usability check, not evidence of demand.
      </p>
    </aside>
  );
}
