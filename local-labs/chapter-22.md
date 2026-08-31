# Chapter 22 Lab — Replace Manual Ownership with Smart Pointers

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.2
- **Starting point:** The working Chapter 21 v3.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Confirm the correct v3.1 program switches schemes and exits normally.
2. Temporarily remove the manual delete in `setScheme` and observe the memory-safety failure using the available memory check; then restore it.
3. Replace the raw owning scheme pointer with `std::unique_ptr<GradingScheme>`.
4. Remove the manual destructor, manual delete, and explicitly deleted copy operations that unique ownership now handles.
5. Keep all grading behavior unchanged.


## Verification

- The intentional raw-pointer defect is detected by a memory-safety check.
- The final smart-pointer version reports no leak.
- Copying a Gradebook is rejected by the type system.
- All three grading schemes still produce the Chapter 21 results.

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

6. For the Chapter 22 memory checks, build and run with AddressSanitizer:

   ```bash
   g++ -std=c++17 -Wall -Wextra -fsanitize=address -g *.cpp -o gradecalc
   ./gradecalc
   ```

   Exercise scheme switching several times, quit normally, and read the
   sanitizer report.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 22 Grade Calculator v3.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 22 checkpoint.
- The commit is pushed to GitHub.
