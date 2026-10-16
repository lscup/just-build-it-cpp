# Chapter 10 Lab — Organize Reusable Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.1
- **Starting point:** Your committed Chapter 9 v1.0 program (one file, six functions, menu loop).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

One file with six functions works, but the grading rules and the program that
uses them are tangled together. This chapter separates them into a reusable
**library**: a header file declaring what the library offers, and an
implementation file containing the code. `main.cpp` then uses those functions
without seeing how they work.

While the functions are moving, two new capabilities go in that belong to the
library rather than to `main`: **input validation** that re-prompts instead of
accepting nonsense, and **overloaded** formatting functions. By the end you
will have:

1. `gradelib.h` — the constants, seven function declarations, and an include
   guard.
2. `gradelib.cpp` — the definitions, including two new validating readers
   that re-prompt until the input is usable.
3. Two functions both named `formatGrade`, distinguished only by their
   parameter type — an **overload**.
4. A default argument on `applyBonus`, so a call that omits the bonus means
   "no bonus".
5. A `main.cpp` of about seventy lines that includes `"gradelib.h"` and
   contains only the program's flow.

> **The build command changes this chapter.** Two `.cpp` files must be compiled
> together. In StudySite, both must be open in the editor when you click
> **Run**; a `.cpp` file that is not open is not compiled, and the linker error
> you get names the missing function, not the missing tab.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradelib.h` | Create (Step 1) |
| `gradelib.cpp` | Create (Step 2) |
| `main.cpp` | Edit (Steps 3-8) |

When you are finished your project has **three** files.

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
3. Click **Load from GitHub**, select **COSC1436xxx-Grade-Calculator-YourLastName**, and click `main.cpp`.
   Confirm the editor shows the expected file paths before editing.
4. Create the two new files in StudySite's internal editor, then finish the steps in order. Keep all three files open, and click **Run** at the ▶ Run checkpoint.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Step 1 — Create `gradelib.h`

> **How to create a file:** in the StudySite editor, create a new file with
> the exact name shown (spelling and lowercase matter, because `#include`
> lines refer to these names). Keep each new file open after you create it.

Create a new file named `gradelib.h` and enter this:

```cpp
// gradelib.h - Grade Calculator v1.1 - Chapter 10
// Declarations for the grading library. Separating declarations from
// definitions lets main.cpp use these functions without seeing their code.
#ifndef GRADELIB_H
#define GRADELIB_H

#include <string>

const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
const bool CAP_AT_100 = true;

/** Adds bonus points to a raw score. Bonus defaults to none. */
double applyBonus(double pointsEarned, double bonusPoints = 0.0);

/** Converts points to a capped, rounded percentage. Requires possible > 0. */
double computePercentage(double earned, double possible);

/** Maps a percentage to a letter grade on the fixed course scale. */
char assignLetterGrade(double percentage);

/** Overload 1: formats a percentage for display, e.g. "89.1%". */
std::string formatGrade(double percentage);

/** Overload 2: formats a letter grade for display, e.g. "B". */
std::string formatGrade(char letter);

/**
 * Reads a non-negative number from the user, re-prompting until valid.
 * @param  prompt  text shown to the user
 * @param  value   receives the validated number
 * @return true if a value was read, false if input closed unexpectedly
 */
bool readNonNegative(const std::string& prompt, double& value);

/** Reads a whole line of text, re-prompting if it is empty. */
std::string readNonEmptyLine(const std::string& prompt);

#endif
```

**Why:** A header is a **contract**. It says what the library provides —
names, parameter types, return types — without saying how any of it works.
`main.cpp` includes this file and can then call the functions; it never needs
to see their bodies.

Three things in it are new.

**The include guard.** `#ifndef GRADELIB_H` / `#define GRADELIB_H` / `#endif`
means "if this has not been included yet, include it; otherwise skip". Without
it, a file that includes the header twice gets two copies of every declaration
and the compiler reports redefinition errors. Every header you ever write
needs a guard.

**The default argument.** `double applyBonus(double pointsEarned, double
bonusPoints = 0.0);` means `applyBonus(45.0)` is legal and means
`applyBonus(45.0, 0.0)`. The default goes in the **declaration only**, never
in the definition — repeating it in `gradelib.cpp` is a compile error.

**The overload.** Two functions are named `formatGrade`: one takes a `double`,
the other a `char`. That is allowed because they differ in parameter type, and
the compiler picks the right one from the argument you pass. Overloading lets
one concept — "format this for display" — keep one name instead of needing
`formatPercentage` and `formatLetter`.

## Step 2 — Create `gradelib.cpp`

Create a new file named `gradelib.cpp` and enter this:

```cpp
// gradelib.cpp - Grade Calculator v1.1 - Chapter 10
// Definitions for the grading library declared in gradelib.h.
#include "gradelib.h"

#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>

double applyBonus(double pointsEarned, double bonusPoints) {
    return pointsEarned + bonusPoints;
}

double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}

std::string formatGrade(double percentage) {
    std::ostringstream out;
    out << std::fixed << std::setprecision(1) << percentage << "%";
    return out.str();
}

std::string formatGrade(char letter) {
    return std::string(1, letter);
}

bool readNonNegative(const std::string& prompt, double& value) {
    while (true) {
        std::cout << prompt;
        if (!(std::cin >> value)) {
            if (std::cin.eof()) {
                return false;   // input closed; caller decides what to do
            }
            // Not a number. Clear the error state and discard the bad input,
            // otherwise every later read fails too.
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "  That is not a number. Please try again.\n";
            continue;
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (value < 0.0) {
            std::cout << "  Points cannot be negative. Please try again.\n";
            continue;
        }
        return true;
    }
}

std::string readNonEmptyLine(const std::string& prompt) {
    std::string line;
    while (true) {
        std::cout << prompt;
        if (!std::getline(std::cin, line)) {
            return "";
        }
        if (!line.empty()) {
            return line;
        }
        std::cout << "  This cannot be blank. Please try again.\n";
    }
}
```

**Why:** This is the implementation side of the contract. The first three
functions are moved from `main.cpp` unchanged, which is the point — separating
declaration from definition does not alter behavior.

`#include "gradelib.h"` uses **quotes**, not angle brackets. Quotes mean "look
next to this file first" and are for your own headers; angle brackets are for
the standard library. An implementation file always includes its own header, so
the compiler can check the definitions match the declarations.

The two reader functions are the chapter's new behavior, and `readNonNegative`
repays careful reading. `if (!(std::cin >> value))` detects a **failed** read —
the user typed `abc` where a number was expected. When that happens the stream
enters an error state and *stays* there: every later read fails instantly,
which is why a program without this handling appears to hang or loop forever
printing prompts. The recovery is two steps and both are required:
`std::cin.clear()` resets the error flags, and `std::cin.ignore(...)` discards
the bad characters still sitting in the buffer. Clear without ignore and the
same bad input fails again on the next attempt.

`std::cin.eof()` is checked separately and returns `false` to the caller.
End-of-input is not a typo — it means there is no more input coming, ever, so
re-prompting would loop forever. Distinguishing "bad input, ask again" from
"no input left, give up" is what makes the loop safe.

`formatGrade(double)` uses a `std::ostringstream` — a stream that writes into a
string instead of to the screen. It lets the function apply `std::fixed` and
`std::setprecision(1)` and hand back `"89.1%"` as a value, so formatting is
decided in one place rather than at every call site. `formatGrade(char)` uses
`std::string(1, letter)`, which builds a string of one character.

## Step 3 — Update `main.cpp`'s header and includes

In `main.cpp`, find the comment header and the five include lines — twelve lines in all:

```cpp
// Grade Calculator v1.0 - Chapter 9
// Same behavior as v0.7, rebuilt from documented functions, plus a menu loop.
// New this version: user-defined functions, a menu that keeps the program running.
// Note: individual assignments are not stored yet (no arrays until Chapter 11),
// so the program keeps running totals only.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc

#include <cmath>
#include <iostream>
#include <iomanip>
#include <limits>
#include <string>
```

Replace all twelve with these eight:

```cpp
// main.cpp - Grade Calculator v1.1 - Chapter 10
// Same behavior as v1.0, now split across three files with validated input.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>
```

**Why:** `main.cpp` now includes `"gradelib.h"` first, then only the standard
headers it still needs itself. `<cmath>` and `<limits>` are gone because the
code that used them moved to `gradelib.cpp` — an include that is no longer
needed should go, or the file's dependencies become fiction.

The `Build:` line is updated to name both `.cpp` files. That is the command
the autograder and your local toolchain will use, and it is the first time
this project needs more than one source file on the command line.

## Step 4 — Remove what moved to the library

In `main.cpp`, find the first constant:

```cpp
const double A_CUTOFF = 90.0;
```

Delete that line and everything below it (the five constants and the three calculation functions with their comments), stopping just **above** this line, which you keep:

```cpp
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
```

Next, find the documentation comment above `printReport` and delete those three lines:

```cpp
/**
 * Prints the full course report for the current totals.
 */
```

Finally, find `readMenuChoice` with its comment and the blank line above it, and delete all of it:

```cpp

/**
 * Displays the menu and returns the user's choice as a character.
 */
char readMenuChoice() {
    std::cout << "1) Add assignment   2) View report   3) Quit\n";
    std::cout << "Choice: ";
    std::string line;
    std::getline(std::cin, line);
    return line.empty() ? '?' : line[0];
}
```

**Why:** Every one of these now lives in the library, and a function defined in
two places is a **link error** — the compiler accepts each file alone and the
linker then finds two definitions of `applyBonus` and refuses to produce a
program. This step is not tidying; the program will not build until it is done.

The constants move to the header rather than the implementation file because
`main.cpp` might need them too, and anything a user of the library can see
belongs in the contract.

`readMenuChoice` is deleted outright rather than moved. It is about this
program's menu, not about grading, so it has no business in a reusable grading
library. Step 7 folds it into `main`. Deciding what does *not* belong in a
library is as much a part of designing one as deciding what does.

The documentation comments on `readAssignment` and `printReport` go too: those
two functions are private to `main.cpp` and their one-line declarations are no
longer published anywhere, so the full `@param` blocks would be describing an
interface nobody else can use.

## Step 5 — Rewrite `readAssignment` to validate its input

In `main.cpp`, find the whole of `readAssignment`:

```cpp
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
    std::string assignmentName;
    std::cout << "  Assignment name : ";
    std::getline(std::cin, assignmentName);

    double pointsEarned = 0.0;
    std::cout << "  Points earned   : ";
    std::cin >> pointsEarned;

    double pointsPossible = 0.0;
    std::cout << "  Points possible : ";
    std::cin >> pointsPossible;

    double bonusPoints = 0.0;
    std::cout << "  Bonus points    : ";
    std::cin >> bonusPoints;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    totalEarned += applyBonus(pointsEarned, bonusPoints);
    totalPossible += pointsPossible;
    ++count;
    std::cout << "  Recorded: " << assignmentName << "\n\n";
}
```

Replace all of it with this:

```cpp
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
    std::string name = readNonEmptyLine("  Assignment name : ");

    double earned = 0.0;
    double possible = 0.0;
    double bonus = 0.0;
    if (!readNonNegative("  Points earned   : ", earned))   { return; }
    if (!readNonNegative("  Points possible : ", possible)) { return; }
    if (!readNonNegative("  Bonus points    : ", bonus))    { return; }

    totalEarned += applyBonus(earned, bonus);
    totalPossible += possible;
    ++count;
    std::cout << "  Recorded: " << name << "\n\n";
}
```

**Why:** Twenty-three lines become fifteen, and the new version is harder to
break. Each raw `std::cin >>` is replaced by a call to `readNonNegative`,
which will not return until it has a usable number — so a typo costs the user
a re-prompt instead of corrupting the totals.

The `if (!readNonNegative(...)) { return; }` pattern handles the
end-of-input case: if input has closed there is nothing more to read, so the
function gives up without recording a partial assignment. Returning early
rather than carrying on with half-filled values is what keeps the totals
trustworthy.

Note `applyBonus(earned, bonus)` is still called explicitly with both
arguments. The default argument added in Step 1 is available — `applyBonus(earned)`
would compile — but passing the bonus the user actually entered is clearer
here.

## Step 6 — Use the formatting overloads in `printReport`

In `main.cpp`, find the two lines that print the percentage and grade:

```cpp
    std::cout << "Percentage:  " << percentage << "%\n";
    std::cout << "Grade:       " << assignLetterGrade(percentage) << "\n\n";
```

Replace both with these:

```cpp
    std::cout << "Percentage:  " << formatGrade(percentage) << "\n";
    std::cout << "Grade:       " << formatGrade(assignLetterGrade(percentage)) << "\n\n";
```

**Why:** Both calls are spelled `formatGrade`, and the compiler chooses between
the two overloads by argument type: `percentage` is a `double` so it gets the
`"89.1%"` version, while `assignLetterGrade(percentage)` returns a `char` so it
gets the one-character version. **This is overload resolution, and it happens
at compile time** — there is no run-time cost to having two functions share a
name.

The `"%"` also disappears from this line, because `formatGrade(double)` now
supplies it. Formatting rules living in one place is the whole reason to pass
values through a formatter rather than assembling strings at each call site.

## Step 7 — Inline the menu prompt into `main`

In `main.cpp`, find the banner line and the three lines that read the student name:

```cpp
    std::cout << "=== GRADE CALCULATOR v1.0 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);
```

Replace those five lines with these two:

```cpp
    std::cout << "=== GRADE CALCULATOR v1.1 ===\n\n";
    std::string studentName = readNonEmptyLine("Student name: ");
```

Then find the menu read and the whole `switch`:

```cpp
        char choice = readMenuChoice();
        switch (choice) {
            case '1':
                readAssignment(totalEarned, totalPossible, assignmentCount);
                break;
            case '2':
                printReport(studentName, totalEarned, totalPossible, assignmentCount);
                break;
            case '3':
                running = false;
                break;
            default:
                std::cout << "Please enter 1, 2, or 3.\n\n";
                break;
        }
```

Replace all fifteen lines with these eleven:

```cpp
        std::cout << "1) Add assignment   2) View report   3) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char choice = line.empty() ? '?' : line[0];

        switch (choice) {
            case '1': readAssignment(totalEarned, totalPossible, assignmentCount); break;
            case '2': printReport(studentName, totalEarned, totalPossible, assignmentCount); break;
            case '3': running = false; break;
            default:  std::cout << "Please enter 1, 2, or 3.\n\n"; break;
        }
```

**Why:** The student name now comes from `readNonEmptyLine`, so a student who
presses Enter without typing is asked again instead of getting a blank report.
Three lines collapse into one, and the validation is free because the library
provides it.

The menu read moves inline because `readMenuChoice` is gone. The important
addition is `if (!std::getline(std::cin, line)) { break; }` — if input closes
while the menu is waiting, the loop exits rather than spinning forever on a
dead stream. The earlier version would have looped printing the menu with no
way to stop.

The `switch` is reformatted to one line per case. The logic is identical; the
parallel structure is simply easier to scan when each case is a single short
statement.

> **The intermediate states in Steps 3-7 do not compile.** Between removing a
> function from `main.cpp` and the library providing it, names are temporarily
> missing or doubly defined. That is expected — finish all five steps, then Run.

> **▶ Run checkpoint:** Click **Run** with all three files open. Then work through the test plan below in the Terminal.

## Test plan

**1. It still works.** Student `Ada Lovelace`, option `1` with `Essay`, `45`,
`50`, `0`, then option `2`. Percentage `90.0%`, grade `A` — identical to
Chapter 9 for the same input.

**2. Bad input is rejected, not absorbed.** Choose `1`, and at
`Points earned` type `abc`. You should see `That is not a number. Please try
again.` and the same prompt once more. Then type `45` and continue normally.
In Chapter 9 this input would have broken every later read.

**3. Negative points are rejected.** At `Points earned` type `-5`:
`Points cannot be negative. Please try again.`

**4. Blank input is rejected.** At the student-name prompt press Enter with no
text: `This cannot be blank. Please try again.` Same at an assignment name.

**5. The library is genuinely separate.** Open `main.cpp` and search for
`A_CUTOFF`, `std::round`, and `std::min`. None should appear — they live in the
library now.

**6. The missing-file error, on purpose.** Close the `gradelib.cpp` tab and
click **Run**. You should get a *linker* error naming `applyBonus` or another
library function as undefined — not a compiler error. Learn to recognize it:
it means a `.cpp` file is missing from the build, not that your code is wrong.
Reopen the tab and Run again.

## Check your work

Then confirm:

- [ ] All three files compile together with no errors and **no warnings**.
- [ ] `gradelib.h` has an include guard.
- [ ] The default argument on `applyBonus` appears in `gradelib.h` only, not
      in `gradelib.cpp`.
- [ ] Both `formatGrade` functions exist and the program calls both.
- [ ] Typing a letter where a number is expected re-prompts and then works.
- [ ] Typing a negative number re-prompts.
- [ ] A blank student name or assignment name re-prompts.
- [ ] `main.cpp` contains no cutoffs and no arithmetic on percentages.
- [ ] `readMenuChoice` no longer exists anywhere.
- [ ] The same inputs produce the same grade as your Chapter 9 program.

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
4. Enter the commit message **Complete Chapter 10 Grade Calculator v1.1**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 10 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
