#!/usr/bin/env bash
# Copy the skills in ./skills into a skills folder. Default: ./.agent/skills
# Usage: bash install_skills.sh [target_dir]
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-.agent/skills}"
mkdir -p "$TARGET"
for d in "$HERE"/skills/*/; do
  name="$(basename "$d")"
  mkdir -p "$TARGET/$name"
  cp -R "$d". "$TARGET/$name/"
  echo "installed: $TARGET/$name"
done
echo "Done. Confirm this is the folder your Antigravity version reads skills from."
