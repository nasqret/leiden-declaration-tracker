# Journal — Leiden Declaration media-coverage tracker

## 2026-06-16 — Initial build

### Brief
Track every internet mention of the **Leiden Declaration on Artificial
Intelligence and Mathematics** (<https://leidendeclaration.ai>), including the
links curated on the `/news` page — newspapers, magazines, blogs, and notable
social-media posts. Package as: memory file, journal, plan, Obsidian vault, local
git repo, private GitHub repo, and a landing page.

### What the subject is
A declaration published **2 June 2026**, growing out of a September 2025 Lorentz
Center workshop at Leiden University. Working group led by **Jim Portegies**
(TU Eindhoven). **Endorsed by the International Mathematical Union**; **2,500+
signatories** including Terence Tao, Peter Scholze, Robbert Dijkgraaf, Kevin
Buzzard, Jeremy Avigad. It warns that AI threatens the core values of
mathematics (proof, verification, attribution, peer review, human oversight).

### Method
1. **Scouted** the site and `/news` page → 12 seed mentions (NYT, Scientific
   American, Science, NRC, Leiden University, LMS, INI, Edinburgh, TU/e, IMU,
   Academy for the Mathematical Sciences, ICM 2026).
2. Ran a **background research workflow** (`leiden-declaration-mentions`):
   - **16-lens discovery fan-out** (US/UK/world press, science/tech magazines,
     Dutch/German/Romance/Asian press, AI newsletters, forums, X/Twitter,
     Mastodon/Bluesky, LinkedIn, mathematicians' blogs, societies, academic
     outlets, podcasts/video, broad catch-all).
   - **Adversarial verification** of every candidate (fetch page, confirm it
     references *this* 2026 declaration, guard against the unrelated 2015 "Leiden
     Manifesto for research metrics").
   - **Gap analysis** → 16 follow-up queries → second discovery + verify round.
   - **Synthesis** of the coverage landscape.
   - Stats: **174 agents, ~2.9M tokens, ~36 min.** One discovery lens
     (podcasts/video) failed on a socket error; the gap round recovered video
     angles. Result: **138 unique candidates → 131 verified, 7 rejected.**

### Verification results
- **131 verified mentions** across **127 outlets** and **~15 languages**
  (English, Dutch, German, French, Spanish, Italian, Portuguese, Chinese,
  Japanese, Korean, Russian, Turkish, Arabic).
- Confidence: 108 `confirmed`, 23 `likely` (paywalled/JS-rendered pages
  corroborated via secondary sources, e.g. NYT).
- By type: 40 newspaper, 33 blog, 23 institutional, 8 magazine, 8 social,
  8 forum, 5 newsletter, 2 wire, 2 other, 1 academic, 1 event.
- **7 false positives rejected** by the adversarial pass: a paywalled Der
  Standard piece that didn't mention it, a misattributed Mastodon mirror, a 403
  NEMO Kennislink index page, a CMU measure-theory PDF, two pre-declaration
  arXiv essays, and a Sept-2025 Kevin Buzzard YouTube talk (predates launch).

### Highlights of the coverage
- **Tier-one:** NYT (Siobhan Roberts), Scientific American (Leila Sloman),
  Science (AAAS), Spektrum der Wissenschaft, Futurism.
- **Wire/syndication:** AFP "don't believe the hype" wire republished across
  25+ countries (Manila Times, The Star, Geo News, Jamaica Observer,
  myRepublica, Canadian Affairs, Epoch Times Deutsch…).
- **Institutions:** IMU endorsement (Christoph Sorger), ICM 2026 panel, national
  societies (LMS, UMI, MSJ, KMS), universities (Oxford, Columbia, Northwestern,
  Edinburgh, Leiden, TU/e).
- **Math blogs/Substacks:** Michael Harris (Silicon Reckoner), Jordan Ellenberg
  (Quomodocumque), Peter Woit (Not Even Wrong), Gil Kalai, Jason Polak (critical).
- **Social:** Terence Tao announced it on Mathstodon; Steven Strogatz and Ananyo
  Bhattacharya amplified on X; several LinkedIn posts.

### Documentation produced
- `data/mentions.json` — single source of truth (subject + 131 mentions +
  synthesis + rejected list).
- `scripts/generate.py` — idempotent generator.
- `vault/` — Obsidian KB: Home MOC, Declaration note, 131 mention notes, master
  table, 127 outlet notes, 6 people notes.
- `landing/index.html` — filterable landing page (search + type/language filters).
- `PLAN.md`, `README.md`, this journal, and a Claude memory file.
- Local git repo → private GitHub repo.

## 2026-06-16 — Public deployment + GitHub Pages

- Switched the GitHub repo from private to **public**.
- Added `.github/workflows/pages.yml` — a GitHub Actions workflow that publishes
  the `landing/` folder to **GitHub Pages** (clean root URL, no file
  duplication; auto-redeploys on any push touching `landing/`).
- Enabled Pages with the "GitHub Actions" build source; set the repo homepage.
- **Live landing page:** <https://nasqret.github.io/leiden-declaration-tracker/>
  — verified HTTP 200 serving all 131 records.

## 2026-06-16 — Missed-mention fix (Gazeta Wyborcza, PL)

- User flagged a missed mention: **Gazeta Wyborcza** (major Polish daily).
  Diagnosing it surfaced *more* uncaptured Polish coverage (gry-online.pl,
  osp1.pl) → a **systematic recall gap**, not a one-off.
- **Root cause:** discovery-recall failure from **enumerated-language bias** (the
  16 lenses named ~12 languages; Polish + many others were never queried) plus a
  **US-locale search index** and the **translated brand name** ("deklaracja
  lejdejska"). Verification fragility on paywalled regional press is a secondary
  factor (Wyborcza blocks automated fetch). Full analysis + remediation in
  `FIXPLAN.md`.
- **Done now:** added the Wyborcza mention (`likely`; count 131 → 132),
  regenerated the vault + landing page, redeployed. Recorded a feedback memory so
  future research sweeps query non-enumerated languages natively.

## 2026-06-16 — Country map, multilingual re-sweep, commentary & corrections

- **Suggestions round 2 (collaborators):** country selector + interactive map; WaPo check; then John Horgan, Le Figaro, Yann LeCun's signature, AI-industry silence, more Substacks.
- **Washington Post:** verified as **not a miss** — no WaPo article exists (NYT is the only major US daily that covered it; Wikipedia's references confirm).
- **Multilingual re-sweep** (FIXPLAN Phase 1+2): 24 native-language lenses + structured sources → **+33 new mentions in 13 new languages** (Catalan, Croatian, Czech, Greek, Hebrew, Hungarian, Indonesian, Norwegian, Persian, Romanian, Serbian, Thai, Vietnamese). Note: the `args` dedup list didn't reach the workflow as an array, so dedup vs the existing set was done at merge time instead.
- **Country + map:** geo-enriched **all mentions** (country, city, lat/lon); added a country `<select>` and a Leaflet dot-map (CARTO dark tiles, graceful offline fallback) to the landing page, plus per-country vault notes and a Home "by country" section.
- **Supplementary commentary sweep:** +6 more (Le Figaro/Aurélie Jean, The Synthesis & How Math Saves the World Substacks, a 2nd Silicon Reckoner post, Clubic, RTS). **Total now 171 mentions, 27 languages, 44 countries.**
- **Corrections / findings (verified):**
  - **Yann LeCun did NOT sign.** The claim traces to an AI-generated search summary misreading the Italian MaddMaths line that calls LeCun "one of the great AI experts" — not a signatory. Official list (2,528) and Wikipedia confirm. Recorded in the Analysis note; not added as a signatory.
  - **AI-industry silence:** no public response from Hassabis/Altman/Amodei/OpenAI/DeepMind/Anthropic/Google/Meta; zero industry-affiliated signatories.
  - Captured commentator framings ("a job application, not a protest letter"; governance template; Harris's "recover the narrative"; Polak's "pathetic") in a generated **Analysis note** + landing "Reception & analysis" panel.
- **Unresolved:** could not locate a **John Horgan** post specifically about the declaration (checked his Cross-Check index + site search). Awaiting the URL from collaborators rather than guessing.

## 2026-06-16 — Correction: Yann LeCun DID sign

- A collaborator corrected my earlier (wrong) finding: **Yann LeCun signed** the
  declaration. Verified at <https://leidendeclaration.ai/signatories?q=Yann> —
  listed as *"Yann LeCun, verified email, New York University."* He published
  nothing about his endorsement.
- **Why I got it wrong:** the verification agent queried the signatories list with
  the wrong parameter (`?search=LeCun`, and only page 1) and treated the empty
  result as proof of absence — a false negative. The correct param is `?q=`.
  Lesson recorded in memory [[verifying-negative-claims]].
- **Fixes applied:** added Yann LeCun to notable signatories + a People note;
  corrected the vault Analysis note and landing "Reception & analysis" panel;
  nuanced the AI-industry finding — institutional silence (no lab/leader response)
  **alongside** one major industry figure (Meta's chief AI scientist) quietly
  signing under his NYU affiliation. Total mentions unchanged (171).

### Notes for next time
- Re-run the research workflow periodically (signatory count and coverage keep
  growing); add new rows to `data/mentions.json` and run `python3
  scripts/generate.py`.
- `likely`-confidence items (notably NYT) are paywalled — re-check if direct
  access becomes available.
