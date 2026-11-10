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

// Week 12: Layla re-scans at home with the app (film: 58 -> 66 -> 74). Only when the visit result improved.
export const weekTwelveScan = { index: 74, takenAt: '2027-07-07', label: '7 Jul' };

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

// Salon Aurora's colourist roster. Lina's home-service permit is not verified yet (shows the Dubai permit risk).
export const colourists = [
  { id: 'dana', name: 'Dana', initial: 'D', salon: 'aurora', permitDefault: true },
  { id: 'rana', name: 'Rana', initial: 'R', salon: 'aurora', permitDefault: true },
  { id: 'lina', name: 'Lina', initial: 'L', salon: 'aurora', permitDefault: false },
];

export const customer = { name: 'Layla', age: 34, area: 'Business Bay', cycleWeeks: 8 };

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

// ---------- Phase 2: colourist, salon and CEO views ----------

// Dana's day. Layla's card reads live demo state; the other two are fixed.
export const todaysVisits = [
  { id: 'v-hala', time: '10:00', customer: 'Hala', area: 'Downtown Dubai', service: 'Essential: roots touch-up + treatment', scan: 64, note: 'Prefers ammonia-free colour.' },
  { id: 'v-sara', time: '14:00', customer: 'Sara', area: 'Business Bay', service: 'Signature: balayage touch-up + treatment', scan: 71, note: 'Second visit of her plan.' },
  { id: 'v-maya', time: '18:00', customer: 'Layla', area: 'Business Bay', service: '', scan: firstScan.index, note: 'First visit. Low moisture.' },
];

export const visitSteps = ['Scan', 'Colour', 'Treatment', 'Re-scan', 'Book next visit'];

// Salon Aurora's client records (fictional). Only clients who agreed to be contacted can be invited.
export const salonClients = [
  { id: 'c-maya', name: 'Layla', lastVisit: '3 Mar 2027', cycleWeeks: 8, consent: true, active: true },
  { id: 'c-hala', name: 'Hala', lastVisit: '10 Mar 2027', cycleWeeks: 6, consent: true, active: true },
  { id: 'c-sara', name: 'Sara', lastVisit: '24 Feb 2027', cycleWeeks: 10, consent: true, active: true },
  { id: 'c-noura', name: 'Noura', lastVisit: '17 Mar 2027', cycleWeeks: 8, consent: true, active: false },
  { id: 'c-reem', name: 'Reem', lastVisit: '2 Mar 2027', cycleWeeks: 12, consent: false, active: false },
  { id: 'c-leila', name: 'Leila', lastVisit: '28 Feb 2027', cycleWeeks: 8, consent: true, active: false },
  { id: 'c-dina', name: 'Dina', lastVisit: '19 Mar 2027', cycleWeeks: 6, consent: false, active: false },
  { id: 'c-amira', name: 'Amira', lastVisit: '11 Mar 2027', cycleWeeks: 10, consent: true, active: false },
  { id: 'c-yasmin', name: 'Yasmin', lastVisit: '5 Mar 2027', cycleWeeks: 8, consent: true, active: false },
  { id: 'c-farah', name: 'Farah', lastVisit: '22 Feb 2027', cycleWeeks: 12, consent: false, active: false },
  { id: 'c-lara', name: 'Lara', lastVisit: '14 Mar 2027', cycleWeeks: 8, consent: true, active: false },
  { id: 'c-hind', name: 'Hind', lastVisit: '8 Mar 2027', cycleWeeks: 10, consent: true, active: false },
];

// Cannibalisation monitor, simulated pilot month.
export const cannibalisation = [
  { salon: 'Salon Aurora', movedToHome: 18, newToSalon: 0 },
  { salon: 'Studio Marjan', movedToHome: 11, newToSalon: 1 },
  { salon: 'Atelier Noor', movedToHome: 7, newToSalon: 0 },
];

// CEO scoreboard. Targets from the M2 dashboard (Team D proposal). `sim` values are invented, shown only on demand.
export interface Kpi { id: string; name: string; target: string; later: string; definition: string; sim: string; simOnTrack: boolean; }
export const kpis: Kpi[] = [
  { id: 'subs', name: 'Active care subscribers', target: '300 in 2027', later: '25k in 2030 · 1m in 2035',
    definition: 'Customers with an active product subscription linked to a certified professional.', sim: '212', simOnTrack: false },
  { id: 'repeat', name: 'Repeat-visit rate', target: '40% pass line, 2027 pilot', later: '60% in 2030 · 70% in 2035',
    definition: 'Share of customers who book a second at-home PRO•GO visit within 90 days, instead of going back to the salon chair.', sim: '43%', simOnTrack: true },
  { id: 'margin', name: 'Margin per visit', target: 'Positive by Q4 2027', later: 'Checked at the Q4 2027 review',
    definition: 'Visit price minus pay to the partner salon, travel and products.', sim: 'AED +125', simOnTrack: true },
  { id: 'score', name: 'Hair score change', target: '+5 points or more in 12 weeks', later: 'Tracked every week in the pilot',
    definition: 'Average change in the Hair Health Index from the first scan to the week-12 scan at home.', sim: '+7', simOnTrack: true },
  { id: 'retention', name: '90-day subscription retention', target: '60% or more by end 2028', later: '',
    definition: 'Share of subscribers who renew their 90-day plan.', sim: '58%', simOnTrack: false },
  { id: 'newsalon', name: 'New-to-salon customers', target: '30% of PRO•GO clients', later: '2028 review',
    definition: 'PRO•GO clients who were not clients of the partner salon before.', sim: '4%', simOnTrack: false },
  { id: 'uplift', name: 'Partner salon income uplift', target: '+10% per partner salon by 2030', later: '',
    definition: 'Extra income for each partner salon from PRO•GO visits and its share.', sim: '+3%', simOnTrack: false },
];

// Margin per visit calculator defaults (Team D estimates, LOW confidence).
export const calcDefaults = { price: 500, salonPay: 230, travel: 60, products: 85, visitsPerDay: 2.5 };

// Appendix B: where the first EUR 3m goes (Team D assumptions, LOW). EUR thousands.
export const firstThreeMillion = [
  { line: 'PRO•GO venture team (about 5 people, 12 months)', k: 700 },
  { line: 'Customer acquisition (resident events, concierge, launch offers)', k: 400 },
  { line: 'Contingency (about 13%)', k: 350 },
  { line: 'Prep for the 2028 build (design, discovery, vendors)', k: 300 },
  { line: 'Partner salon onboarding and minimum-income floor', k: 250 },
  { line: 'Legal, permits, insurance, data protection, claims review', k: 200 },
  { line: 'Quality and safety (dermatologist advisor, mystery visits)', k: 150 },
  { line: 'Research and measurement', k: 150 },
  { line: 'Products and samples', k: 150 },
  { line: 'Professional training, certification, scan kits', k: 120 },
  { line: 'Manual-MVP tools (chat booking, CRM, payments, dashboard)', k: 120 },
  { line: 'Visit delivery (about 1,800 visits at about EUR 60)', k: 110 },
];
