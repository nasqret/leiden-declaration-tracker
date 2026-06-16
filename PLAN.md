# Plan — Leiden Declaration media-coverage tracker

**Goal:** Maintain a complete, verified catalog of every internet mention of the
**Leiden Declaration on Artificial Intelligence and Mathematics**
(<https://leidendeclaration.ai>), including the links curated on
<https://leidendeclaration.ai/news>, plus newspapers, magazines, blogs, and
notable social-media posts — and package that knowledge as a memory file, a
journal, this plan, an Obsidian vault, a local git repo, a private GitHub repo,
and a landing page.

## Subject (one line)
A June 2026 declaration, led by Jim Portegies (TU Eindhoven), endorsed by the
International Mathematical Union and signed by 2,500+ mathematicians (Tao,
Scholze, Dijkgraaf, Buzzard, Avigad…), warning that AI threatens the core values
of mathematics (proof, verification, attribution, peer review, human oversight).

## Approach

1. **Scout** the declaration site and `/news` page to seed the known mentions. ✅
2. **Discover** (fan-out) — parallel web searches across ~16 lenses: US/UK/world
   newspapers, science & tech magazines, Dutch/German/Romance/Asian press, AI
   newsletters, forums (HN/Reddit), X/Twitter, Mastodon/Bluesky, LinkedIn,
   mathematicians' blogs, societies, academic outlets, podcasts/video, and a
   broad catch-all.
3. **Verify** (adversarial) — fetch each candidate, confirm it references *this*
   2026 declaration (guarding against the unrelated 2015 "Leiden Manifesto"),
   and extract metadata (outlet, type, author, date, language, summary, quote,
   significance, confidence).
4. **Gap analysis** — a completeness critic proposes follow-up queries; run a
   second discovery + verification round on what was missed.
5. **Synthesize** — executive summary, recurring themes, notable voices, reach.
6. **Persist** everything to `data/mentions.json` (single source of truth).
7. **Generate** the Obsidian vault and landing page from that JSON
   (`scripts/generate.py`, idempotent / re-runnable).
8. **Document** — memory file, journal, README.
9. **Ship** — local git repo → private GitHub repo (`nasqret`).

## Deliverables & status
- [x] Verified mention catalog — **131 mentions, 127 outlets, ~15 languages** (7 false positives rejected)
- [x] `data/mentions.json` source of truth
- [x] Obsidian vault (`vault/`) — Home MOC, Declaration, 131 Mentions, master table, 127 Outlets, 6 People
- [x] Landing page (`landing/index.html`) — filterable
- [x] Memory file (Claude memory) + `MEMORY.md` index pointer
- [x] Journal (`JOURNAL.md`)
- [x] Plan (`PLAN.md`) — this file
- [x] Local git repository
- [x] ~~Private~~ **Public** GitHub repository — <https://github.com/nasqret/leiden-declaration-tracker>
- [x] Live landing page via GitHub Pages — <https://nasqret.github.io/leiden-declaration-tracker/>

## Round 3 — Deep search & expanded categories (in progress)
A **very deep** sweep for hard-to-locate citations in obscure places and
paywalled journals, plus broader context and new content categories.

- **Forums:** notable **Reddit** threads and **Zulip** (especially the Lean
  community Zulip used by mathematicians), plus Hacker News / Lobsters /
  MathOverflow / LessWrong / EA Forum / n-Category Café.
- **New categories — videos & podcasts:** YouTube videos, talks, panels (incl.
  ICM 2026) and podcast episodes that **explicitly mention** the declaration.
  Brief/passing mentions are acceptable and wanted.
- **Academic / paywalled:** Notices & Bulletin of the AMS, Nature/Science
  editorials, EMS Magazine, *Nieuw Archief voor Wiskunde*, etc., plus scholarly
  **citations** of the Zenodo DOI (Google Scholar / OpenAlex / Crossref / arXiv).
- **Policy & scholarly-communication:** Scholarly Kitchen, LSE Impact, Retraction
  Watch, THE, Inside Higher Ed; niche blogs; deep non-English coverage; Wikipedia
  references across all language editions.

**Quality bar (hard requirements):**
- **Legitimate sources only** — real outlets, named forums, real channels/shows,
  scholarly venues. No spam or SEO content farms.
- **Avoid automatic-duplication engines / scraper mirrors** and near-duplicate
  republications; keep the **original** source, drop machine-republished copies.
- **No duplication** — dedupe by URL against the existing catalogue (the existing
  set is embedded in the sweep script, not passed via `args`, per the FIXPLAN
  lesson) and flag/drop content that merely mirrors an already-catalogued piece.

The generator already supports `video`, `podcast`, `forum`, and `academic`
categories (vault grouping, country map, and landing filters pick them up
automatically).

## Maintenance
To refresh coverage later: re-run the research workflow (or add rows to
`data/mentions.json` by hand), then `python3 scripts/generate.py` to rebuild the
vault and landing page, and commit.
