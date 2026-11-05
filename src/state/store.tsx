import { createContext, useContext, useEffect, useReducer, type Dispatch, type ReactNode } from 'react';
import { CONFIG } from '../config';
import { calcDefaults, colourists, priceVariants, type PlanId, type Scenario, type VariantId } from '../data/mock';

export interface Alert { id: string; customer: string; scenario: Scenario; text: string; }

export interface DemoState {
  variantId: VariantId;
  plan: PlanId;
  scanDone: boolean;
  reserved: boolean;
  slotId: string | null;
  checklist: Record<string, boolean>;
  scenario: Scenario;
  nextBooked: boolean;
  renewed: boolean;
  alerts: Alert[];
  // Phase 2
  notes: Record<string, string>;
  stepsDone: Record<string, number>;
  invited: string[];
  permits: Record<string, boolean>;
  salonShare: number;
  showSim: boolean;
  calc: typeof calcDefaults;
}

export type Action =
  | { type: 'scanDone' }
  | { type: 'choosePlan'; plan: PlanId }
  | { type: 'reserve' }
  | { type: 'chooseSlot'; slotId: string }
  | { type: 'toggleCheck'; id: string }
  | { type: 'setScenario'; scenario: Scenario }
  | { type: 'bookNext' }
  | { type: 'renew' }
  | { type: 'setNote'; id: string; text: string }
  | { type: 'stepDone'; id: string; step: number }
  | { type: 'invite'; id: string }
  | { type: 'togglePermit'; id: string }
  | { type: 'setShare'; value: number }
  | { type: 'toggleSim' }
  | { type: 'setCalc'; key: keyof typeof calcDefaults; value: number }
  | { type: 'resetCalc' };

function randomVariant(): VariantId {
  return priceVariants[Math.floor(Math.random() * priceVariants.length)].id;
}

export function initialState(): DemoState {
  return {
    variantId: randomVariant(), plan: 'essential', scanDone: false, reserved: false, slotId: null,
    checklist: {}, scenario: 'improved', nextBooked: false, renewed: false, alerts: [],
    notes: {}, stepsDone: {}, invited: [],
    permits: Object.fromEntries(colourists.map((c) => [c.id, c.permitDefault])),
    salonShare: CONFIG.SALON_SHARE_DEFAULT, showSim: false, calc: { ...calcDefaults },
  };
}

function withAlert(state: DemoState, scenario: Scenario): Alert[] {
  const others = state.alerts.filter((a) => a.customer !== 'Maya');
  if (scenario === 'improved') return others;
  return [...others, { id: `maya-${scenario}`, customer: 'Maya', scenario, text: 'Result did not improve: Maya' }];
}

function reducer(state: DemoState, a: Action): DemoState {
  switch (a.type) {
    case 'scanDone': return { ...state, scanDone: true };
    case 'choosePlan': return { ...state, plan: a.plan };
    case 'reserve': return { ...state, reserved: true };
    case 'chooseSlot': return { ...state, slotId: a.slotId };
    case 'toggleCheck': return { ...state, checklist: { ...state.checklist, [a.id]: !state.checklist[a.id] } };
    case 'setScenario': return { ...state, scenario: a.scenario, alerts: withAlert(state, a.scenario) };
    case 'bookNext': return { ...state, nextBooked: true };
    case 'renew': return { ...state, renewed: true };
    case 'setNote': return { ...state, notes: { ...state.notes, [a.id]: a.text } };
    case 'stepDone': return { ...state, stepsDone: { ...state.stepsDone, [a.id]: a.step } };
    case 'invite': return state.invited.includes(a.id) ? state : { ...state, invited: [...state.invited, a.id] };
    case 'togglePermit': return { ...state, permits: { ...state.permits, [a.id]: !state.permits[a.id] } };
    case 'setShare': return { ...state, salonShare: a.value };
    case 'toggleSim': return { ...state, showSim: !state.showSim };
    case 'setCalc': return { ...state, calc: { ...state.calc, [a.key]: a.value } };
    case 'resetCalc': return { ...state, calc: { ...calcDefaults } };
  }
}

function load(): DemoState {
  try {
    const raw = localStorage.getItem(CONFIG.STORAGE_KEY);
    if (raw) return { ...initialState(), ...JSON.parse(raw) };
  } catch { /* storage blocked or bad JSON: start clean */ }
  return initialState();
}

const Ctx = createContext<{ state: DemoState; dispatch: Dispatch<Action> } | null>(null);

export function StoreProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(reducer, undefined, load);
  useEffect(() => {
    try { localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(state)); } catch { /* ignore */ }
  }, [state]);
  return <Ctx.Provider value={{ state, dispatch }}>{children}</Ctx.Provider>;
}

export function useStore() {
  const c = useContext(Ctx);
  if (!c) throw new Error('useStore outside StoreProvider');
  return c;
}

export function resetDemo() {
  try { localStorage.removeItem(CONFIG.STORAGE_KEY); } catch { /* ignore */ }
  window.location.hash = '#/customer/invite';
  window.location.reload();
}
