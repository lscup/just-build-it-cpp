# Chapter 05 Lab — Design the Interface

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.4
- **Starting point:** The working Chapter 4 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Create `design.md` containing the program purpose, inputs, processing, outputs, pseudocode, and a test table.
2. Keep the weighted-grading scope statement from `requirements.md` unchanged.
3. Redesign prompts so each states the expected value or constraint.
4. Print a labeled, aligned report and explain the zero-points-possible case.
5. Print a note that bonus points are added to earned points, not possible points.


## Verification

- The calculation still matches Chapter 4.
- Labels are readable and aligned.
- `design.md` matches the program that will be built through Chapter 12.

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
git commit -m "Complete Chapter 5 Grade Calculator v0.4"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 5 checkpoint.
- The commit is pushed to GitHub.
