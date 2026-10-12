# Lab Instruction Authoring

The Grade Calculator labs exist in three forms that must always say the same
thing:

- **Embedded labs** — the "Your StudySite Lab" section near the end of each
  chapter (`NN-*.md`). This is the canonical text.
- **`studysite-labs/chapter-NN.md`** — the embedded lab as a standalone page,
  headings promoted two levels (`###` → `#`, `####` → `##`, `#####` → `###`).
  This is the file copied into each student repository as
  `Instructions/ChapterNN_instructions.md`.
- **`local-labs/chapter-NN.md`** — the same lab for students working with a
  local C++17 toolchain: identical steps, with build commands in place of
  StudySite's **Run**, and `git` commands in place of **Save to GitHub**.

`chapters.json` holds summary metadata for every chapter (title, version,
starting point, what is built, verification items, commit message). It is
also the manifest the `lscup/grade-calculator` repository uses to generate its
own short-form lab pages, so keep its Chapter 13–24 entries in step with the
embedded labs.

## Chapters 18–24

The Chapter 18–24 labs walk students from one solution version to the next
(`v2.4` → `v4.0` in `lscup/grade-calculator`) with explicit find-and-replace
steps. Each lab has been checked mechanically: applying its steps to the
previous version's solution reproduces the next version's solution exactly,
and every Run checkpoint compiles with `g++ -std=c++17 -Wall -Wextra` and no
warnings. Any change to a solution version in `lscup/grade-calculator` must be
reflected in the matching lab, and any change to a lab's code boxes must match
the solution.
