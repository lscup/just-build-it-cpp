# Chapter 08 Lab — Round and Cap the Grade

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.7
- **Starting point:** The working Chapter 7 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Use `std::min` to cap the raw percentage at 100 when the named policy constant is enabled.
2. Use `std::round` to round once to one decimal place.
3. Use the same rounded value for both display and letter-grade selection.
4. Print a note when a raw percentage above 100 was capped.


## Verification

- `10 / 10` with `5` bonus reports `100.0%` and the cap note.
- `89.95 / 100` displays and grades from the same rounded value.
- Disabling the named cap policy reports the uncapped value.

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
git commit -m "Complete Chapter 8 Grade Calculator v0.7"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 8 checkpoint.
- The commit is pushed to GitHub.
