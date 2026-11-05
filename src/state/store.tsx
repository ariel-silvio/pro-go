import { createContext, useContext, useEffect, useReducer, type Dispatch, type ReactNode } from 'react';
import { CONFIG } from '../config';
import { priceVariants, type PlanId, type Scenario, type VariantId } from '../data/mock';

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
}

export type Action =
  | { type: 'scanDone' }
  | { type: 'choosePlan'; plan: PlanId }
  | { type: 'reserve' }
  | { type: 'chooseSlot'; slotId: string }
  | { type: 'toggleCheck'; id: string }
  | { type: 'setScenario'; scenario: Scenario }
  | { type: 'bookNext' }
  | { type: 'renew' };

function randomVariant(): VariantId {
  return priceVariants[Math.floor(Math.random() * priceVariants.length)].id;
}

export function initialState(): DemoState {
  return {
    variantId: randomVariant(), plan: 'essential', scanDone: false, reserved: false, slotId: null,
    checklist: {}, scenario: 'improved', nextBooked: false, renewed: false, alerts: [],
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
