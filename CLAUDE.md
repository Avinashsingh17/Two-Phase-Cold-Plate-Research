# CLAUDE.md — Two-Phase Cold Plate Wiki Schema

## Project reference
Read `PROJECT_CONTEXT.md` for project goals, physics scope, execution phases,
and validation philosophy. That file is authoritative; this file governs only
how the wiki is maintained.

---

## Directory structure

```
two-phase-cold-plate/
├── CLAUDE.md                  # this file — wiki schema
├── PROJECT_CONTEXT.md         # project goals, phases, constraints
├── raw/                       # IMMUTABLE source documents (you read, never modify)
│   ├── papers/                # PDF or markdown-clipped papers
│   └── assets/                # locally downloaded images
├── wiki/                      # LLM-generated knowledge base (you write)
│   ├── index.md               # catalog of all wiki pages (updated on every ingest)
│   ├── log.md                 # append-only chronological record
│   ├── papers/                # one summary page per ingested source
│   ├── concepts/              # physics topics, methods, model choices
│   ├── entities/              # authors, labs, hardware systems, fluids
│   ├── comparisons/           # head-to-head tables and analysis pages
│   ├── synthesis/             # evolving thesis, Pareto landscape, open questions
│   ├── communication/         # audience-facing artifacts (explanations, pitches)
│   └── templates/             # page templates — load on demand, do not preload
└── src/ benchmarks/ tests/ …  # code (see PROJECT_CONTEXT.md)
```

---

## Wiki conventions

- All wiki pages are markdown with YAML frontmatter (see templates/).
- Cross-references use `[[WikiPageName]]` style (Obsidian-compatible).
- Every claim that comes from a source gets an inline citation: `[Author YYYY]`.
- Contradictions between sources are flagged with a `> **CONFLICT:**` blockquote.
- Stale or uncertain claims are tagged `<!-- TODO: verify -->`.

---

## Workflows

### Ingest (adding a new source)

Trigger: user drops a file into `raw/papers/` and says "ingest [filename]".

Steps — execute in order:
1. Read the source document.
2. Briefly discuss key takeaways with the user (2–5 bullets). Ask if anything
   should be emphasized or de-emphasized before writing.
3. Create `wiki/papers/<AuthorYear_slug>.md` using the paper template.
4. Update or create pages in `wiki/concepts/`, `wiki/entities/` that the paper
   touches. Update cross-references in existing pages.
5. Check `wiki/synthesis/` — does the new source support, challenge, or nuance
   the current thesis? Update accordingly.
6. Update `wiki/index.md` — add a one-line entry for every new or materially
   changed page.
7. Append one entry to `wiki/log.md`:
   `## [YYYY-MM-DD] ingest | Author YYYY — Short Title`

Each ingest typically touches 5–15 pages. Prefer updating existing pages over
creating new ones; create new pages when a concept genuinely lacks a home.

### Query (answering a question against the wiki)

Trigger: user asks a question about the literature corpus.

Steps:
1. Read `wiki/index.md` to identify relevant pages.
2. Read those pages. If citations point to `raw/papers/`, read those too if needed.
3. Synthesize an answer with inline citations.
4. If the answer is substantive and reusable (a comparison, a derived insight,
   a resolved contradiction), offer to file it as a new wiki page or update
   an existing synthesis page.

### Lint (health-check)

Trigger: user says "lint the wiki" or "wiki health check".

Check for and report:
- Contradictions between pages not yet flagged with `> **CONFLICT:**`
- Claims superseded by a later-ingested source
- Orphan pages (no inbound `[[links]]`)
- Important concepts mentioned across pages but lacking their own concept page
- Missing cross-references between clearly related pages
- `<!-- TODO: verify -->` items that can now be resolved
- Data gaps worth filling with a targeted web search or new source

Report findings as a prioritized list. Ask before making bulk changes.

---

## Index and log maintenance

**`wiki/index.md`** — organized by category (papers, concepts, entities,
comparisons, synthesis). Format per entry:
```
- [[PageName]] — one-line description  [N sources]
```
Updated on every ingest. Read this first when answering any query.

**`wiki/log.md`** — append-only. Each entry:
```
## [YYYY-MM-DD] <type> | <title>
<1–3 line summary of what changed and why>
```
Types: `ingest`, `query`, `lint`, `update`. Never edit past entries.

---

## Page templates

Templates live in `wiki/templates/`. Load the relevant template when creating
a new page — do not keep templates in memory between tasks.

- `templates/paper.md` — summary of an ingested source
- `templates/concept.md` — physics topic or method
- `templates/entity.md` — author, lab, hardware system, or fluid
- `templates/comparison.md` — head-to-head of two or more sources/models
- `templates/synthesis.md` — evolving thesis or open-questions page

## Communication artifacts

`wiki/communication/` holds audience-facing documents (plain-language
explanations, elevator pitches, poster abstracts) that derive from the
research synthesis but are distinct from it. These are living documents:
when a new ingest materially changes the project narrative, flag the
change and offer to update the affected communication artifacts.

---

## Validation benchmark registry (authoritative)

Stage 1 — RPI shakedown:
  **Krepper & Rzehak 2011**, DEBORA case (subcooled boiling, R12 refrigerant,
  vertical annulus). Reproduces wall-superheat vs. heat-flux curve and axial
  void-fraction profile. Gate for RPI model setup.

Stage 2 — Cold plate geometry:
  **Qu & Mudawar 2003**, saturated water microchannel heat sink (231 µm × 713 µm
  channels, copper, DI water). Reproduces Nu and pressure drop vs. Re, and
  two-phase performance map. Gate for cold plate design exploration.

No design exploration until both gates are passed and documented in
`wiki/synthesis/validation_status.md`.

---

## Behavioral rules

- **Never modify files in `raw/`.**
- **Never cite `raw/` assets directly as conclusions** — they are sources, not claims.
- When uncertain about a correlation form or model setting, say so. Do not
  fabricate physics.
- Industry white papers (e.g. ACT 2023) may be noted in `wiki/papers/` for
  context but must not be cited as primary sources in the manuscript.
- JetCool: no peer-reviewed publications as of 2025 — note in
  `wiki/entities/JetCool.md` for context, do not cite.
- When templates are needed, read them from `wiki/templates/` at task time;
  do not preload them into context.
