# Chapter 18 Lab — Introduce Classes and Invariants

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.5
- **Starting point:** Your committed Chapter 17 v2.4 program (`main.cpp`).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

In this lab you rebuild the Grade Calculator's data around **classes** instead
of structs. By the end you will have:

1. An `Assignment` class that holds one graded item — its name, points earned,
   points possible, and bonus — behind `private` data and `const` accessors.
   The old `Score` struct is folded into it.
2. A `GradeScale` class whose constructor **enforces an invariant**: cutoffs
   strictly descend and the lowest tier is 0. Whatever tiers a user types, the
   constructor repairs them into a usable scale, so no other code ever has to
   check.
3. A `Student` class that **owns its own assignments** and computes its own
   percentage with a `percentage()` member that needs no parameters.
4. A smaller, cleaner `main` with four menu options: **Add student**,
   **Report**, **Custom scale**, and **Quit**.

## What is different about v2.5

v2.5 is a *rebuild*, not an add-on, so a few things from Chapter 17 change on
purpose. Read this before you start so nothing surprises you.

- **Assignments are entered per student.** In v2.4 you added assignments once
  for the whole course, and each student held a list of scores that lined up
  with that list by position. In v2.5 each `Student` owns its own `Assignment`
  objects, so you enter a student's assignments right after the student's
  name. The separate *Add assignment* menu option goes away.
- **The `Gradebook` struct goes away.** `main` holds a `GradeScale`, a
  `std::vector<Student>`, and a next-ID counter directly. (Chapter 19 brings
  back a `Gradebook` — as a real class.)
- **v2.5 starts from a smaller core.** Saving and loading (Chapter 15), the
  regression tests (Chapter 16), and sort and find (Chapter 17) are set aside
  in this checkpoint so you can concentrate on classes. They are not lost:
  your Chapter 17 commit keeps them in your repository's history. Sorting
  returns in Chapter 19, Find by ID in Chapter 23, and saving and loading in
  Chapter 24 — each rebuilt on top of the classes you write today.
- **The grading math does not change.** The same scores still produce the
  same percentage and letter grade.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit. Everything in this lab happens in this one file. |

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

> **Heads-up:** Steps 2 through 7 take the program apart before Step 8 puts
> `main` back together, so the program will **not** compile again until the
> end of Step 8. That is expected. Do not try to fix compiler errors in the
> middle — finish the steps in order, then build.

## Build it: step by step

### Step 1 — Update the header comment

Every version of the program opens with a comment block that says what
changed. Update it so the file describes v2.5.

At the very top of `main.cpp`, find the header comment:

```cpp
// =============================================================================
//  Grade Calculator  v2.4                                          Chapter 17
// -----------------------------------------------------------------------------
//  Change  : Sorting and searching. The roster can be sorted by name, by
//            percentage, or by ID, with the comparison chosen at run time.
//            Search by ID is implemented both linearly and with binary search
//            so the two can be compared on the same data.
//  Format  : documented in gradebook-format.md (section-tagged CSV, chosen so
//            new record types can be added later without breaking old files).
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
// =============================================================================
```

Replace it with:

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

*Why:* the header is the first thing a reader (including future you) sees. It
should describe the code that is actually in the file.

### Step 2 — Update the `#include` list and constants

v2.5 no longer reads or writes files, so it no longer needs `<fstream>`,
`<sstream>`, or the `DEFAULT_FILE` constant. It does need `<algorithm>`,
because `Student::percentage()` will call `std::min`.

Just below the header comment, find the `#include` lines and the two constants:

```cpp
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

const bool CAP_AT_100 = true;
const std::string DEFAULT_FILE = "gradebook.csv";
```

Replace it with:

```cpp
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

const bool CAP_AT_100 = true;
```

*Why:* include what you use, and only what you use (Appendix D, Section D.4).
`CAP_AT_100` stays — the course still caps a reported percentage at 100.

### Step 3 — Replace the structs with an `Assignment` class

Chapter 17's data lived in five structs: `Assignment` (a name and points
possible), `Score` (points earned and bonus), `Student` (which held a list of
`Score`s), `GradeTier`, and `Gradebook`. In v2.5 an assignment belongs to
exactly one student, so it can hold *everything* about itself — and `Score`
is no longer needed.

Find the first struct, just below `CAP_AT_100`:

```cpp
struct Assignment { std::string name; double pointsPossible = 0.0; };
```

Delete that line and everything below it (the `Score`, `Student`, `GradeTier`, and `Gradebook` structs), down to and including this line:

```cpp
};
```

In the space where the five structs were, enter the `Assignment` class:

```cpp
// -----------------------------------------------------------------------------
//  Assignment - one graded item belonging to one student.
// -----------------------------------------------------------------------------
class Assignment {
public:
    Assignment() = default;
    Assignment(const std::string& name, double earned, double possible, double bonus = 0.0)
        : name_(name), pointsEarned_(earned), pointsPossible_(possible), bonusPoints_(bonus) {}

    const std::string& name() const { return name_; }
    double pointsEarned() const     { return pointsEarned_; }
    double pointsPossible() const   { return pointsPossible_; }
    double bonusPoints() const      { return bonusPoints_; }

    /** Points credited to the student: raw score plus any bonus. */
    double totalEarned() const { return pointsEarned_ + bonusPoints_; }

    /** Fraction of possible points earned, or 0 for an ungraded item. */
    double ratio() const {
        return pointsPossible_ > 0.0 ? totalEarned() / pointsPossible_ : 0.0;
    }

private:
    std::string name_;
    double pointsEarned_   = 0.0;
    double pointsPossible_ = 0.0;
    double bonusPoints_    = 0.0;
};
```

Look at what changed:

- The data members are **`private`** and end in an underscore (`name_`,
  `pointsEarned_`) — the naming convention from Appendix D that marks a member
  variable. Code outside the class can no longer change them directly.
- The **constructor** uses a member initializer list to set all four values
  at once. `bonus` has a default of `0.0`, so a caller can leave it out.
- Every accessor ends in **`const`**, which promises the compiler it does not
  change the object.
- `totalEarned()` and `ratio()` are **behavior that lives with the data**.
  Bonus is added to points earned, never to points possible — the D2 rule from
  Chapter 16, now written once in the class that owns the numbers.

### Step 4 — Add the `GradeScale` class and its invariant

In v2.4 the scale was a plain `std::vector<GradeTier>`, and nothing stopped
the program from holding a broken one (tiers out of order, no 0 tier). The
`GradeScale` class makes a broken scale impossible to build.

Find the comment line that now sits just below the `Assignment` class:

```cpp
// ---------- input helpers ----------
```

Directly above it, add:

```cpp
// -----------------------------------------------------------------------------
//  GradeScale - an ordered set of cutoffs and letters.
//  INVARIANT: cutoffs strictly descend and the lowest tier is 0.
//  The constructor enforces this, so no other code needs to check it.
// -----------------------------------------------------------------------------
class GradeScale {
public:
    struct Tier {
        double cutoff = 0.0;
        char   letter = 'F';
    };

    /** Builds the default A/B/C/D/F scale. */
    GradeScale() {
        tiers_ = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };
    }

    /**
     * Builds a scale from user-supplied tiers, repairing what it can.
     * Out-of-order tiers are dropped; a missing floor tier is added.
     * The result is always a usable scale - that is the invariant.
     */
    explicit GradeScale(const std::vector<Tier>& requested) {
        for (const Tier& t : requested) {
            if (t.cutoff < 0.0) { continue; }
            if (!tiers_.empty() && t.cutoff >= tiers_.back().cutoff) { continue; }
            tiers_.push_back(t);
        }
        if (tiers_.empty() || tiers_.back().cutoff > 0.0) {
            tiers_.push_back({0.0, 'F'});
        }
    }

    /** Every percentage from 0 upward maps to a letter. Cannot fail. */
    char letterFor(double percentage) const {
        for (const Tier& t : tiers_) {
            if (percentage >= t.cutoff) { return t.letter; }
        }
        return tiers_.back().letter;
    }

    std::size_t tierCount() const { return tiers_.size(); }
    const std::vector<Tier>& tiers() const { return tiers_; }

    void describe() const {
        std::cout << "  Scale: ";
        for (const Tier& t : tiers_) {
            std::cout << t.letter << " >= " << std::fixed << std::setprecision(0)
                      << t.cutoff << "   ";
        }
        std::cout << "\n";
    }

private:
    std::vector<Tier> tiers_;
};
```

Study the second constructor — it is the heart of this chapter:

- `GradeScale()` with no arguments builds the default A/B/C/D/F scale.
- `explicit GradeScale(const std::vector<Tier>& requested)` walks the tiers
  the user asked for and **keeps only the ones that preserve the invariant**:
  a negative cutoff is skipped, and a cutoff that is not lower than the
  previous kept tier is skipped. If the result does not reach 0, an `F` tier
  at 0 is added.
- Because *every* `GradeScale` passes through one of these constructors, the
  invariant is always true. That is why `letterFor` has no error handling: it
  cannot be handed a bad scale.
- `Tier` is a small struct **nested inside** the class, so its full name is
  `GradeScale::Tier`. It replaces the old `GradeTier` struct.
- `describe()` prints the scale on one line, so `main` does not need to know
  how a scale is stored.

### Step 5 — Add the `Student` class

A `Student` now owns a `std::vector<Assignment>`. Everything needed to compute
a grade is inside the object.

Find the same comment line again — it is now just below the `GradeScale` class:

```cpp
// ---------- input helpers ----------
```

Directly above it, add:

```cpp
// -----------------------------------------------------------------------------
//  Student - owns a name, an ID, and its own assignments.
// -----------------------------------------------------------------------------
class Student {
public:
    Student() = default;
    Student(const std::string& name, int id) : name_(name), id_(id) {}

    const std::string& name() const { return name_; }
    int id() const { return id_; }
    const std::vector<Assignment>& assignments() const { return assignments_; }

    void addAssignment(const Assignment& a) { assignments_.push_back(a); }

    double totalEarned() const {
        double sum = 0.0;
        for (const Assignment& a : assignments_) { sum += a.totalEarned(); }
        return sum;
    }

    double totalPossible() const {
        double sum = 0.0;
        for (const Assignment& a : assignments_) { sum += a.pointsPossible(); }
        return sum;
    }

    /** Points-based course percentage, capped and rounded by course policy. */
    double percentage() const {
        double possible = totalPossible();
        if (possible <= 0.0) { return 0.0; }
        double raw = totalEarned() / possible * 100.0;
        double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
        return std::round(reported * 10.0) / 10.0;
    }

private:
    std::string name_;
    int id_ = 0;
    std::vector<Assignment> assignments_;
};
```

Compare `percentage()` with Chapter 17's `percentageOf(student, assignments)`.
The old function needed the course-wide assignment list passed in, because a
student only held scores. The new member function takes **no parameters** —
the student has everything it needs. It still applies the same course policy:
skip a zero total to avoid dividing by zero, cap at 100 when `CAP_AT_100` is
`true`, and round to one decimal place.

`addAssignment` is the **only** way to put work into a student, so there is
exactly one place to look if a student's work ever looks wrong.

### Step 6 — Update the input-helpers banner

Your `readNonNegative` and `readLine` functions do not change. Only the
comment above them changes, to match the banner style of the classes above it.

Find the comment line:

```cpp
// ---------- input helpers ----------
```

Replace it with:

```cpp
// -----------------------------------------------------------------------------
//  Input helpers
// -----------------------------------------------------------------------------
```

### Step 7 — Remove the code that v2.5 sets aside

Everything between `readLine` and `main` belonged to the struct-based design:
the CSV helpers and `saveGradebook`/`loadGradebook` (Chapter 15), the free
functions `letterFor`, `percentageOf`, and `printReport`, the regression tests
(Chapter 16), and the sort and search functions (Chapter 17). The classes now
do the grading work, and the other features are set aside for this checkpoint
(see *What is different about v2.5*).

Find the line just below the end of `readLine`:

```cpp
// ---------- CSV helpers ----------
```

Delete that line and everything below it (all the CSV, persistence, grading, test, sorting, and searching code), stopping just **above** this line, which you keep:

```cpp
int main() {
```

When you are done, the closing `}` of `readLine` should be followed by one
blank line and then `int main() {`.

*Why:* in Chapter 17 this code worked on `Student::scores` and the shared
`book.assignments` list. Neither exists any more, so keeping it would only
produce compiler errors. Your Chapter 17 commit still has every line of it if
you want to look back.

### Step 8 — Rewrite `main` around the new classes

`main` gets simpler: three local variables replace the `Gradebook` struct, and
the menu has four options.

Find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it, all the way to the final closing `}` at the very end of the file.

In its place, enter the new `main`:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v2.5 (classes) ===\n\n";

    GradeScale scale;   // default scale; invariant guaranteed by construction
    scale.describe();

    std::vector<Student> roster;
    int nextId = 1001;

    bool running = true;
    while (running) {
        std::cout << "\n1) Add student  2) Report  3) Custom scale  4) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char choice = line.empty() ? '?' : line[0];

        if (choice == '1') {
            std::string name = readLine("  Student name: ");
            if (name.empty()) { continue; }
            Student s(name, nextId++);
            while (true) {
                std::string an = readLine("    Assignment name (or 'done'): ");
                if (an == "done" || an.empty()) { break; }
                double earned   = readNonNegative("      Points earned  : ");
                double possible = readNonNegative("      Points possible: ");
                double bonus    = readNonNegative("      Bonus points   : ");
                s.addAssignment(Assignment(an, earned, possible, bonus));
            }
            roster.push_back(s);
            std::cout << "  Added " << s.name() << " as ID " << s.id() << ".\n";

        } else if (choice == '2') {
            std::cout << "\n=====================================\n  CLASS REPORT\n";
            std::cout << "=====================================\n";
            std::cout << std::fixed << std::setprecision(1);
            if (roster.empty()) { std::cout << "No students yet.\n"; continue; }
            for (const Student& s : roster) {
                std::cout << std::left << std::setw(6) << s.id()
                          << std::setw(20) << s.name()
                          << std::right << std::setw(8) << s.percentage() << "%   "
                          << scale.letterFor(s.percentage()) << "\n";
            }

        } else if (choice == '3') {
            std::vector<GradeScale::Tier> requested;
            std::cout << "  Enter tiers highest first, 'done' to finish.\n";
            while (true) {
                std::string letterText = readLine("    Letter (or 'done'): ");
                if (letterText == "done" || letterText.empty()) { break; }
                double cutoff = readNonNegative("      Minimum percentage: ");
                requested.push_back({cutoff, letterText[0]});
            }
            // Any bad input is repaired by the constructor, not by this code.
            scale = GradeScale(requested);
            std::cout << "  Scale accepted.\n";
            scale.describe();

        } else if (choice == '4') {
            running = false;
        } else {
            std::cout << "  Please enter 1-4.\n";
        }
    }
    std::cout << "\nGoodbye.\n";
    return 0;
}
```

Walk through what each part does:

- **Startup.** `GradeScale scale;` builds the default scale — valid by
  construction. `scale.describe()` prints it so the user can see it.
- **Option 1 — Add student.** After reading the name, `Student s(name,
  nextId++)` creates the student with the next ID. The inner loop reads one
  assignment at a time (name, points earned, points possible, bonus) until the
  user types `done` or presses Enter on an empty name, adding each one with
  `s.addAssignment(...)`. Only then is the finished student added to the
  roster.
- **Option 2 — Report.** Each row calls `s.id()`, `s.name()`, and
  `s.percentage()` — accessors, not data members — and
  `scale.letterFor(...)` for the letter.
- **Option 3 — Custom scale.** The loop collects tiers into a
  `std::vector<GradeScale::Tier>` without checking them, then
  `scale = GradeScale(requested);` builds a new scale. **The constructor does
  the repairing** — this code contains no validation at all.
- **Option 4 — Quit** ends the loop. Because there is no file to save in
  v2.5, the program simply says goodbye.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile with no errors and no warnings and show the v2.5 banner, the default scale, and the four-option menu. If you see errors, the message names a line — compare that area with the code boxes above.

## Check your work

Run the program and type the inputs below in your terminal. Your output should
match.

1. Choose `1` (Add student). Enter the name `Ada`. Add two assignments:
   `HW1` with points earned `9`, points possible `10`, bonus `1`; and
   `Midterm` with `84`, `100`, bonus `5`. Type `done`. The program should
   print `Added Ada as ID 1001.`
2. Choose `2` (Report). You should see:

   ```text
   =====================================
     CLASS REPORT
   =====================================
   1001  Ada                     90.0%   A
   ```

   Check it by hand: (9 + 1 + 84 + 5) ÷ (10 + 100) = 99 ÷ 110 = 90.0%.
3. Choose `3` (Custom scale). Enter `A` with `93`, `B` with `85`, and then
   `ZZZ` with `99`. Type `done`. You should see:

   ```text
     Scale accepted.
     Scale: A >= 93   B >= 85   F >= 0
   ```

   The `ZZZ` tier was dropped because 99 is not below 85, and an `F` tier at
   0 was added because your scale did not reach 0. The constructor repaired
   the input — no error, no crash.
4. Choose `2` again. Ada's 90.0% is now a `B` under the stricter scale. The
   data did not change; only the scale did.
5. Choose `4` (Quit). The program prints `Goodbye.` and ends normally.

Then confirm:

- [ ] The program compiles with no errors **and no warnings**.
- [ ] `Assignment`, `GradeScale`, and `Student` have only `private` data
      members; `main` reaches their data only through member functions.
- [ ] Every accessor that does not change its object is marked `const`.
- [ ] The structs `Score`, `GradeTier`, and `Gradebook` no longer appear
      anywhere in `main.cpp`.
- [ ] The menu shows exactly four options: Add student, Report, Custom scale,
      Quit.

## Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Work through Steps 1–8 above in your local editor, in order. Build and run at the ▶ Build checkpoint at the end of Step 8.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 18 Grade Calculator v2.5"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 18 checkpoint.
- The commit is pushed to GitHub.
