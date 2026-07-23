# Chapter 4 — Expressions, Arithmetic, and Errors

## Learning Objectives

When you finish this chapter you will be able to:

- Build expressions from values, variables, and operators, and predict their results. *(SLO 1.3)*
- Explain integer division and modulus, and recognize when integer division is producing a wrong answer. *(SLO 1.1, 1.3)*
- Predict how C++ converts types in a mixed expression, and control conversion with a cast. *(SLO 1.1)*
- Apply operator precedence and associativity, and use parentheses to make intent explicit. *(SLO 1.3)*
- Format numeric output to a chosen number of decimal places. *(SLO 1.3)*
- Distinguish compile-time errors, run-time errors, logic errors, and warnings, and describe how each is found. *(SLO 1.6)*
- Write comments that explain decisions rather than restating code. *(SLO 1.6)*
- Build Grade Calculator v0.3, including a documented bonus-point policy.

---

## 4.1 Expressions and Operators

An **expression** is anything that produces a value. A literal is an expression. A variable is an expression. Combining them with operators produces larger expressions:

```cpp
84.5
pointsEarned
pointsEarned + bonusPoints
pointsEarned / pointsPossible * 100.0
```

An **operator** combines values. The values it works on are **operands**. C++'s arithmetic operators:

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `+` | addition | `7 + 2` | `9` |
| `-` | subtraction | `7 - 2` | `5` |
| `*` | multiplication | `7 * 2` | `14` |
| `/` | division | `7 / 2` | **see Section 4.3** |
| `%` | modulus (remainder) | `7 % 2` | `1` |

Four of those five behave exactly as you expect. The fifth does not, and it is responsible for more early bugs than anything else in this book.

---

## 4.2 Integer and Floating-Point Arithmetic Differ

Here is the rule that matters:

> **If both operands of an operator are integers, the result is an integer. If either operand is floating-point, the result is floating-point.**

For `+`, `-`, and `*` this is harmless. For `/` it changes the answer.

---

## 4.3 Integer Division and Modulus

When both operands are integers, `/` performs **integer division**: it divides and **discards the remainder**. It does not round. It truncates.

```cpp
int a = 7;
int b = 2;
std::cout << "7 / 2 as int:  " << a / b << "\n";
std::cout << "7 % 2 as int:  " << a % b << "\n";
std::cout << "7.0 / 2 mixed: " << 7.0 / b << "\n";
```

```text
7 / 2 as int:  3
7 % 2 as int:  1
7.0 / 2 mixed: 3.5
```

`7 / 2` is 3, not 3.5 and not 4. The `.5` is thrown away. The `%` operator recovers what was discarded: `7 % 2` is 1, the remainder.

### Why this matters for grades

Consider computing a percentage from 84 points out of 100:

```cpp
int earned = 84;
int possible = 100;
double percentage = earned / possible * 100.0;
```

You would expect 84.0. You get **0.0**.

Work through it in the order C++ does. First `earned / possible` is evaluated. Both are `int`, so this is integer division: 84 divided by 100 is 0 with remainder 84, and the remainder is discarded. The result is `0`. Then `0 * 100.0` is `0.0`. Assigning to a `double` at the end cannot recover information already thrown away.

The fix is to make at least one operand floating-point before dividing:

```cpp
double percentage = static_cast<double>(earned) / possible * 100.0;
```

Or, better, declare the variables as `double` in the first place — which is exactly what Section 3.11 concluded, because partial credit exists.

**This is the single most common arithmetic bug in beginning C++.** It produces no error and no warning. The program runs happily and reports the wrong grade. You will create it deliberately in the Grade Calculator section, because meeting it on purpose once is much cheaper than meeting it by accident later.

### Legitimate uses of `%`

Modulus is genuinely useful, not just a curiosity:

```cpp
if (n % 2 == 0) { /* n is even */ }
int minutes = totalSeconds % 60;
if (count % 10 == 0) { /* every tenth item */ }
```

---

## 4.4 Mixed-Type Expressions and Conversion

When operands have different types, C++ converts one before operating. The general direction is toward the type that can hold more information — an `int` mixed with a `double` becomes a `double`. This is an **implicit conversion**, because you did not ask for it.

```cpp
int count = 3;
double average = 10.0;
double total = count * average;    // count becomes 3.0; result 30.0
```

Implicit conversion is convenient and occasionally surprising, so C++ also provides an explicit form. A **cast** states the conversion you want:

```cpp
double exact = static_cast<double>(earned) / possible;
```

`static_cast<double>(earned)` produces a `double` copy of `earned` for this expression. The variable itself is unchanged.

Prefer `static_cast` to the older C-style form `(double)earned`. Appendix D Section D.11 explains why: `static_cast` is searchable, it is visually obvious, and it refuses conversions that are genuinely unsafe.

**Conversion the other way loses information.** Assigning a `double` to an `int` discards the fractional part without warning you at runtime:

```cpp
int rounded = 91.7;    // rounded is 91, not 92 — truncation, not rounding
```

Chapter 8 introduces `std::round` for when you actually want rounding.

---

## 4.5 Operator Precedence and Associativity

**Precedence** decides which operator acts first when an expression contains several.

```cpp
std::cout << 2 + 3 * 4 << "\n";      // 14, not 20
std::cout << (2 + 3) * 4 << "\n";    // 20
```

Multiplication has higher precedence than addition, so `3 * 4` happens first. Parentheses override precedence.

**Associativity** decides the order among operators of equal precedence.

```cpp
std::cout << 10 - 4 - 3 << "\n";     // 3, because (10 - 4) - 3
```

Arithmetic operators are **left-associative**: they group from the left.

### The operators you have met, by precedence

Highest first. Operators on the same row have equal precedence.

| Precedence | Operators | Associativity |
|---|---|---|
| Highest | `()` grouping | — |
| | `++` `--` (prefix), `static_cast` | right to left |
| | `*` `/` `%` | left to right |
| | `+` `-` | left to right |
| | `<<` `>>` (stream) | left to right |
| Lowest | `=` `+=` `-=` `*=` `/=` | right to left |

Later chapters extend this table: Chapter 6 adds the comparison and logical operators, Chapter 7 the conditional operator.

### Precedence and integer division together

Precedence and the integer-division rule interact in a way worth seeing explicitly:

```cpp
std::cout << 84 / 100 * 100 << "\n";      // 0
std::cout << 84.0 / 100 * 100 << "\n";    // 84
```

```text
84 / 100 * 100 = 0
84.0 / 100 * 100 = 84
```

Both expressions look like they should give 84. The first divides before multiplying — left to right, equal precedence — and integer division makes that first step 0. Everything after is doomed.

### Use parentheses for the reader

You do not need parentheses in `a + b * c`. Add them anyway when they make intent obvious:

```cpp
double percentage = (earned + bonus) / possible * 100.0;
```

Here they are genuinely required — without them, only `bonus` would be divided. But even where precedence already gives the right answer, parentheses cost nothing and remove doubt.

---

## 4.6 Compound Assignment, Increment, and Decrement

Adding to a variable is common enough to have a shorthand:

```cpp
int n = 10;
n += 5;    // same as n = n + 5;   n is 15
n -= 3;    // n is 12
n *= 2;    // n is 24
n /= 4;    // n is 6
```

These are **compound assignment** operators. They are shorter and, more usefully, they name the variable once — so you cannot accidentally write `total = totl + 5`.

Adding or subtracting exactly one has its own operators:

```cpp
++count;    // increment: add 1
--count;    // decrement: subtract 1
```

These come in two forms whose difference matters only when you use the value of the expression itself:

```cpp
int i = 5;
int before = i++;      // postfix: use the old value, then add 1
// before is 5, i is 6

int j = 5;
int after = ++j;       // prefix: add 1, then use the new value
// after is 6, j is 6
```

```text
i++ gave 5, i is now 6
++j gave 6, j is now 6
```

When you are not using the result — which is nearly always — the two behave identically, and this book writes `++count` by convention.

> **A warning worth heeding.** Do not modify a variable and also read it in the same statement, as in `std::cout << i++ << i;`. C++ does not define the order in which those happen, so the result is unpredictable and may differ between compilers. Compiling with `-Wall` reports this as `warning: operation on 'i' may be undefined [-Wsequence-point]`. Keep the increment on its own line.

---

## 4.7 Formatting Numeric Output

By default, C++ prints floating-point values with about six significant digits:

```cpp
std::cout << 91.666666 << "\n";      // 91.6667
```

For a grade report you want control. `<iomanip>` provides **manipulators**:

```cpp
#include <iomanip>

std::cout << std::fixed << std::setprecision(1);
std::cout << 91.666666 << "\n";      // 91.7
```

| Manipulator | Effect |
|---|---|
| `std::fixed` | always use decimal notation, not scientific |
| `std::setprecision(n)` | with `fixed`, show exactly *n* digits after the point |
| `std::setw(n)` | pad the **next** value to at least *n* characters |
| `std::left` / `std::right` | control which side the padding goes on |

```text
default:            91.6667
fixed, 1 decimal:   91.7
fixed, 3 decimals:  91.667
setw(10):          [      91.7]
left setw(10):     [91.7      ]
```

Two behaviors trip people up. **`std::fixed` and `std::setprecision` stay in effect** until changed, so set them once before your report rather than repeating them. **`std::setw` applies only to the very next value**, so it must be repeated for each column.

---

## 4.8 Bitwise Operators

C++ can operate on individual bits — the bits of Chapter 1, now directly accessible.

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `&` | AND — 1 where both bits are 1 | `12 & 10` | `8` |
| `\|` | OR — 1 where either bit is 1 | `12 \| 10` | `14` |
| `^` | XOR — 1 where exactly one bit is 1 | `12 ^ 10` | `6` |
| `<<` | shift left | `3 << 2` | `12` |
| `>>` | shift right | `12 >> 2` | `3` |

Work `12 & 10` out in binary and it is obvious:

```text
  1100    (12)
& 1010    (10)
  ----
  1000    (8)
```

Shifting left by *n* multiplies by 2ⁿ, and shifting right divides by 2ⁿ — which follows directly from the place values in Figure 1.2.

**Reference only.** The Grade Calculator never uses bitwise operators, and no exercise requires them. They are covered because they are part of the language and because they make Chapter 1's bit patterns concrete. Note that `<<` and `>>` do double duty as the stream operators — the compiler tells them apart by what is on the left.

---

## 4.9 Kinds of Errors

Programs go wrong in four distinct ways. Telling them apart is what makes debugging systematic rather than random, and it is the foundation Chapter 16 builds on.

### 4.9.1 Compile-time errors

The compiler cannot understand your program. **Nothing is built.**

```cpp
std::cout << "missing semicolon\n"
return 0;
```

These are the friendliest errors you will meet: they are found before the program runs, and the compiler tells you the file and line. Chapter 2 Section 2.6 covered reading these messages.

### 4.9.2 Run-time errors

The program compiled and started, then failed while running.

```cpp
int possible = 0;
int result = 100 / possible;    // integer division by zero
```

The compiler cannot catch this, because `possible` is only zero for certain inputs. Run-time errors are found by testing — particularly testing the boundary cases Chapter 16 makes systematic.

Note the asymmetry: integer division by zero crashes the program, while floating-point division by zero produces the special value `inf` and keeps going. Both are wrong; only one announces itself.

### 4.9.3 Logic errors

The program compiles, runs, finishes normally, and produces the **wrong answer**.

```cpp
int earned = 84;
int possible = 100;
double percentage = earned / possible * 100.0;    // 0.0, not 84.0
```

No error. No warning. No crash. A confidently reported wrong grade.

**Logic errors are the dangerous ones.** The compiler cannot help, because the program is valid — it simply does not do what you meant. They are found by testing against results you worked out independently, which is why every Grade Calculator version in this book comes with expected output.

### 4.9.4 Compiler warnings

The program compiled, and the compiler noticed something suspicious:

```text
warning: unused variable 'total' [-Wunused-variable]
```

A warning is not an error — the executable exists. But warnings are usually right, and a warning ignored today is a logic error hunted next week. Appendix D Section D.10 makes this a rule: **compile with `-Wall -Wextra` and fix every warning.**

### The four compared

| Kind | Found by | Program built? | Program runs? | Typical cause |
|---|---|---|---|---|
| Compile-time | the compiler | no | no | Syntax, misspelling, type mismatch |
| Run-time | testing | yes | starts, then fails | Division by zero, bad input |
| Logic | testing against known answers | yes | yes, finishes | Wrong formula, wrong order, integer division |
| Warning | the compiler | yes | yes | Something suspicious but legal |

---

## 4.10 Comments and Self-Documenting Code

Chapter 2 introduced the two comment forms. Now that expressions can be subtle, here is what makes a comment worth writing.

**A comment that restates the code is noise:**

```cpp
// Do not write this.
totalEarned += pointsEarned;    // add points earned to total earned
```

**A comment that explains a decision earns its place:**

```cpp
// Write this.
// Bonus points are added to points EARNED but not to points POSSIBLE, so a
// percentage above 100 is possible. See CAP_AT_100 for the course policy.
totalEarned += pointsEarned + bonusPoints;
```

The best comment is often the one you did not need to write, because the code says it:

```cpp
// Needs a comment:
double p = (e + b) / t * 100.0;

// Does not:
double percentage = (pointsEarned + bonusPoints) / pointsPossible * 100.0;
```

Good names remove the need for explanation. Comments are for the things names cannot carry: why a policy is what it is, what a formula assumes, what you deliberately chose not to do.

---

## Common Errors and Warnings

| What you see or observe | Cause | Fix |
|---|---|---|
| A percentage is `0` when it should not be | Integer division — both operands are `int` | Make one a `double`, or declare them `double` |
| A value is truncated, e.g. `91.7` becomes `91` | Assigned a `double` to an `int` | Use a `double`, or `std::round` (Chapter 8) |
| `2 + 3 * 4` gives 14, not 20 | Precedence: `*` before `+` | Add parentheses |
| Output shows `91.6667` instead of `91.7` | No formatting set | `std::fixed << std::setprecision(1)` |
| Only the first column lines up | `std::setw` applies to one value only | Repeat `setw` per column |
| `warning: operation on 'i' may be undefined` | Modified and read a variable in one statement | Put the increment on its own line |
| Program crashes on some inputs only | Run-time error, likely integer division by zero | Check the denominator before dividing |
| `error: 'setprecision' was not declared` | Missing header | `#include <iomanip>` |

---

## Design Notes

**Declare the type you mean.** Most integer-division bugs come from declaring an `int` where the quantity was never whole. Section 3.11's justification exercise prevents this before it starts.

**Guard your denominators.** Before dividing, ask what happens if the denominator is zero. The Grade Calculator has a real case: an assignment worth zero points. v0.4 will report it in words rather than printing a meaningless number.

**Decide policy explicitly, then write it down.** You are about to make a real decision — whether a bonus may push a grade above 100. Either answer is defensible. Choosing without recording the choice is what makes code mysterious six months later.

---

## Grade Calculator v0.3 — Percentage and Bonus Points

### What v0.3 does

Reads a named assignment with points earned, points possible, and bonus points, then computes and reports a percentage to one decimal place.

### The policy decision

**Bonus points are added to points earned but not to points possible.** That is what makes them a bonus. It also means a percentage above 100 is possible: 10 out of 10 plus 5 bonus is 150%.

Should your calculator report 150%, or cap it at 100%?

Both are real policies. Uncapped rewards exceptional work and can pull up a low average. Capped treats the maximum as a maximum. **v0.3 reports the raw value uncapped**, and Chapter 8 implements the cap once you have the tools to express it in one clean line. What matters now is that the choice is deliberate and documented.

### The program

```cpp
// Grade Calculator v0.3 - Chapter 4
// Adds bonus points and a percentage calculation.
// New this version: floating-point division, output formatting.
// Design note: bonus points are added to points EARNED but not to points
// POSSIBLE, so a percentage above 100 is possible. v0.3 reports it uncapped.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc

#include <iostream>
#include <iomanip>
#include <string>

int main() {
    std::cout << "=== GRADE CALCULATOR v0.3 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);

    std::string assignmentName;
    std::cout << "Assignment name: ";
    std::getline(std::cin, assignmentName);

    double pointsEarned = 0.0;
    std::cout << "Points earned: ";
    std::cin >> pointsEarned;

    double pointsPossible = 0.0;
    std::cout << "Points possible: ";
    std::cin >> pointsPossible;

    double bonusPoints = 0.0;
    std::cout << "Bonus points (0 if none): ";
    std::cin >> bonusPoints;

    double totalEarned = pointsEarned + bonusPoints;

    // Both operands are double, so this is real division, not integer division.
    double percentage = 0.0;
    if (pointsPossible > 0.0) {
        percentage = totalEarned / pointsPossible * 100.0;
    }

    std::cout << "\n--- Summary ---\n";
    std::cout << "Student:    " << studentName << "\n";
    std::cout << "Assignment: " << assignmentName << "\n";
    std::cout << "Earned:     " << totalEarned << " (" << pointsEarned
              << " + " << bonusPoints << " bonus)\n";
    std::cout << "Possible:   " << pointsPossible << "\n";
    std::cout << "Percentage: " << std::fixed << std::setprecision(1)
              << percentage << "%\n";
    return 0;
}
```

### Expected output

With input `Ada Lovelace`, `Midterm Exam`, `84`, `100`, `5`:

```text
--- Summary ---
Student:    Ada Lovelace
Assignment: Midterm Exam
Earned:     89 (84 + 5 bonus)
Possible:   100
Percentage: 89.0%
```

### What to notice

**`if (pointsPossible > 0.0)` guards the division.** An assignment worth zero points has no percentage, and dividing by zero is the run-time error of Section 4.9.2. You have not formally met `if` yet — Chapter 6 covers it — but its meaning here is plain, and guarding a denominator is a habit worth starting immediately.

**The comment explains why the division is safe**, not what it does. That is the Section 4.10 rule.

**Every variable involved in the division is `double`.** Not by accident. That single decision, made in Chapter 3, is what prevents the bug you are about to create on purpose.

### Your task

1. Build and run it. Confirm the output.

2. **Create the integer-division bug deliberately.** Change the two point variables to `int`:

   ```cpp
   int pointsEarned = 0;
   int pointsPossible = 0;
   ```

   Rebuild and run with 84 and 100. **Predict the output before you look.** You should see `0.0%`.

   Now explain, in a written sentence, exactly which operation produced 0 and why the later multiplication by `100.0` could not rescue it. Then change them back.

   This is the most valuable five minutes in the chapter. You have now produced a logic error, observed that the compiler said nothing, and diagnosed it.

3. Enter 10 points earned out of 10, with 5 bonus. What percentage is reported? Is that the behavior you want? Write one sentence of policy stating your answer, and add it as a comment at the top of the file. Chapter 8 will implement whichever you chose.

4. Change the report to show the percentage to **two** decimal places.

---

## Try It Yourself

### 1. Integer versus floating-point division

```cpp
#include <iostream>

int main() {
    int a = 7;
    int b = 2;
    std::cout << "7 / 2 as int:  " << a / b << "\n";
    std::cout << "7 % 2 as int:  " << a % b << "\n";
    std::cout << "7.0 / 2 mixed: " << 7.0 / b << "\n";
    return 0;
}
```

**Expected output:**

```text
7 / 2 as int:  3
7 % 2 as int:  1
7.0 / 2 mixed: 3.5
```

*Try:* Predict `9 / 4`, `9 % 4`, `9.0 / 4`, and `-7 / 2` before running each.

### 2. Precedence in action

```cpp
#include <iostream>

int main() {
    std::cout << "2 + 3 * 4        = " << 2 + 3 * 4 << "\n";
    std::cout << "(2 + 3) * 4      = " << (2 + 3) * 4 << "\n";
    std::cout << "10 - 4 - 3       = " << 10 - 4 - 3 << "\n";
    std::cout << "84 / 100 * 100   = " << 84 / 100 * 100 << "\n";
    std::cout << "84.0 / 100 * 100 = " << 84.0 / 100 * 100 << "\n";
    return 0;
}
```

**Expected output:**

```text
2 + 3 * 4        = 14
(2 + 3) * 4      = 20
10 - 4 - 3       = 3
84 / 100 * 100   = 0
84.0 / 100 * 100 = 84
```

*Try:* Add parentheses to the fourth line to make it produce 84 without changing any value to a `double`. Is that a good fix? Why might declaring the values as `double` be better?

### 3. Formatting output

```cpp
#include <iostream>
#include <iomanip>

int main() {
    std::cout << "default:           " << 91.666666 << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "fixed, 1 decimal:  " << 91.666666 << "\n";
    std::cout << std::setprecision(3);
    std::cout << "fixed, 3 decimals: " << 91.666666 << "\n";
    std::cout << "setw(10):         [" << std::setw(10) << 91.7 << "]\n";
    return 0;
}
```

**Expected output:**

```text
default:           91.6667
fixed, 1 decimal:  91.7
fixed, 3 decimals: 91.667
setw(10):         [    91.700]
```

*Try:* Explain why the last line shows `91.700` rather than `91.7`. Then add `std::left` before the `setw` and observe the change.

### 4. Compound assignment and increment

```cpp
#include <iostream>

int main() {
    int n = 10;
    n += 5;   std::cout << "n += 5 -> " << n << "\n";
    n -= 3;   std::cout << "n -= 3 -> " << n << "\n";
    n *= 2;   std::cout << "n *= 2 -> " << n << "\n";

    int i = 5;
    int before = i++;
    std::cout << "i++ gave " << before << ", i is now " << i << "\n";

    int j = 5;
    int after = ++j;
    std::cout << "++j gave " << after << ", j is now " << j << "\n";
    return 0;
}
```

**Expected output:**

```text
n += 5 -> 15
n -= 3 -> 12
n *= 2 -> 24
i++ gave 5, i is now 6
++j gave 6, j is now 6
```

*Try:* Add `n /= 5;` after the last compound assignment. `n` is 24 — what does integer division give you?

### 5. Bits, made visible

```cpp
#include <iostream>

int main() {
    std::cout << "12 & 10 = " << (12 & 10) << "\n";
    std::cout << "12 | 10 = " << (12 | 10) << "\n";
    std::cout << "12 ^ 10 = " << (12 ^ 10) << "\n";
    std::cout << "3 << 2  = " << (3 << 2) << "\n";
    return 0;
}
```

**Expected output:**

```text
12 & 10 = 8
12 | 10 = 14
12 ^ 10 = 6
3 << 2  = 12
```

*Try:* Write 12 and 10 in binary and verify each result by hand. Why does `3 << 2` give 12?

### 6. Classify the error

For each, say whether it is a compile-time error, a run-time error, a logic error, or a warning — and how you would find it.

- A semicolon is missing at the end of a statement.
- A percentage is computed as `earned / possible` where both are `int`.
- A program divides by a value the user entered as zero.
- A variable is declared and never used.
- A grade cutoff is written as `80.0` where the policy says `90.0`.
- `std::cout` is written without including `<iostream>`.

### 7. Find the bug by reasoning

This program reports a wrong average. Do not run it — find the error by reading:

```cpp
#include <iostream>

int main() {
    int total = 250;
    int count = 4;
    double average = total / count;
    std::cout << "Average: " << average << "\n";
    return 0;
}
```

What does it print? What should it print? What is the smallest change that fixes it? Now run it and check.

---

## Summary

- An **expression** produces a value. **Operators** combine **operands**.
- **If both operands are integers, the result is an integer.** Integer division **truncates** — `7 / 2` is 3. `%` gives the remainder.
- Computing a percentage with `int` operands gives `0`, silently. This is the most common arithmetic bug in beginning C++.
- Mixed-type expressions **convert implicitly** toward the wider type. A **cast** — `static_cast<double>(x)` — makes conversion explicit. Assigning a `double` to an `int` truncates.
- **Precedence** decides which operator acts first; **associativity** decides among equals. Arithmetic is left-associative. Use parentheses to make intent obvious even when they are not required.
- Compound assignment (`+=`) and increment (`++`) are shorthand. Do not modify and read a variable in the same statement.
- `<iomanip>` provides `std::fixed`, `std::setprecision`, and `std::setw`. Precision persists; `setw` applies only to the next value.
- **Bitwise operators** work on individual bits. Reference only in this book.
- Four kinds of failure: **compile-time** (nothing built), **run-time** (starts, then fails), **logic** (runs and gives a wrong answer), and **warnings** (built, but suspicious). Logic errors are the dangerous ones because nothing announces them.
- Comment **why**, not what. Good names remove the need for most comments.

---

## Key Terms

**associativity** — the rule deciding the order among operators of equal precedence.

**bitwise operator** — an operator acting on the individual bits of a value.

**cast** — an explicit conversion between types, written `static_cast<Type>(value)`.

**compile-time error** — a fault preventing the compiler from producing a program.

**compound assignment** — an operator such as `+=` combining an operation with assignment.

**decrement** — the `--` operator, subtracting one.

**expression** — any construct producing a value.

**implicit conversion** — an automatic type conversion performed by the compiler.

**increment** — the `++` operator, adding one.

**integer division** — division of two integers, discarding the remainder.

**logic error** — a fault in which a valid program produces a wrong result.

**manipulator** — a value such as `std::fixed` that changes how a stream formats output.

**modulus** — the `%` operator, giving the remainder of integer division.

**operand** — a value an operator acts upon.

**operator** — a symbol combining operands to produce a value.

**precedence** — the rule deciding which operator acts first.

**run-time error** — a fault occurring while the program runs.

**truncation** — discarding a fractional part rather than rounding.

**warning** — a compiler report of something suspicious but legal.

---

**Next:** Chapter 5 steps away from the keyboard. Before your calculator gets any more complicated, you will learn to design it — pseudocode, flowcharts, and structure charts — and produce the specification you will carry, and revise, for the next twenty chapters. Grade Calculator v0.4 puts that design work into the program's interface.
