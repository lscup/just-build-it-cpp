# Chapter 09 Lab — Rebuild with Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.0
- **Starting point:** The working Chapter 8 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Refactor into focused functions for reading an assignment, computing a percentage, assigning a letter, and printing a report.
2. Add a menu loop with options to add an assignment, view the report, and quit.
3. Use parameters and return values instead of duplicating calculations.
4. Preserve Chapter 8 behavior while changing the program structure.


## Verification

- Every menu option works, including an invalid choice.
- The same inputs produce the same grade as Chapter 8.
- Boundary tests for `90.0`, `89.9`, `80.0`, `60.0`, `59.9`, and `0.0` pass.

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
git commit -m "Complete Chapter 9 Grade Calculator v1.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 9 checkpoint.
- The commit is pushed to GitHub.
