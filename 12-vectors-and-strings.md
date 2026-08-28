# Chapter 12 — Vectors and Standard Strings

## Learning Objectives

When you finish this chapter you will be able to:

- Explain the limitations of raw arrays that `std::vector` removes. *(SLO 2.6)*
- Declare a vector, add and remove elements, and query its size. *(SLO 1.3, 2.6)*
- Traverse a vector with an indexed loop and with a range-based `for`. *(SLO 1.3)*
- Pass vectors to functions by value and by `const` reference, and say which to use. *(SLO 1.4)*
- Use a vector of vectors as a grid. *(SLO 2.6)*
- Use `std::string` operations to inspect and build text. *(SLO 1.3)*
- Choose between an array and a vector for a given purpose. *(SLO 1.7)*
- Build Grade Calculator v1.3 — the Course I capstone.

---

## 12.1 The Limitations of Raw Arrays

Chapter 11's calculator works and is hemmed in by three restrictions, all from the same source: an array's size is fixed when the program is compiled.

**A fixed maximum.** `MAX_STUDENTS = 40` means a class of 41 does not fit, and a class of 5 wastes room for 35.

**The size does not travel with the array.** Every function taking an array needs a separate count parameter, and passing the wrong one walks off the end.

**No bounds checking, ever.** `scores[99]` on a five-element array compiles and does something undefined.

`std::vector` fixes all three. It grows and shrinks as needed, it knows its own size, and it offers a checked way to access elements.

---

## 12.2 Declaring and Using a Vector

Include `<vector>`. The type of the elements goes in angle brackets:

```cpp
#include <vector>

std::vector<double> scores;                     // empty
std::vector<double> preset(3, 10.0);            // three elements, each 10.0
std::vector<double> listed = {9.0, 84.0, 18.0}; // three given values
std::vector<std::string> names;                 // a vector of strings
```

`std::vector<double>` reads as "vector of double". The angle-bracket notation is a **template**, and Chapter 23 explains how it works. For now, treat `std::vector<T>` as the way to say "a growable collection of T".

Indexing looks exactly like an array:

```cpp
scores[0] = 9.0;
std::cout << scores[1];
```

---

## 12.3 Growing and Shrinking

The essential difference:

```cpp
std::vector<double> scores;          // size 0

scores.push_back(9.0);               // size 1
scores.push_back(84.0);              // size 2
scores.push_back(18.0);              // size 3

scores.pop_back();                   // size 2
```

```text
empty:  size=0 empty=true
after 3 push_back: size=3
after pop_back: size=2
```

**No maximum is declared anywhere.** The vector obtains more memory as it needs it. A class of 41 students is no different from a class of 4.

That memory management is real work happening behind the scenes, and Chapter 22 shows what it involves. For now the useful fact is that it is handled correctly and you do not have to think about it.

---

## 12.4 Vector Member Functions

A vector is an **object**, and the functions it carries are called with a dot. Chapter 18 explains what that means properly; the syntax is worth using now.

| Call | Does |
|---|---|
| `v.size()` | how many elements |
| `v.empty()` | true when size is 0 |
| `v.push_back(x)` | add `x` at the end |
| `v.pop_back()` | remove the last element |
| `v.front()` / `v.back()` | first / last element |
| `v.clear()` | remove everything |
| `v[k]` | element `k`, **unchecked** |
| `v.at(k)` | element `k`, **checked** |

```text
front=9 back=18 [1]=84
```

### `at()` versus `[]`

```cpp
scores[99];        // undefined behavior — may crash, may not
scores.at(99);     // throws std::out_of_range — a definite, catchable error
```

```text
at(99) threw: out_of_range
```

`at()` checks the index; `[]` does not. Checking costs a little time, which is why both exist.

Use `at()` when the index came from outside your program — from a user, a file, a calculation you are not certain of. Use `[]` inside a loop you control, such as `for (k = 0; k < v.size(); ++k)`, where the index is correct by construction.

Chapter 24 will show what `throws` means and how to catch it.

### A signed/unsigned trap

`size()` returns an unsigned type, so comparing it with a signed `int` produces a warning under `-Wall`:

```cpp
for (int k = 0; k < scores.size(); ++k)             // warning: signed/unsigned comparison
for (std::size_t k = 0; k < scores.size(); ++k)     // correct
```

`std::size_t` is the type vectors use for sizes. Appendix D Section D.6 requires it, and the alternative in the next section avoids the question entirely.

---

## 12.5 Range-Based `for` Loops

When you want every element and do not need the index:

```cpp
for (double s : scores) {
    std::cout << s << " ";
}
```

```text
range-based for: 9 84
```

Read `:` as "in". No index, no size, no comparison — so no off-by-one error and no signed/unsigned warning is possible.

To modify elements, take a reference:

```cpp
for (double& s : scores) {
    s += 5.0;                 // modifies the vector
}
```

For anything larger than a number, take a `const` reference to avoid copying — the same rule as Chapter 10 Section 10.7:

```cpp
for (const std::string& name : studentNames) {
    std::cout << name << "\n";
}
```

**Prefer the range-based form when you do not need the index.** Use an indexed loop when you do — for example when walking two parallel vectors together.

---

## 12.6 Vectors and Functions

Unlike arrays, vectors are passed **by value** by default — which copies every element:

```cpp
double sum(std::vector<double> values);              // copies the whole vector
double sum(const std::vector<double>& values);       // copies nothing
```

**Always take a `const` reference** unless you intend to modify:

```cpp
double sum(const std::vector<double>& values) {
    double total = 0.0;
    for (double v : values) { total += v; }
    return total;
}
```

To modify, take a plain reference:

```cpp
void addScore(std::vector<double>& values, double score) {
    values.push_back(score);
}
```

**No count parameter is needed**, because the vector carries its own size. That eliminates an entire class of bug from Chapter 11.

---

## 12.7 Vectors of Vectors

A grid is a vector whose elements are vectors:

```cpp
std::vector<std::vector<double>> grid(2, std::vector<double>(3, 0.0));
grid[1][2] = 7.5;
```

```text
grid[1][2]=7.5 rows=2 cols=3
```

`grid.size()` is the number of rows; `grid[0].size()` is the number of columns in row 0.

Unlike a two-dimensional array, **the rows need not be the same length.** That is exactly what a roster needs: students may have different numbers of assignments recorded, and a vector of vectors accommodates that without wasted space or special cases.

Growing it is straightforward:

```cpp
std::vector<std::vector<double>> roster;
roster.push_back({9.0, 84.0});          // a student with two scores
roster.push_back({7.5, 91.0, 18.0});    // a student with three
```

---

## 12.8 `std::string` as a Sequence

You have used `std::string` since Chapter 3 to hold text. It is also a sequence of characters, with much of the same interface as a vector:

```cpp
std::string name = "Ada Lovelace";

name.length()      // 12  (size() works too)
name[0]            // 'A'
name.back()        // 'e'
name.empty()       // false
```

```text
length=12 [0]=A back=e
```

Chapter 11 Section 11.9 described C strings — fixed-length `char` arrays with a null terminator. `std::string` removes every one of their problems: it grows, `=` copies, `==` compares contents, and it cannot run off its end unnoticed.

---

## 12.9 String Operations

| Call | Does |
|---|---|
| `s.length()` / `s.size()` | number of characters |
| `s.substr(start, count)` | a piece of the string |
| `s.find(x)` | position of `x`, or `std::string::npos` |
| `s + t` | joined |
| `s += t` | append |
| `s == t` | compare contents |
| `s.empty()` | true when there are no characters |

```text
substr(0,3)=Ada
find(' ')=3
find('z')=npos (not found)
concat: Ada Lovelace Jr.
```

### `npos`

`find` returns `std::string::npos` when the text is not present. Test for it explicitly:

```cpp
if (name.find('z') == std::string::npos) {
    std::cout << "not found\n";
}
```

`npos` is a very large number, **not** −1 in any useful sense. Testing `if (pos < 0)` fails to detect it and is a real bug.

### Splitting on a separator

Combining `find` and `substr` splits text:

```cpp
std::string full = "Ada Lovelace";
std::size_t space = full.find(' ');
if (space != std::string::npos) {
    std::string first = full.substr(0, space);
    std::string last  = full.substr(space + 1);
}
```

Chapter 15 uses this pattern to read comma-separated gradebook files.

---

## 12.10 Vectors versus Arrays

| | Raw array | `std::vector` |
|---|---|---|
| Size fixed at compile time | yes | no |
| Knows its own size | no | `size()` |
| Grows and shrinks | no | `push_back`, `pop_back` |
| Bounds checking available | no | `at()` |
| Needs a count parameter | yes | no |
| Passing copies by default | no, passes by reference | yes — use `const&` |

**Use `std::vector`.** In this book, from here on, arrays appear only where a fixed size is genuinely part of the problem.

Chapter 11 was not wasted effort. Vectors are built on arrays, indexing works identically, the loop idiom is the same, and the out-of-bounds danger still exists whenever you use `[]`. Understanding arrays is what makes vectors comprehensible rather than magical.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `warning: comparison of integer expressions of different signedness` | `int k` compared with `size()` | Use `std::size_t`, or a range-based `for` |
| Program crashes on `v[k]` | Index out of range | Use `at()`, or check the index |
| `terminate called after throwing 'std::out_of_range'` | `at()` caught a bad index — working as designed | Fix the index |
| A function does not change the vector | Passed by value | Take `std::vector<T>&` |
| The program is slow with large data | Copying vectors by value | Take `const std::vector<T>&` |
| `error: 'vector' was not declared` | Missing `#include <vector>` | Add the header |
| `if (s.find(x) < 0)` never fires | `npos` is huge, not negative | Compare to `std::string::npos` |
| `v.front()` crashes | The vector is empty | Check `empty()` first |
| Modifying `s` in `for (double s : v)` changes nothing | `s` is a copy | Use `for (double& s : v)` |

---

## Design Notes

**Take `const std::vector<T>&` unless you intend to modify.** Vectors copy by default and can be large.

**Use `at()` for indices from outside your program; `[]` inside loops you control.**

**Prefer a range-based `for` when you do not need the index.** It cannot be off by one.

**Never store the size in a separate variable.** `v.size()` is always correct; a copy of it goes stale the moment anything is added.

---

## Grade Calculator v1.3 — Dynamic Roster

### What v1.3 does

Everything v1.2 did, with **every fixed limit removed** — any number of students, assignments, and grade tiers — plus a **drop-lowest** feature.

This is the **Course I capstone**. It is a complete, genuinely useful points-based grading application, and nothing in Course II is required to make it work. Course II makes it general.

### The program

```cpp
// Grade Calculator v1.3 - Chapter 12 - COURSE I FINAL
// Unlimited roster, assignments, and grade tiers using std::vector.
// New this version: std::vector replaces fixed arrays, drop-lowest feature.
//
// Complete Course I feature set: named assignments, bonus points, custom
// letter scale, multi-student roster, class statistics, drop lowest.
// Grading model: points-based only. Weighted grading arrives in Chapter 20.
//
// Run: click Run in StudySite and use the embedded Terminal.

#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

const bool CAP_AT_100 = true;

// ---------- input helpers ----------

double readNonNegative(const std::string& prompt) {
    double value = 0.0;
    while (true) {
        std::cout << prompt;
        if (!(std::cin >> value)) {
            if (std::cin.eof()) { return 0.0; }
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "  That is not a number. Please try again.\n";
            continue;
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (value < 0.0) {
            std::cout << "  Value cannot be negative. Please try again.\n";
            continue;
        }
        return value;
    }
}

std::string readLine(const std::string& prompt) {
    std::cout << prompt;
    std::string line;
    std::getline(std::cin, line);
    return line;
}

bool readYesNo(const std::string& prompt) {
    std::string answer = readLine(prompt);
    return !answer.empty() && (answer[0] == 'y' || answer[0] == 'Y');
}

// ---------- grade scale ----------

std::vector<double> gradeCutoffs;
std::vector<char> gradeLetters;

void useDefaultScale() {
    gradeCutoffs = {90.0, 80.0, 70.0, 60.0, 0.0};
    gradeLetters = {'A', 'B', 'C', 'D', 'F'};
}

void readGradeScale() {
    gradeCutoffs.clear();
    gradeLetters.clear();
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers highest first. Type 'done' to finish.\n\n";

    while (true) {
        std::string letterText = readLine("Tier letter (or 'done'): ");
        if (letterText == "done" || letterText.empty()) { break; }
        double cutoff = readNonNegative("  Minimum percentage: ");
        if (!gradeCutoffs.empty() && cutoff >= gradeCutoffs.back()) {
            std::cout << "  Cutoff must be lower than " << gradeCutoffs.back()
                      << ". Tier not added.\n";
            continue;
        }
        gradeLetters.push_back(letterText[0]);
        gradeCutoffs.push_back(cutoff);
    }

    if (gradeCutoffs.empty() || gradeCutoffs.back() > 0.0) {
        std::cout << "Note: scale did not reach 0, so an 'F' at 0 was added.\n";
        gradeLetters.push_back('F');
        gradeCutoffs.push_back(0.0);
    }
}

char letterFor(double percentage) {
    for (std::size_t i = 0; i < gradeCutoffs.size(); ++i) {
        if (percentage >= gradeCutoffs[i]) { return gradeLetters[i]; }
    }
    return '?';
}

double computePercentage(double earned, double possible) {
    if (possible <= 0.0) { return 0.0; }
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

int main() {
    std::cout << "=== GRADE CALCULATOR v1.3 ===\n";
    std::cout << "    Course I final version\n\n";

    if (readYesNo("Define a custom grade scale? (y/n): ")) {
        readGradeScale();
    } else {
        useDefaultScale();
        std::cout << "Using default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    // Assignments: name and points possible, any number of them.
    std::vector<std::string> assignmentNames;
    std::vector<double> pointsPossible;

    std::cout << "\n--- Enter assignments ---\n";
    while (true) {
        std::string name = readLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        assignmentNames.push_back(name);
        pointsPossible.push_back(readNonNegative("  Points possible: "));
    }

    // Students: name plus one earned-points entry per assignment.
    std::vector<std::string> studentNames;
    std::vector<std::vector<double>> earned;

    std::cout << "\n--- Enter students ---\n";
    while (true) {
        std::string name = readLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames.push_back(name);

        std::vector<double> row;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            row.push_back(readNonNegative("  " + assignmentNames[a] + " points (incl. bonus): "));
        }
        earned.push_back(row);
    }

    bool dropLowest = false;
    if (assignmentNames.size() > 1) {
        dropLowest = readYesNo("\nDrop each student's lowest assignment? (y/n): ");
    }

    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (std::size_t s = 0; s < studentNames.size(); ++s) {
        double totalEarned = 0.0;
        double totalPossible = 0.0;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            totalEarned += earned[s][a];
            totalPossible += pointsPossible[a];
        }

        // Dropping in a points-based scheme removes BOTH the earned points and
        // the possible points. Removing only one would distort the result.
        if (dropLowest && !assignmentNames.empty()) {
            std::size_t worst = 0;
            double worstRatio = 2.0;
            for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
                if (pointsPossible[a] <= 0.0) { continue; }
                double ratio = earned[s][a] / pointsPossible[a];
                if (ratio < worstRatio) { worstRatio = ratio; worst = a; }
            }
            if (worstRatio <= 1.0) {
                totalEarned -= earned[s][worst];
                totalPossible -= pointsPossible[worst];
            }
        }

        double pct = computePercentage(totalEarned, totalPossible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(8) << pct << "%   "
                  << letterFor(pct) << "\n";
    }

    if (!studentNames.empty()) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(8)
                  << classTotal / studentNames.size() << "%\n";
    } else {
        std::cout << "No students entered.\n";
    }
    return 0;
}
```

### Expected output

Default scale; assignments `Homework 1` (10), `Midterm` (100), `Quiz` (20); Ada scoring 10, 90, 5 and Alan scoring 8, 70, 20; drop-lowest **on**:

```text
=====================================
  CLASS REPORT
=====================================
Ada                     90.9%   A
Alan                    93.3%   A
-------------------------------------
CLASS AVERAGE           92.1%
```

Alan's 93.3% deserves a look. His raw total is 98 out of 130, which is 75.4%. Dropping his worst assignment by ratio — the Midterm, at 70/100 — leaves 28 out of 30, or 93.3%. Dropping one assignment moved him from a C to an A, which is exactly why drop-lowest policies matter and why the arithmetic must be right.

### What to notice

**Not one fixed maximum anywhere.** `MAX_STUDENTS`, `MAX_ASSIGNMENTS`, and `MAX_TIERS` are gone. The program handles four students or four hundred.

**`std::vector<std::vector<double>> earned` replaces the 2D array**, and each row is built with `push_back` as the student's scores are entered.

**Drop-lowest removes both the earned and the possible points.** This is the subtle part. In a points-based scheme, an assignment contributes to both running totals, so dropping it must remove it from both. Remove only the earned points and the student is penalized for an assignment they no longer have.

**Worst is chosen by ratio, not by raw points.** A 60/100 exam is a better performance than 2/10 on a quiz, even though 60 is a bigger number. Comparing `earned / possible` compares like with like.

**Every loop uses `std::size_t`**, matching what `size()` returns and avoiding the signed/unsigned warning.

### The one thing v1.3 still cannot do

Look at how the course percentage is computed: two running totals, one division. Every point counts the same regardless of which assignment it came from.

That is a design decision, and it is correct for a points-based scheme. It also means **weighted grading is impossible here.** If exams were meant to count 50% of the course and homework 30%, no arrangement of two running totals could express it — you would need separate totals per category, combined by weight afterward.

That requirement has been in your specification since Chapter 1, marked out of scope. Course I is now finished and has never needed it. Chapter 13 analyzes it properly, and Chapters 20 and 21 build it.

### Your StudySite Lab — Complete the Dynamic Roster

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.3
- **Starting point:** The working Chapter 11 program and the Chapter 5 design document.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### Required work

1. Replace fixed student, assignment, score, and grade-scale arrays with `std::vector`.
2. Allow any number of assignments and students.
3. Add the drop-lowest option. Remove both earned and possible points for the selected assignment.
4. Preserve validated input, custom grade scales, rounding, capping, and class reporting from the earlier checkpoints.
5. Keep the weighted-grading scope statement unchanged. Weighted grading belongs to COSC 1437.
6. Complete only the Chapter 12 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.


#### Verification

- The program handles more than 40 students.
- Drop-lowest arithmetic matches a hand calculation.
- No-student, no-assignment, zero-possible-points, invalid-scale, cutoff-boundary, bonus, and invalid-numeric-input cases behave correctly.
- The repository contains the complete working v1.3 code checkpoint and the project documents created in earlier chapters.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This avoids
   creating files with names such as `_imported` when the same path is already
   open.
3. Click **Load from GitHub**, select **grade-calculator-1436**, and click each source, header,
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
3. Select **grade-calculator-1436** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 12 Grade Calculator v1.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1436** contains the Chapter 12 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Growing a vector

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<double> scores;
    std::cout << std::boolalpha;
    std::cout << "size=" << scores.size() << " empty=" << scores.empty() << "\n";

    scores.push_back(9.0);
    scores.push_back(84.0);
    scores.push_back(18.0);
    std::cout << "after 3 push_back: size=" << scores.size() << "\n";
    std::cout << "front=" << scores.front() << " back=" << scores.back() << "\n";

    scores.pop_back();
    std::cout << "after pop_back: size=" << scores.size() << "\n";
    return 0;
}
```

**Expected output:**

```text
size=0 empty=true
after 3 push_back: size=3
front=9 back=18
after pop_back: size=2
```

*Try:* Call `front()` on an empty vector. What happens? Add an `empty()` check.

### 2. Two ways to traverse

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<double> scores = {9.0, 84.0, 18.0};

    for (std::size_t k = 0; k < scores.size(); ++k) {
        std::cout << k << ": " << scores[k] << "\n";
    }
    for (double s : scores) {
        std::cout << s << " ";
    }
    std::cout << "\n";
    return 0;
}
```

**Expected output:**

```text
0: 9
1: 84
2: 18
9 84 18 
```

*Try:* Change `std::size_t k` to `int k` and rebuild. Read the warning. Then double every score using a range-based loop — you will need `double&`.

### 3. `at()` versus `[]`

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    std::vector<double> scores = {9.0, 84.0};
    try {
        std::cout << scores.at(99) << "\n";
    } catch (const std::out_of_range&) {
        std::cout << "at(99) threw out_of_range\n";
    }
    return 0;
}
```

**Expected output:**

```text
at(99) threw out_of_range
```

*Try:* Replace `at(99)` with `scores[99]`. Run it several times. Does it crash? Print a value? Both are undefined behavior — which of the two versions would you rather ship?

### 4. A vector of vectors

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<std::vector<double>> roster;
    roster.push_back({9.0, 84.0});
    roster.push_back({7.5, 91.0, 18.0});

    for (std::size_t s = 0; s < roster.size(); ++s) {
        std::cout << "student " << s << " has " << roster[s].size() << " scores: ";
        for (double v : roster[s]) { std::cout << v << " "; }
        std::cout << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
student 0 has 2 scores: 9 84 
student 1 has 3 scores: 7.5 91 18 
```

*Try:* Explain why a two-dimensional array could not hold this data without waste.

### 5. Strings as sequences

```cpp
#include <iostream>
#include <string>

int main() {
    std::string name = "Ada Lovelace";
    std::cout << "length      " << name.length() << "\n";
    std::cout << "first char  " << name[0] << "\n";
    std::cout << "substr(0,3) " << name.substr(0, 3) << "\n";
    std::cout << "find(' ')   " << name.find(' ') << "\n";
    std::cout << "concat      " << name + " Jr." << "\n";
    return 0;
}
```

**Expected output:**

```text
length      12
first char  A
substr(0,3) Ada
find(' ')   3
concat      Ada Lovelace Jr.
```

*Try:* Extract the last name using `find` and `substr` together, without hard-coding the position 4.

### 6. Splitting text

Write a program that reads a full name and prints the first and last names on separate lines.

Then answer: what should it do if the input has no space at all? What if it has two spaces? Your program should not crash on either. Test both before you consider it finished.

### 7. Convert array code to vectors

Rewrite this using `std::vector`, removing the count parameter and the fixed maximum:

```cpp
#include <iostream>

const int MAX = 100;

double average(const double values[], int count) {
    if (count == 0) { return 0.0; }
    double total = 0.0;
    for (int k = 0; k < count; ++k) { total += values[k]; }
    return total / count;
}

int main() {
    double scores[MAX] = {9.0, 84.0, 18.0};
    std::cout << average(scores, 3) << "\n";
    return 0;
}
```

How many parameters did the function lose? What class of bug did that eliminate?

---

## Summary

- `std::vector` removes the three limits of raw arrays: it **grows**, it **knows its own size**, and it offers **bounds-checked access**.
- Declare with `std::vector<T>`. Add with `push_back`, remove with `pop_back`, query with `size()` and `empty()`.
- `v[k]` is unchecked; `v.at(k)` throws `std::out_of_range`. Use `at()` for indices from outside your program.
- `size()` returns an unsigned type — use `std::size_t` for loop indices, or a **range-based `for`**, which cannot be off by one.
- **Vectors copy by value.** Take `const std::vector<T>&` unless you intend to modify. **No count parameter is ever needed.**
- A **vector of vectors** is a grid whose rows may differ in length.
- `std::string` is a sequence of characters with `length`, `substr`, `find`, `+`, and `==`. `find` returns `std::string::npos` when nothing matches — never test for a negative value.
- **Use vectors.** Arrays remain worth understanding because vectors are built on them and `[]` is still unchecked.
- **Grade Calculator v1.3 completes Course I**: named assignments, bonus points, a user-defined letter scale, an unlimited roster, class statistics, and drop-lowest — all on a single points-based grading model.

---

## Key Terms

**at()** — a bounds-checked element access that throws on an invalid index.

**member function** — a function belonging to an object, called with a dot.

**npos** — the value `find` returns when nothing matches.

**pop_back** — removes the last element of a vector.

**push_back** — adds an element to the end of a vector.

**range-based for** — a loop visiting every element of a collection without an index.

**size_t** — the unsigned type used for container sizes and indices.

**std::string** — the standard type for text of any length.

**std::vector** — the standard growable sequence container.

**substr** — a function returning part of a string.

**template** — a type parameterized by another type, as in `std::vector<double>`.

---

**Next:** Course II begins. Chapter 13 steps back from code to ask how software is actually built and maintained — planning, analysis, design, development, and maintenance — and has you write a maintenance plan for the application you just inherited from yourself. Its headline item is the requirement you have deferred since Chapter 1. Grade Calculator v2.0.
