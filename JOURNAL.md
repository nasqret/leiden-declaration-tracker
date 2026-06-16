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

### Notes for next time
- Re-run the research workflow periodically (signatory count and coverage keep
  growing); add new rows to `data/mentions.json` and run `python3
  scripts/generate.py`.
- `likely`-confidence items (notably NYT) are paywalled — re-check if direct
  access becomes available.
