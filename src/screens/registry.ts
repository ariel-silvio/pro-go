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
    seeing: 'A 90-day plan with two options and a price. "Reserve my place" is a fake-door test.',
    tests: 'D15 (riskiest): customers pay about AED 450 to 600 per home visit.',
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
  { id: 'Colourist', path: '/colourist', title: 'Colourist view', seeing: 'Coming in Phase 2.', tests: '—' },
  { id: 'Salon', path: '/salon', title: 'Salon view', seeing: 'Coming in Phase 2.', tests: '—' },
  { id: 'CEO', path: '/ceo', title: 'CEO scoreboard', seeing: 'Coming in Phase 2.', tests: '—' },
];

export const allScreens = [...customerScreens, ...otherScreens];
export const findScreen = (path: string) => allScreens.find((s) => s.path === path);
