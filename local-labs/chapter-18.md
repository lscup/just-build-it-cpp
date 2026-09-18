# Chapter 18 Lab — Introduce Classes and Invariants

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.5
- **Starting point:** The working Chapter 17 v2.4 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Convert `Assignment`, `Student`, and `GradeScale` from structs to classes with private data members.
2. Merge the old `Score` struct into `Assignment`: an assignment now carries its own `pointsEarned`, `pointsPossible`, and `bonusPoints` directly, because each `Assignment` belongs to exactly one `Student` instead of being shared and indexed in parallel with a separate scores list.
3. Give `GradeScale` an invariant, enforced in its constructors: cutoffs strictly descend, no cutoff is negative, and the lowest tier is 0. An out-of-order or invalid tier is repaired or dropped, not rejected with an error — the constructor always produces a usable scale.
4. Add `Student::letterGrade(const GradeScale&) const`, which looks up the student's own `percentage()` on the given scale.
5. Add a **Custom scale** menu option that reads tiers from the user (highest first, `'done'` to finish) and replaces the active `GradeScale` by constructing a new one from what was entered — letting the invariant-enforcing constructor repair whatever the user typed.
6. Carry the Chapter 15–17 features forward onto the new classes: saving and loading the gradebook, the `runTests()` regression suite, and sorting/searching the roster all still need to work — update them to call the new class members instead of the old free functions, but do not drop them.

Item 6 is the one most worth double-checking. It is easy, while converting structs to classes, to rewrite `main` around the new `Student`/`GradeScale`/`Assignment` types and forget to carry every menu option across. Chapter 18 should still have all eight menu options Chapter 17 had, plus the new **Custom scale** option — nine total.

## What changes from Chapter 17

Three real structural changes come with the class conversion, not just renamed types:

- **The `Gradebook` struct is retired.** Chapter 17 grouped `assignments`, `roster`, `scale`, and `nextId` into one `Gradebook` struct passed around together. Chapter 18 has no equivalent struct — `main` now holds a `GradeScale scale`, a `std::vector<Student> roster`, and an `int nextId` as three separate local variables, and the free functions that touched a `Gradebook` (`saveGradebook`, `loadGradebook`) take these three directly as parameters instead.
- **The course-wide assignment list is retired.** Chapter 17 had one shared `std::vector<Assignment> assignments` that every student's `scores` lined up against by index. Chapter 18 has no shared list at all — each `Student` owns its own `std::vector<Assignment>`, added with `Student::addAssignment`. This removes the **Add assignment** menu option entirely; there is nothing course-wide left to add.
- **Assignments are entered per student, not once up front.** Because there is no shared assignment list, the workflow moves: when you choose **Add student**, you now enter that student's name and then loop entering that one student's assignments (name, points earned, points possible, bonus) before the student is added to the roster. This is a real workflow change, not just an implementation detail — the same *grading math* Chapter 17 used is still there, but the *sequence of prompts* a user sees is different, so "the same input reproduces the same run" is no longer literally true input-for-input. What must still match is the same percentage and letter grade for the same scores.
- **The gradebook file format changes to match.** The `ASSIGNMENT` record type is retired — there is no course-wide assignment list left to save. Each `STUDENT` row now carries its own assignment fields inline: `STUDENT,<id>,<name>,<assignmentName>,<earned>,<possible>,<bonus>`, repeated for every assignment that student has. A file saved by Chapter 17 is not compatible with Chapter 18's loader.

Everything else genuinely carries over: `readNonNegative` and `readLine` are untouched, the default A/B/C/D/F scale is unchanged, the report layout is unchanged, and the D1–D3 regression tests still check the exact same three defects with the exact same pass/fail wording.

## Build it: step by step

### Step 1 — Turn `Assignment` into a class, and fold `Score` into it

Chapter 17's `Assignment` only stored a name and a point value; the earned points and bonus lived in a separate `Score` struct, matched to an assignment by list position:

```cpp
// Chapter 17 (retired)
struct Assignment { std::string name; double pointsPossible = 0.0; };
struct Score      { double pointsEarned = 0.0; double bonusPoints = 0.0; };
```

Replace both with one class. Since an `Assignment` now belongs to a single `Student`, it can hold everything about itself:

```cpp
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

private:
    std::string name_;
    double pointsEarned_   = 0.0;
    double pointsPossible_ = 0.0;
    double bonusPoints_    = 0.0;
};
```

`Score` is deleted entirely — do not keep it around unused.

### Step 2 — Turn `GradeScale` into a class with an invariant-enforcing constructor

Chapter 17's grade scale was a `std::vector<GradeTier>` built by the free function `readGradeScale`, with no guarantee anything downstream actually validated it. Chapter 18 makes an invalid scale impossible to construct:

```cpp
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

    /**
     * Every non-negative percentage maps to a letter; a negative percentage
     * (which should never occur from real grading math, but a save file
     * could contain one) returns '?' rather than guessing.
     */
    char letterFor(double percentage) const {
        if (percentage < 0.0) { return '?'; }
        for (const Tier& t : tiers_) {
            if (percentage >= t.cutoff) { return t.letter; }
        }
        return '?';
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

`readGradeScale` and the old free-function `letterFor(pct, scale_vector)` are both retired. Validation now lives in exactly one place: the constructor.

### Step 3 — Turn `Student` into a class that owns its own assignments

```cpp
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

    /** Looks up this student's own letter grade on the given scale. */
    char letterGrade(const GradeScale& scale) const {
        return scale.letterFor(percentage());
    }

private:
    std::string name_;
    int id_ = 0;
    std::vector<Assignment> assignments_;
};
```

Notice `percentage()` takes no parameters — Chapter 17's `percentageOf(student, assignments)` needed the shared assignment list passed in; Chapter 18's `Student` has everything it needs about itself.

### Step 4 — Update persistence for the new per-student format

`splitCsv` does not change. `saveGradebook` and `loadGradebook` do: they no longer take a `Gradebook`, and each `STUDENT` row now carries its assignment fields inline instead of matching against a separate `ASSIGNMENT` section:

```cpp
bool saveGradebook(const GradeScale& scale, const std::vector<Student>& roster,
                   int nextId, const std::string& filename) {
    std::ofstream out(filename);
    if (!out) { return false; }

    out << "# Grade Calculator gradebook file, version 2 (Chapter 18)\n";
    out << "# Section tags allow new record types to be added later.\n";
    out << "NEXTID," << nextId << "\n";
    for (const GradeScale::Tier& t : scale.tiers()) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (const Student& s : roster) {
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

```cpp
bool loadGradebook(GradeScale& scale, std::vector<Student>& roster, int& nextId,
                   const std::string& filename, std::string& message) {
    std::ifstream in(filename);
    if (!in) {
        message = "No file named '" + filename + "' was found.";
        return false;
    }

    std::vector<GradeScale::Tier> loadedTiers;
    std::vector<Student> loadedRoster;
    int loadedNextId = 1001;
    std::string line;
    int lineNumber = 0;
    while (std::getline(in, line)) {
        ++lineNumber;
        if (line.empty() || line[0] == '#') { continue; }
        std::vector<std::string> f = splitCsv(line);
        if (f.empty()) { continue; }

        try {
            if (f[0] == "NEXTID" && f.size() >= 2) {
                loadedNextId = std::stoi(f[1]);
            } else if (f[0] == "TIER" && f.size() >= 3) {
                loadedTiers.push_back({std::stod(f[1]), f[2].empty() ? '?' : f[2][0]});
            } else if (f[0] == "STUDENT" && f.size() >= 3) {
                Student s(f[2], std::stoi(f[1]));
                for (std::size_t i = 3; i + 3 < f.size(); i += 4) {
                    s.addAssignment(Assignment(f[i], std::stod(f[i + 1]),
                                               std::stod(f[i + 2]), std::stod(f[i + 3])));
                }
                loadedRoster.push_back(s);
            } else {
                message = "Unrecognized record on line " + std::to_string(lineNumber)
                        + "; the rest of the file was still loaded.";
            }
        } catch (...) {
            message = "Malformed number on line " + std::to_string(lineNumber)
                    + "; that record was skipped.";
        }
    }

    scale = loadedTiers.empty() ? GradeScale() : GradeScale(loadedTiers);
    if (loadedTiers.empty()) {
        message = "File had no grade scale; the default scale was used.";
    }
    roster = loadedRoster;
    nextId = loadedNextId;
    if (message.empty()) { message = "Loaded " + filename + "."; }
    return true;
}
```

The `ASSIGNMENT` record type from Chapter 17's file format is gone — do not write or read it.

### Step 5 — Update the regression tests to exercise the classes

Same three defects (D1, D2, D3), same pass/fail text, now checked through the class API instead of the old free functions:

```cpp
void runTests() {
    std::cout << "\n--- Regression tests ---\n";
    GradeScale scale;

    // D3: exactly at a cutoff must take the higher grade.
    check(scale.letterFor(90.0) == 'A', "D3 90.0 is an A, not a B");
    check(scale.letterFor(80.0) == 'B', "D3 80.0 is a B, not a C");
    check(scale.letterFor(60.0) == 'D', "D3 60.0 is a D, not an F");

    // D1: a percentage below every cutoff must not read past the end.
    check(scale.letterFor(0.0)  == 'F', "D1 0.0 is an F, no out-of-range read");
    check(scale.letterFor(-5.0) == '?', "D1 below scale returns '?', no crash");

    // D2: bonus raises earned points only, never points possible.
    Student withBonus("Test", 9999);
    withBonus.addAssignment(Assignment("HW1", 8.0, 10.0, 2.0));  // 8 earned + 2 bonus of 10
    check(withBonus.percentage() == 100.0, "D2 8+2 bonus of 10 is 100%, not 83.3%");

    Student noBonus("Test", 9999);
    noBonus.addAssignment(Assignment("HW1", 8.0, 10.0, 0.0));
    check(noBonus.percentage() == 80.0, "D2 8 of 10 with no bonus is 80%");

    // Boundary: an assignment worth zero points must not divide by zero.
    Student zeroPoints("Test", 9999);
    zeroPoints.addAssignment(Assignment("Ungraded", 0.0, 0.0, 0.0));
    check(zeroPoints.percentage() == 0.0, "zero points possible does not crash");

    std::cout << "  " << (checksRun - checksFailed) << " of " << checksRun
              << " checks passed.\n\n";
    checksRun = 0;
    checksFailed = 0;
}
```

`check` and the `checksRun`/`checksFailed` counters are unchanged from Chapter 16.

### Step 6 — Update sorting and searching to compare `Student` objects directly

Chapter 17's `StudentComparer` took the shared assignment list as a third parameter, because `percentageOf` needed it. Chapter 18's comparers do not, because `Student::percentage()` is self-contained:

```cpp
typedef bool (*StudentComparer)(const Student&, const Student&);

bool byName(const Student& a, const Student& b) { return a.name() < b.name(); }
bool byId(const Student& a, const Student& b)   { return a.id() < b.id(); }
bool byPercentageDescending(const Student& a, const Student& b) {
    return a.percentage() > b.percentage();
}

/** Selection sort: same algorithm as Chapter 17, now comparing Students directly. */
void selectionSort(std::vector<Student>& roster, StudentComparer comesFirst) {
    for (std::size_t i = 0; i + 1 < roster.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < roster.size(); ++j) {
            if (comesFirst(roster[j], roster[best])) { best = j; }
        }
        if (best != i) { std::swap(roster[i], roster[best]); }
    }
}
```

`linearSearchById` and `binarySearchById` keep the exact same bodies as Chapter 17 — only the call `roster[i].id` becomes `roster[i].id()`, since `id` is now a private member reached through an accessor. Binary search still runs against a sorted **copy** of the roster, never the live one, exactly as in Chapter 17.

### Step 7 — Rebuild `main`: retire `Gradebook`, add the Custom scale option

The `Gradebook` struct is gone. `main` now holds three separate variables, loads them on startup, and saves them on exit — unchanged from Chapter 15's persistence pattern:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v2.5 (classes) ===\n\n";

    GradeScale scale;   // default scale; invariant guaranteed by construction
    std::vector<Student> roster;
    int nextId = 1001;

    std::string message;
    if (loadGradebook(scale, roster, nextId, DEFAULT_FILE, message)) {
        std::cout << message << "\n\n";
    } else {
        std::cout << message << " Starting a new gradebook.\n\n";
    }
    scale.describe();
```

The menu drops **Add assignment** (there is nothing course-wide left to add) and gains **Custom scale**:

```cpp
    std::cout << "\n1) Add student  2) Report  3) Custom scale  4) Save\n"
                 "5) Run tests  6) Sort roster  7) Find by ID  8) Quit\nChoice: ";
```

**Add student** now loops entering that student's own assignments before adding them to the roster:

```cpp
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
```

**Custom scale** is new — it reads tiers the same way Chapter 14's `readGradeScale` did, but instead of validating them by hand, it hands whatever was entered to the `GradeScale` constructor and lets the invariant repair it:

```cpp
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
```

**Report**, **Save**, **Run tests**, **Sort roster**, and **Find by ID** keep the same menu positions and output shape as Chapter 17 — they now just call the class members (`printReport(roster, scale)`, `s.letterGrade(scale)`, and so on) instead of the old free functions.

## Verification

- Code outside a class cannot modify `Assignment`, `Student`, or `GradeScale` data directly — every field is private.
- Building a `GradeScale` from ascending, negative, empty, or floor-missing tiers always produces a valid, usable scale; nothing crashes or throws.
- For the same scores, a student's reported percentage and letter grade match the same math Chapter 17 used — verify this by comparing a report you already have from Chapter 17 against the same scores entered in Chapter 18.
- Saving, quitting, and relaunching reloads the roster with matching IDs, names, scores, and percentages.
- `Run tests` still reports **8 of 8 checks passed**.
- `Sort roster` and `Find by ID` still work, including the linear-vs-binary comparison counts on **Find by ID**.
- All accessors that do not change an object are `const`.

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
git commit -m "Complete Chapter 18 Grade Calculator v2.5"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 18 checkpoint.
- The commit is pushed to GitHub.
