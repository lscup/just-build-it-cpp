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

The v2.4 data model rebuilt with classes: `Assignment`, `Student`, and `GradeScale` become classes with private data, and the grading math is unchanged. Because each `Student` now owns its own `Assignment` objects instead of sharing one course-wide list, assignments are entered per student (when you add the student) rather than in a separate "add an assignment" step. See "A restructure worth noting" below.

v2.5 also starts from a deliberately smaller core — Add student, Report, Custom scale, and Quit — so the class design gets your full attention. Saving and loading, the regression tests, and sort and find are set aside for this checkpoint; sorting returns in Chapter 19, lookup by ID in Chapter 23, and saving and loading in Chapter 24.

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
- **Starting point:** Your committed Chapter 17 v2.4 program (`main.cpp`).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### What you will build

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

#### What is different about v2.5

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

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit. Everything in this lab happens in this one file. |

#### How to use these steps

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

> **Heads-up:** Steps 2 through 7 take the program apart before Step 8 puts
> `main` back together, so the program will **not** compile again until the
> end of Step 8. That is expected. Do not try to fix compiler errors in the
> middle — finish the steps in order, then Run.

#### Build it: step by step

##### Step 1 — Update the header comment

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

##### Step 2 — Update the `#include` list and constants

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

##### Step 3 — Replace the structs with an `Assignment` class

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

##### Step 4 — Add the `GradeScale` class and its invariant

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

##### Step 5 — Add the `Student` class

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

##### Step 6 — Update the input-helpers banner

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

##### Step 7 — Remove the code that v2.5 sets aside

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

##### Step 8 — Rewrite `main` around the new classes

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

> **▶ Run checkpoint:** Click **Run**. The program should compile with no errors and no warnings and show the v2.5 banner, the default scale, and the four-option menu. If you see errors, the message names a line — compare that area with the code boxes above.

#### Check your work

Run the program and type the inputs below in the Terminal. Your output should
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

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click `main.cpp` to open it.
   Confirm the editor shows the expected file paths before editing.
4. Work through Steps 1–8 above in StudySite's internal editor, in order. Click **Run** at the ▶ Run checkpoint at the end of Step 8.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — for this chapter that is just `main.cpp`. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 18 Grade Calculator v2.5**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
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
