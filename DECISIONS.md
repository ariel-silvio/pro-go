# Decisions log (prototype)

Defaults picked where the handoff was ambiguous or not possible in this environment. Locked baseline (handoff section 1) unchanged.

## Phase 0 — Scaffold (5 Nov 2026)

**Built:** Vite 6 + React 18 + TS + Tailwind 4, HashRouter, phone frame (390 x 844 from 1024 px up) with "What you are seeing" side panel, sticky "Prototype, simulated data" banner, disclaimer footer, feedback button ("Form link coming soon" until the URL is set), Reset demo menu, self-hosted Bodoni Moda + Jost, empty S1–S7 plus placeholder Colourist/Salon/CEO routes, CI build workflow.
**Skipped:** branch-per-phase PRs for Phase 0 (P0-3). Lighthouse not run yet (no content to measure).
**Check:** open https://ariel-silvio.github.io/pro-go/ on a phone.

| # | Decision | Why |
|---|---|---|
| P0-1 | Repo `ariel-silvio/pro-go` (created by Ariel) instead of the suggested `progo-colour-plan-prototype`. | Ariel's choice. A first draft was scaffolded in `ariel-silvio/loreal` before this repo existed; that branch is not merged and can be deleted. |
| P0-2 | Deploy with GitHub Actions (`actions/deploy-pages`) from `main`, Vite `base: '/pro-go/'`. | As in the handoff §11. |
| P0-3 | Phase 0 pushed straight to `main` as the repo's first commit (an empty repo has no branch to open a PR against). From Phase 1: branch per phase plus PR. | Handoff §13. |
| P0-4 | Vite 6 / Tailwind 4 / React Router 6 pinned to exact versions. | Small, stable, React 18 compatible. |
| P0-5 | ~~`--gold-text: #7A5F2E`~~ superseded by P0-7. | |
| P0-6 | Short URL for the forum: `ariel-silvio.github.io/pro-go/` (30 chars). | Fits the 1000-character forum limit. |
| P0-7 | Team D Brand Kit v2.1 applied (claude.ai/artifact/6ceiBuZuAa5FN2s9BNm43U); it overrides the handoff's placeholder tokens (handoff §9). Colours, Bodoni Moda 500 / Jost 400–600, kit type styles (`t-label`, `t-headline`, …), square corners, no shadows, hairline borders, gold rule under headlines, `source-note` fill for the honesty note. | Ariel's instruction; handoff §9 says the kit wins. |
| P0-8 | Light theme only. Kit dark values not wired yet. | Handoff: dark mode "only if time allows". Values are in the kit when needed. |
| P0-9 | Kit items **not** used in the prototype: the "L'ORÉAL GROUPE · TEAM D" slate label and the L'Oréal logo. | Handoff §8 and §12 forbid L'Oréal marks inside the UI; the prototype is a customer-facing mock. Kit is for board/video. |
| P0-10 | Avatars stay round (`radius-pill`); the phone bezel stays rounded. | Kit allows pill for photo frames; the bezel is device chrome, not UI. |
| P0-11 | `--warn` amber added (not in kit) for "LOW confidence" chips. | Kit has positive/negative only; a third state is needed for assumption chips. Always paired with text. |

## Phase 1 — Customer flow (5 Nov 2026)

**Built:** S1 to S8 working end to end on mock data (`src/data/mock.ts`), state in React context + `useReducer` saved to localStorage (`progo-demo-v1`), random price variant per visitor (v1/v2/v3, kept until Reset), rule-based AI note, simulated 3-step scan with a 1.5 s analysis, chat-style booking, visit checklist and 3-hour timeline, before-and-after with an Improved/Flat/Worse demo control, S8 plan adjustment, salon alert stored for Phase 2.
**Skipped:** S9 account summary (Phase 3), guided tour, `?demo=1` auto-play, screenshots in `docs/screens/` (Phase 4).
**Check:** gates 1–9 pass locally (typecheck, build, no console errors at 390 and 1280 px, Lighthouse mobile Performance 97–99 and Accessibility 100 on S1/S3/S4/S6/S7, banner and footer on every screen, claims words absent, Flat/Worse reach S8 and create the alert, Reset returns to a clean S1, deep links load). Please play it through on a real iPhone and Android phone.

| # | Decision | Why |
|---|---|---|
| P1-1 | First visit on **Wed 14 Apr 2027**, not "Tue 14 Apr". | 14 Apr 2027 is a Wednesday. Kept 2027 because the pilot starts Q2 2027 and the first scan is dated 2027-04-14. Second visit Wed 9 Jun 2027 (day 56). Patch test Mon 12 Apr (48 h before). |
| P1-2 | The booking screen says "Message from Salon Aurora (simulated chat)", not "WhatsApp". | Handoff §12: no real brand names inside the UI. The side panel explains it is how the pilot would run on WhatsApp. |
| P1-3 | "Reserve my place" opens the form (when its URL is set) **and** moves on to S5. | Keeps the demo flowing. Without a form URL it only moves on. |
| P1-4 | Feedback prefill uses `CONFIG.FEEDBACK_FIELDS` to map `variant`, `persona`, `plan` to Google Form `entry.NNN` IDs. | Google Forms ignores `?variant=`; it only prefills `entry.` IDs. Ariel pastes them in once the form exists. |
| P1-5 | Plan cards list the colour-care kit as included in the per-visit price. | Handoff says the kit ships between visits but gives no separate price. Team D assumption. |
| P1-6 | Visit timeline: set-up and scan 20 min, colour 100, treatment 45, re-scan and next booking 15 (= 3 h). | Handoff asks for a 3-hour bar with these four steps; split is illustrative, labelled "Team D assumption". |
| P1-7 | Extra AI-note rules for strength below 65 and shine below 60, beside the handoff's moisture rule. | Makes the note react to the scan; all wording avoids "repairs/treats". |
| P1-8 | Without a patch test the visit checklist warns "No patch test, no colour". | Puts the safety rule in front of the customer; demo still continues. |
| P1-9 | Fictional names checked on 5 Nov 2026 with a web search: no Dubai business called "Salon Aurora", "Studio Marjan" or "Atelier Noor" found. Near misses: "Aurora by Tolou" (Bukadra), "Marjan Ladies Salon" (Al Muraqqabat). | Handoff §3 / §17. Names kept; Ariel to confirm. |

## Video work: plan price as a subscription (5 Nov 2026)

| # | Decision | Why |
|---|---|---|
| V-1 | The plan screen (S4) shows the **90-day plan price** as the headline ("AED 900 per 90-day plan", "Subscription, renews every 90 days"), with the per-visit amount in the small print. Before, "per visit" was the headline. | M1 ("care subscriptions"), M2 (active care subscribers) and M3 D7 ("a measured plan, not single bookings"). Per-visit numbers stay as internal unit economics (M2 KPI: margin per visit). Side-panel test note updated to "AED 900 to 1,200 for a 90-day plan". Prices and variants unchanged. |

## Phase 2 — Colourist, salon and CEO views (5 Nov 2026)

**Built:** persona switcher (Customer, Colourist, Salon, CEO) under the banner; Colourist view (Dana's three visits, last scan, local notes, 5-step visit checklist, Maya's patch-test and "did not improve" flags from the customer demo); Salon view (alerts, 12 fictional clients with consent, simulated invite, colourist roster with home-service permit checkbox that blocks assignment, salon share slider, income-uplift target, cannibalisation monitor); CEO scoreboard (six KPIs with targets and "Team D proposal" tags, optional simulated values under a SIMULATED watermark, margin per visit calculator, "Where the first EUR 3m goes" table).
**Skipped:** nothing from §5 Phase 2. Guided tour, auto-play, PWA, QR and S9 stay in Phase 3.
**Check:** 30 automated checks pass at 390 and 1280 px (alert after Flat, consent rule, permit block, checklist, calculator defaults 375 / +125 / 25%, price 370 turns negative, simulated toggle off by default, EUR 3m total 3,000, Reset clears all Phase 2 state); customer flow still passes; Lighthouse mobile Performance 98–99, Accessibility 100 on all three new views.

| # | Decision | Why |
|---|---|---|
| P2-1 | "Q4 2027 **review**" and "2028 review" in the UI, not "gate". | Brand kit and M3 board say review, never gate (see `video/consistency-m2-m3-m4.md`, item G). Handoff wording was "gate". |
| P2-2 | Salon share (35%, editable) and the calculator's "pay to partner salon" (AED 230) are **separate inputs and do not match**: 35% of AED 500 is AED 175, not 230. | Both defaults come from the handoff. Kept both and did not link them, so neither changes silently. **Team to decide** whether AED 230 = salon share + colourist time, or the share should be about 46%. |
| P2-3 | Calculator margin = price − (salon pay + travel + products). Visits per day changes only "margin per colourist day". | The handoff lists visits per day as an input but gives no formula that uses it per visit. |
| P2-4 | All three colourists (Dana, Rana, Lina) sit in Salon Aurora's roster; Lina's permit starts unchecked. | The roster is the salon owner's view; an unchecked colourist shows the permit risk from the first click. |
| P2-5 | Simulated KPI values (212 subscribers, 43% repeat, AED +125, 58%, 4%, +3%) are invented, hidden by default and watermarked. AED +125 matches the calculator defaults. | Handoff: "Do not show invented values by default." |
| P2-6 | Appendix B line "minimum-income guarantee" shown as "minimum-income floor". | Gate 5 bans "guarantee" in user-facing text; same meaning. |
| P2-7 | Appendix B "Manual-MVP tools (WhatsApp, …)" shown as "chat booking". | No real brand names in the UI (handoff §12). |
| P2-8 | Customer tab returns to the last customer screen, not S1. | Keeps the 3-minute click path smooth when switching back and forth. |
