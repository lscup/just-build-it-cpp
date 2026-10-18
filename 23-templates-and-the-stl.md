# Chapter 23 — Templates and the Standard Template Library

## Learning Objectives

When you finish this chapter you will be able to:

- Write a function template and a class template. *(SLO 2.8)*
- Explain what instantiation means and when it happens. *(SLO 2.8)*
- Choose an appropriate STL container for a purpose. *(SLO 2.5, 2.6)*
- Use iterators and iterator ranges. *(SLO 2.5)*
- Use `std::map` for lookup, indexing, and counting. *(SLO 2.5, 2.6)*
- Write lambda functions and capture values. *(SLO 2.5)*
- Apply standard algorithms rather than hand-written loops. *(SLO 2.5)*
- Explain what namespaces are for. *(SLO 2.8)*
- Build Grade Calculator v3.3 — statistics, grade distribution, and indexed lookup.

---

## 23.1 The Case for Generic Code

Suppose you want the mean of some values. For `double`:

```cpp
double mean(const std::vector<double>& v);
```

For `int`, you write it again. For `float`, again. Three functions, one idea, three places for a bug to live.

The computation does not depend on the type. It needs values that can be added and divided, and nothing else.

**A template writes the family of functions for you.**

You have used templates since Chapter 12. `std::vector<double>` and `std::vector<std::string>` are two instances of one template. This chapter shows how that works and how to write your own.

---

## 23.2 Function Templates

```cpp
template <typename T>
T larger(T a, T b) {
    return (a > b) ? a : b;
}
```

`template <typename T>` says: what follows is a pattern, with `T` standing for a type to be supplied later.

```cpp
larger(3, 7);          // T is int
larger(2.5, 1.5);      // T is double
larger('a', 'z');      // T is char
```

The compiler works out `T` from the arguments and **instantiates** a version for each type actually used. This happens at compile time, so there is no run-time cost — unlike the polymorphism in Chapter 21, which decides at run time.

**A template is not code until it is instantiated.** A template nobody calls is never fully checked, so an error in it may not appear until the first use.

### Requirements are implicit

`larger` requires that `T` supports `>`. Nothing states that, and if you instantiate it with a type lacking `>`, you get an error message pointing *inside* the template rather than at your call.

Template error messages have a reputation for being long, and this is why. **Read from the bottom** — the last few lines usually name your call site and the operation that was missing.

---

## 23.3 Class Templates

A class can be a template too:

```cpp
template <typename T>
class Statistics {
public:
    void add(T value) { values_.push_back(value); }

    std::size_t count() const { return values_.size(); }

    T mean() const {
        if (values_.empty()) { return T{}; }
        T sum = T{};
        for (T v : values_) { sum += v; }
        return sum / static_cast<T>(values_.size());
    }

private:
    std::vector<T> values_;
};
```

The type is given explicitly, because there are no arguments to deduce it from:

```cpp
Statistics<double> percentages;
Statistics<int> counts;
```

```text
double: n=3 mean=75 median=75 stdev=16.3299
int:    n=5 mean=2 median=3
```

Two details worth noticing.

**`T{}` is a value-initialized `T`** — zero for numeric types. Writing `0` would fail for types where zero is not a valid literal.

**`Statistics<int>` reports a mean of 2 for the values 3, 1, 4, 1, 5.** The true mean is 2.8. This is **integer division**, from Chapter 4 Section 4.3, arriving inside a template. The template is not wrong; it faithfully does `T` arithmetic, and for `T = int` that truncates.

This is a genuine hazard of generic code: **a template can be correct for every type and still surprise you for a particular one.** The fix is to compute in `double` and return `T`, or to document that integer instantiations truncate. The Grade Calculator uses `Statistics<double>`, so it does not arise — but knowing why is what lets you avoid it elsewhere.

### Templates live in headers

A template must be visible where it is instantiated, so **template definitions go in the header**, not in a `.cpp`. This is the one place Appendix D Section D.4's declaration/definition split does not apply. `statistics.h` in v3.3 contains complete definitions.

---

## 23.4 The Standard Template Library

The **STL** is the part of the standard library built from templates: containers, iterators, and algorithms.

| Container | Header | Good at | Poor at |
|---|---|---|---|
| `std::vector` | `<vector>` | indexing, adding at the end | inserting in the middle |
| `std::map` | `<map>` | lookup by key, sorted order | nothing much; log-time everything |
| `std::unordered_map` | `<unordered_map>` | fastest lookup by key | no ordering |
| `std::set` | `<set>` | membership, uniqueness, sorted | indexing |
| `std::list` | `<list>` | inserting anywhere | indexing |
| `std::deque` | `<deque>` | adding at both ends | slightly slower indexing |

**Use `std::vector` unless you have a reason not to.** It is the default for good reasons: contiguous memory, fast traversal, simple mental model. The Grade Calculator uses vectors everywhere and adds one `map` in this chapter.

---

## 23.5 Iterators

An **iterator** identifies a position in a container. It generalizes the pointer:

```cpp
std::vector<double> v = {1.0, 2.0, 3.0};

for (auto it = v.begin(); it != v.end(); ++it) {
    std::cout << *it << " ";       // * gives the value, like a pointer
}
```

`v.begin()` is the first element. `v.end()` is **one past the last** — not the last element, which is why the test is `!=` rather than `<=`.

That convention makes an empty range natural: `begin() == end()` means nothing is there.

A pair of iterators is a **range**, and it is what standard algorithms take:

```cpp
std::sort(v.begin(), v.end());
```

A range need not be a whole container — `std::sort(v.begin(), v.begin() + 3)` sorts the first three.

**Prefer a range-based `for` when you want every element.** Iterators matter when you need part of a container, a position, or an algorithm.

---

## 23.6 `std::map`

A **map** stores key–value pairs, keeps them sorted by key, and finds by key in logarithmic time.

```cpp
#include <map>

std::map<int, std::string> byId;
byId[1003] = "Alan";
byId[1001] = "Ada";
byId[1002] = "Grace";
```

```text
  1001 Ada
  1002 Grace
  1003 Alan
```

**Inserted in one order, iterated in another.** A map is always sorted by key.

### Lookup

```cpp
auto it = byId.find(1002);
if (it != byId.end()) {
    std::cout << it->second;       // "Grace"
}
```

`find` returns an iterator, and `end()` means not found. Each element is a pair: `it->first` is the key, `it->second` is the value.

```text
find(1002): Grace
find(9999): not found
```

> **`[]` on a map inserts.** `byId[9999]` creates an entry with a default-constructed value if none exists. That makes `if (byId[id] == "")` quietly grow your map. **Use `find` to look up; use `[]` only when you intend to insert or overwrite.**

### Counting

That insert-on-access behavior is exactly right for counting:

```cpp
std::map<char, int> distribution;
for (char c : {'A','B','A','F','B','A'}) {
    ++distribution[c];             // missing keys start at 0
}
```

```text
  A=3
  B=2
  F=1
```

Three lines for a complete tally, sorted, with no initialization and no check for whether a letter has been seen. This is one of the most useful small patterns in C++.

### `std::unordered_map`

Same interface, faster lookup, **no ordering**. Use it when you never iterate in sorted order and lookup speed matters. For a grade distribution you want the sorted order, so `std::map` is the right choice.

---

## 23.7 Lambda Functions

A **lambda** is an unnamed function written where it is used:

```cpp
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
```

```text
9 5 2 1 
```

The `[]` is the **capture list**, then parameters, then the body.

### Capturing

A lambda can use variables from the surrounding scope by capturing them:

```cpp
double threshold = 4.0;
auto passing = std::count_if(v.begin(), v.end(),
                             [threshold](int x) { return x > threshold; });
```

```text
above 4: 2
```

| Capture | Meaning |
|---|---|
| `[]` | capture nothing |
| `[x]` | capture `x` by value (a copy) |
| `[&x]` | capture `x` by reference |
| `[=]` | capture everything used, by value |
| `[&]` | capture everything used, by reference |

**Prefer naming what you capture.** `[threshold]` says exactly what the lambda depends on; `[=]` and `[&]` hide it, and `[&]` can leave a dangling reference if the lambda outlives what it captured.

### Why this matters for the Grade Calculator

Chapter 19 Section 19.4 raised a concern about `Student::operator<`:

```cpp
std::sort(roster_.begin(), roster_.end());   // sorted by... what?
```

You have to go and read `operator<` to find out — and discover it means "highest percentage first", which is not what `<` suggests.

A lambda puts the ordering where it is used:

```cpp
std::sort(roster_.begin(), roster_.end(),
          [](const Student& a, const Student& b) {
              return a.percentage() > b.percentage();
          });
```

Longer, and it says what it does. **v3.3 makes this change**, and it is a genuine improvement in readability rather than a use of a new feature for its own sake.

---

## 23.8 Standard Algorithms

`<algorithm>` provides tested implementations of common operations.

| Algorithm | Does |
|---|---|
| `std::sort` | sort a range |
| `std::find` | first element equal to a value |
| `std::find_if` | first element satisfying a predicate |
| `std::count` / `std::count_if` | how many match |
| `std::min_element` / `std::max_element` | smallest / largest |
| `std::accumulate` | sum a range *(from `<numeric>`)* |
| `std::for_each` | apply a function to each element |
| `std::any_of` / `std::all_of` | does any / do all satisfy a predicate |
| `std::reverse` | reverse in place |
| `std::transform` | apply a function producing a new range |

The pattern is the same throughout: a range, and often a lambda.

```cpp
auto highest = std::max_element(v.begin(), v.end());
auto failing = std::count_if(roster.begin(), roster.end(),
                             [](const Student& s) { return s.percentage() < 60.0; });
```

**A named algorithm says what it does; a hand-written loop makes you work it out.** `std::count_if` announces its purpose in a way that `for` plus `if` plus `++n` does not.

---

## 23.9 Namespaces

A **namespace** groups names so they do not collide:

```cpp
namespace grading {
    double computePercentage(double earned, double possible);
}

double p = grading::computePercentage(84.0, 100.0);
```

`std` is the standard library's namespace, which is why everything from it is written `std::`.

Appendix D Section D.11 forbids `using namespace std;` for two reasons. It pulls thousands of names into scope, inviting collisions with your own — `std::count` and a variable named `count` is a real conflict. And `std::` tells every reader instantly where a name comes from, which is worth five characters.

In a header the rule is absolute: a `using` directive there is forced on every file that includes it.

The Grade Calculator does not define its own namespaces — it is one program with no name conflicts. You will need them as soon as you combine code from several sources.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| Enormous template error message | A type lacks a required operation | Read from the bottom; find your call site |
| `undefined reference` to a template function | Definition in a `.cpp`, not the header | Move it to the header |
| `Statistics<int>` gives a truncated mean | Integer division inside the template | Compute in `double`, or document it |
| A map grows when you only read from it | `[]` inserts missing keys | Use `find` to look up |
| `error: no match for 'operator*'` on an iterator | Dereferencing `end()` | Check `it != end()` first |
| Lambda compiles but sees stale values | Captured by value, expected reference | Capture by reference deliberately |
| Crash after a lambda outlives its scope | Captured by reference; the referent died | Capture by value |
| `error: 'map' was not declared` | Missing `#include <map>` | Add the header |
| Sorting a map fails to compile | A map is already sorted, and by key | Copy into a vector to sort differently |

---

## Design Notes

**Templates go in headers.** They must be visible where instantiated.

**Use `find` to look up in a map; `[]` only to insert or overwrite.**

**Name what a lambda captures.** `[threshold]` documents the dependency; `[=]` hides it.

**Prefer a named algorithm to a hand-written loop.** It says what it does.

**Put the ordering at the call site.** A lambda beats a surprising `operator<`.

**Use `std::vector` unless you have a reason not to.**

---

## Grade Calculator v3.3 — Generic and Indexed

### What v3.3 does

Everything v3.2 did, plus class statistics, a letter-grade distribution, and lookup by student ID — and the sort now states its ordering where it is used.

### `Statistics<T>`

A template, in a header, computing over any numeric type:

```cpp
// statistics.h
template <typename T>
class Statistics {
public:
    void add(T value) { values_.push_back(value); }

    std::size_t count() const { return values_.size(); }
    bool empty() const { return values_.empty(); }

    T mean() const;
    T median() const;
    T lowest() const;
    T highest() const;

    /** Population standard deviation. Zero for fewer than two values. */
    double standardDeviation() const;

private:
    std::vector<T> values_;
};
```

`median` copies before sorting, so the caller's data is untouched:

```cpp
T median() const {
    if (values_.empty()) { return T{}; }
    std::vector<T> sorted = values_;          // copy: do not disturb the caller
    std::sort(sorted.begin(), sorted.end());
    std::size_t mid = sorted.size() / 2;
    if (sorted.size() % 2 == 1) { return sorted[mid]; }
    return (sorted[mid - 1] + sorted[mid]) / static_cast<T>(2);
}
```

**Why a template here at all?** The Grade Calculator only ever uses `Statistics<double>`. The honest answer is that it demonstrates the technique, and that the class is genuinely reusable elsewhere. A template used at exactly one type is not obviously better than a plain class — this one earns its keep by being independently testable and portable to your next program, not by being generic in this one.

### An ID index with `std::map`

```cpp
private:
    // An index from student ID to roster position. std::map keeps its keys
    // sorted and looks up in logarithmic time, replacing the hand-written
    // binary search of Chapter 17 - and it stays correct as students are added.
    std::map<int, std::size_t> idIndex_;
```

```cpp
const Student* Gradebook::findById(int id) const {
    auto it = idIndex_.find(id);
    if (it == idIndex_.end()) { return nullptr; }
    return &roster_[it->second];
}
```

Compare with Chapter 17. The binary search needed the roster sorted by ID, so searching meant sorting a copy first — and any change to the roster invalidated the assumption. **The map maintains itself.**

Returning `nullptr` for "not found" is the same convention Chapter 17 used, with the same weakness: a caller who forgets to check will dereference it. Chapter 24 replaces it.

### The index must be maintained

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
    idIndex_[s.id()] = roster_.size() - 1;
}
```

And critically:

```cpp
void Gradebook::sortByPercentage() {
    const Gradebook* self = this;
    std::sort(roster_.begin(), roster_.end(),
              [self](const Student& a, const Student& b) {
                  return self->percentageFor(a) > self->percentageFor(b);
              });
    // Sorting moved every student, so the ID index must be rebuilt.
    idIndex_.clear();
    for (std::size_t i = 0; i < roster_.size(); ++i) {
        idIndex_[roster_[i].id()] = i;
    }
}
```

**An index is derived data, and derived data goes stale.** Sorting invalidates every stored position, so the index is rebuilt. Forgetting this would produce a silent logic error of exactly the kind Chapter 4 Section 4.9.3 described — lookups returning the wrong student.

That rebuild is the real cost of the index, and it is worth stating plainly: an index is only worth keeping when lookups substantially outnumber the operations that invalidate it.

### The lambda captures `this`

Note `[self]` in the sort. The comparison needs `percentageFor`, which is a member function, so the lambda must reach the object. Capturing a pointer to it explicitly — rather than the terser `[this]` or `[=]` — makes the dependency visible, per the Design Notes.

### Grade distribution

```cpp
std::map<char, int> Gradebook::letterDistribution() const {
    std::map<char, int> counts;
    for (const Student& s : roster_) {
        ++counts[scale_.letterFor(percentageFor(s))];   // missing keys start at 0
    }
    return counts;
}
```

The counting pattern from Section 23.6, and the result arrives sorted by letter for free.

### Expected output

Three students at 95%, 75%, and 55%:

```text
  Students : 3
  Mean     : 75.0%
  Median   : 75.0%
  Range    : 55.0% to 95.0%
  Std dev  : 16.3
  Grades   : A=1  C=1  F=1  
```

Check the standard deviation by hand: deviations from the mean are +20, 0, −20; squares 400, 0, 400; mean square 800/3 ≈ 266.67; square root ≈ 16.33.

### Your StudySite Lab — Add Generic Statistics and an ID Index

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.3
- **Starting point:** Your committed Chapter 22 v3.2 program (eleven files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### What you will build

In this lab you put the Standard Template Library to work and write a class
template of your own. By the end you will have:

1. **`Statistics<T>`**, a header-only class template that computes count,
   mean, median, lowest, highest, and standard deviation for any numeric type.
2. An **ID index** — a `std::map<int, std::size_t>` from student ID to roster
   position — that `Gradebook` keeps up to date, and a `findById` member that
   uses it.
3. A **letter-grade distribution** counted with a `std::map<char, int>`.
4. `sortByPercentage` rewritten with a **lambda** that states the ordering
   right where the sort happens.
5. Two new menu options: **Statistics** and **Find by ID**. Quit moves to
   option 8.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `statistics.h` | Create (Step 1) — a header only; there is no `statistics.cpp` |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 2–5) |
| `main.cpp` | Edit (Step 6) |
| All other files | **No change** — keep them open |

When you are finished your project has **twelve files**.

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

#### Build it: step by step

##### Step 1 — Write the `Statistics<T>` class template

Create a new file named `statistics.h` and enter this code:

```cpp
// statistics.h - Grade Calculator v3.3 - Chapter 23
#ifndef STATISTICS_H
#define STATISTICS_H

#include <algorithm>
#include <cmath>
#include <vector>

/**
 * Descriptive statistics over any numeric type.
 *
 * Written as a template because the computation does not depend on whether the
 * values are double percentages, int point totals, or float weights. One
 * definition serves them all; the compiler generates a version per type used.
 */
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

#endif
```

- `template <typename T>` makes `Statistics` a **blueprint**. When you write
  `Statistics<double>`, the compiler generates a version of the class with
  every `T` replaced by `double`.
- The entire template is in the header. The compiler needs the full
  definition at the point where `Statistics<double>` is used, so a class
  template normally has **no `.cpp` file**.
- `T{}` is a value-initialized `T` — `0.0` for a `double` — and is returned
  when there is no data.
- `median()` **copies** the values before sorting, so asking for the median
  does not rearrange the caller's data.
- `std::min_element` and `std::max_element` from `<algorithm>` return
  iterators; the `*` in front reads the value they point to.

##### Step 2 — Declare the new `Gradebook` members (`gradebook.h`)

In `gradebook.h`, find the first line:

```cpp
// gradebook.h - Grade Calculator v3.2 - Chapter 22
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v3.3 - Chapter 23
```

Find the standard-library include:

```cpp
#include <iosfwd>
```

Directly below it, add:

```cpp
#include <map>
```

Find the declaration of `sortByPercentage`:

```cpp
    void sortByPercentage();
```

Directly below it, add:

```cpp

    /** Finds a student by ID in O(log n) using the id index. Null if absent. */
    const Student* findById(int id) const;

    /** How many students earned each letter grade, in scale order. */
    std::map<char, int> letterDistribution() const;

    /** Prints mean, median, range, and standard deviation for the class. */
    void printStatistics(std::ostream& out) const;
```

In the `private:` section, find:

```cpp
    std::vector<Student> roster_;
```

Directly below it, add:

```cpp

    // An index from student ID to roster position. std::map keeps its keys
    // sorted and looks up in logarithmic time, replacing the hand-written
    // binary search of Chapter 17 - and it stays correct as students are added.
    std::map<int, std::size_t> idIndex_;
```

- `findById` returns a **pointer** to the student, or `nullptr` if there is no
  such ID. A pointer can say "nothing found"; a reference cannot.
- `letterDistribution` returns a `std::map<char, int>`: each letter grade
  mapped to how many students earned it.
- `printStatistics` writes to whatever `std::ostream` it is given — the
  screen today, a file tomorrow.
- `idIndex_` maps an ID (the **key**) to the student's position in `roster_`
  (the **value**). A `std::map` keeps its keys sorted and finds a key in
  logarithmic time — the job Chapter 17's binary search did, without needing
  a sorted copy of the roster.

##### Step 3 — Keep the index current, and look students up (`gradebook.cpp`)

In `gradebook.cpp`, find the first line:

```cpp
// gradebook.cpp - Grade Calculator v3.2 - Chapter 22
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v3.3 - Chapter 23
```

Find the first includes:

```cpp
#include "gradebook.h"

#include <algorithm>
```

Replace it with:

```cpp
#include "gradebook.h"

#include "statistics.h"

#include <algorithm>
#include <map>
```

Find `addStudent`:

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
}
```

Replace it with:

```cpp
void Gradebook::addStudent(const Student& s) {
    roster_.push_back(s);
    idIndex_[s.id()] = roster_.size() - 1;
}

const Student* Gradebook::findById(int id) const {
    auto it = idIndex_.find(id);
    if (it == idIndex_.end()) { return nullptr; }
    return &roster_[it->second];
}
```

- In `addStudent`, the new student was just pushed onto the end of the
  roster, so its position is `roster_.size() - 1`. That position is stored in
  the index under the student's ID.
- `idIndex_.find(id)` returns an **iterator**. If it equals `idIndex_.end()`,
  the ID is not in the map. Otherwise `it->second` is the stored position.
  `auto` lets the compiler spell out the long iterator type for you.

> **▶ Run checkpoint:** Open `statistics.h` along with the other files and click **Run**. The program should compile cleanly and behave exactly like v3.2. `letterDistribution` and `printStatistics` are declared but not yet defined; that is allowed as long as nothing calls them, and nothing does yet.

##### Step 4 — Count letter grades and compute statistics (`gradebook.cpp`)

Directly below the `findById` function you just added — after this code:

```cpp
    return &roster_[it->second];
}
```

Directly below it, add:

```cpp

std::map<char, int> Gradebook::letterDistribution() const {
    std::map<char, int> counts;
    for (const Student& s : roster_) {
        ++counts[scale_.letterFor(percentageFor(s))];   // missing keys start at 0
    }
    return counts;
}

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
}
```

(The first line in the box is blank on purpose: leave one blank line between
`findById` and the new code.)

- `++counts[letter]` is the standard **counting idiom** for a map. If `letter`
  is not in the map yet, `operator[]` inserts it with the value `0`, and `++`
  makes it `1`. Because a `std::map` is sorted by key, the counts come back in
  letter order.
- `printStatistics` fills a `Statistics<double>` with every student's course
  percentage, then prints the results. It uses `percentageFor`, so the
  statistics follow the chosen grading scheme.
- `for (const auto& entry : letterDistribution())` walks the map;
  `entry.first` is the letter and `entry.second` is the count.

##### Step 5 — Sort with a lambda, and rebuild the index (`gradebook.cpp`)

In `sortByPercentage`, find:

```cpp
    std::sort(roster_.begin(), roster_.end());   // uses Student::operator<
```

Replace it with:

```cpp
    // A lambda states the ordering right where it is used, instead of relying
    // on operator< to mean "by percentage, descending" everywhere.
    const Gradebook* self = this;
    std::sort(roster_.begin(), roster_.end(),
              [self](const Student& a, const Student& b) {
                  return self->percentageFor(a) > self->percentageFor(b);
              });
    // Sorting moved every student, so the ID index must be rebuilt.
    idIndex_.clear();
    for (std::size_t i = 0; i < roster_.size(); ++i) {
        idIndex_[roster_[i].id()] = i;
    }
```

- The **lambda** `[self](const Student& a, const Student& b) { ... }` is the
  comparison, written right where it is used. You no longer have to go read
  `Student::operator<` to find out what order the sort produces.
- The lambda needs `percentageFor`, a `Gradebook` member, so it **captures** a
  pointer to the gradebook, `self`, by listing it in the square brackets.
- **An index is derived data, and derived data goes stale.** Sorting moves
  every student to a new position, so every position stored in `idIndex_` is
  now wrong. The loop clears the index and rebuilds it from the sorted roster.
  Forget this, and *Find by ID* silently returns the wrong student.

##### Step 6 — Add *Statistics* and *Find by ID* to the menu (`main.cpp`)

At the top of `main.cpp`, find these lines of the header comment:

```cpp
//  Grade Calculator  v3.2                                          Chapter 22
// -----------------------------------------------------------------------------
//  Change  : Ownership. The raw GradingScheme* becomes std::unique_ptr.
//            Gradebook loses its destructor, its manual delete, and its
//            deleted copy operations - 8 lines of bookkeeping for 0.
//            Behavior is identical to v3.1; both builds are leak-free.
//  Point   : v3.1 is correct because its author remembered three separate
//            things. v3.2 is correct because there is nothing to remember.
//  Verify  : build both with -fsanitize=address, switch schemes, exit.
//            Neither leaks. Then delete Gradebook::~Gradebook from v3.1 and
//            rerun: v3.1 now leaks, v3.2 cannot be broken the same way.
```

Replace it with:

```cpp
//  Grade Calculator  v3.3                                          Chapter 23
// -----------------------------------------------------------------------------
//  Change  : Templates and the STL. Statistics<T> computes mean, median,
//            range, and standard deviation for any numeric type. std::map
//            indexes students by ID and counts the letter distribution.
//            Sorting is expressed with a lambda instead of operator<.
```

At the start of `main`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.2 (leak-free) ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.3 (statistics) ===\n\n";
```

Find the menu prompt:

```cpp
        std::cout << "\n1) Add student  2) Report  3) Sort  "
                     "4) Custom scale  5) Change scheme  6) Quit\nChoice: ";
```

Replace it with:

```cpp
        std::cout << "\n1) Add student  2) Report  3) Sort  "
                     "4) Custom scale  5) Change scheme\n"
                     "6) Statistics  7) Find by ID  8) Quit\nChoice: ";
```

Near the end of the menu loop, find:

```cpp
        } else if (c == '6') {
            running = false;
        } else {
            std::cout << "  Please enter 1-6.\n";
```

Replace it with:

```cpp
        } else if (c == '6') {
            std::cout << "\n--- Class statistics ---\n";
            book.printStatistics(std::cout);
        } else if (c == '7') {
            std::string s = readLine("  Student ID: ");
            int id = 0;
            try { id = std::stoi(s); }
            catch (...) { std::cout << "  Not a valid ID.\n"; continue; }
            const Student* found = book.findById(id);
            if (found != nullptr) {
                std::cout << "  " << found->name() << ": "
                          << book.percentageFor(*found) << "%\n";
            } else {
                std::cout << "  No student with ID " << id << ".\n";
            }
        } else if (c == '8') {
            running = false;
        } else {
            std::cout << "  Please enter 1-8.\n";
```

- **Statistics** (option 6) passes `std::cout` to `printStatistics`.
- **Find by ID** (option 7) converts the typed ID with `std::stoi`, catching
  bad input, then asks `book.findById(id)`. Always compare the result with
  `nullptr` before using it — dereferencing a null pointer crashes the
  program.
- **Quit** moves to option 8.

> **▶ Run checkpoint:** Make sure all twelve files are open and click **Run**. The program should compile with no errors and no warnings and show the eight-option menu.

#### Check your work

Choose `1` (Points-based). Add three students, each with one assignment
(category: press Enter):

| Student | Assignment | Earned | Possible | Bonus |
|---|---|---|---|---|
| `Ana` | `Test` | 95 | 100 | 0 |
| `Ben` | `Test` | 75 | 100 | 0 |
| `Cy` | `Test` | 55 | 100 | 0 |

1. Choose `6` (Statistics). You should see:

   ```text
   --- Class statistics ---
     Students : 3
     Mean     : 75.0%
     Median   : 75.0%
     Range    : 55.0% to 95.0%
     Std dev  : 16.3
     Grades   : A=1  C=1  F=1
   ```

   Check the standard deviation by hand: the deviations from the mean are
   +20, 0, −20; their squares average 800 ÷ 3 ≈ 266.67; √266.67 ≈ 16.3.
2. Choose `7` and enter `1002`. You should see `Ben: 75.0%`.
3. Choose `7` and enter `99`. You should see `No student with ID 99.`
4. Choose `3` (Sort), then `7` with `1002` again. It must still find `Ben` —
   proof that the index was rebuilt after sorting.
5. Choose `8` (Quit).

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] `statistics.h` has an include guard and there is no `statistics.cpp`.
- [ ] `addStudent` updates `idIndex_`, and `sortByPercentage` rebuilds it.
- [ ] Every use of `findById` checks for `nullptr`.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click all eleven project files to open them. You will create `statistics.h` during the lab.
   Confirm the editor shows the expected file paths before editing.
4. Work through Steps 1–6 above in StudySite's internal editor, in order, clicking **Run** at each ▶ Run checkpoint.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

> **Compiling:** In StudySite.ai, just click **Run**. StudySite generates the
> compile command for you, then builds and runs the program in one step, so
> you never type one here. The `Build` line in `main.cpp`'s header comment is
> for building on your own computer instead. For this chapter:
>
> **macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):
>
> ```bash
> clang++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — all twelve files, including the new `statistics.h`. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 23 Grade Calculator v3.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 23
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. A class template at two types

```cpp
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

template <typename T>
class Statistics {
public:
    void add(T v) { values_.push_back(v); }
    std::size_t count() const { return values_.size(); }
    T mean() const {
        if (values_.empty()) { return T{}; }
        T s = T{};
        for (T v : values_) { s += v; }
        return s / static_cast<T>(values_.size());
    }
    T median() const {
        if (values_.empty()) { return T{}; }
        std::vector<T> s = values_;
        std::sort(s.begin(), s.end());
        std::size_t m = s.size() / 2;
        return s.size() % 2 ? s[m] : (s[m - 1] + s[m]) / static_cast<T>(2);
    }
private:
    std::vector<T> values_;
};

int main() {
    Statistics<double> pct;
    for (double v : {95.0, 55.0, 75.0}) { pct.add(v); }
    std::cout << "double: mean=" << pct.mean() << " median=" << pct.median() << "\n";

    Statistics<int> counts;
    for (int v : {3, 1, 4, 1, 5}) { counts.add(v); }
    std::cout << "int:    mean=" << counts.mean() << " median=" << counts.median() << "\n";
    return 0;
}
```

**Expected output:**

```text
double: mean=75 median=75
int:    mean=2 median=3
```

*Try:* The integer mean should be 2.8. Explain the 2. Then change `mean` to compute in `double` and return `T` — what does the integer version report now?

### 2. `std::map` for lookup

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<int, std::string> byId;
    byId[1003] = "Alan";
    byId[1001] = "Ada";
    byId[1002] = "Grace";

    for (const auto& entry : byId) {
        std::cout << "  " << entry.first << " " << entry.second << "\n";
    }

    auto it = byId.find(1002);
    std::cout << "find(1002): " << (it != byId.end() ? it->second : "not found") << "\n";
    std::cout << "find(9999): "
              << (byId.find(9999) != byId.end() ? "found" : "not found") << "\n";
    std::cout << "size after lookups: " << byId.size() << "\n";
    return 0;
}
```

**Expected output:**

```text
  1001 Ada
  1002 Grace
  1003 Alan
find(1002): Grace
find(9999): not found
size after lookups: 3
```

*Try:* Replace `byId.find(9999) != byId.end()` with `byId[9999] != ""` and print the size again. What happened, and why is `find` the right tool for looking up?

### 3. Counting with a map

```cpp
#include <iostream>
#include <map>

int main() {
    std::map<char, int> dist;
    for (char c : {'A','B','A','F','B','A'}) { ++dist[c]; }
    for (const auto& e : dist) { std::cout << "  " << e.first << "=" << e.second << "\n"; }
    return 0;
}
```

**Expected output:**

```text
  A=3
  B=2
  F=1
```

*Try:* Note that no key was initialized and no check for "seen before" was needed. Which map behavior makes that work? Now do the same with `std::unordered_map` — what changes about the output?

### 4. Lambdas and capture

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {5, 2, 9, 1};

    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
    for (int x : v) { std::cout << x << " "; }
    std::cout << "\n";

    int threshold = 4;
    auto above = std::count_if(v.begin(), v.end(),
                               [threshold](int x) { return x > threshold; });
    std::cout << "above " << threshold << ": " << above << "\n";
    return 0;
}
```

**Expected output:**

```text
9 5 2 1 
above 4: 2
```

*Try:* Change `[threshold]` to `[]` and read the error. Then change it to `[&threshold]` and modify `threshold` between the definition and the call — does the lambda see the new value?

### 5. Iterators explicitly

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<double> v = {1.0, 2.0, 3.0};

    for (auto it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << "\n";
    std::cout << "first: " << *v.begin() << "\n";
    std::cout << "size:  " << (v.end() - v.begin()) << "\n";
    return 0;
}
```

**Expected output:**

```text
1 2 3 
first: 1
size:  3
```

*Try:* Print `*v.end()` and see what happens. Why is `end()` one past the last element rather than the last?

### 6. Replace loops with algorithms

Rewrite each using a standard algorithm and a lambda:

```cpp
// count students below 60
int failing = 0;
for (const Student& s : roster) {
    if (s.percentage() < 60.0) { ++failing; }
}
```

```cpp
// find the highest percentage
double highest = roster[0].percentage();
for (const Student& s : roster) {
    if (s.percentage() > highest) { highest = s.percentage(); }
}
```

```cpp
// are all students passing?
bool allPass = true;
for (const Student& s : roster) {
    if (s.percentage() < 60.0) { allPass = false; }
}
```

Which version reads better? Does your answer change if the loop body were three lines longer?

### 7. Reason about templates and containers

- When is a template instantiated, and what does that mean for run-time cost?
- Why must template definitions live in headers?
- Why does `std::map::operator[]` insert, and when is that helpful rather than dangerous?
- What is the difference between `std::map` and `std::unordered_map`, and when does it matter?
- Why prefer `[threshold]` to `[=]`?
- You need to look up a student by ID 10,000 times on a roster that never changes. Which of a linear scan, a sorted vector with binary search, or a map would you choose?

---

## Summary

- A **template** is a pattern from which the compiler generates code for each type used. **Instantiation** happens at compile time, so there is no run-time cost.
- Template requirements are **implicit**, which is why error messages are long. **Read from the bottom.**
- **Template definitions go in headers**, because they must be visible where instantiated.
- A template can be correct for every type and still surprise you for one — `Statistics<int>` truncates because `T` arithmetic on `int` is integer division.
- The **STL** provides containers, iterators, and algorithms. **Use `std::vector` unless you have a reason not to.**
- An **iterator** identifies a position. `begin()` is the first element; `end()` is **one past the last**. A pair of iterators is a **range**.
- **`std::map`** stores key–value pairs sorted by key, with logarithmic lookup. **`[]` inserts missing keys** — use `find` to look up, `[]` to insert or count.
- The **counting idiom** `++counts[key]` needs no initialization and no membership test.
- A **lambda** is an unnamed function written where it is used. **Name what you capture.**
- Putting a sort's ordering in a **lambda at the call site** is clearer than a surprising `operator<`.
- **Standard algorithms** say what they do. Prefer them to hand-written loops.
- **Namespaces** prevent name collisions. Never write `using namespace std;`.
- **An index is derived data and goes stale.** Sorting the roster invalidates the ID index, so it is rebuilt.

---

## Key Terms

**algorithm (STL)** — a standard function operating on an iterator range.

**capture list** — the `[]` of a lambda, naming what it takes from the surrounding scope.

**class template** — a class parameterized by one or more types.

**container** — a class holding a collection of objects.

**function template** — a function parameterized by one or more types.

**instantiation** — the compiler's generation of concrete code from a template for a given type.

**iterator** — an object identifying a position in a container.

**lambda** — an unnamed function defined where it is used.

**map** — an associative container of key–value pairs, sorted by key.

**namespace** — a named scope grouping declarations to prevent collisions.

**range** — a pair of iterators marking the beginning and one-past-the-end of a sequence.

**STL** — the Standard Template Library: containers, iterators, and algorithms.

**template parameter** — the placeholder type in a template, conventionally `T`.

**unordered_map** — a hash-based associative container with faster lookup and no ordering.

---

**Next:** Chapter 24 ships the release. Errors become exceptions with a custom hierarchy, so an invalid grade scale is refused rather than quietly repaired. You will revisit the translation pipeline from Chapter 2 with full understanding, produce a release build and a user guide, and reconcile your design document against the specification you wrote in Chapter 5 — closing a requirement traced across two courses. Grade Calculator v4.0.
