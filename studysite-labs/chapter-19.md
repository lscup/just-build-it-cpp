# Chapter 19 Lab — Split Classes into Files

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.6
- **Starting point:** The working Chapter 18 v2.5 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create one header and one implementation file for each class (`Assignment`, `GradeScale`, `Student`, `Gradebook`); keep `main.cpp` focused on application flow.
2. Add include guards, and keep implementation details out of headers — use `<iosfwd>` for a forward declaration instead of a full `#include` wherever only a reference or pointer is needed.
3. Create a `Gradebook` class that owns the roster, the grade scale, the course name, and the next-ID counter, replacing the loose `scale`/`roster`/`nextId` variables `main` held directly in Chapter 18.
4. Implement `operator<<` for `Assignment`, `GradeScale`, `Student`, and `Gradebook`, each using only that class's own public accessors — no `friend` anywhere.
5. Add checked `Gradebook::at(index)` alongside the existing unchecked `operator[]`. `at` must throw `std::out_of_range` for an invalid index — delegate to `std::vector::at`, which already does this, rather than writing the check by hand.
6. Give `Student` an `operator<` that orders by percentage, highest first, and use it to implement `Gradebook::sortByPercentage()` with `std::sort`.
7. Carry the Chapter 15–18 features forward onto `Gradebook`: saving and loading, the `runTests()` regression suite, and the Chapter 17 sort/search all still need to work as `Gradebook` member functions — do not drop them while splitting files.

Item 7 is the one most worth double-checking, for the same reason it was in Chapter 18: it is easy, while carving `main`'s logic into a new `Gradebook` class, to carry forward only the features the chapter narrative shows in its example and quietly lose the rest.

## What changes from Chapter 18

- **`Gradebook` replaces three loose variables.** Chapter 18's `main` held a `GradeScale scale`, a `std::vector<Student> roster`, and an `int nextId` side by side and passed them to free functions. Chapter 19 wraps all three (plus a course name) in one `Gradebook` class, so `main` now holds a single `Gradebook book` and calls its member functions.
- **Two sorting mechanisms now coexist, deliberately.** `Gradebook::sortByPercentage()` is new: it uses `std::sort` with `Student::operator<`, this chapter's operator-overloading lesson. `Gradebook::sortRoster(SortKey)` is the Chapter 17 selection sort carried forward unchanged in algorithm, generalized to a `Gradebook` member and given a three-way `SortKey` enum (`Name`, `Percentage`, `Id`) so it can still sort by ID — which `binaryFindById` needs — and by name, neither of which `operator<` provides. **These are not redundant**: one teaches operator overloading, the other keeps the algorithm-comparison lesson (linear vs. binary search, with comparison counts) from Chapter 17 intact.
- **Checked access is new.** `Gradebook::at(std::size_t)` did not exist before this chapter. It is a one-line delegation to `std::vector::at`, which already throws `std::out_of_range` for a bad index — there is nothing to hand-write.
- **The save file gains a `COURSE` line**, since `Gradebook` now has a course name that did not exist as a saved field before.
- **The regression suite grows to nine checks.** The eight Chapter 16–18 checks (D1–D3, plus the zero-points boundary check) are unchanged. A ninth check is added for the new checked-access requirement: constructing an empty `Gradebook` and confirming `at(0)` throws `std::out_of_range`.

Everything else genuinely carries over: the grading math, the CSV record shapes for `TIER` and `STUDENT` rows, and the D1–D3 defects' pass/fail wording are all unchanged from Chapter 18.

## Build it: step by step

### Step 1 — Split `Assignment`, `GradeScale`, and `Student` into header/implementation pairs

Each class keeps exactly the members and behavior it had in Chapter 18. Only the file layout changes: declarations go in a header behind an include guard, definitions go in a matching `.cpp`. `Assignment`:

```cpp
// assignment.h
#ifndef ASSIGNMENT_H
#define ASSIGNMENT_H

#include <iosfwd>
#include <string>

/** One graded item belonging to one student. */
class Assignment {
public:
    Assignment() = default;
    Assignment(const std::string& name, double earned, double possible, double bonus = 0.0);

    const std::string& name() const { return name_; }
    double pointsEarned() const     { return pointsEarned_; }
    double pointsPossible() const   { return pointsPossible_; }
    double bonusPoints() const      { return bonusPoints_; }

    double totalEarned() const;
    double ratio() const;

private:
    std::string name_;
    double pointsEarned_   = 0.0;
    double pointsPossible_ = 0.0;
    double bonusPoints_    = 0.0;
};

std::ostream& operator<<(std::ostream& out, const Assignment& a);

#endif
```

```cpp
// assignment.cpp
#include "assignment.h"

#include <iomanip>
#include <ostream>

Assignment::Assignment(const std::string& name, double earned, double possible, double bonus)
    : name_(name), pointsEarned_(earned), pointsPossible_(possible), bonusPoints_(bonus) {}

double Assignment::totalEarned() const { return pointsEarned_ + bonusPoints_; }

double Assignment::ratio() const {
    return pointsPossible_ > 0.0 ? totalEarned() / pointsPossible_ : 0.0;
}

std::ostream& operator<<(std::ostream& out, const Assignment& a) {
    out << std::fixed << std::setprecision(1)
        << std::left << std::setw(18) << a.name()
        << std::right << std::setw(7) << a.totalEarned()
        << " / " << std::setw(6) << a.pointsPossible();
    if (a.bonusPoints() > 0.0) {
        out << "  (+" << a.bonusPoints() << " bonus)";
    }
    return out;
}
```

`GradeScale` and `Student` split the same way — declarations in the header, bodies in the `.cpp`, `<iosfwd>` in the header wherever a full `<string>`/`<vector>` include is not actually needed there. `GradeScale::letterFor` keeps the exact behavior it had at the end of Chapter 18: a negative percentage returns `'?'` rather than guessing, which the D1 regression test below still checks.

### Step 2 — Add `operator<<` for each class, and `operator<` for `Student`

Each `operator<<` uses only its class's public accessors:

```cpp
// gradescale.cpp (excerpt)
std::ostream& operator<<(std::ostream& out, const GradeScale& scale) {
    out << "Scale: ";
    for (const GradeScale::Tier& t : scale.tiers()) {
        out << t.letter << " >= " << std::fixed << std::setprecision(0)
            << t.cutoff << "   ";
    }
    return out;
}
```

```cpp
// student.cpp (excerpt)
bool Student::operator<(const Student& other) const {
    return percentage() > other.percentage();   // highest first
}

std::ostream& operator<<(std::ostream& out, const Student& s) {
    out << std::fixed << std::setprecision(1)
        << std::left << std::setw(6) << s.id()
        << std::setw(20) << s.name()
        << std::right << std::setw(8) << s.percentage() << "%";
    return out;
}
```

`Student::operator<` means "higher percentage first," not numeric less-than — worth remembering when `Gradebook::sortByPercentage()` calls `std::sort` on it in Step 3.

### Step 3 — Create the `Gradebook` class

```cpp
// gradebook.h
#ifndef GRADEBOOK_H
#define GRADEBOOK_H

#include "gradescale.h"
#include "student.h"

#include <iosfwd>
#include <string>
#include <vector>

/** Owns the roster and the grading scale, and produces reports. */
class Gradebook {
public:
    /** Sort key for sortRoster(). */
    enum class SortKey { Name, Percentage, Id };

    explicit Gradebook(const std::string& courseName = "Untitled Course");

    void addStudent(const Student& s);
    void setScale(const GradeScale& scale) { scale_ = scale; }

    const GradeScale& scale() const { return scale_; }
    const std::string& courseName() const { return courseName_; }
    std::size_t size() const { return roster_.size(); }
    bool empty() const { return roster_.empty(); }

    /** Unchecked access. Precondition: index < size(). */
    const Student& operator[](std::size_t index) const { return roster_[index]; }

    /** Checked access: throws std::out_of_range for an invalid index. */
    const Student& at(std::size_t index) const { return roster_.at(index); }

    int nextId() const { return nextId_; }
    int claimNextId() { return nextId_++; }

    double classAverage() const;
    void sortByPercentage();

    void sortRoster(SortKey key);
    int linearFindById(int id, int& comparisons) const;
    int binaryFindById(int id, int& comparisons) const;

    bool save(const std::string& filename) const;
    bool load(const std::string& filename, std::string& message);

private:
    std::string courseName_;
    std::vector<Student> roster_;
    GradeScale scale_;
    int nextId_ = 1001;
};

std::ostream& operator<<(std::ostream& out, const Gradebook& book);

#endif
```

`at` is one line, because `std::vector::at` already does exactly what the requirement asks:

```cpp
const Student& at(std::size_t index) const { return roster_.at(index); }
```

### Step 4 — Implement `Gradebook::operator<<`: the whole report, one operator

```cpp
std::ostream& operator<<(std::ostream& out, const Gradebook& book) {
    out << "\n=====================================\n";
    out << "  " << book.courseName() << "\n";
    out << "  " << book.scale() << "\n";
    out << "=====================================\n";

    if (book.empty()) {
        out << "No students on the roster.\n";
        return out;
    }
    for (std::size_t i = 0; i < book.size(); ++i) {
        const Student& s = book[i];
        out << s << "   " << book.scale().letterFor(s.percentage()) << "\n";
    }
    out << "-------------------------------------\n";
    out << std::fixed << std::setprecision(1)
        << std::left << std::setw(26) << "CLASS AVERAGE"
        << std::right << std::setw(8) << book.classAverage() << "%\n";
    return out;
}
```

Notice the nesting: `Gradebook`'s `operator<<` calls `Student`'s, which calls `GradeScale`'s indirectly through `letterFor`. Each class prints itself; nothing prints anything else's internals.

### Step 5 — Carry Chapter 15's persistence onto `Gradebook`

Same CSV shape as Chapter 18, with one addition: a `COURSE` line, since `Gradebook` now has a name to save.

```cpp
bool Gradebook::save(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out) { return false; }

    out << "# Grade Calculator gradebook file, version 2 (Chapter 19)\n";
    out << "# Section tags allow new record types to be added later.\n";
    out << "COURSE," << courseName_ << "\n";
    out << "NEXTID," << nextId_ << "\n";
    for (const GradeScale::Tier& t : scale_.tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (const Student& s : roster_) {
        out << "STUDENT," << s.id() << "," << s.name();
        for (const Assignment& a : s.assignments()) {
            out << "," << a.name() << "," << a.pointsEarned() << ","
                << a.pointsPossible() << "," << a.bonusPoints();
        }
        out << "\n";
    }
    return out.good();
}
```

`load` mirrors it: read each tagged line, fall back to `Untitled Course`/the default scale when a `COURSE`/`TIER` line is missing, and rebuild `roster_` from the `STUDENT` rows exactly as Chapter 18 did — see `gradebook.cpp` for the full loop. Because `roster_`, `scale_`, `courseName_`, and `nextId_` are all private, `save` and `load` have to be `Gradebook` member functions; there is no way to write them as free functions anymore.

### Step 6 — Carry Chapter 17's sort/search onto `Gradebook`

The selection sort algorithm is unchanged; it now compares `roster_` elements through `Student`'s accessors and lives inside `Gradebook`:

```cpp
void Gradebook::sortRoster(SortKey key) {
    for (std::size_t i = 0; i + 1 < roster_.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < roster_.size(); ++j) {
            bool jComesFirst = false;
            switch (key) {
                case SortKey::Name:       jComesFirst = roster_[j].name() < roster_[best].name(); break;
                case SortKey::Percentage: jComesFirst = roster_[j].percentage() > roster_[best].percentage(); break;
                case SortKey::Id:         jComesFirst = roster_[j].id() < roster_[best].id(); break;
            }
            if (jComesFirst) { best = j; }
        }
        if (best != i) { std::swap(roster_[i], roster_[best]); }
    }
}

int Gradebook::linearFindById(int id, int& comparisons) const {
    comparisons = 0;
    for (std::size_t i = 0; i < roster_.size(); ++i) {
        ++comparisons;
        if (roster_[i].id() == id) { return static_cast<int>(i); }
    }
    return -1;
}

/** Binary search needs sorted data, so it sorts a copy first, never roster_. */
int Gradebook::binaryFindById(int id, int& comparisons) const {
    comparisons = 0;
    std::vector<Student> sorted = roster_;
    for (std::size_t i = 0; i + 1 < sorted.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < sorted.size(); ++j) {
            if (sorted[j].id() < sorted[best].id()) { best = j; }
        }
        if (best != i) { std::swap(sorted[i], sorted[best]); }
    }
    int low = 0;
    int high = static_cast<int>(sorted.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        ++comparisons;
        if (sorted[mid].id() == id)      { return mid; }
        else if (sorted[mid].id() < id)  { low = mid + 1; }
        else                             { high = mid - 1; }
    }
    return -1;
}
```

### Step 7 — Rebuild `main`

`main` now holds one `Gradebook`, loads it on startup, and saves it on exit:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v2.6 (one class per file) ===\n\n";

    Gradebook book("Programming Fundamentals");
    std::string message;
    if (book.load(DEFAULT_FILE, message)) {
        std::cout << message << "\n";
    } else {
        std::cout << message << " Starting a new gradebook.\n";
    }
    std::cout << "  " << book.scale() << "\n";
```

The menu carries every Chapter 18 option forward and adds nothing new to the list itself — **Sort by grade** and **Custom scale** were already in Chapter 18's own menu — but restores **Save**, **Run tests**, **Sort roster**, and **Find by ID**, which the unrestored starting code was missing entirely:

```cpp
    std::cout << "\n1) Add student  2) Report  3) Sort by grade  4) Custom scale  5) Save\n"
                 "6) Run tests  7) Sort roster  8) Find by ID  9) Quit\nChoice: ";
```

**Find by ID** now goes through the checked `at()` from Step 3 to retrieve the found student, giving that new member function an actual caller instead of leaving it unused:

```cpp
if (found >= 0) {
    const Student& s = book.at(static_cast<std::size_t>(found));
    std::cout << "  Found: " << s.name() << " (" << s.percentage() << "%)\n";
} else {
    std::cout << "  No student with ID " << id << ".\n";
}
```

The regression suite gains its ninth check, exercising `at` directly against an empty `Gradebook`:

```cpp
Gradebook emptyBook;
bool threw = false;
try {
    emptyBook.at(0);
} catch (const std::out_of_range&) {
    threw = true;
}
check(threw, "Chapter 19 at(0) on an empty Gradebook throws out_of_range");
```

## Verification

- Every source file (`main.cpp`, `assignment.cpp`, `gradescale.cpp`, `student.cpp`, `gradebook.cpp`) builds together as one program.
- Writing a `Gradebook` to the Terminal and writing one to a file both go through the same `operator<<` — there is only one printing routine to get right.
- `book.at(book.size())` (or any out-of-range index) throws `std::out_of_range` instead of returning garbage; `Run tests` confirms this automatically and should report **9 of 9 checks passed**.
- Saving, quitting, and relaunching reloads the course name, roster, and scale unchanged.
- `Sort by grade` (via `operator<`) and `Sort roster` (via the Chapter 17 selection sort) both still work, as does `Find by ID` with its linear-vs-binary comparison counts.
- All accessors that do not change an object are `const`.


## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click each source,
   header, or documentation file needed for this chapter. Confirm the editor
   shows the expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. For a
   multi-file program, keep every source and header file needed by the build
   open in the editor.
5. Click **Run**. Read compiler messages and program output in the embedded
   Terminal, and type program input there when prompted.
6. Fix every compiler error and warning, then complete the verification
   list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor. **Save to GitHub includes every open editor file**, so close
   scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 19 Grade Calculator v2.6**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 19
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
