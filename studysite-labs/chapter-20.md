# Chapter 20 Lab — Add Weighted Grading with Inheritance

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.0
- **Starting point:** The working Chapter 19 v2.6 multi-file program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add a `category` parameter to `Assignment`, defaulted to `"Uncategorized"`, so every existing constructor call still compiles unchanged.
2. Create a `GradingScheme` base class and `PointsBased` and `Weighted` derived classes.
3. Move the shared cap-and-round policy (`finalize`) into the base class so neither derived class repeats it.
4. Give `Weighted` a `weightsValid()` that checks whether its category weights total 100 within a floating-point tolerance (`std::abs(weightTotal() - 100.0) < 0.001`) — but see "What changes from Chapter 19" below for what happens when they don't.
5. Let the user choose the grading scheme (points-based or weighted) at startup, through `Gradebook`'s constructor.
6. Do not penalize a student for a weighted category with no graded assignments yet: skip it, and redistribute its weight across the categories that do have work.
7. Carry the Chapter 15–19 features forward onto the scheme-aware `Gradebook`: saving and loading, the regression-test suite, checked access, and sort/search all still need to work under either scheme.

Item 7 is the one most worth double-checking, as in the last two chapters: it is easy, while adding a second grading scheme, to carry forward only the report and quietly lose the rest.

## What changes from Chapter 19

- **"Validate" means detect and warn, not reject.** Item 4's `weightsValid()` is a query, not a gate — `Gradebook::setWeights` accepts whatever weights it is given, valid or not. This lab's own verification list once said "weights totaling 80% are rejected," which is not what the reference program does or should do: dividing by `weightTotal()` (the weight actually used) rather than by a hardcoded 100 already normalizes correctly no matter what the weights sum to, so there is nothing to reject. Report the total to the user with `weightsValid()` when it looks wrong; do not block the run.
- **Two independent sort mechanisms now sit on top of two grading schemes.** `Gradebook::sortByPercentage()` (Chapter 19's `operator<`) always orders by `Student`'s raw points-based `percentage()`, regardless of which scheme is active. `Gradebook::sortRoster(SortKey::Percentage)` (the Chapter 17 selection sort, carried forward again this chapter) uses `percentageFor()` — the scheme-aware grade the report actually shows. Under `Weighted` grading these two can disagree on ordering. That is not a defect to fix in this chapter; it is a difference worth knowing about, because it is exactly the kind of thing Chapter 21's redesign will make easier to reason about.
- **The save file grows two new fields**: a `SCHEME` line (`POINTS` or `WEIGHTED`) and, for a weighted gradebook, one `WEIGHT` line per category. Loading a saved gradebook restores its scheme and its weights — including custom weights the user entered — rather than always falling back to the session's startup prompt. If the two disagree, the loaded file's scheme wins, and the program says so.
- **Each `STUDENT` row gains a fifth field per assignment**: the category. Chapter 19's four-field-per-assignment format (`name, earned, possible, bonus`) becomes five (`name, earned, possible, bonus, category`).
- **The regression suite grows by two checks.** Both are new to this chapter, and both come directly from required-work items 4 and 6: the documented 93.8% example (a 90/100 exam at weight 50 plus 10/10 homework at weight 30, with participation ungraded) and a check that an ungraded category's weight is redistributed rather than counted against the student.

Everything else genuinely carries over: `GradeScale`, `Student`, `Gradebook`'s report layout, and the D1–D3 defects' pass/fail wording are all unchanged from Chapter 19 — exactly the point the chapter's own "What did not change" table makes.

## Build it: step by step

### Step 1 — Add a category to `Assignment`, with a default

```cpp
class Assignment {
public:
    Assignment() = default;
    Assignment(const std::string& name, double earned, double possible,
               double bonus = 0.0, const std::string& category = "Uncategorized");
    // ...
    const std::string& category() const { return category_; }
    // ...
private:
    // ...
    std::string category_ = "Uncategorized";
};
```

Every call site from Chapters 13–19 that constructs an `Assignment` with three or four arguments still compiles: the new parameter defaults, so nothing already written breaks.

### Step 2 — Create `GradingScheme` and its two derived classes

```cpp
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

class PointsBased : public GradingScheme {
public:
    PointsBased() : GradingScheme("Points-based") {}
    double computePercentage(const std::vector<Assignment>& work) const;
};

class Weighted : public GradingScheme {
public:
    struct CategoryWeight {
        std::string name;
        double weight = 0.0;
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
```

`PointsBased::computePercentage` is the same total-earned-over-total-possible math every chapter since Chapter 14 has used, just moved into its own class:

```cpp
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
```

### Step 3 — Implement weighted grading, without penalizing ungraded categories

```cpp
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

Dividing by `weightUsed` — the weight actually seen, not a hardcoded 100 — is what makes weights that don't total 100 still produce a sane percentage, and what makes an ungraded category's weight vanish rather than count against the student.

### Step 4 — Make `Gradebook` scheme-aware

```cpp
enum class Scheme { Points, Weighted };

explicit Gradebook(const std::string& courseName = "Untitled Course",
                   Scheme scheme = Scheme::Points);

double percentageFor(const Student& s) const;
std::string schemeName() const;
Scheme scheme() const { return scheme_; }
const Weighted& weightedScheme() const { return weighted_; }
void setWeights(const std::vector<Weighted::CategoryWeight>& w) { weighted_ = Weighted(w); }
```

```cpp
double Gradebook::percentageFor(const Student& s) const {
    // The single branch. One place today; one place per operation as soon as
    // a third scheme or a second calculation is added.
    if (scheme_ == Scheme::Weighted) {
        return weighted_.computePercentage(s.assignments());
    }
    return points_.computePercentage(s.assignments());
}
```

Every place that used to call `s.percentage()` for the *course grade* now calls `book.percentageFor(s)` instead — the report, the class average, and (see Step 6) the scheme-aware sort key. `s.percentage()` itself is untouched and still used for the raw points-based ordering in `sortByPercentage()`.

### Step 5 — Carry persistence forward, with a `SCHEME` line and per-category `WEIGHT` lines

```cpp
bool Gradebook::save(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out) { return false; }

    out << "# Grade Calculator gradebook file, version 3 (Chapter 20)\n";
    out << "# Section tags allow new record types to be added later.\n";
    out << "COURSE," << courseName_ << "\n";
    out << "SCHEME," << (scheme_ == Scheme::Weighted ? "WEIGHTED" : "POINTS") << "\n";
    out << "NEXTID," << nextId_ << "\n";
    for (const GradeScale::Tier& t : scale_.tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    if (scheme_ == Scheme::Weighted) {
        for (const Weighted::CategoryWeight& w : weighted_.weights()) {
            out << "WEIGHT," << w.name << "," << w.weight << "\n";
        }
    }
    for (const Student& s : roster_) {
        out << "STUDENT," << s.id() << "," << s.name();
        for (const Assignment& a : s.assignments()) {
            out << "," << a.name() << "," << a.pointsEarned() << ","
                << a.pointsPossible() << "," << a.bonusPoints() << "," << a.category();
        }
        out << "\n";
    }
    return out.good();
}
```

`load` mirrors it: a `SCHEME` line sets `scheme_`, `WEIGHT` lines are collected and, if any were found, replace `weighted_` with `Weighted(loadedWeights)`; each `STUDENT` row's assignments are now read five fields at a time instead of four, with the fifth restoring `category()`.

### Step 6 — Carry sort/search forward, using the scheme-aware grade where it matters

```cpp
void Gradebook::sortRoster(SortKey key) {
    for (std::size_t i = 0; i + 1 < roster_.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < roster_.size(); ++j) {
            bool jComesFirst = false;
            switch (key) {
                case SortKey::Name:       jComesFirst = roster_[j].name() < roster_[best].name(); break;
                case SortKey::Percentage: jComesFirst = percentageFor(roster_[j]) > percentageFor(roster_[best]); break;
                case SortKey::Id:         jComesFirst = roster_[j].id() < roster_[best].id(); break;
            }
            if (jComesFirst) { best = j; }
        }
        if (best != i) { std::swap(roster_[i], roster_[best]); }
    }
}
```

Notice the `Percentage` case calls `percentageFor(roster_[j])`, not `roster_[j].percentage()`. `linearFindById` and `binaryFindById` are otherwise byte-for-byte what Chapter 19 had; only the printed percentage on a successful find changes, from `s.percentage()` to `book.percentageFor(s)`, so **Find by ID** reports the grade the active scheme actually produces.

### Step 7 — Rebuild `main`: choose a scheme, weigh in on weights, keep every menu option

```cpp
std::cout << "Grading scheme for this session:\n";
std::cout << "  1) Points-based   2) Weighted by category\n";
std::string choice = readLine("Choice: ");

Gradebook::Scheme requestedScheme = (!choice.empty() && choice[0] == '2')
                         ? Gradebook::Scheme::Weighted
                         : Gradebook::Scheme::Points;
Gradebook book("Programming Fundamentals", requestedScheme);

std::string message;
if (book.load(DEFAULT_FILE, message)) {
    std::cout << "\n" << message << "\n";
    if (book.scheme() != requestedScheme) {
        std::cout << "  Note: " << DEFAULT_FILE << " was saved under "
                  << (book.scheme() == Gradebook::Scheme::Weighted ? "weighted" : "points-based")
                  << " grading; using the saved scheme instead of tonight's choice.\n";
    }
} else {
    std::cout << "\n" << message << " Starting a new gradebook.\n";
}
```

A saved gradebook's scheme takes precedence over tonight's prompt, and the program says so rather than silently overriding the user's choice. If the active scheme is `Weighted`, the current weights — the loaded ones if a file existed, the defaults otherwise — are shown before offering to replace them:

```cpp
if (book.scheme() == Gradebook::Scheme::Weighted) {
    std::cout << "\nCurrent weights: ";
    for (const Weighted::CategoryWeight& w : book.weightedScheme().weights()) {
        std::cout << w.name << " " << w.weight << "   ";
    }
    std::cout << "\n";
    if (readLine("Enter your own weights? (y/n): ").substr(0, 1) == "y") {
        // ... unchanged from the original ...
    }
}
```

The menu itself is unchanged from Chapter 19 — all nine options carry forward, none of them new to this chapter:

```cpp
std::cout << "\n1) Add student  2) Report  3) Sort by grade  4) Custom scale  5) Save\n"
             "6) Run tests  7) Sort roster  8) Find by ID  9) Quit\nChoice: ";
```

**Add student** now also prompts for each assignment's category, defaulting to `"Uncategorized"` when left blank, matching the required default on the constructor itself.

The regression suite gains its two new checks — the documented weighted example, and the no-penalty-for-ungraded-categories rule:

```cpp
Weighted defaultWeights;
Student weightedExample("Test", 9999);
weightedExample.addAssignment(Assignment("Midterm", 90.0, 100.0, 0.0, "Exam"));
weightedExample.addAssignment(Assignment("HW1", 10.0, 10.0, 0.0, "Homework"));
check(defaultWeights.computePercentage(weightedExample.assignments()) == 93.8,
      "D4 exam 90/100@50 + homework 10/10@30 (no participation) is 93.8%");

Student redistribute("Test", 9999);
redistribute.addAssignment(Assignment("Midterm", 80.0, 100.0, 0.0, "Exam"));
redistribute.addAssignment(Assignment("Speech", 10.0, 10.0, 0.0, "Participation"));
// Homework (weight 30) has no assignments yet and must not count against the total.
check(defaultWeights.computePercentage(redistribute.assignments()) == 85.7,
      "D5 Weighted redistributes an ungraded category's weight, not penalizes it");
```

## Verification

- The existing points-based examples still produce the same grades as Chapter 19.
- A 90/100 exam at weight 50 and 10/10 homework at weight 30 reports 93.8% when only those categories contain work — `Run tests` checks this automatically now.
- Weights totaling 80% are **not** rejected: `weightsValid()` reports them as invalid and the program says so, but the percentage is still computed correctly because it divides by the weight actually used, not by a hardcoded 100.
- A weighted category with no assignments yet does not lower a student's grade — `Run tests` checks this automatically too, and should report **11 of 11 checks passed**.
- Saving, quitting, and relaunching restores the course name, roster, grade scale, chosen scheme, and (for a weighted gradebook) its category weights.
- `GradeScale`, `Student`, and the report layout are unchanged from Chapter 19, exactly as the "What did not change" table claims — verify this with a diff if you want to see it rather than take it on trust.
- `Sort by grade`, `Sort roster`, and `Find by ID` all still work under either scheme.


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
4. Enter the commit message **Complete Chapter 20 Grade Calculator v3.0**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 20
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
