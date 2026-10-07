#!/usr/bin/env python3
"""File gap entries for all improvised/conflict/fallback elements (grouped <=3)."""
import subprocess, json, sys

WS = "examples/cadence2-dominion"
gaps = [
    # G2
    ("Transient success feedback (\"logged\") and weekly-summary banner patterns — D-13 authored a ruled notice, but no notice/banner artifact exists in the pack; toasts are excluded by doctrine",
     "feedback, banner",
     {"element": "toast notification saying logged; banner summarizing the week", "screen": "Today; History"}),
    # G3
    ("Image-free empty-state pattern and in-character alternatives to illustration and photo upload (imagery prohibited; D-16 authored a ruled statement + one action, no artifact)",
     "empty state, imagery alternatives",
     {"element": "empty state when no rituals exist; illustration in the empty state; upload a photo for the ritual", "screen": "Today; Achievements; Ritual detail"}),
    # G4
    ("Loading/saving indicator and non-linear completion display — the meter is linear and static; a spinner is motion; the system offers no busy-state artifact",
     "loading, progress",
     {"element": "loading spinner while saving; circular progress ring of today's completion", "screen": "Log form; Today hero"}),
    # G5
    ("Chart primitives: bar chart, calendar heatmap, sparkline — data visualization is undefined; bar/ink-density forms were improvised from the rectilinear doctrine",
     "charts, data viz",
     {"element": "bar chart of weekly minutes; calendar heatmap of the month; tiny sparkline trend", "screen": "History; Ritual detail"}),
    # G6
    ("Stat/counter display, achievement badge plate, and status-label pattern (D-10 words-only is authored doctrine but not a pack artifact; streak counter and badge are undefined)",
     "stats, badges, status",
     {"element": "big streak counter; achievement badge for seven days; status label on track or slipping", "screen": "Today; Achievements"}),
    # G7
    ("In-app tab navigation and mobile navigation positioning — resolve mapped 'bottom navigation' to the top masthead; a bottom bar is not in the system (D-20: nav collapses to a plain row)",
     "navigation, tabs",
     {"element": "tabs for today history achievements; bottom navigation bar on mobile", "screen": "All views"}),
    # G8
    ("Ruled register (table) pattern and pagination pattern — D-17 authored the ledger doctrine but the pack carries no table/pagination artifact",
     "table, pagination",
     {"element": "table of logged entries; pagination for older entries", "screen": "History"}),
    # G9
    ("Small tag/chip label primitive and motion-free reorder controls (drag-and-drop excluded by the motion doctrine; text controls used instead)",
     "tag, reorder",
     {"element": "small category tag; drag to reorder rituals", "screen": "Today; Settings"}),
    # G10
    ("Theme modes (reversed colourway applied as a dark theme) and completion ceremony/motion guidance — motion is gated but celebration form is undefined",
     "theme, motion",
     {"element": "dark mode theme; celebration animation when checking off", "screen": "Settings; Today"}),
    # G11
    ("Image-free identity markers: avatar and per-ritual icons — imagery/pictograms prohibited; no image-free alternatives (initials/ordinals) are defined as artifacts",
     "avatar, icons",
     {"element": "profile avatar photo; icon for each ritual", "screen": "Masthead; Today ritual list"}),
    # G12
    ("Multi-line field variant (textarea) and export/download action + feedback pattern (CSV export semantics undefined; no download pattern)",
     "field variants, export",
     {"element": "text area for notes; export the data as csv", "screen": "Log form; History; Settings"}),
    # G13
    ("Platform fallbacks in use: toggle/switch, slider, and stepper — pack defines no controls; native elements styled as fields per fallback/platform-controls",
     "controls: toggle, slider, stepper",
     {"element": "toggle switch in settings; slider for daily goal minutes; number stepper for minutes", "screen": "Settings; Log form"}),
    # G14
    ("Platform fallbacks in use: date picker, checkbox, radio group — pack defines no controls; native elements styled as fields per fallback/platform-controls",
     "controls: date, checkbox, radio",
     {"element": "date picker for the log entry; checkbox for reminders; radio buttons for frequency", "screen": "Log form; Settings"}),
]

for need, scope, ctx in gaps:
    r = subprocess.run(
        ["python3", "tools/da.py", "--pack", "packs/dominion", "gap-add",
         "--workspace", WS, "--need", need, "--scope", scope,
         "--context", json.dumps(ctx)],
        capture_output=True, text=True, cwd="/home/xrim/design-authority")
    if r.returncode != 0:
        print("FAIL:", need[:60], r.stderr[-300:]); sys.exit(1)
    out = json.loads(r.stdout)
    print("filed", out["id"])
print("total filed:", len(gaps) + 1)
