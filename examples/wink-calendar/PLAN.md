# Wink Calendar — Build Plan (planning stage, not yet built)

Authority: **Wink Interface System** v0.2.0 (`authority-wink`, format 0.1)
Pack location: `/home/xrim/.hermes/profiles/qwen/cache/scratch/wink/pack` (all 8 manifest hashes verified)
CLI: `python3 /tmp/design-authority/tools/da.py --pack pack …`
Reference build: https://designauthority.seanyong.xyz/authorities/wink/site/

## 1. What we're building

A single-page calendar app (Google Calendar-like) for **adding, editing and deleting events**.

- Plain HTML + CSS + vanilla JS (the authority requires no framework)
- Local persistence: `localStorage` (no backend requested)
- Delivery: one folder — `index.html`, `styles.css`, `app.js`, `fonts/` (Fraunces-VF + Inter-VF from the pack zip)

## 2. Views & interactions

| View / interaction | Behaviour |
|---|---|
| **Month grid** (primary view) | 6×7 day cells; today highlighted; day cells show event chips |
| **Day panel** | Click a day → agenda for that day, rendered as ledger rows |
| **Create event** | Primary pill button → dialog with event form |
| **Edit event** | Click an event → same dialog, pre-filled |
| **Delete event** | In dialog → destructive confirm pattern |
| **Navigation** | Prev / next month + "Today" button |
| **Feedback** | Inline notice after save/delete (authority records **no toast pattern**) |
| **Empty state** | Day with no events → recorded empty-state pattern |

Event form fields: title (text), date, start time, end time, all-day toggle, notes (textarea).
Event model: `{ id, title, date, start, end, allDay, notes, createdAt, updatedAt }`.

**v1 scope cut:** month view + day agenda only. Week grid, search, and recurring events are out of scope (search is an authority gap anyway — see §5).

## 3. Authority mapping (every UI need → recorded artifact)

All resolutions verified via `da resolve` / `da inspect` on the Wink pack:

Recorded values the build must quote (from `da inspect` on each record):

- **action-pill** — yellow #FFE01B fill + 1px ink ring (`box-shadow 0 0 0 1px #231E15`); dark variant on warm fields (ink fill, white label); secondary = outline pill (2px ink inset); hover `translateY(-4.875px)` + hard shadow `0 4.875px 0 0` (zero blur)
- **navbar** — white bg, dark links, hover = light-grey rounded-rect fill, primary CTA at right end, **must stay single-row (no wrapping)**
- **card** — white, borderless, radius 16 (24 large), warm ink-tinted shadow `rgba(35,30,21,.2) 0 8px 32px`, padding 48; tinted variant Parsnip no shadow; 1px #DEDDDC borders **only on inputs/dividers, never on cards**
- **field-select** — native inputs; small fixed selects (≤12) get 12px radius + serif field text; larger/filtered → platform-controls fallback, marked
- **badge** — pill, yellow fill, 12/600 label
- **ledger** — white surface, 16px-padded rows, hairline #DEDDDC dividers, no zebra, Parsnip header row 13/500 labels, row hover = Parsnip tint, text links ink + underline
- **dialog-overlay** — white 16px-rounded card on warm ink scrim, **instant appearance, no invented motion**, content from existing primitives
- **destructive-confirm** — 16px confirm dialog; consequence sentence in warm voice; confirm = ink-filled pill with the **concrete verb, never "OK"**; cancel = outline pill; destructive action **never gets default focus**
- **empty-state** — centered notice card: serif headline, one plain warm sentence, one primary pill action
- **inline-notice** — parsnip-filled rounded block, bold lead + plain supporting line; **no toast pattern observed**
- **shape-language** — interactive = pill (+1px ink ring); content vessel = 16/24; structural chrome = square
- **voice** — second person, question-first, plain English, non-blaming, dry wit in microcopy, italic serif emphasis fragment allowed

| UI need | Outcome | Artifact |
|---|---|---|
| Create/Save buttons | RESOLVED | `component/action-pill` (yellow #FFE01B fill + 1px ink ring; secondary = outline pill) |
| Top bar (month title, nav) | RESOLVED | `component/navbar` |
| Day agenda rows | RESOLVED | `component/ledger` (white surface, 16px rows, #DEDDDC hairlines, Parsnip header, no zebra) |
| Event card in day panel | RESOLVED | `component/card` (16/24 soft-radius vessel) |
| Text / select inputs | RESOLVED | `component/field-select` |
| Date / time pickers | **FALLBACK** | `fallback/platform-controls` — native `<input type=date/time>` with wink field styling (radius 8, 1px #DEDDDC border, warm ink text), native semantics kept |
| Add/edit dialog | RESOLVED | `pattern/dialog-overlay` |
| Delete confirm | RESOLVED | `pattern/destructive-confirm` |
| No events | RESOLVED | `pattern/empty-state` |
| Save/delete feedback | RESOLVED | `pattern/inline-notice` (parsnip block, bold lead + plain line) |
| All-day / status markers | RESOLVED | `component/badge` |
| Colours | RESOLVED | `token-set/colour` — yellow = brand + primary action **only**; peppercorn = text/ink/shadow; white + parsnip = surfaces; ochre = band terminator; kale = content links; #BF4055 = error |
| Type sizes | RESOLVED | `token-set/type-scale` — display 48–64 w400; section 35/1.0; body 16/1.35; small 14; labels/buttons 13/500 |
| Corner radii | RESOLVED | `guideline/shape-language` — interactive = pill (+1px ink ring); content vessel = 16/24; structural chrome = square |
| Page/section structure | RESOLVED | `guideline/hierarchy` — one page title; sections = uppercase label → display headline → 1–2 sentence paragraph |
| Microcopy | RESOLVED | `guideline/voice` — second person, question-first, plain English, dry wit allowed |

## 4. Improvisations (recorded pieces → visible, marked)

Where the authority is silent, build from the nearest recorded pieces, mark with an HTML comment + `data-improv=""`, and file a gap:

1. **Month grid layout** — no grid record. Compose from: structural square chrome (shape-language), ledger hairline dividers (#DEDDDC), parsnip/white surfaces (colour roles), today = yellow field (brand colour role).
2. **Event chip in a day cell** — compose from `component/badge` (pill shape, ink ring at small scale).
3. **Prev/next navigation buttons** — compose from `component/action-pill` outline (secondary) variant, square container per shape-language.

## 5. Gaps to file (via `da gap-add`, workspace `.design-authority/`)

1. `month/week calendar grid layout` — UNDEFINED
2. `event chip on calendar day cell` — UNDEFINED
3. `icon/ghost button for grid navigation` — UNDEFINED

(Progress and inline-notice were initially UNDEFINED by natural-language resolve but **do exist** in the pack as `pattern/progress` / `pattern/inline-notice` — no gap filed; they're adopted directly.)

## 6. Verification (before claiming done)

Pack ships **no validators** (`validators: []`), so verification is:
1. Re-read the artifact records for every adopted component; confirm quoted values (colours, radii, type, states) match the records — not memory.
2. Cross-check against the reference build (`site/index.html` + `styles.css` in the verified zip) for selectors/states.
3. Exercise all flows in a browser: create → edit → delete, empty state, confirm dialog, inline notices, month navigation, persistence reload.
4. Confirm no values invented outside records; every improvisation carries `data-improv` and a filed gap.

## 7. House rules being followed

- Quote recorded values; never invent a value a record can give.
- Copy selectors/states from the artefacts, not from memory.
- Adopt only Wink records — nothing borrowed from other authorities.
- Agent reports are evidence, not proof — artifacts get re-read at the end.
