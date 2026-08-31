# Chapter 21 Lab — Select Schemes with Polymorphism

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.1
- **Starting point:** The working Chapter 20 v3.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Make `GradingScheme::computePercentage` pure virtual and add a virtual destructor.
2. Have `Gradebook` own a base-class scheme pointer and delegate calculations through it.
3. Allow the user to switch schemes without restarting or re-entering data.
4. Add `WeightedDropLowest` as a third scheme without editing Student, Assignment, GradeScale, or report formatting.
5. Extend the Chapter 15 file format so category names and weights persist.


## Verification

- With Exam 1 at 90/100, Homework 1 at 10/10, Homework 2 at 5/10, and category weights of 50 and 30, the three schemes report 87.5%, 84.4%, and 93.8%.
- Switching schemes immediately recomputes reports.
- The grade calculation contains no type-selection branch.
- Saving and loading preserves categories and weights.

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
git commit -m "Complete Chapter 21 Grade Calculator v3.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 21 checkpoint.
- The commit is pushed to GitHub.
