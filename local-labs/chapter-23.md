# Chapter 23 Lab — Add Generic Statistics and an ID Index

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.3
- **Starting point:** The working Chapter 22 v3.2 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create header-only `Statistics<T>` with mean, median, minimum, maximum, and population standard deviation.
2. Add a `std::map` index from student ID to roster position and maintain it whenever the roster changes order.
3. Add `findById` using the index.
4. Replace the implicit Student ordering with a lambda at the sort call.
5. Add class statistics, letter-grade distribution, and assignment count by category.


## Verification

- `Statistics<double>` and `Statistics<int>` are both exercised.
- ID lookup works before and after sorting.
- A regression test fails if the index rebuild is removed.
- The reported statistics match a hand calculation.

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
git commit -m "Complete Chapter 23 Grade Calculator v3.3"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 23 checkpoint.
- The commit is pushed to GitHub.
