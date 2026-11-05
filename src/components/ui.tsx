import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

type ChipKind = 'sim' | 'low' | 'est' | 'fiction';
const chipStyle: Record<ChipKind, string> = {
  sim: 'border-ink text-ink',
  low: 'border-warn text-warn',
  est: 'border-gold-text text-gold-text',
  fiction: 'border-hairline text-muted',
};

export function Chip({ kind = 'sim', children }: { kind?: ChipKind; children: ReactNode }) {
  return <span className={`t-source inline-block border px-2 py-0.5 font-medium uppercase tracking-[0.1em] ${chipStyle[kind]}`}>{children}</span>;
}

export function Label({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <p className={`t-label text-gold-text ${className}`}>{children}</p>;
}

export function Headline({ children, as: As = 'h1' }: { children: ReactNode; as?: 'h1' | 'h2' }) {
  return (
    <>
      <As className="t-headline mt-2">{children}</As>
      <span className="gold-rule mt-3" aria-hidden />
    </>
  );
}

const btnBase = 't-label flex min-h-12 w-full items-center justify-center px-6 text-center';
export const btnPrimary = `${btnBase} bg-ink text-paper hover:bg-[#2a2a2a]`;
export const btnSecondary = `${btnBase} border border-ink bg-paper text-ink hover:bg-ivory`;

export function LinkButton({ to, children, secondary }: { to: string; children: ReactNode; secondary?: boolean }) {
  return <Link to={to} className={secondary ? btnSecondary : btnPrimary}>{children}</Link>;
}

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <div className={`border border-hairline bg-paper p-4 ${className}`}>{children}</div>;
}

export function Note({ children }: { children: ReactNode }) {
  return <p className="t-card-body border border-hairline bg-source-note px-3 py-2 text-ink">{children}</p>;
}

export function Avatar({ initial, size = 44 }: { initial: string; size?: number }) {
  return (
    <span aria-hidden className="flex shrink-0 items-center justify-center rounded-full border border-gold bg-ivory font-serif text-ink"
      style={{ width: size, height: size, fontSize: size * 0.45 }}>
      {initial}
    </span>
  );
}

export function ColouristCard({ subtitle = 'Certified colourist, Salon Aurora' }: { subtitle?: string }) {
  return (
    <Card className="flex items-center gap-3">
      <Avatar initial="D" />
      <div className="min-w-0">
        <p className="t-card-title">Dana</p>
        <p className="t-card-body text-muted">{subtitle}</p>
      </div>
      <span className="ml-auto"><Chip kind="fiction">Fictional</Chip></span>
    </Card>
  );
}

export function Screen({ children }: { children: ReactNode }) {
  return <div className="flex flex-1 flex-col gap-5 px-6 pb-8 pt-6">{children}</div>;
}

export function Steps({ current }: { current: number }) {
  return (
    <div className="flex items-center gap-1" role="img" aria-label={`Step ${current} of 7`}>
      {Array.from({ length: 7 }, (_, i) => (
        <span key={i} className={`h-0.5 flex-1 ${i < current ? 'bg-ink' : 'bg-hairline'}`} />
      ))}
    </div>
  );
}

export function Bar({ value, tone = 'ink', label }: { value: number; tone?: 'ink' | 'gold' | 'muted'; label?: string }) {
  const fill = tone === 'gold' ? 'bg-gold' : tone === 'muted' ? 'bg-neutral-series' : 'bg-ink';
  return (
    <div className="h-2 w-full bg-ivory" role="img" aria-label={label ?? `${value} out of 100`}>
      <div className={`h-full ${fill}`} style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}
