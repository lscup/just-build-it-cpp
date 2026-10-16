# Chapter 8 — Using Library Functions

## Learning Objectives

When you finish this chapter you will be able to:

- Call a function, and identify its arguments and return value. *(SLO 1.3)*
- Include the correct header for a standard library facility. *(SLO 1.3)*
- Use the mathematical functions in `<cmath>`, including the rounding family. *(SLO 1.3, 1.7)*
- Use `std::min` and `std::max` to express a clamping policy in one line. *(SLO 1.7)*
- Use the character classification functions in `<cctype>`. *(SLO 1.3)*
- Generate pseudorandom numbers with `<random>`. *(SLO 1.7)*
- Read a function's documentation and determine how to call it. *(SLO 1.7)*
- Build Grade Calculator v0.7, resolving the 89.95 problem from Chapter 6.

---

## 8.1 Functions, from the Caller's Side

You have been calling functions since Chapter 3 — `std::getline` is one. This chapter makes the idea explicit and puts the standard library to work. Chapter 9 shows you how to write your own.

A **function** is a named piece of code that performs a task. You **call** it by writing its name followed by parentheses:

```cpp
double root = std::sqrt(16.0);
```

Three things are happening. `std::sqrt` is the function's name. `16.0` is the **argument** — the information you hand it. And the function **returns** a value, 4.0, which is stored in `root`.

The essential idea is that **you do not need to know how it works.** Somebody has already written a correct, tested square-root routine. Using it is faster than writing one, and more importantly it is more likely to be right. This is what a library is for.

---

## 8.2 Arguments, Parameters, and Return Values

Three terms that are easy to blur:

An **argument** is the value you pass at the call site. A **parameter** is the name the function uses for it internally. A **return value** is the result handed back.

```cpp
double area = std::pow(radius, 2.0);
```

`radius` and `2.0` are arguments. Inside `std::pow`, they have parameter names you never see. The result comes back and is stored.

Some functions take several arguments, separated by commas, and **order matters**: `std::pow(2.0, 10.0)` is 1024, while `std::pow(10.0, 2.0)` is 100.

Some functions return nothing. `std::getline(std::cin, name)` does its work by modifying `name` rather than returning a value.

**A returned value that you do not use is discarded.** Writing `std::sqrt(16.0);` on a line by itself computes the root and throws it away. That is legal, useless, and usually a mistake.

---

## 8.3 Headers and the Standard Library

The **standard library** is the collection of facilities every C++ implementation provides. To use one, include its **header**:

| Header | Provides |
|---|---|
| `<iostream>` | `std::cin`, `std::cout` |
| `<string>` | `std::string`, `std::getline` |
| `<iomanip>` | `std::setw`, `std::setprecision`, `std::fixed` |
| `<cmath>` | mathematical functions |
| `<algorithm>` | `std::min`, `std::max`, and much more |
| `<cctype>` | character classification |
| `<random>` | pseudorandom number generation |
| `<limits>` | type limits, and `std::cin.ignore`'s argument |

Appendix D Section D.4 gives the rule: **include what you use.** If your file names `std::sqrt`, include `<cmath>` — even if some other header you included happens to provide it. Relying on an indirect include means your file breaks when an unrelated header changes.

The headers beginning with `c` — `<cmath>`, `<cctype>` — come from the C language. That is why their functions have terse names like `pow` and `isalpha` rather than the fuller style of the rest of the library.

---

## 8.4 Mathematical Functions

`<cmath>` provides the mathematics.

| Function | Returns | Example | Result |
|---|---|---|---|
| `std::sqrt(x)` | square root | `std::sqrt(16.0)` | `4.0` |
| `std::pow(x, y)` | x raised to y | `std::pow(2.0, 10.0)` | `1024.0` |
| `std::abs(x)` | absolute value | `std::abs(-7.5)` | `7.5` |
| `std::round(x)` | nearest whole number | `std::round(89.95)` | `90.0` |
| `std::floor(x)` | largest whole number ≤ x | `std::floor(89.95)` | `89.0` |
| `std::ceil(x)` | smallest whole number ≥ x | `std::ceil(89.95)` | `90.0` |

```text
sqrt(16)     4.0000
pow(2,10)    1024.0000
abs(-7.5)    7.5000
```

Trigonometric and logarithmic functions are there too — `std::sin`, `std::cos`, `std::log`, `std::exp` — and none of them appear in this book's project.

---

## 8.5 Rounding, Minimum, and Maximum

Two small tools that resolve two problems you have been carrying.

### Rounding to a chosen number of decimal places

`std::round` rounds to a whole number. To round to one decimal place, use the standard trick: **multiply, round, divide.**

```cpp
double rounded = std::round(value * 10.0) / 10.0;
```

For two decimal places, use 100.0. For three, 1000.0.

### The 89.95 problem, resolved

Chapter 6 Section 6.12 left you with a genuine dilemma. A percentage of 89.95 *displays* as `90.0` under `setprecision(1)`, but compares as less than 90.0 — so the report says 90.0 and the student gets a B.

Two policies were on the table. Grade the stored value and show more decimals, or **round first and grade what you display.** Here is the second, working:

```cpp
double percentage = 89.95;
double rounded = std::round(percentage * 10.0) / 10.0;

std::cout << "raw     >= 90.0 ? " << (percentage >= 90.0) << "\n";
std::cout << "rounded >= 90.0 ? " << (rounded >= 90.0) << "\n";
```

```text
raw     >= 90.0 ?    false
rounded >= 90.0 ?    true
```

Rounding once, early, and then using the rounded value for **both** the display and the comparison means the number shown is the number graded. No student can ever hold a printout that disagrees with their letter.

From v0.7 onward the Grade Calculator does exactly this. Notice where the fix lives: not in the comparison, and not in the formatting, but in a decision to compute the reported value once and use it everywhere. That is a design fix, which is what Chapter 6 predicted.

### Clamping with `std::min` and `std::max`

From `<algorithm>`:

```cpp
std::min(150.0, 100.0)     // 100.0
std::max(0.0, -5.0)        // 0.0
```

```text
min(150.0,100.0) 100.0
max(0.0,-5.0)    0.0
```

`std::min` is exactly what the bonus-point cap needs. Chapter 4 asked you to decide whether a bonus may push a percentage past 100. If your answer was no, the entire policy is one line:

```cpp
double reported = capAt100 ? std::min(raw, 100.0) : raw;
```

Compare with the hand-written form:

```cpp
double reported = raw;
if (capAt100 && raw > 100.0) {
    reported = 100.0;
}
```

Four lines against one, and the one-line version names the operation. **Both arguments to `std::min` must be the same type** — `std::min(raw, 100)` fails to compile because `raw` is a `double` and `100` is an `int`. Write `100.0`.

---

## 8.6 Character Functions

`<cctype>` classifies and converts single characters.

| Function | True when |
|---|---|
| `std::isdigit(c)` | c is `'0'` through `'9'` |
| `std::isalpha(c)` | c is a letter |
| `std::isspace(c)` | c is a space, tab, or newline |
| `std::isupper(c)` / `std::islower(c)` | c is upper or lower case |
| `std::toupper(c)` / `std::tolower(c)` | returns the converted character |

```text
isdigit('7') true
isalpha('7') false
toupper('a') A
```

Two quirks catch people. **These functions return an `int`, not a `bool`** — zero for false, nonzero for true. `if (std::isdigit(c))` works fine, but comparing to `true` is unreliable.

And **`std::toupper` returns an `int`**, so printing it directly shows a number:

```cpp
std::cout << std::toupper('a');                      // prints 65
std::cout << static_cast<char>(std::toupper('a'));   // prints A
```

Both are consequences of Section 3.6: a `char` *is* a small integer, and these C-inherited functions work in integers.

You can accept either case for a menu choice with one call:

```cpp
if (std::toupper(choice) == 'Y') { ... }
```

---

## 8.7 Random Numbers

Computers produce **pseudorandom** numbers — a sequence that looks random but is generated deterministically from a starting **seed**. Same seed, same sequence.

The modern approach uses `<random>`:

```cpp
#include <random>

std::random_device seedSource;
std::mt19937 generator(seedSource());
std::uniform_int_distribution<int> roll(1, 6);

int value = roll(generator);      // 1 through 6, each equally likely
```

Three pieces: a **seed source**, a **generator** producing raw random bits, and a **distribution** shaping them into the range you want.

This is more setup than the older `rand()` you may see elsewhere, and it is worth it — `rand()` has genuinely poor statistical properties and awkward range behavior. Appendix D excludes it.

**Seeding fixed makes results reproducible**, which is exactly what you want while testing:

```cpp
std::mt19937 generator(12345);    // same sequence every run
```

The Grade Calculator does not use random numbers. They appear here because generating test data is a real need, and because Chapter 16 will have you produce repeatable test cases.

---

## 8.8 Timing with `clock`

`<ctime>` lets you measure elapsed processor time:

```cpp
#include <ctime>

std::clock_t start = std::clock();
// ... work ...
double seconds = static_cast<double>(std::clock() - start) / CLOCKS_PER_SEC;
```

Chapter 17 uses this to compare linear and binary search on the same data — which turns a claim about efficiency into a measurement.

---

## 8.9 Reading Library Documentation

You cannot memorize the standard library, and nobody does. What you need is the ability to read a function's description and work out how to call it.

Documentation gives you a **signature**:

```cpp
double round(double x);
```

Read it in three parts. The **return type** comes first — `double`, so it gives back a floating-point number. The **name** is next. The **parameters** are in parentheses — one `double`.

That signature answers three questions: what do I pass, what do I get back, and what header do I need. When you look up a function, get those three and you can use it.

Two habits are worth forming. **Check the header** — documentation always names it, and a missing include is the most common error when trying something new. And **check the edge cases** — what does this return for zero, for a negative value, for an empty string? Documentation usually says, and it is the part people skip.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `error: 'sqrt' was not declared in this scope` | Missing `#include <cmath>` | Add the header |
| `error: 'min' was not declared in this scope` | Missing `#include <algorithm>` | Add the header |
| `error: no matching function for call to 'min(double, int)'` | Arguments have different types | Write `100.0`, not `100` |
| `std::toupper('a')` prints `65` | It returns an `int` | Wrap in `static_cast<char>(...)` |
| `std::round(89.95)` gives `90`, not `89.95` | `round` goes to a whole number | Multiply by 10, round, divide by 10 |
| Random values are the same every run | Fixed seed | Seed from `std::random_device` |
| Random values differ every run during testing | Seeded from `random_device` | Use a fixed seed while testing |
| A computed value is discarded | Return value not stored | Assign it to something |

---

## Design Notes

**Prefer a library function to your own.** `std::round` is correct, tested, and instantly recognizable. Your hand-rolled version is none of those things.

**Round once, as early as the value is final.** Rounding in two places invites the two results to disagree. The Grade Calculator computes a rounded percentage once and uses it for the report and the letter grade both.

**Let a function name a policy.** `std::min(raw, 100.0)` says *capped at 100* more clearly than four lines of `if`.

**Include what you use.** One header per facility you name, grouped and ordered per Appendix D Section D.4.

---

## Grade Calculator v0.7 — Rounding and Robustness

### What v0.7 does

Everything v0.6 did, with two corrections: the percentage is rounded once and graded as rounded, and the bonus-point cap policy from Chapter 4 is finally implemented.

### The program

```cpp
// Grade Calculator v0.7 - Chapter 8
// Correct rounding and a documented bonus-point cap policy.
// New this version: std::round, std::min, library functions replace hand-rolled logic.
//
// POLICY DECISION (documented per Chapter 4): this gradebook CAPS the reported
// percentage at 100. Bonus points can rescue a low score but cannot produce a
// grade above the maximum. Set CAP_AT_100 to false for uncapped reporting.
//
// Run: click Run in StudySite and use the embedded Terminal.

#include <cmath>
#include <iostream>
#include <iomanip>
#include <limits>
#include <string>

const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
const std::string SENTINEL = "done";
const bool CAP_AT_100 = true;

int main() {
    std::cout << "=== GRADE CALCULATOR v0.7 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);

    std::cout << "\nType " << SENTINEL << " as the assignment name when finished.\n\n";

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
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

        totalEarned += pointsEarned + bonusPoints;
        totalPossible += pointsPossible;
        ++assignmentCount;

        std::cout << "  Recorded.\n\n";
        std::cout << "Assignment name (or " << SENTINEL << "): ";
        std::getline(std::cin, assignmentName);
    }

    std::cout << "\n--- COURSE REPORT ---\n";
    std::cout << "Student:     " << studentName << "\n";
    std::cout << "Assignments: " << assignmentCount << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Total:       " << totalEarned << " / " << totalPossible << "\n";

    if (assignmentCount == 0 || totalPossible <= 0.0) {
        std::cout << "No course grade is available yet.\n";
        return 0;
    }

    double rawPercentage = totalEarned / totalPossible * 100.0;

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
    return 0;
}
```

### Expected output

With `Ada`, then `Homework 1` 10/10 bonus 5, then `done`:

```text
--- COURSE REPORT ---
Student:     Ada
Assignments: 1
Total:       15.0 / 10.0
Percentage:  100.0%
Grade:       A
Note: raw score was 150.0%, capped at 100% by course policy.
```

### What to notice

**The rounded value is used for both the report and the letter grade.** That single decision closes the 89.95 problem. Trace it: 89.95 rounds to 90.0, which satisfies `>= A_CUTOFF`, so the student sees 90.0 and receives an A. The number displayed is the number graded.

**The cap is one line, and it is conditional on a named constant.** Changing course policy means editing `CAP_AT_100` — one word — rather than rewriting logic.

**The cap is applied before rounding.** Order matters here: capping at 100 and then rounding gives 100.0; rounding 150.0 first and then capping gives the same answer in this case but not in every case. Applying the policy to the raw value, then rounding for presentation, is the order that always makes sense.

**The raw value is still reported when it was capped.** Hiding the fact that a cap applied would leave a user puzzled about their missing bonus.

**The guard returns early.** `if (assignmentCount == 0 || totalPossible <= 0.0) { ...; return 0; }` handles the impossible cases first and lets the main logic run unindented — the guard-clause pattern from Appendix D Section D.5.

### Your StudySite Lab — Round and Cap the Grade

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.7
- **Starting point:** Your committed Chapter 7 v0.6 program (one file, sentinel loop, accumulators).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### What you will build

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

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-6) |

When you are finished your project still has **one** `.cpp` file.

#### How to use these steps

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

#### StudySite workflow

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

#### Step 1 — Document the policy and include `<cmath>`

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

#### Step 2 — Add the policy constant and update the banner

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

#### Step 3 — Tidy the instructions and remove two stale comments

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

#### Step 4 — Replace the running total with a brief acknowledgement

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

#### Step 5 — Flatten the decision with an early return

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

#### Step 6 — Cap, round, then grade

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

#### Test plan

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

#### Check your work

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

#### Save this checkpoint

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

#### Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 8 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. The rounding family

```cpp
#include <cmath>
#include <iomanip>
#include <iostream>

int main() {
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "round(89.95) " << std::round(89.95) << "\n";
    std::cout << "floor(89.95) " << std::floor(89.95) << "\n";
    std::cout << "ceil(89.95)  " << std::ceil(89.95) << "\n";
    return 0;
}
```

**Expected output:**

```text
round(89.95) 90.0
floor(89.95) 89.0
ceil(89.95)  90.0
```

*Try:* Predict all three for `-2.5` before running. Does `round` go toward zero or away from it?

### 2. Rounding to one decimal place

```cpp
#include <cmath>
#include <iomanip>
#include <iostream>

int main() {
    double p = 89.95;
    double rounded = std::round(p * 10.0) / 10.0;

    std::cout << std::boolalpha << std::fixed << std::setprecision(1);
    std::cout << "value shown:      " << rounded << "\n";
    std::cout << "raw >= 90.0 ?     " << (p >= 90.0) << "\n";
    std::cout << "rounded >= 90.0 ? " << (rounded >= 90.0) << "\n";
    return 0;
}
```

**Expected output:**

```text
value shown:      90.0
raw >= 90.0 ?     false
rounded >= 90.0 ? true
```

*Try:* Change `p` to `89.94` and rerun. Which line changes, and is that the behavior you want?

### 3. Clamping

```cpp
#include <algorithm>
#include <iomanip>
#include <iostream>

int main() {
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "min(150.0, 100.0) " << std::min(150.0, 100.0) << "\n";
    std::cout << "max(0.0, -5.0)    " << std::max(0.0, -5.0) << "\n";
    return 0;
}
```

**Expected output:**

```text
min(150.0, 100.0) 100.0
max(0.0, -5.0)    0.0
```

*Try:* Change `100.0` to `100` and rebuild. Read the error carefully — it is the type-mismatch message from Common Errors. Then clamp a value into the range 0 to 100 using both functions in one expression.

### 4. Character classification

```cpp
#include <cctype>
#include <iostream>

int main() {
    std::cout << std::boolalpha;
    std::cout << "isdigit('7') " << (std::isdigit('7') != 0) << "\n";
    std::cout << "isalpha('7') " << (std::isalpha('7') != 0) << "\n";
    std::cout << "toupper('a') " << static_cast<char>(std::toupper('a')) << "\n";
    return 0;
}
```

**Expected output:**

```text
isdigit('7') true
isalpha('7') false
toupper('a') A
```

*Try:* Remove the `static_cast` from the last line. Why does it print a number? Chapter 3 Section 3.6 has the answer.

### 5. Reproducible random numbers

```cpp
#include <iostream>
#include <random>

int main() {
    std::mt19937 generator(12345);          // fixed seed
    std::uniform_int_distribution<int> score(60, 100);

    for (int k = 0; k < 5; ++k) {
        std::cout << score(generator) << " ";
    }
    std::cout << "\n";
    return 0;
}
```

*Try:* Run it three times. The values are identical every time. Now change the seed to `54321` and run again. Then replace the fixed seed with `std::random_device{}()` and run three times. Which behavior do you want while testing, and which in a finished program?

### 6. Read a signature

Each of these is a real standard library signature. For each, say what you would pass, what you would get back, and which header you need.

```cpp
double pow(double base, double exponent);
int toupper(int c);
const double& min(const double& a, const double& b);
size_t string::length() const;
```

### 7. Replace hand-written code with library calls

Rewrite each using a standard library function, and name the header.

```cpp
double result = value;
if (value < 0.0) {
    result = -value;
}
```

```cpp
double capped = raw;
if (capped > 100.0) {
    capped = 100.0;
}
```

```cpp
double whole = static_cast<int>(value + 0.5);
```

For the third one: does your library replacement behave identically for negative values? Test it with `-2.5` and explain any difference.

---

## Summary

- A **function** is a named piece of code performing a task. You pass **arguments** and usually receive a **return value**. You do not need to know how it works.
- Include the **header** for every facility you name. `<cmath>`, `<algorithm>`, `<cctype>`, `<random>`, `<ctime>`.
- `<cmath>` provides `sqrt`, `pow`, `abs`, and the rounding family: `round`, `floor`, `ceil`.
- **Round to a chosen number of decimal places** by multiplying, rounding, and dividing.
- **Round once, then use the rounded value for both display and comparison.** This resolves the 89.95 problem from Chapter 6: the number shown becomes the number graded.
- `std::min` and `std::max` from `<algorithm>` express clamping in one line. Both arguments must be the same type.
- `<cctype>` classifies characters. These functions return `int`, not `bool`, and `toupper` needs a cast before printing.
- `<random>` produces **pseudorandom** numbers from a **seed**, a **generator**, and a **distribution**. A fixed seed gives reproducible results, which is what testing wants.
- Reading a **signature** tells you what to pass, what you get back, and which header you need.

---

## Key Terms

**argument** — a value passed to a function at the call site.

**call** — to invoke a function by name.

**distribution** — an object shaping raw random values into a desired range.

**function** — a named piece of code performing a task.

**generator** — an object producing a sequence of pseudorandom values.

**header** — a file declaring library facilities, brought in with `#include`.

**parameter** — the name a function uses internally for an argument it receives.

**pseudorandom** — generated deterministically from a seed but statistically resembling randomness.

**return value** — the result a function hands back to its caller.

**seed** — the starting value determining a pseudorandom sequence.

**signature** — a function's return type, name, and parameter list.

**standard library** — the collection of facilities every C++ implementation provides.

---

**Next:** Chapter 9 turns the tables — instead of calling functions, you will write them. The Grade Calculator is rebuilt from the structure chart you drew in Chapter 5, one function per box, and gains a menu so it no longer runs once and exits. Grade Calculator v1.0.
