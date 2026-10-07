#!/usr/bin/env bash
# Synonym searches for UNDEFINED elements (mandate step 2).
cd /home/xrim/design-authority
out=examples/cadence2-dominion/searches
mkdir -p "$out"
run(){ echo "### $1" >> "$out/search-log.txt"; python3 tools/da.py --pack packs/dominion search "$1" >> "$out/search-log.txt" 2>&1; echo; }
: > "$out/search-log.txt"
# 05 modal
run "dialog"; run "overlay"; run "sheet"
# 06 toast
run "notice"; run "notification"; run "toast"
# 07 banner
run "banner"; run "callout"; run "summary"
# 08 empty
run "empty"; run "empty state"; run "placeholder"
# 10 spinner
run "spinner"; run "loading"; run "busy"
# 11 ring
run "progress ring"; run "gauge"; run "donut"
# 12 chart
run "chart"; run "graph"; run "bar chart"
# 13 heatmap
run "calendar"; run "heatmap"; run "grid"
# 14 sparkline
run "sparkline"; run "trend"; run "line chart"
# 15 streak
run "streak"; run "counter"; run "stat"
# 16 badge
run "badge"; run "achievement"; run "award"
# 17 status
run "status"; run "state label"; run "on track"
echo "done"
