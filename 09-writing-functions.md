# Chapter 9 — Writing Functions

## Learning Objectives

When you finish this chapter you will be able to:

- Define a function with parameters and a return value. *(SLO 1.4)*
- Explain the difference between a prototype and a definition, and say when each is needed. *(SLO 1.4)*
- Explain pass by value and predict what a function can and cannot change. *(SLO 1.4)*
- Write `void` functions and explain when a return value is unnecessary. *(SLO 1.4)*
- Describe the scope and lifetime of a local variable. *(SLO 1.3)*
- Convert a structure chart into a set of functions. *(SLO 1.4, 1.5)*
- Write documentation comments in the form Appendix D requires. *(SLO 1.6)*
- Test a function individually with hand-computed cases. *(SLO 1.6)*
- Build Grade Calculator v1.0 — the modular rebuild, with a menu.

---

## 9.1 Defining a Function

Chapter 8 had you calling functions other people wrote. Now you write your own, and the Grade Calculator gets its first real structure.

A **function definition** has four parts:

```cpp
double computePercentage(double earned, double possible) {
    return earned / possible * 100.0;
}
```

| Part | In the example |
|---|---|
| Return type | `double` |
| Name | `computePercentage` |
| Parameter list | `(double earned, double possible)` |
| Body | the block, containing `return` |

Call it exactly as you called library functions:

```cpp
double pct = computePercentage(84.0, 100.0);    // 84.0
```

The value passed at the call site is an **argument**. The name inside the function is a **parameter**. Chapter 8 Section 8.2 drew that distinction from the caller's side; now you are on the other side of it.

---

## 9.2 Prototypes, Definitions, and Order

C++ reads a file top to bottom. A function must be **declared** before it is called.

The simplest approach is to define every function above `main`:

```cpp
#include <iostream>

double computePercentage(double earned, double possible) {
    return earned / possible * 100.0;
}

int main() {
    std::cout << computePercentage(84.0, 100.0) << "\n";
    return 0;
}
```

Sometimes that ordering is inconvenient. A **prototype** declares a function without defining it — the signature followed by a semicolon:

```cpp
#include <iostream>

double computePercentage(double earned, double possible);    // prototype

int main() {
    std::cout << computePercentage(84.0, 100.0) << "\n";
    return 0;
}

double computePercentage(double earned, double possible) {   // definition
    return earned / possible * 100.0;
}
```

A prototype is a promise: *this function exists somewhere with this signature.* The compiler accepts calls on that promise. If nobody keeps it — if no definition is ever supplied — the **linker** fails, not the compiler.

That is the division from Chapter 2 Section 2.2.4, now something you can trigger deliberately. It is worth doing once: write a prototype, call it, define nothing, and read the message. It looks nothing like a compiler error, and knowing why saves confusion later.

Prototypes become essential in Chapter 10, when your program spans several files.

---

## 9.3 Parameters and Pass by Value

By default C++ uses **pass by value**: the function receives a *copy* of each argument. Changing the parameter does not affect the caller's variable.

```cpp
#include <iostream>

void tryToChange(double points) {
    points = 999.0;                             // changes the copy only
    std::cout << "inside the function: " << points << "\n";
}

int main() {
    double score = 84.0;
    tryToChange(score);
    std::cout << "back in main:       " << score << "\n";
    return 0;
}
```

```text
inside the function: 999
back in main:       84
```

The copy really did change — the function is not failing to assign. The
assignment simply had no effect on `score`, because the function was never
given `score` in the first place. It was given a copy.

This is a safety feature. A function cannot corrupt the caller's data by accident, so you can call one without worrying about what it might do to your variables.

It is also a limitation. A function that genuinely needs to modify its caller's variable cannot do it this way. Chapter 10 introduces **pass by reference** for exactly that case, and the Grade Calculator needs it for input validation.

---

## 9.4 Return Values and `void` Functions

A function returns a value with `return`:

```cpp
char assignLetterGrade(double percentage) {
    if (percentage >= 90.0) { return 'A'; }
    if (percentage >= 80.0) { return 'B'; }
    if (percentage >= 70.0) { return 'C'; }
    if (percentage >= 60.0) { return 'D'; }
    return 'F';
}
```

**`return` exits the function immediately.** That is why this version needs no `else` — reaching the second `if` already means the first was false. Compare with the chained form in Chapter 6 Section 6.9; both are correct, and this one is shorter because `return` does the work `else` was doing.

A function that does something rather than computing something has return type **`void`**:

```cpp
void printReport(const std::string& student, double percentage, char letter) {
    std::cout << "Student:    " << student << "\n";
    std::cout << "Percentage: " << percentage << "%\n";
    std::cout << "Grade:      " << letter << "\n";
}
```

A `void` function needs no `return` statement, though a bare `return;` may be used to exit early.

> **`main` is special.** It returns `int`, and reaching its closing brace without a `return` implicitly returns 0. Every other non-`void` function must return a value on every path — failing to do so is undefined behavior, and `-Wall` warns about it.

---

## 9.5 Local Variables, Scope, and Lifetime

A variable declared inside a function is **local** to it. Chapter 6 Section 6.4 introduced scope for blocks; the same rule applies here, with one addition.

**Scope** is *where* a name is visible. **Lifetime** is *when* the variable exists.

```cpp
double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;    // created here
    return std::round(raw * 10.0) / 10.0;
}                                              // destroyed here
```

`raw` exists only while the function runs. Each call creates a fresh one; nothing carries over between calls.

Two functions may use the same local name without interfering:

```cpp
double computePercentage(double earned, double possible) {
    double result = earned / possible * 100.0;
    return result;
}

char assignLetterGrade(double percentage) {
    char result = 'F';                     // a different variable entirely
    // ...
    return result;
}
```

This independence is what makes functions genuinely modular. You can write, read, and test one without holding the rest of the program in your head.

---

## 9.6 Modular Design in Practice

Here is the rebuild, and the discipline that makes it safe.

Appendix D Section D.5 states the rule: **a function does one thing.** If you find yourself writing a comment that says "now for the second part," that is a second function asking to exist. If you cannot describe what a function does in one sentence without the word "and", split it.

### Refactor incrementally, never in one leap

The completeness rule for this book says no chapter leaves the project in a state that does not build. That constrains *how* you refactor, not just what you end up with.

**Extract one function, recompile, and rerun. Then the next.**

1. Copy the letter-grade chain out of `main` into a new function.
2. Replace the original code with a call.
3. Rebuild. Run. Confirm the output is unchanged.
4. Only then extract the next one.

At every point in that sequence you have a working program. If step 3 fails, you know the cause is the twenty lines you just moved.

The tempting alternative — rewrite everything, then compile — produces a screen of errors with no way to tell which change caused which. Appendix D Section D.5 and the Chapter 2 habit of compiling early and often are the same advice, and this is where it starts to pay.

---

## 9.7 From Structure Chart to Function Set

In Chapter 5 you drew a structure chart. Figure 5.3 had four boxes under the root: **Read Assignment**, **Compute Percentage**, **Assign Letter Grade**, and **Print Report**.

Those boxes are your functions. The conversion is mechanical:

| Structure chart box | Function |
|---|---|
| Read Assignment | `void readAssignment(double&, double&, int&)` |
| Compute Percentage | `double computePercentage(double, double)` |
| Assign Letter Grade | `char assignLetterGrade(double)` |
| Print Report | `void printReport(const std::string&, double, double, int)` |

This is why Chapter 5 was worth the effort. The design decisions — what the parts are, which calls which — were made on paper when they were cheap to change. Chapter 9 is transcription.

Notice how the return types fall out of the box names. A box that *computes* something returns a value. A box that *does* something is `void`. If a box needs both, it is probably two boxes.

---

## 9.8 Commenting and Documenting Functions

Appendix D Section D.3 requires a documentation comment on every function another file can call. The form:

```cpp
/**
 * Converts points to a percentage, capped and rounded by course policy.
 *
 * @param  earned    total points earned, including any bonus
 * @param  possible  total points possible
 * @return the percentage, rounded to one decimal place
 * @pre    possible > 0; the caller must check this first
 */
double computePercentage(double earned, double possible);
```

| Tag | Use |
|---|---|
| `@param name` | What one parameter means, including restrictions on its value |
| `@return` | What the return value means |
| `@throws Type` | An exception this may raise — from Chapter 24 |
| `@pre` | A precondition the caller must satisfy, which the function does not check |

`@pre` deserves attention. `computePercentage` divides by `possible`. It could check for zero itself, but then every caller would have to interpret whatever it returned in that case. Stating the precondition instead makes the contract explicit: **the caller checks, the function assumes.**

Either choice is defensible. What matters is writing down which one you made — an unstated assumption is a defect waiting for the right input.

---

## 9.9 Testing Functions Individually

A function small enough to describe in one sentence is small enough to test on its own. Doing that is what makes modular design pay.

Write a short `main` that calls one function with values whose answers you worked out by hand:

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>

double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;
    return std::round(std::min(raw, 100.0) * 10.0) / 10.0;
}

char assignLetterGrade(double percentage) {
    if (percentage >= 90.0) { return 'A'; }
    if (percentage >= 80.0) { return 'B'; }
    if (percentage >= 70.0) { return 'C'; }
    if (percentage >= 60.0) { return 'D'; }
    return 'F';
}

int main() {                       // a temporary main, used only for testing
    std::cout << computePercentage(84.0, 100.0) << "\n";     // expect 84
    std::cout << computePercentage(0.0, 100.0) << "\n";      // expect 0
    std::cout << computePercentage(15.0, 10.0) << "\n";      // expect 100
    std::cout << assignLetterGrade(90.0) << "\n";            // expect A
    std::cout << assignLetterGrade(89.9) << "\n";            // expect B
    return 0;
}
```

```text
84
0
100
A
B
```

**Choose cases at the boundaries**, exactly as Chapter 5's desk-check habit taught: zero, the cutoff, just below the cutoff, and the impossible-looking case. The ordinary case in the middle almost never finds a bug.

Chapter 16 turns this into a systematic practice with a proper test harness. For now, hand-checking each function as you write it is enough — and it is far more than most people do.

---

## 9.10 Worked Examples

Four small functions worth having.

### Comparing floating-point values safely

Chapters 1, 3, and 6 all warned that `==` is unreliable on floating-point values. Here is the standard technique, finally:

```cpp
/**
 * Reports whether two floating-point values are close enough to treat as equal.
 * @param  a          first value
 * @param  b          second value
 * @param  tolerance  how close counts as equal; defaults to one millionth
 */
bool nearlyEqual(double a, double b, double tolerance = 0.000001) {
    return std::abs(a - b) < tolerance;
}
```

```text
0.1+0.2 == 0.3           false
nearlyEqual(0.1+0.2,0.3) true
nearlyEqual(0.3, 0.4)    false
```

Never `a == b`. Always "are they closer together than I care about?"

### Validating a menu choice

```cpp
/** Returns the first character of a line, or '?' if the line was empty. */
char readMenuChoice() {
    std::cout << "1) Add assignment   2) View report   3) Quit\n";
    std::cout << "Choice: ";
    std::string line;
    std::getline(std::cin, line);
    return line.empty() ? '?' : line[0];
}
```

Reading the whole line with `getline` and taking its first character sidesteps the `>>`-and-`getline` trap from Section 3.12 entirely. There is no `>>`, so there is no stray newline.

### Clamping into a range

```cpp
/** Restricts a value to lie between low and high inclusive. */
double clamp(double value, double low, double high) {
    return std::min(std::max(value, low), high);
}
```

Two library calls from Chapter 8, composed.

### Applying a bonus

```cpp
/** Adds bonus points to a raw score. Bonus defaults to none. */
double applyBonus(double pointsEarned, double bonusPoints = 0.0) {
    return pointsEarned + bonusPoints;
}
```

The `= 0.0` is a **default argument**: callers may omit it. `applyBonus(84.0)` and `applyBonus(84.0, 0.0)` are equivalent. Chapter 10 covers default arguments properly; this one is here because v1.5 will use it to extend an interface without breaking existing calls.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `error: 'computePercentage' was not declared in this scope` | Called before declaring | Define it above `main`, or add a prototype |
| `undefined reference to 'computePercentage'` | Prototype without a definition — a **linker** error | Write the function body |
| `warning: no return statement in function returning non-void` | A path falls off the end | Return a value on every path |
| `warning: parameter 'x' set but not used` | Assigned to a parameter, changing only the copy | Use a reference (Chapter 10) or return a value |
| The caller's variable is unchanged | Pass by value | Return a value, or use a reference |
| `error: too few arguments to function` | Wrong number of arguments | Check the signature |
| `error: 'result' was not declared in this scope` | Used a local outside its function | Return it instead |
| Two `double`s that should match compare unequal | `==` on floating-point | Use `nearlyEqual` |

---

## Design Notes

**One function, one job, one sentence.** If the sentence needs "and", split the function.

**Extract one function at a time and rebuild between each.** The project is never allowed to be broken between two chapters, and it should not be broken between two edits either.

**Document the contract, especially preconditions.** `@pre possible > 0` tells the caller what they are responsible for. Without it, both sides assume the other checked.

**Test each function as you write it**, with boundary values you computed by hand.

**Write functions that return values where you can.** They are easier to test, easier to reason about, and cannot surprise their callers.

---

## Grade Calculator v1.0 — Modular Rebuild

### What v1.0 does

Everything v0.7 did, rebuilt from functions derived from the Chapter 5 structure chart — plus a **menu loop**, so the program no longer runs once and exits.

This is the first version that behaves like an application. The menu shell it gains here remains in every version through Chapter 24.

### Behavior worth stating plainly

v1.0 does not store individual assignments; it keeps running totals, exactly as v0.7 did. Arrays do not arrive until Chapter 11. What changes here is **structure**, not capability — and that is the point. A refactor that alters behavior is a defect, which Chapter 13 will make you prove.

### The program

```cpp
// Grade Calculator v1.0 - Chapter 9
// Same behavior as v0.7, rebuilt from documented functions, plus a menu loop.
// New this version: user-defined functions, a menu that keeps the program running.
// Note: individual assignments are not stored yet (no arrays until Chapter 11),
// so the program keeps running totals only.
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
const bool CAP_AT_100 = true;

/**
 * Adds bonus points to a raw score.
 * @param  pointsEarned  raw points earned, must be >= 0
 * @param  bonusPoints   bonus to add, must be >= 0
 * @return the combined total
 */
double applyBonus(double pointsEarned, double bonusPoints) {
    return pointsEarned + bonusPoints;
}

/**
 * Converts points to a percentage, capped by course policy.
 * @param  earned    total points earned including bonus
 * @param  possible  total points possible, must be > 0
 * @return percentage rounded to one decimal place
 * @pre    possible > 0; the caller must check this first
 */
double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

/**
 * Maps a percentage to a letter grade on the fixed course scale.
 * @param  percentage  a value from 0 upward
 * @return one of A, B, C, D, F
 */
char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}

/**
 * Prompts for and reads one assignment, updating the running totals.
 * @param  totalEarned    running total, updated in place
 * @param  totalPossible  running total, updated in place
 * @param  count          assignment count, updated in place
 */
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

/**
 * Prints the full course report for the current totals.
 */
void printReport(const std::string& student, double earned, double possible, int count) {
    std::cout << "\n--- COURSE REPORT ---\n";
    std::cout << "Student:     " << student << "\n";
    std::cout << "Assignments: " << count << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Total:       " << earned << " / " << possible << "\n";

    if (count == 0 || possible <= 0.0) {
        std::cout << "No course grade is available yet.\n\n";
        return;
    }
    double percentage = computePercentage(earned, possible);
    std::cout << "Percentage:  " << percentage << "%\n";
    std::cout << "Grade:       " << assignLetterGrade(percentage) << "\n\n";
}

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

int main() {
    std::cout << "=== GRADE CALCULATOR v1.0 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);
    std::cout << "\n";

    double totalEarned = 0.0;
    double totalPossible = 0.0;
    int assignmentCount = 0;
    bool running = true;

    while (running) {
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
    }

    printReport(studentName, totalEarned, totalPossible, assignmentCount);
    std::cout << "Goodbye.\n";
    return 0;
}
```

### Expected output

With `Ada`, then `1` and `Homework 1` 9/10 bonus 0, then `1` and `Midterm` 84/100 bonus 5, then `2`, then `3`:

```text
--- COURSE REPORT ---
Student:     Ada
Assignments: 2
Total:       98.0 / 110.0
Percentage:  89.1%
Grade:       B

Goodbye.
```

### What to notice

**Each function came from a box in Figure 5.3.** `readAssignment`, `computePercentage`, `assignLetterGrade`, `printReport`. The design work was done four chapters ago.

**`readAssignment` takes references — `double&` — and this is new.** Chapter 10 explains the syntax properly. What matters now is that pass by value (Section 9.3) could not do this job: the function must update the caller's running totals, and a copy cannot. This is the limitation of Section 9.3 arriving exactly where predicted.

**`printReport` calls `computePercentage`, which calls nothing.** That layering is the structure chart, alive in the code.

**The menu uses `switch` on a `char`.** Chapter 6 Section 6.10 said `switch` cannot handle grade ranges but suits menu choices exactly. Here is the case it was made for.

**`readMenuChoice` uses `getline`, not `>>`.** No `>>` means no stray newline, so the trap from Section 3.12 never arises in the menu.

**`printReport` is called twice** — from the menu and again on exit. That is the value of a function: one definition, several uses, no duplication.

### Your StudySite Lab — Rebuild with Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.0
- **Starting point:** Your committed Chapter 8 v0.7 program (one file, one long `main`).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### What you will build

Your `main` has grown to seventy lines and does five unrelated jobs. This
chapter rebuilds the same behavior out of six small functions, each with one
job and a documentation comment stating what it takes, what it returns, and
what it assumes. Then it adds the thing functions make possible: a **menu
loop**, so the program keeps running and the user chooses what to do next
instead of answering a fixed sequence of questions once.

Nothing about the grading changes. The output for the same inputs is
identical. What changes is that the program becomes something you can read a
piece at a time. By the end you will have:

1. `applyBonus`, `computePercentage`, and `assignLetterGrade` — three pure
   calculations that take values and return values.
2. `readAssignment` — reads one assignment and updates the running totals
   through **reference parameters**.
3. `printReport` and `readMenuChoice` — one prints, one asks.
4. A `main` of about thirty lines: set up, loop on a menu with a `switch`,
   print a final report, exit.

> **Note:** individual assignments are still not stored — there are no arrays
> until Chapter 11 — so the program keeps running totals only. Adding an
> assignment and viewing the report many times is now possible; listing the
> assignments is not, yet.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-9) |

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

#### Step 1 — Update the comment header

In `main.cpp`, find the eight header comment lines above the `Build:` line:

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

Replace it with:

```cpp
// Grade Calculator v1.0 - Chapter 9
// Same behavior as v0.7, rebuilt from documented functions, plus a menu loop.
// New this version: user-defined functions, a menu that keeps the program running.
// Note: individual assignments are not stored yet (no arrays until Chapter 11),
// so the program keeps running totals only.
```

**Why:** The policy block moves out of the header because the policy is about
to live inside `computePercentage`, documented on the function that implements
it. A comment belongs as close as possible to the code it describes. What
replaces it is the new limitation worth recording: no storage of individual
assignments yet.

#### Step 2 — Write `applyBonus`

> **Where these go:** each function in Steps 2-7 is added **above** `int main()`
> and below the constants. Add them in order, so each new one appears directly
> above `int main()` and below the one you added before it. A function must be
> declared before the code that calls it, and `main` calls all of them.

In `main.cpp`, find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Adds bonus points to a raw score.
 * @param  pointsEarned  raw points earned, must be >= 0
 * @param  bonusPoints   bonus to add, must be >= 0
 * @return the combined total
 */
double applyBonus(double pointsEarned, double bonusPoints) {
    return pointsEarned + bonusPoints;
}
```

**Why:** This is the smallest useful function in the program — one line of
arithmetic — and it is worth writing precisely because it is small. The name
says what the operation *means*, where `pointsEarned + bonusPoints` only says
what it does. If the bonus policy ever changes, there is now exactly one place
to change it.

Read the documentation comment carefully, because every function from here on
has one. `@param` describes each input and any constraint on it; `@return`
describes what comes back. Writing this before the body forces you to decide
what the function is responsible for, which is most of the work of designing
one.

#### Step 3 — Write `computePercentage`

Again find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Converts points to a percentage, capped by course policy.
 * @param  earned    total points earned including bonus
 * @param  possible  total points possible, must be > 0
 * @return percentage rounded to one decimal place
 * @pre    possible > 0; the caller must check this first
 */
double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}
```

**Why:** The cap and the rounding from Chapter 8 move in here, unchanged. Now
there is one place in the program that knows how a percentage is produced, and
the policy constant is read at exactly one site.

Note the `@pre` line — a **precondition**. This function divides by
`possible`, so it requires `possible > 0`, and it states that the *caller* must
check. That is a real design decision: the alternative is for the function to
check and return some sentinel value, which pushes the problem to every caller
instead. Either is defensible; what matters is writing down which one you
chose, because a caller cannot guess.

#### Step 4 — Write `assignLetterGrade`

Find the start of `main` once more:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Maps a percentage to a letter grade on the fixed course scale.
 * @param  percentage  a value from 0 upward
 * @return one of A, B, C, D, F
 */
char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}
```

**Why:** Compare this to the `if`/`else if` chain it replaces. There is no
`else if` and no `letter` variable — each test simply **returns** when it
matches. `return` exits the function immediately, so reaching the second `if`
already proves the first was false. The `else` is implied by control flow.

This is the clearest form this logic can take, and it is only available because
the code is in a function. Inside `main` you had to assign to a variable and
carry it along; here the answer leaves the moment it is known. The final
`return 'F';` is the default, reached only when all four tests fail.

#### Step 5 — Write `readAssignment`

Find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Prompts for and reads one assignment, updating the running totals.
 * @param  totalEarned    running total, updated in place
 * @param  totalPossible  running total, updated in place
 * @param  count          assignment count, updated in place
 */
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

**Why:** This is the chapter's most important new idea: the `&` in
`double& totalEarned`. That is a **reference parameter**, and it means the
function receives the caller's actual variable rather than a copy of its value.
`totalEarned += ...` inside this function changes `main`'s `totalEarned`.

Without references this function could not work. A normal parameter is a copy;
adding to the copy would update something that ceases to exist when the
function returns, and `main`'s totals would stay at zero. The three
accumulators must be references because updating them *is* the function's job.

Notice also that this function calls `applyBonus` rather than adding the bonus
itself, and that the prompts and the `std::cin.ignore` call moved in here
wholesale. Everything about reading one assignment now lives in one place.

#### Step 6 — Write `printReport`

Find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Prints the full course report for the current totals.
 */
void printReport(const std::string& student, double earned, double possible, int count) {
    std::cout << "\n--- COURSE REPORT ---\n";
    std::cout << "Student:     " << student << "\n";
    std::cout << "Assignments: " << count << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Total:       " << earned << " / " << possible << "\n";

    if (count == 0 || possible <= 0.0) {
        std::cout << "No course grade is available yet.\n\n";
        return;
    }
    double percentage = computePercentage(earned, possible);
    std::cout << "Percentage:  " << percentage << "%\n";
    std::cout << "Grade:       " << assignLetterGrade(percentage) << "\n\n";
}
```

**Why:** `const std::string& student` is a reference too, but for the opposite
reason. Copying a string means copying its characters, which is wasted work;
passing a reference avoids that. The `const` then promises the function will
not modify it — so the reference is purely an efficiency measure, with no
change in meaning. **`const` reference for input you only read, plain reference
for values you intend to change** is the convention worth internalizing.

The guard clause from Chapter 8 survives as an early `return` from this
function, and the function calls `computePercentage` and `assignLetterGrade`
rather than repeating their logic. This is what the rebuild buys: the report
reads like a description of itself.

#### Step 7 — Write `readMenuChoice`

Find the start of `main` for the last time:

```cpp
int main() {
```

Directly above it, add:

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

**Why:** This reads a whole line with `getline` and returns only its first
character. Reading the line — rather than a single `char` with `>>` — is what
keeps the input buffer clean, so the `getline` inside `readAssignment` is not
derailed by a leftover newline. It is the Chapter 7 lesson applied
structurally: handle input a line at a time and the buffer problem stops
recurring.

`line.empty() ? '?' : line[0]` guards the case where the user just presses
Enter. Reading `line[0]` of an empty string is undefined behavior — it might
appear to work, which is worse than crashing. Returning `'?'` sends it to the
`default` branch and the program asks again.

> **▶ Run checkpoint:** Click **Run**. The program should behave exactly as it did in Chapter 8 — the six new functions are defined but nothing calls them yet. This checkpoint proves all six compile before you rewrite `main` around them.

#### Step 8 — Rebuild `main` around the menu

In `main.cpp`, find the first line inside `main`:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.7 ===\n\n";
```

Delete that line and everything below it (about seventy lines), down to and including this line:

```cpp
    return 0;
```

In the space where that code was, enter this — the whole of the new `main`:

```cpp
    std::cout << "=== GRADE CALCULATOR v1.0 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);
    std::cout << "\n";

    double totalEarned = 0.0;
    double totalPossible = 0.0;
    int assignmentCount = 0;
    bool running = true;

    while (running) {
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
    }

    printReport(studentName, totalEarned, totalPossible, assignmentCount);
    std::cout << "Goodbye.\n";
    return 0;
```

**Why:** `main` is now a description of the program rather than the program
itself: greet, set up the totals, loop until the user quits, print a final
report. Every line of detail lives in a function with a name.

The **menu loop** is the new behavior. `while (running)` keeps going until
something sets `running` to `false`, and the `switch` dispatches on the
character returned by `readMenuChoice`. A `switch` is the natural fit when you
are choosing among a fixed set of discrete values; it reads better than four
chained `if`s comparing the same variable.

Two details that matter. Every `case` ends with `break` — without it, control
**falls through** into the next case and runs its code too, which is a classic
bug and the reason `break` is not optional here. And `default` catches
everything unmatched, so an unexpected keystroke produces a helpful message
rather than silence.

The final `printReport` call after the loop means the student always sees their
grade on the way out, whether or not they chose option 2.

#### Step 9 — Remove the now-unused sentinel

In `main.cpp`, find the `SENTINEL` constant and delete it:

```cpp
const std::string SENTINEL = "done";
```

**Why:** The menu replaced the sentinel: the user now chooses `3` to quit
instead of typing `done` as an assignment name. A constant nothing references
is dead weight that invites the next reader to wonder what it is for. Deleting
code that has stopped being used is part of finishing a change, not an
afterthought.

> **▶ Run checkpoint:** Click **Run** and work through the test plan below in the Terminal.

#### Test plan

**1. The menu works.** Enter student `Ada Lovelace`. You should see the menu.
Choose `2` straight away: the report shows `Assignments: 0` and
`No course grade is available yet.` Then choose `3`: the report prints once
more, followed by `Goodbye.`

**2. Add, view, add, view.** Restart and choose `1`, entering `Essay`, `45`,
`50`, `0`. Choose `2` — total `45.0 / 50.0`, percentage `90.0%`, grade `A`.
Choose `1` again with `Quiz`, `10`, `50`, `0`. Choose `2` — total
`55.0 / 100.0`, `55.0%`, grade `F`. Being able to view a report *between*
entries is the new capability this chapter unlocked.

**3. Invalid input.** At the menu, type `x` and press Enter: `Please enter 1,
2, or 3.` and the menu returns. Then press Enter on its own with no text: the
same message, via the `'?'` from `readMenuChoice`. Neither should crash or
skip a prompt.

**4. Multi-word names still work.** Choose `1` and enter `Final Research
Paper` as the assignment name. It must be stored in full and echoed by the
`Recorded:` line.

**5. Identical results.** Run the same inputs you used in Chapter 8 and
confirm the percentage and grade are the same. This chapter restructured the
program; it must not have changed its answers.

#### Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] `main` is about thirty lines and contains no arithmetic.
- [ ] Each of the six functions has a documentation comment.
- [ ] The three accumulator parameters of `readAssignment` are references
      (`double&`, `int&`), and the totals in `main` actually change.
- [ ] `printReport` takes the student name as a `const std::string&`.
- [ ] Every `case` in the `switch` ends with `break`.
- [ ] Choosing `3` prints the report and then `Goodbye.`
- [ ] `SENTINEL` no longer appears anywhere in the file.
- [ ] The same inputs produce the same grade as your Chapter 8 program.

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
4. Enter the commit message **Complete Chapter 9 Grade Calculator v1.0**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 9 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Your first function

```cpp
#include <iostream>

double computePercentage(double earned, double possible) {
    return earned / possible * 100.0;
}

int main() {
    std::cout << computePercentage(84.0, 100.0) << "\n";
    std::cout << computePercentage(9.0, 10.0) << "\n";
    return 0;
}
```

**Expected output:**

```text
84
90
```

*Try:* Add a third call with `possible` of 0. What happens? Then add a `@pre` comment saying whose responsibility that is.

### 2. Pass by value

```cpp
#include <iostream>

double doubled(double points) {
    points = points * 2.0;
    return points;
}

int main() {
    double score = 84.0;
    double result = doubled(score);
    std::cout << "returned: " << result << "\n";
    std::cout << "original: " << score << "\n";
    return 0;
}
```

**Expected output:**

```text
returned: 168
original: 84
```

*Try:* Explain in one sentence why `score` is unchanged. What would you have to do to change it? Chapter 10 has the answer.

### 3. Comparing floating-point values safely

```cpp
#include <cmath>
#include <iostream>

bool nearlyEqual(double a, double b, double tolerance = 0.000001) {
    return std::abs(a - b) < tolerance;
}

int main() {
    double a = 0.1 + 0.2;
    std::cout << std::boolalpha;
    std::cout << "0.1+0.2 == 0.3           " << (a == 0.3) << "\n";
    std::cout << "nearlyEqual(0.1+0.2,0.3) " << nearlyEqual(a, 0.3) << "\n";
    std::cout << "nearlyEqual(0.3, 0.4)    " << nearlyEqual(0.3, 0.4) << "\n";
    return 0;
}
```

**Expected output:**

```text
0.1+0.2 == 0.3           false
nearlyEqual(0.1+0.2,0.3) true
nearlyEqual(0.3, 0.4)    false
```

*Try:* Call it with a tolerance of `0.2` comparing 0.3 and 0.4. What does that tell you about choosing a tolerance?

### 4. `return` exits immediately

```cpp
#include <iostream>

char assignLetterGrade(double percentage) {
    if (percentage >= 90.0) { return 'A'; }
    if (percentage >= 80.0) { return 'B'; }
    if (percentage >= 70.0) { return 'C'; }
    return 'F';
}

int main() {
    std::cout << assignLetterGrade(95.0) << "\n";
    std::cout << assignLetterGrade(85.0) << "\n";
    std::cout << assignLetterGrade(50.0) << "\n";
    return 0;
}
```

**Expected output:**

```text
A
B
F
```

*Try:* Add `std::cout << "checking B\n";` before the second `if`. Call with 95.0. Does the message print? Why not?

### 5. `void` and early return

```cpp
#include <iostream>

void describe(int count) {
    if (count == 0) {
        std::cout << "No assignments yet.\n";
        return;                     // exit early
    }
    std::cout << count << " assignment(s) recorded.\n";
}

int main() {
    describe(0);
    describe(3);
    return 0;
}
```

**Expected output:**

```text
No assignments yet.
3 assignment(s) recorded.
```

*Try:* Remove the `return;`. What does `describe(0)` print now, and why is that wrong?

### 6. Decompose a long function

This works and does too much. Split it into three functions, each describable in one sentence without "and". Then write a documentation comment for each.

```cpp
#include <iostream>

int main() {
    double earned = 0.0;
    double possible = 0.0;
    std::cout << "Points earned: ";
    std::cin >> earned;
    std::cout << "Points possible: ";
    std::cin >> possible;

    double pct = 0.0;
    if (possible > 0.0) {
        pct = earned / possible * 100.0;
    }

    char letter = 'F';
    if (pct >= 90.0)      { letter = 'A'; }
    else if (pct >= 80.0) { letter = 'B'; }
    else if (pct >= 70.0) { letter = 'C'; }
    else if (pct >= 60.0) { letter = 'D'; }

    std::cout << "Percentage: " << pct << "%\n";
    std::cout << "Grade: " << letter << "\n";
    return 0;
}
```

### 7. Trigger a linker error deliberately

```cpp
#include <iostream>

double mysteryFunction(double x);      // prototype, no definition

int main() {
    std::cout << mysteryFunction(3.0) << "\n";
    return 0;
}
```

Build it. **The message is not a compiler error** — it comes from the linker, and looks completely different from anything in Chapter 2.

- Which of the four translation stages produced it?
- Why did the compiler not object?
- What is the fix?

This is Chapter 2 Section 2.2.4 made real, and it is worth two minutes.

---

## Summary

- A **function definition** has a return type, a name, a parameter list, and a body.
- A **prototype** declares a function without defining it. A prototype with no definition passes the compiler and **fails at the linker**.
- **Pass by value** gives the function a copy. Changing a parameter does not affect the caller. Chapter 10 introduces references for when it must.
- `return` produces a value **and exits immediately**, which is why a chain of `if` statements with `return` needs no `else`.
- A **`void`** function does something rather than computing something. `return;` exits it early.
- **Local variables** have the scope and lifetime of their function. Two functions may reuse a name freely.
- **A function does one thing**, describable in one sentence without "and".
- **Refactor one function at a time, rebuilding between each.** The program should never be broken between two edits.
- A **structure chart box becomes a function.** Boxes that compute return values; boxes that act are `void`.
- Document every function with `@param`, `@return`, and especially `@pre` — preconditions say who is responsible for checking.
- **Test each function individually with boundary values** you computed by hand.
- Compare floating-point values with a **tolerance**, never with `==`.

---

## Key Terms

**default argument** — a parameter value used when the caller omits that argument.

**definition** — a function's full declaration together with its body.

**lifetime** — the period during which a variable exists.

**local variable** — a variable declared inside a function, existing only while it runs.

**modular design** — organizing a program as small parts, each doing one thing.

**parameter** — the name a function uses for a value it receives.

**pass by value** — passing a copy of an argument, so the caller's variable is unaffected.

**precondition** — a requirement the caller must satisfy, stated with `@pre`.

**prototype** — a declaration of a function's signature without its body.

**return** — a statement producing a function's result and exiting it.

**signature** — a function's name and parameter types.

**void** — the return type of a function that returns no value.

---

**Next:** Chapter 10 splits the Grade Calculator across three files, introduces references so a function can genuinely modify its caller's variables, and makes input validation robust enough that no typed input can crash the program. Grade Calculator v1.1.
