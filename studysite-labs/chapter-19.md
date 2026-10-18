# Chapter 19 Lab — Split Classes into Files

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.6
- **Starting point:** Your committed Chapter 18 v2.5 program (`main.cpp`).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

In Chapter 18 all three classes lived in `main.cpp`. In this lab you give each
class its own **header** (`.h`) and **implementation** (`.cpp`) file, add a
`Gradebook` class, and teach every class to print itself with
**`operator<<`**. By the end you will have:

1. `assignment.h`/`.cpp`, `gradescale.h`/`.cpp`, and `student.h`/`.cpp` —
   the Chapter 18 classes, split into declaration and definition, each header
   protected by an **include guard**.
2. An `operator<<` for `Assignment`, `GradeScale`, and `Student`, written
   using only each class's public accessors — no `friend` needed.
3. `Student::operator<`, which orders students by percentage, highest first.
4. A new `Gradebook` class (`gradebook.h`/`.cpp`) that owns the course name,
   the roster, the grade scale, and the next-ID counter, and prints a whole
   class report with a single `operator<<`.
5. A short `main.cpp` with five menu options: **Add student**, **Report**,
   **Sort by grade** (new), **Custom scale**, and **Quit**.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `assignment.h`, `assignment.cpp` | Create (Step 1) |
| `gradescale.h`, `gradescale.cpp` | Create (Step 2) |
| `student.h`, `student.cpp` | Create (Step 3) |
| `gradebook.h`, `gradebook.cpp` | Create (Step 4) |
| `main.cpp` | Edit (Steps 5–7) |

When you are finished your project has **nine files**. Every one of them must
be open in the StudySite editor when you click **Run** — a `.cpp` file that is
not open is not compiled, and the linker error you get names the missing
function, not the missing tab.

> **How to create a file:** in the StudySite editor, create a new file with
> the exact name shown (spelling and lowercase matter, because `#include`
> lines refer to these names). Keep each new file open after you create it.

## How to use these steps

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

> **Heads-up:** Steps 1–4 create the new files; Steps 5–7 remove the old
> class code from `main.cpp`. Do **not** click Run until the checkpoint at the
> end of Step 7 — until then, the classes exist in two places at once.

## Build it: step by step

### Step 1 — Create `assignment.h` and `assignment.cpp`

A **header** declares what a class looks like; its **implementation file**
defines the function bodies. Other files `#include` the header, never the
`.cpp`.

Create a new file named `assignment.h` and enter this code:

```cpp
// assignment.h - Grade Calculator v2.6 - Chapter 19
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

Notice:

- `#ifndef ASSIGNMENT_H` / `#define ASSIGNMENT_H` / `#endif` is an **include
  guard**. If two files both include `assignment.h`, the class is still
  defined only once.
- Short accessors stay in the header. `totalEarned()` and `ratio()` are now
  only **declared** here (they end in `;`); their bodies move to the `.cpp`.
- The header includes `<iosfwd>`, not `<iostream>`. `<iosfwd>` only
  *announces* that `std::ostream` exists, which is all a declaration like
  `operator<<(std::ostream&, ...)` needs. Files that include this header
  compile faster and do not drag in all of `<iostream>`.
- `operator<<` is declared **outside** the class. It is a free function that
  uses the class's public accessors.

Create a new file named `assignment.cpp` and enter this code:

```cpp
// assignment.cpp - Grade Calculator v2.6 - Chapter 19
#include "assignment.h"

#include <iomanip>
#include <ostream>

Assignment::Assignment(const std::string& name, double earned, double possible, double bonus)
    : name_(name), pointsEarned_(earned), pointsPossible_(possible), bonusPoints_(bonus) {}

double Assignment::totalEarned() const {
    return pointsEarned_ + bonusPoints_;
}

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

Each definition outside the class is written with the class name and the
**scope resolution operator**: `Assignment::totalEarned()`. The constructor's
default argument (`bonus = 0.0`) appears only in the header, never again here.

`operator<<` prints an assignment as one aligned line — name, total earned,
and points possible, plus a bonus note when there is one — and **returns the
stream**, which is what lets you chain `<<` calls.

### Step 2 — Create `gradescale.h` and `gradescale.cpp`

Create a new file named `gradescale.h` and enter this code:

```cpp
// gradescale.h - Grade Calculator v2.6 - Chapter 19
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

Create a new file named `gradescale.cpp` and enter this code:

```cpp
// gradescale.cpp - Grade Calculator v2.6 - Chapter 19
#include "gradescale.h"

#include <iomanip>
#include <ostream>

GradeScale::GradeScale() {
    tiers_ = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };
}

GradeScale::GradeScale(const std::vector<Tier>& requested) {
    for (const Tier& t : requested) {
        if (t.cutoff < 0.0) { continue; }
        if (!tiers_.empty() && t.cutoff >= tiers_.back().cutoff) { continue; }
        tiers_.push_back(t);
    }
    if (tiers_.empty() || tiers_.back().cutoff > 0.0) {
        tiers_.push_back({0.0, 'F'});
    }
}

char GradeScale::letterFor(double percentage) const {
    for (const Tier& t : tiers_) {
        if (percentage >= t.cutoff) { return t.letter; }
    }
    return tiers_.back().letter;
}

std::ostream& operator<<(std::ostream& out, const GradeScale& scale) {
    out << "Scale: ";
    for (const GradeScale::Tier& t : scale.tiers()) {
        out << t.letter << " >= " << std::fixed << std::setprecision(0)
            << t.cutoff << "   ";
    }
    return out;
}
```

Two changes from Chapter 18 besides the split:

- The invariant now lives in a **comment above the class**, where anyone
  reading the header will see it. The constructor logic that enforces it is
  unchanged.
- Chapter 18's `describe()` member is gone. **`operator<<` replaces it**, so
  printing a scale is `std::cout << scale` — the same way you print anything
  else. Unlike `describe()`, it does not add `"  "` in front or a newline at the
  end; the caller decides the layout.

### Step 3 — Create `student.h` and `student.cpp`

Create a new file named `student.h` and enter this code:

```cpp
// student.h - Grade Calculator v2.6 - Chapter 19
#ifndef STUDENT_H
#define STUDENT_H

#include "assignment.h"

#include <iosfwd>
#include <string>
#include <vector>

class Student {
public:
    Student() = default;
    Student(const std::string& name, int id);

    const std::string& name() const { return name_; }
    int id() const { return id_; }
    const std::vector<Assignment>& assignments() const { return assignments_; }

    void addAssignment(const Assignment& a);

    double totalEarned() const;
    double totalPossible() const;
    double percentage() const;

    /** Orders students by percentage, highest first. Enables sorting. */
    bool operator<(const Student& other) const;

private:
    std::string name_;
    int id_ = 0;
    std::vector<Assignment> assignments_;
};

std::ostream& operator<<(std::ostream& out, const Student& s);

#endif
```

Create a new file named `student.cpp` and enter this code:

```cpp
// student.cpp - Grade Calculator v2.6 - Chapter 19
#include "student.h"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <ostream>

namespace {
    const bool CAP_AT_100 = true;
}

Student::Student(const std::string& name, int id) : name_(name), id_(id) {}

void Student::addAssignment(const Assignment& a) {
    assignments_.push_back(a);
}

double Student::totalEarned() const {
    double sum = 0.0;
    for (const Assignment& a : assignments_) { sum += a.totalEarned(); }
    return sum;
}

double Student::totalPossible() const {
    double sum = 0.0;
    for (const Assignment& a : assignments_) { sum += a.pointsPossible(); }
    return sum;
}

double Student::percentage() const {
    double possible = totalPossible();
    if (possible <= 0.0) { return 0.0; }
    double raw = totalEarned() / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

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

Notice:

- `student.h` includes `"assignment.h"` — a `Student` holds a
  `std::vector<Assignment>`, so the compiler must see the full `Assignment`
  class first.
- `CAP_AT_100` moved out of `main.cpp` and into an **unnamed namespace** in
  `student.cpp`, the only file that uses it. An unnamed namespace makes the
  name private to that one file.
- **`operator<`** is a member function. It answers "does this student come
  before `other`?" and it means *higher percentage first* — not ordinary
  numeric less-than. That is the convenience and the risk of overloading an
  operator; Chapter 23 revisits it.
- `operator<<` prints ID, name, and percentage. It leaves out the letter
  grade, because a `Student` does not know which scale is in use.

### Step 4 — Create the `Gradebook` class

In Chapter 18, `main` held a scale, a roster, and a next-ID counter as three
separate variables. A `Gradebook` class gathers them into one object that
guards them.

Create a new file named `gradebook.h` and enter this code:

```cpp
// gradebook.h - Grade Calculator v2.6 - Chapter 19
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
    explicit Gradebook(const std::string& courseName = "Untitled Course");

    void addStudent(const Student& s);
    void setScale(const GradeScale& scale) { scale_ = scale; }

    const GradeScale& scale() const { return scale_; }
    const std::string& courseName() const { return courseName_; }
    std::size_t size() const { return roster_.size(); }
    bool empty() const { return roster_.empty(); }

    /** Retrieves a student by position. Precondition: index < size(). */
    const Student& operator[](std::size_t index) const { return roster_[index]; }

    int nextId() const { return nextId_; }
    int claimNextId() { return nextId_++; }

    double classAverage() const;
    void sortByPercentage();

private:
    std::string courseName_;
    std::vector<Student> roster_;
    GradeScale scale_;
    int nextId_ = 1001;
};

std::ostream& operator<<(std::ostream& out, const Gradebook& book);

#endif
```

- All the data is `private`. The roster can change only through
  `addStudent` and `sortByPercentage`, so those are the only two places that
  could ever corrupt it.
- `operator[]` returns a `const Student&` for a position. Its comment states
  the **precondition** (`index < size()`); it does not check.
- `claimNextId()` returns the next ID and advances the counter in one call,
  so an ID can never be handed out twice.

Create a new file named `gradebook.cpp` and enter this code:

```cpp
// gradebook.cpp - Grade Calculator v2.6 - Chapter 19
#include "gradebook.h"

#include <algorithm>
#include <iomanip>
#include <ostream>

Gradebook::Gradebook(const std::string& courseName) : courseName_(courseName) {}

void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
}

double Gradebook::classAverage() const {
    if (roster_.empty()) { return 0.0; }
    double sum = 0.0;
    for (const Student& s : roster_) { sum += s.percentage(); }
    return sum / static_cast<double>(roster_.size());
}

void Gradebook::sortByPercentage() {
    std::sort(roster_.begin(), roster_.end());   // uses Student::operator<
}

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

- `sortByPercentage()` is one line: `std::sort` puts the roster in order
  using `Student::operator<`, so it sorts highest percentage first.
- `operator<<` for `Gradebook` prints the whole report. It prints the course
  name, then the scale **using the scale's own `<<`**, then each student
  **using the student's own `<<`**, followed by the letter grade, and finally
  a class average. Each class knows how to print itself, and nothing knows how
  to print anything else.

### Step 5 — Update the header comment in `main.cpp`

Now switch to `main.cpp`. From here on, `main.cpp` only runs the menu.

At the top of `main.cpp`, find the header comment:

```cpp
// =============================================================================
//  Grade Calculator  v2.5                                          Chapter 18
// -----------------------------------------------------------------------------
//  Change  : Structs become classes with private data and behavior.
//            GradeScale validates its own tiers in the constructor, so an
//            invalid scale can no longer be constructed at all. The loose
//            validation functions of Chapter 11 are gone.
//            Each Student now owns its own Assignment records.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
// =============================================================================
```

Replace it with:

```cpp
// =============================================================================
//  Grade Calculator  v2.6                                          Chapter 19
// -----------------------------------------------------------------------------
//  Change  : One header/implementation pair per class. Reports print through
//            operator<<, so a whole Gradebook is written with a single <<.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

The new `Build` line lists all five `.cpp` files — every one must be compiled
and linked together.

### Step 6 — Remove the classes from `main.cpp`

The classes now live in their own files, so `main.cpp` must stop defining
them. It includes `gradebook.h` instead, which in turn includes the other
headers.

Just below the header comment, find the first `#include` line:

```cpp
#include <algorithm>
```

Delete that line and everything below it (the remaining `#include` lines, `CAP_AT_100`, all three classes, and the *Input helpers* banner), stopping just **above** this line, which you keep:

```cpp
double readNonNegative(const std::string& prompt) {
```

In the space where that code was, enter:

```cpp
#include "gradebook.h"

#include <iostream>
#include <limits>
#include <string>
```

Afterward, `main.cpp` should begin with the header comment, then these four
`#include` lines, then `readNonNegative`.

*Why:* a class must be defined exactly once in the whole program. If
`main.cpp` kept its own copy, the program would have two definitions of each
class. Quoted includes (`"gradebook.h"`) name your own files; angle-bracket
includes (`<iostream>`) name the standard library.

### Step 7 — Rewrite `main` to use a `Gradebook`

Find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it, all the way to the final closing `}` at the very end of the file.

In its place, enter the new `main`:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v2.6 (one class per file) ===\n";

    Gradebook book("Programming Fundamentals");
    bool running = true;

    while (running) {
        std::cout << "\n1) Add student  2) Report  3) Sort by grade  "
                     "4) Custom scale  5) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char choice = line.empty() ? '?' : line[0];

        if (choice == '1') {
            std::string name = readLine("  Student name: ");
            if (name.empty()) { continue; }
            Student s(name, book.claimNextId());
            while (true) {
                std::string an = readLine("    Assignment name (or 'done'): ");
                if (an == "done" || an.empty()) { break; }
                double earned   = readNonNegative("      Points earned  : ");
                double possible = readNonNegative("      Points possible: ");
                double bonus    = readNonNegative("      Bonus points   : ");
                s.addAssignment(Assignment(an, earned, possible, bonus));
            }
            book.addStudent(s);
            std::cout << "  Added " << s.name() << " as ID " << s.id() << ".\n";

        } else if (choice == '2') {
            std::cout << book << "\n";       // one operator<< prints everything

        } else if (choice == '3') {
            book.sortByPercentage();
            std::cout << "  Sorted, highest first.\n";

        } else if (choice == '4') {
            std::vector<GradeScale::Tier> requested;
            std::cout << "  Enter tiers highest first, 'done' to finish.\n";
            while (true) {
                std::string letterText = readLine("    Letter (or 'done'): ");
                if (letterText == "done" || letterText.empty()) { break; }
                double cutoff = readNonNegative("      Minimum percentage: ");
                requested.push_back({cutoff, letterText[0]});
            }
            book.setScale(GradeScale(requested));
            std::cout << "  " << book.scale() << "\n";

        } else if (choice == '5') {
            running = false;
        } else {
            std::cout << "  Please enter 1-5.\n";
        }
    }
    std::cout << "\nGoodbye.\n";
    return 0;
}
```

What changed:

- `Gradebook book("Programming Fundamentals");` replaces the three loose
  variables from Chapter 18.
- **Add student** gets its ID from `book.claimNextId()` and stores the student
  with `book.addStudent(s)`.
- **Report** is now one line: `std::cout << book << "\n";`.
- **Sort by grade** (new, option 3) calls `book.sortByPercentage()`.
- **Custom scale** (now option 4) builds the scale exactly as before and hands
  it to `book.setScale(...)`, then prints it with `<<`.
- **Quit** moves to option 5.

> **▶ Run checkpoint:** Make sure all nine files are open in the editor, then click **Run**. The program should compile with no errors and no warnings and show the v2.6 banner and the five-option menu. An `undefined reference` error means a `.cpp` file is not open or a function name is misspelled; a `redefinition` error means a class is still defined in `main.cpp`.

## Check your work

Run the program and type the inputs below in the Terminal.

1. Choose `1`. Add `Zoe` with one assignment: `HW1`, earned `5`, possible
   `10`, bonus `0`. Type `done`.
2. Choose `1`. Add `Ada` with one assignment: `HW1`, earned `9`, possible
   `10`, bonus `1`. Type `done`.
3. Choose `2` (Report). You should see:

   ```text
   =====================================
     Programming Fundamentals
     Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0
   =====================================
   1001  Zoe                     50.0%   F
   1002  Ada                    100.0%   A
   -------------------------------------
   CLASS AVERAGE                 75.0%
   ```

4. Choose `3` (Sort by grade). The program prints `Sorted, highest first.`
5. Choose `2` again. Ada (1002) is now listed first, Zoe second, and the class
   average is still 75.0%.
6. Choose `5` (Quit). The program prints `Goodbye.`

Then confirm:

- [ ] All nine files are in the project, and the program compiles with no
      errors and no warnings.
- [ ] Every header starts with an include guard (`#ifndef` / `#define`) and
      ends with `#endif`.
- [ ] `main.cpp` no longer contains `class Assignment`, `class GradeScale`,
      `class Student`, or `CAP_AT_100`.
- [ ] The report is printed by `std::cout << book`, and no `operator<<` uses
      `friend`.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click `main.cpp` to open it. You will create the eight new files in the editor during the lab.
   Confirm the editor shows the expected file paths before editing.
4. Work through Steps 1–7 above in StudySite's internal editor, in order. Keep every file open, and click **Run** at the ▶ Run checkpoint at the end of Step 7.
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
> clang++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradebook.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradebook.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — all nine files: `main.cpp` plus the four `.h` and four `.cpp` files you created. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 19 Grade Calculator v2.6**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 19
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
