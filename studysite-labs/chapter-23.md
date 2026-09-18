# Chapter 23 Lab — Add Generic Statistics and an ID Index

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.3
- **Starting point:** The working Chapter 22 v3.2 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create header-only `Statistics<T>` with `mean`, `median`, `lowest`, `highest`, and population `standardDeviation`, all computed over any numeric type `T`.
2. Add a `std::map<int, std::size_t>` index from student ID to roster position, and maintain it whenever the roster changes order.
3. Add `findById` using the index, in O(log n) instead of Chapter 17's O(n) linear or O(log n)-after-an-O(n)-sort binary search.
4. Replace the implicit `Student` ordering with a lambda at the sort call, so the ordering is stated where it is used rather than relied on from `operator<` everywhere.
5. Add class statistics, letter-grade distribution, and assignment count by category to the report, all using the `std::map` counting idiom (`++counts[key]`).
6. Carry the Chapter 15–22 features that this chapter's own architecture does not replace forward onto the templated, indexed `Gradebook`: saving/loading and the regression-test suite.

Item 6 is the one most worth double-checking, exactly as in every chapter since 18 — but read "What changes from Chapter 22" below first, because this chapter deliberately retires two carried-forward pieces rather than silently dropping them.

## What changes from Chapter 22

- **The Chapter 17 selection sort and its comparison-count exercise are retired, not dropped.** `sortRoster(SortKey)`, `linearFindById`, and `binaryFindById` do not appear in v3.3. This is the chapter's own point, stated directly: "Compare with Chapter 17. The binary search needed the roster sorted by ID, so searching meant sorting a copy first — and any change to the roster invalidated the assumption. **The map maintains itself.**" `findById` using `std::map` replaces both linear and binary search outright; there is no longer a hand-written algorithm to compare against.
- **Chapter 19's checked access (`at()`) is retired too, deliberately.** `findById` returns `nullptr` for "not found" — the same convention, and the same weakness, Chapter 17's search functions had. The chapter says so directly: "Returning `nullptr` for 'not found' is the same convention Chapter 17 used, with the same weakness: a caller who forgets to check will dereference it. **Chapter 24 replaces it.**" Index-based bounds checking is not this chapter's concern; exception-based error handling is Chapter 24's, on purpose.
- **An index is derived data, and it must be rebuilt everywhere the roster's order or positions change.** `addStudent` updates `idIndex_` incrementally; `sortByPercentage` — and `load`, since Chapter 15 — must rebuild it from scratch afterward, because sorting moves *every* student and reloading replaces the roster outright. Forgetting either rebuild is a silent logic error: the program keeps running, and `findById` starts returning the wrong student, or the right student's stale data.
- **Sorting now takes a lambda instead of relying on `Student::operator<`.** `sortByPercentage()`'s ordering — "by `percentageFor`, descending" — is stated once, at the one call site that needs it, rather than baked into `Student` as a general-purpose comparison that every caller has to trust means the same thing.
- **Persistence's design is unaffected by any of this.** `typeTag()`/`weightsForSave()`/`SchemeFactory` still let `Gradebook::save()`/`load()` handle any concrete `GradingScheme` without naming one; `idIndex_` itself is never written to or read from the file, because it is derived data — `load()` rebuilds it from the loaded roster the same way `sortByPercentage()` rebuilds it after a sort.
- **The regression suite grows by four checks**, all new to this chapter: `Statistics<double>` and `Statistics<int>` each exercised and checked against a hand calculation, the category-count tally, and — the one the lab's own verification list calls out by name — a check that `findById` is still correct for every ID after a sort. That last check is written so that deleting the `idIndex_` rebuild inside `sortByPercentage()` makes it fail; it is not a general assertion, it is a trap for that specific bug.

## Build it: step by step

### Step 1 — Write `Statistics<T>` as a header-only class template

```cpp
// statistics.h
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
```

Because it is a template, `Statistics` lives entirely in its header — a template's definition has to be visible everywhere it is instantiated, so there is no `statistics.cpp`. The Grade Calculator only ever instantiates `Statistics<double>`, but the class itself does not know that; `Statistics<int>` works identically, which is exactly what the regression suite exercises.

### Step 2 — Add the ID index and keep it current in `addStudent`

```cpp
// gradebook.h
#include <map>
// ...
private:
    // An index from student ID to roster position. std::map keeps its keys
    // sorted and looks up in logarithmic time, replacing the hand-written
    // binary search of Chapter 17 - and it stays correct as students are
    // added, as long as every operation that moves a student rebuilds it.
    std::map<int, std::size_t> idIndex_;
```

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
    idIndex_[s.id()] = roster_.size() - 1;
}
```

A new student is always appended, so its position is always `roster_.size() - 1` at the moment it is added — no existing entry moves, so no rebuild is needed here.

### Step 3 — Add `findById`, and a private `rebuildIndex()` helper for everywhere else

```cpp
const Student* Gradebook::findById(int id) const {
    auto it = idIndex_.find(id);
    if (it == idIndex_.end()) { return nullptr; }
    return &roster_[it->second];
}
```

```cpp
void Gradebook::rebuildIndex() {
    idIndex_.clear();
    for (std::size_t i = 0; i < roster_.size(); ++i) {
        idIndex_[roster_[i].id()] = i;
    }
}
```

`rebuildIndex()` is `private` — it is an internal consistency mechanism, not something a caller should ever need to invoke directly. Every public operation that could move a student calls it itself.

### Step 4 — Sort with a lambda, and rebuild the index afterward

```cpp
void Gradebook::sortByPercentage() {
    // A lambda states the ordering right where it is used, instead of relying
    // on operator< to mean "by percentage, descending" everywhere.
    const Gradebook* self = this;
    std::sort(roster_.begin(), roster_.end(),
              [self](const Student& a, const Student& b) {
                  return self->percentageFor(a) > self->percentageFor(b);
              });
    // Sorting moved every student, so the ID index must be rebuilt. An index
    // is derived data, and derived data goes stale: skip this line and
    // findById() starts returning the wrong student after any sort.
    rebuildIndex();
}
```

The lambda captures `self` — a `const Gradebook*` pointing at `this` — because the comparison needs `percentageFor`, a member function, and there is no other way for the lambda to reach it. Capturing the pointer explicitly, rather than the terser `[this]`, makes that dependency visible at the call site.

### Step 5 — Add letter distribution and assignment count by category, with the same counting idiom

```cpp
std::map<char, int> Gradebook::letterDistribution() const {
    std::map<char, int> counts;
    for (const Student& s : roster_) {
        ++counts[scale_.letterFor(percentageFor(s))];   // missing keys start at 0
    }
    return counts;
}

std::map<std::string, int> Gradebook::assignmentCountByCategory() const {
    std::map<std::string, int> counts;
    for (const Student& s : roster_) {
        for (const Assignment& a : s.assignments()) {
            ++counts[a.category()];   // missing keys start at 0, same pattern
        }
    }
    return counts;
}
```

`operator[]` on a `std::map` inserts a default-constructed value (`0` for `int`) the first time a key is seen, so `++counts[key]` is a complete, correctly-initialized tally in one line — no separate check for "have I seen this key before."

### Step 6 — Add class statistics to the report

```cpp
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

    out << "  Categories: ";
    for (const auto& entry : assignmentCountByCategory()) {
        out << entry.first << "=" << entry.second << "  ";
    }
    out << "\n";
}
```

`std::map` iterates in sorted key order for free, so both the grade distribution and the category tally print alphabetically (or, for letters, gradewise) with no separate sort step.

### Step 7 — Carry persistence forward; `idIndex_` is rebuilt, never saved

`save()` is untouched line for line from Chapter 22 — it never mentions `idIndex_`, because the index is derived data, not part of the gradebook's real state. `load()` gains exactly one new line, at the very end:

```cpp
bool Gradebook::load(const std::string& filename, std::string& message, SchemeFactory makeScheme) {
    // ... parses COURSE, SCHEME, NEXTID, TIER, WEIGHT, STUDENT exactly as Chapter 22 did ...

    courseName_ = loadedCourse;
    scale_ = loadedTiers.empty() ? GradeScale() : GradeScale(loadedTiers);
    setScheme(makeScheme(loadedTag, loadedWeights));
    roster_ = loadedRoster;
    nextId_ = loadedNextId;
    rebuildIndex();   // idIndex_ is derived data; the file never stores it directly.
    if (message.empty()) { message = "Loaded " + filename + "."; }
    return true;
}
```

`roster_ = loadedRoster;` replaces every student's position at once, exactly like a sort does, so it needs exactly the same rebuild.

### Step 8 — Update the menu and regression suite

The menu drops "Sort roster" and "Find by ID"'s old comparison-count output, gains "Statistics", and keeps "Save" and "Run tests" — ten options again, so choices are still compared as whole strings:

```cpp
std::cout << "\n1) Add student  2) Report  3) Sort  4) Custom scale  5) Change scheme\n"
             "6) Statistics  7) Find by ID  8) Save  9) Run tests  10) Quit\nChoice: ";
```

The regression suite's four new checks:

```cpp
// Chapter 23: Statistics<double>, matching the chapter's own worked
// example by hand: 95, 75, 55 -> mean 75.0, median 75.0, range 55-95,
// population standard deviation sqrt(800/3) ~= 16.3.
Statistics<double> pctStats;
pctStats.add(95.0);
pctStats.add(75.0);
pctStats.add(55.0);
check(pctStats.mean() == 75.0, "D7 Statistics<double> mean of 95,75,55 is 75.0");
// ... median, range, and standard deviation checked the same way ...

// Chapter 23: the same template at a different type - Statistics<int>.
Statistics<int> pointStats;
pointStats.add(80);
pointStats.add(90);
pointStats.add(100);
check(pointStats.mean() == 90, "D8 Statistics<int> mean of 80,90,100 is 90");
// ...

// Chapter 23: assignment count by category, the counting-with-a-map idiom.
// ... build a Gradebook with two Exam assignments and one Homework assignment ...
check(categoryCounts["Exam"] == 2 && categoryCounts["Homework"] == 1,
      "D9 assignment count by category tallies Exam=2, Homework=1");

// Chapter 23: ID lookup must survive a sort. Delete the rebuildIndex() call
// inside sortByPercentage() and this check starts failing.
// ... build a Gradebook with three students, sort it, then look each ID up ...
check(foundAlice != nullptr && foundAlice->name() == "Alice"
          && foundBob != nullptr && foundBob->name() == "Bob"
          && foundCarol != nullptr && foundCarol->name() == "Carol",
      "D10 findById is still correct for every ID after sortByPercentage");
```

## Verification

- `Statistics<double>` and `Statistics<int>` are both exercised — `Run tests` checks each one against a hand calculation.
- Three students at 95%, 75%, and 55% report **Mean 75.0%, Median 75.0%, Range 55.0% to 95.0%, Std dev 16.3** — check this by hand: deviations from the mean are +20, 0, −20; squares 400, 0, 400; mean square 800/3 ≈ 266.67; square root ≈ 16.33.
- ID lookup (**Find by ID**) works both before and after **Sort**.
- Deleting the `rebuildIndex()` call inside `sortByPercentage()` makes `Run tests` fail — specifically the D10 check — confirming the test actually catches the bug it claims to.
- The letter-grade distribution and the assignment count by category both print in sorted key order with no separate sort step.
- Saving, quitting, and relaunching still restores the exact concrete scheme that was active, and `findById` still works correctly afterward even though `idIndex_` itself was never written to the file.
- `Run tests` should report **21 of 21 checks passed**.
- Chapter 17's `sortRoster`/`linearFindById`/`binaryFindById` and Chapter 19's `at()` are gone on purpose — `findById` and the lambda-driven `sortByPercentage` are what replaced them, not an oversight.

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
4. Enter the commit message **Complete Chapter 23 Grade Calculator v3.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 23
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
