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
// Build: g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc

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

### Your task

1. Build and run. Enter 10 out of 10 with 5 bonus. Confirm the cap message appears.
2. **Verify the 89.95 fix.** Enter 89.95 points out of 100 with no bonus. Confirm the report shows 90.0 *and* awards an A. Then set `rounded` aside and compare against `rawPercentage` in the chain instead — confirm you get a B, and that the report still says 90.0. Put it back.
3. Set `CAP_AT_100` to `false`, rebuild, and rerun the 15-out-of-10 case. What percentage and letter now?
4. Change the rounding to two decimal places. Which constant did you change, and what does the 89.95 case do now?
5. Replace the `std::min` line with an equivalent `if` statement. Which do you find clearer? There is no wrong answer, but have a reason.

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
