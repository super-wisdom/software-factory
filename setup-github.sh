#!/usr/bin/env bash
# Creates github.com/super-wisdom/software-factory (public) and pushes this scaffold.
# Run from inside this folder, on a machine where the GitHub CLI (gh) is logged in.
set -euo pipefail

ORG="super-wisdom"
REPO="software-factory"
VISIBILITY="public"

echo "==> Software Factory :: GitHub setup"

command -v git >/dev/null || { echo "ERROR: git not found."; exit 1; }
command -v gh  >/dev/null || { echo "ERROR: GitHub CLI not found -> https://cli.github.com"; exit 1; }

if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: not logged in. Run:  gh auth login"; exit 1
fi

cd "$(dirname "$0")"

if [ ! -d .git ]; then
  git init -q
  git branch -M main
fi

git add -A
git commit -qm "chore: initialize software factory scaffold" || echo "(nothing new to commit)"

if gh repo view "$ORG/$REPO" >/dev/null 2>&1; then
  echo "==> $ORG/$REPO already exists; wiring remote and pushing."
  git remote add origin "https://github.com/$ORG/$REPO.git" 2>/dev/null || true
  git push -u origin main
else
  echo "==> Creating $VISIBILITY repo $ORG/$REPO and pushing."
  gh repo create "$ORG/$REPO" --"$VISIBILITY" --source=. --remote=origin --push
fi

echo "==> Done -> https://github.com/$ORG/$REPO"
