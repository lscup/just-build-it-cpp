# Chapter 05 Lab — Design the Interface

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.4
- **Starting point:** Your committed Chapter 4 v0.3 program (one file, computes a percentage).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

This chapter adds no new calculation. The arithmetic at the end is identical to
Chapter 4's. What changes is everything around it: the prompts say what units
and ranges they expect, the report lines up in columns that stay aligned
whatever the values, and the zero-points case explains itself in plain English
instead of quietly printing `0.0%`. Documentation and interface design are the
chapter's subject, and the exercise is to improve a program's usability without
touching what it computes. By the end you will have:

1. A four-line banner naming the application, its version, and its grading
   model.
2. Five prompts that state their units, an example, or their valid range,
   with the colons aligned in a column.
3. A `GRADE REPORT` block using `std::left` and `std::setw` so labels and
   values align regardless of length.
4. An `else` branch that explains *why* there is no percentage when an
   assignment is worth zero points.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-5) |

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

## Step 1 — Update the comment header

In `main.cpp`, find the five header comment lines:

```cpp
// Grade Calculator v0.3 - Chapter 4
// Adds bonus points and a percentage calculation.
// New this version: floating-point division, output formatting.
// Design note: bonus points are added to points EARNED but not to points
// POSSIBLE, so a percentage above 100 is possible. v0.3 reports it uncapped.
```

Replace it with:

```cpp
// Grade Calculator v0.4 - Chapter 5
// Same computation as v0.3, redesigned interface.
// New this version: prompts state units and ranges, aligned report columns,
// a plain-language message when points possible is zero.
```

**Why:** The design note about uncapped percentages goes away because this
version no longer reports a bare percentage in the zero case — the new `else`
branch in Step 5 replaces that behavior with an explanation. A header comment
is only useful while it is true, so a note that no longer describes the code
is worse than no note at all. The replacement records what this version
actually changed: the interface, not the computation.

## Step 2 — Replace the one-line banner with a titled block

In `main.cpp`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.3 ===\n\n";
```

Replace it with these five lines:

```cpp
    std::cout << "=====================================\n";
    std::cout << "  GRADE CALCULATOR  v0.4\n";
    std::cout << "  Points-based grading\n";
    std::cout << "=====================================\n\n";
    std::cout << "Enter the assignment details below.\n\n";
```

**Why:** A program's first screen should answer "what is this and what does it
want from me". The banner names the application and the grading model, and the
line below it tells the user what is about to happen. The `\n\n` on the closing
rule and on the instruction line creates breathing room, so the prompts that
follow are visually separate from the header rather than crowding it.

## Step 3 — Rewrite the five prompts

In `main.cpp`, find the student-name prompt:

```cpp
    std::cout << "Student name: ";
```

Replace it with:

```cpp
    std::cout << "Student name                : ";
```

Find the assignment-name prompt:

```cpp
    std::cout << "Assignment name: ";
```

Replace it with:

```cpp
    std::cout << "Assignment name             : ";
```

Find the points-earned prompt:

```cpp
    std::cout << "Points earned: ";
```

Replace it with:

```cpp
    std::cout << "Points earned (e.g. 42.5)   : ";
```

Find the points-possible prompt:

```cpp
    std::cout << "Points possible: ";
```

Replace it with:

```cpp
    std::cout << "Points possible (must be >0): ";
```

Find the bonus-points prompt:

```cpp
    std::cout << "Bonus points (0 if none): ";
```

Replace it with:

```cpp
    std::cout << "Bonus points (0 for none)   : ";
```

**Why:** Each prompt now carries the information the user needs *before*
typing, not after getting it wrong. `(e.g. 42.5)` shows that decimals are
accepted. `(must be >0)` states the constraint the Step 5 guard enforces.
`(0 for none)` removes the ambiguity about the empty case.

The colons are also padded to the same column, which is why each prompt string
has a different number of trailing spaces. Aligned prompts are easier to scan
and make the program look deliberate rather than assembled. Count the spaces
carefully when you copy — the alignment is the point of the step.

> **▶ Run checkpoint:** Click **Run**. The banner and all five prompts should look new, but the report at the end is still Chapter 4's `--- Summary ---` block. That is next.

## Step 4 — Replace the summary with an aligned report

In `main.cpp`, find this comment:

```cpp
    // Both operands are double, so this is real division, not integer division.
```

Delete that line and everything below it, down to and including this line:

```cpp
    double percentage = 0.0;
```

In the space where those two lines were, enter:

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

    // A zero denominator is explained, not silently reported as 0%.
```

**Why:** This is the chapter's main technique. `std::setw(16)` sets the
**field width** for the next value only: the label is printed into a
sixteen-character space. `std::left` makes it left-aligned within that space
instead of right-aligned, which is the default. Together they guarantee the
values all start at column 17, no matter whether the label is `Student` or
`Points possible`.

`std::setw` applies to exactly one value and then resets, which is why it is
repeated on every line — unlike `std::fixed` and `std::setprecision`, which are
sticky and so are set once, on the first numeric line. That asymmetry between
sticky and one-shot manipulators is worth remembering; it is a common source of
confusion.

Notice the report also breaks `Total earned` out as its own row rather than
showing the arithmetic inline the way Chapter 4 did. In a column layout, one
value per row reads better than a parenthetical.

## Step 5 — Explain the zero-points case

In `main.cpp`, find the line that computes the percentage inside the `if`:

```cpp
        percentage = totalEarned / pointsPossible * 100.0;
```

Replace that single line with this:

```cpp
        double percentage = totalEarned / pointsPossible * 100.0;
        std::cout << std::left << std::setw(16) << "Percentage"
                  << percentage << "%\n";
    } else {
        std::cout << "Percentage      not available\n";
        std::cout << "  An assignment worth 0 points has no percentage,\n";
        std::cout << "  because a score cannot be divided by zero.\n";
```

Now find the old summary block, which the new report has replaced, and delete all of it:

```cpp

    std::cout << "\n--- Summary ---\n";
    std::cout << "Student:    " << studentName << "\n";
    std::cout << "Assignment: " << assignmentName << "\n";
    std::cout << "Earned:     " << totalEarned << " (" << pointsEarned
              << " + " << bonusPoints << " bonus)\n";
    std::cout << "Possible:   " << pointsPossible << "\n";
    std::cout << "Percentage: " << std::fixed << std::setprecision(1)
              << percentage << "%\n";
```

Finally, the report needs a closing rule below the percentage. Find the end of `main`:

```cpp
    return 0;
```

Directly above it, add:

```cpp
    std::cout << "-------------------------------------\n";
```

**Why:** Chapter 4 guarded against division by zero but reported the result as
`0.0%`, which is a lie: an assignment worth zero points does not have a
percentage of zero, it has no percentage at all. Saying `not available` and
then explaining why is honest, and it teaches the user something instead of
leaving them to wonder why their score vanished.

Note also that `percentage` is now declared *inside* the `if` block, rather
than before it. It is only needed there, and a variable declared in the
smallest scope that needs it cannot be accidentally used — or accidentally
trusted — anywhere else. Chapter 4 had to declare it outside and initialize it
to `0.0` precisely because the old code printed it unconditionally; now that
printing happens only where the value exists, the initialization is
unnecessary.

> **▶ Run checkpoint:** Click **Run** and work through the test plan below in the Terminal.

## Test plan

**1. Normal case.** `Ada Lovelace`, `Analytical Engine Essay`, `42.5`, `50`,
`2.5`:

```text
-------------------------------------
  GRADE REPORT
-------------------------------------
Student         Ada Lovelace
Assignment      Analytical Engine Essay
Points earned   42.5
Bonus points    2.5
Total earned    45.0
Points possible 50.0
-------------------------------------
Percentage      90.0%
-------------------------------------
```

Check that every value starts in the same column, including after the long
label `Points possible`.

**2. Zero points possible.** Enter `0` for points possible. The report should
end with the `not available` message and its two explanatory lines, and no
percentage.

**3. A long name.** Enter a student name of twenty or more characters. The
label column must stay sixteen wide and the value must still start at
column 17 — `setw` pads short labels but never truncates long values.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] Every prompt states a unit, an example, or a valid range.
- [ ] The prompt colons line up in a single column.
- [ ] All report values start in the same column, for both short and long
      labels.
- [ ] Entering `0` for points possible prints the `not available` explanation
      and no percentage.
- [ ] The computed percentage is identical to what Chapter 4 produced for the
      same inputs — the interface changed, the arithmetic did not.

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
4. Enter the commit message **Complete Chapter 5 Grade Calculator v0.4**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 5 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
