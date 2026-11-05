// All prototype data. Fictional people and salons, illustrative numbers. No network calls.

export type Persona = 'customer' | 'colourist' | 'salon' | 'ceo';
export type Scenario = 'improved' | 'flat' | 'worse';
export type PlanId = 'essential' | 'signature';
export type VariantId = 'v1' | 'v2' | 'v3';
export type MetricKey = 'moisture' | 'strength' | 'shine' | 'scalp';

export interface Scan { index: number; moisture: number; strength: number; shine: number; scalp: number; takenAt: string; }
export interface Plan { id: PlanId; name: string; visits: number; priceAED: number; includes: string[]; }
export interface PriceVariant { id: VariantId; essential: number; signature: number; }
export interface Slot { id: string; date: string; label: string; time: string; }

export const priceVariants: PriceVariant[] = [
  { id: 'v1', essential: 450, signature: 600 },
  { id: 'v2', essential: 550, signature: 700 },
  { id: 'v3', essential: 650, signature: 800 },
];

export const scenarios: Record<Scenario, { label: string; delta: Omit<Scan, 'takenAt'> }> = {
  improved: { label: 'Improved', delta: { index: +8, moisture: +10, strength: +7, shine: +9, scalp: +4 } },
  flat: { label: 'Flat', delta: { index: +1, moisture: +2, strength: 0, shine: +1, scalp: 0 } },
  worse: { label: 'Worse', delta: { index: -4, moisture: -5, strength: -3, shine: -2, scalp: -1 } },
};

export const firstScan: Scan = { index: 58, moisture: 52, strength: 61, shine: 55, scalp: 70, takenAt: '2027-04-14' };

export function secondScan(s: Scenario): Scan {
  const d = scenarios[s].delta;
  return {
    index: firstScan.index + d.index,
    moisture: firstScan.moisture + d.moisture,
    strength: firstScan.strength + d.strength,
    shine: firstScan.shine + d.shine,
    scalp: firstScan.scalp + d.scalp,
    takenAt: '2027-06-09',
  };
}

export const metrics: { key: MetricKey; label: string; line: string }[] = [
  { key: 'moisture', label: 'Moisture', line: 'How much water your hair holds. Low often feels dry at the ends.' },
  { key: 'strength', label: 'Strength', line: 'How well strands hold up to brushing and styling.' },
  { key: 'shine', label: 'Shine', line: 'How much light your hair reflects.' },
  { key: 'scalp', label: 'Scalp balance', line: 'The balance between oily and dry on your scalp.' },
];

export function plansFor(v: PriceVariant): Plan[] {
  return [
    { id: 'essential', name: 'Essential', visits: 2, priceAED: v.essential,
      includes: ['Colour or roots touch-up', 'Hair treatment', 'Before-and-after scan', 'Colour-care kit between visits'] },
    { id: 'signature', name: 'Signature', visits: 2, priceAED: v.signature,
      includes: ['Balayage or highlights touch-up', 'Hair treatment', 'Before-and-after scan', 'Colour-care kit between visits'] },
  ];
}

export const salons = [
  { id: 'aurora', name: 'Salon Aurora', area: 'Downtown Dubai', owner: 'Mrs. Karim' },
  { id: 'marjan', name: 'Studio Marjan', area: 'Business Bay' },
  { id: 'noor', name: 'Atelier Noor', area: 'Business Bay' },
];

export const colourists = [
  { id: 'dana', name: 'Dana', initial: 'D', salon: 'aurora' },
  { id: 'rana', name: 'Rana', initial: 'R', salon: 'marjan' },
  { id: 'lina', name: 'Lina', initial: 'L', salon: 'noor' },
];

export const customer = { name: 'Maya', age: 34, area: 'Business Bay', cycleWeeks: 8 };

// First visit slots, April 2027 (pilot runs from Q2 2027). Dates checked against the calendar.
export const slots: Slot[] = [
  { id: 's1', date: '2027-04-13', label: 'Tue 13 Apr', time: '18:00' },
  { id: 's2', date: '2027-04-14', label: 'Wed 14 Apr', time: '18:00' },
  { id: 's3', date: '2027-04-15', label: 'Thu 15 Apr', time: '10:00' },
  { id: 's4', date: '2027-04-17', label: 'Sat 17 Apr', time: '10:00' },
  { id: 's5', date: '2027-04-17', label: 'Sat 17 Apr', time: '14:00' },
  { id: 's6', date: '2027-04-19', label: 'Mon 19 Apr', time: '18:00' },
];

// Day 56 after the first visit (8-week colour cycle).
export const nextVisit = { label: 'Wed 9 Jun', time: '18:00' };

// Patch test: 48 h before the visit.
export function patchTestDay(slot: Slot) {
  const d = new Date(slot.date + 'T12:00:00Z');
  d.setUTCDate(d.getUTCDate() - 2);
  return d.toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'UTC' });
}

// The 3-hour home visit, in minutes.
export const visitTimeline = [
  { label: 'Set-up and scan', minutes: 20 },
  { label: 'Colour', minutes: 100 },
  { label: 'Treatment', minutes: 45 },
  { label: 'Re-scan and next booking', minutes: 15 },
];

export const checklistItems = [
  { id: 'patch', label: 'Patch test done', hint: '48 h before the visit, using the kit from your salon.' },
  { id: 'space', label: 'Space and sink ready', hint: 'A chair near a sink, and a towel.' },
  { id: 'air', label: 'Ventilation', hint: 'Open a window or turn on the fan.' },
];

// Simulated AI: plain if/then rules, not a model.
export function aiNotes(scan: Scan, cycleWeeks = customer.cycleWeeks): string[] {
  const notes: string[] = [];
  if (scan.moisture < 60) notes.push(`Colour every ${cycleWeeks} weeks plus low moisture: a treatment each visit is suggested.`);
  if (scan.strength < 65) notes.push('Strength is in the middle range: a gentle colour technique is suggested.');
  if (scan.shine < 60) notes.push('Shine is below 60: a gloss step after colour is suggested.');
  if (notes.length === 0) notes.push('Scores are in a good range: keep your colour cycle and care kit.');
  return notes;
}
