# Chapter 12 Lab — Complete the Dynamic Roster

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.3
- **Starting point:** The working Chapter 11 program and the Chapter 5 design document.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Replace fixed student, assignment, score, and grade-scale arrays with `std::vector`.
2. Allow any number of assignments and students.
3. Add the drop-lowest option. Remove both earned and possible points for the selected assignment.
4. Preserve validated input, custom grade scales, rounding, capping, and class reporting from the earlier checkpoints.
5. Keep the weighted-grading scope statement unchanged. Weighted grading belongs to COSC 1437.
6. Complete only the Chapter 12 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.


## Verification

- The program handles more than 40 students.
- Drop-lowest arithmetic matches a hand calculation.
- No-student, no-assignment, zero-possible-points, invalid-scale, cutoff-boundary, bonus, and invalid-numeric-input cases behave correctly.
- The repository contains the complete working v1.3 code checkpoint and the project documents created in earlier chapters.

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
git commit -m "Complete Chapter 12 Grade Calculator v1.3"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 12 checkpoint.
- The commit is pushed to GitHub.
