from engine import *
from common import *

BASE, TARGET, CHAPTER = "v2.5", "v2.6", 19
M = "main.cpp"

ITEMS = [
    header("Split Classes into Files", "v2.6",
           "Your committed Chapter 18 v2.5 program (`main.cpp`)."),
    Md("""
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
"""),
    HOW_TO_READ,
    Md("""
> **Heads-up:** Steps 1–4 create the new files; Steps 5–7 remove the old
> class code from `main.cpp`. Do **not** click Run until the checkpoint at the
> end of Step 7 — until then, the classes exist in two places at once.

#### Build it: step by step

##### Step 1 — Create `assignment.h` and `assignment.cpp`

A **header** declares what a class looks like; its **implementation file**
defines the function bodies. Other files `#include` the header, never the
`.cpp`.
"""),
    Create("assignment.h", sol(TARGET, "assignment.h"),
           intro="Create a new file named `assignment.h` and enter this code:"),
    Md("""
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
"""),
    Create("assignment.cpp", sol(TARGET, "assignment.cpp"),
           intro="Create a new file named `assignment.cpp` and enter this code:"),
    Md("""
Each definition outside the class is written with the class name and the
**scope resolution operator**: `Assignment::totalEarned()`. The constructor's
default argument (`bonus = 0.0`) appears only in the header, never again here.

`operator<<` prints an assignment as one aligned line — name, total earned,
and points possible, plus a bonus note when there is one — and **returns the
stream**, which is what lets you chain `<<` calls.

##### Step 2 — Create `gradescale.h` and `gradescale.cpp`
"""),
    Create("gradescale.h", sol(TARGET, "gradescale.h"),
           intro="Create a new file named `gradescale.h` and enter this code:"),
    Create("gradescale.cpp", sol(TARGET, "gradescale.cpp"),
           intro="Create a new file named `gradescale.cpp` and enter this code:"),
    Md("""
Two changes from Chapter 18 besides the split:

- The invariant now lives in a **comment above the class**, where anyone
  reading the header will see it. The constructor logic that enforces it is
  unchanged.
- Chapter 18's `describe()` member is gone. **`operator<<` replaces it**, so
  printing a scale is `std::cout << scale` — the same way you print anything
  else. Unlike `describe()`, it does not add `"  "` in front or a newline at the
  end; the caller decides the layout.

##### Step 3 — Create `student.h` and `student.cpp`
"""),
    Create("student.h", sol(TARGET, "student.h"),
           intro="Create a new file named `student.h` and enter this code:"),
    Create("student.cpp", sol(TARGET, "student.cpp"),
           intro="Create a new file named `student.cpp` and enter this code:"),
    Md("""
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
"""),
    Create("gradebook.h", sol(TARGET, "gradebook.h"),
           intro="Create a new file named `gradebook.h` and enter this code:"),
    Md("""
- All the data is `private`. The roster can change only through
  `addStudent` and `sortByPercentage`, so those are the only two places that
  could ever corrupt it.
- `operator[]` returns a `const Student&` for a position. Its comment states
  the **precondition** (`index < size()`); it does not check.
- `claimNextId()` returns the next ID and advances the counter in one call,
  so an ID can never be handed out twice.
"""),
    Create("gradebook.cpp", sol(TARGET, "gradebook.cpp"),
           intro="Create a new file named `gradebook.cpp` and enter this code:"),
    Md("""
- `sortByPercentage()` is one line: `std::sort` puts the roster in order
  using `Student::operator<`, so it sorts highest percentage first.
- `operator<<` for `Gradebook` prints the whole report. It prints the course
  name, then the scale **using the scale's own `<<`**, then each student
  **using the student's own `<<`**, followed by the letter grade, and finally
  a class average. Each class knows how to print itself, and nothing knows how
  to print anything else.

##### Step 5 — Update the header comment in `main.cpp`

Now switch to `main.cpp`. From here on, `main.cpp` only runs the menu.
"""),
    Replace(M, seg(BASE, M, "// ====", "// ====", 2), seg(TARGET, M, "// ====", "// ====", 2),
            intro="At the top of `main.cpp`, find the header comment:"),
    Md("""
The new `Build` line lists all five `.cpp` files — every one must be compiled
and linked together.

##### Step 6 — Remove the classes from `main.cpp`

The classes now live in their own files, so `main.cpp` must stop defining
them. It includes `gradebook.h` instead, which in turn includes the other
headers.
"""),
    DeleteRange(M, "#include <algorithm>", "double readNonNegative(const std::string& prompt) {",
                intro="Just below the header comment, find the first `#include` line:",
                between="the remaining `#include` lines, `CAP_AT_100`, all three classes, "
                        "and the *Input helpers* banner",
                exclusive=True,
                new='#include "gradebook.h"\n\n#include <iostream>\n#include <limits>\n#include <string>\n\n',
                after="In the space where that code was, enter:"),
    Md("""
Afterward, `main.cpp` should begin with the header comment, then these four
`#include` lines, then `readNonNegative`.

*Why:* a class must be defined exactly once in the whole program. If
`main.cpp` kept its own copy, the program would have two definitions of each
class. Quoted includes (`"gradebook.h"`) name your own files; angle-bracket
includes (`<iostream>`) name the standard library.

##### Step 7 — Rewrite `main` to use a `Gradebook`
"""),
    DeleteRange(M, "int main() {", "}", last=True,
                intro="Find the start of `main`:",
                end_text="all the way to the final closing `}` at the very end of the file.",
                new=seg(TARGET, M, "int main() {", "return 0;") + "}\n",
                after="In its place, enter the new `main`:"),
    Md("""
What changed:

- `Gradebook book("Programming Fundamentals");` replaces the three loose
  variables from Chapter 18.
- **Add student** gets its ID from `book.claimNextId()` and stores the student
  with `book.addStudent(s)`.
- **Report** is now one line: `std::cout << book << "\\n";`.
- **Sort by grade** (new, option 3) calls `book.sortByPercentage()`.
- **Custom scale** (now option 4) builds the scale exactly as before and hands
  it to `book.setScale(...)`, then prints it with `<<`.
- **Quit** moves to option 5.
"""),
    Run("Make sure all nine files are open in the editor, then click **Run**. "
        "The program should compile with no errors and no warnings and show "
        "the v2.6 banner and the five-option menu. An `undefined reference` "
        "error means a `.cpp` file is not open or a function name is "
        "misspelled; a `redefinition` error means a class is still defined in "
        "`main.cpp`."),
    Md("""
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
"""),
    workflow("`main.cpp` to open it. You will create the eight new files in "
             "the editor during the lab.",
             "Work through Steps 1–7 above in StudySite's internal editor, in "
             "order. Keep every file open, and click **Run** at the ▶ Run "
             "checkpoint at the end of Step 7."),
    save(CHAPTER, TARGET, "all nine files: `main.cpp` plus the four `.h` and four "
         "`.cpp` files you created."),
]
