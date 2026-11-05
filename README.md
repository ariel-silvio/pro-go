# PRO•GO Colour Plan — clickable prototype

Mobile-first, clickable prototype of a manual-MVP service concept for Team D (IE EMBA, Corporate Entrepreneurship). **Student project. Not affiliated with or endorsed by L'Oréal. Fictional characters and simulated data.**

- **Live:** https://ariel-silvio.github.io/pro-go/
- No login, no backend, no camera, no analytics, no cookies. Demo state lives in `localStorage` (`progo-demo-v1`).

## Run, build, deploy

```bash
npm install
npm run dev        # http://localhost:5173/pro-go/
npm run typecheck
npm run build      # writes dist/
```

Deploy: `.github/workflows/deploy.yml` typechecks, builds and runs the claims check on every push and PR; pushes to `main` deploy `dist/` to GitHub Pages (Settings → Pages → Source: GitHub Actions).

## Reset the demo

Menu (top right) → **Reset demo**. Clears `localStorage` and returns to S1.

## Routes

`#/customer/invite` (S1), `#/customer/scan` (S2), `#/customer/result` (S3), `#/customer/plan` (S4), `#/customer/slot` (S5), `#/customer/visit` (S6), `#/customer/after` (S7), `#/customer/adjust` (S8, only after Flat or Worse), `#/colourist`, `#/salon`, `#/ceo`.

## Connect the feedback form

1. Create the Google Form (3 questions: "Would you try this?", "What would you pay per home visit?", "What is confusing?", plus short-answer fields `variant`, `persona`, `plan`). Do not ask for names, emails or phone numbers.
2. In the form: ⋮ → **Get pre-filled link**, type `v1` / `customer` / `essential` in the three fields, copy the link.
3. In `src/config.ts`: set `FEEDBACK_FORM_URL` to the part before `?`, and set `FEEDBACK_FIELDS` to the three `entry.NNN` IDs from the link.

## Where to edit

| What | File |
|---|---|
| Feedback form URL, exchange rate, pilot communities | `src/config.ts` |
| Colours, radius, spacing (Team D Brand Kit v2.1) | `src/styles/tokens.css` |
| Screen titles and side-panel text | `src/screens/registry.ts` |
| Mock data, prices, slots, scan scores | `src/data/mock.ts` |

## Third-party licences

| Package | Licence |
|---|---|
| react, react-dom | MIT |
| react-router-dom | MIT |
| lucide-react | ISC |
| @fontsource/bodoni-moda, @fontsource/jost (fonts: SIL Open Font License 1.1) | MIT (package) / OFL-1.1 (font) |
| vite, @vitejs/plugin-react | MIT |
| tailwindcss, @tailwindcss/vite | MIT |
| typescript | Apache-2.0 |

See also `DECISIONS.md`, `AI_DISCLOSURE.md`, `FACTS.md`.
