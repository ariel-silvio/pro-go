import type { ScreenMeta } from '../screens/registry';
import { resetDemo } from '../state/store';
import { useTour } from '../tour/Tour';

const qrSrc = `${import.meta.env.BASE_URL}qr.png`;
const qrVideo = `${import.meta.env.BASE_URL}qr-video.png`;
const VIDEO_URL = 'https://youtu.be/T2k37jMMXo4';
const smallBtn = 't-label min-h-11 border border-ink px-3 hover:bg-paper';

export function SidePanel({ screen }: { screen?: ScreenMeta }) {
  const tour = useTour();
  return (
    <aside className="w-80 shrink-0 self-center" aria-label="What you are seeing">
      <p className="t-label text-gold-text">What you are seeing</p>
      {screen ? (
        <>
          <h2 className="t-headline mt-2">{screen.id}. {screen.title}</h2>
          <span className="gold-rule mt-3" aria-hidden />
          <p className="mt-4 text-sm leading-relaxed">{screen.seeing}</p>
          <p className="t-label mt-6 text-muted">Assumption it tests</p>
          <p className="mt-1 text-sm leading-relaxed">{screen.tests}</p>
          {screen.note && <p className="t-card-body mt-4 border-t border-hairline pt-3 text-muted">{screen.note}</p>}
        </>
      ) : (
        <p className="mt-2 text-sm">Pick a screen.</p>
      )}
      <p className="t-card-body mt-8 border border-hairline bg-source-note p-4 text-ink">
        Honesty note: classmates are not Dubai women who colour their hair. Their answers are a rehearsal and a usability check, not evidence of demand.
      </p>
      <div className="mt-6 flex flex-wrap gap-2">
        <button type="button" className={smallBtn} onClick={() => tour.start(false)}>Guided tour</button>
        <button type="button" className={smallBtn} onClick={() => tour.start(true)}>Play demo</button>
        <button type="button" className={smallBtn} onClick={resetDemo}>Reset</button>
      </div>
      <div className="mt-6 flex items-center gap-4">
        <img src={qrSrc} alt="QR code that opens this prototype on a phone" width={96} height={96} className="border border-hairline bg-paper" />
        <p className="t-card-body text-muted">Scan to open on your phone.<br /><span className="text-ink">ariel-silvio.github.io/pro-go</span></p>
      </div>
      <div className="mt-6 border-t border-hairline pt-5">
        <p className="t-label text-gold-text">Watch the M4 video</p>
        <div className="mt-3 flex items-center gap-4">
          <a href={VIDEO_URL} target="_blank" rel="noopener noreferrer" aria-label="Open the M4 video on YouTube">
            <img src={qrVideo} alt="QR code that opens the Team D M4 video, 12 weeks with Layla" width={96} height={96} className="border border-hairline" />
          </a>
          <p className="t-card-body text-muted">
            <span className="font-serif text-base text-ink">12 weeks with Layla</span><br />
            Team D, 8 minutes.<br />
            <a href={VIDEO_URL} target="_blank" rel="noopener noreferrer" className="text-ink underline underline-offset-2">youtu.be/T2k37jMMXo4</a>
          </p>
        </div>
      </div>
    </aside>
  );
}
