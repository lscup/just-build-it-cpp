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

Everything v2.5 did, reorganized: a `Gradebook` class owns the roster and the scale, reports print through `operator<<`, and every class lives in its own header and implementation file.

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
- **Starting point:** The working Chapter 18 v2.5 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Create one header and one implementation file for each class; keep `main.cpp` focused on application flow.
2. Add include guards and keep implementation details out of headers.
3. Create a `Gradebook` class that owns the roster, assignments, scale, and reporting operations.
4. Implement `operator<<` for Assignment, Student, GradeScale, and Gradebook using public accessors.
5. Add checked `at` access alongside unchecked `operator[]`.


#### Verification

- Every source file builds as one program.
- Writing a Gradebook to the Terminal and to a file uses the same `operator<<`.
- Checked access rejects an invalid index.
- The Chapter 18 behavior is unchanged.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437F26-Grade-Calculator-YourLastName**, and click each source,
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
3. Select **COSC1437F26-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 19 Grade Calculator v2.6**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **COSC1437F26-Grade-Calculator-YourLastName** contains the Chapter 19
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
