# Chapter 24 Lab — Add Release-Safe Error Handling

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v4.0
- **Starting point:** Your committed Chapter 23 v3.3 program (twelve files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

### What you will build

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

### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradebookerror.h` | Create (Step 1) |
| `gradescale.h`, `gradescale.cpp` | Edit (Step 2) |
| `gradingscheme.h`, `gradingscheme.cpp` | Edit (Step 3) |
| `gradebook.h` | Edit (Step 4) |
| `main.cpp` | Edit (Steps 5–10) |
| `assignment.*`, `student.*`, `gradebook.cpp`, `statistics.h` | **No change** — keep them open |

When you are finished your project has **thirteen files**.

### How to use these steps

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

### Build it: step by step

#### Step 1 — Write the exception hierarchy

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

#### Step 2 — Make `GradeScale` refuse instead of repair

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

#### Step 3 — Make `Weighted` refuse weights that do not total 100

In `gradingscheme.h`, find the first line:

```cpp
// gradingscheme.h - Grade Calculator v3.1 - Chapter 21
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

#### Step 4 — Let a `Gradebook` be moved (`gradebook.h`)

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
`unique_ptr`, which hands over its scheme. `gradebook.cpp` does not change.

#### Step 5 — Update the header comment and includes in `main.cpp`

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

#### Step 6 — Add `splitCsv` and `saveGradebook`

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

#### Step 7 — Add `loadGradebook`, which builds a replacement first

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

#### Step 8 — Rewrite `chooseScheme` to accept custom weights safely

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

#### Step 9 — Add `editScale`

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

#### Step 10 — Rewrite `main`: load, catch, save

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

### Check your work

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
   back with 90.0%.

Then confirm:

- [ ] The program compiles with no errors and no warnings with all thirteen
      files open.
- [ ] No input you can type makes the program crash or stop unexpectedly.
- [ ] Every `throw` in the program throws a class derived from
      `GradebookError`, and every `catch` catches by **`const` reference**.
- [ ] `gradebook.cpp`, `assignment.*`, `student.*`, and `statistics.h` are
      unchanged from Chapter 23.

### StudySite workflow

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

### Save this checkpoint

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

### Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 24
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
