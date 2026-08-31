# Chapter 15 Lab — Save and Load the Gradebook

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.2
- **Starting point:** The working Chapter 14 v2.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add file-stream support that saves the grade scale, assignments, and students to `gradebook.csv`.
2. Load `gradebook.csv` at startup when it exists.
3. Parse into temporary data and replace the active gradebook only after the complete file is valid.
4. Create `file-format.md` documenting every record type, field order, and the restriction on commas in text fields.
5. Add a menu option that saves to a different filename.


## Verification

- A save-then-load round trip reproduces the same gradebook.
- A missing file is handled without a crash.
- A nonnumeric field, truncated student row, unknown tag, and missing grade tiers are each rejected.
- A failed load does not destroy the active in-memory data.

## Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Edit the current project files in your local editor.
3. Build every source file:

   ```bash
   g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
   ```

4. Fix every compiler error and warning.
5. Run the program and complete the verification list:

   ```bash
   ./gradecalc
   ```

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 15 Grade Calculator v2.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 15 checkpoint.
- The commit is pushed to GitHub.
