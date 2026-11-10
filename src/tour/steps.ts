import type { Dispatch } from 'react';
import type { Action } from '../state/store';

// The 3-minute click path (handoff §16). Seconds are for the auto-play (?demo=1); total 180 s.
export interface TourStep {
  path: string;
  caption: string;
  seconds: number;
  target?: string;                      // data-tour id to highlight
  enter?: (d: Dispatch<Action>) => void; // set demo state when the step starts
  run?: (d: Dispatch<Action>) => () => void; // something that plays during the step (auto-play only)
}

export const tourSteps: TourStep[] = [
  { path: '/customer/invite', seconds: 10, target: 'invite',
    caption: "Layla's own salon invites her. Her colourist, Dana, will come to her home." },
  { path: '/customer/scan', seconds: 8, target: 'scan',
    caption: 'A free hair scan. Simulated: no camera, three illustrated steps.' },
  { path: '/customer/result', seconds: 17, target: 'index',
    caption: 'Hair Health Index 58 out of 100, with four sub-scores and a rule-based note. Not a medical measurement.' },
  { path: '/customer/plan', seconds: 25, target: 'plans',
    caption: 'One price for a 90-day plan with two home visits. Visitors see one of three price variants. "Reserve my place" is a fake door: no payment.' },
  { path: '/customer/slot', seconds: 15, target: 'chat',
    enter: (d) => d({ type: 'chooseSlot', slotId: 's2' }),
    caption: 'She books the same colourist. The salon confirms by chat, with a patch-test reminder 48 h before.' },
  { path: '/customer/visit', seconds: 15, target: 'patch',
    enter: (d) => d({ type: 'setCheck', id: 'patch', value: true }),
    caption: 'Visit day: patch test done, space ready. Scan, colour, treatment, re-scan, in about 3 hours.' },
  { path: '/customer/after', seconds: 20, target: 'before-after',
    enter: (d) => d({ type: 'setScenario', scenario: 'improved' }),
    caption: 'Before and after: 58 to 66. The next visit is booked before Dana leaves.' },
  { path: '/customer/adjust', seconds: 20, target: 'adjust',
    enter: (d) => d({ type: 'setScenario', scenario: 'flat' }),
    caption: 'What if the result is flat? The salon adjusts the treatment and the next scan is free.' },
  { path: '/salon', seconds: 25, target: 'permits',
    caption: 'The salon owner sees the alert, invites only clients who agreed, and can only assign colourists with a home-service permit.' },
  { path: '/ceo', seconds: 25, target: 'calc',
    enter: (d) => d({ type: 'resetCalc' }),
    run: (d) => {
      // After 6 s, lower the price from AED 500 to 360 so the margin crosses break-even (AED 375).
      let price = 500;
      let iv: ReturnType<typeof setInterval> | undefined;
      const t = setTimeout(() => {
        iv = setInterval(() => {
          price -= 10;
          d({ type: 'setCalc', key: 'price', value: price });
          if (price <= 360 && iv) clearInterval(iv);
        }, 700);
      }, 6000);
      return () => { clearTimeout(t); if (iv) clearInterval(iv); };
    },
    caption: 'The CEO view: targets for the Q4 2027 review, and the margin per visit. Below about AED 375 a visit loses money.' },
];
