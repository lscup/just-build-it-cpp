# Chapter 07 Lab — Process Multiple Assignments

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.6
- **Starting point:** Your committed Chapter 6 v0.5 program (one file, one assignment, letter grade).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Until now the program graded exactly one assignment. A course has many, and
you do not know in advance how many — so this chapter introduces the loop that
keeps asking until the user says stop, and the **accumulator** pattern that
builds a result across the iterations. The key insight is worth stating
plainly: points-based grading *is* the accumulator pattern. A course grade is a
running total of points earned divided by a running total of points possible.
By the end you will have:

1. A `SENTINEL` constant holding the word `done`, used both in the prompts
   and in the loop condition.
2. Three accumulators declared before the loop: `totalEarned`,
   `totalPossible`, and `assignmentCount`.
3. A `while` loop that reads one assignment per iteration and reports a
   running total after each.
4. A `std::cin.ignore(...)` call that fixes the classic bug where a
   `getline` after a numeric read returns an empty string.
5. A `COURSE REPORT` that grades the accumulated totals, and says so plainly
   when no assignments were entered at all.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-7) |

When you are finished your project still has **one** `.cpp` file.

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
4. Continue the existing program in StudySite's internal editor, finish the steps in order, then Run.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

> **Compiling:** In StudySite.ai, just click **Run**. StudySite generates the
> compile command for you, then builds and runs the program in one step, so
> you never type one here. The `Build` line in `main.cpp`'s header comment is
> for building on your own computer instead. For this chapter:
>
> **macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):
>
> ```bash
> clang++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

## Step 1 — Update the header and add `<limits>`

In `main.cpp`, find the four header comment lines:

```cpp
// Grade Calculator v0.5 - Chapter 6
// Adds a letter grade from a fixed 90/80/70/60 scale.
// New this version: multi-way if/else if chain, named constants.
// Limitation: the cutoffs are hard-coded. Chapter 11 makes them user-defined.
```

Replace it with:

```cpp
// Grade Calculator v0.6 - Chapter 7
// Accepts many named assignments until a sentinel, then reports the course grade.
// New this version: sentinel-controlled while loop, accumulators.
// Key idea: points-based grading IS the accumulator pattern - a running total
// of points earned divided by a running total of points possible.
```

Now find the `<iomanip>` include and add this below it:

```cpp
#include <iomanip>
```

Directly below it, add:

```cpp
#include <limits>
```

**Why:** `<limits>` provides `std::numeric_limits`, which Step 4 uses to clear
the input buffer. The includes are kept in alphabetical order — `iomanip`,
`limits`, `string` — which is a convention worth following: it makes a missing
include easy to spot and avoids pointless diffs when two people add one.

## Step 2 — Add the sentinel constant

In `main.cpp`, find the two-line comment above the cutoffs and delete it:

```cpp
// Named constants: changing a cutoff means editing one line, not hunting
// for a magic number inside the conditional chain.
```

Then find the `D_CUTOFF` line:

```cpp
const double D_CUTOFF = 60.0;
```

Directly below it, add:

```cpp
const std::string SENTINEL = "done";
```

**Why:** The sentinel — the value that means "no more input" — is defined once
as a constant rather than written as `"done"` in three places. That matters
more than it looks: the word appears in two prompts *and* in the loop
condition, and if those ever disagree the loop becomes impossible to exit. One
constant makes that bug unreachable, and changing the sentinel to `quit` later
is a one-line edit.

The comment above the cutoffs goes because you now know why named constants
exist; the point was made in Chapter 6 and the code no longer needs to argue
for itself.

## Step 3 — Update the banner and the student prompt

In `main.cpp`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.5 ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.6 ===\n\n";
```

Find the student-name prompt and shorten it:

```cpp
    std::cout << "Student name                : ";
```

Replace it with:

```cpp
    std::cout << "Student name: ";
```

**Why:** The student name is now asked once, before the loop, while the
assignment prompts repeat inside it. Those two groups no longer line up in one
column, so the long padding on this prompt has nothing left to align with.

## Step 4 — Add the instructions and the accumulators

In `main.cpp`, find the line that declares the assignment name:

```cpp
    std::string assignmentName;
```

Directly above it, add:

```cpp
    std::cout << "\nEnter assignments one at a time.\n";
    std::cout << "Type " << SENTINEL << " as the assignment name when finished.\n\n";

    // Accumulators: these two running totals are the entire grading algorithm.
    double totalEarned = 0.0;
    double totalPossible = 0.0;
    int assignmentCount = 0;
```

**Why:** The two instruction lines tell the user how to stop *before* they are
trapped in a loop with no visible exit. Printing the sentinel from the constant
means the instructions can never drift out of step with the code.

The three accumulators are the chapter's real content, and where they are
declared is the whole trick. They live **outside** the loop, because a variable
declared inside a loop body is created fresh on every iteration and destroyed
at the end of it — it cannot remember anything. Declared outside, each one
persists across every iteration and accumulates. Each starts at zero, the
identity for addition, so the first `+=` produces the right answer with no
special case for the first assignment.

`assignmentCount` is an `int` rather than a `double` because it counts
discrete things; there is no such thing as 2.5 assignments.

## Step 5 — Turn the single read into a loop

In `main.cpp`, find the assignment-name prompt:

```cpp
    std::cout << "Assignment name             : ";
```

Replace it with:

```cpp
    std::cout << "Assignment name (or " << SENTINEL << "): ";
```

Now find the whole block from the points-earned declaration down to the `Score:` line — nineteen lines in all:

```cpp
    double pointsEarned = 0.0;
    std::cout << "Points earned               : ";
    std::cin >> pointsEarned;

    double pointsPossible = 0.0;
    std::cout << "Points possible (must be >0): ";
    std::cin >> pointsPossible;

    double bonusPoints = 0.0;
    std::cout << "Bonus points (0 for none)   : ";
    std::cin >> bonusPoints;

    double totalEarned = pointsEarned + bonusPoints;

    std::cout << "\n--- GRADE REPORT ---\n";
    std::cout << "Student:    " << studentName << "\n";
    std::cout << "Assignment: " << assignmentName << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Score:      " << totalEarned << " / " << pointsPossible << "\n";
```

Replace all of it with this:

```cpp
    while (assignmentName != SENTINEL) {
        double pointsEarned = 0.0;
        std::cout << "  Points earned   : ";
        std::cin >> pointsEarned;

        double pointsPossible = 0.0;
        std::cout << "  Points possible : ";
        std::cin >> pointsPossible;

        double bonusPoints = 0.0;
        std::cout << "  Bonus points    : ";
        std::cin >> bonusPoints;

        // After reading a number with >>, the newline is still in the buffer.
        // Discard it, or the next getline returns an empty string.
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        totalEarned += pointsEarned + bonusPoints;
        totalPossible += pointsPossible;
        ++assignmentCount;

        std::cout << std::fixed << std::setprecision(1);
        if (totalPossible > 0.0) {
            std::cout << "  Running total: " << totalEarned << " / " << totalPossible
                      << " (" << totalEarned / totalPossible * 100.0 << "%)\n\n";
        } else {
            std::cout << "  Running total: " << totalEarned << " / 0.0\n\n";
        }

        std::cout << "Assignment name (or " << SENTINEL << "): ";
        std::getline(std::cin, assignmentName);
    }

    std::cout << "\n--- COURSE REPORT ---\n";
    std::cout << "Student:     " << studentName << "\n";
    std::cout << "Assignments: " << assignmentCount << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Total:       " << totalEarned << " / " << totalPossible << "\n";
```

**Why:** This is the largest single edit in the course so far, so read what
changed rather than just copying it.

**The loop shape is "read once, then loop".** The first
`getline(std::cin, assignmentName)` happens *before* the `while`, and the last
statement *inside* the loop reads the next one. That arrangement — called a
priming read — is what lets the condition be tested before the body runs even
once. Type `done` at the very first prompt and the body never executes, which
is exactly right: zero assignments is a legitimate input, not an error.

**The accumulators do the work.** `totalEarned += pointsEarned + bonusPoints;`
means "add this to what you already have". `++assignmentCount;` adds one. The
per-assignment variables are declared inside the loop because each iteration
genuinely wants a fresh one; the totals are outside because they must survive.

**`std::cin.ignore(...)` fixes a real bug.** After `std::cin >> bonusPoints`
reads a number, the Enter key the user pressed is *still sitting in the input
buffer*. The next `getline` finds that leftover newline immediately, decides
the line is over, and hands back an empty string — so the loop condition
compares `""` to `"done"`, finds them different, and loops forever asking for
points. The `ignore` call discards everything up to and including the next
newline, clearing the way. `std::numeric_limits<std::streamsize>::max()` is
simply "however much there might be". **Mixing `>>` and `getline` without this
call is one of the most common bugs in beginning C++**, and the symptom —
a prompt that seems to skip itself — looks nothing like its cause.

**The running total is feedback.** Printing progress after each assignment
lets the user catch a typo at the point they made it, rather than discovering a
wrong course grade at the end. It needs the same zero-denominator guard as
before, because the first assignment could be worth zero points.

> **Do not click Run yet.** The grading section below still refers to
> `pointsPossible`, which now lives inside the loop and is not visible outside
> it. The program will not compile until Step 6 replaces that section. This is
> the expected mid-restructure state — finish Steps 6 and 7, then Run.

## Step 6 — Grade the accumulated totals

In `main.cpp`, find the `if` that opens the grading section, together with the comment below it:

```cpp
    if (pointsPossible > 0.0) {
        double percentage = totalEarned / pointsPossible * 100.0;

        // Order matters: the first true condition wins, so cutoffs are
        // tested from highest to lowest.
```

Replace those five lines with these four:

```cpp
    if (assignmentCount == 0) {
        std::cout << "No assignments entered, so there is no course grade yet.\n";
    } else if (totalPossible > 0.0) {
        double percentage = totalEarned / totalPossible * 100.0;
```

Now find the if/else if chain and the lines that print the percentage and grade:

```cpp
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

Replace all fifteen lines with these six:

```cpp
        if (percentage >= A_CUTOFF)      { letter = 'A'; }
        else if (percentage >= B_CUTOFF) { letter = 'B'; }
        else if (percentage >= C_CUTOFF) { letter = 'C'; }
        else if (percentage >= D_CUTOFF) { letter = 'D'; }
        std::cout << "Percentage:  " << percentage << "%\n";
        std::cout << "Grade:       " << letter << "\n";
```

**Why:** The decision now has **three** outcomes, not two, and they must be
tested in this order. `assignmentCount == 0` comes first because "nothing was
entered" is a different situation from "something was entered but it was worth
no points", and the user deserves to be told which one happened. Only after
both of those are ruled out is a percentage meaningful.

The chain itself is unchanged in logic — same cutoffs, same highest-first
order, same `'F'` default — but it now divides the *totals* rather than one
assignment's points, and it is written in the compact one-line-per-branch form.
Both forms are correct; this one shows the parallel structure of the four
branches at a glance, which is easier to check for an ordering mistake.

The note about exceeding 100% is dropped: across a whole course, a bonus on one
assignment rarely pushes the total over, and the line was becoming noise.

## Step 7 — Update the zero-points message

In `main.cpp`, find the two lines in the final `else`:

```cpp
        std::cout << "Percentage: not available (0 points possible)\n";
        std::cout << "Grade:      not available\n";
```

Replace both with this one line:

```cpp
        std::cout << "All assignments were worth 0 points, so no percentage exists.\n";
```

**Why:** The message now describes the course-wide situation — *all* the
assignments were worth zero — rather than a single assignment's points
possible. A message that names the actual condition is the difference between
a user understanding the program and distrusting it.

> **▶ Run checkpoint:** Click **Run** and work through the test plan below in the Terminal.

## Test plan

**1. Three assignments.** Student `Ada Lovelace`, then:

| Assignment | Earned | Possible | Bonus |
|---|---|---|---|
| `Essay` | `45` | `50` | `0` |
| `Quiz` | `18` | `20` | `2` |
| `Project` | `88` | `100` | `0` |

then `done`. Totals should be `153.0 / 170.0`, percentage `90.0%`, grade `A`,
and `Assignments: 3`. Check that the running total after each row matches what
you would compute by hand.

**2. The empty case — the important one.** Enter a student name, then type
`done` at the very first assignment prompt. The report must show
`Assignments: 0` and the message about no course grade yet. The program must
**not** crash, print `nan`, or report an `F`.

**3. The `getline` bug, deliberately.** Enter one assignment, and at the
assignment-name prompt for the second one, type a name with a space in it such
as `Final Exam`. It must be stored in full. If you see the prompt flash past
without waiting for input, or the loop will not exit on `done`, the
`std::cin.ignore(...)` line from Step 5 is missing or misplaced.

**4. All assignments worth zero.** One assignment with points possible `0`,
then `done`: the report should say all assignments were worth 0 points.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] Typing `done` at the first prompt gives `Assignments: 0` and no grade.
- [ ] A multi-word assignment name entered after the first iteration is
      stored in full.
- [ ] The loop exits on `done` every time, not only the first.
- [ ] The running total after each assignment matches the final total.
- [ ] The word `done` appears in the program only as `SENTINEL`, never as a
      literal.
- [ ] The three accumulators are declared before the loop, not inside it.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — for this chapter that is `main.cpp`. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1436xxx-Grade-Calculator-YourLastName** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 7 Grade Calculator v0.6**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 7 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
