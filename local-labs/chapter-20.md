# Chapter 20 Lab — Add Weighted Grading with Inheritance

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.0
- **Starting point:** The working Chapter 19 v2.6 multi-file program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add an assignment category while preserving existing constructor calls with defaults.
2. Create a `GradingScheme` base class and `PointsBased` and `Weighted` derived classes.
3. Move common final rounding and capping into the base class.
4. Validate that category weights total 100 within a floating-point tolerance.
5. Let the user choose the grading scheme at startup.
6. Do not penalize a student for a weighted category with no assignments.


## Verification

- The existing points-based examples still produce the same grades.
- A 90/100 exam at weight 50 and 10/10 homework at weight 30 reports 93.8% when only those categories contain work.
- Weights totaling 80% are rejected.
- Unchanged classes and report code remain unchanged.

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
git commit -m "Complete Chapter 20 Grade Calculator v3.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 20 checkpoint.
- The commit is pushed to GitHub.
