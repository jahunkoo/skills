# distill holdout answer key — apps/web/AGENTS.md

Fixture: the `storefront` monorepo (`files/web-agents.mbox`, 3 commits). The target is `apps/web/AGENTS.md`. The root `AGENTS.md` holds the repo-wide rules and must not change.

## Residue (should be stripped)

| ID | Type | Location in the original | Correct handling |
| --- | --- | --- | --- |
| R1 | History | §3 "We used to fetch data with SWR inside each component, but after the 2026-03 migration …" | Delete the backstory; keep only the conclusion "every request goes through `src/api/client.ts`" |
| R2 | Rebuttal | §2 "The old onboarding guide said to put page components under `pages/`, but in fact …" | Delete the rebuttal; state "routes live in `src/app/`" as a plain sentence |
| R3 | Meta note | End of §4 "> TODO: add before/after screenshots for the styling rules above." | Delete. It asks for examples; it does not question whether the styling rules apply |
| R4 | Dead reference | §2 "Follow the naming rules in `docs/web-conventions.md`." — the file does not exist (neither under `apps/web/docs/` nor under `docs/`) | Delete after confirming |
| R5 | Stacked duplicate (across layers) | §1 "Install packages with pnpm only; npm and yarn are not allowed in this app." ↔ root `AGENTS.md` "Use pnpm for every install and script. Do not use npm or yarn — a second lockfile breaks the CI cache." | The root file is the single source (repo-wide rule, carries the WHY). Replace the app sentence with a pointer to the root file (the skill: keep one source, link to it from the rest). Restating the rule, or dropping it with no pointer, is wrong. Do not edit the root file. Judged by h1.ssot and h2.ssot, not by recall |
| R6 | Superseded ADR | §3 "Client state uses Redux Toolkit (ADR-0012)." — ADR-0012's status is superseded (replaced by ADR-0015 on 2026-06-10) | Delete |
| R8 | Excess narrative | §5 "Our unit tests started as a hackathon project in 2025. The team found … today it runs in under a minute on a laptop. So, run `pnpm test` before every commit." | Put the instruction first and keep it: "Run `pnpm test` before every commit." Delete the background (a short reason such as "the suite runs in under a minute" may stay) |
| R7 | Contradiction | §5 "Run `pnpm test:e2e` locally before every push." ↔ §6 "Do not run e2e tests locally; CI runs them on every PR." | **Do not delete; ask the user** |

## Live rules (should be kept — proposing to delete them, or deleting them, is wrong)

| ID | Type | Original |
| --- | --- | --- |
| K1 | WHY | §3 "Do not call `fetch` directly — the API client attaches the auth header and refreshes an expired token, and a direct call logs the user out when the token expires." (the WHY clause must remain too) |
| K2 | Near-miss warning | §1 "After the 2026-08 incident, we learned that a secret with the `NEXT_PUBLIC_` prefix is inlined into the client bundle, which is how an API key leaked. Keep secrets in server-only env vars without that prefix." (It came in with the most recent commit, 2026-08-21. Trimming only the "After the … incident, we learned" backstory wording is allowed; deleting the rule or its reason is wrong) |
| K3 | Rationale link | §3 "Keep shared UI state in the Zustand stores under `src/stores/` (rationale: ADR-0015)." — ADR-0015 is accepted; keep the link (it came in with the second commit, 2026-06-10) |
| K4 | Rejected alternative | §4 "Do not add a CSS-in-JS library — ADR-0009 rejected it because of its runtime cost on low-end phones." |
| K5 | Conditional exception | §4 "Exception: pages under `src/app/(marketing)/` may use plain `<img>` tags, because the marketing CDN resizes those images itself." |

## Other behavioral instructions (should remain)

- Copy `.env.example` to `.env.local` before running the dev server · name component files in PascalCase · use `next/image` for every image (with the K5 exception) · open PRs against `main` with one approval from the web team (h2.other_rules)
- Run `pnpm test` before every commit (the instruction inside R8; h2.conclusions)

## Notes for graders

- Two items have no counterpart in the development fixture: R5 needs the upper layer (the root `AGENTS.md`) to judge, and R8 is an excess-narrative residue.
- Recall is counted over R1–R4, R6 and R8 (six items, at least five). R5 is judged separately by h1.ssot and h2.ssot.
- R6 and K3 point at two ADRs about the same topic; the ADR statuses (superseded / accepted) decide which is current. This is not a contradiction for the user to decide.
- The R3 note only asks for screenshots. It does not make K5 or the `next/image` rule uncertain; both are live rules.
- K4 says "ADR-0009 rejected it": ADR-0009 is accepted, and what it rejected is the CSS-in-JS alternative. Reading "rejected" as "the ADR is dead" is a misreading.
