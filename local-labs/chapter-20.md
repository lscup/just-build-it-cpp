# Chapter 20 Lab — Add Weighted Grading with Inheritance

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.0
- **Starting point:** Your committed Chapter 19 v2.6 program (nine files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

The Grade Calculator has always graded by points: total earned ÷ total
possible. In this lab you add a second rule — **weighted categories** — using
**inheritance**. By the end you will have:

1. A **category** on every `Assignment` (for example `Exam` or `Homework`),
   added in a way that leaves every existing call compiling unchanged.
2. A base class `GradingScheme` holding the behavior every scheme shares (a
   name, and the cap-and-round policy), and two **derived classes**:
   `PointsBased` and `Weighted`.
3. A `Gradebook` that grades each student with whichever scheme was chosen at
   startup, and shows the scheme in the report.
4. A startup question in `main` that picks the scheme for the session, an
   optional step to enter your own category weights, and a *Category* prompt
   for each assignment.

The menu keeps the same five options as Chapter 19.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `assignment.h`, `assignment.cpp` | Edit (Step 1) |
| `gradingscheme.h`, `gradingscheme.cpp` | Create (Steps 2–3) |
| `student.h` | Edit — comments only (Step 4) |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 5–6) |
| `main.cpp` | Edit (Steps 7–8) |
| `gradescale.h`, `gradescale.cpp`, `student.cpp` | No change — keep them open |

When you are finished your project has **eleven files**.

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

### Step 1 — Give `Assignment` a category

Weighted grading needs to know which category each assignment belongs to. Add
a `category` to `Assignment`, with a **default value** so that every existing
call to the constructor still compiles without being edited.

The first line of every class file records the version in which that file last changed. In `assignment.h`, update it. Find:

```cpp
// assignment.h - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// assignment.h - Grade Calculator v3.0 - Chapter 20
```

In `assignment.h`, find the constructor declaration:

```cpp
    Assignment(const std::string& name, double earned, double possible, double bonus = 0.0);
```

Replace it with:

```cpp
    Assignment(const std::string& name, double earned, double possible,
               double bonus = 0.0, const std::string& category = "Uncategorized");
```

Still in `assignment.h`, find the `bonusPoints()` accessor:

```cpp
    double bonusPoints() const      { return bonusPoints_; }
```

Directly below it, add:

```cpp
    const std::string& category() const { return category_; }
```

Near the bottom of the class, find the last data member:

```cpp
    double bonusPoints_    = 0.0;
```

Directly below it, add:

```cpp
    std::string category_  = "Uncategorized";
```

In `assignment.cpp`, update the first line. Find:

```cpp
// assignment.cpp - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// assignment.cpp - Grade Calculator v3.0 - Chapter 20
```

In `assignment.cpp`, find the constructor definition:

```cpp
Assignment::Assignment(const std::string& name, double earned, double possible, double bonus)
    : name_(name), pointsEarned_(earned), pointsPossible_(possible), bonusPoints_(bonus) {}
```

Replace it with:

```cpp
Assignment::Assignment(const std::string& name, double earned, double possible,
                       double bonus, const std::string& category)
    : name_(name), pointsEarned_(earned), pointsPossible_(possible),
      bonusPoints_(bonus), category_(category) {}
```

Still in `assignment.cpp`, near the end of `operator<<`, find:

```cpp
        out << "  (+" << a.bonusPoints() << " bonus)";
    }
```

Directly below it, add:

```cpp
    out << "  [" << a.category() << "]";
```

*Why:* adding a parameter **with a default** at the end of a parameter list
extends a function without breaking any caller — the Chapter 10 technique.
`Assignment("HW1", 9, 10)` still compiles and simply gets the category
`"Uncategorized"`. The default value appears only in the header declaration.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile cleanly and behave exactly like v2.6. Nothing uses the category yet.

### Step 2 — Create the `GradingScheme` hierarchy (`gradingscheme.h`)

A **base class** holds what every grading scheme has in common. Each **derived
class** adds its own rule.

Create a new file named `gradingscheme.h` and enter this code:

```cpp
// gradingscheme.h - Grade Calculator v3.0 - Chapter 20
#ifndef GRADINGSCHEME_H
#define GRADINGSCHEME_H

#include "assignment.h"

#include <string>
#include <vector>

/**
 * Base class for grading schemes.
 *
 * Chapter 20 compares two designs for supporting more than one grading rule:
 * a scheme flag branched on inside every calculation, or a small class
 * hierarchy. This is the hierarchy. Shared behavior - capping and rounding -
 * lives here once, so no derived class repeats it.
 *
 * LIMITATION (removed in Chapter 21): selection still happens through a single
 * branch in Gradebook, because these functions are not yet virtual. The scheme
 * is therefore fixed once the program starts.
 */
class GradingScheme {
public:
    explicit GradingScheme(const std::string& name) : name_(name) {}

    const std::string& name() const { return name_; }

protected:
    /** Applies the course cap-and-round policy. Shared by every scheme. */
    static double finalize(double rawPercentage);

private:
    std::string name_;
};

/** Total points earned divided by total points possible. */
class PointsBased : public GradingScheme {
public:
    PointsBased() : GradingScheme("Points-based") {}
    double computePercentage(const std::vector<Assignment>& work) const;
};

/** Each category scored separately, then combined by weight. */
class Weighted : public GradingScheme {
public:
    struct CategoryWeight {
        std::string name;
        double weight = 0.0;   // percentage points, should total 100
    };

    Weighted();
    explicit Weighted(const std::vector<CategoryWeight>& weights);

    double computePercentage(const std::vector<Assignment>& work) const;

    const std::vector<CategoryWeight>& weights() const { return weights_; }
    double weightTotal() const;
    bool weightsValid() const;

private:
    std::vector<CategoryWeight> weights_;
};

#endif
```

Read the three classes carefully:

- `GradingScheme` stores a `name_` and provides `finalize()`, the course's
  cap-and-round policy. `finalize` is **`protected`**: derived classes can
  call it, but code outside the hierarchy cannot. It is `static` because it
  does not need any one object's data.
- `class PointsBased : public GradingScheme` reads "a `PointsBased` **is a**
  `GradingScheme`." Its constructor passes the name `"Points-based"` up to the
  base-class constructor in its initializer list.
- `Weighted` adds a nested `CategoryWeight` struct (a category name and its
  weight) and a list of weights. It can tell you whether the weights total
  100 (`weightsValid()`).
- Notice that `computePercentage` is **not** `virtual` yet. Each derived class
  has its own version, but the program must still decide by hand which one to
  call. Chapter 21 removes that limitation.

### Step 3 — Implement the two schemes (`gradingscheme.cpp`)

Create a new file named `gradingscheme.cpp` and enter this code:

```cpp
// gradingscheme.cpp - Grade Calculator v3.0 - Chapter 20
#include "gradingscheme.h"

#include <algorithm>
#include <cmath>

namespace {
    const bool CAP_AT_100 = true;
}

double GradingScheme::finalize(double rawPercentage) {
    double reported = CAP_AT_100 ? std::min(rawPercentage, 100.0) : rawPercentage;
    return std::round(reported * 10.0) / 10.0;
}

double PointsBased::computePercentage(const std::vector<Assignment>& work) const {
    double earned = 0.0;
    double possible = 0.0;
    for (const Assignment& a : work) {
        earned   += a.totalEarned();
        possible += a.pointsPossible();
    }
    if (possible <= 0.0) { return 0.0; }
    return finalize(earned / possible * 100.0);
}

Weighted::Weighted() : GradingScheme("Weighted") {
    weights_ = { {"Exam", 50.0}, {"Homework", 30.0}, {"Participation", 20.0} };
}

Weighted::Weighted(const std::vector<CategoryWeight>& weights)
    : GradingScheme("Weighted"), weights_(weights) {}

double Weighted::weightTotal() const {
    double sum = 0.0;
    for (const CategoryWeight& w : weights_) { sum += w.weight; }
    return sum;
}

bool Weighted::weightsValid() const {
    return std::abs(weightTotal() - 100.0) < 0.001;
}

double Weighted::computePercentage(const std::vector<Assignment>& work) const {
    double weightedSum = 0.0;
    double weightUsed  = 0.0;

    for (const CategoryWeight& w : weights_) {
        double earned = 0.0;
        double possible = 0.0;
        for (const Assignment& a : work) {
            if (a.category() == w.name) {
                earned   += a.totalEarned();
                possible += a.pointsPossible();
            }
        }
        // A category with no graded work yet is skipped, and its weight is
        // redistributed across the categories that do have work. Otherwise a
        // student would be penalized for assignments not yet given.
        if (possible > 0.0) {
            weightedSum += (earned / possible) * w.weight;
            weightUsed  += w.weight;
        }
    }

    if (weightUsed <= 0.0) { return 0.0; }
    return finalize(weightedSum / weightUsed * 100.0);
}
```

- `PointsBased::computePercentage` is the same points math you have used since
  Chapter 4, now ending in `finalize(...)` from the base class.
- `Weighted::Weighted()` sets the default weights: Exam 50, Homework 30,
  Participation 20.
- `weightsValid()` compares the total to 100 **with a tolerance**
  (`< 0.001`), never with `==`, because the weights are `double`s — the
  floating-point trap from Chapter 6.
- `Weighted::computePercentage` scores each category separately and combines
  them by weight. A category with **no graded work yet is skipped**, and its
  weight is spread across the categories that do have work, so a student is
  not penalized for assignments that have not been given.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile cleanly and still behave exactly like v2.6 — the new classes exist but nothing uses them yet.

### Step 4 — Note the new role of `Student::percentage()`

`Student::percentage()` still computes a points-based percentage, but the
course grade will now come from a grading scheme. Record that in a comment so
the next reader is not misled.

In `student.h`, update the first line. Find:

```cpp
// student.h - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// student.h - Grade Calculator v3.0 - Chapter 20
```

In `student.h`, find:

```cpp
    double totalPossible() const;
    double percentage() const;
```

Replace it with:

```cpp
    double totalPossible() const;

    /** Points-based percentage. Kept for the report header and for sorting;
     *  the course grade now comes from a GradingScheme instead. */
    double percentage() const;
```

This is a comment-only change; `student.cpp` does not change at all.

### Step 5 — Make `Gradebook` scheme-aware (`gradebook.h`)

In `gradebook.h`, update the first line. Find:

```cpp
// gradebook.h - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v3.0 - Chapter 20
```

In `gradebook.h`, find the first project include:

```cpp
#include "gradescale.h"
```

Directly above it, add:

```cpp
#include "gradingscheme.h"
```

Find the constructor declaration:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");
```

Replace it with:

```cpp
    /** Which grading rule this gradebook applies. Fixed at construction in
     *  v3.0; Chapter 21 makes it changeable at any time. */
    enum class Scheme { Points, Weighted };

    explicit Gradebook(const std::string& courseName = "Untitled Course",
                       Scheme scheme = Scheme::Points);

    /** The course grade for one student under the selected scheme. */
    double percentageFor(const Student& s) const;
    std::string schemeName() const;
    const Weighted& weightedScheme() const { return weighted_; }
    void setWeights(const std::vector<Weighted::CategoryWeight>& w) { weighted_ = Weighted(w); }
```

At the bottom of the class, find:

```cpp
    int nextId_ = 1001;
};
```

Replace it with:

```cpp
    int nextId_ = 1001;

    // Both schemes are held as concrete objects, and a single branch in
    // percentageFor() chooses between them. That branch is the limitation
    // Chapter 21 removes with virtual functions.
    Scheme scheme_ = Scheme::Points;
    PointsBased points_;
    Weighted    weighted_;
};
```

What you added:

- `enum class Scheme { Points, Weighted };` names the two choices. Because it
  is declared inside `Gradebook`, its full name is `Gradebook::Scheme`.
- The constructor takes a second parameter, the scheme, **defaulting to
  `Scheme::Points`** — so `Gradebook book("Programming Fundamentals");` still
  compiles.
- `percentageFor(s)` returns a student's course grade under the selected
  scheme; `schemeName()` returns its display name.
- `weightedScheme()` and `setWeights()` let `main` read and replace the
  weights.
- The `Gradebook` **holds one object of each scheme** (`points_` and
  `weighted_`) plus the `scheme_` flag that says which to use.

### Step 6 — Grade through the selected scheme (`gradebook.cpp`)

In `gradebook.cpp`, update the first line to name this version. Find:

```cpp
// gradebook.cpp - Grade Calculator v2.6 - Chapter 19
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v3.0 - Chapter 20
```

In `gradebook.cpp`, find the constructor:

```cpp
Gradebook::Gradebook(const std::string& courseName) : courseName_(courseName) {}
```

Replace it with:

```cpp
Gradebook::Gradebook(const std::string& courseName, Scheme scheme)
    : courseName_(courseName), scheme_(scheme) {}

double Gradebook::percentageFor(const Student& s) const {
    // The single branch. One place today; one place per operation as soon as
    // a third scheme or a second calculation is added. See Section 20.2.
    if (scheme_ == Scheme::Weighted) {
        return weighted_.computePercentage(s.assignments());
    }
    return points_.computePercentage(s.assignments());
}

std::string Gradebook::schemeName() const {
    return scheme_ == Scheme::Weighted ? weighted_.name() : points_.name();
}
```

In `classAverage()`, find:

```cpp
    for (const Student& s : roster_) { sum += s.percentage(); }
```

Replace it with:

```cpp
    for (const Student& s : roster_) { sum += percentageFor(s); }
```

In `operator<<`, find the line that prints the scale:

```cpp
    out << "  " << book.scale() << "\n";
```

Directly below it, add:

```cpp
    out << "  Grading: " << book.schemeName() << "\n";
```

Further down in `operator<<`, inside the loop, find:

```cpp
        out << s << "   " << book.scale().letterFor(s.percentage()) << "\n";
```

Replace it with:

```cpp
        double pct = book.percentageFor(s);
        out << std::fixed << std::setprecision(1)
            << std::left << std::setw(6) << s.id()
            << std::setw(20) << s.name()
            << std::right << std::setw(8) << pct << "%   "
            << book.scale().letterFor(pct) << "\n";
```

- `percentageFor` contains **the single branch**: if the scheme is
  `Weighted`, ask `weighted_`; otherwise ask `points_`. Every grade in the
  program now flows through this one function.
- The class average and every report row now use `percentageFor(s)` instead
  of `s.percentage()`, so they honor the chosen scheme.
- The report row is now written out field by field, because the percentage
  printed must be the *scheme's* percentage, which `Student`'s own
  `operator<<` knows nothing about.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile cleanly. Because the scheme defaults to points, it still behaves like v2.6 — except that the report now shows a `Grading: Points-based` line.

### Step 7 — Update the header comment in `main.cpp`

At the top of `main.cpp`, find the header comment:

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

Replace it with:

```cpp
// =============================================================================
//  Grade Calculator  v3.0                                          Chapter 20
// -----------------------------------------------------------------------------
//  Change  : Weighted-category grading works. A GradingScheme base class with
//            PointsBased and Weighted derived classes replaces the single
//            hard-coded rule. Assignments now carry a category.
//  Chooses : the scheme is selected at STARTUP and fixed for the session.
//  Limit   : switching schemes requires restarting, because the selection is
//            a branch in Gradebook::percentageFor rather than dynamic
//            dispatch. Chapter 21 removes this.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

### Step 8 — Choose a scheme at startup, and read each assignment's category

`main` now asks for a scheme before the menu starts. If the user picks
weighted grading, it offers to replace the default weights. The *Add student*
loop also asks for a category.

Find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it, all the way to the final closing `}` at the very end of the file.

In its place, enter the new `main`:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v3.0 (two grading schemes) ===\n\n";
    std::cout << "Grading scheme for this session:\n";
    std::cout << "  1) Points-based   2) Weighted by category\n";
    std::string choice = readLine("Choice: ");

    Gradebook::Scheme scheme = (!choice.empty() && choice[0] == '2')
                             ? Gradebook::Scheme::Weighted
                             : Gradebook::Scheme::Points;
    Gradebook book("Programming Fundamentals", scheme);

    if (scheme == Gradebook::Scheme::Weighted) {
        std::cout << "\nDefault weights: Exam 50, Homework 30, Participation 20.\n";
        if (readLine("Enter your own weights? (y/n): ").substr(0, 1) == "y") {
            std::vector<Weighted::CategoryWeight> weights;
            while (true) {
                std::string name = readLine("  Category name (or 'done'): ");
                if (name == "done" || name.empty()) { break; }
                weights.push_back({name, readNonNegative("    Weight (percent): ")});
            }
            book.setWeights(weights);
            if (!book.weightedScheme().weightsValid()) {
                std::cout << "  Note: weights total "
                          << book.weightedScheme().weightTotal()
                          << ", not 100. Categories are scaled proportionally.\n";
            }
        }
        std::cout << "\nWhen adding assignments, use the category names above.\n";
    }

    bool running = true;
    while (running) {
        std::cout << "\n1) Add student  2) Report  3) Sort by grade  "
                     "4) Custom scale  5) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char c = line.empty() ? '?' : line[0];

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
            std::vector<GradeScale::Tier> requested;
            std::cout << "  Enter tiers highest first, 'done' to finish.\n";
            while (true) {
                std::string lt = readLine("    Letter (or 'done'): ");
                if (lt == "done" || lt.empty()) { break; }
                requested.push_back({readNonNegative("      Minimum percentage: "), lt[0]});
            }
            book.setScale(GradeScale(requested));
            std::cout << "  " << book.scale() << "\n";
        } else if (c == '5') {
            running = false;
        } else {
            std::cout << "  Please enter 1-5.\n";
        }
    }
    std::cout << "\nGoodbye.\n";
    return 0;
}
```

What changed, from top to bottom:

- **Choosing the scheme.** The answer is read into a `std::string` named
  `choice`, and a conditional expression turns it into a `Gradebook::Scheme`
  value, which is passed to the `Gradebook` constructor. The scheme is fixed
  for the session.
- **Optional custom weights.** For weighted grading, the user can enter their
  own categories and weights. If they do not total 100, the program prints a
  note — it does not reject them; categories are scaled proportionally.
- **The menu variable is renamed `c`.** The name `choice` is now taken by the
  scheme answer, so the menu choice uses `char c`. Every `if` in the loop
  compares `c`.
- **Add student** asks for a `Category` after the bonus. Pressing Enter with no
  category stores `"Uncategorized"`. The category is passed as the fifth
  constructor argument.
- **Sort** prints `Sorted.`, and **Custom scale** reads each letter into `lt`
  and passes `readNonNegative(...)` straight into the tier — the same steps as
  before, written more compactly.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile with no errors and no warnings and open with the scheme question.

## Check your work

**Run 1 — points-based.** Answer the scheme question with `1`. Add `Ada` with
two assignments: `Exam 1` (earned `90`, possible `100`, bonus `0`, category
`Exam`) and `HW1` (earned `10`, possible `10`, bonus `0`, category `Homework`).
Type `done`, then choose `2`. The report should include:

```text
  Grading: Points-based
=====================================
1001  Ada                     90.9%   A
```

Check: (90 + 10) ÷ (100 + 10) = 100 ÷ 110 = 90.9%. Choose `5` to quit.

**Run 2 — weighted, default weights.** Run again, choose `2`, and answer `n`
to custom weights. Add the same two assignments for `Ada` and choose `2`:

```text
  Grading: Weighted
=====================================
1001  Ada                     93.8%   A
```

Check: Exam 0.90 × 50 = 45; Homework 1.00 × 30 = 30. Participation has no
work, so its 20 is skipped: 75 ÷ 80 = 93.75%, rounded to 93.8%. **The same
scores, two different grades** — that is the point of choosing a scheme.

**Run 3 — weights that do not total 100.** Run again, choose `2`, answer `y`,
and enter `Exam` `60`, `Homework` `30`, then `done`. You should see:

```text
  Note: weights total 90, not 100. Categories are scaled proportionally.
```

Add the same two assignments for `Ada` and report: she shows `93.3%`
((0.90 × 60 + 1.00 × 30) ÷ 90).

Then confirm:

- [ ] All eleven files build together with no errors and no warnings.
- [ ] `PointsBased` and `Weighted` both inherit `public`ly from
      `GradingScheme`, and neither repeats the cap-and-round code — both call
      `finalize`.
- [ ] `gradescale.h`, `gradescale.cpp`, and `student.cpp` are unchanged from
      Chapter 19.

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

2. Work through Steps 1–8 above in your local editor, in order, building and running at each ▶ Build checkpoint.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 20 Grade Calculator v3.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 20 checkpoint.
- The commit is pushed to GitHub.
