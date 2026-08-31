# Chapter 03 Lab — Store an Assignment

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.2
- **Starting point:** The working Chapter 2 `main.cpp`.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Prompt for a student name and assignment name using `std::string` and `std::getline`.
2. Prompt for points earned and points possible using `double` variables.
3. Add a `double` bonus-points variable and a `const double` A cutoff of `90.0`.
4. Print a labeled summary containing every value. Do not calculate the percentage yet.


## Verification

- Names containing spaces are read completely.
- Decimal point values are accepted.
- The summary echoes all entered data and the A cutoff.

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
git commit -m "Complete Chapter 3 Grade Calculator v0.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 3 checkpoint.
- The commit is pushed to GitHub.
