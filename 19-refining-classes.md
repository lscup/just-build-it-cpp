# Chapter 19 — Refining Classes

## Learning Objectives

When you finish this chapter you will be able to:

- Pass and return objects efficiently and safely. *(SLO 2.2)*
- Explain what `this` refers to inside a member function. *(SLO 2.2)*
- Separate a class declaration from its definitions across a header and implementation file. *(SLO 2.2, 2.4)*
- Overload operators, including `<<`, `[]`, and `<`. *(SLO 2.2, 2.3)*
- Explain what `static` members are and when they are appropriate. *(SLO 2.2)*
- Describe what the compiler generates when you write nothing. *(SLO 2.2)*
- Explain what `friend` does and why it is used sparingly. *(SLO 2.2)*
- Build Grade Calculator v2.6 — one class per file, and a whole report printed with one `<<`.

---

## 19.1 Passing and Returning Objects

Chapter 10 Section 10.7's rule applies to objects, and now matters more, because objects can be large.

```cpp
void printReport(const Gradebook& book);      // yes — no copy, cannot modify
void printReport(Gradebook book);             // no  — copies the entire roster
```

**Take `const&` unless you intend to modify.** A `Gradebook` holding 300 students copies 300 students otherwise.

Returning is different. Returning by value is normal and efficient:

```cpp
Student Gradebook::studentAt(std::size_t i) const {
    return roster_[i];        // fine — the compiler avoids the copy
}
```

Modern C++ elides the copy in almost every such case. What you must **never** do is return a reference to something local:

```cpp
const Student& bad() {
    Student s("Ada", 1001);
    return s;                 // s is destroyed; the reference dangles
}
```

That compiles, warns under `-Wall`, and produces undefined behavior. Returning a reference is only safe when the object outlives the call — a member, or something the caller owns.

---

## 19.2 The `this` Pointer

Inside a member function, `this` is a pointer to the object the function was called on:

```cpp
void Student::rename(const std::string& name) {
    this->name_ = name;       // same as name_ = name
}
```

You rarely need it, because unqualified member names already refer to the current object. Two cases where it earns its place:

**Returning the object itself**, which enables chaining:

```cpp
Student& Student::addAssignment(const Assignment& a) {
    assignments_.push_back(a);
    return *this;             // note the *, giving the object not the pointer
}

ada.addAssignment(hw).addAssignment(exam);   // chained
```

**Distinguishing a member from a parameter of the same name.** Appendix D's trailing underscore makes this unnecessary, which is one reason for the convention.

---

## 19.3 Separating Declaration from Definition

Chapter 10 Section 10.8 split functions across files. Classes split the same way, and Appendix D Section D.4 sets the rule: **one class, one header, one implementation file, all lowercase.**

### The header — `gradescale.h`

```cpp
// gradescale.h - Grade Calculator v2.6 - Chapter 19
#ifndef GRADESCALE_H
#define GRADESCALE_H

#include <iosfwd>
#include <vector>

/**
 * An ordered set of grade cutoffs.
 * INVARIANT: cutoffs strictly descend and the lowest tier is 0, so every
 * percentage from 0 upward maps to exactly one letter.
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

### The implementation — `gradescale.cpp`

```cpp
// gradescale.cpp - Grade Calculator v2.6 - Chapter 19
#include "gradescale.h"

#include <iomanip>
#include <ostream>

GradeScale::GradeScale() {
    tiers_ = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };
}

char GradeScale::letterFor(double percentage) const {
    for (const Tier& t : tiers_) {
        if (percentage >= t.cutoff) { return t.letter; }
    }
    return tiers_.back().letter;
}
```

Each definition is prefixed with `GradeScale::` to say which class it belongs to.

**What goes where.** Very short accessors — one line, no logic — may stay in the header. Anything with real logic goes in the `.cpp`. The header should read as a summary of what the class *is*, uncluttered by how it works.

### `<iosfwd>`

Note the header includes `<iosfwd>` rather than `<ostream>`. It declares that `std::ostream` exists without pulling in the whole stream library — enough to declare `operator<<`, and much less for the compiler to read in every file that includes yours.

The `.cpp` includes the full `<ostream>`, because that is where the definition actually uses it.

**Headers should include as little as possible.** Every file including your header pays for whatever it includes.

---

## 19.4 Operator Overloading

C++ lets you define what operators mean for your own types. Used well, this makes your classes read like built-in ones. Used badly, it makes code cryptic.

**The rule: overload an operator only when its meaning is obvious.** `+` on a `Money` class is obvious. `+` on a `Student` is not.

### Stream output with `operator<<`

The most valuable overload by far:

```cpp
std::ostream& operator<<(std::ostream& out, const Student& s) {
    out << std::fixed << std::setprecision(1)
        << std::left  << std::setw(6)  << s.id()
        << std::setw(14) << s.name()
        << std::right << std::setw(7)  << s.percentage() << "%";
    return out;
}
```

Now a `Student` prints like anything else:

```cpp
std::cout << ada << "\n";
```

Three details make it work:

**It is a free function, not a member.** The left operand is the stream, not your object, so it cannot be a member of your class.

**It takes and returns `std::ostream&`.** Returning the stream is what allows chaining — `out << a << b` works because the first `<<` returns the stream for the second.

**The object parameter is `const&`.** Printing does not modify.

Because it takes any `std::ostream`, the same function writes to `std::cout`, to a file, or to a `std::ostringstream`. **One definition, every destination** — which is Chapter 15 Section 15.1's abstraction paying off.

### Indexing with `operator[]`

```cpp
const Student& Gradebook::operator[](std::size_t index) const {
    return roster_[index];
}
```

```cpp
std::cout << book[1] << "\n";
```

A `Gradebook` now indexes like a vector. Note the **precondition**: this does not check bounds, matching what `[]` means everywhere else in C++. Document it, and provide an `at()` if you want checking — Chapter 12 Section 12.4's distinction, applied to your own class.

### Comparison with `operator<`

```cpp
bool Student::operator<(const Student& other) const {
    return percentage() > other.percentage();   // highest first
}
```

This one deserves a warning. **`operator<` here means "sorts before", not "is less than"** — a student with a *higher* percentage sorts first. That is a legitimate ordering and a surprising definition of `<`.

Chapter 23 shows the alternative: pass a lambda to `std::sort` stating the ordering where it is used. **When an operator's meaning is not obvious, a named function or an explicit comparison is better.**

### Member or free function?

| Overload as | When | Examples |
|---|---|---|
| Member | the left operand is your class | `[]`, `<`, `+=` |
| Free function | the left operand is something else | `<<`, `>>` |

### What you cannot do

You cannot invent new operators, change precedence, or change the number of operands. `**` is not an operator in C++ and cannot be made one.

---

## 19.5 Static Members

A **static member** belongs to the class rather than to any object — one copy shared by all.

```cpp
class Student {
public:
    static int totalCreated();
private:
    static int count_;        // declared here
};

int Student::count_ = 0;      // defined once, in the .cpp
```

Static data members are declared in the class and **defined once** in the implementation file. Forgetting the definition produces a linker error, which is Chapter 2 Section 2.2.4's division appearing again.

A **static member function** has no object and therefore no `this`. It can only touch static members.

Use static members sparingly. Chapter 10 Section 10.1's argument against globals applies: shared mutable state makes a class harder to test, because two tests can affect each other. A counter of objects created is a reasonable use; shared configuration usually is not.

---

## 19.6 What the Compiler Writes for You

If you write none of these, the compiler generates them:

| Generated | Does |
|---|---|
| Default constructor | default-constructs each member — **only if you declare no other constructor** |
| Copy constructor | copies each member |
| Copy assignment | assigns each member |
| Destructor | destroys each member |

For a class holding `std::string` and `std::vector`, **the generated versions are correct**, because those members copy and clean up properly themselves. `Student`, `Assignment`, and `GradeScale` all need nothing.

Two things to remember. **Declaring any constructor removes the free default one** — which is why `Student() = default;` appears explicitly when you also want a parameterized constructor. And the generated versions stop being correct as soon as a class manages a resource directly, which is Chapter 22's subject.

---

## 19.7 Friends

A **friend** function is granted access to a class's private members:

```cpp
class Student {
    friend std::ostream& operator<<(std::ostream&, const Student&);
private:
    std::string name_;
};
```

`friend` deliberately breaks encapsulation, so it needs justification. The usual one is `operator<<`, which must be a free function but wants to print private state.

**Often you do not need it.** If the class already has public accessors, `operator<<` can use those:

```cpp
std::ostream& operator<<(std::ostream& out, const Student& s) {
    out << s.id() << " " << s.name();     // public accessors — no friend needed
    return out;
}
```

**Prefer accessors to friendship.** Grade Calculator v2.6 uses no `friend` at all. The keyword is covered because you will meet it, and because knowing when *not* to reach for it is the useful part.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `undefined reference to 'Student::name()'` | Declared in the header, not defined | Define it in the `.cpp` with `Student::` |
| `undefined reference to 'Student::count_'` | Static member declared, never defined | Define it once in the `.cpp` |
| `error: no match for 'operator<<'` | No overload for your type | Write one, or print members individually |
| `warning: reference to local variable returned` | Returning a reference to a local | Return by value |
| `error: passing 'const X' discards qualifiers` | Non-`const` function on a `const` object | Mark it `const` |
| `error: 'name_' is private within this context` | Free function touching private data | Use an accessor, or `friend` if justified |
| Chained `<<` fails to compile | `operator<<` returns `void` | Return `std::ostream&` |
| Every file recompiles after a small change | Header includes too much | Use `<iosfwd>`; move includes to the `.cpp` |
| `error: redefinition of class` | Missing header guard | Add one |

---

## Design Notes

**Take objects by `const&`; return by value.** Never return a reference to a local.

**One class, one header, one implementation file.** Headers summarize; implementations explain.

**Headers include as little as possible.** `<iosfwd>` over `<ostream>` when a declaration is all you need.

**Overload an operator only when its meaning is obvious.** `operator<<` almost always is; `operator<` on a `Student` is not.

**Prefer accessors to `friend`.**

---

## Grade Calculator v2.6 — Gradebook Class

### What v2.6 does

Everything v2.5 did, reorganized: a `Gradebook` class owns the roster, the scale, the course name, and the next-ID counter; reports print through `operator<<`; and every class lives in its own header and implementation file. It also adds one feature, **Sort by grade**, built on `Student::operator<` and `std::sort`.

### The file layout

```text
assignment.h    assignment.cpp
gradescale.h    gradescale.cpp
student.h       student.cpp
gradebook.h     gradebook.cpp
main.cpp
```

Every `.cpp` file has to reach the compiler. In StudySite that means keeping
`main.cpp`, `assignment.cpp`, `gradescale.cpp`, `student.cpp`, and
`gradebook.cpp` — and their headers — open in the editor before you click
**Run**. A file that is not open is a file that is not built, and the linker
error you get names the missing function, not the missing tab.

Nine files where there was one. That is the cost, and it buys something specific: each class can be read, changed, and reasoned about without the others in front of you.

### The Gradebook class

```cpp
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
```

**`Gradebook` owns everything a gradebook needs.** In v2.5, `main` held a roster, a scale, and a next-ID counter as separate variables and passed them around. Now they are one thing, and the ID counter cannot drift out of step with the roster.

### The whole report, one operator

```cpp
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

And in `main`:

```cpp
std::cout << book << "\n";      // one operator prints everything
```

Notice the nesting. `operator<<` for `Gradebook` uses `operator<<` for `Student`, which uses `operator<<` for `GradeScale`. **Each class knows how to print itself, and nothing knows how to print anything else.**

### Sorting through `operator<`

```cpp
void Gradebook::sortByPercentage() {
    std::sort(roster_.begin(), roster_.end());   // uses Student::operator<
}
```

One line, because `Student` defines its own ordering.

This is also where the concern from Section 19.4 becomes concrete. Reading `std::sort(roster_.begin(), roster_.end())` tells you the roster gets sorted; it does not tell you *by what*. You have to go and read `Student::operator<` — and discover it means "highest percentage first", which is not what `<` usually suggests.

Chapter 23 replaces this with a lambda stating the ordering at the call site. **Keep this version in mind for the comparison.**

### Expected output

Zoe with 5/10 and Ada with 9/10 plus 1 bonus, reported, then sorted, then reported again:

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
1001  Zoe                     50.0%   F
1002  Ada                    100.0%   A
CLASS AVERAGE                 75.0%

  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
1002  Ada                    100.0%   A
1001  Zoe                     50.0%   F
CLASS AVERAGE                 75.0%
```

### What to notice

**`main` shrank considerably.** It reads input, calls member functions, and prints. All the logic moved into the classes that own the data.

**`main` never touches a roster directly.** It cannot — `roster_` is private. Every change goes through `addStudent` or `sortByPercentage`, so the list of things that could corrupt it is exactly two functions.

**No `friend` anywhere.** Every `operator<<` uses public accessors.

**Headers use `<iosfwd>`.** Changing `student.cpp` does not force `gradebook.cpp` to recompile, because `student.h` pulls in almost nothing.

**Every accessor is `const`.** Without that, `operator<<` taking `const Gradebook&` would not compile.

### Your StudySite Lab — Split Classes into Files

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.6
- **Starting point:** Your committed Chapter 18 v2.5 program (`main.cpp`).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### What you will build

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

#### Files in this checkpoint

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

> **Heads-up:** Steps 1–4 create the new files; Steps 5–7 remove the old
> class code from `main.cpp`. Do **not** click Run until the checkpoint at the
> end of Step 7 — until then, the classes exist in two places at once.

#### Build it: step by step

##### Step 1 — Create `assignment.h` and `assignment.cpp`

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

##### Step 2 — Create `gradescale.h` and `gradescale.cpp`

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

##### Step 3 — Create `student.h` and `student.cpp`

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

##### Step 4 — Create the `Gradebook` class

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

##### Step 5 — Update the header comment in `main.cpp`

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

##### Step 6 — Remove the classes from `main.cpp`

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

##### Step 7 — Rewrite `main` to use a `Gradebook`

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

#### Check your work

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

#### StudySite workflow

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

#### Save this checkpoint

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

#### Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 19
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. `operator<<` for your own class

```cpp
#include <iomanip>
#include <iostream>
#include <ostream>
#include <string>

class Student {
public:
    Student(const std::string& n, int i, double p) : name_(n), id_(i), pct_(p) {}
    const std::string& name() const { return name_; }
    int id() const { return id_; }
    double percentage() const { return pct_; }
private:
    std::string name_;
    int id_ = 0;
    double pct_ = 0.0;
};

std::ostream& operator<<(std::ostream& out, const Student& s) {
    out << std::fixed << std::setprecision(1)
        << std::left << std::setw(6) << s.id()
        << std::setw(14) << s.name()
        << std::right << std::setw(7) << s.percentage() << "%";
    return out;
}

int main() {
    Student ada("Ada", 1002, 90.0);
    std::cout << ada << "\n";
    std::cout << "twice: " << ada << " and " << ada << "\n";
    return 0;
}
```

**Expected output:**

```text
1002  Ada              90.0%
twice: 1002  Ada              90.0% and 1002  Ada              90.0%
```

*Try:* Change the return type to `void` and rebuild. Which line fails, and why does returning the stream matter?

### 2. Nested `operator<<` and `operator[]`

```cpp
#include <iomanip>
#include <iostream>
#include <ostream>
#include <string>
#include <vector>

class Student {
public:
    Student(const std::string& n, int i, double p) : name_(n), id_(i), pct_(p) {}
    const std::string& name() const { return name_; }
    int id() const { return id_; }
    double percentage() const { return pct_; }
private:
    std::string name_;
    int id_ = 0;
    double pct_ = 0.0;
};

std::ostream& operator<<(std::ostream& out, const Student& s) {
    out << std::fixed << std::setprecision(1)
        << std::left << std::setw(6) << s.id() << std::setw(14) << s.name()
        << std::right << std::setw(7) << s.percentage() << "%";
    return out;
}

class Gradebook {
public:
    explicit Gradebook(const std::string& c) : course_(c) {}
    void add(const Student& s) { roster_.push_back(s); }
    std::size_t size() const { return roster_.size(); }
    const Student& operator[](std::size_t i) const { return roster_[i]; }
    const std::string& course() const { return course_; }
    double average() const {
        if (roster_.empty()) { return 0.0; }
        double t = 0.0;
        for (const Student& s : roster_) { t += s.percentage(); }
        return t / static_cast<double>(roster_.size());
    }
private:
    std::string course_;
    std::vector<Student> roster_;
};

std::ostream& operator<<(std::ostream& out, const Gradebook& b) {
    out << "== " << b.course() << " ==\n";
    for (std::size_t i = 0; i < b.size(); ++i) { out << b[i] << "\n"; }
    out << std::fixed << std::setprecision(1) << "AVERAGE " << b.average() << "%\n";
    return out;
}

int main() {
    Gradebook book("Programming Fundamentals");
    book.add({"Zoe", 1001, 50.0});
    book.add({"Ada", 1002, 90.0});
    std::cout << book;
    std::cout << "\nsingle student: " << book[1] << "\n";
    return 0;
}
```

**Expected output:**

```text
== Programming Fundamentals ==
1001  Zoe              50.0%
1002  Ada              90.0%
AVERAGE 70.0%

single student: 1002  Ada              90.0%
```

*Try:* Write the same output to a file with `std::ofstream out("r.txt"); out << book;`. How many lines did you change in `operator<<`?

### 3. Returning a reference to a local

```cpp
#include <iostream>
#include <string>

const std::string& bad() {
    std::string local = "temporary";
    return local;                 // local is destroyed on return
}

int main() {
    std::cout << "built\n";
    return 0;
}
```

*Try:* Build it and read the warning. Then call `bad()` and print the result. What happens? Now explain why returning by value is safe where this is not.

### 4. `this` and chaining

```cpp
#include <iostream>
#include <string>
#include <vector>

class Roster {
public:
    Roster& add(const std::string& name) {
        names_.push_back(name);
        return *this;
    }
    void show() const {
        for (const std::string& n : names_) { std::cout << n << " "; }
        std::cout << "\n";
    }
private:
    std::vector<std::string> names_;
};

int main() {
    Roster r;
    r.add("Ada").add("Grace").add("Alan");
    r.show();
    return 0;
}
```

**Expected output:**

```text
Ada Grace Alan 
```

*Try:* Change `return *this;` to `return this;` and read the error. What is the difference between the two?

### 5. Static members

```cpp
#include <iostream>

class Counter {
public:
    Counter() { ++count_; }
    static int created() { return count_; }
private:
    static int count_;
};

int Counter::count_ = 0;

int main() {
    Counter a;
    Counter b;
    Counter c;
    std::cout << "created: " << Counter::created() << "\n";
    return 0;
}
```

**Expected output:**

```text
created: 3
```

*Try:* Delete the line `int Counter::count_ = 0;` and rebuild. Which tool reports the error — compiler or linker? Chapter 2 Section 2.2.4 explains why.

### 6. Split a class across files

Take the `Student` class from Exercise 1 and split it into `student.h` and `student.cpp` with a header guard. Put the `operator<<` declaration in the header and its definition in the `.cpp`.

Then build with only `main.cpp` and identify which stage produces the error.

### 7. Judge an overload

For each, say whether overloading the operator is a good idea, and why:

- `operator+` on a `Money` class, adding amounts
- `operator+` on a `Student` class
- `operator==` on an `Assignment`, comparing name and points
- `operator<` on a `Student`, meaning "higher percentage"
- `operator[]` on a `Gradebook`, retrieving a student
- `operator<<` on anything you want to print

---

## Summary

- **Take objects by `const&`; return by value.** Never return a reference to a local.
- **`this`** points to the object a member function was called on. `return *this;` enables chaining.
- **One class, one header, one implementation file.** Definitions are prefixed with `ClassName::`. Short accessors may stay in the header; logic goes in the `.cpp`.
- **Headers should include as little as possible.** `<iosfwd>` declares `std::ostream` without the whole library.
- **`operator<<`** is the most valuable overload: a free function taking and returning `std::ostream&`, with the object as `const&`. Because it takes any stream, one definition serves the console, files, and string streams.
- **Overload an operator only when its meaning is obvious.** `operator<` meaning "highest first" is a real trap.
- Overload as a **member** when the left operand is your class; as a **free function** when it is not.
- **Static members** belong to the class, not to objects, and must be defined once outside it.
- The compiler generates a **default constructor, copy constructor, copy assignment, and destructor** — correct for classes holding standard types. Declaring any constructor removes the free default one.
- **`friend` breaks encapsulation deliberately.** Prefer public accessors; v2.6 needs no friends.

---

## Key Terms

**copy assignment** — the operation assigning one existing object to another.

**copy constructor** — the constructor creating an object as a copy of another.

**friend** — a function granted access to a class's private members.

**operator overloading** — defining what an operator means for a user-defined type.

**static member** — a member belonging to the class rather than to any object.

**this** — a pointer, available in member functions, to the object the function was called on.

---

**Next:** Chapter 20 is where Course II pays off. The requirement you deferred in Chapter 1 finally arrives: weighted-category grading. You will see what a flag-and-branch design would cost, then build a small class hierarchy instead — and discover that the classes you spent two chapters encapsulating need no changes at all. Grade Calculator v3.0.
