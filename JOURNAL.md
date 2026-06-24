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

## 2026-06-16 — Added de Volkskrant + Trouw (flagged by Rodrigo Ochigame)

- Co-author Rodrigo Ochigame flagged two missed **leading Dutch dailies**:
  **de Volkskrant** ("Prominente wiskundigen waarschuwen voor gevaren van AI:
  'OpenAI is totaal niet open…'") and **Trouw** ("Wiskundigen waarschuwen voor
  AI in hun vak: wat is nog onze rol?"). Both added (`likely`; paywalled/blocked
  fetch, slugs + Dutch search snippets corroborate). Total **171 → 173**.
- Notable: these were missed **despite** a Dutch-press lens in the original
  sweep — confirming recall gaps occur *within* covered languages, not just for
  un-enumerated ones. The catalogue remains an explicit lower bound ("probably
  even more out there").

## 2026-06-16 — Neutralized: facts only, analysis removed

- Per request, the website and project are now **fact-only and neutral**. Removed
  all interpretive/opinion content (much of it derived from opinion pieces):
  - Landing page: deleted the **"Reception & analysis"** panel and the
    **Executive summary / Recurring themes / Notable voices / Reach** panel;
    replaced with a neutral **"About this tracker"** panel (what it is + counts +
    "lower bound, not exhaustive").
  - Vault: deleted the **Analysis note**; removed the synthesis sections from
    **Home**; removed the per-mention **"Significance"** (editorial `influence`)
    section. Neutralized the Yann LeCun People bio to facts only.
  - Data: removed the `analysis` and `synthesis` blocks and the per-mention
    `influence` field from `data/mentions.json`.
- **Kept (facts):** the full catalogue (outlet, type, author, date, country,
  language, URL, a factual summary of what each source says, and attributed
  quotes), the map, filters, counts, and the declaration's factual details.
  Opinion pieces remain **listed as mentions** (factual record that they exist);
  their opinions are no longer adopted as project analysis.
- This development journal and git history remain as a factual record of the work
  (including that analysis was added and then removed on request).

## 2026-06-16 — Round 3 deep search (forums / video / academic)

- Deep sweep (12 lenses + gap round, legit-only, anti-mirror, dedup vs the 173
  embedded URLs): 17 fresh candidates → **kept 9** legit/non-mirror, **dropped 2
  scraper mirrors**, **rejected 5** (incl. the April 2026 Economist piece and a
  Sept-2025 Leiden symposium video — both pre-/non-declaration; an arXiv essay; a
  CACM piece). Added **8** → total **173 → 181**.
- New entries: **FDLIST** (Bielefeld math dept Discourse forum), **John Baez**
  Mathstodon thread, **Scott Aaronson** (Shtetl-Optimized), **RT DE** (German),
  **Bilibili** video (Chinese), Marius Buliga & Dan Ma math blogs, ODSC "Last
  Week in AI" recap. New categories now populated: **forum** (10) and **video** (1).
- **Excluded:** a Reddit r/math thread whose specific URL could not be confirmed
  to exist (all Reddit endpoints/archives blocked, no corroborating search hit) —
  held out rather than risk a dead/wrong link.
- **Honest gap:** video/podcast yield was thin (1 video, 0 podcasts verifiable) —
  most candidates predate the declaration or don't explicitly mention it. Need
  specific URLs from collaborators to add the known video/podcast entries.
- All new entries carry only factual fields (no `influence`/analysis), per the
  neutrality rule.

## 2026-06-17 — Map dot accuracy fix

- A collaborator noted some dots (e.g. Edinburgh) sat far from the actual town.
- **Investigation:** bbox-checked all 75 distinct locations against their
  country and eyeballed every city/lat-lon. **All stored coordinates are
  correct** (Edinburgh = 55.9533,-3.1883, the true city centre). The drift was a
  rendering artifact: the map added up to **±0.55° (~60 km) random jitter** to
  separate overlapping dots, which threw coastal singletons into the sea.
- **Fix:** replaced random jitter with coordinate-grouping — **singletons are
  placed exactly** on their city; only genuinely co-located dots are fanned out
  on a **small ring (≤~13 km) centred on the true location**. No coordinate data
  was wrong, so none needed changing. (3 US-only Substacks with unknown city
  remain at the US centroid as an explicit country-level placeholder.)

## 2026-06-21 — Round 4: second deep search (+23 → 211)

- Fresh deep sweep (12 lenses + gap round; legit-only, anti-mirror; deduped vs
  the 188 embedded URLs; verifiers geo-located inline). 36 fresh candidates →
  **kept 23**, **dropped 5 scraper mirrors** (Mirage, Gizmodo Japan,
  McInformactions, Habr, Wetterauer Zeitung), **rejected 8** (the April-2026
  Economist again; pre-/non-declaration arXiv papers; the Lorentz workshop
  YouTube channel; the Backreaction blog text again; an El País piece that
  doesn't cite it; an Azim Premji faculty page). Total **188 → 211**.
- **Washington Post — correction of an earlier finding:** WaPo *did* publish on
  the declaration — "Math has helped define humanity…" (science, 14 June 2026).
  My earlier "no WaPo coverage (not a miss)" was true at the time but is now
  superseded; it's added.
- Other notable adds: a *Nature*-tier institutional spread — **Vrije
  Universiteit Amsterdam**, **TU/e CASA** (Portegies's own group), **McDermott
  Will & Emery** (law-firm IP/AI analysis), **Retraction Watch**, **ANSA** wire
  (Italy), **N+1** (Russia), **HuffPost España**, Greek press (Protagon,
  Unboxholics), **Menéame** (×2, Spain forum), more Tao/Baez **Mathstodon**
  threads, a 2nd Bilibili video, and structured index records (**OpenAlex**,
  **Wikidata**).
- Social author-geo normalized to match existing convention (Tao→Los Angeles,
  Baez→Edinburgh). All 211 entries geo-located; still neutral/facts-only.

## 2026-06-21 — Academy AI primer + Vision IA video (→ 213)

- **Academy for the Mathematical Sciences — "Mathematics in the age of AI" primer**
  (Leslie et al., DOI 10.5281/zenodo.20538963, 12 June 2026), provided by the
  user. Added as one entry (landing page + PDF + DOI are one work). **Caveat:**
  the Academy site is 403 and Wayback is unreachable, so I could not confirm the
  primer/landing page explicitly cite the Leiden Declaration; the Zenodo abstract
  doesn't, though the full PDF may. Included as a closely-related Academy
  publication at the user's request, `likely`, flagged for removal if it doesn't
  actually reference the declaration.
- **Vision IA (YouTube), "L'IA pensait avoir tué les maths…"** (French), declaration
  discussed ~half-way (t=801s). `likely`; title/channel confirmed via YouTube
  oembed. Videos now 4.
- **Bug fixed (dedup):** the merge `norm()` stripped URL query strings, so all
  `youtube.com/watch?v=...` URLs collapsed to `youtube.com/watch` and a 2nd
  YouTube video was wrongly flagged a duplicate. Re-added Vision IA with a
  video-ID check. (Stored data always kept full URLs, so no display collision.)
  NOTE for future sweeps: the deep-search workflows used the same norm, so they
  may have silently dropped new YouTube videos that collided with an existing
  watch URL — use a video-ID-aware norm next time.

### Notes for next time
- Re-run the research workflow periodically (signatory count and coverage keep
  growing); add new rows to `data/mentions.json` and run `python3
  scripts/generate.py`.
- `likely`-confidence items (notably NYT) are paywalled — re-check if direct
  access becomes available.
