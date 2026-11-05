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
