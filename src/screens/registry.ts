// One place for every screen: route, title and the "What you are seeing" side-panel text.
export interface ScreenMeta {
  id: string;
  path: string;
  title: string;
  seeing: string;
  tests: string;
  note?: string;
}

export const customerScreens: ScreenMeta[] = [
  { id: 'S1', path: '/customer/invite', title: 'Invite from her salon',
    seeing: "Maya's own salon invites her to PRO•GO Colour Plan and introduces the colourist who will visit her.",
    tests: 'A salon-routed invitation, with her own colourist, feels trustworthy.' },
  { id: 'S2', path: '/customer/scan', title: 'Free hair scan (simulated)',
    seeing: 'Three illustrative capture steps. No camera is used.',
    tests: 'A free scan is a good reason to start.' },
  { id: 'S3', path: '/customer/result', title: 'Scan result',
    seeing: 'An illustrative Hair Health Index with four sub-scores and a rule-based note.',
    tests: 'Customers want healthy hair with a number they can see.' },
  { id: 'S4', path: '/customer/plan', title: 'Plan and price',
    seeing: 'A 90-day care subscription with two options and one plan price (two home visits included). "Reserve my place" is a fake-door test.',
    tests: 'D15 (riskiest): customers pay about AED 900 to 1,200 for a 90-day plan with two home visits (AED 450 to 600 a visit).',
    note: 'Each visitor sees one of three price variants at random (v1 450/600, v2 550/700, v3 650/800 AED), shown in tiny text on the card. Classmates are not the target customers, so results are a rehearsal, not market evidence.' },
  { id: 'S5', path: '/customer/slot', title: 'Choose a slot',
    seeing: 'A chat-style booking with the same colourist, as the pilot would run on WhatsApp. No real booking is made.',
    tests: 'Manual MVP booking works for the customer.' },
  { id: 'S6', path: '/customer/visit', title: 'Home visit day',
    seeing: 'What to prepare, and how the 3-hour visit runs.',
    tests: 'Customers accept a 3-hour home visit with a patch test 48 h before.' },
  { id: 'S7', path: '/customer/after', title: 'Before-and-after result',
    seeing: 'The before-and-after scan and the next visit, booked before the colourist leaves.',
    tests: 'A visible result drives the repeat-visit rate.',
    note: 'Use the demo control to switch the outcome to Flat or Worse: that opens S8 and raises an alert for the salon.' },
  { id: 'S8', path: '/customer/adjust', title: 'Plan adjustment',
    seeing: 'What happens when the result does not improve: the salon adjusts the treatment and the next scan is free.',
    tests: 'Customers stay when a result is flat, if the salon owns the fix.' },
];

export const otherScreens: ScreenMeta[] = [
  { id: 'Colourist', path: '/colourist', title: "Dana's day",
    seeing: "The colourist's view: today's home visits with first names only, the last scan, local notes and a step-by-step visit checklist.",
    tests: 'A salon colourist can run home visits with a simple checklist, inside the manual MVP.',
    note: "Maya's card follows the customer demo: plan, patch test and a flag if her result did not improve." },
  { id: 'Salon', path: '/salon', title: 'Partner salon dashboard',
    seeing: 'The salon owner invites consenting clients, checks which colourists hold a home-service permit, sets its revenue share and watches cannibalisation.',
    tests: 'Salons see PRO•GO as extra income, not as a rival for their chairs.',
    note: 'Untick a permit to see a colourist blocked from home visits: this is the Dubai permit risk. Set S7 to Flat or Worse to see the alert.' },
  { id: 'CEO', path: '/ceo', title: 'CEO scoreboard',
    seeing: 'The six board KPIs with their targets, and a calculator for margin per visit, the riskiest number.',
    tests: 'A visit at about AED 500 leaves a positive margin per visit after paying the salon, travel and products.',
    note: 'Targets only by default. "Show simulated demo data" fills the tiles with invented values under a SIMULATED watermark.' },
];

export const allScreens = [...customerScreens, ...otherScreens];
export const findScreen = (path: string) => allScreens.find((s) => s.path === path);
