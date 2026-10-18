# Chapter 11 Lab — Build a Class Roster

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.2
- **Starting point:** Your committed Chapter 10 v1.1 program (three files, validated input).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Two limits fall in this chapter. The program has only ever held **one**
student, and its grade scale has only ever been the one written into the code.
Arrays fix the first: a 2D array stores every student's score on every
assignment. A **table** of cutoffs and letters fixes the second, and that is
the chapter's real idea — the `if`/`else if` chain from Chapter 6 becomes a
loop over data, so changing the grading scheme no longer means changing code.

By the end you will have:

1. `MAX_TIERS` in the library, and three new library functions:
   `useDefaultScale`, `readGradeScale`, and `letterFor`.
2. A grade scale held in **parallel arrays** — `cutoffs[i]` and `letters[i]`
   describe the same tier — that the user can define at run time, with
   validation that the cutoffs descend.
3. `assignLetterGrade` and the four `*_CUTOFF` constants **gone**, replaced by
   the table.
4. A roster in `main.cpp`: a 2D array of earned points, parallel arrays of
   student and assignment names, and a class report with per-student grades,
   a class average, and per-assignment averages.

> **Limitation, by design:** the arrays are fixed size — 40 students, 20
> assignments, 12 tiers. Chapter 12 removes all three limits with
> `std::vector`.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradelib.h` | Edit (Steps 1-3) |
| `gradelib.cpp` | Edit (Steps 4-6) |
| `main.cpp` | Edit (Steps 7-8) |

When you are finished your project still has **three** files.

## How to use these steps

This lab is a guided exercise, not a test. Each step tells you **which file**
to open, shows the **exact code to find**, and shows the **exact code to put in
its place**. Work through the steps in order and copy the code from the boxes
rather than retyping it where you can.

- A **find** box shows code exactly as it appears in your program at the end
  of the previous chapter. Use the editor's search to locate it. If you cannot
  find it, your program differs from the previous checkpoint — compare it with
  your last commit on GitHub before going further.
- A **▶ Build checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.

## Optional local workflow

Build and run this chapter's program with the command for your platform:

**macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):

```bash
clang++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
./gradecalc
```

**Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):

```powershell
g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc.exe
.\gradecalc.exe
```

The ▶ Build checkpoints below use `g++ -std=c++17 -Wall -Wextra *.cpp -o
gradecalc`, which works as written on macOS, Linux, and WSL. On Windows, use
the Windows command above instead.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Continue the existing project in your local editor. Keep all three files open, and build and run at the ▶ Build checkpoint.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Step 1 — Replace the fixed cutoffs with a tier limit

In `gradelib.h`, update the first comment line:

```cpp
// gradelib.h - Grade Calculator v1.1 - Chapter 10
```

Replace it with:

```cpp
// gradelib.h - Grade Calculator v1.2 - Chapter 11
```

Then find the four cutoff constants and delete all four:

```cpp
const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
```

Find the `CAP_AT_100` constant:

```cpp
const bool CAP_AT_100 = true;
```

Directly below it, add:

```cpp

// The most tiers a grade scale may hold. Chapter 12 removes this limit.
const int MAX_TIERS = 12;
```

**Why:** `A_CUTOFF` and friends were an improvement on magic numbers in
Chapter 6, but they are still *code*. A grade scale is **data**: this course
uses 90/80/70/60, another might use 93/85/77/70, and a program that needs
recompiling to change that is the wrong shape. From here the cutoffs live in
arrays the user can fill, and the constants have nothing left to do.

`MAX_TIERS` replaces them with a different kind of limit — how many tiers the
fixed-size array can hold. That is a real constraint of arrays, and naming it
is how the limit stays in one place.

## Step 2 — Document the new `computePercentage` contract

In `gradelib.h`, find the one-line comment above `computePercentage`:

```cpp
/** Converts points to a capped, rounded percentage. Requires possible > 0. */
```

Replace it with this fuller block:

```cpp
/**
 * Converts points to a capped, rounded percentage.
 * @param  earned    total points earned including bonus
 * @param  possible  total points possible
 * @return percentage rounded to one decimal place, or 0.0 when possible <= 0
 */
```

**Why:** Chapter 10's version carried a precondition — the caller had to
ensure `possible > 0`. That worked when one caller existed. A roster has many:
every student row calls it, and any of them could total zero possible points if
every assignment is worth 0. Pushing the check into the function is the right
call once the number of callers grows, and the documented contract changes from
"you must check" to "returns 0.0 in that case". Step 4 implements it.

## Step 3 — Swap the fixed lookup for the table-driven one

In `gradelib.h`, find the `assignLetterGrade` declaration with its comment and the blank line below it, and delete all three lines:

```cpp
/** Maps a percentage to a letter grade on the fixed course scale. */
char assignLetterGrade(double percentage);
```

Then find the last line of the file:

```cpp
#endif
```

Directly above it, add:

```cpp
/**
 * Fills a scale with the default tiers: A 90, B 80, C 70, D 60, F 0.
 * @param  cutoffs  receives the minimum percentage for each tier
 * @param  letters  receives the letter for each tier
 * @param  count    receives the number of tiers written
 */
void useDefaultScale(double cutoffs[], char letters[], int& count);

/**
 * Reads a custom grade scale from the user into two parallel arrays, highest
 * cutoff first. A tier whose cutoff is not below the previous one is refused,
 * and an 'F' at 0 is appended if the scale does not reach 0.
 * @return the number of tiers stored, never more than MAX_TIERS
 */
int readGradeScale(double cutoffs[], char letters[]);

/**
 * Table-driven lookup: the letter of the first tier the percentage reaches.
 * @pre    cutoffs[0..count-1] strictly descend
 * @return that tier's letter, or '?' if the scale does not reach this value
 */
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);
```

**Why:** These three declarations are the chapter's new interface, and the
shape of `letterFor` is worth reading closely:

```cpp
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);
```

An array parameter does **not** carry its own length in C++ — `cutoffs[]`
decays to a pointer, and `sizeof` inside the function would tell you the size
of a pointer, not the array. So the count must be passed alongside it. That is
why every one of these functions takes or returns a `count`, and it is the
single most important thing to understand about passing arrays to functions.

`const` on the two lookup arrays promises `letterFor` will not modify them.
`useDefaultScale` and `readGradeScale` take them non-`const`, because filling
them in *is* their job.

## Step 4 — Guard the division in `computePercentage`

In `gradelib.cpp`, update the first comment line:

```cpp
// gradelib.cpp - Grade Calculator v1.1 - Chapter 10
```

Replace it with:

```cpp
// gradelib.cpp - Grade Calculator v1.2 - Chapter 11
```

Then find the start of `computePercentage`:

```cpp
double computePercentage(double earned, double possible) {
```

Directly below it, add:

```cpp
    // A roster can produce a zero denominator (every assignment worth 0, or
    // every assignment dropped), so the guard lives here rather than in every
    // caller.
    if (possible <= 0.0) { return 0.0; }
```

**Why:** This is the precondition from Step 2 turned into code. Returning
`0.0` for a zero denominator means a student whose assignments are all worth
nothing shows 0.0% rather than `inf` or `nan` — and because the check lives
here, every caller in the roster loop gets it for free.

## Step 5 — Remove `assignLetterGrade`

In `gradelib.cpp`, find the whole of `assignLetterGrade` and the blank line below it, and delete all eight lines:

```cpp
char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}
```

**Why:** Its replacement arrives in the next step. Deleting it now, in the
same chapter, is deliberate: a program with two grading functions — one fixed,
one table-driven — invites a caller to use the wrong one, and the fixed one
would silently ignore whatever scale the user defined.

## Step 6 — Add the three scale functions

Go to the very end of `gradelib.cpp`. After the last line, leave one blank line and add all three functions:

```cpp
void useDefaultScale(double cutoffs[], char letters[], int& count) {
    const char defLetters[] = {'A', 'B', 'C', 'D', 'F'};
    const double defCutoffs[] = {90.0, 80.0, 70.0, 60.0, 0.0};
    count = 5;
    for (int i = 0; i < count; ++i) {
        letters[i] = defLetters[i];
        cutoffs[i] = defCutoffs[i];
    }
}

int readGradeScale(double cutoffs[], char letters[]) {
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers from highest to lowest. The last tier should be 0.\n";
    std::cout << "Example: A 90, B 80, C 70, D 60, F 0\n\n";

    int count = 0;
    while (count < MAX_TIERS) {
        std::string prompt = "Tier " + std::to_string(count + 1) + " letter (or 'done'): ";
        std::string letterText = readNonEmptyLine(prompt);
        if (letterText == "done" || letterText.empty()) { break; }

        double cutoff = 0.0;
        if (!readNonNegative("  Minimum percentage for this tier: ", cutoff)) { break; }

        // Validation: cutoffs must strictly descend, or the lookup breaks.
        if (count > 0 && cutoff >= cutoffs[count - 1]) {
            std::cout << "  Cutoff must be lower than the previous tier ("
                      << cutoffs[count - 1] << "). Tier not added.\n";
            continue;
        }
        letters[count] = letterText[0];
        cutoffs[count] = cutoff;
        ++count;
    }

    // A scale that does not reach 0 leaves low scores unclassified.
    if (count == 0 || cutoffs[count - 1] > 0.0) {
        std::cout << "\nNote: your scale did not reach 0, so an 'F' at 0 was added.\n";
        if (count < MAX_TIERS) {
            letters[count] = 'F';
            cutoffs[count] = 0.0;
            ++count;
        }
    }
    return count;
}

char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int i = 0; i < count; ++i) {
        if (percentage >= cutoffs[i]) {
            return letters[i];
        }
    }
    return '?';
}
```

**Why:** Three things to notice.

**`useDefaultScale` copies from local arrays.** It writes the course default
into the caller's arrays element by element. The `const char defLetters[] =
{...}` initializer form is how you write a small fixed table inline.

**`readGradeScale` validates that cutoffs descend.** `if (count > 0 && cutoff
>= cutoffs[count - 1])` refuses a tier that is not strictly below the one
before it. This is not fussiness: `letterFor` returns the *first* tier the
percentage reaches, so an out-of-order table silently returns wrong letters
rather than failing. The function also appends an `F` at 0 if the user's scale
stops short, because a scale that never reaches 0 leaves low percentages with
no letter at all — `letterFor` would return `'?'`.

**`letterFor` is the payoff.** Compare it with the chain it replaces:

```cpp
for (int i = 0; i < count; ++i) {
    if (percentage >= cutoffs[i]) { return letters[i]; }
}
return '?';
```

Four lines, and it works for *any* scale with any number of tiers. The
Chapter 6 chain was eight lines and worked for exactly one scale. **Replacing
branching logic with a loop over data is one of the most valuable moves in
programming**, and this is the clearest example of it in the book.

> **Do not click Run yet.** `main.cpp` still calls `assignLetterGrade`, which
> no longer exists, so the link will fail. Finish Steps 7 and 8 first.

## Step 7 — Rewrite the top of `main.cpp`

In `main.cpp`, find the comment header and the include lines — eight lines in all:

```cpp
// main.cpp - Grade Calculator v1.1 - Chapter 10
// Same behavior as v1.0, now split across three files with validated input.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>
```

Replace all eight with these sixteen:

```cpp
// main.cpp - Grade Calculator v1.2 - Chapter 11
// Multi-student roster on arrays, plus a USER-DEFINED letter grade scale.
// New this version: 2D arrays, parallel arrays, table-driven grade lookup.
//
// Central lesson: the hard-coded if/else chain of v1.1 becomes a loop over a
// table of data. Changing the grading scheme no longer means changing code.
//
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>

const int MAX_STUDENTS = 40;
const int MAX_ASSIGNMENTS = 20;
```

**Why:** `MAX_STUDENTS` and `MAX_ASSIGNMENTS` live in `main.cpp`, not the
library, because they describe *this program's* capacity rather than anything
about grading. `MAX_TIERS` went in the header instead, because the library's
own `readGradeScale` needs it. Deciding which constant belongs on which side of
the interface is the same judgment as deciding which functions belong there.

## Step 8 — Replace the body with the roster

In `main.cpp`, find the start of `readAssignment`:

```cpp
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
```

Delete that line and everything below it (both helper functions and the whole of the old `main`), down to and including this line:

```cpp
    return 0;
```

In the space where that code was, enter this:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v1.2 ===\n";

    // Parallel arrays: studentNames[s] belongs with pointsEarned[s][...]
    std::string studentNames[MAX_STUDENTS];
    std::string assignmentNames[MAX_ASSIGNMENTS];
    double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS] = {{0.0}};
    double pointsPossible[MAX_ASSIGNMENTS] = {0.0};
    int studentCount = 0;
    int assignmentCount = 0;

    double cutoffs[MAX_TIERS] = {0.0};
    char letters[MAX_TIERS] = {'\0'};
    int tierCount = 0;

    std::string useCustom = readNonEmptyLine("Define a custom grade scale? (y/n): ");
    if (!useCustom.empty() && (useCustom[0] == 'y' || useCustom[0] == 'Y')) {
        tierCount = readGradeScale(cutoffs, letters);
    } else {
        useDefaultScale(cutoffs, letters, tierCount);
        std::cout << "Using the default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    std::cout << "\n--- Enter assignments ---\n";
    while (assignmentCount < MAX_ASSIGNMENTS) {
        std::string name = readNonEmptyLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        assignmentNames[assignmentCount] = name;
        if (!readNonNegative("  Points possible: ", pointsPossible[assignmentCount])) { break; }
        ++assignmentCount;
    }

    std::cout << "\n--- Enter students ---\n";
    while (studentCount < MAX_STUDENTS) {
        std::string name = readNonEmptyLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames[studentCount] = name;
        for (int a = 0; a < assignmentCount; ++a) {
            std::string prompt = "  " + assignmentNames[a] + " points earned (incl. bonus): ";
            if (!readNonNegative(prompt, pointsEarned[studentCount][a])) { break; }
        }
        ++studentCount;
    }

    // ---------- report ----------
    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (int s = 0; s < studentCount; ++s) {
        double earned = 0.0;
        double possible = 0.0;
        for (int a = 0; a < assignmentCount; ++a) {
            earned += pointsEarned[s][a];
            possible += pointsPossible[a];
        }
        double pct = computePercentage(earned, possible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(9) << formatGrade(pct) << "   "
                  << formatGrade(letterFor(pct, cutoffs, letters, tierCount)) << "\n";
    }

    if (studentCount > 0) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(9)
                  << formatGrade(classTotal / studentCount) << "\n";
    } else {
        std::cout << "No students entered.\n";
    }

    std::cout << "\nPer-assignment averages:\n";
    for (int a = 0; a < assignmentCount; ++a) {
        double sum = 0.0;
        for (int s = 0; s < studentCount; ++s) { sum += pointsEarned[s][a]; }
        double avg = (studentCount > 0) ? sum / studentCount : 0.0;
        std::cout << "  " << std::left << std::setw(20) << assignmentNames[a]
                  << avg << " / " << pointsPossible[a] << "\n";
    }
    return 0;
```

**Why:** `readAssignment` and `printReport` go because both assumed a single
student. What replaces them is the chapter's data structure work.

**The 2D array.** `double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS]` is a
grid: `pointsEarned[s][a]` is student `s`'s score on assignment `a`. The
`= {{0.0}}` initializer zeroes the whole thing — without it the array holds
whatever was in that memory, and a student who skipped an assignment would get
a garbage score.

**Parallel arrays.** `studentNames[s]` describes the same student as
`pointsEarned[s][...]`, and `assignmentNames[a]` and `pointsPossible[a]` the
same assignment. Nothing in the language enforces that correspondence — it is
a convention you maintain, which is exactly why the comment naming it is
there. Insert into one and forget the other and the data silently misaligns.
Chapter 14 replaces this arrangement with `struct`s, which make the grouping
real.

**Nested loops.** The report's outer loop walks students; the inner loop walks
that student's assignments to total them. The per-assignment averages at the
end invert the nesting — outer over assignments, inner over students — to sum
a *column* of the grid instead of a row. Which index is on the outside
determines what you are summing, and getting that backwards is a classic
error.

**Counts, not capacities.** Every loop runs to `studentCount` or
`assignmentCount`, never to `MAX_STUDENTS` or `MAX_ASSIGNMENTS`. The arrays
are 40 long but only the first `studentCount` entries hold real data; reading
past the count gives you the zeroes from initialization and a wrong class
average. **With fixed arrays you always track how many entries are actually in
use** — the array cannot tell you.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> Click **Run** with all three files open, then work through the test plan below in the Terminal.

## Test plan

**1. Default scale, two assignments, two students.** Answer `n` to the custom
scale, then `Essay` / `50`, `Quiz` / `20`, `done`; then `Ada Lovelace` with
`45` and `18`, `Grace Hopper` with `30` and `10`, `done`. Expected:

```text
=====================================
  CLASS REPORT
=====================================
Ada Lovelace            90.0%   A
Grace Hopper            57.1%   F
-------------------------------------
CLASS AVERAGE           73.5%

Per-assignment averages:
  Essay               37.5 / 50.0
  Quiz                14.0 / 20.0
```

Check the arithmetic by hand: Ada has 63 of 70 possible, which is 90.0%.

**2. A custom scale.** Answer `y`, then enter `A` 85, `B` 70, `C` 50, `done`.
Note the message that an `F` at 0 was added — your scale stopped at 50, so
anything below it had no letter. Then one assignment worth `100`, and students
scoring `88` and `60`. With this scale 88 is an `A` and 60 is a `C`; with the
default scale they would be a `B` and a `D`. **Same program, same data,
different scheme, no recompile** — that is the chapter.

**3. Cutoffs must descend.** Answer `y`, enter `A` 80, then `B` 90. The tier is
refused with a message naming the previous cutoff. Enter `B` 70 instead and
carry on.

**4. Bad input still recovers.** At any points prompt type `abc`, then `-5`,
then a real number. The library's validation from Chapter 10 is unchanged and
still handles both.

**5. No students.** Answer `n`, enter one assignment, then `done` immediately
at the student prompt. The report prints `No students entered.` and the program
exits normally — no division by zero.

## Check your work

Then confirm:

- [ ] All three files compile together with no errors and **no warnings**.
- [ ] `A_CUTOFF` through `D_CUTOFF` and `assignLetterGrade` no longer appear
      anywhere in the project.
- [ ] A custom scale changes the letters awarded without any code change.
- [ ] A tier whose cutoff is not below the previous one is refused.
- [ ] A scale that does not reach 0 gets an `F` at 0 appended, with a message.
- [ ] Per-student percentages match a hand calculation of their row.
- [ ] Per-assignment averages match a hand calculation of their column.
- [ ] Entering no students prints `No students entered.` and exits cleanly.
- [ ] Every loop runs to a count, never to `MAX_STUDENTS` or
      `MAX_ASSIGNMENTS`.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 11 Grade Calculator v1.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 11 checkpoint.
- The commit is pushed to GitHub.
