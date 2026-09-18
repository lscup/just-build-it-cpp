# Chapter 21 Lab — Select Schemes with Polymorphism

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.1
- **Starting point:** The working Chapter 20 v3.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Make `GradingScheme::computePercentage` pure virtual and give the class a virtual destructor, so it can no longer be instantiated and every concrete scheme must supply its own rule.
2. Have `Gradebook` own a base-class `GradingScheme*` pointer and delegate every calculation through it — v3.0's `if (scheme_ == Scheme::Weighted)` branch is gone.
3. Because `Gradebook` now owns a raw pointer, write all three pieces of ownership bookkeeping that correctness requires: a destructor that deletes it, a `setScheme` that deletes the old scheme before installing the new one, and copy construction/assignment disabled.
4. Allow the user to switch schemes mid-session (a new menu option) without restarting or re-entering data; every report immediately reflects the new scheme.
5. Add `WeightedDropLowest` as a third scheme, inheriting from `Weighted`, without editing `Student`, `Assignment`, `GradeScale`, or the report code — and give it its own name so it never reports as plain "Weighted" in menu or report output despite grading differently.
6. Extend the Chapter 15 file format so the active scheme and its category weights persist, and reload as the correct concrete scheme — reached only through virtuals on `GradingScheme`, never by adding a second branch inside `Gradebook` itself.
7. Carry the Chapter 15–20 features forward onto the polymorphic `Gradebook`: saving/loading, the regression-test suite, checked access (`at()`), and sort/search all still need to work no matter which scheme is active.

Item 7 is the one most worth double-checking, exactly as in every chapter since 18: it is easy, while making the scheme polymorphic, to carry forward only the report and quietly lose the rest.

## What changes from Chapter 20

- **The branch moves out of the calculation entirely.** v3.0's `percentageFor()` asked `if (scheme_ == Scheme::Weighted)` on every call. v3.1's asks nothing — `scheme_->computePercentage(...)` lets the object decide. The only branch left anywhere is the one-time choice of *which object to construct*, in `chooseScheme()`.
- **`Gradebook` now owns a pointer, not two value members.** v3.0 kept both a `points_` and a `weighted_` member and picked one. v3.1 keeps one `GradingScheme*` and only ever has one scheme object alive. That gain requires the three pieces of hand-written bookkeeping in required-work item 3 — miss any one of them and the program leaks or double-frees.
- **Persisting the scheme can no longer be a hardcoded string.** v3.0's `save()` wrote `"POINTS"` or `"WEIGHTED"` directly, because `Gradebook` knew both concrete types by name. v3.1's `Gradebook` does not know `PointsBased`, `Weighted`, or `WeightedDropLowest` exist — so each scheme supplies its own `typeTag()` (a short string identifying it) and `weightsForSave()` (its category weights, or an empty list for a scheme that has none), and `Gradebook::save()`/`load()` call these two virtuals polymorphically. The chapter's own narrative says `chooseScheme()` is "the one place that names concrete types" — persistence needs a second one, a factory function that maps a saved tag back to a constructor. That factory lives in `main.cpp`, beside `chooseScheme()`, for the same reason: it is the file that is already allowed to know concrete scheme types exist.
- **`WeightedDropLowest` needs its own display name.** Simply inheriting `Weighted`'s constructor gives it the name `"Weighted"` too, so the menu would print `Grading is now: Weighted` for either scheme even though they compute different grades. `Weighted` gains a protected constructor that accepts a scheme name, and `WeightedDropLowest` uses it to report `"Weighted (lowest dropped)"` instead.
- **A saved gradebook's scheme is restored automatically, not re-prompted.** Prompting `chooseScheme()` unconditionally after a successful `load()` would silently throw away the scheme that was just loaded. The prompt now runs only when no save file was found; otherwise the program reports which scheme it loaded and reminds the user which menu option changes it.
- **The menu grows to ten options**, which breaks the single-character `choice[0]` comparison every chapter since 18 has used — `"10"[0]` is `'1'`, so a two-digit choice would silently be misread as option 1. The menu now reads and compares the whole line instead of just its first character.
- **The regression suite grows by one check, in two parts.** Both are new to this chapter: one confirms that calling `computePercentage` through a `GradingScheme*` really does reach `WeightedDropLowest`'s override rather than the base, and a worked numeric example confirms the drop-lowest arithmetic itself.

Everything else genuinely carries over: `GradeScale`, `Student`, `Assignment`, and the report's `operator<<` layout are unchanged from Chapter 20 — exactly the point the chapter's "What did not change" table makes.

## Build it: step by step

### Step 1 — Make `GradingScheme` abstract, and add the two virtuals persistence needs

```cpp
class GradingScheme {
public:
    explicit GradingScheme(const std::string& name) : name_(name) {}
    virtual ~GradingScheme() = default;

    /** Computes the course percentage. Every scheme defines its own rule. */
    virtual double computePercentage(const std::vector<Assignment>& work) const = 0;

    /** A short tag identifying the concrete scheme, for persistence. */
    virtual std::string typeTag() const = 0;

    /** Category weights as (name, weight) pairs, for a scheme that has them;
     *  empty for a scheme that does not. Used only for persistence. */
    virtual std::vector<std::pair<std::string, double>> weightsForSave() const { return {}; }

    const std::string& name() const { return name_; }

protected:
    static double finalize(double rawPercentage);

private:
    std::string name_;
};
```

`computePercentage` and `typeTag` are pure virtual, so `GradingScheme` cannot be instantiated. `weightsForSave` has a default body returning an empty list, because `PointsBased` has no weights to save — only `Weighted` needs to override it. The destructor is virtual because `Gradebook` will delete through a `GradingScheme*`; without `virtual` here, only the base part of a `Weighted` or `WeightedDropLowest` object would be destroyed.

### Step 2 — Give `Weighted` a name that a subclass can override

```cpp
class Weighted : public GradingScheme {
public:
    struct CategoryWeight {
        std::string name;
        double weight = 0.0;
    };

    Weighted();
    explicit Weighted(const std::vector<CategoryWeight>& weights);

    double computePercentage(const std::vector<Assignment>& work) const override;
    std::string typeTag() const override { return "WEIGHTED"; }
    std::vector<std::pair<std::string, double>> weightsForSave() const override;

    const std::vector<CategoryWeight>& weights() const { return weights_; }
    double weightTotal() const;
    bool weightsValid() const;

protected:
    // Lets WeightedDropLowest report its own name() instead of inheriting
    // "Weighted" unchanged - the two schemes must never look identical in
    // menu output even though one is built from the other.
    Weighted(const std::string& schemeName, const std::vector<CategoryWeight>& weights);

    std::vector<CategoryWeight> weights_;
};
```

```cpp
Weighted::Weighted() : GradingScheme("Weighted") {
    weights_ = { {"Exam", 50.0}, {"Homework", 30.0}, {"Participation", 20.0} };
}

Weighted::Weighted(const std::vector<CategoryWeight>& weights)
    : GradingScheme("Weighted"), weights_(weights) {}

Weighted::Weighted(const std::string& schemeName, const std::vector<CategoryWeight>& weights)
    : GradingScheme(schemeName), weights_(weights) {}

std::vector<std::pair<std::string, double>> Weighted::weightsForSave() const {
    std::vector<std::pair<std::string, double>> result;
    for (const CategoryWeight& w : weights_) { result.push_back({w.name, w.weight}); }
    return result;
}
```

`computePercentage`'s body is unchanged from Chapter 20. The new protected constructor exists only so `WeightedDropLowest` (Step 3) can supply its own name while still reusing every other line of `Weighted`.

### Step 3 — Add `WeightedDropLowest` as a third scheme

```cpp
class WeightedDropLowest : public Weighted {
public:
    WeightedDropLowest();
    explicit WeightedDropLowest(const std::vector<CategoryWeight>& weights);
    double computePercentage(const std::vector<Assignment>& work) const override;
    std::string typeTag() const override { return "WEIGHTED_DROP_LOWEST"; }
};
```

```cpp
WeightedDropLowest::WeightedDropLowest()
    : Weighted("Weighted (lowest dropped)",
               { {"Exam", 50.0}, {"Homework", 30.0}, {"Participation", 20.0} }) {}

WeightedDropLowest::WeightedDropLowest(const std::vector<CategoryWeight>& weights)
    : Weighted("Weighted (lowest dropped)", weights) {}

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

This required no change to `Gradebook`, `Student`, `GradeScale`, `Assignment`, or the report code — only a new class, reusing `weights_` because Chapter 20 already made it `protected` for exactly this purpose. `weightsForSave()` is inherited from `Weighted` unchanged: only `typeTag()` needs its own override, so persistence needed no new code either.

### Step 4 — Make `Gradebook` own a `GradingScheme*`, correctly

```cpp
using SchemeFactory = GradingScheme* (*)(const std::string& tag,
                                         const std::vector<Weighted::CategoryWeight>& weights);

explicit Gradebook(const std::string& courseName = "Untitled Course");
~Gradebook();

// Copying is disabled: Gradebook owns a raw pointer, and a default copy
// would leave two objects deleting the same scheme. Chapter 22 replaces
// this restriction with smart-pointer ownership.
Gradebook(const Gradebook&) = delete;
Gradebook& operator=(const Gradebook&) = delete;

void setScheme(GradingScheme* scheme);
double percentageFor(const Student& s) const;
std::string schemeName() const;
```

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

All three pieces of ownership bookkeeping from required-work item 3 are here: the destructor, the delete-before-replace inside `setScheme`, and the deleted copy operations. `percentageFor` no longer asks which scheme it has — there is nothing left to ask.

### Step 5 — Persist through the base class; reconstruct through a factory

```cpp
bool Gradebook::save(const std::string& filename) const {
    std::ofstream out(filename);
    if (!out) { return false; }

    out << "# Grade Calculator gradebook file, version 4 (Chapter 21)\n";
    out << "# Section tags allow new record types to be added later.\n";
    out << "COURSE," << courseName_ << "\n";
    out << "SCHEME," << scheme_->typeTag() << "\n";
    out << "NEXTID," << nextId_ << "\n";
    for (const GradeScale::Tier& t : scale_.tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (const auto& w : scheme_->weightsForSave()) {
        out << "WEIGHT," << w.first << "," << w.second << "\n";
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

`save()` never writes `"POINTS"`, `"WEIGHTED"`, or `"WEIGHTED_DROP_LOWEST"` as a literal — it calls `scheme_->typeTag()` and iterates `scheme_->weightsForSave()`, both reached only through the `GradingScheme` base. `load()` collects the tag and any weight lines while parsing, the same way it always has for other fields, and reconstructs the scheme once at the end:

```cpp
bool Gradebook::load(const std::string& filename, std::string& message, SchemeFactory makeScheme) {
    // ... parses COURSE, NEXTID, TIER, STUDENT exactly as Chapter 20 did ...
    // ... also collects: loadedTag from a SCHEME line, loadedWeights from WEIGHT lines ...

    setScheme(makeScheme(loadedTag, loadedWeights));
    roster_ = loadedRoster;
    nextId_ = loadedNextId;
    // ...
}
```

`makeScheme` is not a member of `Gradebook` — it is passed in as a `SchemeFactory` function pointer, defined in `main.cpp`:

```cpp
GradingScheme* makeScheme(const std::string& tag, const std::vector<Weighted::CategoryWeight>& weights) {
    if (tag == "WEIGHTED_DROP_LOWEST") {
        return weights.empty() ? new WeightedDropLowest() : new WeightedDropLowest(weights);
    }
    if (tag == "WEIGHTED") {
        return weights.empty() ? new Weighted() : new Weighted(weights);
    }
    return new PointsBased();
}
```

This is the second — and only other — place in the whole program that names `PointsBased`, `Weighted`, and `WeightedDropLowest` directly. `Gradebook` itself never does.

### Step 6 — Carry checked access and sort/search forward, unchanged in shape

```cpp
/** Checked access: throws std::out_of_range for an invalid index. */
const Student& at(std::size_t index) const { return roster_.at(index); }

void sortRoster(SortKey key);
int linearFindById(int id, int& comparisons) const;
int binaryFindById(int id, int& comparisons) const;
```

`sortRoster`'s `SortKey::Percentage` case still calls `percentageFor(roster_[j])`, so it stays scheme-aware no matter which `GradingScheme` is active; `linearFindById`, `binaryFindById`, and `at()` are otherwise byte-for-byte what Chapter 20 had.

### Step 7 — Rebuild `main`: a `makeScheme` factory, a load-first startup, and a ten-item menu

`chooseScheme()` itself is unchanged from Chapter 20 — it is still the only place a fresh session's choice constructs a scheme:

```cpp
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

But it now runs only when nothing was loaded:

```cpp
Gradebook book("Programming Fundamentals");
std::string message;
bool loaded = book.load(DEFAULT_FILE, message, makeScheme);
std::cout << message << (loaded ? "\n" : " Starting a new gradebook.\n");
std::cout << "  " << book.scale() << "\n";

if (loaded) {
    std::cout << "Loaded grading scheme: " << book.schemeName()
              << " (use menu option 5 to change it)\n";
} else {
    std::cout << "Select a grading scheme:\n";
    chooseScheme(book);
}
```

The menu adds "Change scheme" as option 5 and "Quit" moves to option 10, which means every choice must now be compared as a whole line, not `line[0]`:

```cpp
std::cout << "\n1) Add student  2) Report  3) Sort  4) Custom scale  5) Change scheme\n"
             "6) Save  7) Run tests  8) Sort roster  9) Find by ID  10) Quit\nChoice: ";
std::string line;
if (!std::getline(std::cin, line)) { break; }
// Two-digit choices ("10") need the whole line, not just line[0].
std::string c = line.empty() ? "?" : line;

if (c == "1") { /* Add student */ }
// ...
} else if (c == "5") {
    // Every existing student is regraded under the new rule. No data
    // is re-entered, and no other class knows this happened.
    chooseScheme(book);
} else if (c == "10") {
    running = false;
}
```

Comparing `c == "1"` through `c == "10"` as full strings is what makes `"10"` behave as Quit instead of being misread as `"1"`, Add student.

The regression suite's new check confirms both the polymorphism and the arithmetic:

```cpp
WeightedDropLowest dropLowest;
Student dropLowestExample("Test", 9999);
dropLowestExample.addAssignment(Assignment("Midterm", 80.0, 100.0, 0.0, "Exam"));  // kept, weight 50
dropLowestExample.addAssignment(Assignment("HW1", 5.0, 10.0, 0.0, "Homework"));    // 50%, dropped
dropLowestExample.addAssignment(Assignment("HW2", 10.0, 10.0, 0.0, "Homework"));   // 100%, kept
GradingScheme* asBase = &dropLowest;
check(asBase->computePercentage(dropLowestExample.assignments())
          == dropLowest.computePercentage(dropLowestExample.assignments()),
      "D6 a GradingScheme* dispatches to WeightedDropLowest, not the base");
check(dropLowest.computePercentage(dropLowestExample.assignments()) == 87.5,
      "D6 exam 80/100@50 + homework (HW1 dropped, HW2 kept)@30 is 87.5%");
```

## Verification

- With Exam 1 at 90/100, Homework 1 at 10/10, Homework 2 at 5/10, and category weights of 50 and 30, the three schemes report 87.5%, 84.4%, and 93.8% — matching the chapter's own worked example.
- Switching schemes with menu option 5 immediately recomputes every report, with no data re-entered.
- `Weighted` and `WeightedDropLowest` report different names ("Weighted" and "Weighted (lowest dropped)") even though one is built from the other.
- `Gradebook::percentageFor` and `Gradebook::save`/`load` contain no type-selection branch — `PointsBased`, `Weighted`, and `WeightedDropLowest` are named only in `chooseScheme()` and `makeScheme()`, both in `main.cpp`.
- Saving, quitting, and relaunching restores the course name, roster, grade scale, and the exact concrete scheme that was active — including a `WeightedDropLowest` gradebook, which must reload as `WeightedDropLowest`, not plain `Weighted`.
- A gradebook loaded from a file is not re-prompted for a scheme at startup; a fresh gradebook with no save file still is.
- `Run tests` should report **13 of 13 checks passed**.
- `Sort`, `Sort roster`, `Find by ID`, and checked access (`at()`) all still work under any of the three schemes.

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
git commit -m "Complete Chapter 21 Grade Calculator v3.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 21 checkpoint.
- The commit is pushed to GitHub.
