# Chapter 16 Lab — Debug and Add Regression Tests

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.3
- **Starting point:** The working Chapter 15 v2.2 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Use the three supplied defect descriptions: change a grade cutoff comparison from `>=` to `>`; add bonus points to possible points; and allow a grade-scale loop to read index `size()`.
2. Observe each failure, then restore the correct code one defect at a time.
3. Add a small regression-test harness and a menu option that runs it.
4. Add tests for exact cutoffs, zero percent, below-scale input, bonus arithmetic, zero possible points, an empty roster, and a capped percentage.
5. Create `defect-reports.md` recording symptoms, reproduction steps, cause, correction, and regression test for all three defects.


## Verification

- All seeded defects fail at least one test before correction.
- All regression tests pass after correction.
- Ordinary input and boundary input both produce correct results.
- The normal Grade Calculator menu still works.

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
git commit -m "Complete Chapter 16 Grade Calculator v2.3"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 16 checkpoint.
- The commit is pushed to GitHub.
