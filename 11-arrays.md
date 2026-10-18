# Chapter 11 — Arrays

## Learning Objectives

When you finish this chapter you will be able to:

- Declare, initialize, and index an array. *(SLO 2.6)*
- Traverse an array with a loop and explain the standard idiom. *(SLO 1.4, 2.6)*
- Pass an array to a function together with its size. *(SLO 1.4, 2.6)*
- Use parallel arrays to associate related values. *(SLO 2.6)*
- Declare and traverse a two-dimensional array. *(SLO 2.6)*
- Explain what happens when an index goes out of bounds. *(SLO 1.6)*
- Replace a hard-coded conditional chain with a table-driven loop. *(SLO 1.7)*
- Build Grade Calculator v1.2 — a class roster, and a grade scale the user defines.

---

## 11.1 Why Collections Are Needed

Your calculator handles one student and keeps running totals. To handle a class, you would need a variable per student — and you do not know how many students there are when you write the program.

```cpp
double student1 = 0.0;
double student2 = 0.0;
double student3 = 0.0;      // and then what?
```

An **array** holds many values of one type under a single name, reached by number.

There is a second problem this chapter solves, and it is the more interesting one. In Chapter 6 you built a letter-grade chain and the chapter ended by pointing out its limitation: every cutoff is compiled into the program, so no user can define their own scale. That limitation is not fixed by writing a longer chain. It is fixed by turning the cutoffs into **data**, and arrays are what make data-driven code possible.

---

## 11.2 Declaring and Initializing Arrays

```cpp
double scores[5];                                   // 5 doubles, uninitialized
double scores[5] = {9.0, 84.0, 18.0, 45.0, 30.0};   // 5 doubles, initialized
double scores[5] = {0.0};                           // all five set to 0.0
double scores[] = {9.0, 84.0, 18.0};                // size 3, deduced
```

The number in brackets is the **size**, and it must be a compile-time constant:

```cpp
const int MAX_STUDENTS = 40;
double totals[MAX_STUDENTS];      // fine

int count = 0;
std::cin >> count;
double totals[count];             // NOT standard C++
```

That last restriction is a real limitation — you must decide a maximum in advance and hope it is enough. Chapter 12 removes it with `std::vector`.

**Always initialize.** `double scores[5];` contains garbage, and Section 3.2's warning applies with five times the force.

---

## 11.3 Indexing and Bounds

Reach an element with a **subscript**:

```cpp
double scores[5] = {9.0, 84.0, 18.0, 45.0, 30.0};

std::cout << scores[0];      // 9.0  — the FIRST element
std::cout << scores[4];      // 30.0 — the LAST element
scores[2] = 20.0;            // assign to the third
```

**Indices start at 0.** An array of size 5 has valid indices 0, 1, 2, 3, 4. There is no `scores[5]`.

This is why Chapter 7 Section 7.4 taught you to count from zero with `<`:

```cpp
for (int k = 0; k < 5; ++k)      // visits 0,1,2,3,4 — every element, exactly once
```

### Out of bounds

C++ does not check subscripts. Reading or writing past the end compiles, runs, and does something undefined:

```cpp
double scores[5];
scores[5] = 100.0;      // one past the end — no error, no warning
```

It may appear to work. It may corrupt another variable. It may crash. It may behave differently on different days.

**This is the single most dangerous thing in this chapter.** An out-of-bounds write is the first seeded defect in Chapter 16's debugging lab, precisely because it is invisible until it is catastrophic.

Two defenses. **Use `< size`, never `<= size`.** And **check any index that came from outside your program** before using it.

---

## 11.4 Traversing an Array

The standard idiom:

```cpp
const int COUNT = 5;
double scores[COUNT] = {9.0, 84.0, 18.0, 45.0, 30.0};

double total = 0.0;
for (int k = 0; k < COUNT; ++k) {
    total += scores[k];
}
```

This is Chapter 7's accumulator pattern with an array supplying the values. The loop and the array fit together so naturally that the pairing is worth memorizing: **`for (int k = 0; k < size; ++k)` visits every element exactly once.**

Finding the largest follows the same shape:

```cpp
double highest = scores[0];              // start with the first, not with 0.0
for (int k = 1; k < COUNT; ++k) {        // start at 1 — element 0 is already in
    if (scores[k] > highest) {
        highest = scores[k];
    }
}
```

Starting `highest` at `scores[0]` rather than `0.0` matters: with all-negative data, starting at zero gives an answer that is not in the array at all.

---

## 11.5 Arrays and Functions

An array does **not** carry its size. Pass both:

```cpp
double sum(const double values[], int count) {
    double total = 0.0;
    for (int k = 0; k < count; ++k) {
        total += values[k];
    }
    return total;
}

double total = sum(scores, COUNT);
```

Two things differ from every other parameter you have met.

**Arrays are passed by reference automatically** — the function receives the array's address, not a copy. So a function *can* modify the caller's array, unlike the `double` in Chapter 9 Section 9.3. That is efficient and slightly dangerous.

**`const` prevents modification.** `const double values[]` promises the function will not change it, and the compiler enforces the promise. Use `const` on every array parameter you do not intend to modify.

Because the size does not travel with the array, `count` must be correct. Pass the wrong count and the function walks off the end.

---

## 11.6 Parallel Arrays

To associate several pieces of information about the same thing, use **parallel arrays** — separate arrays where the same index refers to the same item:

```cpp
std::string studentNames[3] = {"Ada", "Grace", "Alan"};
double studentTotals[3]     = {89.0, 91.5, 72.0};
char studentLetters[3]      = {'B', 'A', 'C'};

// index 1 is Grace, 91.5, 'A'
```

This works and has a real weakness: **nothing enforces the correspondence.** Sort one array and not the others and every student gets someone else's grade. Add a student to two of the three and the arrays drift out of step permanently.

Chapter 14 replaces parallel arrays with a `struct`, which makes that class of bug structurally impossible. For Course I, parallel arrays are the tool available — and knowing exactly why they are risky is what makes Chapter 14 land.

---

## 11.7 Two-Dimensional Arrays

A roster is naturally a grid: students down, assignments across.

```cpp
const int MAX_STUDENTS = 3;
const int MAX_ASSIGNMENTS = 4;

double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS] = {{0.0}};

pointsEarned[1][2] = 20.0;     // student 1, assignment 2
```

![A grid of three rows and four columns holding points earned, with rows labelled as students Ada, Grace and Alan, columns labelled as assignment indices 0 to 3, and the cell at row 1 column 2 highlighted.](figures/ch11-fig1-2d-array.svg)

**Figure 11.1 — A two-dimensional array of points earned.**

*Description of Figure 11.1.* A grid with three rows and four columns. Rows are students, indexed 0 (Ada), 1 (Grace), and 2 (Alan). Columns are assignments, indexed 0 through 3.

| | [0] | [1] | [2] | [3] |
|---|---|---|---|---|
| **[0] Ada** | 9.0 | 84.0 | 18.0 | 45.0 |
| **[1] Grace** | 7.5 | 91.0 | **20.0** | 40.0 |
| **[2] Alan** | 10.0 | 62.0 | 15.0 | 50.0 |

The highlighted cell is `pointsEarned[1][2]`, holding 20.0. The first index selects the row, the second the column, and both start at 0. A separate array of names runs alongside: `studentNames[1]` is `"Grace"`.

### Traversing with nested loops

Chapter 7 Section 7.6 introduced nested loops. This is what they were for:

```cpp
for (int s = 0; s < studentCount; ++s) {
    double total = 0.0;
    for (int a = 0; a < assignmentCount; ++a) {
        total += pointsEarned[s][a];
    }
    std::cout << studentNames[s] << ": " << total << "\n";
}
```

The outer loop walks students; the inner walks that student's assignments. Reverse them and you total per assignment instead — same data, different question.

**Arrays are stored in row-major order**, meaning row 0 sits entirely in memory before row 1 begins. That matters for performance in large programs and not at all here.

### Higher dimensions

C++ allows more:

```cpp
double scores[4][30][10];      // sections, students, assignments
```

Three dimensions is occasionally useful and rapidly hard to reason about. Two is enough for this book.

---

## 11.8 Replacing Code with Data

This section is the chapter's real lesson.

Here is the letter-grade logic from Chapter 6:

```cpp
char letter = 'F';
if (percentage >= 90.0)      { letter = 'A'; }
else if (percentage >= 80.0) { letter = 'B'; }
else if (percentage >= 70.0) { letter = 'C'; }
else if (percentage >= 60.0) { letter = 'D'; }
```

The cutoffs and letters are **written into the control flow**. To use a different scale you must edit and recompile.

Now put the same information in parallel arrays:

```cpp
double cutoffs[5] = {90.0, 80.0, 70.0, 60.0, 0.0};
char letters[5]   = {'A',  'B',  'C',  'D',  'F'};
int tierCount = 5;

char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int k = 0; k < count; ++k) {
        if (percentage >= cutoffs[k]) {
            return letters[k];
        }
    }
    return '?';
}
```

Compare them honestly:

| | Chapter 6 chain | Table-driven loop |
|---|---|---|
| Lines of logic | grows with every tier | 5, always |
| Adding a tier | edit code, recompile | add one array element |
| A plus-minus scale | rewrite the chain | supply different data |
| **A scale the user types in** | **impossible** | just fill the arrays |
| Testing | test every branch | test one loop |

The loop is shorter, it never grows, and — decisively — **the data can come from anywhere**, including the user.

That last row is what makes this a turning point rather than a tidying-up. There is no arrangement of `if/else if` that accepts a grading scale at run time. The moment the cutoffs became an array, an entire category of feature became possible.

**This pattern — replacing branching code with a table of data — recurs throughout the book.** In Chapter 14 the two parallel arrays become one array of `struct`. In Chapter 18 that becomes a `GradeScale` class that validates itself. The idea does not change; only the container does.

---

## 11.9 C-Style Strings

Before `std::string`, C++ inherited C's approach: an array of `char` ending with a **null terminator**, the character `'\0'`.

```cpp
char name[6] = {'A', 'd', 'a', '\0'};
char name[] = "Ada";                    // same thing; the '\0' is added for you
```

`"Ada"` occupies four bytes, not three. Every string literal you have written since Chapter 2 has been a C string.

They are awkward. The size is fixed, `=` does not copy them, `==` compares addresses rather than contents, and forgetting the terminator makes functions read off the end of the array.

**Use `std::string`.** C strings are covered because you will meet them in older code and in library interfaces, and because they explain what a string literal actually is.

---

## 11.10 Command-Line Arguments *(reference only)*

A program can receive information from the command line through a different form of `main`:

```cpp
#include <iostream>

int main(int argc, char* argv[]) {
    for (int k = 0; k < argc; ++k) {
        std::cout << "argv[" << k << "] = " << argv[k] << "\n";
    }
    return 0;
}
```

`argc` is the number of arguments and `argv` is an array of C strings holding them. `argv[0]` is always the program's own name.

```text
./gradecalc period3 --verbose

argv[0] = ./gradecalc
argv[1] = period3
argv[2] = --verbose
```

This belongs in the arrays chapter because `argv` is an array of C strings — both concepts from this chapter, combined.

**It is reference material only.** Every program in this book is menu-driven and reads its input interactively from `std::cin`. The Grade Calculator never reads command-line arguments, and no exercise requires them. You should recognize `int main(int argc, char* argv[])` when you see it elsewhere, and that is all this section is for.

---

## 11.11 Common Array Errors

| What you see or observe | Cause | Fix |
|---|---|---|
| Values are garbage | Array not initialized | `double a[5] = {0.0};` |
| The program crashes, or a nearby variable changes | Index out of bounds | Use `< size`, never `<= size` |
| The loop misses the last element | Started at 1, or used `< size - 1` | Start at 0, test `< size` |
| The loop runs one time too many | `<= size` | Use `< size` |
| The wrong grade goes to the wrong student | Parallel arrays out of step | Update all of them together; Chapter 14 fixes this properly |
| `error: array must be initialized with a brace-enclosed initializer` | Assigned an array with `=` | Copy element by element |
| `error: array bound is not an integer constant` | Size from a variable | Use a `const int`, or `std::vector` |
| A function sums the wrong number of elements | Wrong count passed | Pass the same constant used to declare it |
| Comparing two C strings with `==` is always false | Comparing addresses | Use `std::string` |

---

## Design Notes

**Always pass the size with the array.** An array does not know how big it is, and a function that guesses is a defect waiting for the wrong input.

**Mark array parameters `const` unless you intend to modify them.** Arrays pass by reference, so without `const` any function can rewrite your data.

**Prefer data to branching.** If a conditional chain encodes a table, make it a table. The code shrinks and the capability grows.

**Treat parallel arrays as a known risk.** Every operation must touch all of them. Write a comment saying so, and look forward to Chapter 14.

---

## Grade Calculator v1.2 — Class Roster and Custom Letter Scale

### What v1.2 does

Two features arrive together, because both are the same idea: replacing code with data.

A **multi-student roster**, stored in a two-dimensional array of points with parallel arrays of names. And a **user-defined letter grade scale** — an instructor can now type in A/B/C/D/F, a plus-minus scale, or pass/fail, without the program changing.

### The program

```cpp
// Grade Calculator v1.2 - Chapter 11
// Multi-student roster on arrays, plus a USER-DEFINED letter grade scale.
// New this version: 2D arrays, parallel arrays, table-driven grade lookup.
//
// Central lesson: the hard-coded if/else chain of v1.1 becomes a loop over a
// table of data. Changing the grading scheme no longer means changing code.
//
// Run: click Run in StudySite and use the embedded Terminal.

#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>

const int MAX_STUDENTS = 40;
const int MAX_ASSIGNMENTS = 20;
const int MAX_TIERS = 12;
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

// ---------- grade scale (parallel arrays) ----------

/**
 * Reads a custom grade scale from the user into two parallel arrays.
 * Tiers must be entered highest cutoff first. Validated on entry.
 * @return the number of tiers actually read
 */
int readGradeScale(double cutoffs[], char letters[]) {
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers from highest to lowest. The last tier should be 0.\n";
    std::cout << "Example: A 90, B 80, C 70, D 60, F 0\n\n";

    int count = 0;
    while (count < MAX_TIERS) {
        std::string prompt = "Tier " + std::to_string(count + 1) + " letter (or 'done'): ";
        std::string letterText = readLine(prompt);
        if (letterText == "done" || letterText.empty()) { break; }

        double cutoff = readNonNegative("  Minimum percentage for this tier: ");

        // Validation: cutoffs must strictly descend, or lookup breaks.
        if (count > 0 && cutoff >= cutoffs[count - 1]) {
            std::cout << "  Cutoff must be lower than the previous tier ("
                      << cutoffs[count - 1] << "). Tier not added.\n";
            continue;
        }
        letters[count] = letterText[0];
        cutoffs[count] = cutoff;
        ++count;
    }

    // A scale that does not reach 0 leaves low scores unclassified.
    if (count == 0 || cutoffs[count - 1] > 0.0) {
        std::cout << "\nNote: your scale did not reach 0, so an 'F' at 0 was added.\n";
        if (count < MAX_TIERS) {
            letters[count] = 'F';
            cutoffs[count] = 0.0;
            ++count;
        }
    }
    return count;
}

void useDefaultScale(double cutoffs[], char letters[], int& count) {
    const char defLetters[] = {'A', 'B', 'C', 'D', 'F'};
    const double defCutoffs[] = {90.0, 80.0, 70.0, 60.0, 0.0};
    count = 5;
    for (int i = 0; i < count; ++i) {
        letters[i] = defLetters[i];
        cutoffs[i] = defCutoffs[i];
    }
}

/**
 * Table-driven lookup. Compare with the if/else chain in v1.1: this version
 * works for any scale the user defines, and is shorter.
 */
char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int i = 0; i < count; ++i) {
        if (percentage >= cutoffs[i]) {
            return letters[i];
        }
    }
    return '?';
}

double computePercentage(double earned, double possible) {
    if (possible <= 0.0) { return 0.0; }
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

// ---------- main ----------

int main() {
    std::cout << "=== GRADE CALCULATOR v1.2 ===\n";

    // Parallel arrays: names[i] belongs with scores[i][...]
    std::string studentNames[MAX_STUDENTS];
    std::string assignmentNames[MAX_ASSIGNMENTS];
    double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS] = {{0.0}};
    double pointsPossible[MAX_ASSIGNMENTS] = {0.0};
    int studentCount = 0;
    int assignmentCount = 0;

    double cutoffs[MAX_TIERS] = {0.0};
    char letters[MAX_TIERS] = {'\0'};
    int tierCount = 0;

    std::string useCustom = readLine("Define a custom grade scale? (y/n): ");
    if (!useCustom.empty() && (useCustom[0] == 'y' || useCustom[0] == 'Y')) {
        tierCount = readGradeScale(cutoffs, letters);
    } else {
        useDefaultScale(cutoffs, letters, tierCount);
        std::cout << "Using the default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    std::cout << "\n--- Enter assignments ---\n";
    while (assignmentCount < MAX_ASSIGNMENTS) {
        std::string name = readLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        assignmentNames[assignmentCount] = name;
        pointsPossible[assignmentCount] = readNonNegative("  Points possible: ");
        ++assignmentCount;
    }

    std::cout << "\n--- Enter students ---\n";
    while (studentCount < MAX_STUDENTS) {
        std::string name = readLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames[studentCount] = name;
        for (int a = 0; a < assignmentCount; ++a) {
            std::string prompt = "  " + assignmentNames[a] + " points earned (incl. bonus): ";
            pointsEarned[studentCount][a] = readNonNegative(prompt);
        }
        ++studentCount;
    }

    // ---------- report ----------
    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (int s = 0; s < studentCount; ++s) {
        double earned = 0.0;
        double possible = 0.0;
        for (int a = 0; a < assignmentCount; ++a) {
            earned += pointsEarned[s][a];
            possible += pointsPossible[a];
        }
        double pct = computePercentage(earned, possible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(8) << pct << "%   "
                  << letterFor(pct, cutoffs, letters, tierCount) << "\n";
    }

    if (studentCount > 0) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(8) << classTotal / studentCount << "%\n";
    } else {
        std::cout << "No students entered.\n";
    }

    std::cout << "\nPer-assignment averages:\n";
    for (int a = 0; a < assignmentCount; ++a) {
        double sum = 0.0;
        for (int s = 0; s < studentCount; ++s) { sum += pointsEarned[s][a]; }
        double avg = (studentCount > 0) ? sum / studentCount : 0.0;
        std::cout << "  " << std::left << std::setw(20) << assignmentNames[a]
                  << avg << " / " << pointsPossible[a] << "\n";
    }
    return 0;
}
```

### Expected output

With a custom scale of A 93, B 85, C 77, F 0; assignments `Homework 1` (10 points) and `Midterm` (100 points); students Ada (10, 90) and Alan (8, 70):

```text
=====================================
  CLASS REPORT
=====================================
Ada                     90.9%   B
Alan                    70.9%   F
-------------------------------------
CLASS AVERAGE           80.9%

Per-assignment averages:
  Homework 1          9.0 / 10.0
  Midterm             80.0 / 100.0
```

Note Alan's F. Under the default scale, 70.9% is a C. Under the custom scale, where C requires 77, it is an F. **The program did not change — the data did.**

### What to notice

**`letterFor` is five lines and never grows.** It handles a five-tier scale, a twelve-tier plus-minus scale, and a two-tier pass/fail scale identically. Put it beside the chain in v1.1 and the difference in *capability*, not just length, is the point.

**Validation moved from the compiler to run time.** When cutoffs were code, a wrong order was a bug you introduced. Now a user can type them out of order, so `readGradeScale` checks that each is lower than the last and rejects the ones that are not. **Data from outside the program must be validated inside it.**

**The scale is repaired if it does not reach 0.** Without a bottom tier, a low percentage matches nothing and `letterFor` returns `'?'`. Rather than let that happen, the program adds an F at 0 and says so.

**Two nested loops, two different questions.** Students-outer gives per-student totals; assignments-outer gives per-assignment averages. Same array, transposed traversal.

**Every array parameter that is not modified is `const`.**

**The fixed maxima are a real limitation.** `MAX_STUDENTS = 40` means a class of 41 does not fit. Chapter 12 removes the limit entirely.

### Your StudySite Lab — Build a Class Roster

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.2
- **Starting point:** Your committed Chapter 10 v1.1 program (three files, validated input).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

#### What you will build

Two limits fall in this chapter. The program has only ever held **one**
student, and its grade scale has only ever been the one written into the code.
Arrays fix the first: a 2D array stores every student's score on every
assignment. A **table** of cutoffs and letters fixes the second, and that is
the chapter's real idea — the `if`/`else if` chain from Chapter 6 becomes a
loop over data, so changing the grading scheme no longer means changing code.

By the end you will have:

1. `MAX_TIERS` in the library, and three new library functions:
   `useDefaultScale`, `readGradeScale`, and `letterFor`.
2. A grade scale held in **parallel arrays** — `cutoffs[i]` and `letters[i]`
   describe the same tier — that the user can define at run time, with
   validation that the cutoffs descend.
3. `assignLetterGrade` and the four `*_CUTOFF` constants **gone**, replaced by
   the table.
4. A roster in `main.cpp`: a 2D array of earned points, parallel arrays of
   student and assignment names, and a class report with per-student grades,
   a class average, and per-assignment averages.

> **Limitation, by design:** the arrays are fixed size — 40 students, 20
> assignments, 12 tiers. Chapter 12 removes all three limits with
> `std::vector`.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradelib.h` | Edit (Steps 1-3) |
| `gradelib.cpp` | Edit (Steps 4-6) |
| `main.cpp` | Edit (Steps 7-8) |

When you are finished your project still has **three** files.

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

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select **COSC1436xxx-Grade-Calculator-YourLastName**, and click `main.cpp`, `gradelib.h`, and `gradelib.cpp`.
   Confirm the editor shows the expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. Keep all three files open, and click **Run** at the ▶ Run checkpoint.
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
> clang++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

#### Step 1 — Replace the fixed cutoffs with a tier limit

In `gradelib.h`, update the first comment line:

```cpp
// gradelib.h - Grade Calculator v1.1 - Chapter 10
```

Replace it with:

```cpp
// gradelib.h - Grade Calculator v1.2 - Chapter 11
```

Then find the four cutoff constants and delete all four:

```cpp
const double A_CUTOFF = 90.0;
const double B_CUTOFF = 80.0;
const double C_CUTOFF = 70.0;
const double D_CUTOFF = 60.0;
```

Find the `CAP_AT_100` constant:

```cpp
const bool CAP_AT_100 = true;
```

Directly below it, add:

```cpp

// The most tiers a grade scale may hold. Chapter 12 removes this limit.
const int MAX_TIERS = 12;
```

**Why:** `A_CUTOFF` and friends were an improvement on magic numbers in
Chapter 6, but they are still *code*. A grade scale is **data**: this course
uses 90/80/70/60, another might use 93/85/77/70, and a program that needs
recompiling to change that is the wrong shape. From here the cutoffs live in
arrays the user can fill, and the constants have nothing left to do.

`MAX_TIERS` replaces them with a different kind of limit — how many tiers the
fixed-size array can hold. That is a real constraint of arrays, and naming it
is how the limit stays in one place.

#### Step 2 — Document the new `computePercentage` contract

In `gradelib.h`, find the one-line comment above `computePercentage`:

```cpp
/** Converts points to a capped, rounded percentage. Requires possible > 0. */
```

Replace it with this fuller block:

```cpp
/**
 * Converts points to a capped, rounded percentage.
 * @param  earned    total points earned including bonus
 * @param  possible  total points possible
 * @return percentage rounded to one decimal place, or 0.0 when possible <= 0
 */
```

**Why:** Chapter 10's version carried a precondition — the caller had to
ensure `possible > 0`. That worked when one caller existed. A roster has many:
every student row calls it, and any of them could total zero possible points if
every assignment is worth 0. Pushing the check into the function is the right
call once the number of callers grows, and the documented contract changes from
"you must check" to "returns 0.0 in that case". Step 4 implements it.

#### Step 3 — Swap the fixed lookup for the table-driven one

In `gradelib.h`, find the `assignLetterGrade` declaration with its comment and the blank line below it, and delete all three lines:

```cpp
/** Maps a percentage to a letter grade on the fixed course scale. */
char assignLetterGrade(double percentage);
```

Then find the last line of the file:

```cpp
#endif
```

Directly above it, add:

```cpp
/**
 * Fills a scale with the default tiers: A 90, B 80, C 70, D 60, F 0.
 * @param  cutoffs  receives the minimum percentage for each tier
 * @param  letters  receives the letter for each tier
 * @param  count    receives the number of tiers written
 */
void useDefaultScale(double cutoffs[], char letters[], int& count);

/**
 * Reads a custom grade scale from the user into two parallel arrays, highest
 * cutoff first. A tier whose cutoff is not below the previous one is refused,
 * and an 'F' at 0 is appended if the scale does not reach 0.
 * @return the number of tiers stored, never more than MAX_TIERS
 */
int readGradeScale(double cutoffs[], char letters[]);

/**
 * Table-driven lookup: the letter of the first tier the percentage reaches.
 * @pre    cutoffs[0..count-1] strictly descend
 * @return that tier's letter, or '?' if the scale does not reach this value
 */
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);
```

**Why:** These three declarations are the chapter's new interface, and the
shape of `letterFor` is worth reading closely:

```cpp
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);
```

An array parameter does **not** carry its own length in C++ — `cutoffs[]`
decays to a pointer, and `sizeof` inside the function would tell you the size
of a pointer, not the array. So the count must be passed alongside it. That is
why every one of these functions takes or returns a `count`, and it is the
single most important thing to understand about passing arrays to functions.

`const` on the two lookup arrays promises `letterFor` will not modify them.
`useDefaultScale` and `readGradeScale` take them non-`const`, because filling
them in *is* their job.

#### Step 4 — Guard the division in `computePercentage`

In `gradelib.cpp`, update the first comment line:

```cpp
// gradelib.cpp - Grade Calculator v1.1 - Chapter 10
```

Replace it with:

```cpp
// gradelib.cpp - Grade Calculator v1.2 - Chapter 11
```

Then find the start of `computePercentage`:

```cpp
double computePercentage(double earned, double possible) {
```

Directly below it, add:

```cpp
    // A roster can produce a zero denominator (every assignment worth 0, or
    // every assignment dropped), so the guard lives here rather than in every
    // caller.
    if (possible <= 0.0) { return 0.0; }
```

**Why:** This is the precondition from Step 2 turned into code. Returning
`0.0` for a zero denominator means a student whose assignments are all worth
nothing shows 0.0% rather than `inf` or `nan` — and because the check lives
here, every caller in the roster loop gets it for free.

#### Step 5 — Remove `assignLetterGrade`

In `gradelib.cpp`, find the whole of `assignLetterGrade` and the blank line below it, and delete all eight lines:

```cpp
char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}
```

**Why:** Its replacement arrives in the next step. Deleting it now, in the
same chapter, is deliberate: a program with two grading functions — one fixed,
one table-driven — invites a caller to use the wrong one, and the fixed one
would silently ignore whatever scale the user defined.

#### Step 6 — Add the three scale functions

Go to the very end of `gradelib.cpp`. After the last line, leave one blank line and add all three functions:

```cpp
void useDefaultScale(double cutoffs[], char letters[], int& count) {
    const char defLetters[] = {'A', 'B', 'C', 'D', 'F'};
    const double defCutoffs[] = {90.0, 80.0, 70.0, 60.0, 0.0};
    count = 5;
    for (int i = 0; i < count; ++i) {
        letters[i] = defLetters[i];
        cutoffs[i] = defCutoffs[i];
    }
}

int readGradeScale(double cutoffs[], char letters[]) {
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers from highest to lowest. The last tier should be 0.\n";
    std::cout << "Example: A 90, B 80, C 70, D 60, F 0\n\n";

    int count = 0;
    while (count < MAX_TIERS) {
        std::string prompt = "Tier " + std::to_string(count + 1) + " letter (or 'done'): ";
        std::string letterText = readNonEmptyLine(prompt);
        if (letterText == "done" || letterText.empty()) { break; }

        double cutoff = 0.0;
        if (!readNonNegative("  Minimum percentage for this tier: ", cutoff)) { break; }

        // Validation: cutoffs must strictly descend, or the lookup breaks.
        if (count > 0 && cutoff >= cutoffs[count - 1]) {
            std::cout << "  Cutoff must be lower than the previous tier ("
                      << cutoffs[count - 1] << "). Tier not added.\n";
            continue;
        }
        letters[count] = letterText[0];
        cutoffs[count] = cutoff;
        ++count;
    }

    // A scale that does not reach 0 leaves low scores unclassified.
    if (count == 0 || cutoffs[count - 1] > 0.0) {
        std::cout << "\nNote: your scale did not reach 0, so an 'F' at 0 was added.\n";
        if (count < MAX_TIERS) {
            letters[count] = 'F';
            cutoffs[count] = 0.0;
            ++count;
        }
    }
    return count;
}

char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int i = 0; i < count; ++i) {
        if (percentage >= cutoffs[i]) {
            return letters[i];
        }
    }
    return '?';
}
```

**Why:** Three things to notice.

**`useDefaultScale` copies from local arrays.** It writes the course default
into the caller's arrays element by element. The `const char defLetters[] =
{...}` initializer form is how you write a small fixed table inline.

**`readGradeScale` validates that cutoffs descend.** `if (count > 0 && cutoff
>= cutoffs[count - 1])` refuses a tier that is not strictly below the one
before it. This is not fussiness: `letterFor` returns the *first* tier the
percentage reaches, so an out-of-order table silently returns wrong letters
rather than failing. The function also appends an `F` at 0 if the user's scale
stops short, because a scale that never reaches 0 leaves low percentages with
no letter at all — `letterFor` would return `'?'`.

**`letterFor` is the payoff.** Compare it with the chain it replaces:

```cpp
for (int i = 0; i < count; ++i) {
    if (percentage >= cutoffs[i]) { return letters[i]; }
}
return '?';
```

Four lines, and it works for *any* scale with any number of tiers. The
Chapter 6 chain was eight lines and worked for exactly one scale. **Replacing
branching logic with a loop over data is one of the most valuable moves in
programming**, and this is the clearest example of it in the book.

> **Do not click Run yet.** `main.cpp` still calls `assignLetterGrade`, which
> no longer exists, so the link will fail. Finish Steps 7 and 8 first.

#### Step 7 — Rewrite the top of `main.cpp`

In `main.cpp`, find the comment header and the include lines — eight lines in all:

```cpp
// main.cpp - Grade Calculator v1.1 - Chapter 10
// Same behavior as v1.0, now split across three files with validated input.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>
```

Replace all eight with these sixteen:

```cpp
// main.cpp - Grade Calculator v1.2 - Chapter 11
// Multi-student roster on arrays, plus a USER-DEFINED letter grade scale.
// New this version: 2D arrays, parallel arrays, table-driven grade lookup.
//
// Central lesson: the hard-coded if/else chain of v1.1 becomes a loop over a
// table of data. Changing the grading scheme no longer means changing code.
//
// Build: g++ -std=c++17 -Wall -Wextra main.cpp gradelib.cpp -o gradecalc
#include "gradelib.h"

#include <iomanip>
#include <iostream>
#include <string>

const int MAX_STUDENTS = 40;
const int MAX_ASSIGNMENTS = 20;
```

**Why:** `MAX_STUDENTS` and `MAX_ASSIGNMENTS` live in `main.cpp`, not the
library, because they describe *this program's* capacity rather than anything
about grading. `MAX_TIERS` went in the header instead, because the library's
own `readGradeScale` needs it. Deciding which constant belongs on which side of
the interface is the same judgment as deciding which functions belong there.

#### Step 8 — Replace the body with the roster

In `main.cpp`, find the start of `readAssignment`:

```cpp
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
```

Delete that line and everything below it (both helper functions and the whole of the old `main`), down to and including this line:

```cpp
    return 0;
```

In the space where that code was, enter this:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v1.2 ===\n";

    // Parallel arrays: studentNames[s] belongs with pointsEarned[s][...]
    std::string studentNames[MAX_STUDENTS];
    std::string assignmentNames[MAX_ASSIGNMENTS];
    double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS] = {{0.0}};
    double pointsPossible[MAX_ASSIGNMENTS] = {0.0};
    int studentCount = 0;
    int assignmentCount = 0;

    double cutoffs[MAX_TIERS] = {0.0};
    char letters[MAX_TIERS] = {'\0'};
    int tierCount = 0;

    std::string useCustom = readNonEmptyLine("Define a custom grade scale? (y/n): ");
    if (!useCustom.empty() && (useCustom[0] == 'y' || useCustom[0] == 'Y')) {
        tierCount = readGradeScale(cutoffs, letters);
    } else {
        useDefaultScale(cutoffs, letters, tierCount);
        std::cout << "Using the default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    std::cout << "\n--- Enter assignments ---\n";
    while (assignmentCount < MAX_ASSIGNMENTS) {
        std::string name = readNonEmptyLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        assignmentNames[assignmentCount] = name;
        if (!readNonNegative("  Points possible: ", pointsPossible[assignmentCount])) { break; }
        ++assignmentCount;
    }

    std::cout << "\n--- Enter students ---\n";
    while (studentCount < MAX_STUDENTS) {
        std::string name = readNonEmptyLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames[studentCount] = name;
        for (int a = 0; a < assignmentCount; ++a) {
            std::string prompt = "  " + assignmentNames[a] + " points earned (incl. bonus): ";
            if (!readNonNegative(prompt, pointsEarned[studentCount][a])) { break; }
        }
        ++studentCount;
    }

    // ---------- report ----------
    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (int s = 0; s < studentCount; ++s) {
        double earned = 0.0;
        double possible = 0.0;
        for (int a = 0; a < assignmentCount; ++a) {
            earned += pointsEarned[s][a];
            possible += pointsPossible[a];
        }
        double pct = computePercentage(earned, possible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(9) << formatGrade(pct) << "   "
                  << formatGrade(letterFor(pct, cutoffs, letters, tierCount)) << "\n";
    }

    if (studentCount > 0) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(9)
                  << formatGrade(classTotal / studentCount) << "\n";
    } else {
        std::cout << "No students entered.\n";
    }

    std::cout << "\nPer-assignment averages:\n";
    for (int a = 0; a < assignmentCount; ++a) {
        double sum = 0.0;
        for (int s = 0; s < studentCount; ++s) { sum += pointsEarned[s][a]; }
        double avg = (studentCount > 0) ? sum / studentCount : 0.0;
        std::cout << "  " << std::left << std::setw(20) << assignmentNames[a]
                  << avg << " / " << pointsPossible[a] << "\n";
    }
    return 0;
```

**Why:** `readAssignment` and `printReport` go because both assumed a single
student. What replaces them is the chapter's data structure work.

**The 2D array.** `double pointsEarned[MAX_STUDENTS][MAX_ASSIGNMENTS]` is a
grid: `pointsEarned[s][a]` is student `s`'s score on assignment `a`. The
`= {{0.0}}` initializer zeroes the whole thing — without it the array holds
whatever was in that memory, and a student who skipped an assignment would get
a garbage score.

**Parallel arrays.** `studentNames[s]` describes the same student as
`pointsEarned[s][...]`, and `assignmentNames[a]` and `pointsPossible[a]` the
same assignment. Nothing in the language enforces that correspondence — it is
a convention you maintain, which is exactly why the comment naming it is
there. Insert into one and forget the other and the data silently misaligns.
Chapter 14 replaces this arrangement with `struct`s, which make the grouping
real.

**Nested loops.** The report's outer loop walks students; the inner loop walks
that student's assignments to total them. The per-assignment averages at the
end invert the nesting — outer over assignments, inner over students — to sum
a *column* of the grid instead of a row. Which index is on the outside
determines what you are summing, and getting that backwards is a classic
error.

**Counts, not capacities.** Every loop runs to `studentCount` or
`assignmentCount`, never to `MAX_STUDENTS` or `MAX_ASSIGNMENTS`. The arrays
are 40 long but only the first `studentCount` entries hold real data; reading
past the count gives you the zeroes from initialization and a wrong class
average. **With fixed arrays you always track how many entries are actually in
use** — the array cannot tell you.

> **▶ Run checkpoint:** Click **Run** with all three files open, then work through the test plan below in the Terminal.

#### Test plan

**1. Default scale, two assignments, two students.** Answer `n` to the custom
scale, then `Essay` / `50`, `Quiz` / `20`, `done`; then `Ada Lovelace` with
`45` and `18`, `Grace Hopper` with `30` and `10`, `done`. Expected:

```text
=====================================
  CLASS REPORT
=====================================
Ada Lovelace            90.0%   A
Grace Hopper            57.1%   F
-------------------------------------
CLASS AVERAGE           73.5%

Per-assignment averages:
  Essay               37.5 / 50.0
  Quiz                14.0 / 20.0
```

Check the arithmetic by hand: Ada has 63 of 70 possible, which is 90.0%.

**2. A custom scale.** Answer `y`, then enter `A` 85, `B` 70, `C` 50, `done`.
Note the message that an `F` at 0 was added — your scale stopped at 50, so
anything below it had no letter. Then one assignment worth `100`, and students
scoring `88` and `60`. With this scale 88 is an `A` and 60 is a `C`; with the
default scale they would be a `B` and a `D`. **Same program, same data,
different scheme, no recompile** — that is the chapter.

**3. Cutoffs must descend.** Answer `y`, enter `A` 80, then `B` 90. The tier is
refused with a message naming the previous cutoff. Enter `B` 70 instead and
carry on.

**4. Bad input still recovers.** At any points prompt type `abc`, then `-5`,
then a real number. The library's validation from Chapter 10 is unchanged and
still handles both.

**5. No students.** Answer `n`, enter one assignment, then `done` immediately
at the student prompt. The report prints `No students entered.` and the program
exits normally — no division by zero.

#### Check your work

Then confirm:

- [ ] All three files compile together with no errors and **no warnings**.
- [ ] `A_CUTOFF` through `D_CUTOFF` and `assignLetterGrade` no longer appear
      anywhere in the project.
- [ ] A custom scale changes the letters awarded without any code change.
- [ ] A tier whose cutoff is not below the previous one is refused.
- [ ] A scale that does not reach 0 gets an `F` at 0 appended, with a message.
- [ ] Per-student percentages match a hand calculation of their row.
- [ ] Per-assignment averages match a hand calculation of their column.
- [ ] Entering no students prints `No students entered.` and exits cleanly.
- [ ] Every loop runs to a count, never to `MAX_STUDENTS` or
      `MAX_ASSIGNMENTS`.

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — for this chapter that is `main.cpp`, `gradelib.h`, and `gradelib.cpp` — all three must be open. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1436xxx-Grade-Calculator-YourLastName** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 11 Grade Calculator v1.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 11 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Declaring, indexing, traversing

```cpp
#include <iostream>

int main() {
    const int COUNT = 5;
    double scores[COUNT] = {9.0, 84.0, 18.0, 45.0, 30.0};

    std::cout << "first: " << scores[0] << "\n";
    std::cout << "last:  " << scores[COUNT - 1] << "\n";

    double total = 0.0;
    for (int k = 0; k < COUNT; ++k) {
        total += scores[k];
    }
    std::cout << "total: " << total << "\n";
    return 0;
}
```

**Expected output:**

```text
first: 9
last:  30
total: 186
```

*Try:* Change `k < COUNT` to `k <= COUNT` and run it several times. Does the total change between runs? What does that tell you?

### 2. Finding the largest

```cpp
#include <iostream>

int main() {
    const int COUNT = 5;
    double scores[COUNT] = {9.0, 84.0, 18.0, 45.0, 30.0};

    double highest = scores[0];
    for (int k = 1; k < COUNT; ++k) {
        if (scores[k] > highest) { highest = scores[k]; }
    }
    std::cout << "highest: " << highest << "\n";
    return 0;
}
```

**Expected output:**

```text
highest: 84
```

*Try:* Change all five values to negative numbers, then change `highest = scores[0]` to `highest = 0.0`. What answer do you get, and why is it wrong?

### 3. Arrays and functions

```cpp
#include <iostream>

double sum(const double values[], int count) {
    double total = 0.0;
    for (int k = 0; k < count; ++k) { total += values[k]; }
    return total;
}

int main() {
    double scores[4] = {10.0, 20.0, 30.0, 40.0};
    std::cout << "sum: " << sum(scores, 4) << "\n";
    std::cout << "wrong count: " << sum(scores, 6) << "\n";
    return 0;
}
```

**Expected output:** the first line is `sum: 100`. The second reads past the end and prints an unpredictable value.

*Try:* Remove `const` from the parameter and add `values[0] = 0.0;` inside `sum`. Print `scores[0]` in `main` afterward. What does that tell you about how arrays are passed?

### 4. Two-dimensional traversal

```cpp
#include <iomanip>
#include <iostream>

int main() {
    const int STUDENTS = 3;
    const int ASSIGNMENTS = 2;
    double points[STUDENTS][ASSIGNMENTS] = {{9.0, 84.0}, {7.5, 91.0}, {10.0, 62.0}};

    for (int s = 0; s < STUDENTS; ++s) {
        double total = 0.0;
        for (int a = 0; a < ASSIGNMENTS; ++a) { total += points[s][a]; }
        std::cout << "student " << s << " total: " << total << "\n";
    }
    for (int a = 0; a < ASSIGNMENTS; ++a) {
        double total = 0.0;
        for (int s = 0; s < STUDENTS; ++s) { total += points[s][a]; }
        std::cout << "assignment " << a << " total: " << total << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
student 0 total: 93
student 1 total: 98.5
student 2 total: 72
assignment 0 total: 26.5
assignment 1 total: 237
```

*Try:* Add a per-student average. Which loop does that belong in?

### 5. Table-driven grade lookup

```cpp
#include <iostream>

char letterFor(double percentage, const double cutoffs[], const char letters[], int count) {
    for (int k = 0; k < count; ++k) {
        if (percentage >= cutoffs[k]) { return letters[k]; }
    }
    return '?';
}

int main() {
    double cutoffs[5] = {90.0, 80.0, 70.0, 60.0, 0.0};
    char letters[5]   = {'A',  'B',  'C',  'D',  'F'};

    double tests[5] = {95.0, 85.0, 75.0, 65.0, 30.0};
    for (int k = 0; k < 5; ++k) {
        std::cout << tests[k] << " -> " << letterFor(tests[k], cutoffs, letters, 5) << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
95 -> A
85 -> B
75 -> C
65 -> D
30 -> F
```

*Try:* Change the arrays to a plus-minus scale with eight tiers, updating the count. **You did not touch `letterFor`.** Now do the same to the Chapter 6 chain and compare the effort.

### 6. Parallel arrays drift

```cpp
#include <iostream>
#include <string>

int main() {
    std::string names[3] = {"Ada", "Grace", "Alan"};
    double totals[3]     = {89.0, 91.5, 72.0};

    // Someone "fixes" the order of one array and not the other.
    std::string temp = names[0];
    names[0] = names[2];
    names[2] = temp;

    for (int k = 0; k < 3; ++k) {
        std::cout << names[k] << ": " << totals[k] << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
Alan: 89
Grace: 91.5
Ada: 72
```

*Try:* Every grade is now attached to the wrong student, and the program reported it confidently. Write one sentence describing what would have to be true for this bug to be impossible. Chapter 14 makes it so.

### 7. Reason about arrays

- An array is declared `double a[8];`. What are the valid indices? What is `a[8]`?
- Why must a function receiving an array also receive its size?
- Why does adding `const` to an array parameter matter more than adding it to a `double` parameter?
- A grading scale has 12 tiers. How many lines does the table-driven lookup need? How many does an `if/else if` chain need?
- Give one thing parallel arrays cannot guarantee that a single array of records could.

---

## Summary

- An **array** holds many values of one type under one name, reached by **index**. Indices start at **0**; an array of size *n* has valid indices 0 through *n*−1.
- The size must be a **compile-time constant**. Always initialize.
- **C++ does not check bounds.** Going past the end is undefined behavior — it may work, corrupt data, or crash. Use `< size`, never `<= size`.
- `for (int k = 0; k < size; ++k)` visits every element exactly once.
- **Arrays pass by reference automatically** and do not carry their size, so always pass the count. Mark array parameters `const` unless you intend to modify them.
- **Parallel arrays** associate values by shared index and are fragile: nothing enforces the correspondence. Chapter 14 replaces them with `struct`.
- A **two-dimensional array** is a grid; nested loops traverse it, and swapping the loops answers a different question.
- **Replacing a conditional chain with a table of data** shrinks the code and, decisively, allows the data to come from the user. This is the chapter's central lesson and it recurs in Chapters 14 and 18.
- **Data from outside the program must be validated inside it.** What the compiler used to guarantee is now your job.
- **C strings** are `char` arrays ending in `'\0'`. Use `std::string`. **Command-line arguments** are reference material only.

---

## Key Terms

**array** — a collection of values of one type, stored under one name and reached by index.

**bounds** — the valid range of indices for an array, 0 through size−1.

**C string** — a `char` array terminated by the null character `'\0'`.

**element** — one value stored in an array.

**index** — the number identifying an element's position; also called a subscript.

**null terminator** — the `'\0'` character marking the end of a C string.

**out of bounds** — an index outside the valid range; undefined behavior.

**parallel arrays** — separate arrays in which the same index refers to related values.

**row-major order** — the layout in which each row of a two-dimensional array is stored contiguously.

**subscript** — the bracketed index used to reach an element.

**table-driven** — organized so that behavior is determined by data rather than by branching code.

**two-dimensional array** — an array of arrays, forming a grid.

---

**Next:** Chapter 12 removes the fixed maxima. `std::vector` grows to fit any number of students, assignments, or grade tiers, `std::string` replaces the last of the fixed-length text, and the calculator gains a drop-lowest feature. That version is the Course I capstone. Grade Calculator v1.3.
