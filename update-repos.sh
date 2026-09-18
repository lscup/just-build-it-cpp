#!/usr/bin/env bash
# update-repos.sh — Push the Chapter 13-24 restoration to GitHub.
#
# Run this in your own Terminal on your Mac (not through Claude) — it uses
# whatever git/gh login you already have. Three phases:
#   1) commit + push the textbook repo (lscup/just-build-it-cpp)
#   2) commit + push the grade-calculator reference-solution repo (lscup/grade-calculator)
#   3) find every student repo (COSC1437F26-Grade-Calculator-*) and show what's
#      inside one of them, so Claude can write the exact Phase 4 step that
#      updates the Instructions files across all of them — nothing is
#      touched in student repos by this script; it only looks.
#
# Safe to re-run: every push asks for confirmation first, and shows you
# `git status --short` / `git diff` so you can see exactly what would move.

set -euo pipefail

TEXTBOOK_DIR="$HOME/Documents/LSC/Cpp Textbook"
GRADE_CALC_DIR="$TEXTBOOK_DIR/grade-calculator"
ORG="lscup"
STUDENT_REPO_PREFIX="COSC1437F26-Grade-Calculator-"
WORKDIR="$HOME/Documents/LSC/_student-repo-updates"

echo "=============================================="
echo " Preflight checks"
echo "=============================================="

if ! command -v gh >/dev/null 2>&1; then
  echo "ERROR: GitHub CLI ('gh') not found."
  echo "Install it with:  brew install gh"
  echo "Then:             gh auth login"
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "ERROR: gh is installed but not logged in."
  echo "Run:  gh auth login"
  exit 1
fi

echo "gh is authenticated as:"
gh api user -q '.login'
echo ""

# ─────────────────────────────────────────────────────────────────────────
# PHASE 1 — textbook repo
# ─────────────────────────────────────────────────────────────────────────
echo "=============================================="
echo " Phase 1: lscup/just-build-it-cpp"
echo "=============================================="

if [[ ! -d "$TEXTBOOK_DIR/.git" ]]; then
  echo "ERROR: $TEXTBOOK_DIR is not a git repo (no .git found). Skipping Phase 1."
else
  cd "$TEXTBOOK_DIR"
  echo "Working directory: $(pwd)"
  echo ""
  echo "--- git status ---"
  git status --short
  echo ""

  if [[ -z "$(git status --porcelain)" ]]; then
    echo "Nothing to commit here — already clean. Skipping."
  else
    read -r -p "Commit and push these changes to lscup/just-build-it-cpp? [y/N] " ok
    if [[ "$ok" == "y" || "$ok" == "Y" ]]; then
      git add -A
      git commit -m "Restore Chapters 13-24 with verified C++ and explicit step-by-step labs

- Chapters 13, 14, 16-24: restored polymorphism, unique_ptr ownership,
  templates/STL, and exception-based error handling onto the reference
  solutions, with persistence/regression-tests/sort-search carried forward
  each chapter instead of silently dropped
- Chapter 24 (v4.0): GradebookError hierarchy, atomic load (build-fresh-
  then-move-swap), corrected chooseScheme(), 26/26 regression checks
- Replaced F26 with xxx throughout student-facing files so they are
  reusable across semesters
- Synced Chapter 15 and 17 embedded textbook lab sections with their
  already-correct standalone studysite-labs versions (missing Build-it
  step-by-step walkthroughs)"
      git push origin main
      echo "Pushed."
    else
      echo "Skipped push (changes are staged/committed locally only if you ran git add/commit yourself)."
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# PHASE 1B — discover the instructor-edition repo (read-only — nothing is
# pushed here). There is no local clone of just-build-it-cpp-instructor
# anywhere Claude could find, and it's private (can't even be read
# anonymously), so this phase clones/pulls it into a scratch folder and
# shows what's actually different from just-build-it-cpp. Paste that
# output back to Claude so the real sync step can be written correctly
# instead of guessing at what "instructor edition" contains.
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 1B: lscup/just-build-it-cpp-instructor (discovery only)"
echo "=============================================="

INSTRUCTOR_DIR="$WORKDIR/just-build-it-cpp-instructor"
mkdir -p "$WORKDIR"

if gh repo view "$ORG/just-build-it-cpp-instructor" >/dev/null 2>&1; then
  if [[ -d "$INSTRUCTOR_DIR/.git" ]]; then
    echo "Already cloned at $INSTRUCTOR_DIR — pulling latest."
    (cd "$INSTRUCTOR_DIR" && git pull --ff-only)
  else
    echo "Cloning lscup/just-build-it-cpp-instructor to $INSTRUCTOR_DIR ..."
    rm -rf "$INSTRUCTOR_DIR"
    gh repo clone "$ORG/just-build-it-cpp-instructor" "$INSTRUCTOR_DIR" -- --quiet
  fi

  echo ""
  echo "--- File tree (excluding .git) ---"
  find "$INSTRUCTOR_DIR" -not -path '*/.git*' -type f | sed "s|$INSTRUCTOR_DIR/||" | sort

  echo ""
  echo "--- Diff vs just-build-it-cpp (names only; grade-calculator/textbook-examples/build excluded) ---"
  diff -rq "$TEXTBOOK_DIR" "$INSTRUCTOR_DIR" \
    -x .git -x grade-calculator -x textbook-examples -x build -x update-repos.sh \
    2>&1 | head -150
else
  echo "Could not view $ORG/just-build-it-cpp-instructor with gh — check access/name."
fi

echo ""
echo "--- Checking whether separate 'public' or 'html' repos exist under $ORG ---"
for name in just-build-it-cpp-public just-build-it-cpp-html just-build-it-cpp-student; do
  if gh repo view "$ORG/$name" >/dev/null 2>&1; then
    echo "  FOUND: $ORG/$name"
  else
    echo "  not found: $ORG/$name"
  fi
done

# ─────────────────────────────────────────────────────────────────────────
# PHASE 2 — grade-calculator reference-solution repo
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 2: lscup/grade-calculator"
echo "=============================================="

if [[ ! -d "$GRADE_CALC_DIR/.git" ]]; then
  echo "ERROR: $GRADE_CALC_DIR is not a git repo (no .git found). Skipping Phase 2."
else
  cd "$GRADE_CALC_DIR"
  echo "Working directory: $(pwd)"
  echo ""
  echo "--- git status ---"
  git status --short
  echo ""

  if [[ -z "$(git status --porcelain)" ]]; then
    echo "Nothing to commit here — already clean. Skipping."
  else
    read -r -p "Commit and push these changes to lscup/grade-calculator? [y/N] " ok
    if [[ "$ok" == "y" || "$ok" == "Y" ]]; then
      git add -A
      git commit -m "Add v4.0 (Chapter 24): exceptions, atomic persistence, regression tests

GradebookError hierarchy (InvalidScaleError, WeightSumError,
FileFormatError); GradeScale and Weighted refuse invalid input instead of
silently repairing it; persistence moved to free functions with an
atomic build-fresh-then-move-swap load so a malformed file leaves the
caller's Gradebook completely untouched; 26/26 regression checks
(D1-D13), verified leak-free under AddressSanitizer."
      git push origin main
      echo "Pushed."
    else
      echo "Skipped push."
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# PHASE 3 — discover student repos (read-only, nothing is changed)
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 3: discovering student repos"
echo "=============================================="

mkdir -p "$WORKDIR"
echo "Listing ${ORG} repos matching '${STUDENT_REPO_PREFIX}*' ..."
gh repo list "$ORG" --limit 1000 --json name -q '.[].name' \
  | grep "^${STUDENT_REPO_PREFIX}" | sort > "$WORKDIR/student-repos.txt" || true

COUNT=$(wc -l < "$WORKDIR/student-repos.txt" | tr -d ' ')
echo "Found $COUNT matching repo(s)."
echo "Full list saved to: $WORKDIR/student-repos.txt"
echo ""

if [[ "$COUNT" -eq 0 ]]; then
  echo "No repos matched '${STUDENT_REPO_PREFIX}*' in ${ORG}."
  echo "Either the prefix is different, or 'gh' doesn't have visibility into"
  echo "that org's private repos yet (check: gh auth status --show-token"
  echo "should list 'repo' and 'read:org' scopes)."
else
  FIRST=$(head -1 "$WORKDIR/student-repos.txt")
  echo "Cloning one sample repo to inspect its layout: $FIRST"
  rm -rf "$WORKDIR/_sample"
  gh repo clone "$ORG/$FIRST" "$WORKDIR/_sample" -- --depth 1 --quiet

  echo ""
  echo "--- Full file tree of $FIRST (excluding .git) ---"
  find "$WORKDIR/_sample" -not -path '*/.git*' -type f | sed "s|$WORKDIR/_sample/||" | sort

  echo ""
  echo "--- Contents of any Instructions/README-like files found ---"
  find "$WORKDIR/_sample" -not -path '*/.git*' -type f \( -iname "*instruction*" -o -iname "readme*" \) | while read -r f; do
    echo ""
    echo "===== $f ====="
    head -40 "$f"
    echo "... (truncated, see file directly for full contents)"
  done
fi

echo ""
echo "=============================================="
echo " Done. Paste back to Claude:"
echo "   - The Phase 1B file tree + diff output (so the instructor-repo"
echo "     sync step can be written correctly instead of guessed at)"
echo "   - The Phase 3 output (or the contents of $WORKDIR/student-repos.txt"
echo "     and $WORKDIR/_sample) so Phase 4, the real Instructions-file"
echo "     update across all student repos, can be written to match."
echo "=============================================="
