# Chapter 02 Lab — Hello, Gradebook

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.1
- **Starting point:** The Chapter 1 repository containing `README.md` and `requirements.md`.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Create `main.cpp` with the required C++ program structure: include `<iostream>`, define `int main()`, and return `0`.
2. Print a Grade Calculator banner, `COSC 1436`, and your name.
3. Keep the output plain text and make the program exit normally.


## Verification

- The program builds without warnings.
- The banner, course, and student name appear exactly once.
- The program reaches a normal exit.

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
git commit -m "Complete Chapter 2 Grade Calculator v0.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 2 checkpoint.
- The commit is pushed to GitHub.
