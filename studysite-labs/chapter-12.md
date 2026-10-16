# Chapter 12 Lab — Complete the Dynamic Gradebook

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.3
- **Starting point:** Your committed Chapter 11 v1.2 program (three files, fixed-size roster).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

This is the Course I capstone, and it removes the last artificial limit in the
program. Chapter 11's arrays hold 40 students, 20 assignments and 12 tiers
because somebody had to pick a number. `std::vector` picks no number: it grows
as you add to it, it knows its own size, and it frees its own memory. Every
`MAX_` constant and every separate `count` variable disappears with it.

Then one real feature: **drop each student's lowest assignment**, which is both
genuinely useful and a good lesson in getting a policy right — dropping an
assignment in a points-based scheme has to remove the points possible as well
as the points earned.

By the end you will have:

1. The grade scale as `std::vector<double>` and `std::vector<char>`, with no
   tier limit and no `count` parameter.
2. `readYesNo` in the library, replacing the hand-rolled y/n checks.
3. A roster of `std::vector<std::string>` and
   `std::vector<std::vector<double>>` — a vector of rows — with no student or
   assignment limit.
4. An optional drop-lowest pass, offered only when there is more than one
   assignment to drop.

> **Course I complete.** After this checkpoint the program has the full Course I
> feature set: named assignments, bonus points, a custom letter scale, a
> multi-student roster, class statistics, and drop-lowest. The grading model is
> points-based only; weighted grading arrives in Chapter 20.

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
  your last commit on GitHub, or ask the Tutor to help you line it up, before
  going further.
- A **▶ Run checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select **COSC1436xxx-Grade-Calculator-YourLastName**, and click `main.cpp`, `gradelib.h`, and `gradelib.cpp`.
   Confirm the editor shows the expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. Keep all three files open, and click **Run** at the ▶ Run checkpoint.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Step 1 — Include `<vector>` and drop the tier limit

In `gradelib.h`, find the three header comment lines:

```cpp
// gradelib.h - Grade Calculator v1.2 - Chapter 11
// Declarations for the grading library. Separating declarations from
// definitions lets main.cpp use these functions without seeing their code.
```

Replace it with:

```cpp
// gradelib.h - Grade Calculator v1.3 - Chapter 12 - COURSE I FINAL
// Declarations for the grading library. The fixed-size arrays of v1.2 are
// gone: the scale is now a pair of std::vectors with no tier limit.
```

Then find the include and add the new one below it:

```cpp
#include <string>
```

Directly below it, add:

```cpp
#include <vector>
```

Now find the `MAX_TIERS` comment and constant, and the blank line below them, and delete all three lines:

```cpp
// The most tiers a grade scale may hold. Chapter 12 removes this limit.
const int MAX_TIERS = 12;
```

**Why:** `MAX_TIERS` existed only because an array has to be declared with a
size before you know how much you need. A vector does not, so the constant has
nothing left to describe. **Deleting a limit is the clearest possible evidence
that a data structure changed** — if you find yourself keeping a `MAX_`
constant alongside a vector, something has not actually been converted.

`<vector>` must be included wherever `std::vector` appears in a declaration,
and here that is the header itself, because the scale functions now take
vectors as parameters.

## Step 2 — Add `readYesNo` to the library

In `gradelib.h`, find the `readNonEmptyLine` declaration:

```cpp
std::string readNonEmptyLine(const std::string& prompt);
```

Directly below it, add:

```cpp

/** Reads a line and reports whether it begins with y or Y. */
bool readYesNo(const std::string& prompt);
```

**Why:** `main.cpp` has been writing `!answer.empty() && (answer[0] == 'y' ||
answer[0] == 'Y')` by hand, and this chapter adds a second place that needs
it. Two copies of a condition is the point at which it should become a
function — not because it is long, but because two copies can disagree. The
library is the right home: asking a yes/no question is input handling, which
is what the other readers in there do.

## Step 3 — Convert the scale declarations to vectors

In `gradelib.h`, find the `useDefaultScale` comment block and declaration:

```cpp
 * Fills a scale with the default tiers: A 90, B 80, C 70, D 60, F 0.
 * @param  cutoffs  receives the minimum percentage for each tier
 * @param  letters  receives the letter for each tier
 * @param  count    receives the number of tiers written
 */
void useDefaultScale(double cutoffs[], char letters[], int& count);
```

Replace all six lines with these four:

```cpp
 * Replaces the scale with the default tiers: A 90, B 80, C 70, D 60, F 0.
 * Both vectors are resized to match, so no count has to be tracked.
 */
void useDefaultScale(std::vector<double>& cutoffs, std::vector<char>& letters);
```

Find the `readGradeScale` comment block and declaration:

```cpp
 * Reads a custom grade scale from the user into two parallel arrays, highest
 * cutoff first. A tier whose cutoff is not below the previous one is refused,
 * and an 'F' at 0 is appended if the scale does not reach 0.
 * @return the number of tiers stored, never more than MAX_TIERS
 */
int readGradeScale(double cutoffs[], char letters[]);
```

Replace them with:

```cpp
 * Reads a custom grade scale from the user, highest cutoff first, into two
 * parallel vectors. A tier whose cutoff is not below the previous one is
 * refused, and an 'F' at 0 is appended if the scale does not reach 0. There
 * is no limit on the number of tiers.
 */
void readGradeScale(std::vector<double>& cutoffs, std::vector<char>& letters);
```

Find the `letterFor` precondition line and declaration:

```cpp
 * @pre    cutoffs[0..count-1] strictly descend
 * @return that tier's letter, or '?' if the scale does not reach this value
 */
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);
```

Replace them with:

```cpp
 * @pre    cutoffs strictly descend, and letters is the same size
 * @return that tier's letter, or '?' if the scale does not reach this value
 */
char letterFor(double percentage, const std::vector<double>& cutoffs,
               const std::vector<char>& letters);
```

**Why:** Compare the two signatures of `letterFor`:

```cpp
char letterFor(double pct, const double cutoffs[], const char letters[], int count);
char letterFor(double pct, const std::vector<double>& cutoffs,
               const std::vector<char>& letters);
```

**The `count` parameter is gone, and that is the whole argument for vectors.**
An array cannot tell a function how long it is, so the length had to travel
separately — and nothing stopped a caller passing the wrong one. A vector
carries its own size, so `cutoffs.size()` is always right and the two can never
disagree.

`readGradeScale` also changes from returning `int` to returning `void`, for the
same reason: it used to report how many tiers it stored, and now the vector
knows.

Both vectors are still passed **by reference**. `const&` on the lookup
parameters avoids copying the whole vector while promising not to modify it;
plain `&` on the two filling functions is what lets them write into the
caller's vectors. The Chapter 10 rule holds: `const&` for input you read,
plain `&` for what you change.

## Step 4 — Update the implementation header and comment

In `gradelib.cpp`, update the first comment line:

```cpp
// gradelib.cpp - Grade Calculator v1.2 - Chapter 11
```

Replace it with:

```cpp
// gradelib.cpp - Grade Calculator v1.3 - Chapter 12 - COURSE I FINAL
```

Then find these two comment lines inside `computePercentage`:

```cpp
    // every assignment dropped), so the guard lives here rather than in every
    // caller.
```

Replace it with:

```cpp
    // the only assignment dropped), so the guard lives here rather than in
    // every caller.
```

**Why:** The guard's reasoning gains a case. In Chapter 11 a zero denominator
meant every assignment was worth nothing; now dropping the only assignment a
student has produces the same situation. Same code, one more way to reach it,
so the comment says so.

## Step 5 — Add `readYesNo` and convert `useDefaultScale`

In `gradelib.cpp`, find the whole of `useDefaultScale`:

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
```

Replace all nine lines with these — `readYesNo` first, then the new `useDefaultScale`:

```cpp
bool readYesNo(const std::string& prompt) {
    std::string answer = readNonEmptyLine(prompt);
    return !answer.empty() && (answer[0] == 'y' || answer[0] == 'Y');
}

void useDefaultScale(std::vector<double>& cutoffs, std::vector<char>& letters) {
    cutoffs = {90.0, 80.0, 70.0, 60.0, 0.0};
    letters = {'A', 'B', 'C', 'D', 'F'};
}
```

**Why:** `useDefaultScale` goes from eight lines to three. The array version
had to write each element in a loop and set a count; the vector version assigns
a whole **initializer list** in one statement — `cutoffs = {90.0, 80.0, 70.0,
60.0, 0.0};` — and the vector resizes itself to fit. There is no count to set,
because there is no count.

`readYesNo` delegates to `readNonEmptyLine`, so an empty answer is re-prompted
rather than silently treated as "no". That is a small behavioral improvement
the refactor buys for free.

## Step 6 — Convert `readGradeScale` and `letterFor`

In `gradelib.cpp`, find the whole of `readGradeScale` — thirty-six lines:

```cpp
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
```

Replace all of it with this:

```cpp
void readGradeScale(std::vector<double>& cutoffs, std::vector<char>& letters) {
    cutoffs.clear();
    letters.clear();
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers highest first. Type 'done' to finish.\n\n";

    while (true) {
        std::string letterText = readNonEmptyLine("Tier letter (or 'done'): ");
        if (letterText == "done" || letterText.empty()) { break; }

        double cutoff = 0.0;
        if (!readNonNegative("  Minimum percentage: ", cutoff)) { break; }

        // Validation: cutoffs must strictly descend, or the lookup breaks.
        if (!cutoffs.empty() && cutoff >= cutoffs.back()) {
            std::cout << "  Cutoff must be lower than " << cutoffs.back()
                      << ". Tier not added.\n";
            continue;
        }
        letters.push_back(letterText[0]);
        cutoffs.push_back(cutoff);
    }

    // A scale that does not reach 0 leaves low scores unclassified.
    if (cutoffs.empty() || cutoffs.back() > 0.0) {
        std::cout << "Note: scale did not reach 0, so an 'F' at 0 was added.\n";
        letters.push_back('F');
        cutoffs.push_back(0.0);
    }
}
```

Then find the whole of `letterFor`:

```cpp
char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int i = 0; i < count; ++i) {
        if (percentage >= cutoffs[i]) {
            return letters[i];
        }
    }
    return '?';
}
```

Replace it with:

```cpp
char letterFor(double percentage, const std::vector<double>& cutoffs,
               const std::vector<char>& letters) {
    for (std::size_t i = 0; i < cutoffs.size(); ++i) {
        if (percentage >= cutoffs[i]) { return letters[i]; }
    }
    return '?';
}
```

**Why:** `readGradeScale` loses six lines and gains unlimited tiers. Three
specific changes are worth naming:

- `while (count < MAX_TIERS)` becomes `while (true)`. The loop no longer has a
  capacity to run out of; only the user's `done` ends it.
- `cutoffs[count] = cutoff; ++count;` becomes `cutoffs.push_back(cutoff);`.
  **`push_back` is the vector idiom**: it appends and grows the vector as
  needed, with no index to maintain and no risk of writing past the end.
- `cutoffs[count - 1]` becomes `cutoffs.back()`, and `count > 0` becomes
  `!cutoffs.empty()`. Both say what they mean instead of doing arithmetic on an
  index — and `cutoffs[count - 1]` with `count == 0` would read `cutoffs[-1]`,
  which is undefined behavior the old code avoided only because of the
  `count > 0` guard sitting in front of it.

`letterFor` loops to `cutoffs.size()` with a `std::size_t` index. `size()`
returns an unsigned type, so comparing it against a signed `int` is exactly the
kind of mismatch `-Wall -Wextra` warns about — using `std::size_t` for the
index is what keeps the build clean.

> **Do not click Run yet.** `main.cpp` still declares the scale as arrays and
> calls the old signatures, so it will not compile against the new library.
> Finish Steps 7 and 8 first.

## Step 7 — Convert the top of `main.cpp`

In `main.cpp`, find the comment header, the includes, and the two capacity constants — sixteen lines:

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

Replace all sixteen with these fifteen:

```cpp
// main.cpp - Grade Calculator v1.3 - Chapter 12 - COURSE I FINAL
// Unlimited roster, assignments, and grade tiers using std::vector.
// New this version: std::vector replaces fixed arrays, drop-lowest feature.
//
// Complete Course I feature set: named assignments, bonus points, custom
// letter scale, multi-student roster, class statistics, drop lowest.
// Grading model: points-based only. Weighted grading arrives in Chapter 20.
//
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
```

**Why:** `MAX_STUDENTS` and `MAX_ASSIGNMENTS` follow `MAX_TIERS` out of the
program. The roster is about to become vectors, so there is no capacity to
declare — the only limit left is the machine's memory.

## Step 8 — Convert the roster and add drop-lowest

In `main.cpp`, find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it (the whole of the old `main`), down to and including this line:

```cpp
    return 0;
```

In the space where that code was, enter this:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v1.3 ===\n";
    std::cout << "    Course I final version\n\n";

    std::vector<double> cutoffs;
    std::vector<char> letters;

    if (readYesNo("Define a custom grade scale? (y/n): ")) {
        readGradeScale(cutoffs, letters);
    } else {
        useDefaultScale(cutoffs, letters);
        std::cout << "Using default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    // Assignments: name and points possible, any number of them.
    std::vector<std::string> assignmentNames;
    std::vector<double> pointsPossible;

    std::cout << "\n--- Enter assignments ---\n";
    while (true) {
        std::string name = readNonEmptyLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        double possible = 0.0;
        if (!readNonNegative("  Points possible: ", possible)) { break; }
        assignmentNames.push_back(name);
        pointsPossible.push_back(possible);
    }

    // Students: name plus one earned-points entry per assignment.
    std::vector<std::string> studentNames;
    std::vector<std::vector<double>> earned;

    std::cout << "\n--- Enter students ---\n";
    while (true) {
        std::string name = readNonEmptyLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames.push_back(name);

        std::vector<double> row;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            double value = 0.0;
            readNonNegative("  " + assignmentNames[a] + " points (incl. bonus): ", value);
            row.push_back(value);
        }
        earned.push_back(row);
    }

    bool dropLowest = false;
    if (assignmentNames.size() > 1) {
        dropLowest = readYesNo("\nDrop each student's lowest assignment? (y/n): ");
    }

    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (std::size_t s = 0; s < studentNames.size(); ++s) {
        double totalEarned = 0.0;
        double totalPossible = 0.0;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            totalEarned += earned[s][a];
            totalPossible += pointsPossible[a];
        }

        // Dropping in a points-based scheme removes BOTH the earned points and
        // the possible points. Removing only one would distort the result.
        if (dropLowest && !assignmentNames.empty()) {
            std::size_t worst = 0;
            double worstRatio = 2.0;
            for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
                if (pointsPossible[a] <= 0.0) { continue; }
                double ratio = earned[s][a] / pointsPossible[a];
                if (ratio < worstRatio) { worstRatio = ratio; worst = a; }
            }
            if (worstRatio <= 1.0) {
                totalEarned -= earned[s][worst];
                totalPossible -= pointsPossible[worst];
            }
        }

        double pct = computePercentage(totalEarned, totalPossible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(9) << formatGrade(pct) << "   "
                  << formatGrade(letterFor(pct, cutoffs, letters)) << "\n";
    }

    if (!studentNames.empty()) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(9)
                  << formatGrade(classTotal / studentNames.size()) << "\n";
    } else {
        std::cout << "No students entered.\n";
    }
    return 0;
```

**Why:** Read this in three parts.

**The roster becomes vectors.** `std::vector<std::vector<double>> earned` is a
**vector of vectors** — `earned[s]` is student `s`'s whole row, and
`earned[s][a]` is one score, exactly as the 2D array indexed. The difference is
that each row is built with `push_back` as the scores are read and then
appended with `earned.push_back(row)`, so the structure is exactly as big as
the data. Note also that there is no longer any `= {{0.0}}` initializer: a
vector starts empty and every element is created by being pushed, so there is
no uninitialized memory to worry about.

**Every loop bound comes from the data.** `studentNames.size()`,
`assignmentNames.size()`. No parallel `count` variables, and no way for a
count to drift out of step with its array — the bug that fixed-size arrays
invite and vectors make impossible.

**Drop-lowest, and why it removes two numbers.** The loop finds the assignment
with the worst **ratio** of earned to possible, not the lowest raw score: 8/10
is a worse performance than 40/100, even though 8 is the smaller number.
Assignments worth 0 points are skipped, since their ratio is undefined. Then:

```cpp
totalEarned -= earned[s][worst];
totalPossible -= pointsPossible[worst];
```

**Both** subtractions are required. Removing only the earned points would be
equivalent to scoring zero on the assignment — the opposite of dropping it —
and removing only the possible points would hand the student free marks. In a
points-based scheme, dropping means the assignment never existed, and that
means removing it from both sides of the division.

The offer is guarded by `assignmentNames.size() > 1`, because dropping the only
assignment leaves nothing to grade.

> **▶ Run checkpoint:** Click **Run** with all three files open, then work through the test plan below in the Terminal.

## Test plan

**1. Same answers as Chapter 11.** Answer `n`, then `Essay` / `50`,
`Quiz` / `20`, `done`; `Ada Lovelace` with `45` and `18`, `Grace Hopper` with
`30` and `10`, `done`; then `n` to dropping. Ada should be `90.0%` `A` and
Grace `57.1%` `F`, with a class average of `73.5%` — identical to Chapter 11.
The data structures changed; the answers must not.

**2. Drop-lowest, verified by hand.** One student, two assignments:
`Essay` / `50` and `Quiz` / `20`; `Ada` scoring `40` and `19`; then `y`.

Essay is 40/50 = 0.80, Quiz is 19/20 = 0.95, so Essay is dropped. What remains
is 19 of 20, which is `95.0%` and an `A`. Without the drop it would be 59 of 70
= `84.3%` and a `B`. Confirm you get `95.0%`.

**3. Ratio, not raw score.** One student, two assignments: `Final` / `100` and
`Pop quiz` / `10`; scores `85` and `6`. Raw scores say the pop quiz (6) is
lowest; ratios say 0.60 against 0.85, so the pop quiz is correctly the one
dropped, leaving 85/100 = `85.0%`. Had the program compared raw scores it would
have reached the same answer here — construct a case where it would not, such
as `Final` / `100` scoring `60` and `Quiz` / `10` scoring `9`: ratios 0.60 and
0.90 drop the Final, leaving `90.0%`.

**4. More than twelve tiers.** Answer `y` and enter thirteen or more tiers
with strictly descending cutoffs — `A+` 97, `A` 93, `A-` 90, `B+` 87, and so
on down. Chapter 11 would have stopped accepting them at twelve. All of them
should now be accepted.

**5. One assignment: no drop offer.** Enter a single assignment. The
drop-lowest question must not appear at all.

**6. No students.** `done` immediately at the student prompt prints
`No students entered.` and exits cleanly.

## Check your work

Then confirm:

- [ ] All three files compile together with no errors and **no warnings**.
- [ ] `MAX_TIERS`, `MAX_STUDENTS` and `MAX_ASSIGNMENTS` appear nowhere in the
      project.
- [ ] No `count` variable tracks the length of anything; every bound comes
      from `.size()`.
- [ ] A scale with more than twelve tiers is accepted.
- [ ] The same inputs give the same percentages and letters as your Chapter 11
      program.
- [ ] Drop-lowest removes the assignment with the worst **ratio**, and removes
      its points possible as well as its points earned.
- [ ] With one assignment, the drop-lowest question is not asked.
- [ ] Entering no students prints `No students entered.` and exits cleanly.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — for this chapter that is `main.cpp`, `gradelib.h`, and `gradelib.cpp` — all three must be open. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1436xxx-Grade-Calculator-YourLastName** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 12 Grade Calculator v1.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 12 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
