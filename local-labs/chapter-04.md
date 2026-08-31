# Chapter 04 Lab — Calculate Percentage and Bonus

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.3
- **Starting point:** The working Chapter 3 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Calculate `(points earned + bonus points) / points possible * 100.0` using floating-point arithmetic.
2. Guard against points possible being zero before dividing.
3. Display the percentage to one decimal place.
4. Keep the percentage uncapped in this checkpoint and document that policy in a comment.


## Verification

- `84 / 100` with `5` bonus reports `89.0%`.
- `10 / 10` with `5` bonus reports `150.0%`.
- Zero points possible produces an explanation instead of a division error.

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
git commit -m "Complete Chapter 4 Grade Calculator v0.3"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 4 checkpoint.
- The commit is pushed to GitHub.
