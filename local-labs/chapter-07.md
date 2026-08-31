# Chapter 07 Lab — Process Multiple Assignments

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.6
- **Starting point:** The working Chapter 6 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Use `done` as the sentinel for assignment entry.
2. Maintain total earned, total possible, assignment count, and bonus-assignment count.
3. Display a running percentage after each assignment.
4. After the sentinel, display the final course percentage and letter grade.
5. Handle no assignments and all-zero-point assignments without dividing by zero.


## Verification

- Three assignments produce correct running totals.
- Entering `done` immediately reports no assignments.
- Names still work after numeric input; no `getline` is skipped.

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
git commit -m "Complete Chapter 7 Grade Calculator v0.6"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 7 checkpoint.
- The commit is pushed to GitHub.
