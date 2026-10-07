#!/usr/bin/env bash
# Batch-resolve the 42 elements against the dominion pack.
cd /home/xrim/design-authority
mkdir -p examples/cadence2-dominion/resolve-out
elems=(
"a primary button for the main action"
"a secondary button and a text link"
"delete a ritual permanently"
"a confirmation dialog before deleting"
"a modal with ritual details"
"a toast notification saying logged"
"a banner summarizing the week"
"an empty state when no rituals exist"
"an error message under the field"
"a loading spinner while saving"
"a circular progress ring of today's completion"
"a bar chart of weekly minutes"
"a calendar heatmap of the month"
"a tiny sparkline trend of the last week"
"a big streak counter"
"an achievement badge for seven days"
"a status label on track or slipping"
"a profile avatar photo"
"an icon for each ritual"
"a toggle switch in settings"
"a slider for daily goal minutes"
"a date picker for the log entry"
"a number stepper for minutes"
"a text field for the ritual name"
"a select for ritual category"
"a checkbox for reminders"
"radio buttons for frequency"
"a text area for notes"
"tabs for today history achievements"
"a bottom navigation bar on mobile"
"a table of logged entries"
"pagination for older entries"
"a search box to filter rituals"
"a small category tag"
"drag to reorder rituals"
"an undo button after deleting"
"a three-step onboarding wizard"
"export the data as csv"
"a dark mode theme"
"a celebration animation when checking off"
"an illustration in the empty state"
"upload a photo for the ritual"
)
i=0
for e in "${elems[@]}"; do
  i=$((i+1))
  n=$(printf "%02d" $i)
  python3 tools/da.py --pack packs/dominion resolve "$e" > "examples/cadence2-dominion/resolve-out/$n.txt" 2>&1
done
echo "done $i"
