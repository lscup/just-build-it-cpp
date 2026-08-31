# Chapter 14 Lab — Replace Parallel Arrays with Structs

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.1
- **Starting point:** The working Chapter 13 v2.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create `GradeTier`, `Assignment`, and `Student` structs.
2. Replace parallel arrays and vectors with vectors of the appropriate record type.
3. Add a `Course` struct that owns the course name, assignments, students, and grade scale.
4. Pass a single `Course` object to report functions instead of unrelated containers.
5. Preserve all v2.0 behavior.


## Verification

- Student names cannot be reordered separately from their scores.
- A grade letter cannot exist without its cutoff.
- The same input produces the same report as Chapter 13.
- The program builds without warnings.

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
git commit -m "Complete Chapter 14 Grade Calculator v2.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 14 checkpoint.
- The commit is pushed to GitHub.
