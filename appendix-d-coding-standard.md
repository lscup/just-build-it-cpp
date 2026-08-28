# Appendix D — Coding Standard and Style Guide

Every code listing in this book follows the rules in this appendix. So does every version of the Grade Calculator in Appendix E. When Chapter 13 asks you to bring your Course I code into conformance with a written standard, this is that standard.

A style guide is not a matter of taste dressed up as rules. It exists so that you spend your attention on what a program *does* instead of on what it *looks like*, and so that a reader who has never seen your code can find their way around it. Chapter 13 makes the professional case at length. This appendix is the rules themselves.

**How to use this appendix.** Read Sections D.1 through D.5 once, early. Refer back to the rest when a specific question comes up. Section D.12 is a one-page checklist you can run through before submitting work.

---

## D.1 Layout

### Indentation

Use **four spaces** per level. Never use tab characters — they render at different widths in different editors, and a file that mixes tabs and spaces looks correct to its author and broken to everyone else.

Most editors can insert spaces when you press Tab. In VS Code and the StudySite editor this is on by default.

```cpp
int main() {
    double total = 0.0;
    if (total > 0.0) {
        std::cout << "positive\n";
    }
    return 0;
}
```

### Braces

The opening brace goes on the **same line** as the statement that introduces it. The closing brace goes on its own line, aligned with the start of that statement.

```cpp
if (percentage >= 90.0) {
    letter = 'A';
} else {
    letter = 'B';
}
```

**Always use braces**, even when the body is a single statement. This is not fussiness. Consider:

```cpp
// Do not write this.
if (possible > 0.0)
    percentage = earned / possible * 100.0;
```

The day someone adds a second line to that body — and forgets the braces — the program compiles and silently does the wrong thing. Braces from the start make that impossible.

One exception is permitted, for short guard clauses where the whole statement fits on one line:

```cpp
if (possible <= 0.0) { return 0.0; }
```

The braces are still there. The line is just compact enough to read at a glance.

### Line length

Keep lines to **90 characters** or fewer. Long lines force horizontal scrolling, which makes code hard to read on a laptop, in a browser editor, and in a side-by-side diff.

When a line must wrap, break it at a point that makes the structure obvious, and indent the continuation:

```cpp
std::cout << std::left << std::setw(20) << student.name()
          << std::right << std::setw(8) << student.percentage() << "%\n";
```

### Blank lines

Use a single blank line to separate logical groups within a function, and between functions. Never use two or more consecutive blank lines inside a function — if a function needs that much visual separation, it probably wants to be two functions.

---

## D.2 Naming

Names are the most valuable documentation in a program, because they appear at every point of use.

| Kind | Convention | Examples |
|---|---|---|
| Variable | `camelCase` | `pointsEarned`, `assignmentName`, `totalPossible` |
| Function | `camelCase`, verb phrase | `computePercentage`, `readNonNegative`, `printReport` |
| Class or struct | `PascalCase`, noun | `Student`, `GradeScale`, `WeightedDropLowest` |
| Class data member | `camelCase` with trailing `_` | `name_`, `pointsEarned_`, `roster_` |
| Constant | `SCREAMING_SNAKE_CASE` | `A_CUTOFF`, `MAX_STUDENTS`, `CAP_AT_100` |
| Enumeration type | `PascalCase` | `Scheme`, `Category` |
| Enumerator | `PascalCase` | `Scheme::Points`, `Scheme::Weighted` |
| File | `lowercase`, no separators | `gradescale.h`, `gradingscheme.cpp` |
| Header guard | `SCREAMING_SNAKE_CASE` of the filename | `GRADESCALE_H` |

### Why members end in an underscore

The trailing underscore on data members tells you, at every single use, whether you are looking at a member of the object or at a local variable or parameter. Compare:

```cpp
double Student::percentage() const {
    double possible = totalPossible();       // local: no underscore
    if (possible <= 0.0) { return 0.0; }
    return totalEarned() / possible * 100.0;
}
```

You never have to scroll up to the class definition to answer "where does this value come from?" It also lets a constructor parameter share its member's name without ambiguity:

```cpp
Student::Student(const std::string& name, int id) : name_(name), id_(id) {}
```

### Choosing good names

**Say what the thing is, not what type it is.** `pointsEarned` is better than `dblPoints`. The compiler already knows the type; the reader needs to know the meaning.

**Prefer clarity to brevity, but do not pad.** `computePercentage` is better than both `cp` and `computeTheFinalPercentageValue`.

**Single letters are acceptable only for loop counters** with an obvious, short scope — `i`, `j`, `a`, `s`. Anything that lives longer than a few lines deserves a real name.

**Booleans read as a question or a claim.** `capAt100`, `dropLowest`, `weightsValid` — each reads naturally in an `if`.

**Avoid abbreviations that are not universal.** `pts` saves three characters and costs a moment's thought every time it is read. `max`, `min`, `id`, and `csv` are fine; they are standard.

---

## D.3 Comments

A comment should explain **why**, not **what**. The code already says what it does. If the code is so unclear that it needs a comment to restate it, rewrite the code instead.

```cpp
// Do not write this. It says nothing the code does not.
totalEarned += pointsEarned;   // add points earned to total earned

// Write this. It explains a decision the code cannot express.
// Bonus points are added to points EARNED but not to points POSSIBLE, so a
// percentage above 100 is possible. Course policy caps it; see CAP_AT_100.
totalEarned += pointsEarned + bonusPoints;
```

### Documentation comments

Every function that another file can call gets a documentation comment in `/** */` form, placed in the header file, above the declaration. Use these tags:

| Tag | Use |
|---|---|
| `@param name` | What one parameter means, including any restriction on its value |
| `@return` | What the return value means |
| `@throws Type` | An exception this function may raise and the condition that raises it |
| `@pre` | A precondition the caller is responsible for, which the function does not check |

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

Not every function needs all four tags. A function that takes nothing, returns nothing, throws nothing, and requires nothing needs a single sentence.

Short private helpers used only inside one file may take a one-line `//` comment instead.

### File headers

Every file begins with a header giving its identity and purpose. Implementation files that belong to a class need only a single line:

```cpp
// gradescale.cpp - Grade Calculator v4.0 - Chapter 24
```

The file containing `main` gets a fuller block, because it is where a reader starts:

```cpp
// =============================================================================
//  Grade Calculator  v3.1                                          Chapter 21
// -----------------------------------------------------------------------------
//  Change  : GradingScheme is now abstract with a pure virtual computePercentage
//            and a virtual destructor. Gradebook holds a GradingScheme* and
//            never asks which scheme it has.
//  Run     : click Run in StudySite and use the embedded Terminal.
// =============================================================================
```

### Section banners

In a long file, separate major groups of functions with a banner. Keep them consistent within a file.

```cpp
// -----------------------------------------------------------------------------
//  Input helpers
// -----------------------------------------------------------------------------
```

### Recording known limitations

When you knowingly leave something imperfect, say so in the code, and say what would fix it. A limitation you documented is a decision. A limitation you did not is a bug waiting to be blamed on you.

```cpp
// LIMITATION (removed in Chapter 21): selection happens through a single branch
// here, because computePercentage is not yet virtual. The scheme is therefore
// fixed once the program starts.
```

---

## D.4 Files and Includes

### One class per file

Each class gets a header and an implementation file named after it in lowercase: `gradescale.h` and `gradescale.cpp`. Small, tightly related helper types may share their owner's header — `GradeScale::Tier` lives inside `gradescale.h` because it has no meaning apart from `GradeScale`.

### Header guards

Every header is wrapped in a guard so that including it twice is harmless:

```cpp
#ifndef GRADESCALE_H
#define GRADESCALE_H

// ... contents ...

#endif
```

Name the guard after the file, in capitals, with the dot replaced by an underscore. `#pragma once` works on every compiler this book targets and is shorter, but it is not part of the C++ standard, so this book uses guards.

### Include order

Group includes, most specific first, with a blank line between groups:

1. The header this file implements, if any
2. Other headers from this project
3. Standard library headers

```cpp
#include "gradebook.h"        // the header this file implements

#include "gradebookerror.h"   // other project headers

#include <algorithm>          // standard library, alphabetical
#include <iostream>
#include <vector>
```

Putting the file's own header first is not arbitrary: if that header is missing an include it needs, this arrangement makes the compiler say so immediately instead of hiding the problem behind whatever came before.

### Include what you use

If a file names `std::vector`, it includes `<vector>` — even if some other header it includes happens to provide it already. Relying on an indirect include means your file breaks when an unrelated header changes.

### Never write `using namespace std;`

Write `std::cout`, `std::vector`, `std::string` in full. The five extra characters tell every reader exactly where a name comes from, and they prevent collisions between your names and the standard library's. This rule is absolute in headers, where a `using` directive would be forced on every file that includes them, and it is followed in implementation files too for consistency.

---

## D.5 Functions

**A function does one thing.** If you find yourself writing a comment that says "now we do the second part," that is a second function asking to exist.

**Keep functions short enough to see at once.** There is no hard limit, but a function longer than about 40 lines is worth a second look.

**Use guard clauses to handle the exceptional case first**, then let the main logic run unindented:

```cpp
double Student::percentage() const {
    double possible = totalPossible();
    if (possible <= 0.0) { return 0.0; }      // guard: get it out of the way

    double raw = totalEarned() / possible * 100.0;
    return std::round(std::min(raw, 100.0) * 10.0) / 10.0;
}
```

**Pass large objects by `const` reference**, not by value. Copying a `std::string` or `std::vector` on every call is wasted work, and `const` documents that the function will not modify it.

```cpp
void printReport(const std::string& student, const std::vector<Assignment>& work);
```

Pass small values — `int`, `double`, `char`, `bool` — by value. A reference to a `double` is no cheaper than the `double`.

**Use an output parameter only when a function must return two things.** Prefer a return value where one will do.

**Mark member functions `const` when they do not modify the object.** Do this from the beginning; retrofitting `const` onto a finished class is tedious, and until it is done, `const` objects are almost unusable.

---

## D.6 Variables and Types

**Declare a variable at the point where you can give it a useful value**, not at the top of the function. A variable that exists for twenty lines before it means anything is twenty lines of opportunity to misuse it.

**Always initialize.** An uninitialized variable holds whatever was in that memory, which makes the resulting bug different every run.

```cpp
double totalEarned = 0.0;    // yes
double totalEarned;          // no
```

Class members are initialized where they are declared:

```cpp
private:
    std::string name_;
    double pointsEarned_   = 0.0;
    double pointsPossible_ = 0.0;
    double bonusPoints_    = 0.0;
```

**Use `const` for anything that should not change**, including function parameters you do not intend to modify.

**Name your magic numbers.** A bare `90.0` in the middle of a conditional means nothing to a reader; `A_CUTOFF` means everything. The exceptions are `0`, `1`, and values whose meaning is unmistakable in context, such as `100.0` when converting a ratio to a percentage.

**Use `auto` where the type is obvious from the right-hand side** and the name still carries the meaning:

```cpp
auto it = idIndex_.find(id);        // yes: the iterator type is noise
auto total = 0;                     // no: is this an int? a double? say so
```

**Choose the type that matches the quantity.** Points are `double` because partial credit exists. Counts are `int`. A student ID is `int` because it is an identifier, not a quantity you do arithmetic on. Container sizes are `std::size_t`, which is what the containers themselves return.

---

## D.7 Classes

Order the members of a class definition as follows:

1. `public:` — constructors, then member functions
2. `protected:` — anything derived classes need
3. `private:` — helper functions, then data members

Public first, because the interface is what a reader wants and the implementation is what they can skip.

```cpp
class GradeScale {
public:
    struct Tier {
        double cutoff = 0.0;
        char   letter = 'F';
    };

    GradeScale();
    explicit GradeScale(const std::vector<Tier>& requested);

    char letterFor(double percentage) const;
    std::size_t tierCount() const { return tiers_.size(); }

private:
    std::vector<Tier> tiers_;
};
```

**Data members are always private.** If callers need access, provide an accessor. A public data member is a promise you cannot later take back.

**Mark single-argument constructors `explicit`** unless you specifically want the implicit conversion. Without it, the compiler will silently convert anything convertible to the parameter type into your class, in places you did not intend.

**Very short accessors may be defined inline in the header.** Anything with real logic goes in the `.cpp` file.

**State class invariants in a comment above the class**, and enforce them in the constructor:

```cpp
/**
 * An ordered set of grade cutoffs.
 * INVARIANT: cutoffs strictly descend and the lowest tier is 0, so every
 * percentage from 0 upward maps to exactly one letter.
 */
```

An invariant established in the constructor is a fact the rest of your code can rely on without checking. That is the entire value of encapsulation, and it is why `letterFor` needs no error handling.

---

## D.8 Error Handling

**Validate input where it enters the program.** Once a value is inside a well-designed class, it should already be known good.

**Throw an exception when a function cannot do what its name promises.** Do not return a sentinel value that callers will forget to check, and do not silently substitute a default the user did not ask for.

```cpp
// The user typed a scale whose tiers do not descend. Refusing is honest;
// quietly repairing it would compute grades from something they never chose.
throw InvalidScaleError("tier 'B' at 85 is not below the previous tier at 80.");
```

**Catch exceptions where you can do something useful about them** — usually where you can tell the user what happened and let them try again.

**Exception messages address the user, not the programmer.** Name what went wrong, where, and what to do about it. `"Cannot read 'gradebook.csv' at line 14: expected a number here."` is useful. `"parse error"` is not.

**Leave no operation half-finished.** If an operation can fail partway, build the result separately and install it only on success, so a failure leaves the previous state untouched.

---

## D.9 Output Formatting

Console output is this book's entire user interface, so it gets the same care as the code.

**Prompts state what is wanted and any restriction on it**:

```
Points possible (must be > 0): 
```

**Align related output in columns** using `std::setw` and `std::left` / `std::right`. A ragged report is hard to scan.

**Set floating-point formatting once, near the output**, not scattered through the function:

```cpp
std::cout << std::fixed << std::setprecision(1);
```

**Use `"\n"`, not `std::endl`.** `std::endl` also flushes the stream, which is rarely what you want and is slower in a loop. Reach for `std::flush` explicitly on the rare occasion you need it.

**Explain a missing result rather than printing a misleading one.** An assignment worth zero points has no percentage; say that, do not print `0.0%`.

**Use plain text only.** No ANSI color codes, no box-drawing characters, no cursor positioning. Output must be readable in the StudySite terminal, in Codespaces, and by a screen reader.

---

## D.10 Portability

Every program in this book must build and run unchanged in the StudySite editor and in GitHub Codespaces. That rules out:

- Platform headers — `<windows.h>`, `<conio.h>`, `<unistd.h>`
- `system()` calls of any kind, including `system("pause")` and `system("cls")`
- Compiler extensions and anything outside the C++17 standard
- Absolute file paths, and backslash path separators
- External libraries — the standard library only

Every file must compile clean under C++17 with all warnings enabled:

```
-std=c++17 -Wall -Wextra
```

StudySite's **Run** applies these settings for you. If you also build locally,
pass them to `g++` yourself — the standard is the settings, not the command.

**Warnings are errors.** A warning is the compiler telling you it understood your program differently than you probably meant. Fix the cause; do not silence the message.

---

## D.11 What Not to Do

A short list of habits that appear in older textbooks and internet examples, with the reason each is excluded.

| Avoid | Why |
|---|---|
| `using namespace std;` | Hides where names come from; invites collisions |
| `goto` | Makes control flow unfollowable; every use here has a better structured form |
| `system("pause")` | Not portable, and launches a shell to do nothing |
| C-style casts, `(int)x` | Silent and unsearchable; use `static_cast<int>(x)` |
| `char*` string handling | Use `std::string`; see Section 11.9 for why C strings still get covered |
| Global variables | Any function can change them, so no function can be reasoned about alone |
| `#define` for constants | No type, no scope; use `const` |
| Single-letter names outside loops | Costs the reader more than it saves the writer |
| Commented-out code | Delete it — that is what version control is for |
| `std::endl` in a loop | Flushes on every iteration for no benefit |

---

## D.12 Pre-Submission Checklist

Run through this before you hand in any program.

**Builds and runs**

- [ ] Compiles under `-std=c++17 -Wall -Wextra` with **no warnings** — in StudySite, click **Run**
- [ ] Runs to a normal exit on valid input
- [ ] Does not crash on invalid input that its own prompts invite
- [ ] Uses only the standard library and no platform-specific calls
- [ ] Saved to your project repository with **Save to GitHub**, and the commit is visible on GitHub

**Layout**

- [ ] Four-space indentation, no tab characters
- [ ] Braces on every block, opening brace on the same line
- [ ] No line longer than 90 characters

**Naming**

- [ ] Variables and functions `camelCase`, classes `PascalCase`, constants `SCREAMING_SNAKE_CASE`
- [ ] Class data members end in `_`
- [ ] No magic numbers — every meaningful constant is named
- [ ] No single-letter names outside short loops

**Comments**

- [ ] File header present and accurate
- [ ] Every public function has a documentation comment with the tags that apply
- [ ] Comments explain *why*, never restate *what*
- [ ] Any known limitation is recorded in the code
- [ ] No commented-out code left behind

**Structure**

- [ ] Each function does one thing
- [ ] Data members are private
- [ ] Non-modifying member functions are marked `const`
- [ ] Large parameters passed by `const` reference
- [ ] Every variable initialized where declared
- [ ] Headers guarded, includes grouped and ordered
- [ ] No `using namespace std;` anywhere

---

## D.13 A Conforming Example

The following is `gradescale.h` from Grade Calculator v4.0, unmodified. Every rule in this appendix is visible in it: the file header, the guard, grouped includes, the class-invariant comment, public-before-private ordering, `explicit`, a `const` member function, a documentation comment with `@throws`, a trailing-underscore data member, and four-space indentation throughout.

```cpp
// gradescale.h - Grade Calculator v4.0 - Chapter 24
#ifndef GRADESCALE_H
#define GRADESCALE_H

#include <iosfwd>
#include <vector>

/**
 * An ordered set of grade cutoffs.
 * INVARIANT: cutoffs strictly descend and the lowest tier is 0, so every
 * percentage from 0 upward maps to exactly one letter. The constructor
 * establishes this, and no member function can break it.
 */
class GradeScale {
public:
    struct Tier {
        double cutoff = 0.0;
        char   letter = 'F';
    };

    GradeScale();

    /**
     * Builds a scale from user-supplied tiers.
     *
     * @param  requested  tiers in descending order, lowest cutoff 0
     * @throws InvalidScaleError if the tiers do not strictly descend, if any
     *         cutoff is negative, or if the scale does not reach 0.
     */
    explicit GradeScale(const std::vector<Tier>& requested);

    char letterFor(double percentage) const;
    std::size_t tierCount() const { return tiers_.size(); }
    const std::vector<Tier>& tiers() const { return tiers_; }

private:
    std::vector<Tier> tiers_;
};

std::ostream& operator<<(std::ostream& out, const GradeScale& scale);

#endif
```

Every version of the Grade Calculator in Appendix E conforms to this standard. When you need to see a rule applied in context, read the reference implementation for the chapter you are working on.
