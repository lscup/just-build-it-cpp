# Chapter 04 Lab — Calculate Percentages

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.3
- **Starting point:** Your committed Chapter 3 v0.2 program (one file, reads and echoes one assignment).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Your program stores numbers but does not yet do arithmetic with them. In this
chapter it starts calculating: it accepts bonus points, adds them to the score,
and reports a percentage formatted to one decimal place. Two traps appear here
that catch nearly everyone — integer division silently throwing away the
fraction, and dividing by zero — and you will handle both deliberately. By the
end you will have:

1. A third numeric prompt for bonus points.
2. A `totalEarned` value combining the score and the bonus.
3. A percentage computed with real (floating-point) division, guarded so it is
   never computed when `pointsPossible` is zero.
4. Output formatted with `std::fixed` and `std::setprecision(1)`, so a
   percentage always shows exactly one decimal.

> **Design note:** bonus points are added to points *earned* but not to points
> *possible*, so a percentage above 100 is possible. This version reports it
> uncapped on purpose. Chapter 8 revisits that policy.

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

## Step 1 — Update the comment header and include `<iomanip>`

In `main.cpp`, find the first three comment lines:

```cpp
// Grade Calculator v0.2 - Chapter 3
// Reads one named assignment and echoes a formatted summary.
// New this version: typed variables, std::getline for names.
```

Replace it with:

```cpp
// Grade Calculator v0.3 - Chapter 4
// Adds bonus points and a percentage calculation.
// New this version: floating-point division, output formatting.
// Design note: bonus points are added to points EARNED but not to points
// POSSIBLE, so a percentage above 100 is possible. v0.3 reports it uncapped.
```

Now find the `<iostream>` include and add the new one directly below it:

```cpp
#include <iostream>
```

Directly below it, add:

```cpp
#include <iomanip>
```

**Why:** `std::fixed` and `std::setprecision` are declared in `<iomanip>`
("input/output manipulators"). Without the include the compiler reports that
`std::setprecision` is not declared, which is the same class of error as
forgetting `<string>` in Chapter 3. The design note now lives in the file
header because a decision about *policy* — whether a percentage may exceed
100 — belongs with the code that implements it, where the next reader will
find it.

## Step 2 — Update the banner version

In `main.cpp`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.2 ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.3 ===\n\n";
```

**Why:** The banner names the version so that when a student shows you their
output you can both tell which checkpoint they are running. Update it every
chapter.

## Step 3 — Remove two comments that have served their purpose

In `main.cpp`, find this comment and delete it:

```cpp
    // Names may contain spaces, so getline is required here.
```

Find this comment and delete it too:

```cpp
    // Points are double, not int: partial credit such as 8.5 is common.
```

**Why:** Both comments explained a decision you have now internalized —
`getline` for names, `double` for points. A comment that restates what the
code plainly says becomes noise, and noise is what stops people reading
comments at all. Delete explanatory comments once the explanation has landed;
keep the ones that record a decision you could not infer from the code, like
the design note in the header.

> **▶ Run checkpoint:** Click **Run**. The program should behave exactly as it did in Chapter 3, with the new version number in the banner. Nothing has changed functionally yet.

## Step 4 — Read the bonus points

In `main.cpp`, find the three lines that read the points possible:

```cpp
    double pointsPossible = 0.0;
    std::cout << "Points possible: ";
    std::cin >> pointsPossible;
```

Directly below it, add:

```cpp

    double bonusPoints = 0.0;
    std::cout << "Bonus points (0 if none): ";
    std::cin >> bonusPoints;
```

**Why:** The prompt says `(0 if none)` because a prompt that gives no guidance
leaves the user guessing whether to type `0`, press Enter, or type `none`. Only
one of those works. Telling the user what to type for the empty case costs
eight characters and prevents the most common input mistake.

## Step 5 — Compute the total and the percentage

In `main.cpp`, find the line that reads the bonus points:

```cpp
    std::cin >> bonusPoints;
```

Directly below it, add:

```cpp

    double totalEarned = pointsEarned + bonusPoints;

    // Both operands are double, so this is real division, not integer division.
    double percentage = 0.0;
    if (pointsPossible > 0.0) {
        percentage = totalEarned / pointsPossible * 100.0;
    }
```

**Why:** Two things are happening, and both are the chapter's real content.

First, **division**. `totalEarned / pointsPossible` divides one `double` by
another, which is real division and keeps the fraction. Had both values been
`int`, C++ would perform *integer* division and throw the remainder away —
`8 / 10` would be `0`, and the percentage would come out as `0` instead of
`80`. The reason this program uses `double` for points is as much about this
division as about accepting `8.5` as input.

Second, the **guard**. `if (pointsPossible > 0.0)` prevents a division by
zero, which for floating-point numbers does not crash but silently produces
`inf` or `nan` — values that then contaminate everything they touch and print
as meaningless text. Because `percentage` was initialized to `0.0` at its
declaration, skipping the calculation leaves a sensible value behind rather
than garbage.

## Step 6 — Report the total, the possible, and the percentage

In `main.cpp`, find the score line in the summary:

```cpp
    std::cout << "Score:      " << pointsEarned << " / " << pointsPossible << "\n";
```

Replace that one line with these five:

```cpp
    std::cout << "Earned:     " << totalEarned << " (" << pointsEarned
              << " + " << bonusPoints << " bonus)\n";
    std::cout << "Possible:   " << pointsPossible << "\n";
    std::cout << "Percentage: " << std::fixed << std::setprecision(1)
              << percentage << "%\n";
```

**Why:** The summary now shows the arithmetic rather than just the result:
`Earned: 9.5 (8.5 + 1 bonus)` lets the user verify the total themselves, which
is what makes output trustworthy. `std::fixed` tells the stream to use fixed
rather than scientific notation, and `std::setprecision(1)` fixes the number of
digits after the decimal point at one — so `80` prints as `80.0` and
`83.33333` as `83.3`. Note that these two manipulators are **sticky**: once
set, they affect every later floating-point value on that stream, which is why
they appear on the last line rather than the first.

Note also that the statement spans two lines. A long chain of `<<` can be
broken wherever you like; the compiler does not care, and the indentation
lines the continuation up under the first value for readability.

> **▶ Run checkpoint:** Click **Run** and work through the test plan below in the Terminal.

## Test plan

Run the program three times with these inputs.

**1. Normal case with a bonus.** `Ada Lovelace`, `Analytical Engine Essay`,
`8.5`, `10`, `1`:

```text
--- Summary ---
Student:    Ada Lovelace
Assignment: Analytical Engine Essay
Earned:     9.5 (8.5 + 1 bonus)
Possible:   10
Percentage: 95.0%
```

**2. No bonus.** Same, but `0` for the bonus — `Earned: 8.5 (8.5 + 0 bonus)`
and `Percentage: 85.0%`.

**3. Zero points possible.** Enter `0` for points possible. The percentage
must print `0.0%`, not `inf` or `nan`. This is the guard from Step 5 doing its
job; without it this run would produce nonsense.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] A percentage always shows exactly one digit after the decimal point.
- [ ] Entering `0` for points possible prints `0.0%` and never `inf` or `nan`.
- [ ] The `Earned:` line shows the total, the original score, and the bonus.
- [ ] A bonus large enough to exceed the points possible produces a
      percentage above 100, and the program still exits normally.

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
4. Enter the commit message **Complete Chapter 4 Grade Calculator v0.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 4 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
