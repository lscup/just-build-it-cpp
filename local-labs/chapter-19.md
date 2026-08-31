# Chapter 19 Lab — Split Classes into Files

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.6
- **Starting point:** The working Chapter 18 v2.5 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create one header and one implementation file for each class; keep `main.cpp` focused on application flow.
2. Add include guards and keep implementation details out of headers.
3. Create a `Gradebook` class that owns the roster, assignments, scale, and reporting operations.
4. Implement `operator<<` for Assignment, Student, GradeScale, and Gradebook using public accessors.
5. Add checked `at` access alongside unchecked `operator[]`.


## Verification

- Every source file builds as one program.
- Writing a Gradebook to the Terminal and to a file uses the same `operator<<`.
- Checked access rejects an invalid index.
- The Chapter 18 behavior is unchanged.

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
git commit -m "Complete Chapter 19 Grade Calculator v2.6"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 19 checkpoint.
- The commit is pushed to GitHub.
