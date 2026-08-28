# Chapter 14 — Structs: Grouping Related Data

## Learning Objectives

When you finish this chapter you will be able to:

- Explain the specific weakness of parallel arrays that a record removes. *(SLO 2.2, 2.6)*
- Declare a `struct` and access its members. *(SLO 2.2)*
- Pass structs to and from functions, by value and by `const` reference. *(SLO 2.2)*
- Build and traverse a vector of structs. *(SLO 2.2, 2.6)*
- Nest structs to model composite information. *(SLO 2.2)*
- Design a set of records from a requirements statement. *(SLO 2.2)*
- Explain how a struct differs from a class, and why structs come first. *(SLO 2.2, 2.8)*
- Build Grade Calculator v2.1, replacing every parallel-array pair with a record.

---

## 14.1 The Problem with Parallel Arrays

Chapter 11 introduced parallel arrays and flagged their weakness. Chapter 13 put "replace parallel arrays with records" at the top of your maintenance backlog as *preventive* work. This chapter does it.

Here is the weakness, made concrete:

```cpp
std::vector<std::string> names  = {"Ada", "Grace", "Alan"};
std::vector<double>      totals = {89.0, 91.5, 72.0};
```

The correspondence between `names[1]` and `totals[1]` exists only in your head. Nothing in the program records it. So:

- Sort one and not the other, and every grade attaches to the wrong student.
- Add to one and not the other, and they drift permanently out of step.
- Remove from the middle of one, and everything after it shifts by one.
- Pass one to a function without the other, and the function cannot know who a value belongs to.

Chapter 12's Exercise 6 demonstrated this: three students, one reordering, every grade wrong, and the program reported it confidently.

**None of these are hard to avoid. All of them are easy to forget.** That is the distinction worth holding on to — the goal is not to be more careful, but to make the mistake impossible to express.

---

## 14.2 Declaring and Using a `struct`

A **struct** groups related values into a single type:

```cpp
struct Assignment {
    std::string name;
    double pointsPossible = 0.0;
};
```

That declares a new type named `Assignment`. The values inside are its **members**.

Note the semicolon after the closing brace. It is required, and forgetting it produces a confusing error pointing at the *next* line.

Create one and use it:

```cpp
Assignment hw;
hw.name = "Homework 1";
hw.pointsPossible = 10.0;
```

Or initialize it directly:

```cpp
Assignment hw{"Homework 1", 10.0};
```

```text
hw.name=Homework 1 possible=10
```

Members are given values in declaration order. **Give members default values where you declare them**, as `= 0.0` does above — Appendix D Section D.6's initialization rule applies to members exactly as it does to variables.

---

## 14.3 Member Access

The dot operator reaches a member:

```cpp
hw.pointsPossible = 20.0;
std::cout << hw.name;
double half = hw.pointsPossible / 2.0;
```

You have used this syntax since Chapter 12 — `scores.size()`, `name.length()`. Those were member *functions* on objects. This is member *data* on a struct. Chapter 18 unifies the two, which is exactly why structs come first.

---

## 14.4 Structs and Functions

A struct is a value like any other. It can be passed, returned, and assigned:

```cpp
double total(const Student& s) {
    double t = 0.0;
    for (const Score& sc : s.scores) {
        t += sc.pointsEarned + sc.bonusPoints;
    }
    return t;
}
```

Chapter 10 Section 10.7's rule applies: **pass by `const` reference.** A struct may be large — this one contains a `std::string` and a `std::vector` — and copying it costs real work.

To modify, take a plain reference:

```cpp
void addScore(Student& s, double earned, double bonus) {
    s.scores.push_back({earned, bonus});
}
```

Unlike arrays, structs **assign and copy properly**:

```cpp
Student a = b;         // a full, independent copy — every member
```

This is one of the quiet advantages of records. Two parallel arrays cannot be copied as a unit; a struct can.

---

## 14.5 Vectors of Structs

The essential move:

```cpp
std::vector<Student> roster;
roster.push_back({"Ada", 1001, {}});
roster.push_back({"Grace", 1002, {{10.0, 0.0}}});
```

One vector. One `push_back`. Every field travels together, permanently.

Now look at what happens when you sort:

```cpp
std::sort(roster.begin(), roster.end(),
          [](const Student& a, const Student& b) { return total(a) > total(b); });
```

```text
1001 Ada 94
1002 Grace 10
```

Every student's name, ID, and scores moved together, because they were never separate. **The bug from Chapter 12's Exercise 6 cannot be written here.** There is no second array to forget.

That is what "structurally impossible" means, and it is worth being precise about the claim. The struct did not make you more careful. It removed the thing you had to be careful about.

---

## 14.6 Nested Structs

A struct member may itself be a struct:

```cpp
struct Score {
    double pointsEarned = 0.0;
    double bonusPoints  = 0.0;
};

struct Student {
    std::string name;
    int id = 0;
    std::vector<Score> scores;      // a vector of structs, inside a struct
};
```

Reach through with repeated dots:

```cpp
ada.scores[0].bonusPoints = 1.0;
```

Read it left to right: the student `ada`, her `scores`, the first one, its `bonusPoints`.

Nesting lets a record mirror the shape of the real thing. A student *has* scores; a score *has* earned and bonus points. When the data structure matches the problem, code that walks it tends to read plainly.

---

## 14.7 Designing Records from Requirements

Deciding what the records are is a **design** activity — Chapter 13's phase 3.

The technique is simple and effective: **read your requirements statement and look for the nouns.**

From the Grade Calculator specification: *student*, *assignment*, *points earned*, *points possible*, *bonus points*, *grade scale*, *tier*, *cutoff*, *letter*.

Group nouns that always travel together:

| Record | Members | Why grouped |
|---|---|---|
| `Assignment` | name, points possible | An assignment always has both |
| `Score` | points earned, bonus points | One student's result on one assignment |
| `Student` | name, ID, scores | A student has an identity and results |
| `GradeTier` | cutoff, letter | A cutoff is meaningless without its letter |

That last one deserves attention. `GradeTier` replaces the two parallel vectors — `gradeCutoffs` and `gradeLetters` — that Chapter 11 introduced. They were the most fragile thing in v1.3, because a mismatch between them silently assigns wrong letters to everyone.

**A useful test: if two values must always be updated together, they belong in one record.**

---

## 14.8 Structs as a Bridge to Classes

A struct holds data. It has no behavior — the functions operating on it live outside:

```cpp
struct Student { std::string name; int id = 0; std::vector<Score> scores; };

double total(const Student& s);           // outside the struct
double percentage(const Student& s);      // outside the struct
```

That is the **procedural** methodology from Chapter 13 Section 13.4: data and the code acting on it are separate.

Two consequences follow, and they are what Chapter 18 addresses.

**Nothing protects the members.** Any code can write `s.id = -5;` or leave `scores` inconsistent. The record groups the data but does not defend it.

**The related functions are not attached to it.** `total` and `percentage` are obviously about `Student`, but nothing in the program says so. They sit among every other function in the file.

A **class** fixes both: it bundles the data *with* the functions, and it can make members private so only those functions may touch them.

Structs come first because they are the smaller step. You get grouping now, and protection in Chapter 18, and you will be able to say precisely what the second step bought you.

> In C++ a `struct` and a `class` are the same construct with one difference: members of a struct are public by default, members of a class are private by default. Everything in Chapter 18 could be written with `struct`. The convention this book follows — and Appendix D Section D.7 states — is `struct` for plain data with no invariants, `class` when there is behavior or something to protect.

---

## Common Errors and Warnings

| What you see | Cause | Fix |
|---|---|---|
| `error: expected ';' after struct definition` | Missing semicolon after the closing brace | Add `;` |
| `error: 'name' was not declared in this scope` | Used a member without the object | Write `s.name`, not `name` |
| `error: 'struct Student' has no member named 'Name'` | Wrong capitalization | C++ is case-sensitive |
| Members contain garbage | No default values given | `double x = 0.0;` in the struct |
| The program is slow with a large roster | Passing structs by value | Take `const Student&` |
| A function's changes do not stick | Passed by value | Take `Student&` |
| `error: too many initializers` | More values than members | Match the member list |
| Values land in the wrong members | Initializer order does not match declaration order | Assign member by member |

---

## Design Notes

**If two values must always change together, put them in one record.** That is the test.

**Give every member a default value where it is declared.**

**Pass structs by `const` reference** unless modifying.

**Name records after the real-world thing they represent.** `Student`, `Assignment`, `GradeTier` — nouns from the requirements, not invented abbreviations.

**Keep records small and specific.** A struct with fifteen unrelated members is a bag, not a record.

---

## Grade Calculator v2.1 — Student Records

### What v2.1 does

Everything v1.3 did, with every parallel-array pair replaced by a record. Behavior is unchanged; **structure is the change**, and this is a preventive-maintenance item from your Chapter 13 backlog.

### The records

```cpp
struct Assignment {
    std::string name;
    double pointsPossible = 0.0;
};

struct Score {
    double pointsEarned = 0.0;
    double bonusPoints  = 0.0;
};

struct Student {
    std::string name;
    int id = 0;
    std::vector<Score> scores;   // one entry per assignment, same order
};

struct GradeTier {
    double cutoff = 0.0;
    char   letter = 'F';
};
```

### What each replaces

| v1.3 | v2.1 |
|---|---|
| `std::vector<std::string> assignmentNames` + `std::vector<double> pointsPossible` | `std::vector<Assignment>` |
| `std::vector<std::string> studentNames` + `std::vector<std::vector<double>> earned` | `std::vector<Student>` |
| `std::vector<double> gradeCutoffs` + `std::vector<char> gradeLetters` | `std::vector<GradeTier>` |

**Six containers become three.** More importantly, three opportunities for drift become zero.

### The grading functions

```cpp
std::vector<GradeTier> defaultScale() {
    return { {90.0, 'A'}, {80.0, 'B'}, {70.0, 'C'}, {60.0, 'D'}, {0.0, 'F'} };
}

char letterFor(double percentage, const std::vector<GradeTier>& scale) {
    for (const GradeTier& tier : scale) {
        if (percentage >= tier.cutoff) { return tier.letter; }
    }
    return '?';
}
```

Compare `letterFor` with v1.2's four-parameter version:

```cpp
// v1.2 — two arrays and a count, all of which must agree
char letterFor(double percentage, const double cutoffs[], const char letters[], int count);

// v2.1 — one thing
char letterFor(double percentage, const std::vector<GradeTier>& scale);
```

**Four parameters become two.** The count is gone because the vector knows its size; the second array is gone because the tiers are one thing. Three ways to pass inconsistent arguments have disappeared from the signature.

### Computing a student's percentage

```cpp
double studentPercentage(const Student& student,
                         const std::vector<Assignment>& assignments,
                         bool dropLowest) {
    double earned = 0.0;
    double possible = 0.0;
    for (std::size_t a = 0; a < assignments.size() && a < student.scores.size(); ++a) {
        earned   += student.scores[a].pointsEarned + student.scores[a].bonusPoints;
        possible += assignments[a].pointsPossible;
    }
    if (dropLowest && assignments.size() > 1) {
        std::size_t worst = 0;
        double worstRatio = 2.0;
        for (std::size_t a = 0; a < assignments.size() && a < student.scores.size(); ++a) {
            if (assignments[a].pointsPossible <= 0.0) { continue; }
            double ratio = (student.scores[a].pointsEarned + student.scores[a].bonusPoints)
                         / assignments[a].pointsPossible;
            if (ratio < worstRatio) { worstRatio = ratio; worst = a; }
        }
        if (worstRatio <= 1.0) {
            earned   -= student.scores[worst].pointsEarned + student.scores[worst].bonusPoints;
            possible -= assignments[worst].pointsPossible;
        }
    }
    return computePercentage(earned, possible);
}
```

### Expected output

Default scale; assignments `Homework 1` (10) and `Midterm` (100); Ada with 9 + 90 (bonus 5 on the midterm) and Alan with 8 + 70; drop-lowest off:

```text
=====================================
  CLASS REPORT
=====================================
1001  Ada                     94.5%   A
1002  Alan                    70.9%   C
-------------------------------------
CLASS AVERAGE                 82.7%
```

### What to notice

**Student IDs appeared.** Adding a field to a record is one line. Adding a parallel array would have meant finding every place the other arrays are touched and touching this one too — which is exactly the maintenance cost records remove.

**`student.scores[a].pointsEarned` reads as a path.** The student, her scores, the one for assignment `a`, the points earned. The expression describes the data.

**The `&& a < student.scores.size()` guard.** A student may have fewer scores recorded than there are assignments. The struct did not eliminate the need to check bounds — it eliminated the possibility of two containers being *silently* out of step. Chapter 18's `Student` class will enforce the correspondence properly.

**Nothing about the grading arithmetic changed.** This is a preventive refactor, and Chapter 13's rule applies: verify it by comparing output.

### Your StudySite Lab — Replace Parallel Arrays with Structs

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.1
- **Starting point:** The working Chapter 13 v2.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Create `GradeTier`, `Assignment`, and `Student` structs.
2. Replace parallel arrays and vectors with vectors of the appropriate record type.
3. Add a `Course` struct that owns the course name, assignments, students, and grade scale.
4. Pass a single `Course` object to report functions instead of unrelated containers.
5. Preserve all v2.0 behavior.


#### Verification

- Student names cannot be reordered separately from their scores.
- A grade letter cannot exist without its cutoff.
- The same input produces the same report as Chapter 13.
- The program builds without warnings.

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
4. Enter the commit message **Complete Chapter 14 Grade Calculator v2.1**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1437** contains the Chapter 14 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. A first struct

```cpp
#include <iostream>
#include <string>

struct Assignment {
    std::string name;
    double pointsPossible = 0.0;
};

int main() {
    Assignment hw;
    hw.name = "Homework 1";
    hw.pointsPossible = 10.0;

    Assignment exam{"Midterm", 100.0};

    std::cout << hw.name << " is worth " << hw.pointsPossible << "\n";
    std::cout << exam.name << " is worth " << exam.pointsPossible << "\n";
    return 0;
}
```

**Expected output:**

```text
Homework 1 is worth 10
Midterm is worth 100
```

*Try:* Remove the `= 0.0` default, declare an `Assignment` without initializing, and print `pointsPossible`. What do you get?

### 2. Structs in functions

```cpp
#include <iostream>
#include <string>

struct Assignment {
    std::string name;
    double pointsPossible = 0.0;
};

void describe(const Assignment& a) {
    std::cout << a.name << ": " << a.pointsPossible << " points\n";
}

void doubleValue(Assignment& a) {
    a.pointsPossible *= 2.0;
}

int main() {
    Assignment hw{"Homework 1", 10.0};
    describe(hw);
    doubleValue(hw);
    describe(hw);
    return 0;
}
```

**Expected output:**

```text
Homework 1: 10 points
Homework 1: 20 points
```

*Try:* Remove the `&` from `doubleValue`'s parameter. What changes, and why?

### 3. Nested structs and a vector of structs

```cpp
#include <iostream>
#include <string>
#include <vector>

struct Score   { double pointsEarned = 0.0; double bonusPoints = 0.0; };
struct Student { std::string name; int id = 0; std::vector<Score> scores; };

double total(const Student& s) {
    double t = 0.0;
    for (const Score& sc : s.scores) { t += sc.pointsEarned + sc.bonusPoints; }
    return t;
}

int main() {
    Student ada;
    ada.name = "Ada";
    ada.id = 1001;
    ada.scores.push_back({9.0, 1.0});
    ada.scores.push_back({84.0, 0.0});

    std::cout << ada.name << " (" << ada.id << ") total = " << total(ada) << "\n";
    std::cout << "first bonus: " << ada.scores[0].bonusPoints << "\n";
    return 0;
}
```

**Expected output:**

```text
Ada (1001) total = 94
first bonus: 1
```

*Try:* Add a third score and rerun. How many lines did you change?

### 4. Sorting keeps records intact

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

struct Student { std::string name; int id = 0; double total = 0.0; };

int main() {
    std::vector<Student> roster = {
        {"Ada", 1001, 89.0}, {"Grace", 1002, 91.5}, {"Alan", 1003, 72.0}
    };

    std::sort(roster.begin(), roster.end(),
              [](const Student& a, const Student& b) { return a.total > b.total; });

    for (const Student& s : roster) {
        std::cout << s.id << " " << s.name << " " << s.total << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
1002 Grace 91.5
1001 Ada 89
1003 Alan 72
```

*Try:* Compare this with Chapter 12's Exercise 6, where sorting one parallel array scrambled the data. What would you have to do here to produce that bug?

### 5. Replace parallel arrays

Rewrite this using a struct. Then say which specific bug becomes impossible.

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> titles = {"Intro", "Advanced"};
    std::vector<int> credits = {3, 4};
    std::vector<char> grades = {'A', 'B'};

    for (std::size_t k = 0; k < titles.size(); ++k) {
        std::cout << titles[k] << " " << credits[k] << " " << grades[k] << "\n";
    }
    return 0;
}
```

### 6. Design records from requirements

For a library system: *A member has a name, a membership number, and a list of borrowed books. A book has a title, an author, an ISBN, and a due date when borrowed. A due date has a day, a month, and a year.*

Write the structs. Which are nested? Which values must always change together?

### 7. Reason about records

- Why does a struct need a semicolon after its closing brace?
- Why pass a struct by `const` reference rather than by value?
- What is the test for whether two values belong in the same record?
- A struct groups data but does not protect it. Give one specific way a caller could put a `Student` into an invalid state.
- What is the only real difference between `struct` and `class` in C++?

---

## Summary

- **Parallel arrays** keep their correspondence only in the programmer's head. A **struct** records it in the program.
- A struct declares a new type whose **members** are accessed with the dot operator. The declaration ends with a **semicolon**.
- **Give every member a default value where it is declared.**
- Structs are passed and returned like any value. **Pass by `const` reference** unless modifying. Unlike arrays, structs **copy properly**.
- A **vector of structs** keeps every field of every record together permanently. Sorting cannot scramble them, because there is nothing to keep in step.
- Structs **nest**, letting a record mirror the shape of the real thing.
- Design records by finding the **nouns** in your requirements. **If two values must always be updated together, they belong in one record.**
- A struct groups data but does not **protect** it, and the functions that operate on it live outside. Chapter 18's **class** fixes both.
- In C++ `struct` and `class` differ only in default access. Use `struct` for plain data, `class` when there is behavior or an invariant to defend.

---

## Key Terms

**aggregate initialization** — initializing a struct's members with a brace-enclosed list in declaration order.

**dot operator** — `.`, used to reach a member of a struct or object.

**member** — a variable declared inside a struct or class.

**nested struct** — a struct used as the type of a member of another struct.

**record** — a group of related values treated as one item; in C++, a struct.

**struct** — a type grouping related values under one name.

---

**Next:** Chapter 15 makes your gradebook survive being closed. File streams save the roster, the assignments, and the custom grade scale to a text file and read them back — and you will design the file format yourself, including deciding whether it can accommodate a feature you have not built yet. Grade Calculator v2.2.
