# Chapter 21 Lab — Select Schemes with Polymorphism

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.1
- **Starting point:** Your committed Chapter 20 v3.0 program (eleven files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

In v3.0 the grading scheme was chosen once at startup, and `Gradebook` used
an `if` to decide which scheme's `computePercentage` to call. In this lab you
make the scheme **polymorphic**. By the end you will have:

1. An **abstract** `GradingScheme` base class with a **pure virtual**
   `computePercentage` and a **virtual destructor**.
2. A third scheme, `WeightedDropLowest`, that drops the weakest assignment in
   each category — added **without changing** `Gradebook`, `Student`,
   `GradeScale`, `Assignment`, or the report code.
3. A `Gradebook` that holds a single `GradingScheme*` and calls through it.
   The `if` is gone, and because the `Gradebook` owns that pointer, it manages
   the memory correctly by hand: a destructor, a `delete` before replacing,
   and copying disabled.
4. A `chooseScheme` function and a new menu option, **Change scheme**, so the
   user can switch schemes mid-session and every grade recomputes
   immediately.

## What is different about v3.1

- **No startup weights prompt.** v3.0 let you type custom category weights
  at startup. v3.1 removes that prompt to keep the focus on polymorphism:
  `Weighted` and `WeightedDropLowest` use the default weights (Exam 50,
  Homework 30, Participation 20). Custom weights come back in Chapter 24.
- **The menu grows to six options**: Add student, Report, Sort, Custom scale,
  **Change scheme** (new), and Quit (now option 6).

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradingscheme.h`, `gradingscheme.cpp` | Edit (Steps 1–2) |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 3–4) |
| `main.cpp` | Edit (Steps 5–7) |
| `assignment.*`, `gradescale.*`, `student.*` | **No change** — keep them open |

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

## Build it: step by step

### Step 1 — Make `GradingScheme` abstract (`gradingscheme.h`)

In `gradingscheme.h`, find the first line:

```cpp
// gradingscheme.h - Grade Calculator v3.0 - Chapter 20
```

Replace it with:

```cpp
// gradingscheme.h - Grade Calculator v3.1 - Chapter 21
```

Next, inside the comment block above `class GradingScheme`, find these lines:

```cpp
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
```

Replace it with:

```cpp
 * Abstract base class for grading schemes.
 *
 * computePercentage is pure virtual, so GradingScheme cannot be instantiated
 * and every concrete scheme must supply a rule. Gradebook holds a pointer to
 * this type and never asks which scheme it has - the branch from v3.0 is gone.
 *
 * The destructor is virtual because Gradebook deletes through a base pointer.
 * Without it, only the base part of the object would be destroyed.
 *
 * OWNERSHIP NOTE (revisited in Chapter 22): Gradebook owns a raw pointer.
 * That is correct here, but only because Gradebook also writes a destructor,
 * deletes the old scheme before replacing it, and disables copying. Miss any
 * one of those three and the program leaks or double-frees. Chapter 22 shows
 * how to get the same behavior with none of that hand-written ceremony.
```

Inside `class GradingScheme`, find the constructor:

```cpp
    explicit GradingScheme(const std::string& name) : name_(name) {}
```

Directly below it, add:

```cpp
    virtual ~GradingScheme() = default;

    /** Computes the course percentage. Every scheme defines its own rule. */
    virtual double computePercentage(const std::vector<Assignment>& work) const = 0;
```

These two lines change what kind of class `GradingScheme` is:

- **`= 0`** makes `computePercentage` a **pure virtual function**. The base
  class declares that every scheme *has* a rule but supplies none itself. A
  class with a pure virtual function is **abstract** — you cannot create a
  plain `GradingScheme` object, only objects of derived classes.
- **`virtual`** means that when code calls `computePercentage` through a
  `GradingScheme*`, C++ looks at the object the pointer actually points to and
  runs *that* class's version. This is **dynamic dispatch**.
- The **virtual destructor** matters because `Gradebook` will `delete` a
  scheme through a `GradingScheme*`. Without `virtual`, only the base part of
  the object would be destroyed.

Now mark each derived class's version with `override`.

In `class PointsBased`, find:

```cpp
    PointsBased() : GradingScheme("Points-based") {}
    double computePercentage(const std::vector<Assignment>& work) const;
```

Replace it with:

```cpp
    PointsBased() : GradingScheme("Points-based") {}
    double computePercentage(const std::vector<Assignment>& work) const override;
```

In `class Weighted`, find:

```cpp
    explicit Weighted(const std::vector<CategoryWeight>& weights);

    double computePercentage(const std::vector<Assignment>& work) const;
```

Replace it with:

```cpp
    explicit Weighted(const std::vector<CategoryWeight>& weights);

    double computePercentage(const std::vector<Assignment>& work) const override;
```

`override` asks the compiler to confirm that this function really overrides a
virtual function in the base class. If you misspell the name or get a
parameter wrong, you get a compile error instead of a silent new function.

Finally, let a future derived class reach `Weighted`'s weights, and add the
third scheme.

At the bottom of `class Weighted`, find:

```cpp
private:
    std::vector<CategoryWeight> weights_;
};
```

Replace it with:

```cpp
protected:
    std::vector<CategoryWeight> weights_;
};

/**
 * Proof that the design is open to extension: a third scheme.
 *
 * Adding this class required NO change to Gradebook, Student, GradeScale,
 * Assignment, or the report code. Compare with the flag-based design of
 * Section 20.2, where a third scheme means editing every branch.
 */
class WeightedDropLowest : public Weighted {
public:
    WeightedDropLowest();
    explicit WeightedDropLowest(const std::vector<CategoryWeight>& weights);
    double computePercentage(const std::vector<Assignment>& work) const override;
};
```

- `weights_` changes from `private` to **`protected`**, so the derived class
  `WeightedDropLowest` can read the weights directly.
- `class WeightedDropLowest : public Weighted` inherits everything from
  `Weighted` — the weights, `weightTotal()`, `weightsValid()`, even its name —
  and overrides only `computePercentage`.

### Step 2 — Implement the third scheme (`gradingscheme.cpp`)

In `gradingscheme.cpp`, find the first line:

```cpp
// gradingscheme.cpp - Grade Calculator v3.0 - Chapter 20
```

Replace it with:

```cpp
// gradingscheme.cpp - Grade Calculator v3.1 - Chapter 21
```

Go to the very end of `gradingscheme.cpp`, after the closing `}` of `Weighted::computePercentage`. Leave one blank line and add:

```cpp
WeightedDropLowest::WeightedDropLowest() : Weighted() {}

WeightedDropLowest::WeightedDropLowest(const std::vector<CategoryWeight>& weights)
    : Weighted(weights) {}

double WeightedDropLowest::computePercentage(const std::vector<Assignment>& work) const {
    double weightedSum = 0.0;
    double weightUsed  = 0.0;

    for (const CategoryWeight& w : weights_) {
        // Collect this category's work, then discard its weakest item.
        std::vector<const Assignment*> items;
        for (const Assignment& a : work) {
            if (a.category() == w.name && a.pointsPossible() > 0.0) {
                items.push_back(&a);
            }
        }
        if (items.size() > 1) {
            std::size_t worst = 0;
            for (std::size_t i = 1; i < items.size(); ++i) {
                if (items[i]->ratio() < items[worst]->ratio()) { worst = i; }
            }
            items.erase(items.begin() + static_cast<long>(worst));
        }

        double earned = 0.0;
        double possible = 0.0;
        for (const Assignment* a : items) {
            earned   += a->totalEarned();
            possible += a->pointsPossible();
        }
        if (possible > 0.0) {
            weightedSum += (earned / possible) * w.weight;
            weightUsed  += w.weight;
        }
    }
    if (weightUsed <= 0.0) { return 0.0; }
    return finalize(weightedSum / weightUsed * 100.0);
}
```

- Both constructors pass straight through to `Weighted`'s constructors, so a
  `WeightedDropLowest` starts with the same default weights.
- `computePercentage` follows the same plan as `Weighted`'s, with one extra
  step per category: it collects pointers to that category's assignments,
  finds the one with the lowest `ratio()`, and erases it — but only if the
  category has more than one item.

> **▶ Run checkpoint:** Click **Run**. The program should compile cleanly and behave exactly like v3.0. `Gradebook` still holds concrete `PointsBased` and `Weighted` objects, which is allowed — only `GradingScheme` itself is abstract.

### Step 3 — Hold the scheme through a base-class pointer (`gradebook.h`)

In `gradebook.h`, find the first line:

```cpp
// gradebook.h - Grade Calculator v3.0 - Chapter 20
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v3.1 - Chapter 21
```

Inside the class, find the scheme enum, the constructor, and the scheme accessors:

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

Replace it with:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");
    ~Gradebook();

    // Copying is disabled: Gradebook owns a raw pointer, and a default copy
    // would leave two objects deleting the same scheme. Chapter 22 replaces
    // this restriction with smart-pointer ownership.
    Gradebook(const Gradebook&) = delete;
    Gradebook& operator=(const Gradebook&) = delete;

    /**
     * Installs a grading scheme. The Gradebook takes ownership.
     * Can be called at any time; every grade is recomputed on the next report.
     */
    void setScheme(GradingScheme* scheme);

    /** The course grade for one student. No branch: the scheme decides. */
    double percentageFor(const Student& s) const;
    std::string schemeName() const;
```

At the bottom of the class, find:

```cpp
    // Both schemes are held as concrete objects, and a single branch in
    // percentageFor() chooses between them. That branch is the limitation
    // Chapter 21 removes with virtual functions.
    Scheme scheme_ = Scheme::Points;
    PointsBased points_;
    Weighted    weighted_;
```

Replace it with:

```cpp
    // One pointer to an abstract base. Which concrete scheme it refers to is
    // not this class's concern - that is what polymorphism buys.
    GradingScheme* scheme_ = nullptr;
```

- The `Scheme` enum, the two concrete scheme objects, `weightedScheme()`, and
  `setWeights()` are all gone. `Gradebook` now holds **one pointer to the
  abstract base**, and never needs to know which concrete scheme it points to.
- `setScheme` installs a new scheme. The comment states the ownership rule:
  **the `Gradebook` takes ownership** of the object it is given.
- Owning a raw pointer brings three duties, and the header shows all three:
  1. a **destructor** (`~Gradebook();`) to `delete` the scheme;
  2. `setScheme` must `delete` the old scheme before replacing it (Step 4);
  3. **copying is disabled** with `= delete`. A copied `Gradebook` would
     hold the same pointer as the original, and both would `delete` it.

### Step 4 — Dispatch through the pointer (`gradebook.cpp`)

In `gradebook.cpp`, find the first line:

```cpp
// gradebook.cpp - Grade Calculator v3.0 - Chapter 20
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v3.1 - Chapter 21
```

Find the constructor, `percentageFor`, and `schemeName`:

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

Replace it with:

```cpp
Gradebook::Gradebook(const std::string& courseName)
    : courseName_(courseName), scheme_(new PointsBased()) {}

Gradebook::~Gradebook() {
    delete scheme_;
}

void Gradebook::setScheme(GradingScheme* scheme) {
    if (scheme == nullptr || scheme == scheme_) { return; }
    delete scheme_;          // release the previous scheme before replacing it
    scheme_ = scheme;
}

double Gradebook::percentageFor(const Student& s) const {
    // Dynamic dispatch: the object decides which computePercentage runs.
    return scheme_->computePercentage(s.assignments());
}

std::string Gradebook::schemeName() const {
    return scheme_->name();
}
```

- The constructor starts every `Gradebook` with a `new PointsBased()`, so
  `scheme_` is never null.
- The destructor deletes the scheme. `setScheme` ignores a null pointer or the
  scheme it already holds, deletes the old scheme, then stores the new one.
- **`percentageFor` has no branch.** `scheme_->computePercentage(...)` runs
  `PointsBased`'s, `Weighted`'s, or `WeightedDropLowest`'s version depending
  on the object `scheme_` points to. The same is true of `schemeName()`.

The rest of `gradebook.cpp` — `classAverage`, `sortByPercentage`, and
`operator<<` — does not change, because it already calls `percentageFor`.

> **Heads-up:** `main.cpp` still uses `Gradebook::Scheme`, which no longer
> exists, so the program will not compile until the end of Step 7.

### Step 5 — Update the header comment in `main.cpp`

At the top of `main.cpp`, find the header comment:

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

Replace it with:

```cpp
// =============================================================================
//  Grade Calculator  v3.1                                          Chapter 21
// -----------------------------------------------------------------------------
//  Change  : GradingScheme is now abstract with a pure virtual computePercentage
//            and a virtual destructor. Gradebook holds a GradingScheme* and
//            never asks which scheme it has - the v3.0 branch is gone.
//            The scheme can be switched MID-SESSION and every grade recomputes.
//            A third scheme (WeightedDropLowest) was added without changing
//            Gradebook, Student, GradeScale, Assignment, or the report code.
//  Cost    : correct raw-pointer ownership needs three pieces of hand-written
//            bookkeeping in Gradebook - a destructor, a delete inside
//            setScheme, and deleted copy operations. This build has all three
//            and does not leak. Chapter 22 removes the need for any of them.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

### Step 6 — Add `chooseScheme`, the one place that names concrete types

In `main.cpp`, find the first line of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/** Builds the scheme the user asked for. The only place that names the
 *  concrete types; everything downstream sees only GradingScheme. */
void chooseScheme(Gradebook& book) {
    std::cout << "  1) Points-based\n";
    std::cout << "  2) Weighted by category\n";
    std::cout << "  3) Weighted, lowest dropped per category\n";
    std::string c = readLine("  Choice: ");
    if (!c.empty() && c[0] == '2')      { book.setScheme(new Weighted()); }
    else if (!c.empty() && c[0] == '3') { book.setScheme(new WeightedDropLowest()); }
    else                                { book.setScheme(new PointsBased()); }
    std::cout << "  Grading is now: " << book.schemeName() << "\n";
}
```

This function still has a branch — but look at what it does. It runs only
when the user makes a choice, and its only job is to **create** the right
object with `new` and hand it to `book.setScheme(...)`, which takes
ownership. Nothing downstream ever asks which scheme it has.

### Step 7 — Rewrite `main` with a *Change scheme* option

Find the start of `main`:

```cpp
int main() {
```

Delete that line and everything below it, all the way to the final closing `}` at the very end of the file.

In its place, enter the new `main`:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v3.1 (switchable schemes) ===\n\n";

    Gradebook book("Programming Fundamentals");
    std::cout << "Select a grading scheme:\n";
    chooseScheme(book);

    bool running = true;
    while (running) {
        std::cout << "\n1) Add student  2) Report  3) Sort  "
                     "4) Custom scale  5) Change scheme  6) Quit\nChoice: ";
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
            // Every existing student is regraded under the new rule. No data
            // is re-entered, and no other class knows this happened.
            chooseScheme(book);
        } else if (c == '6') {
            running = false;
        } else {
            std::cout << "  Please enter 1-6.\n";
        }
    }
    std::cout << "\nGoodbye.\n";
    return 0;
}
```

- At startup, the `Gradebook` is created first (with its default points
  scheme), and then `chooseScheme(book)` lets the user pick.
- The menu has six options. **Change scheme** (option 5) simply calls
  `chooseScheme(book)` again. Every existing student is regraded under the new
  rule the next time you ask for a report — no data is re-entered.
- **Sort**, **Custom scale**, and **Add student** work exactly as in v3.0.

> **▶ Run checkpoint:** Make sure all eleven files are open and click **Run**. The program should compile with no errors and no warnings and open by asking you to select a grading scheme.

## Check your work

Run the program and choose `1` (Points-based). Add `Ada` with three
assignments:

| Assignment | Earned | Possible | Bonus | Category |
|---|---|---|---|---|
| `Exam 1` | 90 | 100 | 0 | `Exam` |
| `HW1` | 10 | 10 | 0 | `Homework` |
| `HW2` | 5 | 10 | 0 | `Homework` |

Then report, switch schemes with option `5`, and report again — without
re-entering anything:

1. Choose `2`. You should see `Grading: Points-based` and
   `1001  Ada                     87.5%   B` (105 ÷ 120).
2. Choose `5`, then `2` (Weighted). Choose `2` (Report):
   `Grading: Weighted` and `1001  Ada                     84.4%   B`
   (Exam 0.90 × 50 = 45; Homework 15/20 = 0.75 × 30 = 22.5; 67.5 ÷ 80).
3. Choose `5`, then `3` (Weighted, lowest dropped). Choose `2`:
   `1001  Ada                     93.8%   A`. Dropping HW2 leaves Homework at
   10/10, so (45 + 30) ÷ 80 = 93.75%.
4. Choose `6` (Quit).

Notice that in step 3 the report still says `Grading: Weighted`.
`WeightedDropLowest` inherits its name from `Weighted`'s constructor and does
not set its own — a small reminder that a derived class gets *everything* from
its base unless it overrides it.

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] `Gradebook::percentageFor` contains no `if` — the call goes through
      `scheme_->computePercentage`.
- [ ] `Gradebook` has a destructor that deletes `scheme_`, `setScheme`
      deletes the old scheme before storing the new one, and the copy
      constructor and copy assignment are `= delete`.
- [ ] `assignment.*`, `gradescale.*`, and `student.*` are unchanged from
      Chapter 20.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click all eleven project files to open them.
   Confirm the editor shows the expected file paths before editing.
4. Work through Steps 1–7 above in StudySite's internal editor, in order, clicking **Run** at each ▶ Run checkpoint.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — all eleven files. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 21 Grade Calculator v3.1**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 21
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
