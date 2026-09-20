# Green Hope University — Garowe Campus
## Freshman Orientation & Welcome Portal

A polished **Streamlit** web application that welcomes new students to the Garowe
campus and walks them through freshman onboarding end to end — checklist,
progress tracking, and a campus department directory with one-click email.

Built as a portfolio-ready reference implementation: modular code, a custom CSS
design system, persisted session state, and a test suite.

---

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the portal
streamlit run app.py
```

The app opens at <http://localhost:8501>.

> **Tip for demos:** click **Load demo student** in the sidebar. It fills in a
> sample profile (Amina Yusuf Abdi, BSc Computer Science) and pre-completes four
> checklist steps so the progress dashboard is populated straight away — much
> better than opening on an empty 0%.

---

## What the portal does

### 1. Welcome (landing)
A two-panel hero pairing the campus photograph with a solid brand panel, the
university crest, a warm welcome letter, and a **four-step quick-start guide**
for freshmen. Key deadlines are shown as live countdown cards ("in 11 days").

### 2. Onboarding Checklist
The ten freshman steps, grouped into three orientation phases:

| Phase | Steps |
|---|---|
| **Phase 1 · Before You Arrive** | Registration & documents · Email/portal activation · Tuition & fees |
| **Phase 2 · Week One on Campus** | Student ID card · Hostel allocation · Health check & insurance · Orientation attendance |
| **Phase 3 · Academic Setup** | Course registration · Library card · Student handbook |

Each step is a real checkbox with:
- **weighted points** (the ten weights sum to exactly 100, so the percentage is
  an honest weighted score — paying fees gates your start more than a library card);
- a **deadline chip** that turns amber when due within 7 days and red when overdue;
- an expander containing **why it matters, ordered steps, what to bring, the fee,
  where to go, a practical tip, and a one-click email** to the owning office.

Progress **persists**: ticks are mirrored to `state/progress.json` and replayed
on the next visit, so a student can work through it over several days.

### 3. Progress
A tracking dashboard: an SVG **completion ring**, KPI tiles, **weighted bars by
phase and by category**, a **Plotly deadline countdown**, a **timeline of
orientation week** (all ten sessions, tagged Mandatory / Recommended / Social),
and a sortable table of every outstanding step with its owning office.

### 4. Departments & Contact
The official campus address — **`garowecampus@greenhopeuniversity.edu.so`** —
is given the visual weight it deserves at the top of the tab, with quick actions
(email, call, WhatsApp, website). Below it, all **nine departments**
(Admissions & Registrar, Finance/Bursar, Student Affairs, Academic Advising,
Library, IT Support, Health Center, Hostel & Welfare, Career Services) each with
description, contact person and role, location, hours, services, and a
**one-click `mailto:` link**.

Eight **ready-to-send enquiry templates** handle the common freshman questions
(document status, fees and instalments, hostel, course registration, portal
access, health check, internships, general enquiries). Each opens pre-addressed
and pre-filled with the student's own name, ID and programme.

---

## Project structure

```
green-hope-orientation-portal/
├── app.py                      # Entry point: page config, sidebar, tabs
├── config.yaml                 # ALL branding, contacts, dates, palette
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml             # Theme + static file serving
├── assets/                     # Source images
│   ├── campus_hero.png
│   ├── welcome_illustration.png
│   └── crest.png
├── static/                     # Auto-synced copy, served at app/static/
├── state/
│   └── progress.json           # Persisted checklist + student profile
├── portal/
│   ├── settings.py             # config.yaml loader (deep-merged over defaults)
│   ├── assets.py               # static/ vs base64 data-URI image resolution
│   ├── styles.py               # CSS design system (string.Template)
│   ├── components.py           # Reusable HTML builders + SVG progress ring
│   ├── data.py                 # Checklist, departments, schedule, templates
│   ├── state.py                # Session state + JSON persistence
│   ├── logic/
│   │   ├── progress.py         # Weighted maths, deadlines (pure functions)
│   │   └── mailto.py           # Pre-filled mailto: URL construction
│   └── views/
│       ├── hero.py             # Welcome tab
│       ├── checklist.py        # Onboarding Checklist tab
│       ├── progress.py         # Progress tab
│       └── directory.py        # Departments & Contact tab
└── tests/
    └── test_portal.py          # Standalone test suite (no pytest needed)
```

---

## Configuration

Everything an administrator would change lives in **`config.yaml`** — no view
module hard-codes branding, contacts, dates or colours, so the portal can be
re-skinned for another campus by editing that one file.

```yaml
contact:
  primary_email: "garowecampus@greenhopeuniversity.edu.so"

orientation:
  week_start: "2026-09-21"
  fees_deadline: "2026-10-05"
```

```bash
# Verify the configuration loaded as expected
python3 -c "from portal.settings import CFG; print(CFG['contact']['primary_email'])"
```

**Replacing the images:** drop a new file into `assets/` using the same
filename (e.g. `campus_hero.png`) and restart. `assets.sync_static_dir()`
mirrors it into `static/` on start-up automatically.

**Campus colours:** the palette in `config.yaml → theme` flows into the CSS
custom properties, so the whole UI re-themes from those hex values.

---

## Tests

The suite runs standalone — no pytest required:

```bash
python3 tests/test_portal.py
```

It covers:
- weighted progress maths (weights total 100; 43% for the demo student);
- deadline state transitions (overdue / due-soon / upcoming / none);
- `mailto:` construction and percent-encoding (a key regression risk: `&` in a
  body must not truncate the query string);
- template placeholder rendering, including the unknown-placeholder fallback;
- data integrity — 10 items, 9 departments, every `dept` slug resolving;
- a source-level check that every view module references only names it imports.

---

## Design notes

**Why the ring and bars are hand-built.** The progress ring is inline SVG with
`stroke-dasharray`, and the phase/category bars are plain CSS. Charting
libraries that render to `<canvas>` can lay out at zero width when their tab is
hidden — Streamlit mounts every tab, but only the active one is visible, so a
canvas-based ring would sometimes appear blank until resize. Inline SVG and CSS
have no such failure mode. Plotly is used only for the deadline countdown,
where hover values genuinely add information.

**Why `mailto:` over a form.** The requirement is "direct email contact". A
`mailto:` link hands off to the user's own mail client — no server, no email
credentials, nothing to phish. The message is pre-filled but the student sends
it themselves, and can edit it first.

**Why two image modes.** `brand.image_mode: "static"` (default) serves images
from `./static` via Streamlit's static handler, so the browser caches them;
`"inline"` base64-encodes instead, which is self-contained but re-transmits on
every rerun. `portal/assets.py` abstracts both behind `img_src()`.

---

## Extending it

- **Real data:** replace the literals in `portal/data.py` with database queries
  returning the same dataclasses — no view code changes.
- **Real persistence:** reimplement `load_persisted` / `save_persisted` in
  `portal/state.py` against a database; nothing else touches storage.
- **Authentication:** add `streamlit-authenticator` in front of `main()` and
  key the checklist by student ID.

---

*Green Hope University · Garowe Campus · Knowledge · Service · Hope*
