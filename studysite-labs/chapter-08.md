# Chapter 08 Lab — Round and Cap the Grade

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.7
- **Starting point:** Your committed Chapter 7 v0.6 program (one file, sentinel loop, accumulators).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Chapter 4 left a question open: should bonus points be able to push a grade
above 100%? This chapter answers it — and, more importantly, answers it *in
one place*, with the decision written down. You will also fix a subtle
unfairness in how the grade is decided, by rounding the percentage **before**
comparing it to the cutoffs rather than only when printing it. Both changes are
made with standard library functions instead of hand-written logic. By the end
you will have:

1. A `CAP_AT_100` constant, and a header comment recording the policy it
   implements and how to reverse it.
2. `std::min` applied to the raw percentage, expressing the cap in one line.
3. `std::round` used to round to one decimal place, so the number displayed
   and the number graded are the same number.
4. An early `return 0;` for the no-grade cases, which flattens the nested
   decision that was starting to get hard to follow.
5. A note reporting the uncapped score when the cap actually applies.

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

## Step 1 — Document the policy and include `<cmath>`

In `main.cpp`, find the five header comment lines:

```cpp
// Grade Calculator v0.6 - Chapter 7
// Accepts many named assignments until a sentinel, then reports the course grade.
// New this version: sentinel-controlled while loop, accumulators.
// Key idea: points-based grading IS the accumulator pattern - a running total
// of points earned divided by a running total of points possible.
```

Replace it with:

```cpp
// Grade Calculator v0.7 - Chapter 8
// Correct rounding and a documented bonus-point cap policy.
// New this version: std::round, std::min, library functions replace hand-rolled logic.
//
// POLICY DECISION (documented per Chapter 4): this gradebook CAPS the reported
// percentage at 100. Bonus points can rescue a low score but cannot produce a
// grade above the maximum. Set CAP_AT_100 to false for uncapped reporting.
//
```

Now find the `<iostream>` include and add this above it:

```cpp
#include <iostream>
```

Directly above it, add:

```cpp
#include <cmath>
```

**Why:** `<cmath>` declares `std::round`; `std::min` comes from `<algorithm>`,
but in practice it is reachable here through the other headers — on a strict
compiler you would add `<algorithm>` explicitly, and it is good practice to do
so if yours complains.

The header block is where the **policy decision** is recorded, and this is the
chapter's quieter lesson. Capping at 100 is a choice, not a fact: a different
course could reasonably decide the other way. Code that silently embodies a
policy is code nobody can question or change safely. Naming the decision,
saying who it came from, and saying exactly what to flip to reverse it turns an
invisible assumption into a documented one.

## Step 2 — Add the policy constant and update the banner

In `main.cpp`, find the `SENTINEL` line:

```cpp
const std::string SENTINEL = "done";
```

Directly below it, add:

```cpp
const bool CAP_AT_100 = true;
```

Then find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.6 ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.7 ===\n\n";
```

**Why:** `const bool CAP_AT_100 = true;` is the switch the header comment
promises. A named boolean constant is better than writing `true` inside the
calculation for the same reason `A_CUTOFF` beat `90.0`: the name says what the
value *means*, and changing the policy is a one-line edit in an obvious place
rather than a hunt through the logic.

## Step 3 — Tidy the instructions and remove two stale comments

In `main.cpp`, find the two instruction lines above the accumulators:

```cpp
    std::cout << "\nEnter assignments one at a time.\n";
    std::cout << "Type " << SENTINEL << " as the assignment name when finished.\n\n";
```

Replace both with this one line:

```cpp
    std::cout << "\nType " << SENTINEL << " as the assignment name when finished.\n\n";
```

Find the comment above the accumulators and delete it:

```cpp
    // Accumulators: these two running totals are the entire grading algorithm.
```

Then find the blank line and two-line comment above the `std::cin.ignore` call and delete all three lines:

```cpp

        // After reading a number with >>, the newline is still in the buffer.
        // Discard it, or the next getline returns an empty string.
```

**Why:** All three were teaching comments that have done their job. The
accumulator pattern and the `>>`/`getline` buffer problem were Chapter 7's
subject; by now they are part of how you read this code rather than something
it has to explain. The `ignore` call stays, of course — only the commentary
goes. Leaving the call tucked directly under the read it belongs to actually
makes the pairing clearer than the comment did.

## Step 4 — Replace the running total with a brief acknowledgement

In `main.cpp`, find the running-total block inside the loop — seven lines, plus the blank line below it:

```cpp
        std::cout << std::fixed << std::setprecision(1);
        if (totalPossible > 0.0) {
            std::cout << "  Running total: " << totalEarned << " / " << totalPossible
                      << " (" << totalEarned / totalPossible * 100.0 << "%)\n\n";
        } else {
            std::cout << "  Running total: " << totalEarned << " / 0.0\n\n";
        }
```

Replace all of it with this single line:

```cpp
        std::cout << "  Recorded.\n\n";
```

**Why:** The running total duplicated the percentage calculation, and from this
chapter on that calculation acquires a cap and a rounding rule. Two copies of a
rule that is about to get more complicated is exactly the kind of duplication
that drifts out of step — one copy gets the cap, the other does not, and the
running total starts contradicting the final report. Removing the second copy
now is cheaper than keeping them synchronized, and `Recorded.` still gives the
user the confirmation they need that the entry was accepted.

> **▶ Run checkpoint:** Click **Run**. The program should behave as it did in Chapter 7, except that each assignment is acknowledged with `Recorded.` instead of a running total. The grading at the end is unchanged so far.

## Step 5 — Flatten the decision with an early return

In `main.cpp`, find the start of the grading section — the `if` testing the count, through the line that computes the percentage:

```cpp
    if (assignmentCount == 0) {
        std::cout << "No assignments entered, so there is no course grade yet.\n";
    } else if (totalPossible > 0.0) {
        double percentage = totalEarned / totalPossible * 100.0;
```

Replace those four lines with these six:

```cpp
    if (assignmentCount == 0 || totalPossible <= 0.0) {
        std::cout << "No course grade is available yet.\n";
        return 0;
    }

    double rawPercentage = totalEarned / totalPossible * 100.0;
```

**Why:** This is a **guard clause**: handle the cases that have no answer,
return immediately, and let the rest of the function assume the normal case.
Compare the two shapes. Before, the real work sat indented inside an
`else if`, with its conditions held in your head while you read it. After, the
impossible cases are dealt with in four lines at the top and everything below
runs at one level of indentation with nothing left to remember.

The two no-grade conditions also combine with `||` into one branch, because
they produce the same outcome. Chapter 7 separated them to explain the
difference; now that the distinction has been made, one message for "no grade
available" is simpler and the user loses nothing.

Note that `rawPercentage` is the name, not `percentage`. From here there are
*three* related numbers — raw, capped, rounded — and giving each its own exact
name is what keeps the next three steps readable.

## Step 6 — Cap, round, then grade

In `main.cpp`, find everything from the `char letter` declaration down to the closing brace of the final `else` — ten lines:

```cpp
        char letter = 'F';
        if (percentage >= A_CUTOFF)      { letter = 'A'; }
        else if (percentage >= B_CUTOFF) { letter = 'B'; }
        else if (percentage >= C_CUTOFF) { letter = 'C'; }
        else if (percentage >= D_CUTOFF) { letter = 'D'; }
        std::cout << "Percentage:  " << percentage << "%\n";
        std::cout << "Grade:       " << letter << "\n";
    } else {
        std::cout << "All assignments were worth 0 points, so no percentage exists.\n";
    }
```

Replace all of it with this:

```cpp
    // std::min expresses the cap policy in one readable line.
    double reported = CAP_AT_100 ? std::min(rawPercentage, 100.0) : rawPercentage;

    // Round to one decimal place: multiply, round, divide. Doing this once here
    // means the displayed number and the graded number are always the same.
    double rounded = std::round(reported * 10.0) / 10.0;

    char letter = 'F';
    if (rounded >= A_CUTOFF)      { letter = 'A'; }
    else if (rounded >= B_CUTOFF) { letter = 'B'; }
    else if (rounded >= C_CUTOFF) { letter = 'C'; }
    else if (rounded >= D_CUTOFF) { letter = 'D'; }

    std::cout << "Percentage:  " << rounded << "%\n";
    std::cout << "Grade:       " << letter << "\n";
    if (CAP_AT_100 && rawPercentage > 100.0) {
        std::cout << "Note: raw score was " << rawPercentage
                  << "%, capped at 100% by course policy.\n";
    }
```

**Why:** Three ideas, in the order the code applies them.

**`std::min` expresses the cap.** `std::min(rawPercentage, 100.0)` is "whatever
is smaller". Written by hand it would be an `if` with a reassignment, four lines
instead of one, with room for a `>` that should have been `>=`. The conditional
operator `? :` then selects between capped and uncapped reporting based on the
policy constant: read it as "if `CAP_AT_100`, use the capped value, otherwise
use the raw one".

**`std::round` makes the grade fair.** This is the real bug fix, and it is
worth understanding. Previously `std::setprecision(1)` rounded the number *for
display only* — a percentage of 89.96 printed as `90.0` but was compared to
the cutoffs as 89.96, and so came out a `B`. A student seeing `90.0%` next to
a `B` has a legitimate complaint. `std::round(reported * 10.0) / 10.0` is the
standard idiom for rounding to one decimal: scale up, round to the nearest
whole number, scale back down. Doing it **once, here, before the comparison**
guarantees the number shown and the number graded are the same number.

**The note reports what the cap hid.** When the cap applies, the student should
be able to see the uncapped figure and the reason it was not used. `CAP_AT_100
&& rawPercentage > 100.0` is true only when the cap actually changed something
— with the policy off, or a score under 100, no note appears.

> **▶ Run checkpoint:** Click **Run** and work through the test plan below in the Terminal.

## Test plan

All rows use student `Ada Lovelace` and a single assignment named `Essay`,
then `done`.

| Earned | Possible | Bonus | Percentage | Grade | What it proves |
|---|---|---|---|---|---|
| `90` | `100` | `0` | 90.0% | `A` | Exact cutoff still works |
| `89.96` | `100` | `0` | 90.0% | **`A`** | **The rounding fix** — this was a `B` before |
| `89.94` | `100` | `0` | 89.9% | `B` | Rounds down, so correctly a `B` |
| `100` | `100` | `10` | 100.0% | `A` | Cap applies; note shows raw 110.0% |
| `50` | `100` | `45` | 95.0% | `A` | Bonus rescues a low score, under the cap |
| `0` | `100` | `0` | 0.0% | `F` | Zero is valid |

**The second row is the point of the chapter.** Run it on your Chapter 7
program if you still have it and you will get a `B`; here you get an `A`,
because the grade is now decided from the same rounded number the student sees.

Then two structural cases:

**No assignments.** Type `done` immediately: `No course grade is available
yet.` and a clean exit via the guard clause.

**All worth zero points.** One assignment with possible `0`, then `done`: the
same message, because the guard now covers both conditions.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] A raw percentage of 89.96 reports `90.0%` **and** grade `A`.
- [ ] A raw percentage of 89.94 reports `89.9%` and grade `B`.
- [ ] A score above 100% is reported as `100.0%` with the note naming the
      raw figure.
- [ ] Setting `CAP_AT_100` to `false`, rebuilding, and re-running the
      110% case reports `110.0%` with no note — then set it back to `true`.
- [ ] The percentage is rounded once, before the grade comparison, not only
      in the output.
- [ ] Both no-grade cases exit through the single guard clause.

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
4. Enter the commit message **Complete Chapter 8 Grade Calculator v0.7**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 8 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
