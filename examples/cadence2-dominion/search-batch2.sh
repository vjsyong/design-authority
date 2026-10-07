#!/usr/bin/env bash
cd /home/xrim/design-authority
out=examples/cadence2-dominion/searches
run(){ echo "### $1" >> "$out/search-log.txt"; python3 tools/da.py --pack packs/dominion search "$1" >> "$out/search-log.txt" 2>&1; echo; }
# 19 icon
run "icon"; run "pictogram"; run "symbol"
# 25 select
run "select"; run "dropdown"
# 28 textarea
run "textarea"; run "multiline"
# 29 tabs
run "tabs"; run "tab"; run "segmented"
# 31 table
run "table"; run "ledger"; run "register"
# 32 pagination
run "pagination"; run "pager"
# 34 tag
run "tag"; run "chip"; run "category"
# 35 reorder
run "reorder"; run "sort"; run "drag"
# 37 wizard
run "wizard"; run "stepper"; run "onboarding"
# 38 export
run "export"; run "download"; run "csv"
# 39 dark
run "dark"; run "theme"
# 40 celebration
run "animation"; run "motion"; run "celebrate"
# 30 verify
run "bottom navigation"; run "navigation"
echo done
