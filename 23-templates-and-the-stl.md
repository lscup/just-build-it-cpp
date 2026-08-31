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
- **Starting point:** The working Chapter 22 v3.2 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Create header-only `Statistics<T>` with mean, median, minimum, maximum, and population standard deviation.
2. Add a `std::map` index from student ID to roster position and maintain it whenever the roster changes order.
3. Add `findById` using the index.
4. Replace the implicit Student ordering with a lambda at the sort call.
5. Add class statistics, letter-grade distribution, and assignment count by category.


#### Verification

- `Statistics<double>` and `Statistics<int>` are both exercised.
- ID lookup works before and after sorting.
- A regression test fails if the index rebuild is removed.
- The reported statistics match a hand calculation.

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
4. Enter the commit message **Complete Chapter 23 Grade Calculator v3.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **COSC1437F26-Grade-Calculator-YourLastName** contains the Chapter 23
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
