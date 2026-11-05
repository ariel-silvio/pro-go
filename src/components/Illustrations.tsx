// Simple line illustrations. No photos, no people.
const stroke = { fill: 'none', stroke: 'var(--ink)', strokeWidth: 1.5, strokeLinecap: 'round' as const };

function Frame({ children, label }: { children: React.ReactNode; label: string }) {
  return (
    <svg viewBox="0 0 200 140" className="h-auto w-full" role="img" aria-label={label}>
      <rect x="0.5" y="0.5" width="199" height="139" fill="var(--ivory)" stroke="var(--hairline)" />
      {children}
    </svg>
  );
}

function Grid() {
  const lines = [];
  for (let i = 1; i < 6; i++) lines.push(<line key={`v${i}`} x1={60 + i * 13.3} y1="30" x2={60 + i * 13.3} y2="110" stroke="var(--gold)" strokeWidth="0.6" />);
  for (let i = 1; i < 6; i++) lines.push(<line key={`h${i}`} x1="60" y1={30 + i * 13.3} x2="140" y2={30 + i * 13.3} stroke="var(--gold)" strokeWidth="0.6" />);
  return <g>{lines}<rect x="60" y="30" width="80" height="80" fill="none" stroke="var(--gold)" strokeWidth="1.2" /></g>;
}

export function ScanRoots() {
  return (
    <Frame label="Scanner over the roots at the crown">
      <path d="M40 120 C40 60 160 60 160 120" {...stroke} />
      {[55, 70, 85, 100, 115, 130, 145].map((x, i) => <path key={i} d={`M${x} ${118 - (i % 2) * 4} C${x - 3} 95 ${x + 3} 80 ${x} 66`} {...stroke} strokeWidth={1} />)}
      <Grid />
    </Frame>
  );
}

export function ScanLengths() {
  return (
    <Frame label="Scanner over the lengths of a hair strand">
      {[70, 85, 100, 115, 130].map((x, i) => <path key={i} d={`M${x} 15 C${x + 12} 45 ${x - 12} 85 ${x + 4} 125`} {...stroke} strokeWidth={1.2} />)}
      <Grid />
    </Frame>
  );
}

export function ScanEnds() {
  return (
    <Frame label="Scanner over the ends of the hair">
      {[70, 85, 100, 115, 130].map((x, i) => (
        <g key={i}>
          <path d={`M${x} 15 L${x + 2} 95`} {...stroke} strokeWidth={1.2} />
          <path d={`M${x + 2} 95 L${x - 3} 110 M${x + 2} 95 L${x + 6} 108`} {...stroke} strokeWidth={0.9} />
        </g>
      ))}
      <Grid />
    </Frame>
  );
}

export function Analysing() {
  return (
    <svg viewBox="0 0 200 140" className="h-auto w-full" role="img" aria-label="Analysing">
      <rect x="0.5" y="0.5" width="199" height="139" fill="var(--ivory)" stroke="var(--hairline)" />
      <Grid />
      <rect x="60" y="30" width="80" height="2" fill="var(--ink)" className="scan-line" />
    </svg>
  );
}
