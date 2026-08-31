# Chapter 11 Lab — Build a Class Roster and Custom Scale

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.2
- **Starting point:** The working Chapter 10 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Store up to 40 students and their scores in arrays.
2. Store grade letters and cutoffs as parallel arrays entered by the user.
3. Reject a cutoff that is not lower than the previous cutoff and ensure the scale reaches `0`.
4. Replace the fixed letter-grade chain with a loop over the scale data.
5. Display every student's grade, the class average, and highest and lowest course percentage.


## Verification

- Default and custom scales can give different letters for the same score.
- A pass/fail scale works without code changes.
- An out-of-order cutoff is rejected.
- The 40-student limit is handled explicitly.

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
git commit -m "Complete Chapter 11 Grade Calculator v1.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 11 checkpoint.
- The commit is pushed to GitHub.
