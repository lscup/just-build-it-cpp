# Chapter 24 — Exceptions, Release, and the Road Ahead

## Learning Objectives

When you finish this chapter you will be able to:

- Explain why return codes are insufficient for reporting errors. *(SLO 2.1)*
- Throw and catch exceptions. *(SLO 2.1)*
- Define a custom exception hierarchy and catch by specificity. *(SLO 2.2, 2.3)*
- Explain stack unwinding and why RAII makes exceptions safe. *(SLO 2.1)*
- Decide when an exception is appropriate and when it is not. *(SLO 2.1)*
- Describe every phase of program translation from source to executable. *(SLO 2.9)*
- Distinguish static from dynamic libraries, and debug from release builds. *(SLO 2.9)*
- Produce release documentation and reconcile a design document. *(SLO 2.1, 2.4)*
- Build Grade Calculator v4.0 — the release.

---

## 24.1 Why Return Codes Are Not Enough

Your calculator has reported failure three ways, and all three have the same weakness.

**A sentinel return value.** Chapter 17's `linearSearchById` returns −1 for "not found":

```cpp
int index = linearSearchById(roster, id, comparisons);
const Student& s = roster[index];      // if index is -1, undefined behavior
```

**A status flag by reference.** Chapter 10's `readNonNegative` returns `bool` alongside the value. Better, and still ignorable.

**Silent repair.** Chapter 18's `GradeScale` quietly fixes an invalid scale. The user's input was wrong and nothing said so.

The common failure: **nothing forces the caller to notice.** Ignoring a return value is legal, silent, and easy. And a function that computes a percentage has no spare `double` to mean "failed" — every value is a legitimate answer.

**An exception cannot be ignored.** Unhandled, it terminates the program. That is a strong default, and the right one for a condition that must not pass unnoticed.

---

## 24.2 `throw`, `try`, and `catch`

```cpp
double computePercentage(double earned, double possible) {
    if (possible <= 0.0) {
        throw std::invalid_argument("points possible must be greater than zero");
    }
    return earned / possible * 100.0;
}
```

`throw` abandons the function immediately. Execution jumps to the nearest enclosing handler:

```cpp
try {
    double pct = computePercentage(earned, possible);
    std::cout << pct << "%\n";
} catch (const std::invalid_argument& e) {
    std::cout << "Cannot compute: " << e.what() << "\n";
}
```

Three parts. The **`try` block** contains code that might throw. The **`catch` clause** names the type it handles and receives the exception object. **`what()`** returns the message.

**Always catch by `const` reference.** Catching by value slices the exception — Chapter 21 Section 21.4's problem, in a new place, and it discards exactly the derived information you wanted.

---

## 24.3 Standard Exception Types

`<stdexcept>` provides a hierarchy rooted at `std::exception`:

| Type | Meaning |
|---|---|
| `std::exception` | the base of all standard exceptions |
| `std::logic_error` | a fault in the program's logic |
| `std::invalid_argument` | an argument was unacceptable |
| `std::out_of_range` | an index or key was outside the valid range |
| `std::runtime_error` | a fault detectable only while running |

You have already met two. `std::vector::at` throws `std::out_of_range` — Chapter 12 Section 12.4. `std::stod` throws `std::invalid_argument` — Chapter 15 Section 15.6.

---

## 24.4 A Custom Exception Hierarchy

Standard types are fine for general faults. For your own application, define types that name your own failures — this is the inheritance of Chapter 20 applied to error reporting.

```cpp
/**
 * Base class for every error this application reports.
 *
 * Deriving from std::runtime_error means these can be caught either
 * specifically, or as GradebookError, or as std::exception - a caller chooses
 * how much it wants to know.
 */
class GradebookError : public std::runtime_error {
public:
    explicit GradebookError(const std::string& what) : std::runtime_error(what) {}
};

/** A grade scale whose tiers do not descend, or that does not reach 0. */
class InvalidScaleError : public GradebookError {
public:
    explicit InvalidScaleError(const std::string& what)
        : GradebookError("Invalid grade scale: " + what) {}
};

/** Category weights that do not total 100 percent. */
class WeightSumError : public GradebookError {
public:
    explicit WeightSumError(double actual)
        : GradebookError(describe(actual)), actual_(actual) {}
    double actual() const { return actual_; }
private:
    static std::string describe(double actual);
    double actual_;
};
```

Note that `WeightSumError` carries **data**, not just a message. A handler can call `actual()` and offer to scale the weights. An exception is an object, and it may hold whatever the handler needs.

---

## 24.5 Catching Multiple Exceptions

Several `catch` clauses may follow one `try`. **The first matching one runs**, so order from most specific to least:

```cpp
try {
    // ...
} catch (const InvalidScaleError& e) {
    std::cout << "  caught InvalidScaleError: " << e.what() << "\n";
} catch (const GradebookError& e) {
    std::cout << "  caught GradebookError:    " << e.what() << "\n";
} catch (const std::exception& e) {
    std::cout << "  caught std::exception:    " << e.what() << "\n";
}
```

```text
  caught InvalidScaleError: Invalid grade scale: tier 'B' at 85 is not below the previous tier at 80.
  caught GradebookError:    Category weights total 80.0 percent; they must total 100.
  caught std::exception:    something else entirely
```

Three different throws, three different handlers — each caught at the level of detail it needed. A `WeightSumError` is a `GradebookError`, so the second clause caught it.

**Reverse the order and the general clause catches everything**, making the specific ones unreachable. That is the same first-match-wins rule as Chapter 6 Section 6.9's `if/else if` chain, with the same consequence for getting the order wrong.

`catch (...)` catches anything. Chapter 15 used it as a blunt instrument. It is appropriate at the top of `main` as a last resort, and rarely elsewhere — you cannot examine what you caught.

---

## 24.6 Stack Unwinding and Exception Safety

When an exception is thrown, C++ **unwinds the stack**: it leaves each function between the throw and the handler, **running the destructor of every local object** on the way.

```text
--- stack unwinding ---
  built a
  built b
  destroyed b
  destroyed a
  handler: boom
```

Both objects were destroyed, in reverse order, before the handler ran.

**This is why RAII matters so much in C++.** Chapter 22 argued that `std::unique_ptr` is better than manual `delete` because there is nothing to remember. Exceptions make the argument decisive:

```cpp
void risky() {
    GradingScheme* s = new Weighted();
    somethingThatThrows();               // exception thrown here
    delete s;                            // never reached — leaked
}
```

The `delete` is skipped. With a `unique_ptr`, the destructor runs during unwinding and the memory is released.

**Manual resource management and exceptions do not mix.** Any function that can throw — which is most of them — leaks if it manages a resource by hand. RAII is not merely tidier; it is what makes exceptions usable.

### Leave no operation half-finished

The other half of exception safety is a design rule you have already applied. Chapter 15's `loadGradebook` built a complete `Gradebook` in a temporary and installed it only on success, so a file that failed partway left the previous data untouched.

**Build the replacement, then install it.** An operation that fails should leave the object as it was.

---

## 24.7 When to Use Exceptions

Not for everything.

**Use an exception when** a function cannot do what its name promises, the caller must not proceed as though it had, and there is no natural return value meaning failure.

**Do not use an exception for** ordinary control flow, or for expected conditions. A user typing `abc` where a number belongs is **expected** — Chapter 10's validation loop handles it by re-prompting, which is correct. Throwing there would be using an exception as a `goto`.

| Situation | Handle it how |
|---|---|
| User types text where a number belongs | Re-prompt — expected |
| Menu choice out of range | Re-prompt — expected |
| Grade scale tiers out of order | **Throw** — the object cannot be built |
| Category weights do not total 100 | **Throw** — the scheme would be wrong |
| Gradebook file is malformed | **Throw** — loading cannot proceed |
| A student ID is not found | Return `nullptr` or an optional — a normal outcome |

That last row is a judgment worth defending. "Not found" is a normal result of searching, not a failure — so v4.0 keeps returning `nullptr` from `findById` rather than throwing.

---

## 24.8 Program Translation, Revisited

Chapter 2 Section 2.2 described four stages before you knew what a linker error meant. This is SLO 2.9, and you can now understand every part of it.

### The four stages

| Stage | Tool | Input | Output |
|---|---|---|---|
| 1 | Preprocessor | `main.cpp` | translation unit |
| 2 | Compiler | translation unit | assembly |
| 3 | Assembler | assembly | object file `main.o` |
| 4 | Linker | object files + libraries | executable |

**Preprocessing** carries out `#include` and `#define`. Chapter 2 measured a six-line program expanding to 32,192 lines. You now know why headers should include as little as possible — Chapter 19 Section 19.3's `<iosfwd>` — because every file including yours pays for whatever it pulls in.

**Compilation** checks syntax and types and emits assembly. Templates are instantiated here, which is why a template must be visible where it is used — Chapter 23 Section 23.3.

**Assembly** produces machine code with unfilled references.

**Linking** resolves those references. You have now caused this failure deliberately several times: a prototype with no definition (Chapter 9), a `.cpp` omitted from the build (Chapter 10), a `static` member declared but not defined (Chapter 19). All three are the same thing — the compiler accepted a promise nobody kept.

### Separate compilation

Each `.cpp` compiles independently into an object file. That is why changing one implementation file rebuilds only that file, while changing a *header* rebuilds everything that includes it — the measurement from Chapter 19 task 7.

### Static and dynamic libraries

A **library** is precompiled code you link against.

A **static library** (`.a`, `.lib`) is copied into your executable at link time. The result is larger and self-contained.

A **dynamic library** (`.so`, `.dll`, `.dylib`) is loaded when the program runs. The executable is smaller, several programs share one copy, and updating the library updates every program — but the library must be present on the machine.

The C++ standard library is usually linked dynamically, which is why your `gradecalc` is a few kilobytes rather than a few megabytes.

### Debug and release builds

| Setting | Debug | Release |
|---|---|---|
| Flag | `-g` | `-O2` |
| Debug information | yes | no |
| Optimization | none | aggressive |
| Assertions | active | removed with `-DNDEBUG` |
| Size | larger | smaller |
| Speed | slower | faster |

```text
g++ -std=c++17 -Wall -Wextra -g main.cpp -o gradecalc          # debug
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG main.cpp -o gradecalc # release
```

**Test the release build, not only the debug build.** Optimization occasionally exposes undefined behavior that happened to work unoptimized — the out-of-bounds access from Chapter 11, or the uninitialized variable from Chapter 3, can behave differently at `-O2`. A program that works in debug and fails in release almost always has undefined behavior somewhere.

### A makefile, optionally

Twenty-four chapters and every build has been one command. For larger projects, a build tool records the recipe:

```text
CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -g
SRCS = main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp

gradecalc: $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o gradecalc

clean:
	rm -f gradecalc
```

Then `make` builds and `make clean` removes. This is a convenience, not a requirement — the Grade Calculator builds fine without it.

---

## 24.9 Preparing a Release

Software that only its author can run is not finished. A release needs four things.

**A release build**, compiled with optimization, tested with the same cases as the debug build.

**A README** — what it is, how to build it, how to run it, what it requires.

**A user guide** — how to use it, what every menu option does, what the file format is, what the error messages mean.

**Reconciled design documentation** — a design document matching what was actually built.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `terminate called after throwing an instance of ...` | Unhandled exception | Add a handler, or fix the cause |
| A derived exception is caught by the wrong clause | Order runs general to specific | Most specific first |
| `e.what()` gives a generic message | Caught by value — sliced | Catch by `const&` |
| Memory leaks when an exception is thrown | Manual `delete` skipped by unwinding | Use RAII |
| Half-modified object after a failure | Modified in place, then threw | Build a replacement, install on success |
| The release build behaves differently | Undefined behavior exposed by optimization | Run sanitizers; test both builds |
| `undefined reference` | Definition missing at link time | Define it; list every `.cpp` |
| Assertions do nothing in release | `-DNDEBUG` removes them | Do not rely on assertions for user input |
| Every file rebuilds after a one-line change | A header changed | Keep headers minimal |

---

## Design Notes

**Throw when a function cannot keep its promise.** Do not throw for expected conditions.

**Catch by `const` reference**, most specific first.

**Never manage a resource by hand in code that can throw.**

**Build the replacement, then install it.** A failed operation leaves the object as it was.

**Exception messages address the user**: name what went wrong, where, and what to do.

---

## Grade Calculator v4.0 — Release

### What v4.0 does

Everything v3.3 did, with errors reported as exceptions from a `GradebookError` hierarchy — plus a release build, a README, and a user guide.

### GradeScale now refuses

Chapter 18 Section 18.8 flagged this. The constructor **repaired** invalid input, and the section noted that rejection is the honest alternative once there is a way to report failure.

```cpp
GradeScale::GradeScale(const std::vector<Tier>& requested) {
    if (requested.empty()) {
        throw InvalidScaleError("no tiers were given.");
    }
    for (const Tier& t : requested) {
        if (t.cutoff < 0.0) {
            throw InvalidScaleError(std::string("tier '") + t.letter
                                    + "' has a negative cutoff.");
        }
        if (!tiers_.empty() && t.cutoff >= tiers_.back().cutoff) {
            throw InvalidScaleError(std::string("tier '") + t.letter + "' at "
                + std::to_string(static_cast<int>(t.cutoff))
                + " is not below the previous tier at "
                + std::to_string(static_cast<int>(tiers_.back().cutoff)) + ".");
        }
        tiers_.push_back(t);
    }
    if (tiers_.back().cutoff > 0.0) {
        throw InvalidScaleError("the lowest tier must have a cutoff of 0 so that"
                                " every percentage maps to a letter.");
    }
}
```

**The invariant did not change** — cutoffs descend, the lowest is 0. Only what happens when someone violates it. That the invariant survived a change this large is evidence it was the right thing to state in Chapter 18.

### The caller reports and recovers

```cpp
void editScale(Gradebook& book) {
    std::vector<GradeScale::Tier> requested;
    // ... read tiers from the user ...
    try {
        book.setScale(GradeScale(requested));
        std::cout << "  " << book.scale() << "\n";
    } catch (const InvalidScaleError& e) {
        // The old scale is untouched: the new one was never constructed.
        std::cout << "  " << e.what() << "\n";
        std::cout << "  Your previous scale is still in effect.\n";
    }
}
```

That comment is the exception-safety point. `book.setScale(...)` is never reached, because constructing the argument threw first. **The gradebook cannot be left holding a half-built scale.**

### Expected behavior

Entering a scale with A at 80 then B at 85 — out of order:

```text
  Invalid grade scale: tier 'B' at 85 is not below the previous tier at 80.
  Your previous scale is still in effect.
1001  Ada                     90.0%   A
```

Entering weights of 50 and 30, totalling 80:

```text
  Category weights total 80.0 percent; they must total 100.
  The grading scheme was not changed.
```

Both refused, both explained, both leaving the program in its previous working state.

### Loading translates library exceptions

```cpp
try {
    // ... std::stod, std::stoi on fields from the file ...
} catch (const std::invalid_argument&) {
    // stod and stoi throw this on non-numeric text. Translate it into
    // an error that names the file and line the user can actually fix.
    throw FileFormatError(filename, lineNumber, "expected a number here.");
}
```

`std::invalid_argument` says a conversion failed. It does not say which file, which line, or what to do. **Catching a low-level exception and rethrowing a meaningful one** is how a library error becomes a user-facing message.

Compare with Chapter 15's `catch (...)`, which knew something went wrong and could say nothing useful. That was appropriate then; this is better now.

### Running the release check

Keep every source and header file open, click **Run**, and work through the
full test plan in the embedded Terminal — not only the handful of cases you
happened to try while writing the code. A release is a claim that you tested
the whole thing.

---

### Your StudySite Lab — Add Release-Safe Error Handling

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v4.0
- **Starting point:** Your committed Chapter 23 v3.3 program (twelve files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### What you will build

This is the release checkpoint. Until now, bad input was either quietly
repaired (an invalid grade scale) or quietly accepted (weights that do not
total 100). In this lab you make the program **refuse bad input with an
exception, explain why, and carry on**. By the end you will have:

1. An **exception hierarchy** in `gradebookerror.h`: a `GradebookError` base
   class derived from `std::runtime_error`, and three specific errors —
   `InvalidScaleError`, `WeightSumError`, and `FileFormatError`.
2. A `GradeScale` constructor that **throws** `InvalidScaleError` instead of
   repairing the tiers.
3. A `Weighted` constructor that **throws** `WeightSumError` when the
   weights do not total 100.
4. **Saving and loading** the gradebook to `gradebook.csv`: loaded at
   startup, saved from a new **Save** option, and saved again on Quit. A
   malformed file produces a `FileFormatError` that names the file and line.
5. `try`/`catch` blocks in `main` that report each error and keep the program
   running, plus the return of **custom category weights** when choosing a
   weighted scheme.

The menu grows to nine options: Add student, Report, Sort, **Edit scale**
(renamed), Change scheme, Statistics, Find by ID, **Save** (new), and Quit.

> **Scope:** Complete only the Chapter 24 code checkpoint here. Final-project
> documentation, finishing touches, and submission instructions will be
> provided separately.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradebookerror.h` | Create (Step 1) |
| `gradescale.h`, `gradescale.cpp` | Edit (Step 2) |
| `gradingscheme.h`, `gradingscheme.cpp` | Edit (Step 3) |
| `gradebook.h`, `gradebook.cpp` | Edit (Step 4) |
| `main.cpp` | Edit (Steps 5–10) |
| `assignment.*`, `student.*`, `statistics.h` | **No change** — keep them open |

When you are finished your project has **thirteen files**.

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

#### Build it: step by step

##### Step 1 — Write the exception hierarchy

Create a new file named `gradebookerror.h` and enter this code:

```cpp
// gradebookerror.h - Grade Calculator v4.0 - Chapter 24
#ifndef GRADEBOOKERROR_H
#define GRADEBOOKERROR_H

#include <sstream>
#include <stdexcept>
#include <string>

/**
 * Base class for every error this application reports.
 *
 * Deriving from std::runtime_error means these can be caught either
 * specifically, or as GradebookError, or as std::exception - a caller chooses
 * how much it wants to know. A function that cannot produce a sensible return
 * value for bad input throws instead of returning a sentinel nobody checks.
 */
class GradebookError : public std::runtime_error {
public:
    explicit GradebookError(const std::string& what) : std::runtime_error(what) {}
};

/** A grade scale whose tiers do not descend, or that does not reach 0. */
class InvalidScaleError : public GradebookError {
public:
    explicit InvalidScaleError(const std::string& what)
        : GradebookError("Invalid grade scale: " + what) {}
};

/** Category weights that do not total 100 percent. */
class WeightSumError : public GradebookError {
public:
    explicit WeightSumError(double actual)
        : GradebookError(describe(actual)), actual_(actual) {}
    double actual() const { return actual_; }
private:
    static std::string describe(double actual) {
        std::ostringstream out;
        out.setf(std::ios::fixed);
        out.precision(1);
        out << "Category weights total " << actual << " percent; they must total 100.";
        return out.str();
    }
    double actual_;
};

/** A gradebook file that cannot be parsed. */
class FileFormatError : public GradebookError {
public:
    FileFormatError(const std::string& filename, int line, const std::string& why)
        : GradebookError("Cannot read '" + filename + "' at line "
                         + std::to_string(line) + ": " + why),
          filename_(filename), line_(line) {}
    const std::string& filename() const { return filename_; }
    int line() const { return line_; }
private:
    std::string filename_;
    int line_;
};

#endif
```

- `GradebookError` **inherits from `std::runtime_error`**, so every error this
  program throws can be caught as a `GradebookError`, or more generally as a
  `std::exception`. The message passed to the constructor is what `what()`
  returns later.
- Each derived class adds a prefix or builds a more specific message.
  `WeightSumError` formats the actual total into its message and also keeps it
  in `actual()`. `FileFormatError` records the file name and line number.
- A thrown exception carries **data**, not just a message, so the code that
  catches it can decide what to do.

##### Step 2 — Make `GradeScale` refuse instead of repair

In `gradescale.h`, find the first line:

```cpp
// gradescale.h - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// gradescale.h - Grade Calculator v4.0 - Chapter 24
```

Inside the class, find the two constructor declarations:

```cpp
    GradeScale();
    explicit GradeScale(const std::vector<Tier>& requested);
```

Replace it with:

```cpp
    GradeScale();

    /**
     * Builds a scale from user-supplied tiers.
     * @throws InvalidScaleError if the tiers do not strictly descend, if any
     *         cutoff is negative, or if the scale does not reach 0.
     *
     * v2.5 quietly repaired bad input, which meant a user could type a broken
     * scale and get grades computed from something they never asked for.
     * Refusing to construct is the honest behavior; the caller reports why.
     */
    explicit GradeScale(const std::vector<Tier>& requested);
```

In `gradescale.cpp`, find the first lines of the file:

```cpp
// gradescale.cpp - Grade Calculator v2.6 - Chapter 19
#include "gradescale.h"

#include <iomanip>
#include <ostream>
```

Replace it with:

```cpp
// gradescale.cpp - Grade Calculator v4.0 - Chapter 24
#include "gradescale.h"
#include "gradebookerror.h"

#include <iomanip>
#include <string>
#include <ostream>
```

Find the start of the constructor that takes tiers:

```cpp
GradeScale::GradeScale(const std::vector<Tier>& requested) {
```

Delete that line and everything below it (the body of that constructor), down to and including this line:

```cpp
}
```

In its place, enter:

```cpp
GradeScale::GradeScale(const std::vector<Tier>& requested) {
    if (requested.empty()) {
        throw InvalidScaleError("no tiers were given.");
    }
    for (const Tier& t : requested) {
        if (t.cutoff < 0.0) {
            throw InvalidScaleError(std::string("tier '") + t.letter
                                    + "' has a negative cutoff.");
        }
        if (!tiers_.empty() && t.cutoff >= tiers_.back().cutoff) {
            throw InvalidScaleError(std::string("tier '") + t.letter + "' at "
                + std::to_string(static_cast<int>(t.cutoff))
                + " is not below the previous tier at "
                + std::to_string(static_cast<int>(tiers_.back().cutoff)) + ".");
        }
        tiers_.push_back(t);
    }
    if (tiers_.back().cutoff > 0.0) {
        throw InvalidScaleError("the lowest tier must have a cutoff of 0 so that"
                                " every percentage maps to a letter.");
    }
}
```

**The invariant did not change** — cutoffs still strictly descend and the
lowest tier is still 0. Only the response to a violation changed: instead of
skipping or patching a bad tier, the constructor **throws**. A constructor
that throws never finishes, so **no half-built `GradeScale` can exist**.

The doc comment in the header now says `@throws InvalidScaleError`, so anyone
calling the constructor knows to be ready for it.

> **▶ Run checkpoint:** Click **Run** with every file open, including `gradebookerror.h`. The program should compile cleanly. Do **not** test *Custom scale* yet — nothing catches the new exception until Step 9, so a bad scale would end the program.

##### Step 3 — Make `Weighted` refuse weights that do not total 100

In `gradingscheme.h`, find the first line:

```cpp
// gradingscheme.h - Grade Calculator v3.2 - Chapter 22
```

Replace it with:

```cpp
// gradingscheme.h - Grade Calculator v4.0 - Chapter 24
```

In `class Weighted`, find the two constructor declarations:

```cpp
    Weighted();
    explicit Weighted(const std::vector<CategoryWeight>& weights);
```

Replace it with:

```cpp
    Weighted();

    /**
     * @throws WeightSumError if the weights do not total 100 percent.
     *         A gradebook that silently normalizes bad weights produces
     *         grades the instructor did not ask for.
     */
    explicit Weighted(const std::vector<CategoryWeight>& weights);
```

In `gradingscheme.cpp`, find the first two lines:

```cpp
// gradingscheme.cpp - Grade Calculator v3.1 - Chapter 21
#include "gradingscheme.h"
```

Replace it with:

```cpp
// gradingscheme.cpp - Grade Calculator v4.0 - Chapter 24
#include "gradingscheme.h"
#include "gradebookerror.h"
```

Find the `Weighted` constructor that takes weights:

```cpp
Weighted::Weighted(const std::vector<CategoryWeight>& weights)
    : GradingScheme("Weighted"), weights_(weights) {}
```

Replace it with:

```cpp
Weighted::Weighted(const std::vector<CategoryWeight>& weights)
    : GradingScheme("Weighted"), weights_(weights) {
    if (!weightsValid()) {
        throw WeightSumError(weightTotal());
    }
}
```

In v3.0 weights that did not total 100 were scaled proportionally, with only
a note. Now the constructor uses its own `weightsValid()` check and throws a
`WeightSumError` carrying the actual total.

`WeightedDropLowest`'s weights-taking constructor calls this constructor, so
it gets the same check **for free** — you do not change `WeightedDropLowest`
at all.

##### Step 4 — Let a `Gradebook` be moved, and keep IDs unique

Loading a file will build a complete new `Gradebook` and then move it into
place. A `Gradebook` cannot be copied (it holds a `unique_ptr`), but it can be
**moved**.

In `gradebook.h`, find the first line:

```cpp
// gradebook.h - Grade Calculator v3.3 - Chapter 23
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v4.0 - Chapter 24
```

Find the constructor and the comment below it:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");

    // No destructor is needed now. unique_ptr releases the scheme when the
```

Replace it with:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");

    // Movable so a fully-built replacement can be swapped in atomically after
    // a successful load. Copying stays disabled: schemes are uniquely owned.
    Gradebook(Gradebook&&) = default;
    Gradebook& operator=(Gradebook&&) = default;

    // No destructor is needed now. unique_ptr releases the scheme when the
```

`= default` asks the compiler to generate the move constructor and move
assignment operator. Each member is moved in turn — including the
`unique_ptr`, which hands over its scheme.

There is one more thing to fix before students can be loaded from a file. A
loaded student keeps the ID it was saved with, but the `Gradebook`'s next-ID
counter starts at 1001 every time the program runs. Without a fix, the first
student you add after a reload would get an ID that is already taken.

In `gradebook.cpp`, find the first line:

```cpp
// gradebook.cpp - Grade Calculator v3.3 - Chapter 23
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v4.0 - Chapter 24
```

In `addStudent`, find:

```cpp
    roster_.push_back(s);
    idIndex_[s.id()] = roster_.size() - 1;
```

Directly below it, add:

```cpp
    // A student loaded from a file keeps its saved ID. Move the counter past
    // it so the next new student never receives an ID that is already taken.
    if (s.id() >= nextId_) { nextId_ = s.id() + 1; }
```

`addStudent` is the one place every student enters the roster — typed in or
loaded — so this is the one place the counter has to be kept ahead of the
IDs already in use. **A class protects its own invariants**; here the
invariant is "every ID handed out is unused."

##### Step 5 — Update the header comment and includes in `main.cpp`

At the top of `main.cpp`, find the header comment:

```cpp
// =============================================================================
//  Grade Calculator  v3.3                                          Chapter 23
// -----------------------------------------------------------------------------
//  Change  : Templates and the STL. Statistics<T> computes mean, median,
//            range, and standard deviation for any numeric type. std::map
//            indexes students by ID and counts the letter distribution.
//            Sorting is expressed with a lambda instead of operator<.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

Replace it with:

```cpp
// =============================================================================
//  Grade Calculator  v4.0                                          Chapter 24
//  RELEASE BUILD
// -----------------------------------------------------------------------------
//  Change  : Errors are reported as exceptions from a GradebookError hierarchy
//            instead of silently repaired or returned as sentinel values.
//              InvalidScaleError  tiers that do not descend or reach 0
//              WeightSumError     category weights that do not total 100
//              FileFormatError    a gradebook file that cannot be parsed
//            Bad input now costs the user one clear message and one retry,
//            never a grade computed from something they did not ask for.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
//  Usage   : see README.md
// =============================================================================
```

Below it, find the includes:

```cpp
#include "gradebook.h"

#include <iostream>
#include <memory>
#include <utility>
#include <limits>
#include <string>
```

Replace it with:

```cpp
#include "gradebook.h"
#include "gradebookerror.h"

#include <fstream>
#include <iostream>
#include <limits>
#include <memory>
#include <sstream>
#include <string>
#include <utility>

const std::string DEFAULT_FILE = "gradebook.csv";
```

`<fstream>` and `<sstream>` are back for file input and output, and
`DEFAULT_FILE` names the file the gradebook is saved to.

##### Step 6 — Add `splitCsv` and `saveGradebook`

Find the comment just above `chooseScheme` (below `readLine`):

```cpp
/** Builds the scheme the user asked for. The only place that names the
```

Directly above it, add:

```cpp
// -----------------------------------------------------------------------------
//  Persistence
// -----------------------------------------------------------------------------

std::vector<std::string> splitCsv(const std::string& line) {
    std::vector<std::string> fields;
    std::istringstream in(line);
    std::string field;
    while (std::getline(in, field, ',')) { fields.push_back(field); }
    return fields;
}

void saveGradebook(const Gradebook& book, const std::string& filename) {
    std::ofstream out(filename);
    if (!out) {
        throw GradebookError("Cannot open '" + filename + "' for writing.");
    }
    out << "# Grade Calculator gradebook, format version 2\n";
    for (const GradeScale::Tier& t : book.scale().tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (std::size_t i = 0; i < book.size(); ++i) {
        const Student& s = book[i];
        out << "STUDENT," << s.id() << "," << s.name() << "\n";
        for (const Assignment& a : s.assignments()) {
            out << "WORK," << s.id() << "," << a.name() << "," << a.pointsEarned()
                << "," << a.pointsPossible() << "," << a.bonusPoints()
                << "," << a.category() << "\n";
        }
    }
    if (!out.good()) {
        throw GradebookError("Writing '" + filename + "' failed partway through.");
    }
}
```

- `splitCsv` is the same helper you wrote in Chapter 15.
- The file format is **version 2**: `TIER` lines for the scale, then a
  `STUDENT` line for each student, followed by one `WORK` line per assignment
  — including its **category**.
- `saveGradebook` returns nothing. If the file cannot be opened, or the
  writing fails partway through, it **throws** a `GradebookError` instead of
  returning `false` for a caller to forget to check.

##### Step 7 — Add `loadGradebook`, which builds a replacement first

Find the same comment line again — it is now just below `saveGradebook`:

```cpp
/** Builds the scheme the user asked for. The only place that names the
```

Directly above it, add:

```cpp
/** @throws FileFormatError if any record is malformed. */
void loadGradebook(Gradebook& book, const std::string& filename) {
    std::ifstream in(filename);
    if (!in) {
        throw GradebookError("No file named '" + filename + "' was found.");
    }

    std::vector<GradeScale::Tier> tiers;
    std::vector<Student> loaded;
    std::string line;
    int lineNumber = 0;

    while (std::getline(in, line)) {
        ++lineNumber;
        if (line.empty() || line[0] == '#') { continue; }
        std::vector<std::string> f = splitCsv(line);
        if (f.empty()) { continue; }

        try {
            if (f[0] == "TIER") {
                if (f.size() < 3 || f[2].empty()) {
                    throw FileFormatError(filename, lineNumber, "a TIER needs a cutoff and a letter.");
                }
                tiers.push_back({std::stod(f[1]), f[2][0]});
            } else if (f[0] == "STUDENT") {
                if (f.size() < 3) {
                    throw FileFormatError(filename, lineNumber, "a STUDENT needs an ID and a name.");
                }
                loaded.push_back(Student(f[2], std::stoi(f[1])));
            } else if (f[0] == "WORK") {
                if (f.size() < 7) {
                    throw FileFormatError(filename, lineNumber, "a WORK record needs seven fields.");
                }
                int owner = std::stoi(f[1]);
                bool placed = false;
                for (Student& s : loaded) {
                    if (s.id() == owner) {
                        s.addAssignment(Assignment(f[2], std::stod(f[3]),
                                                   std::stod(f[4]), std::stod(f[5]), f[6]));
                        placed = true;
                        break;
                    }
                }
                if (!placed) {
                    throw FileFormatError(filename, lineNumber,
                                          "work belongs to unknown student ID " + f[1] + ".");
                }
            } else {
                throw FileFormatError(filename, lineNumber, "unrecognized record type '" + f[0] + "'.");
            }
        } catch (const std::invalid_argument&) {
            // stod and stoi throw this on non-numeric text. Translate it into
            // an error that names the file and line the user can actually fix.
            throw FileFormatError(filename, lineNumber, "expected a number here.");
        } catch (const std::out_of_range&) {
            throw FileFormatError(filename, lineNumber, "a number is out of range.");
        }
    }

    // Build the scale first: if it is invalid, nothing is loaded.
    Gradebook fresh(book.courseName());
    if (!tiers.empty()) {
        fresh.setScale(GradeScale(tiers));   // may throw InvalidScaleError
    }
    for (const Student& s : loaded) { fresh.addStudent(s); }
    book = std::move(fresh);
}

// -----------------------------------------------------------------------------
```

Read this function in two halves.

**Reading.** Every line is parsed into local variables — `tiers` and
`loaded` — never directly into `book`. Inside the loop:

- A record with too few fields, a `WORK` line for an unknown student, or an
  unrecognized record type throws a `FileFormatError` naming the line.
- `std::stod` and `std::stoi` throw `std::invalid_argument` on text that is
  not a number, and `std::out_of_range` on a number too large. The `catch`
  blocks **translate** those library exceptions into a `FileFormatError` that
  names the file and line the user can actually fix.

**Committing.** Only after the whole file has been read does the function
build a `fresh` gradebook, set its scale (which may throw
`InvalidScaleError`), add the students, and finally
`book = std::move(fresh);`. If anything throws before that last line, `book`
is **untouched** — the load either succeeds completely or changes nothing.
That is what the move operations from Step 4 make possible.

The `// ----` line at the end separates the persistence section from the
menu helpers below it.

> **▶ Run checkpoint:** Click **Run**. The program should compile cleanly; the new functions exist but are not called yet.

##### Step 8 — Rewrite `chooseScheme` to accept custom weights safely

Find the comment above `chooseScheme`:

```cpp
/** Builds the scheme the user asked for. The only place that names the
```

Delete that line and everything below it (the whole `chooseScheme` function), down to and including this line:

```cpp
}
```

In its place, enter:

```cpp
void chooseScheme(Gradebook& book) {
    std::cout << "  1) Points-based\n";
    std::cout << "  2) Weighted by category\n";
    std::cout << "  3) Weighted, lowest dropped per category\n";
    std::string c = readLine("  Choice: ");

    if (c.empty() || c[0] == '1') {
        book.setScheme(std::make_unique<PointsBased>());
    } else {
        std::vector<Weighted::CategoryWeight> weights;
        if (readLine("  Enter your own category weights? (y/n): ").substr(0, 1) == "y") {
            while (true) {
                std::string name = readLine("    Category (or 'done'): ");
                if (name == "done" || name.empty()) { break; }
                weights.push_back({name, readNonNegative("      Weight (percent): ")});
            }
        }
        try {
            if (c[0] == '2') {
                book.setScheme(weights.empty() ? std::make_unique<Weighted>()
                                               : std::make_unique<Weighted>(weights));
            } else {
                book.setScheme(weights.empty() ? std::make_unique<WeightedDropLowest>()
                                               : std::make_unique<WeightedDropLowest>(weights));
            }
        } catch (const WeightSumError& e) {
            std::cout << "  " << e.what() << "\n";
            std::cout << "  The grading scheme was not changed.\n";
            return;
        }
    }
    std::cout << "  Grading is now: " << book.schemeName() << "\n";
}
```

- Points-based grading is chosen as before.
- For either weighted scheme, the user may now enter their own categories
  and weights. If they enter none, the default weights are used.
- Creating the scheme sits inside a `try` block. If the weights do not total
  100, the `Weighted` constructor throws, the `catch` prints the error's
  message, and the function **returns early** — `setScheme` was never reached,
  so the previous scheme is still in effect.

##### Step 9 — Add `editScale`

Find the first line of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
void editScale(Gradebook& book) {
    std::vector<GradeScale::Tier> requested;
    std::cout << "  Enter tiers highest first; the lowest must be 0. 'done' to finish.\n";
    while (true) {
        std::string lt = readLine("    Letter (or 'done'): ");
        if (lt == "done" || lt.empty()) { break; }
        requested.push_back({readNonNegative("      Minimum percentage: "), lt[0]});
    }
    try {
        book.setScale(GradeScale(requested));
        std::cout << "  " << book.scale() << "\n";
    } catch (const InvalidScaleError& e) {
        // The old scale is untouched: the new one was never constructed.
        std::cout << "  " << e.what() << "\n";
        std::cout << "  Your previous scale is still in effect.\n";
    }
}
```

This is the *Custom scale* code from `main`, moved into its own function and
protected by `try`/`catch`. Look at the comment in the `catch` block: because
`GradeScale(requested)` throws **before** `book.setScale(...)` runs, the old
scale is never replaced. The user sees why the scale was refused and keeps
the scale they had.

##### Step 10 — Rewrite `main`: load, catch, save

Find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it, all the way to the final closing `}` at the very end of the file.

In its place, enter the new `main`:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v4.0 ===\n\n";

    Gradebook book("Programming Fundamentals");

    try {
        loadGradebook(book, DEFAULT_FILE);
        std::cout << "Loaded " << DEFAULT_FILE << " (" << book.size() << " students).\n";
    } catch (const GradebookError& e) {
        std::cout << e.what() << "\n";
        std::cout << "Starting a new gradebook.\n";
    }

    std::cout << "\nSelect a grading scheme:\n";
    chooseScheme(book);

    bool running = true;
    while (running) {
        std::cout << "\n1) Add student  2) Report  3) Sort  4) Edit scale\n"
                     "5) Change scheme  6) Statistics  7) Find by ID  "
                     "8) Save  9) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char c = line.empty() ? '?' : line[0];

        try {
            if (c == '1') {
                std::string name = readLine("  Student name: ");
                if (name.empty()) { continue; }
                Student s(name, book.claimNextId());
                while (true) {
                    std::string an = readLine("    Assignment name (or 'done'): ");
                    if (an == "done" || an.empty()) { break; }
                    double earned   = readNonNegative("      Points earned  : ");
                    double possible = readNonNegative("      Points possible: ");
                    double bonus    = readNonNegative("      Bonus points   : ");
                    std::string cat = readLine("      Category       : ");
                    if (cat.empty()) { cat = "Uncategorized"; }
                    s.addAssignment(Assignment(an, earned, possible, bonus, cat));
                }
                book.addStudent(s);
                std::cout << "  Added " << s.name() << " as ID " << s.id() << ".\n";
            } else if (c == '2') {
                std::cout << book << "\n";
            } else if (c == '3') {
                book.sortByPercentage();
                std::cout << "  Sorted.\n";
            } else if (c == '4') {
                editScale(book);
            } else if (c == '5') {
                chooseScheme(book);
            } else if (c == '6') {
                std::cout << "\n--- Class statistics ---\n";
                book.printStatistics(std::cout);
            } else if (c == '7') {
                std::string s = readLine("  Student ID: ");
                int id = 0;
                try { id = std::stoi(s); }
                catch (...) { std::cout << "  Not a valid ID.\n"; continue; }
                const Student* found = book.findById(id);
                if (found != nullptr) {
                    std::cout << "  " << found->name() << ": "
                              << book.percentageFor(*found) << "%\n";
                } else {
                    std::cout << "  No student with ID " << id << ".\n";
                }
            } else if (c == '8') {
                saveGradebook(book, DEFAULT_FILE);
                std::cout << "  Saved to " << DEFAULT_FILE << ".\n";
            } else if (c == '9') {
                running = false;
            } else {
                std::cout << "  Please enter 1-9.\n";
            }
        } catch (const GradebookError& e) {
            // Any error our own code raises is reported and the loop continues.
            // No operation leaves the gradebook half-modified.
            std::cout << "  " << e.what() << "\n";
        }
    }

    try {
        saveGradebook(book, DEFAULT_FILE);
        std::cout << "\nGradebook saved. Goodbye.\n";
    } catch (const GradebookError& e) {
        std::cout << "\nWarning: " << e.what() << "\n";
        std::cout << "Your work was not saved. Goodbye.\n";
        return 1;
    }
    return 0;
}
```

- **Startup** tries to load `gradebook.csv`. If there is no file, or it is
  malformed, the error is printed and a new gradebook starts.
- **The whole menu body is inside one `try` block.** Any `GradebookError`
  raised by an option is caught at the bottom of the loop, its message is
  printed, and the loop continues. The `catch` names `GradebookError`, so it
  handles all three specific errors.
- **Edit scale** (option 4) calls `editScale`, and **Change scheme**
  (option 5) calls the new `chooseScheme`.
- **Save** (option 8) is new. **Quit** moves to option 9.
- **On exit** the gradebook is saved. If that fails, the program says so and
  returns `1` — a nonzero exit code tells the operating system something went
  wrong.

> **▶ Run checkpoint:** Make sure all thirteen files are open and click **Run**. The program should compile with no errors and no warnings. On the first run it prints `No file named 'gradebook.csv' was found.` and `Starting a new gradebook.` — that is correct.

#### Check your work

Work through this test plan in the Terminal. A release is a claim that you
tested the whole program, not only the cases you happened to try while typing.

1. **Fresh start.** Choose `1` (Points-based). Add `Ada` with one assignment:
   `HW1`, earned `9`, possible `10`, bonus `0`, category Enter. Report with
   `2`: `1001  Ada                     90.0%   A`.
2. **An invalid scale is refused.** Choose `4` (Edit scale). Enter `A` with
   `80`, then `B` with `85`, then `done`. You should see:

   ```text
     Invalid grade scale: tier 'B' at 85 is not below the previous tier at 80.
     Your previous scale is still in effect.
   ```

   Report again: Ada is still an `A` under the default scale.
3. **A scale that does not reach 0 is refused.** Choose `4` and enter only `A`
   with `90`, then `done`. You should see a message that the lowest tier must
   have a cutoff of 0, and the previous scale stays in effect.
4. **Bad weights are refused.** Choose `5`, then `2`, answer `y`, and enter
   `Exam` `50` and `Homework` `30`, then `done`. You should see:

   ```text
     Category weights total 80.0 percent; they must total 100.
     The grading scheme was not changed.
   ```

5. **Save and reload.** Choose `8`. You should see
   `Saved to gradebook.csv.` Then choose `9` to quit; the program prints
   `Gradebook saved. Goodbye.` Click **Run** again: the program should print
   `Loaded gradebook.csv (1 students).` Choose a scheme, then report — Ada is
   back with 90.0%. Now add a new student, `Bo`, with no assignments
   (type `done` right away). The program should print `Added Bo as ID 1002.`
   — not 1001, which Ada already has.

Then confirm:

- [ ] All thirteen files build together with no errors and no warnings.
- [ ] No input you can type makes the program crash or stop unexpectedly.
- [ ] Every `throw` in the program throws a class derived from
      `GradebookError`, and every `catch` catches by **`const` reference**.
- [ ] `assignment.*`, `student.*`, and `statistics.h` are unchanged from
      Chapter 23.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click all twelve project files to open them. You will create `gradebookerror.h` during the lab.
   Confirm the editor shows the expected file paths before editing.
4. Work through Steps 1–10 above in StudySite's internal editor, in order, clicking **Run** at each ▶ Run checkpoint.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

> **Compiling:** In StudySite.ai, just click **Run**. StudySite generates the
> compile command for you, then builds and runs the program in one step, so
> you never type one here. The `Build` line in `main.cpp`'s header comment is
> for building on your own computer instead. For this chapter:
>
> **macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):
>
> ```bash
> clang++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — all thirteen files, including the new `gradebookerror.h`. You do not need to commit `gradebook.csv`. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 24 Grade Calculator v4.0**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 24
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## The Road Ahead

You can now read and write substantial C++. Some directions worth knowing about.

**Modern C++ beyond C++17.** C++20 adds concepts (stating a template's requirements, so error messages point at your call), ranges (composable algorithms without explicit iterators), and modules (an alternative to headers that would change Chapter 2's translation pipeline considerably).

**Testing frameworks.** Chapter 16's `check` harness is a small version of Catch2 or GoogleTest, which add fixtures, parameterized tests, and reporting.

**Concurrency.** `<thread>` and `<mutex>` let a program do several things at once, with a new class of defect that the debugging discipline of Chapter 16 extends to reach.

**Data structures and algorithms.** Chapter 17 covered searching and sorting. Trees, graphs, and hash tables follow, along with the analysis that makes the choices principled.

**Beyond the console.** Every program here reads `std::cin` and writes `std::cout`. Graphical interfaces, web services, and databases are the obvious next boundaries.

**What transfers.** The languages will change. The habits will not: design before coding, name what you decide, verify rather than assume, test at boundaries, encapsulate what should not be reachable, and leave your code readable by whoever inherits it. That last person is often you.

---

## Try It Yourself

### 1. A custom exception hierarchy

```cpp
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

class GradebookError : public std::runtime_error {
public:
    explicit GradebookError(const std::string& w) : std::runtime_error(w) {}
};

class InvalidScaleError : public GradebookError {
public:
    explicit InvalidScaleError(const std::string& w)
        : GradebookError("Invalid grade scale: " + w) {}
};

class WeightSumError : public GradebookError {
public:
    explicit WeightSumError(double actual)
        : GradebookError(describe(actual)), actual_(actual) {}
    double actual() const { return actual_; }
private:
    static std::string describe(double a) {
        std::ostringstream o;
        o.setf(std::ios::fixed);
        o.precision(1);
        o << "Category weights total " << a << " percent; they must total 100.";
        return o.str();
    }
    double actual_;
};

void tryIt(int which) {
    try {
        if (which == 1) { throw InvalidScaleError("tier 'B' at 85 is not below 80."); }
        if (which == 2) { throw WeightSumError(80.0); }
        if (which == 3) { throw std::runtime_error("something else entirely"); }
    }
    catch (const InvalidScaleError& e) { std::cout << "  InvalidScaleError: " << e.what() << "\n"; }
    catch (const GradebookError& e)    { std::cout << "  GradebookError:    " << e.what() << "\n"; }
    catch (const std::exception& e)    { std::cout << "  std::exception:    " << e.what() << "\n"; }
}

int main() {
    for (int i = 1; i <= 3; ++i) { tryIt(i); }
    return 0;
}
```

**Expected output:**

```text
  InvalidScaleError: Invalid grade scale: tier 'B' at 85 is not below 80.
  GradebookError:    Category weights total 80.0 percent; they must total 100.
  std::exception:    something else entirely
```

*Try:* Move the `std::exception` clause first and rebuild. Read the warning, then predict which handler catches each throw.

### 2. Stack unwinding

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>

struct Noisy {
    std::string n;
    explicit Noisy(std::string s) : n(std::move(s)) { std::cout << "  built " << n << "\n"; }
    ~Noisy() { std::cout << "  destroyed " << n << "\n"; }
};

int main() {
    try {
        Noisy a("a");
        Noisy b("b");
        throw std::runtime_error("boom");
    } catch (const std::runtime_error& e) {
        std::cout << "  handler: " << e.what() << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
  built a
  built b
  destroyed b
  destroyed a
  handler: boom
```

*Try:* In what order were they destroyed, and why that order? Now imagine `Noisy` held a `new`ed pointer released in its destructor — what does that tell you about RAII and exceptions?

### 3. An exception that carries data

```cpp
#include <iostream>
#include <stdexcept>

class TooLarge : public std::runtime_error {
public:
    explicit TooLarge(int value)
        : std::runtime_error("value is too large"), value_(value) {}
    int value() const { return value_; }
private:
    int value_;
};

int main() {
    try {
        throw TooLarge(150);
    } catch (const TooLarge& e) {
        std::cout << e.what() << ": " << e.value() << "\n";
        std::cout << "clamped to " << (e.value() > 100 ? 100 : e.value()) << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
value is too large: 150
clamped to 100
```

*Try:* Catch it as `const std::runtime_error&` instead. Can you still call `value()`? What does that tell you about catching too generally?

### 4. Catching by value slices

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

class Specific : public std::runtime_error {
public:
    Specific() : std::runtime_error("specific message") {}
};

int main() {
    try {
        throw Specific();
    } catch (std::runtime_error e) {          // by value — sliced
        std::cout << "by value:     " << e.what() << "\n";
    }
    try {
        throw Specific();
    } catch (const std::runtime_error& e) {   // by reference
        std::cout << "by reference: " << e.what() << "\n";
    }
    return 0;
}
```

**Note:** this listing produces `warning: catching polymorphic type ... by value`. That warning *is* the lesson — the compiler is telling you the exception is about to be sliced. It is the one listing in this book that is not warning-clean, deliberately.

*Try:* Add a virtual function to `Specific` that `std::runtime_error` does not have, and call it in each handler. Which one compiles? Which one would have given you the derived behavior?

### 5. Translate a library exception

Write a function reading a number from a string and throwing your own `ParseError` — naming the line and what was expected — when `std::stod` fails. Catch `std::invalid_argument` and rethrow.

Then compare the two messages. Which would you rather show a user?

### 6. Debug versus release

Build any Grade Calculator version both ways:

```text
g++ -std=c++17 -Wall -Wextra -g main.cpp -o gc_debug
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG main.cpp -o gc_release
```

Compare file sizes. Add an `assert` that fails and run both. Then run your full test plan against the release build — does anything behave differently? If so, you have found undefined behavior.

### 7. Decide: exception or not?

For each, say whether to throw, and why:

- A user types `abc` where a number belongs
- A gradebook file is missing
- A gradebook file exists but line 14 is malformed
- A student ID is not on the roster
- Category weights total 90 percent
- A grade scale has no tier at 0
- The user enters menu choice 9 when options are 1–8
- The program cannot write its save file on exit

---

## Summary

- **Return codes can be ignored.** An exception cannot: unhandled, it terminates the program.
- **`throw`** abandons a function; **`try`**/**`catch`** handles what it throws. **`what()`** gives the message.
- **Always catch by `const` reference.** Catching by value slices the exception.
- `<stdexcept>` provides a hierarchy rooted at `std::exception`. Define your own for your own failures, and let them carry data when a handler could use it.
- Several `catch` clauses may follow one `try`; **the first match wins**, so order most specific to least.
- **Stack unwinding** destroys every local object between the throw and the handler. **This is what makes RAII essential** — manual `delete` is skipped, so any function that can throw leaks if it manages a resource by hand.
- **Build the replacement, then install it**, so a failed operation leaves the object as it was.
- **Throw when a function cannot keep its promise**; do not throw for expected conditions such as invalid typed input.
- **Translation has four stages**: preprocessing, compilation, assembly, and linking. Every "undefined reference" you have met is stage 4 finding a promise nobody kept.
- **Static libraries** are copied in; **dynamic libraries** are loaded at run time.
- **Test the release build**, not only the debug build — optimization can expose undefined behavior.
- A release needs a build, a README, a user guide, and reconciled design documentation.

---

## Key Terms

**catch** — a clause handling an exception of a stated type.

**debug build** — a build with debug information and no optimization.

**dynamic library** — a library loaded when a program runs.

**exception** — an object thrown to signal a condition the caller must handle.

**exception safety** — the property that a failed operation leaves objects in a valid state.

**release build** — an optimized build with assertions removed.

**stack unwinding** — destroying local objects while leaving functions between a throw and its handler.

**static library** — a library copied into an executable at link time.

**throw** — to raise an exception.

**try block** — a region whose exceptions may be handled by following `catch` clauses.

**what()** — the member function returning an exception's message.

---

## Afterword

You began at Chapter 1 with a bit pattern that meant nothing until a program said what it was. You end with an application that computes grades three ways, refuses to be built wrong, explains its failures in sentences, and can be handed to someone else with documentation they can follow.

The specific thing worth noticing: **you wrote twenty-three working programs, and every one of them ran.** Not one chapter left you with something broken. That was a constraint on how this book was written, and it is also a description of how software is best built — in small, complete, verified steps.

The weighted-grading requirement you recorded in Chapter 1 and resolved in Chapter 21 is the same idea at a larger scale. It was written down before it could be built, analyzed before it was understood, deferred deliberately rather than forgotten, and delivered twenty chapters later against a specification that still said what it was supposed to do.

That is the whole discipline, and it transfers to every language you will use after this one.
