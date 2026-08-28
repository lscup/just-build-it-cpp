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

| | Debug | Release |
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
- **Starting point:** The working Chapter 23 v3.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Create a `GradebookError` hierarchy for invalid scales, invalid weights, malformed files, and lookup failures.
2. Throw meaningful exceptions at the point of failure and catch them where the program can explain the problem and continue.
3. Translate low-level conversion and file errors into messages that identify the affected operation.
4. Run the complete regression plan against the Chapter 24 code checkpoint.
5. Complete only the Chapter 24 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.


#### Verification

- Invalid scales and invalid weights are refused without changing the working gradebook.
- Missing and malformed files produce clear messages instead of crashes.
- Points-based, weighted, and weighted-drop-lowest grading all work.
- Save/load, lookup, statistics, and reports all work.
- The repository contains the Chapter 12 foundation plus the completed Chapter 13–24 code checkpoints.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This avoids
   creating files with names such as `_imported` when the same path is already
   open.
3. Click **Load from GitHub**, select **grade-calculator-1437**, and click each source, header,
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
3. Select **grade-calculator-1437** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 24 Grade Calculator v4.0**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1437** contains the Chapter 24 checkpoint.
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
