# Chapter 24 Lab — Add Release-Safe Error Handling

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v4.0
- **Starting point:** The working Chapter 23 v3.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create a `GradebookError` hierarchy (`gradebookerror.h`): a base class deriving from `std::runtime_error`, plus `InvalidScaleError`, `WeightSumError`, and `FileFormatError`.
2. Make `GradeScale`'s constructor throw `InvalidScaleError` instead of repairing bad tiers, and make `Weighted`'s weights-taking constructor throw `WeightSumError` instead of only being queryable through `weightsValid()`.
3. Move persistence out of `Gradebook` and into two free functions, `saveGradebook` and `loadGradebook`, that throw `GradebookError`/`FileFormatError` instead of returning a bool and an out-parameter message.
4. Make `loadGradebook` exception-safe: build a complete replacement `Gradebook` and only move-assign it over the caller's once every record has parsed and every object has constructed without throwing, so a bad file leaves the caller's gradebook completely untouched.
5. Catch each exception where the program can explain the problem and continue — `editScale` and `chooseScheme` report the error and keep the previous scale or scheme; `main` reports a bad save file and starts a new gradebook instead of crashing.
6. Run the complete regression plan against the Chapter 24 code checkpoint, including three new checks for the exception behavior above.
7. Complete only the Chapter 24 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.

Item 6 is the one most worth double-checking, exactly as in every chapter since 18 — but read "What changes from Chapter 23" below first, because this chapter deliberately retires the *lenient* half of Chapter 23's persistence, not the format it saves.

## What changes from Chapter 23

- **`GradeScale`'s constructor refuses bad input instead of repairing it.** Chapters 15 through 23 quietly fixed an out-of-order or incomplete scale so the program could keep running. That meant a user who mistyped a scale got grades computed from something they never asked for, with no warning. The constructor now throws `InvalidScaleError` for an empty tier list, a negative cutoff, tiers that do not strictly descend, or a scale that never reaches 0 — the exact same invariant Chapter 18 stated, just enforced by refusing to construct instead of silently correcting.
- **`Weighted`'s weights-taking constructor refuses weights that do not total 100**, instead of merely letting a caller ask `weightsValid()` and choose to ignore the answer. `WeightSumError` carries the actual total, so the message can say what the total *is*, not just that it is wrong.
- **Persistence moves out of `Gradebook` entirely.** `save()`/`load()` are gone as member functions; `saveGradebook(book, filename)` and `loadGradebook(book, filename, makeScheme)` in `main.cpp` do the same job as free functions, so `Gradebook` itself no longer needs to `#include <fstream>` or know what a file looks like.
- **The file format on disk has not changed.** `saveGradebook`/`loadGradebook` still read and write the exact version-4 format Chapter 21 introduced — `COURSE`/`SCHEME`/`NEXTID`/`TIER`/`WEIGHT`/`STUDENT` — through the same `schemeTypeTag()`/`schemeWeightsForSave()`/`SchemeFactory` design. A file saved by Chapter 21, 22, or 23 loads correctly here, and a file saved here loads correctly there.
- **A record `loadGradebook` cannot recognize is now refused, not skipped.** Chapter 23's `load()` collected a warning message for an unrecognized record or a bad number and kept going, loading everything else it could. This chapter's `loadGradebook` throws `FileFormatError` — naming the file, the line, and the reason — the moment it meets a record it cannot parse, on the theory that a record it cannot understand might also be one it cannot safely ignore.
- **A failed load leaves the caller's gradebook completely untouched — not just "mostly untouched."** Every parsed value is accumulated into local variables while the file is read; only after every line has parsed and a complete `Gradebook` has been built does `loadGradebook` move-assign it over the caller's, in a single statement. If anything throws before that point — a malformed number, an unrecognized record, an invalid scale, invalid weights — the caller's original gradebook was never touched at all. This is what `Gradebook`'s move assignment operator from Chapter 22 makes possible: replacing an entire object's state is one statement, not a sequence of field-by-field updates that could be interrupted halfway through.
- **`editScale` and `chooseScheme` catch what their own construction throws.** `editScale` never calls `book.setScale(...)` unless `GradeScale(requested)` has already succeeded, so a rejected scale leaves the working scale exactly as it was — there is nothing to roll back, because the broken replacement was never built. `chooseScheme` is guarded by the same pattern for consistency, even though every choice it currently offers uses default weights that always total 100.
- **The regression suite grows by three checks**, all new to this chapter: constructing an invalid `GradeScale` throws `InvalidScaleError` (D11), constructing `Weighted` with weights that do not total 100 throws `WeightSumError` and reports the true total (D12), and — the one the lab's own verification list calls out by name — loading a malformed file throws `FileFormatError` *and* leaves a pre-populated sentinel gradebook completely unchanged (D13). That last check is written so that committing parsed data straight into the caller's gradebook while parsing, instead of building a separate replacement first, makes it fail.

## Build it: step by step

### Step 1 — Write the exception hierarchy

```cpp
// gradebookerror.h
#ifndef GRADEBOOKERROR_H
#define GRADEBOOKERROR_H

#include <sstream>
#include <stdexcept>
#include <string>

/** Base class for every error this application reports. Deriving from
 *  std::runtime_error means these can be caught specifically, as
 *  GradebookError, or as std::exception - a caller chooses how much it
 *  wants to know. */
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

Every error type carries a complete, user-facing message built at the point it is thrown — `FileFormatError` in particular already knows the filename and line number, so whoever catches it does not have to reconstruct that context from scratch.

### Step 2 — Make `GradeScale`'s constructor refuse instead of repair

```cpp
// gradescale.cpp
#include "gradescale.h"
#include "gradebookerror.h"

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

The invariant is unchanged from Chapter 18 — cutoffs strictly descend, the lowest tier is 0. Only the response to violating it changed: throwing partway through means `tiers_` is left in whatever partial state it reached, but that does not matter, because a `GradeScale` that threw during construction never finishes constructing — there is no object left for `tiers_` to be a broken member of.

### Step 3 — Make `Weighted`'s weights-taking constructors refuse bad totals

```cpp
// gradingscheme.cpp
Weighted::Weighted(const std::vector<CategoryWeight>& weights)
    : GradingScheme("Weighted"), weights_(weights) {
    if (!weightsValid()) {
        throw WeightSumError(weightTotal());
    }
}

Weighted::Weighted(const std::string& schemeName, const std::vector<CategoryWeight>& weights)
    : GradingScheme(schemeName), weights_(weights) {
    if (!weightsValid()) {
        throw WeightSumError(weightTotal());
    }
}
```

`weightsValid()` and `weightTotal()` are unchanged from Chapter 20 — this chapter does not add a new way to check the weights, it adds a consequence for failing the check that already existed. `WeightedDropLowest`'s weights-taking constructor delegates to the second constructor above, so it inherits the same guarantee automatically.

### Step 4 — Move persistence into free functions that build a replacement first

```cpp
// main.cpp
void saveGradebook(const Gradebook& book, const std::string& filename) {
    std::ofstream out(filename);
    if (!out) {
        throw GradebookError("Cannot write '" + filename + "'.");
    }
    out << "# Grade Calculator gradebook file, version 4 (Chapter 21)\n";
    out << "COURSE," << book.courseName() << "\n";
    out << "SCHEME," << book.schemeTypeTag() << "\n";
    out << "NEXTID," << book.nextId() << "\n";
    for (const GradeScale::Tier& t : book.scale().tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (const auto& w : book.schemeWeightsForSave()) {
        out << "WEIGHT," << w.first << "," << w.second << "\n";
    }
    for (std::size_t i = 0; i < book.size(); ++i) {
        const Student& s = book[i];
        out << "STUDENT," << s.id() << "," << s.name();
        for (const Assignment& a : s.assignments()) {
            out << "," << a.name() << "," << a.pointsEarned() << ","
                << a.pointsPossible() << "," << a.bonusPoints() << "," << a.category();
        }
        out << "\n";
    }
    if (!out.good()) {
        throw GradebookError("Writing '" + filename + "' failed partway through.");
    }
}

bool loadGradebook(Gradebook& book, const std::string& filename, Gradebook::SchemeFactory makeScheme) {
    std::ifstream in(filename);
    if (!in) { return false; }   // no save file yet is normal, not an error

    std::string loadedCourse = book.courseName();
    std::string loadedTag = book.schemeTypeTag();
    std::vector<GradeScale::Tier> loadedTiers;
    std::vector<Weighted::CategoryWeight> loadedWeights;
    std::vector<Student> loadedStudents;
    int loadedNextId = 1001;

    // ... parse every line into the local variables above, exactly as
    //     Chapter 23's load() did, except that a bad number or an
    //     unrecognized record throws FileFormatError instead of noting a
    //     message and continuing (Step 5) ...

    // Nothing above this point has touched book. Everything below builds a
    // complete, independent replacement; only the final statement touches
    // book, and only after every step here has succeeded.
    Gradebook fresh(loadedCourse);
    fresh.setScale(loadedTiers.empty() ? GradeScale() : GradeScale(loadedTiers));
    fresh.setScheme(makeScheme(loadedTag, loadedWeights));
    for (const Student& s : loadedStudents) { fresh.addStudent(s); }
    fresh.setNextId(loadedNextId);

    book = std::move(fresh);
    return true;
}
```

Compare this with Chapter 23's `load()`, which wrote straight into `this` at the end — `courseName_ = loadedCourse; scale_ = ...;` field by field. That worked in Chapter 23 because `load()` never threw partway through: a bad record there just meant a note in `message` and moving on to the next line. Once bad input can throw, field-by-field assignment stops being safe — a throw between the second and third field would leave `book` in a state that never existed on its own. Building `fresh` completely, then replacing `book` with one `std::move`, means there is no such window: either every field changes together, or none of them do.

`Gradebook::gradebook.h`'s `SchemeFactory` and `Gradebook(Gradebook&&) = default;` / `operator=(Gradebook&&) = default;` (from Chapter 22) are what make this pattern work — `Gradebook`'s move assignment already correctly replaces every member, including releasing the old `unique_ptr<GradingScheme>` and taking over the new one, with no extra code required here.

### Step 5 — Translate `stod`/`stoi` failures and reject unrecognized records

```cpp
namespace {
    double parseDouble(const std::string& filename, int lineNumber, const std::string& text) {
        try {
            return std::stod(text);
        } catch (const std::invalid_argument&) {
            throw FileFormatError(filename, lineNumber, "'" + text + "' is not a number.");
        } catch (const std::out_of_range&) {
            throw FileFormatError(filename, lineNumber, "'" + text + "' is out of range.");
        }
    }

    int parseInt(const std::string& filename, int lineNumber, const std::string& text) {
        try {
            return std::stoi(text);
        } catch (const std::invalid_argument&) {
            throw FileFormatError(filename, lineNumber, "'" + text + "' is not a whole number.");
        } catch (const std::out_of_range&) {
            throw FileFormatError(filename, lineNumber, "'" + text + "' is out of range.");
        }
    }
}
```

Every place `loadGradebook` used to call `std::stod`/`std::stoi` directly now calls these instead — `parseInt(filename, lineNumber, f[1])` in place of `std::stoi(f[1])`, and so on for `TIER`, `WEIGHT`, and `STUDENT` records. A record type the loop does not recognize at all now throws directly:

```cpp
} else {
    // Chapter 23's load() noted this in a message and kept going.
    // This version refuses instead.
    throw FileFormatError(filename, lineNumber, "unrecognized record '" + f[0] + "'.");
}
```

`std::invalid_argument` and `std::out_of_range` are standard library exceptions that say a conversion failed, but not which file, which line, or what a user should do about it. Catching them and throwing `FileFormatError` in their place turns a low-level failure into a message someone can act on.

### Step 6 — Catch each exception where the program can explain and continue

```cpp
void editScale(Gradebook& book) {
    std::vector<GradeScale::Tier> requested;
    // ... read tiers from the user ...
    try {
        book.setScale(GradeScale(requested));
        std::cout << "  " << book.scale() << "\n";
    } catch (const InvalidScaleError& e) {
        std::cout << "  " << e.what() << " Keeping the previous scale.\n";
    }
}

void chooseScheme(Gradebook& book) {
    // ... read the user's choice ...
    try {
        // ... construct the chosen scheme with its default weights ...
        std::cout << "  Grading is now: " << book.schemeName() << "\n";
    } catch (const WeightSumError& e) {
        std::cout << "  " << e.what() << " Keeping the previous scheme.\n";
    }
}
```

In `editScale`, `book.setScale(...)` is never reached unless `GradeScale(requested)` succeeded — the broken scale was never built, so there is nothing to roll back. `main()` wraps the startup load the same way:

```cpp
try {
    loaded = loadGradebook(book, DEFAULT_FILE, makeScheme);
    std::cout << (loaded ? "Loaded " + DEFAULT_FILE + ".\n"
                          : "No file named '" + DEFAULT_FILE + "' was found. Starting a new gradebook.\n");
} catch (const GradebookError& e) {
    std::cout << "  " << e.what() << " Starting a new gradebook instead.\n";
}
```

A missing file is not an error — `loadGradebook` returns `false` for that, not a throw. A *malformed* file is an error, and `main()` recovers from it exactly the way it recovers from a missing one: by starting fresh, after telling the user why.

### Step 7 — Update the menu and add three regression checks

The menu is unchanged from Chapter 23 — ten options, compared as whole strings, with option 8 now calling `saveGradebook` inside a `try`/`catch` instead of checking a returned `bool`:

```cpp
} else if (c == "8") {
    try {
        saveGradebook(book, DEFAULT_FILE);
        std::cout << "  Saved to " << DEFAULT_FILE << ".\n";
    } catch (const GradebookError& e) {
        std::cout << "  " << e.what() << "\n";
    }
}
```

The three new regression checks:

```cpp
// Chapter 24: a scale that does not strictly descend must be refused.
bool threw11 = false;
try {
    GradeScale bad({ {50.0, 'A'}, {80.0, 'B'} });   // out of order
} catch (const InvalidScaleError&) {
    threw11 = true;
}
check(threw11, "D11 GradeScale with non-descending tiers throws InvalidScaleError");

// Chapter 24: weights that do not total 100 must be refused, with the
// actual total reported.
bool threw12 = false;
try {
    Weighted bad({ {"Exam", 50.0}, {"Homework", 40.0} });   // totals 90, not 100
} catch (const WeightSumError& e) {
    threw12 = true;
    check(std::abs(e.actual() - 90.0) < 0.01,
          "D12 WeightSumError reports the actual total (90.0)");
}
check(threw12, "D12 Weighted with weights not totaling 100 throws WeightSumError");

// Chapter 24: a malformed file must be refused, and the gradebook passed
// into loadGradebook() must come out exactly as it went in.
// ... write a file with a STUDENT record whose ID field is not a number,
//     pre-populate a "sentinel" Gradebook with one student, remember its
//     course name and size, call loadGradebook(sentinel, badFile, makeScheme) ...
check(threw13, "D13 loading a malformed file throws FileFormatError");
check(sentinel.courseName() == sentinelCourseBefore && sentinel.size() == sentinelSizeBefore,
      "D13 a failed load leaves the caller's gradebook completely untouched");
```

D13 is written so that committing parsed values straight into `book` while the file is still being read — instead of accumulating into local variables and swapping in one `std::move` at the end — makes it fail. That was checked directly while building this chapter: moving `fresh.addStudent(s)` to a `book.addStudent(s)` executed *during* the parse loop, ahead of the malformed record that throws, made the second D13 check report **FAIL**, exactly as the atomic-swap design predicts. The passing version you are building is the one that keeps every mutation inside `fresh` until the very last line.

## Verification

- Entering an out-of-order custom scale (for example, A at 80, then B at 85) is refused: **Custom scale** reports the specific problem and the working scale is unchanged.
- Reloading with weights that do not total 100 is refused: the scheme is unchanged, and the reported message states the actual total (for example, "Category weights total 80.0 percent; they must total 100.").
- Starting the program with no `gradebook.csv` present reports "No file... was found" and starts a new gradebook — this is not an error path.
- Starting the program with a `gradebook.csv` containing an unrecognized record, or a non-numeric field where a number is expected, reports the specific file and line and starts a new gradebook instead of crashing.
- A gradebook saved by this chapter loads correctly if you rename it and load it with the Chapter 21, 22, or 23 program, and vice versa — the file format itself did not change.
- Points-based, weighted, and weighted-drop-lowest grading, plus save/load, sorting, `findById`, and statistics, all still work exactly as in Chapter 23.
- `Run tests` should report **26 of 26 checks passed**.
- Building with `-fsanitize=address` and switching schemes, throwing and catching every exception path, and exiting reports no leaks — `Gradebook`'s move assignment (Chapter 22) still runs cleanly when it is invoked from `loadGradebook` instead of by hand.

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

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 24 Grade Calculator v4.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 24 checkpoint.
- The commit is pushed to GitHub.
