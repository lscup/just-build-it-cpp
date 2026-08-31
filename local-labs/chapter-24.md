# Chapter 24 Lab — Add Release-Safe Error Handling

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v4.0
- **Starting point:** The working Chapter 23 v3.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create a `GradebookError` hierarchy for invalid scales, invalid weights, malformed files, and lookup failures.
2. Throw meaningful exceptions at the point of failure and catch them where the program can explain the problem and continue.
3. Translate low-level conversion and file errors into messages that identify the affected operation.
4. Run the complete regression plan against the Chapter 24 code checkpoint.
5. Complete only the Chapter 24 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.


## Verification

- Invalid scales and invalid weights are refused without changing the working gradebook.
- Missing and malformed files produce clear messages instead of crashes.
- Points-based, weighted, and weighted-drop-lowest grading all work.
- Save/load, lookup, statistics, and reports all work.
- The repository contains the Chapter 12 foundation plus the completed Chapter 13–24 code checkpoints.

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
git commit -m "Complete Chapter 24 Grade Calculator v4.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 24 checkpoint.
- The commit is pushed to GitHub.
