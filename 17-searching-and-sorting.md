# Chapter 17 — Searching and Sorting

## Learning Objectives

When you finish this chapter you will be able to:

- Implement and trace a linear search. *(SLO 2.5)*
- Implement and trace a binary search, and state its precondition. *(SLO 2.5)*
- Implement selection sort and insertion sort, and trace each pass. *(SLO 2.5)*
- Describe merge sort and the divide-and-conquer idea. *(SLO 2.5)*
- Compare algorithms by counting operations rather than by timing alone. *(SLO 2.5)*
- Sort by different criteria using a comparison function. *(SLO 2.5, 2.8)*
- Use `std::sort` and `std::find` from the standard library. *(SLO 2.5)*
- Build Grade Calculator v2.4 — a sortable, searchable roster.

---

## 17.1 Why Algorithm Choice Matters

Item five on your Chapter 13 backlog: sort and search the roster. *Perfective* maintenance.

Two things make this chapter different from what came before. These are the first named **algorithms** in the book — general procedures with known properties, not code written for one situation. And it is the first time the *choice* between two correct programs matters, because both give the right answer and one takes far longer.

With 30 students, any approach works. With 30,000, the difference is the difference between instant and unusable. Knowing which is which is the skill.

---

## 17.2 Linear Search

Look at each element in turn until you find what you want:

```cpp
int linearSearchById(const std::vector<Student>& roster, int id, int& comparisons) {
    comparisons = 0;
    for (std::size_t i = 0; i < roster.size(); ++i) {
        ++comparisons;
        if (roster[i].id == id) {
            return static_cast<int>(i);
        }
    }
    return -1;      // not found
}
```

Returning −1 for "not found" is a common convention. It works only because a valid index is never negative — and Chapter 24 replaces it with something better, because a caller who forgets to check −1 will use it as an index.

**Linear search works on any data, in any order.** That is its whole appeal, and it is not a small one.

| Case | Comparisons |
|---|---|
| Found first | 1 |
| Found in the middle | about *n*/2 |
| Found last, or absent | *n* |

Doubling the roster doubles the work. That relationship — work proportional to *n* — is what makes it a **linear** search.

---

## 17.3 Binary Search

If the data is **sorted**, you can do far better. Look at the middle. If it is what you want, stop. If your target is smaller, everything to the right is eliminated; if larger, everything to the left is. Repeat on what remains.

```cpp
int binarySearchById(const std::vector<Student>& roster, int id, int& comparisons) {
    comparisons = 0;
    int low = 0;
    int high = static_cast<int>(roster.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        ++comparisons;
        if (roster[mid].id == id)     { return mid; }
        else if (roster[mid].id < id) { low = mid + 1; }
        else                          { high = mid - 1; }
    }
    return -1;
}
```

### The precondition

**Binary search requires sorted data.** On unsorted data it does not merely run slowly — it gives wrong answers, reporting that a present element is absent. That is a logic error of the Chapter 4 Section 4.9.3 kind: silent and confident.

This is a `@pre` in the sense of Chapter 9 Section 9.8, and it should be documented:

```cpp
/**
 * @pre roster is sorted by id, ascending. Results are meaningless otherwise.
 */
```

### Why `low + (high - low) / 2`

The obvious midpoint is `(low + high) / 2`. It is subtly wrong: for very large values, `low + high` can overflow — Chapter 3 Section 3.4's wraparound, in a real algorithm. The form above cannot overflow and is worth writing by habit.

### The trade-off

Each comparison eliminates half of what remains, so the work grows with the *logarithm* of *n*:

| Roster size | Linear (worst) | Binary (worst) |
|---|---|---|
| 10 | 10 | 4 |
| 100 | 100 | 7 |
| 1,000 | 1,000 | 10 |
| 1,000,000 | 1,000,000 | 20 |

A million students, twenty comparisons. That is not a small improvement; it is a different category of thing.

But look at a small case measured honestly. Searching for all five keys in a five-element vector:

```text
linear search, all 5 keys: 15 comparisons
binary search, all 5 keys: 11 comparisons
```

Barely better — and that ignores the cost of sorting in the first place. **Binary search only pays when the data is already sorted, or when you will search many times.** Sorting once to search once is worse than not sorting at all.

---

## 17.4 Selection Sort

Repeatedly find the smallest remaining element and move it into place.

```cpp
void selectionSort(std::vector<int>& a) {
    for (std::size_t i = 0; i + 1 < a.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < a.size(); ++j) {
            if (a[j] < a[best]) { best = j; }
        }
        if (best != i) { std::swap(a[i], a[best]); }
    }
}
```

Traced on `64 25 12 22 11`:

| Pass | Result | What happened |
|---|---|---|
| start | `64 25 12 22 11` | |
| 1 | `11 25 12 22 64` | smallest (11) swapped to front |
| 2 | `11 12 25 22 64` | smallest of the rest (12) into place |
| 3 | `11 12 22 25 64` | 22 into place |
| 4 | `11 12 22 25 64` | already correct |

```text
start:  64 25 12 22 11 
pass 1: 11 25 12 22 64 
pass 2: 11 12 25 22 64 
pass 3: 11 12 22 25 64 
pass 4: 11 12 22 25 64 
```

**The left portion is sorted and final; the right is unexamined.** That invariant is what makes it easy to trace by hand, which is why this book starts here.

Selection sort makes *n*(*n*−1)/2 comparisons **regardless of the input**. Already-sorted data takes just as long as random data. It does, however, make at most *n*−1 swaps, which matters when moving elements is expensive.

---

## 17.5 Insertion Sort

Take each element and insert it into its correct position among those already handled — the way most people sort a hand of cards.

```cpp
void insertionSort(std::vector<int>& a) {
    for (std::size_t i = 1; i < a.size(); ++i) {
        int key = a[i];
        std::size_t j = i;
        while (j > 0 && a[j - 1] > key) {
            a[j] = a[j - 1];
            --j;
        }
        a[j] = key;
    }
}
```

Same data:

| Pass | Result | What happened |
|---|---|---|
| start | `64 25 12 22 11` | |
| 1 | `25 64 12 22 11` | 25 inserted before 64 |
| 2 | `12 25 64 22 11` | 12 inserted at the front |
| 3 | `12 22 25 64 11` | 22 inserted after 12 |
| 4 | `11 12 22 25 64` | 11 inserted at the front |

```text
start:  64 25 12 22 11 
pass 1: 25 64 12 22 11 
pass 2: 12 25 64 22 11 
pass 3: 12 22 25 64 11 
pass 4: 11 12 22 25 64 
```

Here the left portion is sorted **among itself** but not final — later elements still move into it.

Insertion sort's advantage is that it **adapts to its input**. On nearly-sorted data the inner `while` barely runs, and the whole thing approaches *n* comparisons. On reversed data it is as bad as selection sort. Real data is often nearly sorted, which makes this a better default than its reputation suggests.

---

## 17.6 Bubble Sort and Its Reputation

Bubble sort repeatedly walks the data swapping adjacent out-of-order pairs, so large values "bubble" to the end.

It is famous because it is easy to explain, and it is not recommended. It does the same number of comparisons as selection sort while making far more swaps. Insertion sort is simpler to write correctly and faster on nearly every input.

It is mentioned here so you recognize the name, and so you know that meeting it in older code is not evidence that it was a good choice.

---

## 17.7 Merge Sort and Divide and Conquer

Selection and insertion sort both do work proportional to *n*². Doubling the data quadruples the time. For 30 students that is nothing; for 30,000 it is fatal.

**Merge sort** does better with a different strategy — **divide and conquer**:

1. If the data has 0 or 1 elements, it is already sorted. *(base case)*
2. Otherwise, split it in half.
3. Sort each half — by the same method, recursively.
4. **Merge** the two sorted halves into one sorted whole.

Step 4 is where the work happens, and it is easy: with two sorted lists, repeatedly take the smaller of the two front elements.

This is the recursion from Chapter 10 Section 10.4 doing something a loop cannot express as naturally. The splitting is self-similar all the way down, and the base case is reached because each split is strictly smaller.

Merge sort does work proportional to *n* log *n*:

| Size | *n*² (roughly) | *n* log *n* (roughly) |
|---|---|---|
| 100 | 10,000 | 700 |
| 1,000 | 1,000,000 | 10,000 |
| 10,000 | 100,000,000 | 130,000 |

At 10,000 elements the difference is a factor of several hundred.

Merge sort's cost is memory: merging needs somewhere to put the result. Selection and insertion sort work in place.

---

## 17.8 Comparing Algorithms

The honest way to compare algorithms is to **count operations**, not to time them. Timing depends on the machine, the compiler, and what else is running; a comparison count is a property of the algorithm.

| Algorithm | Comparisons (worst) | Best case | Extra memory | Adapts to input |
|---|---|---|---|---|
| Linear search | *n* | 1 | none | — |
| Binary search | log₂ *n* | 1 | none | requires sorted data |
| Selection sort | *n*²/2 | *n*²/2 | none | **no** |
| Insertion sort | *n*²/2 | *n* | none | **yes** |
| Merge sort | *n* log *n* | *n* log *n* | *n* | no |

Two habits follow.

**Instrument your code to count.** The `comparisons` reference parameter in Sections 17.2 and 17.3 exists for this. A measured count settles an argument that estimation cannot.

**Measure on your actual data.** Merge sort beats insertion sort asymptotically and loses on small or nearly-sorted inputs, which is why real library implementations switch between strategies by size.

---

## 17.9 Sorting by Different Criteria

A roster might be sorted by name, by percentage, or by ID. Writing three sorts would be three chances to get it wrong.

Instead, pass the comparison in. A **function pointer** holds the address of a function:

```cpp
typedef bool (*StudentComparer)(const Student&, const Student&,
                                const std::vector<Assignment>&);

bool byName(const Student& a, const Student& b, const std::vector<Assignment>&) {
    return a.name < b.name;
}

bool byId(const Student& a, const Student& b, const std::vector<Assignment>&) {
    return a.id < b.id;
}
```

Then one sort serves all orderings:

```cpp
void selectionSort(std::vector<Student>& roster,
                   const std::vector<Assignment>& as,
                   StudentComparer comesFirst) {
    for (std::size_t i = 0; i + 1 < roster.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < roster.size(); ++j) {
            if (comesFirst(roster[j], roster[best], as)) { best = j; }
        }
        if (best != i) { std::swap(roster[i], roster[best]); }
    }
}
```

**The algorithm and the ordering are now separate concerns.** Adding a new ordering means writing one small function; the sort is untouched.

Note that `byName` and `byId` ignore their third parameter — it is unnamed for exactly that reason, which is how you tell the compiler an unused parameter is deliberate. They must accept it because they all need one signature.

> This is worth remembering. In Chapter 20 you will meet the same problem in a larger form: several ways to compute a grade, and code that should not have to know which. The solution there is a class hierarchy, and function pointers are its ancestor.

---

## 17.10 Library Sorting and Searching

You will rarely write a sort in production. `<algorithm>` provides tested implementations:

```cpp
#include <algorithm>

std::sort(v.begin(), v.end());                                   // ascending
std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; }); // descending
```

```text
ascending:  11 12 22 25 64 
descending: 64 25 22 12 11 
```

`v.begin()` and `v.end()` are **iterators** marking a range; Chapter 23 covers them. The `[](int a, int b) { return a > b; }` is a **lambda** — an unnamed function written where it is used. Also Chapter 23; for now, read it as a comparison function without a name.

Also available:

| Call | Does |
|---|---|
| `std::find(v.begin(), v.end(), x)` | linear search |
| `std::binary_search(v.begin(), v.end(), x)` | binary search on sorted data |
| `std::min_element` / `std::max_element` | smallest / largest |
| `std::reverse(v.begin(), v.end())` | reverse in place |

`std::sort` is typically a hybrid, switching strategies by size, and is faster than anything you would write by hand.

**So why implement sorts yourself?** Because the reasoning transfers. You will choose between algorithms, recognize when a precondition is violated, and estimate whether an approach will scale — and none of that comes from calling a library function.

---

## Common Errors

| What you see or observe | Cause | Fix |
|---|---|---|
| Binary search reports absent items as present, or vice versa | Data not sorted | Sort first; document the precondition |
| Sort runs forever | Comparison not strict — returns true for equal items | Use `<`, never `<=` |
| The last element is never sorted | Loop bound off by one | Trace the first and last passes |
| Crash during sort | Index out of range in the inner loop | Check `j < size` |
| Sorted names but wrong grades | Sorting parallel arrays separately | Sort records — Chapter 14 |
| `std::sort` will not compile | No `<` for your type | Supply a comparison function |
| Binary search never terminates | `low`/`high` not moving | `mid + 1` and `mid - 1`, not `mid` |
| Results differ between runs | Comparison depends on something unstable | Make the ordering total and deterministic |

---

## Design Notes

**State and document preconditions.** Binary search on unsorted data is a silent wrong answer, not a slow one.

**Count operations rather than guessing.** Instrument the code; the number ends the argument.

**Separate the algorithm from the ordering.** One sort plus several comparison functions beats several sorts.

**Sort records, never parallel arrays.** Chapter 14's lesson, and sorting is exactly where it bites.

**Use the library.** Implement sorts to learn; call `std::sort` to ship.

---

## Grade Calculator v2.4 — Rankings

### What v2.4 does

Everything v2.3 did, plus: sort the roster by name, percentage, or ID with the ordering chosen at run time; find a student by ID; and report the comparison counts for linear and binary search on the same data.

### The searches, instrumented

Both take a `comparisons` reference so their cost can be measured rather than assumed:

```cpp
int linearSearchById(const std::vector<Student>& roster, int id, int& comparisons);
int binarySearchById(const std::vector<Student>& roster, int id, int& comparisons);
```

The menu handler runs both and reports both counts:

```cpp
int linearCost = 0;
int found = linearSearchById(book.roster, id, linearCost);

// Binary search needs sorted data, so sort a copy first.
std::vector<Student> sorted = book.roster;
selectionSort(sorted, book.assignments, byId);
int binaryCost = 0;
binarySearchById(sorted, id, binaryCost);

std::cout << "  Comparisons - linear: " << linearCost
          << ", binary: " << binaryCost << "\n";
```

**Note what that comparison honestly shows.** Sorting a copy to run one binary search is far more work than the linear scan it replaced. On a roster of three students, both report one comparison. The measurement demonstrates the technique and simultaneously demonstrates that it is not worth it at this size — which is the more useful lesson.

### Expected output

Three students entered as Zoe, Ada, Max; sorted by name; then a search for ID 1002:

```text
1002  Ada                     90.0%   A
1003  Max                     70.0%   C
1001  Zoe                     50.0%   F

  Found: Ada (90.0%)
  Comparisons - linear: 1, binary: 1
```

The roster is alphabetical, and every student's ID, name, and scores moved together — Chapter 14's records earning their keep.

### The grade scale as a search problem

Look again at `letterFor`. It walks a list of tiers from the top until it finds one the percentage reaches. **That is a linear search.**

For five tiers it is exactly right — a binary search would be more code, more chances to be wrong, and no faster. For a fifty-tier scale it would be worth reconsidering.

This is the chapter's judgment in miniature: **the better algorithm is the one that fits the size of your problem.** Recognizing that `letterFor` is a linear search is what lets you make that call deliberately rather than by default.

### Your StudySite Lab — Sort and Search the Roster

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.4
- **Starting point:** The working Chapter 16 v2.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Add roster sorting by student ID, name, and percentage.
2. Add linear search by student ID.
3. Add binary search by student ID and ensure its data is sorted by ID first.
4. Report the comparison count for each search.
5. Add ordering by letter grade and then name.


#### Verification

- Every sort order is correct for at least five students.
- Linear and binary search find the same existing student.
- Both searches report not found for a missing ID.
- The binary-search precondition is enforced instead of assumed.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This avoids
   creating files with names such as `_imported` when the same path is already
   open.
3. Click **Load from GitHub**, select **grade-calculator-1437**, and click each source, header,
   or documentation file needed for this chapter. Confirm the editor shows the
   expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. For a
   multi-file program, keep every source and header file needed by the build
   open in the editor.
5. Click **Run**. Read compiler messages and program output in the embedded
   Terminal, and type program input there when prompted.
6. Fix every compiler error and warning, then complete the verification list.
7. Use the Tutor with the current code or Terminal output when you need help.

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the editor.
   **Save to GitHub includes every open editor file**, so close scratch files
   and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **grade-calculator-1437** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 17 Grade Calculator v2.4**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1437** contains the Chapter 17 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Selection sort, pass by pass

```cpp
#include <iostream>
#include <string>
#include <vector>

void show(const std::vector<int>& v, const std::string& label) {
    std::cout << label;
    for (int x : v) { std::cout << x << " "; }
    std::cout << "\n";
}

int main() {
    std::vector<int> a = {64, 25, 12, 22, 11};
    show(a, "start:  ");
    for (std::size_t i = 0; i + 1 < a.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < a.size(); ++j) {
            if (a[j] < a[best]) { best = j; }
        }
        if (best != i) { std::swap(a[i], a[best]); }
        show(a, "pass " + std::to_string(i + 1) + ": ");
    }
    return 0;
}
```

**Expected output:**

```text
start:  64 25 12 22 11 
pass 1: 11 25 12 22 64 
pass 2: 11 12 25 22 64 
pass 3: 11 12 22 25 64 
pass 4: 11 12 22 25 64 
```

*Try:* Run it on already-sorted data. How many passes? How many comparisons? What does that say about selection sort?

### 2. Insertion sort, pass by pass

```cpp
#include <iostream>
#include <string>
#include <vector>

void show(const std::vector<int>& v, const std::string& label) {
    std::cout << label;
    for (int x : v) { std::cout << x << " "; }
    std::cout << "\n";
}

int main() {
    std::vector<int> b = {64, 25, 12, 22, 11};
    show(b, "start:  ");
    for (std::size_t i = 1; i < b.size(); ++i) {
        int key = b[i];
        std::size_t j = i;
        while (j > 0 && b[j - 1] > key) { b[j] = b[j - 1]; --j; }
        b[j] = key;
        show(b, "pass " + std::to_string(i) + ": ");
    }
    return 0;
}
```

**Expected output:**

```text
start:  64 25 12 22 11 
pass 1: 25 64 12 22 11 
pass 2: 12 25 64 22 11 
pass 3: 12 22 25 64 11 
pass 4: 11 12 22 25 64 
```

*Try:* Run it on `{11, 12, 22, 25, 64}`. Add a counter to the inner `while`. How many times does it run now, and why is that insertion sort's advantage?

### 3. Counting comparisons

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> sorted = {11, 12, 22, 25, 64};
    int lin = 0;
    int bin = 0;

    for (int x : sorted) {
        for (std::size_t k = 0; k < sorted.size(); ++k) {
            ++lin;
            if (sorted[k] == x) { break; }
        }
    }
    for (int x : sorted) {
        int lo = 0;
        int hi = 4;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
            ++bin;
            if (sorted[mid] == x)      { break; }
            else if (sorted[mid] < x)  { lo = mid + 1; }
            else                       { hi = mid - 1; }
        }
    }
    std::cout << "linear: " << lin << " comparisons\n";
    std::cout << "binary: " << bin << " comparisons\n";
    return 0;
}
```

**Expected output:**

```text
linear: 15 comparisons
binary: 11 comparisons
```

*Try:* Extend to 100 sorted values. Now what are the counts? At roughly what size does binary search become clearly worthwhile?

### 4. Binary search on unsorted data

```cpp
#include <iostream>
#include <vector>

bool binarySearch(const std::vector<int>& v, int target) {
    int lo = 0;
    int hi = static_cast<int>(v.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (v[mid] == target)     { return true; }
        else if (v[mid] < target) { lo = mid + 1; }
        else                      { hi = mid - 1; }
    }
    return false;
}

int main() {
    std::vector<int> unsorted = {64, 25, 12, 22, 11};
    std::cout << std::boolalpha;
    std::cout << "is 11 present? " << binarySearch(unsorted, 11) << "\n";
    std::cout << "(11 is at index 4)\n";
    return 0;
}
```

**Expected output:**

```text
is 11 present? false
(11 is at index 4)
```

*Try:* Test every value in the vector. How many are found? This is a **wrong answer**, not a slow one — write one sentence on why that is worse.

### 5. Sorting by different criteria

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Student { std::string name; int id = 0; double pct = 0.0; };

int main() {
    std::vector<Student> roster = {
        {"Zoe", 1001, 50.0}, {"Ada", 1002, 90.0}, {"Max", 1003, 70.0}
    };

    std::sort(roster.begin(), roster.end(),
              [](const Student& a, const Student& b) { return a.name < b.name; });
    for (const Student& s : roster) { std::cout << s.name << " "; }
    std::cout << "\n";

    std::sort(roster.begin(), roster.end(),
              [](const Student& a, const Student& b) { return a.pct > b.pct; });
    for (const Student& s : roster) { std::cout << s.name << " "; }
    std::cout << "\n";
    return 0;
}
```

**Expected output:**

```text
Ada Max Zoe 
Ada Max Zoe 
```

*Try:* The two orderings coincide for this data. Change one student's percentage so they differ, and confirm. Then sort by ID descending.

### 6. Trace by hand first

Before running anything, trace **selection sort** on `{5, 2, 9, 1, 7}`, writing the vector after each pass. Then trace **insertion sort** on the same data.

Which reaches a fully sorted state sooner? Which does less work overall? Now verify with code.

### 7. Reason about algorithms

- Why does binary search require sorted data, and what happens if it is not?
- Why is `low + (high - low) / 2` preferred to `(low + high) / 2`?
- Selection sort makes the same number of comparisons on sorted and reversed input. Why?
- Insertion sort does not. Why?
- You must search a 50-element roster once. Sort then binary search, or just scan? Justify it.
- You must search the same roster 10,000 times. Same question, different answer — why?

---

## Summary

- **Linear search** examines elements in order and works on any data. Work grows with *n*.
- **Binary search** halves the remaining range each step, and work grows with log *n* — but it **requires sorted data**, and on unsorted data it gives silent wrong answers.
- Use `low + (high - low) / 2` for the midpoint to avoid overflow.
- **Selection sort** repeatedly moves the smallest remaining element into place. Its cost is the same for every input.
- **Insertion sort** inserts each element into the sorted portion. It **adapts** — nearly-sorted data is nearly free.
- **Bubble sort** is famous, not recommended.
- **Merge sort** divides, sorts each half recursively, and merges. Work grows with *n* log *n*, at the cost of extra memory.
- **Compare algorithms by counting operations**, not by timing. Instrument your code.
- Pass a **comparison function** so one sort serves many orderings, separating the algorithm from the ordering.
- `std::sort`, `std::find`, and `std::binary_search` are tested and fast. Implement sorts to learn; call the library to ship.
- **The better algorithm is the one that fits the size of your problem.** For a five-tier grade scale, a linear scan is right.

---

## Key Terms

**binary search** — a search that halves the remaining range each step; requires sorted data.

**comparison function** — a function defining an ordering, passed to a sorting routine.

**divide and conquer** — solving a problem by splitting it, solving the parts, and combining.

**function pointer** — a variable holding the address of a function.

**insertion sort** — a sort that inserts each element into the sorted portion; adapts to input.

**linear search** — a search examining elements one at a time in order.

**merge** — combining two sorted sequences into one sorted sequence.

**merge sort** — a divide-and-conquer sort with *n* log *n* comparisons.

**precondition** — a requirement that must hold before an algorithm is used.

**selection sort** — a sort that repeatedly moves the smallest remaining element into place.

**stability** — whether a sort preserves the relative order of equal elements.

---

**Next:** Chapter 18 begins the object-oriented material in earnest. Your structs gain behavior and become classes, and a `GradeScale` that validates itself in its constructor makes an invalid grading scale impossible to construct — closing a category of defect you have been checking for by hand since Chapter 11. Grade Calculator v2.5.
