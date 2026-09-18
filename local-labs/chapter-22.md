# Chapter 22 Lab — Replace Manual Ownership with Smart Pointers

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.2
- **Starting point:** The working Chapter 21 v3.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Confirm the correct v3.1 program switches schemes and exits normally, with no leak reported by a memory check.
2. On a throwaway copy, temporarily remove the manual `delete scheme_;` inside `setScheme` and observe the memory-safety failure using the available memory check; then restore it (or discard the copy) — v3.1 itself must not ship with this defect.
3. Replace `Gradebook`'s raw owning `GradingScheme*` with `std::unique_ptr<GradingScheme>`.
4. Remove the manual destructor, the manual `delete` inside `setScheme`, and the explicitly deleted copy operations — unique ownership now provides all three for free.
5. Keep all grading behavior unchanged, including the ability to switch schemes mid-session.
6. Carry the Chapter 15–21 features forward onto the smart-pointer `Gradebook`: saving/loading (through the same `typeTag()`/`weightsForSave()`/`SchemeFactory` design, now returning `std::unique_ptr<GradingScheme>` instead of a raw pointer), the regression-test suite, checked access, sort/search, and `WeightedDropLowest`'s own display name.

Item 6 is the one most worth double-checking, exactly as in every chapter since 18: it is easy, while changing how the scheme is owned, to carry forward only the report and quietly lose the rest.

## What changes from Chapter 21

- **Three pieces of ownership bookkeeping become zero.** Chapter 21's `Gradebook` needed a hand-written destructor, a `delete` before every replacement inside `setScheme`, and explicitly deleted copy operations — miss any one and the program leaks or double-frees. None of the three is written in v3.2: `std::unique_ptr<GradingScheme>` is itself move-only and self-cleaning, so the compiler-generated destructor already releases the scheme correctly, and the compiler-generated copy constructor and copy assignment are already deleted because a `unique_ptr` member cannot be copied.
- **`setScheme` takes ownership by value, not by raw pointer.** Its parameter type is `std::unique_ptr<GradingScheme>`, so a caller must hand over a `std::unique_ptr` — typically the direct result of `std::make_unique<Weighted>()`, or an existing one moved with `std::move`. The type system itself makes the ownership transfer visible; Chapter 21's `void setScheme(GradingScheme* scheme)` could not tell a borrowed pointer from an owned one just by looking at the signature.
- **`SchemeFactory` returns `std::unique_ptr<GradingScheme>` instead of `GradingScheme*`.** `Gradebook::load()` still calls it exactly the same way, and `main.cpp`'s `makeScheme()` is still the only other place besides `chooseScheme()` that names a concrete scheme type — only the return type, and `new` becoming `std::make_unique`, changed.
- **The one-line defect from required-work item 2 is a diagnostic exercise, not a feature of the final program.** Removing `delete scheme_;` from a raw-pointer `setScheme` produces a small, silent leak — invisible from the program's own output, and detectable only with a memory-safety tool. That exercise happens on a disposable copy of the *v3.1* code; the v3.2 code you submit never contains the removed line, because it does not contain a manual `delete` at all.
- **Everything else is a straight port.** The regression suite, persistence, sort/search, and checked access change only where they touch scheme ownership directly — nowhere else.

Everything not touched by ownership carries over exactly: `GradeScale`, `Student`, `Assignment`, `PointsBased`, `Weighted`, `WeightedDropLowest`'s grading math, and the report's `operator<<` layout are all unchanged from Chapter 21.

## Build it: step by step

### Step 1 — See the leak Chapter 21 avoided, on a disposable copy

Before changing anything, make a scratch copy of your working Chapter 21 code and delete exactly one line from it: the `delete scheme_;` inside `setScheme`.

```cpp
void Gradebook::setScheme(GradingScheme* scheme) {
    if (scheme == nullptr || scheme == scheme_) { return; }
    // delete scheme_;          <-- temporarily remove this line only
    scheme_ = scheme;
}
```

Build the scratch copy with AddressSanitizer and switch schemes a couple of times:

```bash
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g *.cpp -o gradecalc
./gradecalc
```

Choose a scheme, then use menu option 5 to change it twice more, then quit normally. A leaking build reports something like:

```text
SUMMARY: AddressSanitizer: 264 byte(s) leaked in 4 allocation(s).
```

The program still prints correct grades the whole time — the leak is invisible from the outside, which is exactly why it needs a memory-safety tool to catch, not a glance at the output. Discard this scratch copy (or restore the deleted line) once you have seen the report; it is not part of what you submit.

### Step 2 — Replace the raw pointer with `std::unique_ptr` in `Gradebook`

```cpp
#include <memory>
// ...

class Gradebook {
public:
    explicit Gradebook(const std::string& courseName = "Untitled Course");

    // No destructor, and no deleted copy operations, are written here.
    // Gradebook holds a std::unique_ptr<GradingScheme>, and unique_ptr is
    // itself move-only: the compiler-generated destructor already releases
    // the scheme correctly, and the compiler-generated copy constructor and
    // copy assignment are already deleted because unique_ptr cannot be
    // copied. Chapter 21's three hand-written pieces of ownership bookkeeping
    // all come for free.

    /**
     * Installs a grading scheme. Ownership transfers to the Gradebook.
     * The unique_ptr parameter makes that transfer visible at every call
     * site: a caller must std::move (or hand over a temporary) into it, so
     * ownership is never ambiguous.
     */
    void setScheme(std::unique_ptr<GradingScheme> scheme);

    // ...

private:
    // ...
    // An owning smart pointer to an abstract base. Polymorphism is unchanged
    // from Chapter 21; only the ownership question is answered differently.
    std::unique_ptr<GradingScheme> scheme_;
};
```

Notice what is *not* here: no `~Gradebook()`, and no `Gradebook(const Gradebook&) = delete;` / `Gradebook& operator=(const Gradebook&) = delete;`. All three are gone, not because they stopped mattering, but because `unique_ptr` already enforces them.

### Step 3 — Implement `setScheme` with `std::move`

```cpp
Gradebook::Gradebook(const std::string& courseName)
    : courseName_(courseName), scheme_(std::make_unique<PointsBased>()) {}

void Gradebook::setScheme(std::unique_ptr<GradingScheme> scheme) {
    if (!scheme) { return; }
    // Assigning to a unique_ptr destroys whatever it held first. This one
    // line replaces Chapter 21's manual delete, and the destructor and
    // deleted copy operations that had to accompany it.
    scheme_ = std::move(scheme);
}
```

`percentageFor` and `schemeName` are unchanged from Chapter 21 — `scheme_->computePercentage(...)` and `scheme_->name()` read exactly the same through a `unique_ptr` as they did through a raw pointer.

### Step 4 — Update the `SchemeFactory` type persistence uses to reconstruct a scheme

```cpp
/**
 * Builds a concrete GradingScheme from a saved type tag and, if that
 * scheme uses them, its saved weights. Passed into load() so Gradebook
 * itself never has to name a concrete scheme type - see gradingscheme.h.
 * Returns by unique_ptr, matching setScheme(), so ownership is unambiguous
 * from construction all the way to installation.
 */
using SchemeFactory = std::unique_ptr<GradingScheme> (*)(
    const std::string& tag, const std::vector<Weighted::CategoryWeight>& weights);

bool load(const std::string& filename, std::string& message, SchemeFactory makeScheme);
```

`Gradebook::load()`'s body does not otherwise change: it still parses `COURSE`, `SCHEME`, `NEXTID`, `TIER`, `WEIGHT`, and `STUDENT` lines exactly as Chapter 21 did, and still finishes with `setScheme(makeScheme(loadedTag, loadedWeights));` — only now that call hands over a `unique_ptr` instead of a raw pointer. `save()` is untouched line for line: `scheme_->typeTag()` and `scheme_->weightsForSave()` are called through `operator->` exactly the same way on a `unique_ptr` as they were on a raw pointer.

### Step 5 — Update the two places that name concrete scheme types

```cpp
void chooseScheme(Gradebook& book) {
    std::cout << "  1) Points-based\n";
    std::cout << "  2) Weighted by category\n";
    std::cout << "  3) Weighted, lowest dropped per category\n";
    std::string c = readLine("  Choice: ");
    if (!c.empty() && c[0] == '2') {
        book.setScheme(std::make_unique<Weighted>());
    } else if (!c.empty() && c[0] == '3') {
        book.setScheme(std::make_unique<WeightedDropLowest>());
    } else {
        book.setScheme(std::make_unique<PointsBased>());
    }
    std::cout << "  Grading is now: " << book.schemeName() << "\n";
}

std::unique_ptr<GradingScheme> makeScheme(const std::string& tag,
                                          const std::vector<Weighted::CategoryWeight>& weights) {
    if (tag == "WEIGHTED_DROP_LOWEST") {
        return weights.empty() ? std::make_unique<WeightedDropLowest>()
                                : std::make_unique<WeightedDropLowest>(weights);
    }
    if (tag == "WEIGHTED") {
        return weights.empty() ? std::make_unique<Weighted>()
                                : std::make_unique<Weighted>(weights);
    }
    return std::make_unique<PointsBased>();
}
```

Every `new SomeScheme(...)` from Chapter 21 becomes `std::make_unique<SomeScheme>(...)`. Nothing else in either function changes — `chooseScheme()` is still the only place a fresh session's choice constructs a scheme, and `makeScheme()` is still the only other place, reached only through the `SchemeFactory` function pointer `Gradebook::load()` was given.

### Step 6 — Carry everything else forward unchanged in shape

`GradingScheme`'s pure virtual `computePercentage`, its virtual destructor, `typeTag()`, and `weightsForSave()`; `Weighted`'s protected name-forwarding constructor that lets `WeightedDropLowest` report `"Weighted (lowest dropped)"` instead of plain `"Weighted"`; `Gradebook`'s `SortKey` enum, `sortRoster()`, `linearFindById()`/`binaryFindById()`, and `at()`; and the regression suite's D1 through D6 checks are all untouched — none of them names a raw pointer or a `unique_ptr` anywhere in their own logic, so ownership's change underneath them changes nothing about what they do.

### Step 7 — Confirm the final build is leak-free

Build the real v3.2 submission with AddressSanitizer and repeat Step 1's scheme-switching exercise:

```bash
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g *.cpp -o gradecalc
./gradecalc
```

This time, no matter how many times you switch schemes, there is nothing to report. `unique_ptr` cannot be made to leak by forgetting a line, because there is no longer a line to forget.

## Verification

- The intentional raw-pointer defect from required-work item 2, reproduced on a disposable copy, is detected by AddressSanitizer (or your available memory-safety check) — and does not appear in the code you submit.
- The final `std::unique_ptr` version reports no leak under the same exercise.
- `Gradebook(const Gradebook&) = delete;` no longer appears anywhere, yet copying a `Gradebook` is still rejected by the compiler — because `std::unique_ptr` cannot be copied, and a class containing one inherits that restriction automatically.
- All three grading schemes still produce the Chapter 21 results: 87.5%, 84.4%, and 93.8% for the documented example, and `WeightedDropLowest` still reports as **"Weighted (lowest dropped)"**, not plain `"Weighted"`.
- Saving, quitting, and relaunching still restores the exact concrete scheme that was active, including a `WeightedDropLowest` gradebook.
- `Run tests` should still report **13 of 13 checks passed**.
- `Sort`, `Sort roster`, `Find by ID`, and checked access (`at()`) all still work under any of the three schemes.

## Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Edit the current project files in your local editor.
3. Build every source file:

   ```bash
   g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
   ```

4. Fix every compiler error and warning.
5. Run the program and complete the verification list:

   ```bash
   ./gradecalc
   ```

6. For the Chapter 22 memory checks, build and run with AddressSanitizer —
   once on the disposable Step 1 copy with `delete scheme_;` removed, and
   again on the real Step 7 submission:

   ```bash
   g++ -std=c++17 -Wall -Wextra -fsanitize=address -g *.cpp -o gradecalc
   ./gradecalc
   ```

   Exercise scheme switching several times (menu option 5), quit normally,
   and read the sanitizer report. The disposable copy should report a leak;
   the real submission should report nothing.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 22 Grade Calculator v3.2"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 22 checkpoint.
- The commit is pushed to GitHub.
