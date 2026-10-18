# Chapter 06 Lab — Assign Letter Grades

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.5
- **Starting point:** Your committed Chapter 5 v0.4 program (one file, aligned report).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

A percentage is a number; a grade is a judgment. This chapter adds the
judgment: a four-way decision that turns the percentage into a letter using a
fixed 90/80/70/60 scale. The technique is the `if`/`else if` chain, and the
thing to understand about it is that **order matters** — the first true
condition wins and the rest are never tested. By the end you will have:

1. Four named constants at file scope holding the grade cutoffs.
2. A `char letter` variable set by an `if`/`else if` chain testing the
   cutoffs from highest to lowest.
3. `Percentage` and `Grade` lines in the report, plus a note when bonus
   points push the score above 100%.
4. A simplified report layout, so the two new rows fit without the block
   growing unwieldy.

> **Limitation, by design:** the cutoffs are hard-coded in this version. That
> is a real constraint, not an oversight — Chapter 11 replaces them with a
> scale the user defines at run time.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-6) |

When you are finished your project still has **one** `.cpp` file.

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
clang++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
./gradecalc
```

**Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):

```powershell
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc.exe
.\gradecalc.exe
```

The ▶ Build checkpoints below use `g++ -std=c++17 -Wall -Wextra *.cpp -o
gradecalc`, which works as written on macOS, Linux, and WSL. On Windows, use
the Windows command above instead.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Continue the existing program in your local editor, finish the steps in order, then build.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Step 1 — Update the comment header

In `main.cpp`, find the four header comment lines:

```cpp
// Grade Calculator v0.4 - Chapter 5
// Same computation as v0.3, redesigned interface.
// New this version: prompts state units and ranges, aligned report columns,
// a plain-language message when points possible is zero.
```

Replace it with:

```cpp
// Grade Calculator v0.5 - Chapter 6
// Adds a letter grade from a fixed 90/80/70/60 scale.
// New this version: multi-way if/else if chain, named constants.
// Limitation: the cutoffs are hard-coded. Chapter 11 makes them user-defined.
```

**Why:** The `Limitation:` line is the important addition. Recording a known
constraint, and where it gets fixed, is how you keep a limitation from being
mistaken for a bug by the next person to read the file — including you, three
chapters from now.

## Step 2 — Add the grade cutoffs as named constants

In `main.cpp`, find the last include line:

```cpp
#include <string>
```

Directly below it, add:

```cpp

// Named constants: changing a cutoff means editing one line, not hunting
// for a magic number inside the conditional chain.
const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
```

**Why:** `90.0` written directly inside an `if` is a **magic number**: a value
whose meaning depends on where it appears. `A_CUTOFF` says what it is. The
practical payoff is that changing the scale means editing one line instead of
searching the conditional chain for every occurrence, and getting it wrong in
one place is no longer possible.

`const` tells the compiler the value never changes, so an accidental
assignment becomes a compile error rather than a silent bug. These are declared
*outside* `main`, at file scope, because in Chapter 9 the grading logic moves
into its own function and will need to see them too.

## Step 3 — Simplify the banner

In `main.cpp`, find the five banner lines:

```cpp
    std::cout << "=====================================\n";
    std::cout << "  GRADE CALCULATOR  v0.4\n";
    std::cout << "  Points-based grading\n";
    std::cout << "=====================================\n\n";
    std::cout << "Enter the assignment details below.\n\n";
```

Replace all five with this single line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.5 ===\n\n";
```

Then find the points-earned prompt and shorten it:

```cpp
    std::cout << "Points earned (e.g. 42.5)   : ";
```

Replace it with:

```cpp
    std::cout << "Points earned               : ";
```

**Why:** The report is about to gain two rows and a conditional note. Trimming
the header and the longest prompt keeps the whole interaction on one screen,
which matters more for usability than a decorative banner does. The prompt
colons stay aligned — check that your edit preserves the column.

## Step 4 — Simplify the report block

In `main.cpp`, find the eleven-line report block:

```cpp
    std::cout << "\n-------------------------------------\n";
    std::cout << "  GRADE REPORT\n";
    std::cout << "-------------------------------------\n";
    std::cout << std::left << std::setw(16) << "Student"    << studentName << "\n";
    std::cout << std::left << std::setw(16) << "Assignment" << assignmentName << "\n";
    std::cout << std::left << std::setw(16) << "Points earned"
              << std::fixed << std::setprecision(1) << pointsEarned << "\n";
    std::cout << std::left << std::setw(16) << "Bonus points" << bonusPoints << "\n";
    std::cout << std::left << std::setw(16) << "Total earned" << totalEarned << "\n";
    std::cout << std::left << std::setw(16) << "Points possible" << pointsPossible << "\n";
    std::cout << "-------------------------------------\n";
```

Replace all eleven lines with these five:

```cpp
    std::cout << "\n--- GRADE REPORT ---\n";
    std::cout << "Student:    " << studentName << "\n";
    std::cout << "Assignment: " << assignmentName << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Score:      " << totalEarned << " / " << pointsPossible << "\n";
```

Then find this comment and delete it:

```cpp
    // A zero denominator is explained, not silently reported as 0%.
```

**Why:** The `std::setw` column layout from Chapter 5 is replaced by a compact
label style, and the six separate point rows collapse into one `Score:` line
showing total over possible. The grading result, not the breakdown of points,
is what this version is about.

Note that `std::fixed` and `std::setprecision(1)` now sit on a line of their
own, with no value after them. That is legal and often clearer: they configure
the stream, and every floating-point value printed after them is affected.
Setting stream state separately from printing data is worth preferring once
more than one or two values are involved.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should work exactly as in Chapter 5, with the simpler report. No letter grade yet.

## Step 5 — Add the if/else if chain

In `main.cpp`, find the two lines that print the percentage inside the `if`:

```cpp
        std::cout << std::left << std::setw(16) << "Percentage"
                  << percentage << "%\n";
```

Replace both lines with this:

```cpp

        // Order matters: the first true condition wins, so cutoffs are
        // tested from highest to lowest.
        char letter = 'F';
        if (percentage >= A_CUTOFF) {
            letter = 'A';
        } else if (percentage >= B_CUTOFF) {
            letter = 'B';
        } else if (percentage >= C_CUTOFF) {
            letter = 'C';
        } else if (percentage >= D_CUTOFF) {
            letter = 'D';
        }

        std::cout << "Percentage: " << percentage << "%\n";
        std::cout << "Grade:      " << letter << "\n";
        if (percentage > 100.0) {
            std::cout << "Note: bonus points pushed this above 100%.\n";
        }
```

**Why:** This is the chapter's core idea, and there are three things in it.

**Order matters.** The chain tests the highest cutoff first. In an
`if`/`else if` chain, evaluation stops at the first condition that is true, so
a percentage of 95 matches `>= A_CUTOFF` and the B, C, and D tests never run.
Reverse the order and every passing score would match `>= D_CUTOFF` first and
come out as a D. The ordering is not stylistic — it is the logic.

**The default comes first.** `letter` is initialized to `'F'` before any test.
That means the chain needs no final `else`: anything that fails all four tests
keeps the initial value. Initializing to the fallback and then overwriting it
is a common, readable pattern for this shape of decision.

**A `char` holds one character.** `'A'` in single quotes is a `char` — a
single character. `"A"` in double quotes would be a string, and assigning it
to a `char` is a compile error. The distinction catches people out constantly.

The nested `if (percentage > 100.0)` prints a note only when the bonus pushed
the score past full marks. The percentage above 100 is still reported as-is —
the Chapter 4 policy stands — but now the output says why it looks unusual.

## Step 6 — Update the zero-points branch

In `main.cpp`, find the three lines in the `else` branch:

```cpp
        std::cout << "Percentage      not available\n";
        std::cout << "  An assignment worth 0 points has no percentage,\n";
        std::cout << "  because a score cannot be divided by zero.\n";
```

Replace all three with these two:

```cpp
        std::cout << "Percentage: not available (0 points possible)\n";
        std::cout << "Grade:      not available\n";
```

Then find the closing rule after the `else` block and delete it:

```cpp
    std::cout << "-------------------------------------\n";
```

**Why:** The `else` branch now has to report *two* missing values, not one —
there is no percentage and therefore no grade either. Saying so for both keeps
the report's shape the same in each branch, so a reader always finds a
`Percentage:` line and a `Grade:` line whatever the input. The reason is now
given parenthetically rather than on its own lines, matching the compact style
of the rest of the report.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> Click **Run** and work through the test plan below in the Terminal.

## Test plan

Run the program once per row. All use `Ada Lovelace` and `Essay`, with points
possible `100` and bonus `0` unless stated.

| Points earned | Percentage | Expected grade | Why this case |
|---|---|---|---|
| `95` | 95.0% | `A` | Comfortably above the A cutoff |
| `90` | 90.0% | `A` | **Exactly** on the cutoff — `>=` must include it |
| `89.9` | 89.9% | `B` | Just below; proves the boundary is not off by a hair |
| `80` | 80.0% | `B` | Exactly on the B cutoff |
| `70` | 70.0% | `C` | Exactly on the C cutoff |
| `60` | 60.0% | `D` | Exactly on the D cutoff |
| `59.9` | 59.9% | `F` | Below every cutoff — the initialized default |
| `0` | 0.0% | `F` | Zero is a valid score, not an error |

Then two more:

**Above 100%.** Points earned `100`, bonus `5`: the grade is `A`, the
percentage reads `105.0%`, and the note about bonus points appears.

**Zero points possible.** Enter `0` for points possible: both `Percentage:`
and `Grade:` report `not available`, and no letter is printed.

> The boundary rows are the ones that matter. An off-by-one error in a grade
> scale is invisible on a score of 95 and obvious on a score of exactly 90 —
> which is the score a student is most likely to argue about.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] Every row of the table above produces the expected grade.
- [ ] A score of exactly 90 is an `A`, not a `B`.
- [ ] A score below 60 is an `F` with no final `else` in your chain.
- [ ] The cutoffs appear only in the four `const double` declarations, not
      as numbers inside the `if` chain.
- [ ] A bonus above 100% prints the note and still reports a grade.
- [ ] Zero points possible reports both values as `not available`.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 6 Grade Calculator v0.5"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 6 checkpoint.
- The commit is pushed to GitHub.
