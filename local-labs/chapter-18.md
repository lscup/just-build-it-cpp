# Chapter 18 Lab — Introduce Classes and Invariants

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.5
- **Starting point:** The working Chapter 17 v2.4 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Convert `Assignment`, `Student`, and `GradeScale` from structs to classes.
2. Make data members private and expose only the constructors, accessors, and operations callers need.
3. Give `GradeScale` an invariant: cutoffs descend, no cutoff is negative, and the lowest tier is 0.
4. Add `Student::letterGrade(const GradeScale&) const`.
5. Preserve the Chapter 17 features and output.


## Verification

- Code outside a class cannot modify its private data directly.
- Ascending, negative, empty, and no-zero grade scales are handled by the class.
- The same input produces the same report as Chapter 17.
- All accessors that do not change an object are `const`.

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
git commit -m "Complete Chapter 18 Grade Calculator v2.5"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 18 checkpoint.
- The commit is pushed to GitHub.
