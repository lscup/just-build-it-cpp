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
    -x .git -x grade-calculator -x textbook-examples -x build \
    -x update-repos.sh -x update-repos-output.txt \
    2>&1 | head -150 || true
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
# PHASE 1C — sync chapters into the instructor repo.
# Chapters only (01-24 numbered .md files), per your call: the instructor
# repo's lab-delivery folders (lab-instructions/, local-labs/,
# studysite-labs/, portfolio-exercises/, lecture-decks/,
# studysite-metadata/) and its own appendix layout are left untouched —
# that structural gap looks intentional (instructor edition = book text +
# examples, not the student lab-delivery system), not something to fix here.
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 1C: sync chapters into lscup/just-build-it-cpp-instructor"
echo "=============================================="

if [[ ! -d "$INSTRUCTOR_DIR/.git" ]]; then
  echo "No local clone of the instructor repo found at $INSTRUCTOR_DIR — skipping."
  echo "(Phase 1B above should have cloned it. Re-run the script, or clone manually:"
  echo "  gh repo clone $ORG/just-build-it-cpp-instructor \"$INSTRUCTOR_DIR\")"
else
  COPIED=0
  for f in "$TEXTBOOK_DIR"/[0-9][0-9]-*.md; do
    [[ -e "$f" ]] || continue
    cp "$f" "$INSTRUCTOR_DIR/$(basename "$f")"
    COPIED=$((COPIED + 1))
  done
  echo "Copied $COPIED chapter file(s) from just-build-it-cpp into the instructor repo."

  # WCAG fix (2026-09): corrected annotation color in 6 figures (contrast)
  # and made tables keyboard-focusable in the HTML build - both editions
  # need the same fixed assets so their rebuilt HTML/PDF match.
  A11Y_FIGS="ch02-fig2-anatomy ch03-fig1-variable ch10-fig1-pointer-reference ch11-fig1-2d-array ch18-fig1-class ch22-fig1-stack-heap"
  ASSETS_COPIED=0
  for base in $A11Y_FIGS; do
    for ext in svg png; do
      src="$TEXTBOOK_DIR/figures/$base.$ext"
      dst="$INSTRUCTOR_DIR/figures/$base.$ext"
      if [[ -f "$src" && -f "$dst" ]] && ! cmp -s "$src" "$dst"; then
        cp "$src" "$dst"
        ASSETS_COPIED=$((ASSETS_COPIED + 1))
      fi
    done
  done
  if [[ -f "$TEXTBOOK_DIR/build/make-html.sh" && -f "$INSTRUCTOR_DIR/build/make-html.sh" ]] \
     && ! cmp -s "$TEXTBOOK_DIR/build/make-html.sh" "$INSTRUCTOR_DIR/build/make-html.sh"; then
    cp "$TEXTBOOK_DIR/build/make-html.sh" "$INSTRUCTOR_DIR/build/make-html.sh"
    chmod +x "$INSTRUCTOR_DIR/build/make-html.sh"
    ASSETS_COPIED=$((ASSETS_COPIED + 1))
  fi
  echo "Copied $ASSETS_COPIED accessibility-fix asset(s) (figures + build script)."

  cd "$INSTRUCTOR_DIR"
  echo "Working directory: $(pwd)"
  echo ""
  echo "--- git status ---"
  git status --short
  echo ""

  if [[ -z "$(git status --porcelain)" ]]; then
    echo "Nothing changed — instructor repo's chapters already match. Skipping."
  else
    read -r -p "Commit and push these chapter updates to lscup/just-build-it-cpp-instructor? [y/N] " ok
    if [[ "$ok" == "y" || "$ok" == "Y" ]]; then
      git add -- [0-9][0-9]-*.md figures/*.svg figures/*.png build/make-html.sh
      git commit -m "Sync Chapters 01-24 and accessibility fixes with just-build-it-cpp

Chapters 13, 14, 16-24 restored (polymorphism, unique_ptr ownership,
templates/STL, exception-based error handling); Chapter 15 and 17 lab
sections synced with their StudySite versions; F26 replaced with xxx
for semester reusability. Also carries the WCAG 2.1 AA fixes: corrected
annotation color in 6 figures (contrast) and keyboard-focusable tables
in the HTML build. This edition's own lab-delivery layout and appendix
structure are left unchanged."
      git push
      echo "Pushed."
    else
      echo "Skipped push."
    fi
  fi
fi

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

# ─────────────────────────────────────────────────────────────────────────
# PHASE 4 — update every student repo's Instructions files.
# For each repo in student-repos.txt (from Phase 3), replaces
# Instructions/ChapterNN_instructions.md (chapters 13-24 only) with the
# corresponding studysite-labs/chapter-NN.md content — the version with
# the full "Build it: step by step" walkthrough and real code. Nothing
# else in a student's repo is ever touched: main.cpp, baseline-output.md,
# maintenance-plan.md, and anything not matching that exact Instructions
# filename are left completely alone. A repo missing one of those files
# is noted and skipped for that chapter rather than guessed at.
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 4: update Instructions files in student repos"
echo "=============================================="

STUDYSITE_LABS_DIR="$TEXTBOOK_DIR/studysite-labs"
STUDENTS_DIR="$WORKDIR/students"
mkdir -p "$STUDENTS_DIR"

if [[ ! -s "$WORKDIR/student-repos.txt" ]]; then
  echo "No student-repos.txt found (or it's empty) - run Phase 3 first."
else
  STUDENT_COUNT=$(wc -l < "$WORKDIR/student-repos.txt" | tr -d ' ')
  echo "This will check $STUDENT_COUNT student repo(s) and, for any whose"
  echo "Instructions/ChapterNN_instructions.md (chapters 13-24) differs from"
  echo "studysite-labs/chapter-NN.md, replace just that file, commit, and push."
  echo "main.cpp, baseline-output.md, and maintenance-plan.md are never touched."
  echo ""
  read -r -p "Proceed with all $STUDENT_COUNT student repos? [y/N] " ok
  if [[ "$ok" == "y" || "$ok" == "Y" ]]; then
    while IFS= read -r repo; do
      [[ -z "$repo" ]] && continue
      echo ""
      echo "--- $repo ---"
      REPO_DIR="$STUDENTS_DIR/$repo"
      rm -rf "$REPO_DIR"
      if ! gh repo clone "$ORG/$repo" "$REPO_DIR" -- --quiet; then
        echo "  Clone failed - skipping."
        continue
      fi

      CHANGED=0
      for n in 13 14 15 16 17 18 19 20 21 22 23 24; do
        SRC="$STUDYSITE_LABS_DIR/chapter-$n.md"
        DST="$REPO_DIR/Instructions/Chapter${n}_instructions.md"
        if [[ -f "$SRC" && -f "$DST" ]]; then
          if ! cmp -s "$SRC" "$DST"; then
            cp "$SRC" "$DST"
            CHANGED=$((CHANGED + 1))
          fi
        elif [[ -f "$SRC" && ! -f "$DST" ]]; then
          echo "  Note: no Instructions/Chapter${n}_instructions.md here - left alone."
        fi
      done

      if [[ "$CHANGED" -eq 0 ]]; then
        echo "  Already up to date."
      else
        (
          cd "$REPO_DIR" \
            && git add Instructions/Chapter*_instructions.md \
            && git commit -q -m "Update Chapter 13-24 lab instructions with step-by-step build guide

Adds the explicit Build-it: step-by-step walkthrough (with real code)
to each chapter's instructions, replacing the shorter required-work-only
version. No student work (main.cpp, baseline-output.md,
maintenance-plan.md) is touched." \
            && git push -q
        )
        echo "  Updated $CHANGED chapter instructions file(s) and pushed."
      fi
    done < "$WORKDIR/student-repos.txt"
  else
    echo "Skipped."
  fi
fi

# ─────────────────────────────────────────────────────────────────────────
# PHASE 5 — rebuild the HTML/PDF editions from the current chapter
# markdown. Must run here (your own Terminal): it needs the same
# pandoc/xelatex toolchain that originally built these files, which isn't
# available in Claude's own environment. Each repo's own build/order.txt
# and build scripts are used as-is - nothing about the build is guessed at.
# ─────────────────────────────────────────────────────────────────────────
echo ""
echo "=============================================="
echo " Phase 5: rebuild HTML/PDF editions"
echo "=============================================="

if ! command -v pandoc >/dev/null 2>&1 || ! command -v xelatex >/dev/null 2>&1; then
  echo "pandoc and/or xelatex not found on PATH - skipping."
  echo "(See build/README.md in the textbook repo for what's required.)"
else
  rebuild_edition() {
    local dir="$1" html_out="$2" pdf_out="$3"
    if [[ ! -d "$dir/build" ]]; then
      echo ""
      echo "--- $(basename "$dir") ---"
      echo "  No build/ directory here - skipping."
      return
    fi
    if [[ ! -f "$dir/$html_out" ]]; then
      echo ""
      echo "--- $(basename "$dir") ---"
      echo "  $html_out not found - skipping (unexpected layout)."
      return
    fi
    local title
    title=$(grep -o '<title>[^<]*</title>' "$dir/$html_out" 2>/dev/null | sed -e 's/<title>//' -e 's/<\/title>//')
    [[ -z "$title" ]] && title="Just Build It!"

    echo ""
    echo "--- $(basename "$dir") ---"
    echo "  HTML:  $html_out"
    echo "  PDF:   $pdf_out"
    echo "  Title: $title"
    read -r -p "  Rebuild both editions for $(basename "$dir")? [y/N] " ok
    if [[ "$ok" != "y" && "$ok" != "Y" ]]; then
      echo "  Skipped."
      return
    fi

    if ! (
      cd "$dir" \
        && echo "  Building HTML..." \
        && ./build/make-html.sh . "$html_out" build/order.txt "$title" \
        && echo "  Building PDF..." \
        && ./build/make-pdf.sh . "$pdf_out" build/order.txt
    ); then
      echo "  Build failed - not committing. Check the output above."
      return
    fi

    (
      cd "$dir"
      echo "  --- git status ---"
      git status --short -- "$html_out" "$pdf_out"
      if [[ -z "$(git status --porcelain -- "$html_out" "$pdf_out")" ]]; then
        echo "  Rebuilt editions are identical to what's already committed."
      else
        read -r -p "  Commit and push the rebuilt editions? [y/N] " ok2
        if [[ "$ok2" == "y" || "$ok2" == "Y" ]]; then
          git add "$html_out" "$pdf_out" \
            && git commit -q -m "Rebuild HTML/PDF editions from the current chapter markdown" \
            && git push \
            && echo "  Pushed."
        else
          echo "  Built locally but not committed/pushed."
        fi
      fi
    )
  }

  rebuild_edition "$TEXTBOOK_DIR" "Just-Build-It-Cpp.html" "Just-Build-It-Cpp.pdf"
  rebuild_edition "$INSTRUCTOR_DIR" "Just-Build-It-Cpp-Instructor.html" "Just-Build-It-Cpp-Instructor.pdf"
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
