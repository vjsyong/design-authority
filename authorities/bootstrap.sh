#!/usr/bin/env bash
# Clone (or update) every authority repo into authorities/.
# The repos are public; nothing here needs credentials.
set -e
cd "$(dirname "$0")"

REPOS=(
  authority-triage
  authority-triage-evolution
  authority-wink
  authority-leader
  authority-dominion
  authority-phantom
  authority-indaba
  authority-orbit
)

for r in "${REPOS[@]}"; do
  name="${r#authority-}"
  if [ -d "$name/.git" ]; then
    (cd "$name" && git pull -q --ff-only) || echo "warn: could not fast-forward $r"
  else
    git clone -q "https://github.com/vjsyong/$r.git" "$name" || echo "warn: $r not reachable yet"
  fi
done
echo "authorities: up to date"
