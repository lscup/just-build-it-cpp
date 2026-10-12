from engine import *
from common import *

BASE, TARGET, CHAPTER = "v2.6", "v3.0", 20
M = "main.cpp"


def line(ver, f, text):
    return seg(ver, f, text, text)


ITEMS = [
    header("Add Weighted Grading with Inheritance", "v3.0",
           "Your committed Chapter 19 v2.6 program (nine files)."),
    Md("""
#### What you will build

The Grade Calculator has always graded by points: total earned ÷ total
possible. In this lab you add a second rule — **weighted categories** — using
**inheritance**. By the end you will have:

1. A **category** on every `Assignment` (for example `Exam` or `Homework`),
   added in a way that leaves every existing call compiling unchanged.
2. A base class `GradingScheme` holding the behavior every scheme shares (a
   name, and the cap-and-round policy), and two **derived classes**:
   `PointsBased` and `Weighted`.
3. A `Gradebook` that grades each student with whichever scheme was chosen at
   startup, and shows the scheme in the report.
4. A startup question in `main` that picks the scheme for the session, an
   optional step to enter your own category weights, and a *Category* prompt
   for each assignment.

The menu keeps the same five options as Chapter 19.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `assignment.h`, `assignment.cpp` | Edit (Step 1) |
| `gradingscheme.h`, `gradingscheme.cpp` | Create (Steps 2–3) |
| `student.h` | Edit — comments only (Step 4) |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 5–6) |
| `main.cpp` | Edit (Steps 7–8) |
| `gradescale.h`, `gradescale.cpp`, `student.cpp` | No change — keep them open |

When you are finished your project has **eleven files**, and all of them must
be open in the editor when you click **Run**.
"""),
    HOW_TO_READ,
    Md("""
#### Build it: step by step

##### Step 1 — Give `Assignment` a category

Weighted grading needs to know which category each assignment belongs to. Add
a `category` to `Assignment`, with a **default value** so that every existing
call to the constructor still compiles without being edited.
"""),
    Replace("assignment.h", line(BASE, "assignment.h", "// assignment.h - Grade Calculator"), line(TARGET, "assignment.h", "// assignment.h - Grade Calculator"),
            intro="The first line of every class file records the version in which that file last changed. In `assignment.h`, update it. Find:"),
    Replace("assignment.h",
            line(BASE, "assignment.h", "Assignment(const std::string& name, double earned"),
            seg(TARGET, "assignment.h", "Assignment(const std::string& name, double earned",
                "category = \"Uncategorized\");"),
            intro="In `assignment.h`, find the constructor declaration:"),
    InsertAfter("assignment.h", line(BASE, "assignment.h", "double bonusPoints() const"),
                line(TARGET, "assignment.h", "category() const"),
                intro="Still in `assignment.h`, find the `bonusPoints()` accessor:"),
    InsertAfter("assignment.h", line(BASE, "assignment.h", "double bonusPoints_    = 0.0;"),
                line(TARGET, "assignment.h", "std::string category_"),
                intro="Near the bottom of the class, find the last data member:"),
    Replace("assignment.cpp", line(BASE, "assignment.cpp", "// assignment.cpp - Grade Calculator"), line(TARGET, "assignment.cpp", "// assignment.cpp - Grade Calculator"),
            intro="In `assignment.cpp`, update the first line. Find:"),
    Replace("assignment.cpp",
            seg(BASE, "assignment.cpp", "Assignment::Assignment(", "bonusPoints_(bonus) {}"),
            seg(TARGET, "assignment.cpp", "Assignment::Assignment(", "category_(category) {}"),
            intro="In `assignment.cpp`, find the constructor definition:"),
    InsertAfter("assignment.cpp",
                seg(BASE, "assignment.cpp", 'out << "  (+"', "    }"),
                line(TARGET, "assignment.cpp", "a.category()"),
                intro="Still in `assignment.cpp`, near the end of `operator<<`, find:"),
    Md("""
*Why:* adding a parameter **with a default** at the end of a parameter list
extends a function without breaking any caller — the Chapter 10 technique.
`Assignment("HW1", 9, 10)` still compiles and simply gets the category
`"Uncategorized"`. The default value appears only in the header declaration.
"""),
    Run("Click **Run** with all nine files open. The program should compile "
        "cleanly and behave exactly like v2.6. Nothing uses the category yet."),
    Md("""
##### Step 2 — Create the `GradingScheme` hierarchy (`gradingscheme.h`)

A **base class** holds what every grading scheme has in common. Each **derived
class** adds its own rule.
"""),
    Create("gradingscheme.h", sol(TARGET, "gradingscheme.h"),
           intro="Create a new file named `gradingscheme.h` and enter this code:"),
    Md("""
Read the three classes carefully:

- `GradingScheme` stores a `name_` and provides `finalize()`, the course's
  cap-and-round policy. `finalize` is **`protected`**: derived classes can
  call it, but code outside the hierarchy cannot. It is `static` because it
  does not need any one object's data.
- `class PointsBased : public GradingScheme` reads "a `PointsBased` **is a**
  `GradingScheme`." Its constructor passes the name `"Points-based"` up to the
  base-class constructor in its initializer list.
- `Weighted` adds a nested `CategoryWeight` struct (a category name and its
  weight) and a list of weights. It can tell you whether the weights total
  100 (`weightsValid()`).
- Notice that `computePercentage` is **not** `virtual` yet. Each derived class
  has its own version, but the program must still decide by hand which one to
  call. Chapter 21 removes that limitation.

##### Step 3 — Implement the two schemes (`gradingscheme.cpp`)
"""),
    Create("gradingscheme.cpp", sol(TARGET, "gradingscheme.cpp"),
           intro="Create a new file named `gradingscheme.cpp` and enter this code:"),
    Md("""
- `PointsBased::computePercentage` is the same points math you have used since
  Chapter 4, now ending in `finalize(...)` from the base class.
- `Weighted::Weighted()` sets the default weights: Exam 50, Homework 30,
  Participation 20.
- `weightsValid()` compares the total to 100 **with a tolerance**
  (`< 0.001`), never with `==`, because the weights are `double`s — the
  floating-point trap from Chapter 6.
- `Weighted::computePercentage` scores each category separately and combines
  them by weight. A category with **no graded work yet is skipped**, and its
  weight is spread across the categories that do have work, so a student is
  not penalized for assignments that have not been given.
"""),
    Run("Open both new files and click **Run**. The program should compile "
        "cleanly and still behave exactly like v2.6 — the new classes exist but "
        "nothing uses them yet."),
    Md("""
##### Step 4 — Note the new role of `Student::percentage()`

`Student::percentage()` still computes a points-based percentage, but the
course grade will now come from a grading scheme. Record that in a comment so
the next reader is not misled.
"""),
    Replace("student.h", line(BASE, "student.h", "// student.h - Grade Calculator"), line(TARGET, "student.h", "// student.h - Grade Calculator"),
            intro="In `student.h`, update the first line. Find:"),
    Replace("student.h",
            seg(BASE, "student.h", "double totalPossible() const;", "double percentage() const;"),
            seg(TARGET, "student.h", "double totalPossible() const;", "double percentage() const;"),
            intro="In `student.h`, find:"),
    Md("""
This is a comment-only change; `student.cpp` does not change at all.

##### Step 5 — Make `Gradebook` scheme-aware (`gradebook.h`)
"""),
    Replace("gradebook.h", line(BASE, "gradebook.h", "// gradebook.h - Grade Calculator"), line(TARGET, "gradebook.h", "// gradebook.h - Grade Calculator"),
            intro="In `gradebook.h`, update the first line. Find:"),
    InsertBefore("gradebook.h", line(BASE, "gradebook.h", '#include "gradescale.h"'),
                 line(TARGET, "gradebook.h", '#include "gradingscheme.h"'),
                 intro="In `gradebook.h`, find the first project include:"),
    Replace("gradebook.h",
            line(BASE, "gradebook.h", "explicit Gradebook(const std::string& courseName"),
            seg(TARGET, "gradebook.h", "/** Which grading rule", "void setWeights("),
            intro="Find the constructor declaration:"),
    Replace("gradebook.h",
            seg(BASE, "gradebook.h", "int nextId_ = 1001;", "};"),
            seg(TARGET, "gradebook.h", "int nextId_ = 1001;", "};"),
            intro="At the bottom of the class, find:"),
    Md("""
What you added:

- `enum class Scheme { Points, Weighted };` names the two choices. Because it
  is declared inside `Gradebook`, its full name is `Gradebook::Scheme`.
- The constructor takes a second parameter, the scheme, **defaulting to
  `Scheme::Points`** — so `Gradebook book("Programming Fundamentals");` still
  compiles.
- `percentageFor(s)` returns a student's course grade under the selected
  scheme; `schemeName()` returns its display name.
- `weightedScheme()` and `setWeights()` let `main` read and replace the
  weights.
- The `Gradebook` **holds one object of each scheme** (`points_` and
  `weighted_`) plus the `scheme_` flag that says which to use.

##### Step 6 — Grade through the selected scheme (`gradebook.cpp`)
"""),
    Replace("gradebook.cpp", line(BASE, "gradebook.cpp", "// gradebook.cpp - Grade Calculator"), line(TARGET, "gradebook.cpp", "// gradebook.cpp - Grade Calculator"),
            intro="In `gradebook.cpp`, update the first line to name this version. Find:"),
    Replace("gradebook.cpp",
            line(BASE, "gradebook.cpp", "Gradebook::Gradebook(const std::string& courseName)"),
            seg(TARGET, "gradebook.cpp", "Gradebook::Gradebook(", "points_.name();") + "}\n",
            intro="In `gradebook.cpp`, find the constructor:"),
    Replace("gradebook.cpp",
            line(BASE, "gradebook.cpp", "sum += s.percentage();"),
            line(TARGET, "gradebook.cpp", "sum += percentageFor(s);"),
            intro="In `classAverage()`, find:"),
    InsertAfter("gradebook.cpp", line(BASE, "gradebook.cpp", 'out << "  " << book.scale()'),
                line(TARGET, "gradebook.cpp", "Grading: "),
                intro="In `operator<<`, find the line that prints the scale:"),
    Replace("gradebook.cpp",
            line(BASE, "gradebook.cpp", "out << s << "),
            seg(TARGET, "gradebook.cpp", "double pct = book.percentageFor(s);", "letterFor(pct)"),
            intro="Further down in `operator<<`, inside the loop, find:"),
    Md("""
- `percentageFor` contains **the single branch**: if the scheme is
  `Weighted`, ask `weighted_`; otherwise ask `points_`. Every grade in the
  program now flows through this one function.
- The class average and every report row now use `percentageFor(s)` instead
  of `s.percentage()`, so they honor the chosen scheme.
- The report row is now written out field by field, because the percentage
  printed must be the *scheme's* percentage, which `Student`'s own
  `operator<<` knows nothing about.
"""),
    Run("Click **Run**. The program should compile cleanly. Because the "
        "scheme defaults to points, it still behaves like v2.6 — except that "
        "the report now shows a `Grading: Points-based` line."),
    Md("""
##### Step 7 — Update the header comment in `main.cpp`
"""),
    Replace(M, seg(BASE, M, "// ====", "// ====", 2), seg(TARGET, M, "// ====", "// ====", 2),
            intro="At the top of `main.cpp`, find the header comment:"),
    Md("""
##### Step 8 — Choose a scheme at startup, and read each assignment's category

`main` now asks for a scheme before the menu starts. If the user picks
weighted grading, it offers to replace the default weights. The *Add student*
loop also asks for a category.
"""),
    DeleteRange(M, "int main() {", "}", last=True,
                intro="Find the start of `main`:",
                end_text="all the way to the final closing `}` at the very end of the file.",
                new=seg(TARGET, M, "int main() {", "return 0;") + "}\n",
                after="In its place, enter the new `main`:"),
    Md("""
What changed, from top to bottom:

- **Choosing the scheme.** The answer is read into a `std::string` named
  `choice`, and a conditional expression turns it into a `Gradebook::Scheme`
  value, which is passed to the `Gradebook` constructor. The scheme is fixed
  for the session.
- **Optional custom weights.** For weighted grading, the user can enter their
  own categories and weights. If they do not total 100, the program prints a
  note — it does not reject them; categories are scaled proportionally.
- **The menu variable is renamed `c`.** The name `choice` is now taken by the
  scheme answer, so the menu choice uses `char c`. Every `if` in the loop
  compares `c`.
- **Add student** asks for a `Category` after the bonus. Pressing Enter with no
  category stores `"Uncategorized"`. The category is passed as the fifth
  constructor argument.
- **Sort** prints `Sorted.`, and **Custom scale** reads each letter into `lt`
  and passes `readNonNegative(...)` straight into the tier — the same steps as
  before, written more compactly.
"""),
    Run("Make sure all eleven files are open and click **Run**. The program "
        "should compile with no errors and no warnings and open with the "
        "scheme question."),
    Md("""
#### Check your work

**Run 1 — points-based.** Answer the scheme question with `1`. Add `Ada` with
two assignments: `Exam 1` (earned `90`, possible `100`, bonus `0`, category
`Exam`) and `HW1` (earned `10`, possible `10`, bonus `0`, category `Homework`).
Type `done`, then choose `2`. The report should include:

```text
  Grading: Points-based
=====================================
1001  Ada                     90.9%   A
```

Check: (90 + 10) ÷ (100 + 10) = 100 ÷ 110 = 90.9%. Choose `5` to quit.

**Run 2 — weighted, default weights.** Run again, choose `2`, and answer `n`
to custom weights. Add the same two assignments for `Ada` and choose `2`:

```text
  Grading: Weighted
=====================================
1001  Ada                     93.8%   A
```

Check: Exam 0.90 × 50 = 45; Homework 1.00 × 30 = 30. Participation has no
work, so its 20 is skipped: 75 ÷ 80 = 93.75%, rounded to 93.8%. **The same
scores, two different grades** — that is the point of choosing a scheme.

**Run 3 — weights that do not total 100.** Run again, choose `2`, answer `y`,
and enter `Exam` `60`, `Homework` `30`, then `done`. You should see:

```text
  Note: weights total 90, not 100. Categories are scaled proportionally.
```

Add the same two assignments for `Ada` and report: she shows `93.3%`
((0.90 × 60 + 1.00 × 30) ÷ 90).

Then confirm:

- [ ] All eleven files build together with no errors and no warnings.
- [ ] `PointsBased` and `Weighted` both inherit `public`ly from
      `GradingScheme`, and neither repeats the cap-and-round code — both call
      `finalize`.
- [ ] `gradescale.h`, `gradescale.cpp`, and `student.cpp` are unchanged from
      Chapter 19.
"""),
    workflow("every file in the project (`main.cpp` and the eight class "
             "files) to open it. You will create two new files during the lab.",
             "Work through Steps 1–8 above in StudySite's internal editor, in "
             "order, clicking **Run** at each ▶ Run checkpoint."),
    save(CHAPTER, TARGET, "all eleven files: `main.cpp`, and the `.h` and `.cpp` "
         "files for `Assignment`, `GradeScale`, `Student`, `Gradebook`, and "
         "`GradingScheme`."),
]
