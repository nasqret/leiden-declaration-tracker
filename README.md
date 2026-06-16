# Leiden Declaration — Media Coverage Tracker

**🌐 Live landing page: <https://nasqret.github.io/leiden-declaration-tracker/>**

A knowledge base tracking **every traced mention across the internet** of the
[**Leiden Declaration on Artificial Intelligence and Mathematics**](https://leidendeclaration.ai) —
newspapers, magazines, blogs, institutional announcements, and notable
social-media posts — including the links curated on
[leidendeclaration.ai/news](https://leidendeclaration.ai/news).

> The Leiden Declaration (published 2 June 2026, led by Jim Portegies of TU
> Eindhoven, endorsed by the International Mathematical Union and signed by
> 2,500+ mathematicians including Terence Tao, Peter Scholze, Robbert Dijkgraaf
> and Kevin Buzzard) warns that AI threatens the core values of mathematics —
> proof, verification, attribution, peer review and human oversight.

## Repository layout

```
data/mentions.json     Single source of truth: subject + verified mentions + synthesis
scripts/generate.py    Builds the vault + landing page from mentions.json (idempotent)
vault/                 Obsidian vault (the knowledge base)
  Home.md              Map of Content — the coverage map
  Declaration/         The declaration overview note
  Mentions/            One note per mention + a master table (_All mentions.md)
  Outlets/             One note per outlet, aggregating its mentions
  People/              Key figures, backlinked to their coverage
landing/index.html     Self-contained, filterable landing page
PLAN.md                Plan & status
JOURNAL.md             Chronological work log
```

## Usage

Open `vault/` as an Obsidian vault (Open folder as vault) and start at **Home**.
Open `landing/index.html` in any browser for the filterable public view.

### Regenerate after editing data

```bash
python3 scripts/generate.py
```

Edit or extend `data/mentions.json` (add rows to `mentions`), then regenerate.
The `vault/Mentions/`, `vault/Outlets/` notes and `landing/index.html` are
derived artifacts and are rebuilt every run.

## Methodology

Mentions were discovered with a multi-lens web-search fan-out (general press,
science/tech media, multiple languages, AI newsletters, forums, social media,
mathematicians' blogs, societies, academic outlets, podcasts/video) and then
**adversarially verified** — each page was fetched and confirmed to reference
*this* 2026 declaration, guarding against the unrelated 2015 "Leiden Manifesto
for research metrics." Each entry carries a `confidence` value
(`confirmed` / `likely` / `unverified`).
