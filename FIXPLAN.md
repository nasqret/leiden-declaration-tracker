# Fixing plan — coverage gaps in the mention sweep

**Trigger:** A user flagged a missed mention —
[Gazeta Wyborcza (PL)](https://wyborcza.pl/7,75400,32842045,matematycy-bronia-matematyki-przed-ai-tysiace-podpisow-pod.html),
a major Polish national daily. While diagnosing, search also surfaced *further*
uncaptured Polish coverage (gry-online.pl, osp1.pl), confirming a **systematic
recall gap**, not a one-off.

## What happened (root cause)

The miss is a **discovery-recall** failure, not a verification error. The
verified catalog is high-precision but a **lower bound**, weakest for languages
we never explicitly searched.

1. **Enumerated-language bias (primary).** The 16 discovery lenses named specific
   languages — Dutch, German, French, Spanish, Italian, Portuguese, Chinese,
   Japanese, Korean, Russian, Turkish, Arabic. **Polish was never named**, nor
   were Nordic, Czech/Slovak, Hungarian, Romanian, Ukrainian, Greek, Hebrew,
   Hindi & other Indian languages, Indonesian/Malay, Vietnamese, Thai, Tagalog.
   An agent told to search "Romance/Asian press" issues queries only in the
   languages it was given; non-enumerated languages got **zero targeted queries**.
2. **US-locale search index.** `WebSearch` is US-based. Polish-language,
   Poland-region pages are heavily down-ranked for English/brand-only queries.
   Surfacing them needs **native-language queries** (e.g. *"deklaracja
   lejdejska"*, *"matematycy AI"*).
3. **Translated brand name.** Polish coverage uses *"deklaracja lejdejska"*, not
   "Leiden Declaration", so English brand-string searches (incl. the broad
   catch-all lens) miss it.
4. **Gap critic inherited the blind spot.** The completeness critic reasoned from
   "what's missing among what we found" and prioritized other angles; it never
   generated a Poland/Polish query because it shared the same enumerated-language
   prior.
5. **Verification fragility (secondary).** Even if discovered, Wyborcza is
   paywalled and blocks automated fetch (confirmed: `WebFetch` failed), so it
   could only reach `likely` via corroboration — and a verifier hitting a hard
   block might have dropped it instead of downgrading confidence.
6. **No authoritative seed lists / structured sources.** We didn't seed per-country
   top-newspaper lists, nor mine high-recall structured sources (Altmetric/Crossref
   Event Data on the Zenodo DOI, Google News country editions, the References of
   the Wikipedia article across language editions, reverse-links to
   leidendeclaration.ai).

## The fix

### Phase 0 — Immediate (DONE 2026-06-16)
- [x] Added the Wyborcza mention manually (`likely`; metadata partly
      reconstructed because the page is paywalled).
- [x] Regenerated the vault + landing page; redeployed Pages.

### Phase 1 — Close the language/region gap (highest leverage) — DONE 2026-06-16
- [x] Ran **24 native-language lenses** (querying in-language + local translation,
      seeded with national outlets). Result: **+33 mentions in 13 new languages**
      (Catalan, Croatian, Czech, Greek, Hebrew, Hungarian, Indonesian, Norwegian,
      Persian, Romanian, Serbian, Thai, Vietnamese). Catalogue 131 → 171;
      languages 15 → 27; now 44 countries.
- Lesson: the `args` dedup list did not arrive in the workflow as an array
  (`Array.isArray(args)` false → empty), so the in-workflow pre-filter was a
  no-op and ~57 already-known URLs were re-verified; final dedupe-on-merge kept
  the data correct. Next time embed the existing-URL set in the script (as done
  for the geo-enrichment step) rather than relying on `args`.

### Phase 2 — Higher-recall discovery beyond keyword search
- [ ] Mine **Altmetric / Crossref Event Data** for DOI `10.5281/zenodo.20302944`
      (captures news + blogs + social systematically).
- [ ] Pull the **References & External links** from the Wikipedia article in
      **all language editions**.
- [ ] Query **Google News** per-country/per-language editions.
- [ ] Reverse-link search: who links to `leidendeclaration.ai`.

### Phase 3 — Verification robustness for paywalled/regional press
- [ ] On blocked fetch (paywall/403/JS), fall back to **archive.org /
      archive.today / Google cache / AMP-mobile** variants before giving up.
- [ ] **Never drop** on fetch failure — downgrade to `likely`/`unverified` with a
      note (as we now do for NYT/Wyborcza).
- [ ] Per-language **false-positive guard** keyed on the translated declaration
      name.

### Phase 4 — Process / QA so gaps are visible, not silent
- [ ] A **missing-language critic** that enumerates languages/countries NOT yet
      represented and forces ≥1 native query per gap; **loop-until-dry** per
      language.
- [ ] **Log coverage explicitly** (languages covered; items dropped on fetch) so
      under-coverage is reported, not silently absent.
- [ ] Make re-runs **incremental**: dedupe new finds against `data/mentions.json`,
      append only.

## Honest status line
After Phases 1–2: **171 verified mentions, 27 languages, 44 countries** — high
precision, far broader recall. Still a lower bound: long-tail regional/social
coverage continues to grow, and some flagged items remain open (e.g. a John
Horgan post we could not locate; paywalled items like Le Figaro held at
`likely`). The adversarial pass also rejected a circulating false claim that
Yann LeCun signed (he did not — see the vault Analysis note).
