# Chapter 18 — Classes and Objects

## Learning Objectives

When you finish this chapter you will be able to:

- Explain the difference between a class and an object. *(SLO 2.2)*
- Declare a class with private data and public member functions. *(SLO 2.2)*
- Explain encapsulation and why data members are private. *(SLO 2.2, 2.3)*
- Write constructors, including a default and a parameterized one. *(SLO 2.2)*
- Write accessors and mutators, and mark non-modifying functions `const`. *(SLO 2.2)*
- State a class invariant and enforce it in the constructor. *(SLO 2.2, 2.8)*
- Identify candidate classes from a requirements statement. *(SLO 2.2)*
- Build Grade Calculator v2.5, in which an invalid grade scale becomes impossible to construct.

---

## 18.1 From Struct to Class

Chapter 14 gave you records. Chapter 14 Section 14.8 also named what they do not do:

- **Nothing protects the members.** Any code can write `s.id = -5;`.
- **The related functions live outside**, among every other function in the file.

A **class** fixes both. This is item six on your Chapter 13 backlog — *preventive* maintenance, making future change cheaper.

![Two panels: on the left a struct Student with three public members and separate free functions outside it; on the right a class Student with the same members marked private and the member functions enclosed inside the boundary.](figures/ch18-fig1-class.svg)

**Figure 18.1 — A struct compared with a class holding the same data.**

*Description of Figure 18.1.* The left panel shows `struct Student` with three public members — `name`, `id`, `scores` — and, drawn separately outside the struct in a dashed box, the free functions `total` and `percentage`. A note records that any code can write `s.id = -5;`.

The right panel shows `class Student` with the same information, arranged differently: a `public:` section listing `addAssignment`, `totalEarned`, and `percentage`, and a `private:` section holding `name_`, `id_`, and `work_`, all inside one boundary. A note records that outside code can only call the functions.

**The data did not change. What can reach it did.**

---

## 18.2 Objects, State, and Behavior

An **object** bundles **state** — the data it holds — with **behavior** — the operations on that data.

A **class** describes what objects of a kind look like and can do. An **object** is one actual instance:

```cpp
Student ada("Ada Lovelace", 1001);      // one object
Student grace("Grace Hopper", 1002);    // another, independent
```

A class is a blueprint; objects are the buildings. Each object has its own copy of the data.

You have used objects since Chapter 12. `std::vector<double> scores;` creates an object; `scores.push_back(9.0)` calls a member function on it; the vector's internal storage is state you never see. Everything in this chapter is how that was built.

---

## 18.3 Declaring a Class

```cpp
class Student {
public:
    Student() = default;
    Student(const std::string& name, int id);

    const std::string& name() const { return name_; }
    int id() const { return id_; }

    void addAssignment(const Assignment& a);
    double totalEarned() const;
    double percentage() const;

private:
    std::string name_;
    int id_ = 0;
    std::vector<Assignment> assignments_;
};
```

Three things to note.

**Access specifiers.** `public:` members are reachable by any code. `private:` members are reachable only from inside the class. Everything after a specifier has that access until the next one.

**Ordering.** Appendix D Section D.7 requires `public` first, then `protected`, then `private` — because the interface is what a reader wants and the implementation is what they can skip.

**Trailing underscores.** `name_`, `id_` — Appendix D Section D.2's convention, so you can tell a member from a local at every point of use, and so a constructor parameter can share its member's name without ambiguity.

> `struct` and `class` are the same construct in C++, differing only in default access: struct members are public, class members are private. Everything here could be written with `struct`. The convention this book follows is `struct` for plain data with no invariants, `class` when there is behavior or something to protect.

---

## 18.4 Member Functions

A **member function** is declared inside the class and operates on the object it is called on:

```cpp
double Student::totalEarned() const {
    double sum = 0.0;
    for (const Assignment& a : assignments_) {
        sum += a.totalEarned();
    }
    return sum;
}
```

`Student::` says which class this belongs to. Inside, `assignments_` refers to **this object's** member — no parameter needed, because the object is implicit.

Compare with the free function from Chapter 14:

```cpp
double total(const Student& s);      // Chapter 14: takes the student
double Student::totalEarned() const; // Chapter 18: is part of the student
```

Called as `ada.totalEarned()`, which reads as asking the object for something rather than performing an operation on it.

### `const` member functions

A member function that does not modify the object is marked `const`:

```cpp
double totalEarned() const;    // does not change the object
void addAssignment(const Assignment& a);   // does
```

This matters more than it looks. **A `const` object can only have its `const` member functions called.** Since Chapter 10 you have been passing things as `const Student&`, so without `const` member functions, a `const Student` would be nearly useless.

Appendix D Section D.5 asks you to do this from the start: retrofitting `const` onto a finished class is tedious, and until it is done, `const` references are unusable.

---

## 18.5 Encapsulation

**Encapsulation** is bundling data with the functions that operate on it, and restricting access to the data.

The word people reach for is "hiding," which undersells it. The point is not secrecy. **The point is that a class can guarantee things about itself that a struct cannot.**

With a struct:

```cpp
Student s;
s.id = -5;                    // nonsense, and nothing stops it
s.scores.clear();             // now scores and assignments disagree
```

With a class, those members are private. The only way to change a `Student` is through its member functions, and those can check.

Two practical consequences:

**You can change the implementation freely.** If `Student` stores a cached total instead of recomputing it, no calling code changes — the interface is the same. With public members, every user of `scores` is a user of your implementation.

**Bugs have a small number of suspects.** When a `Student` holds a wrong value, the only code that could have caused it is `Student`'s own member functions. That is a handful of functions instead of the whole program — the same argument Chapter 10 Section 10.1 made against globals, applied at a smaller scale.

---

## 18.6 Constructors

A **constructor** runs when an object is created, and its job is to leave the object in a valid state.

```cpp
class Student {
public:
    Student() = default;                                   // default constructor
    Student(const std::string& name, int id);              // parameterized
    // ...
};

Student::Student(const std::string& name, int id)
    : name_(name), id_(id) {}
```

The `: name_(name), id_(id)` is an **initializer list**, and it runs before the constructor body. Prefer it to assignment inside the body — it initializes members directly rather than default-constructing them and then overwriting.

`= default` asks the compiler to generate the obvious default constructor. Combined with member defaults declared in the class, that is usually all you need:

```cpp
private:
    std::string name_;
    int id_ = 0;
    std::vector<Assignment> assignments_;
```

### `explicit`

A single-argument constructor should usually be `explicit`:

```cpp
explicit GradeScale(const std::vector<Tier>& requested);
```

Without it, the compiler will silently convert a `std::vector<Tier>` into a `GradeScale` anywhere one is expected — including places you did not intend. Appendix D Section D.7 requires `explicit` unless the implicit conversion is genuinely wanted.

### Destructors

A **destructor** runs when an object is destroyed:

```cpp
~Student();
```

For a class holding only `std::string` and `std::vector`, you do not need one — those clean up after themselves. Destructors become essential in Chapter 22, when a class owns memory directly.

---

## 18.7 Accessors and Mutators

An **accessor** reads state; a **mutator** changes it:

```cpp
const std::string& name() const { return name_; }     // accessor
void setName(const std::string& n) { name_ = n; }     // mutator
```

A caution worth taking seriously: **an accessor and mutator for every member is a struct with extra steps.**

```cpp
// This class protects nothing.
class Student {
public:
    int getId() const { return id_; }
    void setId(int id) { id_ = id; }      // still allows id = -5
private:
    int id_ = 0;
};
```

Ask what the class is *for*. A `Student` needs `addAssignment` and `percentage` — operations meaningful in the problem. It does not need `setScores`, because nothing in the problem replaces a student's entire score list.

**Provide the operations the problem needs, not one pair per member.** That distinction is what separates object-oriented design from struct-with-ceremony.

---

## 18.8 Class Invariants

An **invariant** is something that is always true of an object, from construction until destruction.

This is the most valuable idea in the chapter.

Since Chapter 11, your grade scale has needed three properties: cutoffs strictly descending, no negative cutoffs, and a bottom tier at 0 so every percentage maps to a letter. You have been checking these by hand in `readGradeScale`, and every future path that builds a scale would need the same checks.

State it once, as an invariant, and enforce it in the constructor:

```cpp
/**
 * An ordered set of grade cutoffs.
 * INVARIANT: cutoffs strictly descend and the lowest tier is 0, so every
 * percentage from 0 upward maps to exactly one letter. The constructor
 * establishes this, and no member function can break it.
 */
class GradeScale {
public:
    struct Tier { double cutoff = 0.0; char letter = 'F'; };

    GradeScale() {
        tiers_ = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };
    }

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

    char letterFor(double percentage) const {
        for (const Tier& t : tiers_) {
            if (percentage >= t.cutoff) { return t.letter; }
        }
        return tiers_.back().letter;
    }

private:
    std::vector<Tier> tiers_;
};
```

Feed it deliberate nonsense — out of order, negative, no floor tier:

```cpp
GradeScale bad({{90.0,'A'}, {95.0,'X'}, {-5.0,'Q'}, {85.0,'B'}});
```

```text
repaired tiers=3
  96 -> A
  90 -> A
  86 -> B
  10 -> F
```

The `X` tier was rejected because 95 is not below 90. The `Q` tier was rejected as negative. A floor tier was added. **What survived is a valid scale**, and there was never a moment when the object was invalid.

### What the invariant buys

Look at `letterFor` again. It has **no error handling**. No check that the scale is non-empty, no `'?'` return for a percentage below every tier, no defensive anything.

It does not need any, because the constructor guarantees the scale is usable. Compare with Chapter 11's version, which returned `'?'` when nothing matched — a value every caller then had to handle.

**An invariant established in the constructor is a fact the rest of your code may rely on without checking.** That is the entire return on encapsulation, and it is why the members must be private: if a caller could write `tiers_` directly, the guarantee would be worthless.

### Repair or reject?

This version *repairs* bad input. That is one policy. The alternative is to refuse — to make constructing an invalid `GradeScale` impossible rather than silently corrected.

Repair is friendlier and hides the fact that the user's input was wrong. Rejection is honest and requires a way to report the failure, which you do not have until Chapter 24.

**Chapter 24 switches this class to rejection**, throwing `InvalidScaleError`. Notice that the *invariant* does not change — only what happens when someone violates it. That is a sign the invariant was the right thing to state.

---

## 18.9 Identifying Classes from Requirements

Chapter 14 Section 14.7 found records by looking for **nouns**. Classes are found the same way, with an added question.

For each noun, ask: **does it have behavior, or rules about what values are valid?**

| Noun | Behavior or rules? | Verdict |
|---|---|---|
| Assignment | computes its own total and ratio | class |
| Student | accumulates work, computes a percentage | class |
| Grade scale | must be ordered and complete | class — the invariant demands it |
| Tier | a cutoff and a letter, nothing more | **struct**, nested inside `GradeScale` |
| Score | two numbers | struct — or fold into `Assignment` |

`GradeScale::Tier` staying a struct is deliberate. It has no behavior and no invariant of its own; it exists only as part of a scale. Making it a class would add ceremony and protect nothing. **Not everything should be a class.**

Note also that `Tier` is declared *inside* `GradeScale`. A tier has no meaning apart from a scale, and nesting says so — Appendix D Section D.4's guidance about small helper types.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `error: 'name_' is private within this context` | Outside code touching a private member | Add an accessor, or a real operation |
| `error: passing 'const Student' as 'this' discards qualifiers` | Non-`const` function called on a `const` object | Mark the function `const` |
| `error: no matching function for call to 'Student::Student()'` | No default constructor, but one is needed | Add `Student() = default;` |
| `error: expected ';' after class definition` | Missing semicolon after `}` | Add `;` |
| Members hold garbage | Constructor did not initialize them | Use an initializer list, or member defaults |
| A conversion happens unexpectedly | Single-argument constructor not `explicit` | Mark it `explicit` |
| `error: 'class Student' has no member named 'Name'` | Wrong capitalization | C++ is case-sensitive |
| An object reaches an invalid state | The invariant is not enforced | Enforce it in the constructor; keep members private |

---

## Design Notes

**Data members are always private.** A public member is a promise you cannot take back.

**Mark every non-modifying member function `const`, from the start.**

**State the invariant in a comment above the class, and enforce it in the constructor.** Then trust it everywhere else.

**Provide the operations the problem needs, not a getter and setter per member.**

**Not everything is a class.** Plain data with no rules stays a struct.

---

## Grade Calculator v2.5 — Student and GradeScale Classes

### What v2.5 does

Everything v2.4 did, with `Student`, `Assignment`, and `GradeScale` converted from structs to classes. The grading math and the saved report are unchanged; **what can reach the data is** — and one class of defect disappears. One workflow detail does change: because each `Student` now owns its own `Assignment` objects instead of sharing one course-wide list, assignments are entered per student (when you add the student) rather than in a separate "add an assignment" step. See "A restructure worth noting" below.

### A restructure worth noting

Each `Student` now owns its own `Assignment` objects, where previously assignments were a separate list and students held parallel scores:

```cpp
class Assignment {
public:
    Assignment(const std::string& name, double earned, double possible, double bonus = 0.0);
    const std::string& name() const { return name_; }
    double totalEarned() const;      // earned + bonus
    double ratio() const;            // fraction of possible, or 0
private:
    std::string name_;
    double pointsEarned_   = 0.0;
    double pointsPossible_ = 0.0;
    double bonusPoints_    = 0.0;
};
```

This removes the correspondence problem entirely. A student's assignments cannot be out of step with a separate list, because there is no separate list. It also makes `Student::percentage()` self-contained:

```cpp
double Student::percentage() const {
    double possible = totalPossible();
    if (possible <= 0.0) { return 0.0; }
    double raw = totalEarned() / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}
```

No parameters. The student has everything it needs.

### GradeScale enforces its invariant

The class from Section 18.8, used directly:

```cpp
GradeScale scale;                    // default: A/B/C/D/F, valid by construction
scale = GradeScale(userTiers);       // custom: repaired to valid, or built valid
```

`readGradeScale`'s hand-written validation from Chapter 11 is **gone**. It moved into the constructor, where it cannot be bypassed.

### Expected output

Add Ada with `HW1` 9/10 bonus 1 and `Midterm` 84/100 bonus 5, view the report, then set a custom scale of A 93, B 85, and a deliberately invalid tier `ZZZ` at 99:

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
1001  Ada                     90.0%   A
  Scale accepted.
  Scale: A >= 93   B >= 85   F >= 0   
1001  Ada                     90.0%   B
```

Three things happened. The `ZZZ` tier at 99 was **silently rejected**, because 99 is not below 93. A floor tier `F` at 0 was **added**, because the user's scale did not reach 0. And the same 90.0% became a **B** under the stricter scale — the data changed, not the code.

### What to notice

**`letterFor` has no error handling and needs none.** The invariant guarantees a usable scale.

**The validation code exists once.** In v1.3 it lived in `readGradeScale`. Any second way of building a scale — from a file, from a default, from a copy — would have needed its own copy of the checks. Now every path goes through the constructor.

**`std::min` needs `<algorithm>`, and `std::round` needs `<cmath>`.** Appendix D Section D.4: include what you use.

**The class is longer than the struct.** That is the cost, and it is real. What you get for it is that a whole category of wrong state can no longer be expressed.

### Your StudySite Lab — Introduce Classes and Invariants

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.5
- **Starting point:** The working Chapter 17 v2.4 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Convert `Assignment`, `Student`, and `GradeScale` from structs to classes with private data members.
2. Merge the old `Score` struct into `Assignment`: an assignment now carries its own `pointsEarned`, `pointsPossible`, and `bonusPoints` directly, because each `Assignment` belongs to exactly one `Student` instead of being shared and indexed in parallel with a separate scores list.
3. Give `GradeScale` an invariant, enforced in its constructors: cutoffs strictly descend, no cutoff is negative, and the lowest tier is 0. An out-of-order or invalid tier is repaired or dropped, not rejected with an error — the constructor always produces a usable scale.
4. Add `Student::letterGrade(const GradeScale&) const`, which looks up the student's own `percentage()` on the given scale.
5. Add a **Custom scale** menu option that reads tiers from the user (highest first, `'done'` to finish) and replaces the active `GradeScale` by constructing a new one from what was entered — letting the invariant-enforcing constructor repair whatever the user typed.
6. Carry the Chapter 15–17 features forward onto the new classes: saving and loading the gradebook, the `runTests()` regression suite, and sorting/searching the roster all still need to work — update them to call the new class members instead of the old free functions, but do not drop them.

Item 6 is the one most worth double-checking. It is easy, while converting structs to classes, to rewrite `main` around the new `Student`/`GradeScale`/`Assignment` types and forget to carry every menu option across. Chapter 18 should still have all eight menu options Chapter 17 had, plus the new **Custom scale** option — nine total.

#### What changes from Chapter 17

Three real structural changes come with the class conversion, not just renamed types:

- **The `Gradebook` struct is retired.** Chapter 17 grouped `assignments`, `roster`, `scale`, and `nextId` into one `Gradebook` struct passed around together. Chapter 18 has no equivalent struct — `main` now holds a `GradeScale scale`, a `std::vector<Student> roster`, and an `int nextId` as three separate local variables, and the free functions that touched a `Gradebook` (`saveGradebook`, `loadGradebook`) take these three directly as parameters instead.
- **The course-wide assignment list is retired.** Chapter 17 had one shared `std::vector<Assignment> assignments` that every student's `scores` lined up against by index. Chapter 18 has no shared list at all — each `Student` owns its own `std::vector<Assignment>`, added with `Student::addAssignment`. This removes the **Add assignment** menu option entirely; there is nothing course-wide left to add.
- **Assignments are entered per student, not once up front.** Because there is no shared assignment list, the workflow moves: when you choose **Add student**, you now enter that student's name and then loop entering that one student's assignments (name, points earned, points possible, bonus) before the student is added to the roster. This is a real workflow change, not just an implementation detail — the same *grading math* Chapter 17 used is still there, but the *sequence of prompts* a user sees is different, so "the same input reproduces the same run" is no longer literally true input-for-input. What must still match is the same percentage and letter grade for the same scores.
- **The gradebook file format changes to match.** The `ASSIGNMENT` record type is retired — there is no course-wide assignment list left to save. Each `STUDENT` row now carries its own assignment fields inline: `STUDENT,<id>,<name>,<assignmentName>,<earned>,<possible>,<bonus>`, repeated for every assignment that student has. A file saved by Chapter 17 is not compatible with Chapter 18's loader.

Everything else genuinely carries over: `readNonNegative` and `readLine` are untouched, the default A/B/C/D/F scale is unchanged, the report layout is unchanged, and the D1–D3 regression tests still check the exact same three defects with the exact same pass/fail wording.

#### Build it: step by step

##### Step 1 — Turn `Assignment` into a class, and fold `Score` into it

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

##### Step 2 — Turn `GradeScale` into a class with an invariant-enforcing constructor

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

##### Step 3 — Turn `Student` into a class that owns its own assignments

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

##### Step 4 — Update persistence for the new per-student format

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

##### Step 5 — Update the regression tests to exercise the classes

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

##### Step 6 — Update sorting and searching to compare `Student` objects directly

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

##### Step 7 — Rebuild `main`: retire `Gradebook`, add the Custom scale option

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

#### Verification

- Code outside a class cannot modify `Assignment`, `Student`, or `GradeScale` data directly — every field is private.
- Building a `GradeScale` from ascending, negative, empty, or floor-missing tiers always produces a valid, usable scale; nothing crashes or throws.
- For the same scores, a student's reported percentage and letter grade match the same math Chapter 17 used — verify this by comparing a report you already have from Chapter 17 against the same scores entered in Chapter 18.
- Saving, quitting, and relaunching reloads the roster with matching IDs, names, scores, and percentages.
- `Run tests` still reports **8 of 8 checks passed**.
- `Sort roster` and `Find by ID` still work, including the linear-vs-binary comparison counts on **Find by ID**.
- All accessors that do not change an object are `const`.

#### StudySite workflow

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

#### Save this checkpoint

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
4. Enter the commit message **Complete Chapter 18 Grade Calculator v2.5**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 18
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.

---

## Try It Yourself

### 1. A first class

```cpp
#include <iostream>
#include <string>

class Assignment {
public:
    Assignment(const std::string& name, double earned, double possible)
        : name_(name), earned_(earned), possible_(possible) {}

    const std::string& name() const { return name_; }
    double ratio() const { return possible_ > 0.0 ? earned_ / possible_ : 0.0; }

private:
    std::string name_;
    double earned_ = 0.0;
    double possible_ = 0.0;
};

int main() {
    Assignment hw("Homework 1", 9.0, 10.0);
    std::cout << hw.name() << " ratio " << hw.ratio() << "\n";
    return 0;
}
```

**Expected output:**

```text
Homework 1 ratio 0.9
```

*Try:* Add `hw.earned_ = 100.0;` to `main` and read the error. That error is encapsulation working.

### 2. `const` member functions

```cpp
#include <iostream>
#include <string>

class Student {
public:
    explicit Student(const std::string& name) : name_(name) {}
    const std::string& name() const { return name_; }
    void rename(const std::string& n) { name_ = n; }
private:
    std::string name_;
};

void show(const Student& s) {
    std::cout << s.name() << "\n";        // works: name() is const
}

int main() {
    Student ada("Ada");
    show(ada);
    ada.rename("Ada Lovelace");
    show(ada);
    return 0;
}
```

**Expected output:**

```text
Ada
Ada Lovelace
```

*Try:* Add `s.rename("X");` inside `show` and read the error. Then remove `const` from `name()` and see `show` stop compiling. Explain the connection.

### 3. An invariant enforced

```cpp
#include <iostream>
#include <vector>

class GradeScale {
public:
    struct Tier { double cutoff = 0.0; char letter = 'F'; };

    GradeScale() { tiers_ = {{90.0,'A'},{80.0,'B'},{70.0,'C'},{60.0,'D'},{0.0,'F'}}; }

    explicit GradeScale(const std::vector<Tier>& requested) {
        for (const Tier& t : requested) {
            if (t.cutoff < 0.0) { continue; }
            if (!tiers_.empty() && t.cutoff >= tiers_.back().cutoff) { continue; }
            tiers_.push_back(t);
        }
        if (tiers_.empty() || tiers_.back().cutoff > 0.0) { tiers_.push_back({0.0,'F'}); }
    }

    char letterFor(double pct) const {
        for (const Tier& t : tiers_) { if (pct >= t.cutoff) { return t.letter; } }
        return tiers_.back().letter;
    }
    std::size_t tierCount() const { return tiers_.size(); }

private:
    std::vector<Tier> tiers_;
};

int main() {
    GradeScale d;
    std::cout << "default tiers=" << d.tierCount()
              << " 95->" << d.letterFor(95) << " 0->" << d.letterFor(0) << "\n";

    GradeScale bad({{90.0,'A'},{95.0,'X'},{-5.0,'Q'},{85.0,'B'}});
    std::cout << "repaired tiers=" << bad.tierCount() << "\n";
    for (double p : {96.0, 90.0, 86.0, 10.0}) {
        std::cout << "  " << p << " -> " << bad.letterFor(p) << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
default tiers=5 95->A 0->F
repaired tiers=3
  96 -> A
  90 -> A
  86 -> B
  10 -> F
```

*Try:* Work out by hand which of the four requested tiers survived and why. Then construct a scale from an empty vector — what do you get, and does `letterFor` still work?

### 4. Constructors and initializer lists

```cpp
#include <iostream>
#include <string>

class Course {
public:
    Course() = default;
    Course(const std::string& title, int credits)
        : title_(title), credits_(credits) {}

    void describe() const {
        std::cout << "[" << title_ << "] " << credits_ << " credits\n";
    }

private:
    std::string title_ = "Untitled";
    int credits_ = 0;
};

int main() {
    Course a;
    Course b("Programming Fundamentals", 4);
    a.describe();
    b.describe();
    return 0;
}
```

**Expected output:**

```text
[Untitled] 0 credits
[Programming Fundamentals] 4 credits
```

*Try:* Remove `Course() = default;` and rebuild. Which line fails, and why does supplying one constructor remove the free one?

### 5. Convert a struct to a class

Take this struct and make it a class with a meaningful invariant: a bank balance may never be negative.

```cpp
struct Account {
    std::string owner;
    double balance = 0.0;
};
```

Provide `deposit` and `withdraw`. What should `withdraw` do when the amount exceeds the balance? Your answer is a design decision — write it down, and note that Chapter 24 gives you a better option than the ones available now.

### 6. Identify the classes

For a library system: *A member has a name, a number, and a list of borrowed books. A book has a title, an author, and an availability status. A member may borrow at most five books. A book cannot be borrowed by two members at once.*

Which nouns become classes and which stay structs? **What are the invariants?** Where is each enforced?

### 7. Reason about encapsulation

- Why must data members be private for an invariant to mean anything?
- What is the difference between a class and an object?
- Why should non-modifying member functions be `const`, and what breaks if they are not?
- Why is a class with a getter and setter for every member no better than a struct?
- `GradeScale::letterFor` has no error handling. Why is that safe here and would not be in Chapter 11?

---

## Summary

- A **class** describes a kind of object; an **object** is one instance with its own state.
- **Encapsulation** bundles data with behavior and restricts access. Data members are **private**; the interface is public.
- A **member function** operates on the object it is called on. Mark non-modifying ones **`const`**, from the start.
- A **constructor** leaves a new object in a valid state. Prefer an **initializer list** to assignment in the body. Mark single-argument constructors **`explicit`**.
- **An invariant is something always true of an object.** State it above the class and enforce it in the constructor.
- **An invariant established in the constructor is a fact the rest of your code may rely on without checking** — which is why `letterFor` needs no error handling.
- **A getter and setter for every member protects nothing.** Provide the operations the problem needs.
- Find classes by looking for nouns with **behavior or rules**. Plain data with neither stays a **struct**.
- The point of privacy is not secrecy. It is that a class can **guarantee** things about itself that a struct cannot.

---

## Key Terms

**accessor** — a member function that reads state without modifying it.

**access specifier** — `public`, `protected`, or `private`, controlling what may reach a member.

**class** — a type bundling data with the functions that operate on it.

**const member function** — a member function that does not modify the object.

**constructor** — a function run when an object is created, establishing its invariant.

**destructor** — a function run when an object is destroyed.

**encapsulation** — bundling data with behavior and restricting access to the data.

**explicit** — a qualifier preventing implicit conversion through a constructor.

**initializer list** — the `: member(value)` syntax initializing members before the constructor body.

**instance** — one object of a class.

**invariant** — a property that is always true of an object.

**member function** — a function declared inside a class, operating on an object of it.

**mutator** — a member function that changes state.

**object** — an instance of a class, holding its own state.

**state** — the data an object holds.

---

**Next:** Chapter 19 finishes the conversion. A `Gradebook` class takes ownership of the roster and the scale, `operator<<` prints an entire report with a single `<<`, and every class moves into its own header and implementation file pair. Grade Calculator v2.6.
