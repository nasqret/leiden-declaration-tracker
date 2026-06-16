#!/usr/bin/env python3
"""
Generate the Obsidian knowledge base and the landing page from data/mentions.json.

Single source of truth: data/mentions.json
Outputs (regenerated, safe to delete and rebuild):
  vault/Home.md                      - Map of Content (MOC)
  vault/Declaration/...              - the declaration overview note
  vault/Mentions/<NN-slug>.md        - one note per mention
  vault/Mentions/_All mentions.md    - master sortable table
  vault/Outlets/<outlet>.md          - one note per outlet, aggregating its mentions
  vault/People/<person>.md           - notes for key people, backlinked
  landing/index.html                 - self-contained, filterable landing page

Usage:  python3 scripts/generate.py
"""
import json
import re
import html
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "mentions.json"
VAULT = ROOT / "vault"
LANDING = ROOT / "landing"

TYPE_LABELS = {
    "newspaper": "📰 Newspapers & wire services",
    "wire": "📰 Newspapers & wire services",
    "magazine": "🧪 Science & tech magazines",
    "academic": "🎓 Academic & scholarly",
    "institutional": "🏛️ Institutions & societies",
    "blog": "✍️ Blogs",
    "newsletter": "📨 Newsletters",
    "social": "💬 Social media",
    "forum": "🗣️ Forums & discussion",
    "podcast": "🎙️ Podcasts",
    "video": "🎬 Video",
    "event": "📅 Events",
    "preprint": "📄 Preprints",
    "other": "🔗 Other",
}
# Ordering for display
TYPE_ORDER = [
    "newspaper", "wire", "magazine", "academic", "institutional",
    "blog", "newsletter", "social", "forum", "podcast", "video",
    "event", "preprint", "other",
]


def slugify(text, maxlen=70):
    text = (text or "").strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return (text[:maxlen]).strip("-") or "untitled"


def safe_name(text, maxlen=80):
    """Filesystem/Obsidian-safe note title (no path separators or illegal chars)."""
    text = (text or "").strip()
    text = re.sub(r'[\\/:*?"<>|#\^\[\]]', "-", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:maxlen].strip() or "Untitled"


def yaml_value(v):
    if v is None:
        return '""'
    s = str(v).replace('"', "'")
    return f'"{s}"'


def yaml_list(items):
    if not items:
        return "[]"
    return "[" + ", ".join(yaml_value(i) for i in items) + "]"


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def type_label(t):
    return TYPE_LABELS.get(t, TYPE_LABELS["other"])


# Key people get dedicated, backlinked notes in People/
KEY_PEOPLE = {
    "Jim Portegies": "Eindhoven University of Technology (TU/e); chair of the working group that drafted the declaration.",
    "Terence Tao": "UCLA; Fields Medalist; prominent signatory and frequent commentator on AI in mathematics.",
    "Peter Scholze": "University of Bonn / Max Planck Institute; Fields Medalist; notable signatory.",
    "Robbert Dijkgraaf": "Mathematical physicist; former Dutch Minister of Education, Culture and Science; notable signatory.",
    "Kevin Buzzard": "Imperial College London; leader of formalization (Lean) efforts; notable signatory.",
    "Jeremy Avigad": "Carnegie Mellon University; logic and formal verification; notable signatory.",
}


def render_mention_note(idx, m):
    title = m.get("title") or "(untitled)"
    outlet = m.get("outlet") or "Unknown outlet"
    note_title = safe_name(f"{outlet} — {title}")
    slug = f"{idx:02d}-{slugify(outlet + '-' + title)}"
    tags = ["mention", m.get("outlet_type", "other")]
    if m.get("language") and m["language"].lower() not in ("english", "en"):
        tags.append("non-english")
    if m.get("confidence"):
        tags.append("conf/" + m["confidence"])

    fm = [
        "---",
        f"title: {yaml_value(title)}",
        f"outlet: {yaml_value(outlet)}",
        f"type: {yaml_value(m.get('outlet_type', 'other'))}",
        f"author: {yaml_value(m.get('author', ''))}",
        f"date: {yaml_value(m.get('date', ''))}",
        f"language: {yaml_value(m.get('language', 'English'))}",
        f"confidence: {yaml_value(m.get('confidence', ''))}",
        f"url: {yaml_value(m.get('url', ''))}",
        f"tags: {yaml_list(tags)}",
        "---",
        "",
    ]
    body = [
        f"# {title}",
        "",
        f"> **Outlet:** [[{safe_name(outlet)}]] · **Type:** {type_label(m.get('outlet_type','other'))}"
        + (f" · **Author:** {m['author']}" if m.get("author") else "")
        + (f" · **Date:** {m['date']}" if m.get("date") else "")
        + (f" · **Language:** {m['language']}" if m.get("language") else ""),
        "",
        f"**Link:** {m.get('url','')}",
        "",
        "## Summary",
        "",
        m.get("summary", "_No summary available._"),
        "",
    ]
    if m.get("key_quote"):
        body += ["## Key quote", "", f"> {m['key_quote']}", ""]
    if m.get("influence"):
        body += ["## Significance", "", m["influence"], ""]
    if m.get("notes"):
        body += ["## Notes", "", m["notes"], ""]
    body += [
        "---",
        "",
        "Part of [[Leiden Declaration on AI and Mathematics]] coverage · see [[Home]]",
        "",
    ]
    return slug, note_title, "\n".join(fm) + "\n".join(body)


def render_home(data, mentions):
    subj = data.get("subject", {})
    synth = data.get("synthesis", {}) or {}
    counts = data.get("counts", {}) or {}
    by_type = defaultdict(list)
    for m in mentions:
        by_type[m.get("outlet_type", "other")].append(m)

    lines = [
        "---",
        "tags: [moc, home]",
        "---",
        "",
        "# 🗺️ Leiden Declaration — Media Coverage Map",
        "",
        f"Knowledge base tracking **every traced mention** of the "
        f"[[Leiden Declaration on AI and Mathematics]] across the internet — "
        f"newspapers, magazines, blogs, institutional announcements and social media.",
        "",
        f"- **Total verified mentions:** {len(mentions)}",
        f"- **Declaration published:** {subj.get('published','2026-06-02')}",
        f"- **Knowledge base generated:** {data.get('generated','')}",
        "",
        "## Executive summary",
        "",
        synth.get("executive_summary", "_Pending._"),
        "",
    ]
    if synth.get("reach_assessment"):
        lines += ["## Reach", "", synth["reach_assessment"], ""]
    if synth.get("coverage_themes"):
        lines += ["## Recurring themes", ""]
        lines += [f"- {t}" for t in synth["coverage_themes"]]
        lines += [""]
    if synth.get("notable_voices"):
        lines += ["## Notable voices", ""]
        lines += [f"- {v}" for v in synth["notable_voices"]]
        lines += [""]

    lines += ["## Mentions by category", ""]
    for t in TYPE_ORDER:
        items = by_type.get(t)
        if not items:
            continue
        lines += [f"### {type_label(t)} ({len(items)})", ""]
        for m in items:
            nt = safe_name(f"{m.get('outlet','')} — {m.get('title','')}")
            meta = " · ".join(filter(None, [m.get("date", ""), m.get("author", "")]))
            lines.append(f"- [[{nt}]]" + (f" — _{meta}_" if meta else ""))
        lines.append("")

    lines += [
        "## Indexes",
        "",
        "- [[_All mentions]] — master table",
        "- Browse the **Outlets/** and **People/** folders",
        "- Open the **graph view** to see how outlets, people and the declaration connect",
        "",
    ]
    return "\n".join(lines)


def render_declaration(data):
    subj = data.get("subject", {})
    lines = [
        "---",
        "tags: [declaration, core]",
        f"url: {yaml_value(subj.get('url','https://leidendeclaration.ai'))}",
        f"doi: {yaml_value(subj.get('doi',''))}",
        f"published: {yaml_value(subj.get('published',''))}",
        "---",
        "",
        "# Leiden Declaration on AI and Mathematics",
        "",
        subj.get("summary", ""),
        "",
        "## Facts",
        "",
        f"- **Website:** {subj.get('url','https://leidendeclaration.ai')}",
        f"- **DOI:** {subj.get('doi','')}",
        f"- **Published:** {subj.get('published','')}",
        f"- **Origin:** {subj.get('origin','')}",
        f"- **Working group lead:** {subj.get('lead','')}",
        f"- **Endorsement:** {subj.get('endorsement','')}",
        f"- **Signatories:** {subj.get('signatory_count','')}",
        "",
        "## Notable signatories",
        "",
    ]
    for s in subj.get("notable_signatories", []):
        nm = safe_name(s)
        if s in KEY_PEOPLE:
            lines.append(f"- [[{nm}]]")
        else:
            lines.append(f"- {s}")
    lines += [
        "",
        "## Coverage",
        "",
        "See [[Home]] for the full media-coverage map.",
        "",
    ]
    return "\n".join(lines)


def render_outlets(mentions):
    by_outlet = defaultdict(list)
    for m in mentions:
        by_outlet[m.get("outlet", "Unknown")].append(m)
    for outlet, items in by_outlet.items():
        nm = safe_name(outlet)
        lines = [
            "---",
            "tags: [outlet]",
            f"mentions: {len(items)}",
            "---",
            "",
            f"# {outlet}",
            "",
            f"{len(items)} traced mention(s) of the [[Leiden Declaration on AI and Mathematics]]:",
            "",
        ]
        for m in items:
            nt = safe_name(f"{m.get('outlet','')} — {m.get('title','')}")
            meta = " · ".join(filter(None, [m.get("date", ""), m.get("author", "")]))
            lines.append(f"- [[{nt}]]" + (f" — _{meta}_" if meta else ""))
        lines.append("")
        write(VAULT / "Outlets" / f"{nm}.md", "\n".join(lines))


def render_people(data, mentions):
    subj = data.get("subject", {})
    # union of curated key people + notable signatories that we know about
    people = dict(KEY_PEOPLE)
    for m in mentions:
        a = (m.get("author") or "").strip()
        if a and a in KEY_PEOPLE:
            pass
    for name, blurb in people.items():
        nm = safe_name(name)
        authored = [m for m in mentions if (m.get("author") or "").strip() == name]
        lines = [
            "---",
            "tags: [person]",
            "---",
            "",
            f"# {name}",
            "",
            blurb,
            "",
            f"Connected to the [[Leiden Declaration on AI and Mathematics]].",
            "",
        ]
        if authored:
            lines += ["## Wrote / spoke about it", ""]
            for m in authored:
                nt = safe_name(f"{m.get('outlet','')} — {m.get('title','')}")
                lines.append(f"- [[{nt}]]")
            lines.append("")
        write(VAULT / "People" / f"{nm}.md", "\n".join(lines))


def render_table(mentions):
    lines = [
        "---",
        "tags: [index, table]",
        "---",
        "",
        "# All mentions — master table",
        "",
        f"{len(mentions)} verified mentions. See [[Home]] for the grouped view.",
        "",
        "| # | Outlet | Type | Title | Author | Date | Lang | Conf | Link |",
        "|---|--------|------|-------|--------|------|------|------|------|",
    ]
    for i, m in enumerate(mentions, 1):
        nt = safe_name(f"{m.get('outlet','')} — {m.get('title','')}")
        row = [
            str(i),
            m.get("outlet", ""),
            m.get("outlet_type", ""),
            f"[[{nt}\\|{(m.get('title','') or '')[:60]}]]",
            m.get("author", "") or "",
            m.get("date", "") or "",
            m.get("language", "") or "",
            m.get("confidence", "") or "",
            f"[link]({m.get('url','')})" if m.get("url") else "",
        ]
        row = [c.replace("|", "\\|") for c in row]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    return "\n".join(lines)


def render_landing(data, mentions):
    subj = data.get("subject", {})
    synth = data.get("synthesis", {}) or {}
    payload = json.dumps(mentions, ensure_ascii=False)
    types = sorted({m.get("outlet_type", "other") for m in mentions})
    langs = sorted({m.get("language", "English") or "English" for m in mentions})
    esc = html.escape
    type_options = "".join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in types)
    lang_options = "".join(f'<option value="{esc(l)}">{esc(l)}</option>' for l in langs)
    themes = "".join(f"<li>{esc(t)}</li>" for t in synth.get("coverage_themes", []))
    voices = "".join(f"<li>{esc(v)}</li>" for v in synth.get("notable_voices", []))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Leiden Declaration — Media Coverage Tracker</title>
<style>
  :root {{
    --bg:#0f1020; --card:#1a1b30; --ink:#e8e8f0; --muted:#a4a4c0;
    --accent:#8b5cf6; --accent2:#22d3ee; --line:#2c2d48;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
         background:linear-gradient(180deg,#0b0c18,#0f1020 40%); color:var(--ink); }}
  a {{ color:var(--accent2); text-decoration:none; }}
  a:hover {{ text-decoration:underline; }}
  header {{ padding:56px 24px 32px; max-width:1100px; margin:0 auto; }}
  .eyebrow {{ letter-spacing:.18em; text-transform:uppercase; color:var(--accent); font-size:.72rem; font-weight:700; }}
  h1 {{ font-size:2.4rem; line-height:1.1; margin:.3em 0 .2em; }}
  .sub {{ color:var(--muted); max-width:760px; font-size:1.05rem; }}
  .stats {{ display:flex; flex-wrap:wrap; gap:14px; margin:26px 0 0; }}
  .stat {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:14px 18px; min-width:130px; }}
  .stat b {{ display:block; font-size:1.7rem; color:#fff; }}
  .stat span {{ color:var(--muted); font-size:.8rem; }}
  main {{ max-width:1100px; margin:0 auto; padding:0 24px 80px; }}
  .panel {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:22px 24px; margin:18px 0 28px; }}
  .panel h2 {{ margin:.1em 0 .5em; font-size:1.05rem; color:var(--accent2); }}
  .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
  .cols ul {{ margin:.2em 0; padding-left:1.1em; color:var(--muted); }}
  .controls {{ position:sticky; top:0; z-index:5; background:rgba(15,16,32,.92); backdrop-filter:blur(8px);
               display:flex; flex-wrap:wrap; gap:10px; padding:16px 0; border-bottom:1px solid var(--line); margin-bottom:8px; }}
  input,select {{ background:#13142a; color:var(--ink); border:1px solid var(--line); border-radius:10px; padding:10px 12px; font:inherit; }}
  input[type=search] {{ flex:1; min-width:220px; }}
  .count {{ color:var(--muted); align-self:center; font-size:.85rem; }}
  .item {{ background:var(--card); border:1px solid var(--line); border-radius:14px; padding:18px 20px; margin:12px 0;
           transition:border-color .15s, transform .15s; }}
  .item:hover {{ border-color:var(--accent); transform:translateY(-1px); }}
  .item h3 {{ margin:0 0 6px; font-size:1.08rem; }}
  .meta {{ color:var(--muted); font-size:.85rem; display:flex; flex-wrap:wrap; gap:8px 14px; margin-bottom:8px; }}
  .badge {{ display:inline-block; background:#2a1d52; color:#c4b5fd; border:1px solid #3b2a72;
            border-radius:999px; padding:1px 10px; font-size:.72rem; text-transform:uppercase; letter-spacing:.04em; }}
  .summary {{ color:#cfd0e6; }}
  .quote {{ border-left:3px solid var(--accent); padding-left:12px; color:var(--muted); font-style:italic; margin:10px 0 0; }}
  footer {{ max-width:1100px; margin:0 auto; padding:24px; color:var(--muted); font-size:.82rem; border-top:1px solid var(--line); }}
  @media (max-width:720px) {{ .cols {{ grid-template-columns:1fr; }} h1{{font-size:1.9rem;}} }}
</style>
</head>
<body>
<header>
  <div class="eyebrow">Media coverage tracker</div>
  <h1>The Leiden Declaration on AI &amp; Mathematics</h1>
  <p class="sub">{esc(subj.get('summary',''))}</p>
  <div class="stats">
    <div class="stat"><b>{len(mentions)}</b><span>traced mentions</span></div>
    <div class="stat"><b>{len(types)}</b><span>channel types</span></div>
    <div class="stat"><b>{len(langs)}</b><span>languages</span></div>
    <div class="stat"><b>{esc(str(subj.get('signatory_count','')))}</b><span>signatories</span></div>
    <div class="stat"><b>{esc(str(subj.get('published','')))}</b><span>published</span></div>
  </div>
  <p class="sub" style="margin-top:18px">
    Declaration: <a href="{esc(subj.get('url','https://leidendeclaration.ai'))}">{esc(subj.get('url','leidendeclaration.ai'))}</a>
    &nbsp;·&nbsp; News page: <a href="https://leidendeclaration.ai/news">leidendeclaration.ai/news</a>
  </p>
</header>
<main>
  <div class="panel">
    <h2>Executive summary</h2>
    <p>{esc(synth.get('executive_summary',''))}</p>
    <p style="color:var(--muted)">{esc(synth.get('reach_assessment',''))}</p>
    <div class="cols">
      <div><h2>Recurring themes</h2><ul>{themes}</ul></div>
      <div><h2>Notable voices</h2><ul>{voices}</ul></div>
    </div>
  </div>

  <div class="controls">
    <input id="q" type="search" placeholder="Search title, outlet, author, summary…">
    <select id="type"><option value="">All types</option>{type_options}</select>
    <select id="lang"><option value="">All languages</option>{lang_options}</select>
    <span class="count" id="count"></span>
  </div>
  <div id="list"></div>
</main>
<footer>
  Generated {esc(str(data.get('generated','')))} from <code>data/mentions.json</code>.
  Each mention was located via multi-source web search and adversarially verified.
  This tracker is an independent knowledge base about the declaration's reception.
</footer>
<script>
const DATA = {payload};
const list = document.getElementById('list');
const q = document.getElementById('q');
const typeSel = document.getElementById('type');
const langSel = document.getElementById('lang');
const count = document.getElementById('count');
function esc(s){{ return (s||'').replace(/[&<>"]/g, c => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c])); }}
function render(){{
  const term = q.value.trim().toLowerCase();
  const t = typeSel.value, l = langSel.value;
  const rows = DATA.filter(m => {{
    if (t && m.outlet_type !== t) return false;
    if (l && (m.language||'English') !== l) return false;
    if (term){{
      const hay = [m.title,m.outlet,m.author,m.summary,m.key_quote].join(' ').toLowerCase();
      if (!hay.includes(term)) return false;
    }}
    return true;
  }});
  count.textContent = rows.length + ' / ' + DATA.length + ' shown';
  list.innerHTML = rows.map(m => `
    <div class="item">
      <h3><a href="${{esc(m.url)}}" target="_blank" rel="noopener">${{esc(m.title)}}</a></h3>
      <div class="meta">
        <span class="badge">${{esc(m.outlet_type)}}</span>
        <span><b>${{esc(m.outlet)}}</b></span>
        ${{m.author?`<span>✍ ${{esc(m.author)}}</span>`:''}}
        ${{m.date?`<span>📅 ${{esc(m.date)}}</span>`:''}}
        ${{m.language?`<span>🌐 ${{esc(m.language)}}</span>`:''}}
      </div>
      <div class="summary">${{esc(m.summary)}}</div>
      ${{m.key_quote?`<p class="quote">${{esc(m.key_quote)}}</p>`:''}}
    </div>`).join('');
}}
q.addEventListener('input', render);
typeSel.addEventListener('change', render);
langSel.addEventListener('change', render);
render();
</script>
</body>
</html>
"""


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    mentions = data.get("mentions", [])
    # stable ordering: by type order, then date desc, then outlet
    type_rank = {t: i for i, t in enumerate(TYPE_ORDER)}
    mentions.sort(key=lambda m: (type_rank.get(m.get("outlet_type", "other"), 99),
                                 str(m.get("date", "")), m.get("outlet", "")))

    # clean previous generated mention notes (keep folder)
    for p in (VAULT / "Mentions").glob("*.md"):
        p.unlink()
    for p in (VAULT / "Outlets").glob("*.md"):
        p.unlink()

    for i, m in enumerate(mentions, 1):
        slug, _title, content = render_mention_note(i, m)
        write(VAULT / "Mentions" / f"{slug}.md", content)

    write(VAULT / "Home.md", render_home(data, mentions))
    write(VAULT / "Declaration" / "Leiden Declaration on AI and Mathematics.md", render_declaration(data))
    write(VAULT / "Mentions" / "_All mentions.md", render_table(mentions))
    render_outlets(mentions)
    render_people(data, mentions)
    write(LANDING / "index.html", render_landing(data, mentions))

    print(f"Generated {len(mentions)} mention notes + Home + Declaration + "
          f"{len(set(m.get('outlet') for m in mentions))} outlet notes + landing page.")


if __name__ == "__main__":
    main()
