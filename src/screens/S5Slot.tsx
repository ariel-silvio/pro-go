import { Headline, Label, ColouristCard, LinkButton, Note, Screen, Steps } from '../components/ui';
import { patchTestDay, slots } from '../data/mock';
import { useStore } from '../state/store';

export default function S5Slot() {
  const { state, dispatch } = useStore();
  const slot = slots.find((s) => s.id === state.slotId);
  return (
    <Screen>
      <Steps current={5} />
      <div>
        <Label>Book your first visit</Label>
        <Headline>Choose a time</Headline>
      </div>
      <ColouristCard subtitle="Same colourist every visit" />
      <fieldset>
        <legend className="t-label mb-2 text-muted">April 2027</legend>
        <div className="grid grid-cols-2 gap-2">
          {slots.map((s) => {
            const on = s.id === state.slotId;
            return (
              <button key={s.id} type="button" aria-pressed={on}
                onClick={() => dispatch({ type: 'chooseSlot', slotId: s.id })}
                className={`min-h-14 border px-3 py-2 text-left ${on ? 'border-ink bg-ink text-paper' : 'border-hairline bg-paper hover:border-ink'}`}>
                <span className="t-card-title block">{s.label}</span>
                <span className="t-card-body block">{s.time}</span>
              </button>
            );
          })}
        </div>
      </fieldset>

      {slot && (
        <div className="bg-ivory p-4" aria-live="polite">
          <p className="t-source mb-2 text-center text-muted">Message from Salon Aurora (simulated chat)</p>
          <div className="ml-auto max-w-[85%] border border-hairline bg-paper px-3 py-2">
            <p className="text-sm leading-relaxed">
              Dana will visit you on {slot.label}, {slot.time}. Please do a patch test 48 h before ({patchTestDay(slot)}).
            </p>
            <p className="t-source mt-1 text-right text-muted">Salon Aurora</p>
          </div>
        </div>
      )}
      <Note>No real booking is made. In the pilot, booking runs on chat with the salon.</Note>
      <div className="mt-auto">
        {slot ? <LinkButton to="/customer/visit">Continue to visit day</LinkButton>
          : <p className="t-card-body text-center text-muted">Pick a time to continue.</p>}
      </div>
    </Screen>
  );
}
