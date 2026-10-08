#!/usr/bin/env python3
"""Cadence v3 evidence collection: resolve + search + precedent queries for the 42 spec elements."""
import json, subprocess, pathlib

REPO = pathlib.Path('/home/xrim/design-authority')
OUT = REPO / 'examples' / 'cadence3-leader'
EV = OUT / '_evidence'
EV.mkdir(parents=True, exist_ok=True)

ELEMENTS = [
 "a primary button for the main action",
 "a secondary button and a text link",
 "delete a ritual permanently",
 "a confirmation dialog before deleting",
 "a modal with ritual details",
 "a toast notification saying logged",
 "a banner summarizing the week",
 "an empty state when no rituals exist",
 "an error message under the field",
 "a loading spinner while saving",
 "a circular progress ring of today's completion",
 "a bar chart of weekly minutes",
 "a calendar heatmap of the month",
 "a tiny sparkline trend of the last week",
 "a big streak counter",
 "an achievement badge for seven days",
 "a status label on track or slipping",
 "a profile avatar photo",
 "an icon for each ritual",
 "a toggle switch in settings",
 "a slider for daily goal minutes",
 "a date picker for the log entry",
 "a number stepper for minutes",
 "a text field for the ritual name",
 "a select for ritual category",
 "a checkbox for reminders",
 "radio buttons for frequency",
 "a text area for notes",
 "tabs for today history achievements",
 "a bottom navigation bar on mobile",
 "a table of logged entries",
 "pagination for older entries",
 "a search box to filter rituals",
 "a small category tag",
 "drag to reorder rituals",
 "an undo button after deleting",
 "a three-step onboarding wizard",
 "export the data as csv",
 "a dark mode theme",
 "a celebration animation when checking off",
 "an illustration in the empty state",
 "upload a photo for the ritual",
]

SYNONYMS = {
 "delete a ritual permanently": ["destructive", "delete permanently", "remove"],
 "a confirmation dialog before deleting": ["confirm", "confirmation"],
 "a modal with ritual details": ["dialog", "overlay", "panel"],
 "a toast notification saying logged": ["toast", "notification", "transient feedback"],
 "a banner summarizing the week": ["notice", "summary", "banner"],
 "an empty state when no rituals exist": ["empty", "empty state"],
 "an error message under the field": ["error", "validation error"],
 "a loading spinner while saving": ["loading", "spinner", "progress"],
 "a circular progress ring of today's completion": ["ring", "gauge", "progress ring", "circle"],
 "a calendar heatmap of the month": ["heatmap", "month grid", "calendar"],
 "an achievement badge for seven days": ["badge", "medal", "award"],
 "a profile avatar photo": ["avatar", "monogram", "profile"],
 "an icon for each ritual": ["icon", "glyph", "mark"],
 "a number stepper for minutes": ["stepper", "increment", "number input"],
 "tabs for today history achievements": ["tabs", "tab bar", "segmented control"],
 "a bottom navigation bar on mobile": ["bottom bar", "bottom navigation", "navbar"],
 "a table of logged entries": ["table", "ledger", "rows"],
 "pagination for older entries": ["pagination", "pager", "pages"],
 "an undo button after deleting": ["undo", "revert"],
 "a three-step onboarding wizard": ["wizard", "onboarding", "steps"],
 "export the data as csv": ["export", "download", "csv"],
 "a dark mode theme": ["dark", "theme", "colour scheme"],
 "a celebration animation when checking off": ["animation", "motion", "celebration"],
 "an illustration in the empty state": ["illustration", "image"],
 "upload a photo for the ritual": ["photo", "upload", "image"],
 "a toggle switch in settings": ["toggle", "switch"],
 "a slider for daily goal minutes": ["slider", "range"],
 "a date picker for the log entry": ["date", "date picker", "picker"],
 "a select for ritual category": ["select", "dropdown"],
 "drag to reorder rituals": ["drag", "reorder", "sort"],
 "a small category tag": ["tag", "label", "status"],
}

PREC_QUERIES = ["toast", "spinner", "loading", "badge", "achievement", "icon", "avatar", "photo",
 "delete", "confirm", "table", "ledger", "drag", "reorder", "csv", "export", "dark", "theme",
 "toggle", "slider", "checkbox", "radio", "date", "select", "dialog", "modal", "wizard", "onboarding",
 "ring", "gauge", "tabs", "pagination", "undo", "animation", "motion", "step", "empty", "progress"]

def da(args):
    p = subprocess.run(['python3', 'tools/da.py', '--pack', 'packs/leader'] + args,
                       cwd=str(REPO), capture_output=True, text=True)
    return p

res_path = EV / 'resolves.jsonl'
search_path = EV / 'searches.jsonl'
prec_path = EV / 'precedent-queries.jsonl'

rows = []
with res_path.open('w') as rf:
    for i, el in enumerate(ELEMENTS, 1):
        p = da(['resolve', el, '--json'])
        d = json.loads(p.stdout)
        rf.write(json.dumps(d) + '\n')
        res = d.get('resolution') or {}
        rid = None
        for key in ('artifact', 'recipe', 'fallback', 'prohibition'):
            if isinstance(res.get(key), dict) and res[key].get('id'):
                rid = res[key]['id']; break
        pre = [x['id'] for x in (d.get('precedents') or [])]
        closest = [(c['id'], c['score']) for c in (d.get('closest') or [])]
        rows.append({'n': i, 'el': el, 'outcome': d['outcome'], 'id': rid,
                     'precedents': pre, 'closest': closest,
                     'why': d.get('why', '')})

# searches: one per element + synonyms for undefined/unclear ones
with search_path.open('w') as sf:
    for el in ELEMENTS:
        for q in [el] + SYNONYMS.get(el, []):
            p = da(['search', q, '--json'])
            try:
                sr = json.loads(p.stdout)
            except Exception:
                sr = []
            sf.write(json.dumps({'element': el, 'query': q, 'results': sr}) + '\n')

with prec_path.open('w') as pf:
    for q in PREC_QUERIES:
        p = da(['precedents', '--query', q, '--json'])
        d = json.loads(p.stdout)
        if d.get('count'):
            pf.write(json.dumps({'query': q, 'count': d['count'],
                                 'ids': [x['id'] for x in d['precedents']]}) + '\n')

print(f"{'#':>2} | {'outcome':<9} | {'resolution':<34} | precedents | element")
for r in rows:
    idor = (r['id'] or '')[:34]
    pr = ','.join(x.replace('precedent/declined-', '') for x in r['precedents'])
    cl = ' | closest: ' + str(r['closest'][:1]) if r['outcome'] == 'UNDEFINED' else ''
    print(f"{r['n']:>2} | {r['outcome']:<9} | {idor:<34} | {pr}{cl}")

from collections import Counter
print('\nMIX:', dict(Counter(r['outcome'] for r in rows)))
