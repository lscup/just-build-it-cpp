# Chapter 06 Lab — Assign Letter Grades

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.5
- **Starting point:** The working Chapter 5 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Add named cutoffs: A `90`, B `80`, C `70`, and D `60`.
2. Use an `if / else if` chain from highest to lowest to assign a `char` letter grade; F is the default.
3. Display the percentage and letter grade together.
4. Keep the raw percentage policy from Chapter 4 for now.


## Verification

- Test `95`, `85`, `75`, `65`, and `55` percent.
- Test exactly `90.0` and just below `90.0`.
- A score above 100 still receives A and is not hidden.

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
git commit -m "Complete Chapter 6 Grade Calculator v0.5"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 6 checkpoint.
- The commit is pushed to GitHub.
