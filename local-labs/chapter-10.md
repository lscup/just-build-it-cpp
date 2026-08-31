# Chapter 10 Lab — Organize Reusable Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.1
- **Starting point:** The working Chapter 9 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Move reusable declarations to `gradelib.h` and definitions to `gradelib.cpp`; keep application flow in `main.cpp`.
2. Add an include guard to `gradelib.h`.
3. Add validated numeric input that recovers after invalid text.
4. Pass output values by reference where a function must update the caller.
5. Add `readInRange` and use it to keep points possible between `0` and `1000`.


## Verification

- All source files build together.
- Typing `abc` for a number does not trap the program in a loop or crash it.
- The existing menu and grade calculations still work.

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
git commit -m "Complete Chapter 10 Grade Calculator v1.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 10 checkpoint.
- The commit is pushed to GitHub.
