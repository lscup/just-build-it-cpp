# Chapter 17 Lab — Sort and Search the Roster

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.4
- **Starting point:** The working Chapter 16 v2.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add roster sorting by student ID, name, and percentage.
2. Add linear search by student ID.
3. Add binary search by student ID and ensure its data is sorted by ID first.
4. Report the comparison count for each search.
5. Add ordering by letter grade and then name.


## Verification

- Every sort order is correct for at least five students.
- Linear and binary search find the same existing student.
- Both searches report not found for a missing ID.
- The binary-search precondition is enforced instead of assumed.

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
git commit -m "Complete Chapter 17 Grade Calculator v2.4"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 17 checkpoint.
- The commit is pushed to GitHub.
