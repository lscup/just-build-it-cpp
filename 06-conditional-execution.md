# Chapter 6 — Conditional Execution

## Learning Objectives

When you finish this chapter you will be able to:

- Write Boolean expressions using the relational operators. *(SLO 1.3)*
- Use `if`, `if/else`, and multi-way `if/else if` chains to choose between paths. *(SLO 1.3, 1.4)*
- Combine conditions with `&&`, `||`, and `!`, and explain short-circuit evaluation. *(SLO 1.3)*
- Explain how a block determines the scope of a variable. *(SLO 1.3)*
- Write a `switch` statement and say when it is a better choice than an `if/else if` chain. *(SLO 1.3)*
- Identify and fix the common faults in conditional logic, including boundary errors and floating-point comparison. *(SLO 1.6, 1.7)*
- Build Grade Calculator v0.5, and explain why a percentage that displays as 90.0 may still receive a B.

---

## 6.1 The `bool` Type Revisited

Chapter 5 identified **selection** as one of the three structures of structured programming, and drew it as a diamond. This chapter is the C++ for that diamond.

Everything rests on `bool`, introduced in Section 3.7. A `bool` holds exactly `true` or `false`.

```cpp
bool capAt100 = true;
bool dropLowest = false;
```

Printing a `bool` shows `1` or `0` by default. `std::boolalpha` makes it readable, which is useful while you are learning:

```cpp
std::cout << std::boolalpha;
std::cout << (5 > 3) << "\n";      // true
```

---

## 6.2 Relational Operators and Boolean Expressions

A **relational operator** compares two values and produces a `bool`.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `>` | greater than | `5 > 3` | `true` |
| `<` | less than | `5 < 3` | `false` |
| `>=` | greater than or equal to | `5 >= 5` | `true` |
| `<=` | less than or equal to | `3 <= 5` | `true` |
| `==` | equal to | `5 == 3` | `false` |
| `!=` | not equal to | `5 != 3` | `true` |

An expression producing a `bool` is a **Boolean expression** — the *condition* a selection tests.

> **`=` and `==` are different, and confusing them is legal C++.** A single `=` assigns; a double `==` compares. `if (x = 3)` stores 3 in `x` and is always true. Compiling with `-Wall` warns about this, which is one more reason Appendix D Section D.10 requires you to fix warnings.

---

## 6.3 The Simple `if` Statement

```cpp
if (condition) {
    // runs only when condition is true
}
```

```cpp
if (pointsPossible > 0.0) {
    percentage = totalEarned / pointsPossible * 100.0;
}
```

You have used this since Chapter 4 to guard a division. Now it is formal.

The parentheses around the condition are required. The braces are not, strictly — but Appendix D Section D.1 requires them anyway, and the reason is worth restating:

```cpp
// Do not write this.
if (percentage >= 90.0)
    letter = 'A';
```

The day someone adds a second line to that body and forgets to add braces, the second line runs unconditionally, the program still compiles, and the resulting logic error is invisible. Braces from the start make it impossible.

> **A semicolon after the condition is a silent disaster.** `if (x > 5);` is legal: the `;` is an empty statement forming the entire body, so the block that follows always runs. The compiler accepts it. Section 6.12 returns to this.

---

## 6.4 Compound Statements and Scope

A **block** is statements enclosed in braces, treated as one statement.

A block also defines **scope** — the region where a name exists:

```cpp
if (pointsPossible > 0.0) {
    double percentage = totalEarned / pointsPossible * 100.0;
    std::cout << percentage << "\n";      // fine
}
std::cout << percentage << "\n";          // error: does not exist here
```

`percentage` is created on entering the block and destroyed on leaving it. Using it outside is a compile-time error.

The fix is to declare it where it needs to live:

```cpp
double percentage = 0.0;
if (pointsPossible > 0.0) {
    percentage = totalEarned / pointsPossible * 100.0;
}
std::cout << percentage << "\n";          // fine
```

**Declare a variable in the smallest scope that will hold it.** Appendix D Section D.6 puts it this way: a variable that exists longer than it means anything is an opportunity to misuse it.

---

## 6.5 The `if/else` Statement

```cpp
if (pointsPossible > 0.0) {
    std::cout << "Percentage: " << percentage << "%\n";
} else {
    std::cout << "Percentage: not available\n";
}
```

Exactly one branch runs — never both, never neither. This is the flowchart diamond of Figure 5.1 with both exits labelled.

---

## 6.6 Logical Operators and Compound Conditions

Three operators combine Boolean expressions.

| Operator | Name | True when |
|---|---|---|
| `&&` | AND | both operands are true |
| `\|\|` | OR | at least one operand is true |
| `!` | NOT | the operand is false |

```cpp
if (percentage >= 80.0 && percentage < 90.0) {
    letter = 'B';
}

if (pointsPossible <= 0.0 || pointsEarned < 0.0) {
    std::cout << "Invalid assignment data.\n";
}

if (!scaleIsValid) {
    std::cout << "Please define a grade scale first.\n";
}
```

### Precedence

`!` binds tightest, then `&&`, then `||`. All relational operators bind tighter than any of them, which is why this works without parentheses:

```cpp
if (percentage >= 80.0 && percentage < 90.0)
```

Both comparisons happen before the `&&`. Where a mix of `&&` and `||` appears, add parentheses — Appendix D asks for clarity over minimalism:

```cpp
if ((a && b) || c)      // clearer than a && b || c
```

### The chained comparison trap

Mathematics writes `0 ≤ score ≤ 100`. C++ does not work that way, and the result is not what you would guess:

```cpp
if (0 <= score <= 100)      // WRONG - and always true
```

C++ evaluates left to right. `0 <= score` produces a `bool`, which converts to 1 or 0. Then `1 <= 100` is compared — and that is true no matter what `score` was. A score of 150 or −50 both pass.

Compiling with `-Wall` catches it:

```text
warning: comparison of constant '100' with boolean expression is always true
         [-Wbool-compare]
```

The correct form states both comparisons:

```cpp
if (0 <= score && score <= 100)
```

---

## 6.7 Short-Circuit Evaluation

C++ stops evaluating a compound condition as soon as the answer is settled. This is **short-circuit evaluation**.

For `&&`, if the left operand is false, the right is never evaluated — the result is already false. For `||`, if the left is true, the right is never evaluated.

This is not an optimization detail you can ignore. It is a tool:

```cpp
if (pointsPossible > 0.0 && totalEarned / pointsPossible > 0.9) {
    // ...
}
```

If `pointsPossible` is zero, the left operand is false and **the division never happens**. Reverse the order and the program divides by zero.

**Order your conditions so the check that makes the rest safe comes first.** This pattern appears throughout the Grade Calculator, and it is the reason a great many potential run-time errors never occur.

---

## 6.8 Nested Conditionals

An `if` inside another `if`:

```cpp
if (pointsPossible > 0.0) {
    if (totalEarned > pointsPossible) {
        std::cout << "Note: bonus points pushed this above 100%.\n";
    } else {
        std::cout << "Score is within the normal range.\n";
    }
} else {
    std::cout << "No percentage is available.\n";
}
```

Nesting is sometimes necessary and quickly becomes hard to read. Two levels is usually fine. Three is a signal to reconsider — either combine conditions with `&&`, or extract the inner logic into a function once you reach Chapter 9.

---

## 6.9 Multi-way `if/else if` Chains

For more than two mutually exclusive outcomes, chain the tests:

```cpp
char letter = 'F';
if (percentage >= 90.0) {
    letter = 'A';
} else if (percentage >= 80.0) {
    letter = 'B';
} else if (percentage >= 70.0) {
    letter = 'C';
} else if (percentage >= 60.0) {
    letter = 'D';
}
```

**The first true condition wins, and the rest are skipped.** That is what makes this correct despite each condition looking incomplete. A percentage of 95 satisfies `>= 90`, gets an `A`, and never reaches the `>= 80` test.

### Order matters absolutely

Reverse the chain and it breaks completely:

```cpp
// WRONG
if (percentage >= 60.0) {
    letter = 'D';
} else if (percentage >= 70.0) {
    letter = 'C';
    // ...
}
```

Now 95 satisfies `>= 60` first and gets a `D`. Nothing below is ever reached. This is Exercise 5 from Chapter 5, and it compiles without complaint — a logic error of exactly the kind Section 4.9.3 warned about.

**Order a chain from most restrictive to least.** For grade cutoffs, that means highest first.

### Why `else` matters here

Without `else`, each `if` is independent and every test runs:

```cpp
// WRONG
if (percentage >= 90.0) { letter = 'A'; }
if (percentage >= 80.0) { letter = 'B'; }
if (percentage >= 70.0) { letter = 'C'; }
```

A 95 sets `letter` to `A`, then overwrites it with `B`, then `C`. Everyone gets a C. The `else` is what makes the branches mutually exclusive.

---

## 6.10 The `switch` Statement

When you compare one value against a list of **exact** constants, `switch` is often clearer:

```cpp
switch (letter) {
    case 'A':
        std::cout << "Excellent\n";
        break;
    case 'B':
        std::cout << "Good\n";
        break;
    case 'C':
        std::cout << "Satisfactory\n";
        break;
    default:
        std::cout << "Needs improvement\n";
        break;
}
```

`break` exits the switch. Without it, execution **falls through** into the next case and keeps going — a real source of bugs, and occasionally useful when several cases share behavior:

```cpp
switch (letter) {
    case 'A':
    case 'B':
        std::cout << "Passing with distinction\n";
        break;
    default:
        std::cout << "Other\n";
        break;
}
```

### When `switch` will not work

`switch` requires **integral** values — `int`, `char`, `bool`, or an enumeration — compared against compile-time constants. It cannot test ranges and cannot switch on a `double`.

So this is impossible:

```cpp
switch (percentage) {          // error: percentage is a double
    case >= 90.0:              // error: cases must be constants, not ranges
```

**Grade cutoffs are ranges over a `double`, so letter-grade logic must use an `if/else if` chain.** `switch` earns its place for menu choices, where you compare one `char` against a fixed list — which is exactly how the Grade Calculator uses it from Chapter 9 onward.

---

## 6.11 The Conditional Operator

For choosing between two *values*, C++ offers a compact form:

```cpp
condition ? valueIfTrue : valueIfFalse
```

```cpp
double reported = capAt100 ? std::min(raw, 100.0) : raw;
```

That line appears in Grade Calculator v0.7 and expresses the whole cap policy in one readable statement.

Use it for short value selections. Do not use it to choose between actions, and never nest it — an `if/else` is clearer and Appendix D prefers clarity.

---

## 6.12 Errors in Conditional Statements

Six faults account for most conditional bugs. Four are silent.

### `=` instead of `==`

```cpp
if (letter = 'A') {     // assigns, then is always true
```

Caught by `-Wall`. Fix your warnings.

### A stray semicolon

```cpp
if (percentage >= 90.0);
{
    letter = 'A';       // always runs
}
```

The `;` is the entire body. The block that follows is unconditional. **Silent.**

### Reversed chain order

Covered in Section 6.9. Everyone gets a D. **Silent.**

### Missing `else`

Also Section 6.9. Later assignments overwrite earlier ones. **Silent.**

### Comparing floating-point values with `==`

```cpp
double a = 0.1 + 0.2;
if (a == 0.3) { ... }      // false
```

```text
0.1+0.2 == 0.3 ?      false
0.1+0.2 is exactly 0.30000000000000004
```

Chapters 1 and 3 warned about this; here is where it bites. **Never test floating-point values with `==` or `!=`.** Compare with `<`, `>`, `<=`, `>=`, or against a tolerance — Chapter 9 shows the standard technique. **Silent.**

### Boundary errors — and one worth dwelling on

Does a percentage of exactly 90.0 earn an A or a B? With `>= 90.0`, an A. With `> 90.0`, a B. Both compile. Only one matches your policy.

Now the case that catches nearly everyone. Consider a student whose percentage is 89.95:

```cpp
double percentage = 89.95;
std::cout << std::fixed << std::setprecision(1);
std::cout << "Percentage: " << percentage << "\n";
std::cout << "Gets an A?  " << std::boolalpha << (percentage >= 90.0) << "\n";
```

```text
Percentage: 90.0
Gets an A?  false
```

**The report says 90.0 and the student gets a B.**

Nothing here is broken. `setprecision(1)` rounds *for display only* — it does not change the stored value, which is still 89.95 and genuinely less than 90. But try explaining that to the student holding a printout that says 90.0.

This is a design decision disguised as a formatting detail, and you must choose:

1. **Grade the stored value.** 89.95 is a B, and the report should show more decimal places so the number matches the grade.
2. **Grade the rounded value.** Round to one decimal place *first*, then compare — so the displayed 90.0 is the number actually graded.

Chapter 8 implements option 2 with `std::round`, and from v0.7 onward the Grade Calculator rounds once and grades what it displays. It is worth noticing that the fix belongs in the design, not in the comparison.

---

## Common Errors and Warnings

| What you see or observe | Cause | Fix |
|---|---|---|
| `warning: suggest parentheses around assignment used as truth value` | `=` where `==` was meant | Use `==` |
| `warning: comparison ... is always true [-Wbool-compare]` | Chained comparison such as `0 <= x <= 100` | Write `0 <= x && x <= 100` |
| A branch always runs | Stray `;` after the condition | Delete the semicolon |
| Everyone gets the same grade | Chain ordered least-restrictive first | Order highest cutoff first |
| Later branches overwrite earlier ones | Missing `else` between tests | Chain with `else if` |
| Two equal-looking values compare unequal | `==` on floating-point values | Use `<`, `>`, or a tolerance |
| `error: 'x' was not declared in this scope` | Used a variable outside its block | Declare it in an enclosing scope |
| `error: switch quantity not an integer` | Switched on a `double` | Use an `if/else if` chain |
| A case runs and the next one also runs | Missing `break` | Add `break` to each case |

---

## Design Notes

**Order conditions so the safe one comes first.** Short-circuit evaluation makes `possible > 0.0 && earned / possible > 0.9` safe. The reverse order divides by zero.

**Use `else if` for mutually exclusive outcomes.** Independent `if` statements let more than one branch fire, which is almost never what a grade scale means.

**Decide your boundaries explicitly and write them down.** Is 90.0 an A? Is 89.95? Your specification from Chapter 5 should answer both. If it does not, revise it now.

**Test at the boundary, on both sides.** For a cutoff of 90, test 89.9, 90.0, and 90.1. Chapter 16 makes this systematic; Chapter 5's desk-check habit makes it early.

---

## Grade Calculator v0.5 — Letter Grades

### What v0.5 does

Everything v0.4 did, plus a letter grade from a fixed scale: A at 90, B at 80, C at 70, D at 60, F below.

### The program

```cpp
// Grade Calculator v0.5 - Chapter 6
// Adds a letter grade from a fixed 90/80/70/60 scale.
// New this version: multi-way if/else if chain, named constants.
// Limitation: the cutoffs are hard-coded. Chapter 11 makes them user-defined.
// Run: click Run in StudySite and use the embedded Terminal.

#include <iostream>
#include <iomanip>
#include <string>

// Named constants: changing a cutoff means editing one line, not hunting
// for a magic number inside the conditional chain.
const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;

int main() {
    std::cout << "=== GRADE CALCULATOR v0.5 ===\n\n";

    std::string studentName;
    std::cout << "Student name                : ";
    std::getline(std::cin, studentName);

    std::string assignmentName;
    std::cout << "Assignment name             : ";
    std::getline(std::cin, assignmentName);

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

    if (pointsPossible > 0.0) {
        double percentage = totalEarned / pointsPossible * 100.0;

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
    } else {
        std::cout << "Percentage: not available (0 points possible)\n";
        std::cout << "Grade:      not available\n";
    }
    return 0;
}
```

### Expected output

With `Ada Lovelace`, `Midterm Exam`, `84`, `100`, `5`:

```text
--- GRADE REPORT ---
Student:    Ada Lovelace
Assignment: Midterm Exam
Score:      89.0 / 100.0
Percentage: 89.0%
Grade:      B
```

### What to notice

**The cutoffs are named constants.** Changing the A cutoff to 93 is one edit. If the numbers were written inline, it would be a search through the chain — and Appendix D Section D.6 calls those magic numbers for exactly this reason.

**`letter` starts at `'F'` and the chain has no final `else`.** Anything failing every test keeps the initial value. This is deliberate: the F case needs no test, because F *is* the default.

**The chain runs highest to lowest.** Reverse it and everyone passes with a D.

**Bonus above 100 is reported, not hidden.** The note tells the user why an unusual number appeared.

### The limitation

Every cutoff is compiled into the program. An instructor wanting a plus-minus scale, or a pass/fail scale, cannot have one without editing and rebuilding.

Look at the chain and ask: *what would it take to let the user define their own scale?* With what you know now, the answer is a longer chain — and a longer chain still fixed at compile time. There is no arrangement of `if/else if` that accepts a scale from the user.

That is not a failure of your code. It is a limit of the tool, and Chapter 11 provides the missing one. The cutoffs will become **data** rather than code, the chain will collapse into a short loop, and the same program will handle any scale. Keep this chain in mind; you will delete it with some satisfaction.

### Your StudySite Lab — Assign Letter Grades

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.5
- **Starting point:** The working Chapter 5 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### Required work

1. Add named cutoffs: A `90`, B `80`, C `70`, and D `60`.
2. Use an `if / else if` chain from highest to lowest to assign a `char` letter grade; F is the default.
3. Display the percentage and letter grade together.
4. Keep the raw percentage policy from Chapter 4 for now.


#### Verification

- Test `95`, `85`, `75`, `65`, and `55` percent.
- Test exactly `90.0` and just below `90.0`.
- A score above 100 still receives A and is not hidden.

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
4. Enter the commit message **Complete Chapter 6 Grade Calculator v0.5**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1436** contains the Chapter 6 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Relational and logical operators

```cpp
#include <iostream>

int main() {
    std::cout << std::boolalpha;
    std::cout << "5 > 3         " << (5 > 3) << "\n";
    std::cout << "5 == 3        " << (5 == 3) << "\n";
    std::cout << "true && false " << (true && false) << "\n";
    std::cout << "true || false " << (true || false) << "\n";
    std::cout << "!true         " << (!true) << "\n";
    return 0;
}
```

**Expected output:**

```text
5 > 3         true
5 == 3        false
true && false false
true || false true
!true         false
```

*Try:* Predict `(5 > 3) && (2 > 4)` and `!(5 == 5)` before running them.

### 2. The boundary that looks wrong

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double percentage = 89.95;
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Percentage: " << percentage << "\n";
    std::cout << std::boolalpha;
    std::cout << "Gets an A?  " << (percentage >= 90.0) << "\n";
    return 0;
}
```

**Expected output:**

```text
Percentage: 90.0
Gets an A?  false
```

*Try:* Change the precision to 4 and rerun. Does the report now agree with the grade? Which fix would you rather ship — showing more decimals, or rounding before comparing?

### 3. Floating-point equality

```cpp
#include <iostream>
#include <iomanip>

int main() {
    double a = 0.1 + 0.2;
    std::cout << std::boolalpha;
    std::cout << "0.1+0.2 == 0.3 ? " << (a == 0.3) << "\n";
    std::cout << std::setprecision(17);
    std::cout << "0.1+0.2 is exactly " << a << "\n";
    return 0;
}
```

**Expected output:**

```text
0.1+0.2 == 0.3 ? false
0.1+0.2 is exactly 0.30000000000000004
```

*Try:* Test whether the difference between them is smaller than 0.000001. Does that comparison give the answer you wanted?

### 4. Short-circuit evaluation protects you

```cpp
#include <iostream>

int main() {
    double possible = 0.0;
    double earned = 50.0;

    if (possible > 0.0 && earned / possible > 0.9) {
        std::cout << "High score\n";
    } else {
        std::cout << "Not computed - possible is zero\n";
    }
    return 0;
}
```

**Expected output:**

```text
Not computed - possible is zero
```

*Try:* Swap the two conditions so the division comes first. What happens now, and why did the original order prevent it?

### 5. A menu with `switch`

```cpp
#include <iostream>
#include <string>

int main() {
    std::cout << "1) Add  2) Report  3) Quit\nChoice: ";
    std::string line;
    std::getline(std::cin, line);
    char choice = line.empty() ? '?' : line[0];

    switch (choice) {
        case '1': std::cout << "Adding\n";    break;
        case '2': std::cout << "Reporting\n"; break;
        case '3': std::cout << "Goodbye\n";   break;
        default:  std::cout << "Please enter 1, 2, or 3\n"; break;
    }
    return 0;
}
```

*Try:* Remove the `break` from case 1 and enter `1`. What happens? That is fall-through.

### 6. Find the bug by reading

Each compiles. Each is wrong. Say what happens and why.

```cpp
if (percentage >= 60.0)      { letter = 'D'; }
else if (percentage >= 70.0) { letter = 'C'; }
else if (percentage >= 80.0) { letter = 'B'; }
else if (percentage >= 90.0) { letter = 'A'; }
```

```cpp
if (percentage >= 90.0) { letter = 'A'; }
if (percentage >= 80.0) { letter = 'B'; }
if (percentage >= 70.0) { letter = 'C'; }
```

```cpp
if (percentage >= 90.0);
{
    letter = 'A';
}
```

```cpp
if (0 <= percentage <= 100) {
    std::cout << "valid\n";
}
```

### 7. Design and implement

Write a program reading a percentage and reporting a **plus-minus** letter grade: A at 93, A− at 90, B+ at 87, B at 83, B− at 80, and F below 80.

Write the `if/else if` chain, then test 93, 92.9, 90, 89.9, 87, 80, and 79.9.

Then answer: how many lines is your chain? How many would a full A-through-F plus-minus scale need? Now reconsider the question from the Grade Calculator section — what would it take to let a user *define* this scale without touching the code?

---

## Summary

- A **relational operator** compares values and produces a `bool`. `=` assigns; `==` compares.
- `if` runs a block when a condition is true; `if/else` chooses exactly one of two paths. **Always use braces.**
- A **block** defines **scope**. A variable declared inside one does not exist outside it.
- `&&`, `||`, and `!` combine conditions. **Chained comparisons such as `0 <= x <= 100` do not work** — write `0 <= x && x <= 100`.
- **Short-circuit evaluation** stops as soon as the answer is known. Put the check that makes the rest safe first.
- A multi-way **`if/else if` chain** handles mutually exclusive outcomes. **The first true condition wins**, so order from most restrictive to least. Without `else`, later branches overwrite earlier ones.
- **`switch`** compares one integral value against exact constants. It cannot test ranges or `double`s, so letter-grade logic needs a chain. Each case needs `break`.
- The **conditional operator** `? :` selects between two values.
- Four conditional errors are **silent**: a stray semicolon, reversed chain order, a missing `else`, and `==` on floating-point values.
- **A value that displays as 90.0 may still be less than 90.0.** `setprecision` rounds the display, not the value. Decide whether you grade the stored number or the rounded one, and write the decision down.

---

## Key Terms

**block** — statements enclosed in braces and treated as one statement.

**Boolean expression** — an expression producing `true` or `false`.

**condition** — the Boolean expression a selection statement tests.

**conditional operator** — `? :`, which selects between two values.

**fall-through** — continuing into the next `case` because `break` was omitted.

**logical operator** — `&&`, `||`, or `!`, combining Boolean expressions.

**nested conditional** — a conditional statement inside another.

**relational operator** — an operator comparing two values: `<`, `>`, `<=`, `>=`, `==`, `!=`.

**scope** — the region of a program in which a name exists.

**selection** — a control structure choosing between paths.

**short-circuit evaluation** — stopping evaluation of a compound condition once the result is determined.

**switch** — a statement comparing one integral value against a list of constants.

---

**Next:** Chapter 7 gives you **repetition**, the third structure from Chapter 5. Your calculator will accept as many assignments as a student has, accumulating totals as it goes — and you will see that points-based grading *is* the accumulator pattern. Grade Calculator v0.6.
