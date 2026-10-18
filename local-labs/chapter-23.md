# Chapter 23 Lab — Add Generic Statistics and an ID Index

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.3
- **Starting point:** Your committed Chapter 22 v3.2 program (eleven files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

In this lab you put the Standard Template Library to work and write a class
template of your own. By the end you will have:

1. **`Statistics<T>`**, a header-only class template that computes count,
   mean, median, lowest, highest, and standard deviation for any numeric type.
2. An **ID index** — a `std::map<int, std::size_t>` from student ID to roster
   position — that `Gradebook` keeps up to date, and a `findById` member that
   uses it.
3. A **letter-grade distribution** counted with a `std::map<char, int>`.
4. `sortByPercentage` rewritten with a **lambda** that states the ordering
   right where the sort happens.
5. Two new menu options: **Statistics** and **Find by ID**. Quit moves to
   option 8.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `statistics.h` | Create (Step 1) — a header only; there is no `statistics.cpp` |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 2–5) |
| `main.cpp` | Edit (Step 6) |
| All other files | **No change** — keep them open |

When you are finished your project has **twelve files**.

## How to use these steps

This lab is a guided exercise, not a test. Each step tells you **which file**
to open, shows the **exact code to find**, and shows the **exact code to put in
its place**. Work through the steps in order and copy the code from the boxes
rather than retyping it where you can.

- A **find** box shows code exactly as it appears in your program at the end
  of the previous chapter. Use the editor's search to locate it. If you cannot
  find it, your program differs from the previous checkpoint — compare it with
  your last commit on GitHub before going further.
- A **▶ Build checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.

## Build it: step by step

### Step 1 — Write the `Statistics<T>` class template

Create a new file named `statistics.h` and enter this code:

```cpp
// statistics.h - Grade Calculator v3.3 - Chapter 23
#ifndef STATISTICS_H
#define STATISTICS_H

#include <algorithm>
#include <cmath>
#include <vector>

/**
 * Descriptive statistics over any numeric type.
 *
 * Written as a template because the computation does not depend on whether the
 * values are double percentages, int point totals, or float weights. One
 * definition serves them all; the compiler generates a version per type used.
 */
template <typename T>
class Statistics {
public:
    void add(T value) { values_.push_back(value); }

    std::size_t count() const { return values_.size(); }
    bool empty() const { return values_.empty(); }

    T mean() const {
        if (values_.empty()) { return T{}; }
        T sum = T{};
        for (T v : values_) { sum += v; }
        return sum / static_cast<T>(values_.size());
    }

    T median() const {
        if (values_.empty()) { return T{}; }
        std::vector<T> sorted = values_;          // copy: do not disturb the caller
        std::sort(sorted.begin(), sorted.end());
        std::size_t mid = sorted.size() / 2;
        if (sorted.size() % 2 == 1) { return sorted[mid]; }
        return (sorted[mid - 1] + sorted[mid]) / static_cast<T>(2);
    }

    T lowest() const {
        return values_.empty() ? T{} : *std::min_element(values_.begin(), values_.end());
    }

    T highest() const {
        return values_.empty() ? T{} : *std::max_element(values_.begin(), values_.end());
    }

    /** Population standard deviation. Zero for fewer than two values. */
    double standardDeviation() const {
        if (values_.size() < 2) { return 0.0; }
        double m = static_cast<double>(mean());
        double sumSquares = 0.0;
        for (T v : values_) {
            double diff = static_cast<double>(v) - m;
            sumSquares += diff * diff;
        }
        return std::sqrt(sumSquares / static_cast<double>(values_.size()));
    }

private:
    std::vector<T> values_;
};

#endif
```

- `template <typename T>` makes `Statistics` a **blueprint**. When you write
  `Statistics<double>`, the compiler generates a version of the class with
  every `T` replaced by `double`.
- The entire template is in the header. The compiler needs the full
  definition at the point where `Statistics<double>` is used, so a class
  template normally has **no `.cpp` file**.
- `T{}` is a value-initialized `T` — `0.0` for a `double` — and is returned
  when there is no data.
- `median()` **copies** the values before sorting, so asking for the median
  does not rearrange the caller's data.
- `std::min_element` and `std::max_element` from `<algorithm>` return
  iterators; the `*` in front reads the value they point to.

### Step 2 — Declare the new `Gradebook` members (`gradebook.h`)

In `gradebook.h`, find the first line:

```cpp
// gradebook.h - Grade Calculator v3.2 - Chapter 22
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v3.3 - Chapter 23
```

Find the standard-library include:

```cpp
#include <iosfwd>
```

Directly below it, add:

```cpp
#include <map>
```

Find the declaration of `sortByPercentage`:

```cpp
    void sortByPercentage();
```

Directly below it, add:

```cpp

    /** Finds a student by ID in O(log n) using the id index. Null if absent. */
    const Student* findById(int id) const;

    /** How many students earned each letter grade, in scale order. */
    std::map<char, int> letterDistribution() const;

    /** Prints mean, median, range, and standard deviation for the class. */
    void printStatistics(std::ostream& out) const;
```

In the `private:` section, find:

```cpp
    std::vector<Student> roster_;
```

Directly below it, add:

```cpp

    // An index from student ID to roster position. std::map keeps its keys
    // sorted and looks up in logarithmic time, replacing the hand-written
    // binary search of Chapter 17 - and it stays correct as students are added.
    std::map<int, std::size_t> idIndex_;
```

- `findById` returns a **pointer** to the student, or `nullptr` if there is no
  such ID. A pointer can say "nothing found"; a reference cannot.
- `letterDistribution` returns a `std::map<char, int>`: each letter grade
  mapped to how many students earned it.
- `printStatistics` writes to whatever `std::ostream` it is given — the
  screen today, a file tomorrow.
- `idIndex_` maps an ID (the **key**) to the student's position in `roster_`
  (the **value**). A `std::map` keeps its keys sorted and finds a key in
  logarithmic time — the job Chapter 17's binary search did, without needing
  a sorted copy of the roster.

### Step 3 — Keep the index current, and look students up (`gradebook.cpp`)

In `gradebook.cpp`, find the first line:

```cpp
// gradebook.cpp - Grade Calculator v3.2 - Chapter 22
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v3.3 - Chapter 23
```

Find the first includes:

```cpp
#include "gradebook.h"

#include <algorithm>
```

Replace it with:

```cpp
#include "gradebook.h"

#include "statistics.h"

#include <algorithm>
#include <map>
```

Find `addStudent`:

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
}
```

Replace it with:

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
    idIndex_[s.id()] = roster_.size() - 1;
}

const Student* Gradebook::findById(int id) const {
    auto it = idIndex_.find(id);
    if (it == idIndex_.end()) { return nullptr; }
    return &roster_[it->second];
}
```

- In `addStudent`, the new student was just pushed onto the end of the
  roster, so its position is `roster_.size() - 1`. That position is stored in
  the index under the student's ID.
- `idIndex_.find(id)` returns an **iterator**. If it equals `idIndex_.end()`,
  the ID is not in the map. Otherwise `it->second` is the stored position.
  `auto` lets the compiler spell out the long iterator type for you.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile cleanly and behave exactly like v3.2. `letterDistribution` and `printStatistics` are declared but not yet defined; that is allowed as long as nothing calls them, and nothing does yet.

### Step 4 — Count letter grades and compute statistics (`gradebook.cpp`)

Directly below the `findById` function you just added — after this code:

```cpp
    return &roster_[it->second];
}
```

Directly below it, add:

```cpp

std::map<char, int> Gradebook::letterDistribution() const {
    std::map<char, int> counts;
    for (const Student& s : roster_) {
        ++counts[scale_.letterFor(percentageFor(s))];   // missing keys start at 0
    }
    return counts;
}

void Gradebook::printStatistics(std::ostream& out) const {
    if (roster_.empty()) {
        out << "No students, so there are no statistics.\n";
        return;
    }
    Statistics<double> stats;
    for (const Student& s : roster_) { stats.add(percentageFor(s)); }

    out << std::fixed << std::setprecision(1);
    out << "  Students : " << stats.count() << "\n";
    out << "  Mean     : " << stats.mean() << "%\n";
    out << "  Median   : " << stats.median() << "%\n";
    out << "  Range    : " << stats.lowest() << "% to " << stats.highest() << "%\n";
    out << "  Std dev  : " << stats.standardDeviation() << "\n";

    out << "  Grades   : ";
    for (const auto& entry : letterDistribution()) {
        out << entry.first << "=" << entry.second << "  ";
    }
    out << "\n";
}
```

(The first line in the box is blank on purpose: leave one blank line between
`findById` and the new code.)

- `++counts[letter]` is the standard **counting idiom** for a map. If `letter`
  is not in the map yet, `operator[]` inserts it with the value `0`, and `++`
  makes it `1`. Because a `std::map` is sorted by key, the counts come back in
  letter order.
- `printStatistics` fills a `Statistics<double>` with every student's course
  percentage, then prints the results. It uses `percentageFor`, so the
  statistics follow the chosen grading scheme.
- `for (const auto& entry : letterDistribution())` walks the map;
  `entry.first` is the letter and `entry.second` is the count.

### Step 5 — Sort with a lambda, and rebuild the index (`gradebook.cpp`)

In `sortByPercentage`, find:

```cpp
    std::sort(roster_.begin(), roster_.end());   // uses Student::operator<
```

Replace it with:

```cpp
    // A lambda states the ordering right where it is used, instead of relying
    // on operator< to mean "by percentage, descending" everywhere.
    const Gradebook* self = this;
    std::sort(roster_.begin(), roster_.end(),
              [self](const Student& a, const Student& b) {
                  return self->percentageFor(a) > self->percentageFor(b);
              });
    // Sorting moved every student, so the ID index must be rebuilt.
    idIndex_.clear();
    for (std::size_t i = 0; i < roster_.size(); ++i) {
        idIndex_[roster_[i].id()] = i;
    }
```

- The **lambda** `[self](const Student& a, const Student& b) { ... }` is the
  comparison, written right where it is used. You no longer have to go read
  `Student::operator<` to find out what order the sort produces.
- The lambda needs `percentageFor`, a `Gradebook` member, so it **captures** a
  pointer to the gradebook, `self`, by listing it in the square brackets.
- **An index is derived data, and derived data goes stale.** Sorting moves
  every student to a new position, so every position stored in `idIndex_` is
  now wrong. The loop clears the index and rebuilds it from the sorted roster.
  Forget this, and *Find by ID* silently returns the wrong student.

### Step 6 — Add *Statistics* and *Find by ID* to the menu (`main.cpp`)

At the top of `main.cpp`, find these lines of the header comment:

```cpp
//  Grade Calculator  v3.2                                          Chapter 22
// -----------------------------------------------------------------------------
//  Change  : Ownership. The raw GradingScheme* becomes std::unique_ptr.
//            Gradebook loses its destructor, its manual delete, and its
//            deleted copy operations - 8 lines of bookkeeping for 0.
//            Behavior is identical to v3.1; both builds are leak-free.
//  Point   : v3.1 is correct because its author remembered three separate
//            things. v3.2 is correct because there is nothing to remember.
//  Verify  : build both with -fsanitize=address, switch schemes, exit.
//            Neither leaks. Then delete Gradebook::~Gradebook from v3.1 and
//            rerun: v3.1 now leaks, v3.2 cannot be broken the same way.
```

Replace it with:

```cpp
//  Grade Calculator  v3.3                                          Chapter 23
// -----------------------------------------------------------------------------
//  Change  : Templates and the STL. Statistics<T> computes mean, median,
//            range, and standard deviation for any numeric type. std::map
//            indexes students by ID and counts the letter distribution.
//            Sorting is expressed with a lambda instead of operator<.
```

At the start of `main`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.2 (leak-free) ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.3 (statistics) ===\n\n";
```

Find the menu prompt:

```cpp
        std::cout << "\n1) Add student  2) Report  3) Sort  "
                     "4) Custom scale  5) Change scheme  6) Quit\nChoice: ";
```

Replace it with:

```cpp
        std::cout << "\n1) Add student  2) Report  3) Sort  "
                     "4) Custom scale  5) Change scheme\n"
                     "6) Statistics  7) Find by ID  8) Quit\nChoice: ";
```

Near the end of the menu loop, find:

```cpp
        } else if (c == '6') {
            running = false;
        } else {
            std::cout << "  Please enter 1-6.\n";
```

Replace it with:

```cpp
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
            running = false;
        } else {
            std::cout << "  Please enter 1-8.\n";
```

- **Statistics** (option 6) passes `std::cout` to `printStatistics`.
- **Find by ID** (option 7) converts the typed ID with `std::stoi`, catching
  bad input, then asks `book.findById(id)`. Always compare the result with
  `nullptr` before using it — dereferencing a null pointer crashes the
  program.
- **Quit** moves to option 8.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile with no errors and no warnings and show the eight-option menu.

## Check your work

Choose `1` (Points-based). Add three students, each with one assignment
(category: press Enter):

| Student | Assignment | Earned | Possible | Bonus |
|---|---|---|---|---|
| `Ana` | `Test` | 95 | 100 | 0 |
| `Ben` | `Test` | 75 | 100 | 0 |
| `Cy` | `Test` | 55 | 100 | 0 |

1. Choose `6` (Statistics). You should see:

   ```text
   --- Class statistics ---
     Students : 3
     Mean     : 75.0%
     Median   : 75.0%
     Range    : 55.0% to 95.0%
     Std dev  : 16.3
     Grades   : A=1  C=1  F=1
   ```

   Check the standard deviation by hand: the deviations from the mean are
   +20, 0, −20; their squares average 800 ÷ 3 ≈ 266.67; √266.67 ≈ 16.3.
2. Choose `7` and enter `1002`. You should see `Ben: 75.0%`.
3. Choose `7` and enter `99`. You should see `No student with ID 99.`
4. Choose `3` (Sort), then `7` with `1002` again. It must still find `Ben` —
   proof that the index was rebuilt after sorting.
5. Choose `8` (Quit).

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] `statistics.h` has an include guard and there is no `statistics.cpp`.
- [ ] `addStudent` updates `idIndex_`, and `sortByPercentage` rebuilds it.
- [ ] Every use of `findById` checks for `nullptr`.

## Optional local workflow

Build and run this chapter's program with the command for your platform:

**macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):

```bash
clang++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
./gradecalc
```

**Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):

```powershell
g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc.exe
.\gradecalc.exe
```

The ▶ Build checkpoints below use `g++ -std=c++17 -Wall -Wextra *.cpp -o
gradecalc`, which works as written on macOS, Linux, and WSL. On Windows, use
the Windows command above instead.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Work through Steps 1–6 above in your local editor, in order, building and running at each ▶ Build checkpoint.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 23 Grade Calculator v3.3"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 23 checkpoint.
- The commit is pushed to GitHub.
