# Chapter 7 — Iteration

## Learning Objectives

When you finish this chapter you will be able to:

- Write `while`, `do/while`, and `for` loops, and choose appropriately among them. *(SLO 1.3, 1.4)*
- Distinguish counter-controlled from sentinel-controlled repetition. *(SLO 1.4)*
- Use accumulators and counters to build running totals. *(SLO 1.3, 1.7)*
- Write and trace nested loops. *(SLO 1.4)*
- Use `break` and `continue`, and explain why they should be used sparingly. *(SLO 1.3)*
- Diagnose infinite loops and off-by-one errors. *(SLO 1.6)*
- Build Grade Calculator v0.6, and explain why points-based grading *is* the accumulator pattern.

---

## 7.1 The `while` Statement

Chapter 5 named three control structures. You have sequence and selection. This chapter is **repetition**, the last one — and after it, Course I is essentially complete as a language matter. Everything remaining organizes what you can already express.

The simplest loop:

```cpp
while (condition) {
    // repeats while the condition is true
}
```

```cpp
int i = 1;
while (i <= 5) {
    std::cout << i << " ";
    ++i;
}
```

```text
1 2 3 4 5
```

The condition is tested **before** each pass. If it is false initially, the body never runs at all.

Three things must be present, and forgetting any one of them is a bug:

1. **Initialize** something before the loop — here, `i = 1`.
2. **Test** it in the condition — `i <= 5`.
3. **Change** it inside the body — `++i`.

Omit step 3 and `i` stays 1 forever. The condition never becomes false. That is an **infinite loop**, and Section 7.8 covers it.

---

## 7.2 Counter-Controlled and Sentinel-Controlled Loops

Loops divide into two kinds by how they know when to stop.

**Counter-controlled** repetition runs a known number of times:

```cpp
int count = 1;
while (count <= assignmentCount) {
    // process assignment number `count`
    ++count;
}
```

**Sentinel-controlled** repetition runs until a special value appears. You do not know in advance how many passes there will be:

```cpp
std::string name;
std::cout << "Assignment name (or 'done'): ";
std::getline(std::cin, name);

while (name != "done") {
    // process this assignment
    std::cout << "Assignment name (or 'done'): ";
    std::getline(std::cin, name);
}
```

The value `"done"` is the **sentinel** — a value that means "stop", chosen so it cannot be confused with real data. An assignment is unlikely to be named `done`; a sentinel of `0` for a score would be a poor choice, since 0 is a real score.

Notice the shape of the sentinel loop: **read once before the loop, then read again at the end of the body.** That first read is called a *priming read*, and without it the condition has nothing to test on the first pass. Forgetting it is a common early mistake.

Grade Calculator v0.6 uses exactly this structure, because a student may have any number of assignments.

---

## 7.3 The `do/while` Statement

A `do/while` tests the condition **after** the body, so the body always runs at least once:

```cpp
int n = 100;
do {
    std::cout << "body ran with n=" << n << "\n";
} while (n < 5);
```

```text
body ran with n=100
```

The condition was false from the start, and the body still ran once.

Note the semicolon after `while (n < 5);` — it is required here and forbidden after a plain `while`, which is a small inconsistency worth remembering.

Use `do/while` when the action must happen at least once: prompting for input you will validate, showing a menu before asking for a choice. Use `while` otherwise. In practice `while` is far more common.

---

## 7.4 The `for` Statement

When a loop is counter-controlled, `for` gathers all three parts into one line:

```cpp
for (initialization; condition; update) {
    // body
}
```

```cpp
for (int k = 1; k <= 5; ++k) {
    std::cout << k << " ";
}
```

```text
1 2 3 4 5
```

This is exactly the `while` loop from Section 7.1, rearranged. The advantage is that all three parts sit together where you can see them, so a missing update is obvious rather than hidden twenty lines down.

The loop variable declared in the initialization exists **only inside the loop** — that is Section 6.4's scope rule, and it is a feature. It cannot leak, and you can reuse `k` in the next loop without conflict.

### Counting from zero

C++ programmers conventionally count from 0:

```cpp
for (int k = 0; k < 5; ++k) {      // runs 5 times: 0, 1, 2, 3, 4
```

Note `<` rather than `<=`. With `k < 5` starting from 0, the loop runs exactly 5 times. This convention exists because array indices start at 0, as Chapter 11 will show, so `for (int k = 0; k < size; ++k)` visits every element exactly once.

---

## 7.5 Choosing the Right Loop

| Use | When |
|---|---|
| `for` | You know how many passes, or you are stepping through a range |
| `while` | Repetition depends on a condition, and may not run at all |
| `do/while` | The body must run at least once |

All three are interchangeable in principle. Choosing the one that matches your intent tells a reader what you meant.

---

## 7.6 Nested Loops

A loop inside a loop. The inner loop completes fully for each single pass of the outer:

```cpp
for (int r = 1; r <= 3; ++r) {
    for (int c = 1; c <= 3; ++c) {
        std::cout << r * c << "\t";
    }
    std::cout << "\n";
}
```

```text
1	2	3
2	4	6
3	6	9
```

The outer loop runs 3 times; the inner runs 3 times per outer pass; the body executes 9 times. **The pass counts multiply.**

Nested loops become the natural tool in Chapter 11, where a roster of students each having several assignments is a two-dimensional structure: outer loop over students, inner loop over assignments.

---

## 7.7 Altering Loop Flow

Two statements change the normal course of a loop.

**`break`** exits the loop immediately:

```cpp
while (true) {
    std::string line = readLine("Choice: ");
    if (line == "quit") {
        break;
    }
    // handle the choice
}
```

**`continue`** skips the rest of the current pass and goes to the next:

```cpp
for (int k = 0; k < count; ++k) {
    if (pointsPossible[k] <= 0.0) {
        continue;          // skip ungraded items
    }
    // process this one
}
```

Both are legitimate and both are easy to overuse. A loop with several `break`s and `continue`s scattered through it has many exit points, and following it means holding all of them in mind at once.

**Prefer a clear condition to a `break` where you can.** `while (name != "done")` says what it means; `while (true)` with a `break` buried inside does not.

> **`goto` is excluded from this book.** C++ has it. It can jump anywhere, which is precisely what structured programming was invented to prevent, and Appendix D Section D.11 excludes it. Every use has a clearer structured form.

---

## 7.8 Infinite Loops

An **infinite loop** never terminates. The three common causes:

**The update is missing.**

```cpp
int i = 1;
while (i <= 5) {
    std::cout << i << " ";      // no ++i — runs forever
}
```

**The update moves the wrong way.**

```cpp
for (int k = 5; k > 0; ++k) {   // k grows; condition never fails
```

**The condition can never become false.**

```cpp
double x = 0.1;
while (x != 1.0) {              // floating-point never lands exactly on 1.0
    x += 0.1;
}
```

That third one is Chapter 6 Section 6.12 again: **never use `==` or `!=` on floating-point values.** Written as `while (x < 1.0)` it terminates.

If your program hangs, press **Ctrl+C** to stop it. Then check: is the loop variable updated? Does the update move toward the condition failing? Can the condition become false at all?

A trace table of the first three passes finds nearly every infinite loop in under a minute.

---

## 7.9 Accumulators, Counters, and Running Totals

This section is the heart of the chapter for the Grade Calculator.

An **accumulator** is a variable that builds a total across passes. A **counter** counts passes. Both must be **initialized before the loop** — an uninitialized accumulator starts at garbage, and Section 3.2 warned about exactly this.

```cpp
double totalEarned = 0.0;      // accumulator
double totalPossible = 0.0;    // accumulator
int assignmentCount = 0;       // counter

// inside the loop, for each assignment:
totalEarned += pointsEarned + bonusPoints;
totalPossible += pointsPossible;
++assignmentCount;
```

Trace it with three assignments — 9/10, 84/100, and 18/20:

| Pass | earned | possible | totalEarned | totalPossible | percentage so far |
|---|---|---|---|---|---|
| start | — | — | 0 | 0 | — |
| 1 | 9 | 10 | 9 | 10 | 90.00% |
| 2 | 84 | 100 | 93 | 110 | 84.55% |
| 3 | 18 | 20 | 111 | 130 | 85.38% |

```text
after item 1: 9/10 = 90%
after item 2: 93/110 = 84.5455%
after item 3: 111/130 = 85.3846%
```

### Why this matters more than it looks

Look at that final row. The course percentage is `totalEarned / totalPossible × 100`. Two running totals, one division.

**Points-based grading *is* the accumulator pattern.** There is nothing else to it. This is why Course I can build a genuinely useful grade calculator with only the tools you now have, and why the procedural code in Chapters 9 through 12 is honest rather than a straw man.

It is also worth noticing what this pattern *cannot* do. Every assignment contributes to one pair of totals, so every point counts the same regardless of what kind of work it came from. If exams were meant to count 50% of the course and homework 30%, two running totals could not express it — you would need separate totals per category, combined by weight afterward.

That is weighted grading, the requirement your Chapter 1 specification deferred. Nothing in Course I will need it. Chapter 20 is where the accumulator pattern finally runs out, and the answer to what replaces it is the reason Course II exists.

---

## 7.10 Loop Design and Off-by-One Errors

An **off-by-one error** runs a loop one time too many or too few. It is the most common loop bug, and it is silent.

```cpp
for (int k = 0; k < 5; ++k)     // runs 5 times: 0 1 2 3 4
for (int k = 0; k <= 5; ++k)    // runs 6 times: 0 1 2 3 4 5
```

```text
k < 5 runs:  0 1 2 3 4
k <= 5 runs: 0 1 2 3 4 5
```

One character apart. In Chapter 11 that extra pass reads past the end of an array, which is a genuine defect and the first seeded bug in Chapter 16's debugging lab.

**Trace the first and last passes by hand.** Write down what the loop variable is on the first pass and on the last, and confirm both are what you intended. Two lines of a trace table catch nearly every off-by-one error, and they cost far less than finding one later.

For the standard idiom, memorize the pairing: **start at 0, test with `<`, and the loop runs exactly as many times as the limit.**

---

## Common Errors and Warnings

| What you see or observe | Cause | Fix |
|---|---|---|
| The program hangs | Infinite loop | Ctrl+C; check the update moves toward the condition failing |
| The loop runs one time too many | Off-by-one, `<=` where `<` was meant | Trace the first and last passes |
| The loop never runs | Condition false initially | Check the initial value; consider `do/while` |
| The total is nonsense | Accumulator not initialized | Set it to 0 before the loop |
| The total keeps growing across students | Accumulator not reset | Reinitialize inside the outer loop |
| `while (x != 1.0)` never ends | `!=` on a floating-point value | Use `<` or `>` |
| A `getline` after the loop returns nothing | Leftover newline from `>>` | `std::cin.ignore(...)` — Section 3.12 |
| `error: 'k' was not declared in this scope` | Used a `for` variable after the loop | Declare it before the loop |
| The loop body runs once, always | Stray `;` after `while (...)` | Delete the semicolon |

---

## Design Notes

**Initialize accumulators immediately before the loop**, not at the top of the function. The distance between initialization and use is where reset bugs live.

**Choose a sentinel that cannot be real data.** `"done"` is a safe assignment name. `0` is a real score and a terrible sentinel.

**Trace before you run.** Three rows of a trace table is faster than three rebuild cycles.

**Prefer a meaningful condition to `while (true)` plus `break`.** The condition documents the loop's purpose in the place a reader looks first.

---

## Grade Calculator v0.6 — Multiple Assignments

### What v0.6 does

Accepts any number of named assignments using a sentinel, accumulating totals as it goes, reporting the running percentage after each entry and a final course grade at the end.

This is the first version that handles a realistic amount of data.

### The program

```cpp
// Grade Calculator v0.6 - Chapter 7
// Accepts many named assignments until a sentinel, then reports the course grade.
// New this version: sentinel-controlled while loop, accumulators.
// Key idea: points-based grading IS the accumulator pattern - a running total
// of points earned divided by a running total of points possible.
// Run: click Run in StudySite and use the embedded Terminal.

#include <iostream>
#include <iomanip>
#include <limits>
#include <string>

const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
const std::string SENTINEL = "done";

int main() {
    std::cout << "=== GRADE CALCULATOR v0.6 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);

    std::cout << "\nEnter assignments one at a time.\n";
    std::cout << "Type " << SENTINEL << " as the assignment name when finished.\n\n";

    // Accumulators: these two running totals are the entire grading algorithm.
    double totalEarned = 0.0;
    double totalPossible = 0.0;
    int assignmentCount = 0;

    std::string assignmentName;
    std::cout << "Assignment name (or " << SENTINEL << "): ";
    std::getline(std::cin, assignmentName);

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

    if (assignmentCount == 0) {
        std::cout << "No assignments entered, so there is no course grade yet.\n";
    } else if (totalPossible > 0.0) {
        double percentage = totalEarned / totalPossible * 100.0;
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
    return 0;
}
```

### Expected output

With `Ada`, then `Homework 1` 9/10 bonus 0, `Midterm` 84/100 bonus 5, then `done`:

```text
--- COURSE REPORT ---
Student:     Ada
Assignments: 2
Total:       98.0 / 110.0
Percentage:  89.1%
Grade:       B
```

### What to notice

**The `std::cin.ignore` line is finally necessary.** Chapter 3 Section 3.12 explained the `>>`-then-`getline` trap, and v0.2 avoided it by ordering the reads so it never arose. A loop forces them to interleave: three `>>` reads, then a `getline` at the bottom. Without the `ignore`, that `getline` receives the leftover newline, the sentinel test sees an empty string rather than a name, and the loop exits after one assignment. Remove the line and watch it happen — it is worth thirty seconds.

**Two accumulators and a counter, all initialized before the loop.** They are declared immediately above it, per the Design Notes.

**The priming read is before the loop**, and the matching read is the last statement of the body. Both prompts are identical, which is how a sentinel loop should look.

**Three cases at the end, not one.** No assignments entered, all assignments worth zero points, and the normal case. Chapter 5's desk-check habit is what surfaces the first two.

### Your StudySite Lab — Process Multiple Assignments

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.6
- **Starting point:** The working Chapter 6 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### Required work

1. Use `done` as the sentinel for assignment entry.
2. Maintain total earned, total possible, assignment count, and bonus-assignment count.
3. Display a running percentage after each assignment.
4. After the sentinel, display the final course percentage and letter grade.
5. Handle no assignments and all-zero-point assignments without dividing by zero.


#### Verification

- Three assignments produce correct running totals.
- Entering `done` immediately reports no assignments.
- Names still work after numeric input; no `getline` is skipped.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This avoids
   creating files with names such as `_imported` when the same path is already
   open.
3. Click **Load from GitHub**, select **grade-calculator-1436**, and click each source, header,
   or documentation file needed for this chapter. Confirm the editor shows the
   expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. For a
   multi-file program, keep every source and header file needed by the build
   open in the editor.
5. Click **Run**. Read compiler messages and program output in the embedded
   Terminal, and type program input there when prompted.
6. Fix every compiler error and warning, then complete the verification list.
7. Use the Tutor with the current code or Terminal output when you need help.

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the editor.
   **Save to GitHub includes every open editor file**, so close scratch files
   and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **grade-calculator-1436** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 7 Grade Calculator v0.6**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1436** contains the Chapter 7 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. The same loop, three ways

```cpp
#include <iostream>

int main() {
    std::cout << "while: ";
    int i = 1;
    while (i <= 5) { std::cout << i << " "; ++i; }

    std::cout << "\nfor:   ";
    for (int k = 1; k <= 5; ++k) { std::cout << k << " "; }

    std::cout << "\ndo:    ";
    int j = 1;
    do { std::cout << j << " "; ++j; } while (j <= 5);

    std::cout << "\n";
    return 0;
}
```

**Expected output:**

```text
while: 1 2 3 4 5 
for:   1 2 3 4 5 
do:    1 2 3 4 5 
```

*Try:* Change all three to start at 5 and count down to 1.

### 2. `do/while` runs at least once

```cpp
#include <iostream>

int main() {
    int n = 100;

    while (n < 5) {
        std::cout << "while body ran\n";
    }

    do {
        std::cout << "do body ran with n=" << n << "\n";
    } while (n < 5);

    return 0;
}
```

**Expected output:**

```text
do body ran with n=100
```

*Try:* Explain in one sentence why the `while` produced nothing.

### 3. Off by one

```cpp
#include <iostream>

int main() {
    std::cout << "k < 5:  ";
    for (int k = 0; k < 5; ++k) { std::cout << k << " "; }
    std::cout << "\nk <= 5: ";
    for (int k = 0; k <= 5; ++k) { std::cout << k << " "; }
    std::cout << "\n";
    return 0;
}
```

**Expected output:**

```text
k < 5:  0 1 2 3 4 
k <= 5: 0 1 2 3 4 5 
```

*Try:* Write a loop printing exactly ten values starting at 1. Which comparison did you use, and why?

### 4. The accumulator pattern

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double earned[3]   = {9.0, 84.0, 18.0};
    double possible[3] = {10.0, 100.0, 20.0};

    double totalEarned = 0.0;
    double totalPossible = 0.0;

    std::cout << std::fixed << std::setprecision(2);
    for (int k = 0; k < 3; ++k) {
        totalEarned   += earned[k];
        totalPossible += possible[k];
        std::cout << "after item " << k + 1 << ": "
                  << totalEarned << "/" << totalPossible << " = "
                  << totalEarned / totalPossible * 100.0 << "%\n";
    }
    return 0;
}
```

**Expected output:**

```text
after item 1: 9.00/10.00 = 90.00%
after item 2: 93.00/110.00 = 84.55%
after item 3: 111.00/130.00 = 85.38%
```

*Try:* Move the two accumulator initializations *inside* the loop. What happens, and what does the final percentage become? This is the reset bug from Common Errors.

### 5. Nested loops

```cpp
#include <iostream>

int main() {
    for (int r = 1; r <= 3; ++r) {
        for (int c = 1; c <= 3; ++c) {
            std::cout << r * c << "\t";
        }
        std::cout << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
1	2	3
2	4	6
3	6	9
```

*Try:* Extend to 5 by 5. How many times does the inner body run in total? Verify by adding a counter.

### 6. Find the infinite loop

Each of these never ends. Say why, and give the smallest fix. Do not run them without being ready to press Ctrl+C.

```cpp
int i = 1;
while (i <= 5) {
    std::cout << i << " ";
}
```

```cpp
for (int k = 5; k > 0; ++k) {
    std::cout << k << " ";
}
```

```cpp
double x = 0.0;
while (x != 1.0) {
    x += 0.1;
}
```

```cpp
int count = 0;
while (count < 10);
{
    ++count;
}
```

### 7. Design a loop from a specification

Write a program that reads scores until the user enters `-1`, then reports how many scores were entered, their total, their average, the highest, and the lowest.

Before you write code:

- What is your sentinel, and why is `-1` a safe choice here when `0` would not be?
- How do you initialize "highest" and "lowest" so the first real score sets them correctly?
- What should the program report if the very first entry is `-1`?

Answer all three in writing, then implement it and test the no-scores case first.

---

## Summary

- **Repetition** is the third structure of structured programming. Every loop needs three parts: **initialize**, **test**, and **change**.
- `while` tests before the body. `do/while` tests after, so the body always runs at least once. `for` gathers all three parts on one line and suits counter-controlled loops.
- **Counter-controlled** loops run a known number of times; **sentinel-controlled** loops run until a special value appears. A sentinel loop needs a **priming read** before it and a matching read at the end of the body.
- Choose a sentinel that cannot be mistaken for real data.
- **Nested loops** multiply their pass counts.
- `break` exits a loop; `continue` skips to the next pass. Prefer a clear condition where you can. `goto` is excluded from this book.
- **Infinite loops** come from a missing update, an update in the wrong direction, or a condition that can never be false — including `!=` on floating-point values.
- An **accumulator** builds a total across passes; a **counter** counts them. Both must be initialized before the loop, and reset in the right place when nested.
- **Points-based grading is the accumulator pattern**: two running totals and one division. It is also the reason weighted grading cannot be expressed this way — which is Chapter 20's problem.
- **Off-by-one errors** are the commonest loop bug and are silent. Trace the first and last passes. The standard idiom is: start at 0, test with `<`.

---

## Key Terms

**accumulator** — a variable that builds a running total across loop passes.

**break** — a statement exiting a loop immediately.

**continue** — a statement skipping the rest of the current pass.

**counter** — a variable counting the number of loop passes.

**counter-controlled** — repetition running a known number of times.

**do/while** — a loop testing its condition after the body, so the body always runs once.

**for** — a loop gathering initialization, condition, and update into one line.

**infinite loop** — a loop whose condition never becomes false.

**iteration** — one pass through a loop body; also, repetition in general.

**loop control variable** — the variable a loop tests and updates.

**nested loop** — a loop contained within another loop.

**off-by-one error** — a loop running one pass too many or too few.

**priming read** — an input read before a sentinel loop, so the condition has something to test.

**sentinel** — a special input value signalling the end of data.

**sentinel-controlled** — repetition running until a sentinel value appears.

**while** — a loop testing its condition before each pass.

---

**Next:** Chapter 8 introduces the standard library's functions — rounding, minimum and maximum, character tests, and random numbers. You will replace your hand-written rounding with `std::round` and finally implement the bonus-point cap policy you chose in Chapter 4. Grade Calculator v0.7.
