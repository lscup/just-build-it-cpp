from engine import *
from common import *

BASE, TARGET, CHAPTER = "v3.0", "v3.1", 21
M = "main.cpp"
GH, GC = "gradingscheme.h", "gradingscheme.cpp"
BH, BC = "gradebook.h", "gradebook.cpp"


def line(ver, f, text):
    return seg(ver, f, text, text)


ITEMS = [
    header("Select Schemes with Polymorphism", "v3.1",
           "Your committed Chapter 20 v3.0 program (eleven files)."),
    Md("""
#### What you will build

In v3.0 the grading scheme was chosen once at startup, and `Gradebook` used
an `if` to decide which scheme's `computePercentage` to call. In this lab you
make the scheme **polymorphic**. By the end you will have:

1. An **abstract** `GradingScheme` base class with a **pure virtual**
   `computePercentage` and a **virtual destructor**.
2. A third scheme, `WeightedDropLowest`, that drops the weakest assignment in
   each category — added **without changing** `Gradebook`, `Student`,
   `GradeScale`, `Assignment`, or the report code.
3. A `Gradebook` that holds a single `GradingScheme*` and calls through it.
   The `if` is gone, and because the `Gradebook` owns that pointer, it manages
   the memory correctly by hand: a destructor, a `delete` before replacing,
   and copying disabled.
4. A `chooseScheme` function and a new menu option, **Change scheme**, so the
   user can switch schemes mid-session and every grade recomputes
   immediately.

#### What is different about v3.1

- **No startup weights prompt.** v3.0 let you type custom category weights
  at startup. v3.1 removes that prompt to keep the focus on polymorphism:
  `Weighted` and `WeightedDropLowest` use the default weights (Exam 50,
  Homework 30, Participation 20). Custom weights come back in Chapter 24.
- **The menu grows to six options**: Add student, Report, Sort, Custom scale,
  **Change scheme** (new), and Quit (now option 6).

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradingscheme.h`, `gradingscheme.cpp` | Edit (Steps 1–2) |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 3–4) |
| `main.cpp` | Edit (Steps 5–7) |
| `assignment.*`, `gradescale.*`, `student.*` | **No change** — keep them open |
"""),
    HOW_TO_READ,
    Md("""
#### Build it: step by step

##### Step 1 — Make `GradingScheme` abstract (`gradingscheme.h`)
"""),
    Replace(GH, line(BASE, GH, "// gradingscheme.h"), line(TARGET, GH, "// gradingscheme.h"),
            intro="In `gradingscheme.h`, find the first line:"),
    Replace(GH, seg(BASE, GH, " * Base class for grading schemes.", "is therefore fixed"),
            seg(TARGET, GH, " * Abstract base class", "hand-written ceremony."),
            intro="Next, inside the comment block above `class GradingScheme`, find these lines:"),
    InsertAfter(GH, line(BASE, GH, "explicit GradingScheme(const std::string& name)"),
                seg(TARGET, GH, "virtual ~GradingScheme()", "= 0;"),
                intro="Inside `class GradingScheme`, find the constructor:"),
    Md("""
These two lines change what kind of class `GradingScheme` is:

- **`= 0`** makes `computePercentage` a **pure virtual function**. The base
  class declares that every scheme *has* a rule but supplies none itself. A
  class with a pure virtual function is **abstract** — you cannot create a
  plain `GradingScheme` object, only objects of derived classes.
- **`virtual`** means that when code calls `computePercentage` through a
  `GradingScheme*`, C++ looks at the object the pointer actually points to and
  runs *that* class's version. This is **dynamic dispatch**.
- The **virtual destructor** matters because `Gradebook` will `delete` a
  scheme through a `GradingScheme*`. Without `virtual`, only the base part of
  the object would be destroyed.

Now mark each derived class's version with `override`.
"""),
    Replace(GH, seg(BASE, GH, 'PointsBased() : GradingScheme("Points-based") {}', "computePercentage"),
            seg(TARGET, GH, 'PointsBased() : GradingScheme("Points-based") {}', "computePercentage"),
            intro="In `class PointsBased`, find:"),
    Replace(GH, seg(BASE, GH, "explicit Weighted(const std::vector<CategoryWeight>& weights);", "computePercentage"),
            seg(TARGET, GH, "explicit Weighted(const std::vector<CategoryWeight>& weights);", "computePercentage"),
            intro="In `class Weighted`, find:"),
    Md("""
`override` asks the compiler to confirm that this function really overrides a
virtual function in the base class. If you misspell the name or get a
parameter wrong, you get a compile error instead of a silent new function.

Finally, let a future derived class reach `Weighted`'s weights, and add the
third scheme.
"""),
    Replace(GH, "private:\n    std::vector<CategoryWeight> weights_;\n};\n",
            lines(TARGET, GH, 68, 84),
            intro="At the bottom of `class Weighted`, find:"),
    Md("""
- `weights_` changes from `private` to **`protected`**, so the derived class
  `WeightedDropLowest` can read the weights directly.
- `class WeightedDropLowest : public Weighted` inherits everything from
  `Weighted` — the weights, `weightTotal()`, `weightsValid()`, even its name —
  and overrides only `computePercentage`.

##### Step 2 — Implement the third scheme (`gradingscheme.cpp`)
"""),
    Replace(GC, line(BASE, GC, "// gradingscheme.cpp"), line(TARGET, GC, "// gradingscheme.cpp"),
            intro="In `gradingscheme.cpp`, find the first line:"),
    Append(GC, seg(TARGET, GC, "WeightedDropLowest::WeightedDropLowest() : Weighted() {}", "return finalize(weightedSum / weightUsed * 100.0);", 1) + "}\n",
           intro="Go to the very end of `gradingscheme.cpp`, after the closing `}` of "
                 "`Weighted::computePercentage`. Leave one blank line and add:"),
    Md("""
- Both constructors pass straight through to `Weighted`'s constructors, so a
  `WeightedDropLowest` starts with the same default weights.
- `computePercentage` follows the same plan as `Weighted`'s, with one extra
  step per category: it collects pointers to that category's assignments,
  finds the one with the lowest `ratio()`, and erases it — but only if the
  category has more than one item.
"""),
    Run("Click **Run**. The program should compile cleanly and behave exactly "
        "like v3.0. `Gradebook` still holds concrete `PointsBased` and "
        "`Weighted` objects, which is allowed — only `GradingScheme` itself is "
        "abstract."),
    Md("""
##### Step 3 — Hold the scheme through a base-class pointer (`gradebook.h`)
"""),
    Replace(BH, line(BASE, BH, "// gradebook.h"), line(TARGET, BH, "// gradebook.h"),
            intro="In `gradebook.h`, find the first line:"),
    Replace(BH, seg(BASE, BH, "/** Which grading rule", "void setWeights("),
            seg(TARGET, BH, 'explicit Gradebook(const std::string& courseName = "Untitled Course");',
                "std::string schemeName() const;"),
            intro="Inside the class, find the scheme enum, the constructor, and the scheme accessors:"),
    Replace(BH, seg(BASE, BH, "// Both schemes are held", "Weighted    weighted_;"),
            seg(TARGET, BH, "// One pointer to an abstract base", "GradingScheme* scheme_ = nullptr;"),
            intro="At the bottom of the class, find:"),
    Md("""
- The `Scheme` enum, the two concrete scheme objects, `weightedScheme()`, and
  `setWeights()` are all gone. `Gradebook` now holds **one pointer to the
  abstract base**, and never needs to know which concrete scheme it points to.
- `setScheme` installs a new scheme. The comment states the ownership rule:
  **the `Gradebook` takes ownership** of the object it is given.
- Owning a raw pointer brings three duties, and the header shows all three:
  1. a **destructor** (`~Gradebook();`) to `delete` the scheme;
  2. `setScheme` must `delete` the old scheme before replacing it (Step 4);
  3. **copying is disabled** with `= delete`. A copied `Gradebook` would
     hold the same pointer as the original, and both would `delete` it.

##### Step 4 — Dispatch through the pointer (`gradebook.cpp`)
"""),
    Replace(BC, line(BASE, BC, "// gradebook.cpp"), line(TARGET, BC, "// gradebook.cpp"),
            intro="In `gradebook.cpp`, find the first line:"),
    Replace(BC, seg(BASE, BC, "Gradebook::Gradebook(const std::string& courseName, Scheme scheme)",
                    "points_.name();") + "}\n",
            seg(TARGET, BC, "Gradebook::Gradebook(const std::string& courseName)",
                "return scheme_->name();") + "}\n",
            intro="Find the constructor, `percentageFor`, and `schemeName`:"),
    Md("""
- The constructor starts every `Gradebook` with a `new PointsBased()`, so
  `scheme_` is never null.
- The destructor deletes the scheme. `setScheme` ignores a null pointer or the
  scheme it already holds, deletes the old scheme, then stores the new one.
- **`percentageFor` has no branch.** `scheme_->computePercentage(...)` runs
  `PointsBased`'s, `Weighted`'s, or `WeightedDropLowest`'s version depending
  on the object `scheme_` points to. The same is true of `schemeName()`.

The rest of `gradebook.cpp` — `classAverage`, `sortByPercentage`, and
`operator<<` — does not change, because it already calls `percentageFor`.

> **Heads-up:** `main.cpp` still uses `Gradebook::Scheme`, which no longer
> exists, so the program will not compile until the end of Step 7.

##### Step 5 — Update the header comment in `main.cpp`
"""),
    Replace(M, seg(BASE, M, "// ====", "// ====", 2), seg(TARGET, M, "// ====", "// ====", 2),
            intro="At the top of `main.cpp`, find the header comment:"),
    Md("""
##### Step 6 — Add `chooseScheme`, the one place that names concrete types
"""),
    InsertBefore(M, "int main() {\n", seg(TARGET, M, "/** Builds the scheme the user asked for.", "Grading is now: ") + "}\n\n",
                 intro="In `main.cpp`, find the first line of `main`:"),
    Md("""
This function still has a branch — but look at what it does. It runs only
when the user makes a choice, and its only job is to **create** the right
object with `new` and hand it to `book.setScheme(...)`, which takes
ownership. Nothing downstream ever asks which scheme it has.

##### Step 7 — Rewrite `main` with a *Change scheme* option
"""),
    DeleteRange(M, "int main() {", "}", last=True,
                intro="Find the start of `main`:",
                end_text="all the way to the final closing `}` at the very end of the file.",
                new=seg(TARGET, M, "int main() {", "return 0;") + "}\n",
                after="In its place, enter the new `main`:"),
    Md("""
- At startup, the `Gradebook` is created first (with its default points
  scheme), and then `chooseScheme(book)` lets the user pick.
- The menu has six options. **Change scheme** (option 5) simply calls
  `chooseScheme(book)` again. Every existing student is regraded under the new
  rule the next time you ask for a report — no data is re-entered.
- **Sort**, **Custom scale**, and **Add student** work exactly as in v3.0.
"""),
    Run("Make sure all eleven files are open and click **Run**. The program "
        "should compile with no errors and no warnings and open by asking you "
        "to select a grading scheme."),
    Md("""
#### Check your work

Run the program and choose `1` (Points-based). Add `Ada` with three
assignments:

| Assignment | Earned | Possible | Bonus | Category |
|---|---|---|---|---|
| `Exam 1` | 90 | 100 | 0 | `Exam` |
| `HW1` | 10 | 10 | 0 | `Homework` |
| `HW2` | 5 | 10 | 0 | `Homework` |

Then report, switch schemes with option `5`, and report again — without
re-entering anything:

1. Choose `2`. You should see `Grading: Points-based` and
   `1001  Ada                     87.5%   B` (105 ÷ 120).
2. Choose `5`, then `2` (Weighted). Choose `2` (Report):
   `Grading: Weighted` and `1001  Ada                     84.4%   B`
   (Exam 0.90 × 50 = 45; Homework 15/20 = 0.75 × 30 = 22.5; 67.5 ÷ 80).
3. Choose `5`, then `3` (Weighted, lowest dropped). Choose `2`:
   `1001  Ada                     93.8%   A`. Dropping HW2 leaves Homework at
   10/10, so (45 + 30) ÷ 80 = 93.75%.
4. Choose `6` (Quit).

Notice that in step 3 the report still says `Grading: Weighted`.
`WeightedDropLowest` inherits its name from `Weighted`'s constructor and does
not set its own — a small reminder that a derived class gets *everything* from
its base unless it overrides it.

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] `Gradebook::percentageFor` contains no `if` — the call goes through
      `scheme_->computePercentage`.
- [ ] `Gradebook` has a destructor that deletes `scheme_`, `setScheme`
      deletes the old scheme before storing the new one, and the copy
      constructor and copy assignment are `= delete`.
- [ ] `assignment.*`, `gradescale.*`, and `student.*` are unchanged from
      Chapter 20.
"""),
    workflow("all eleven project files to open them.",
             "Work through Steps 1–7 above in StudySite's internal editor, in "
             "order, clicking **Run** at each ▶ Run checkpoint."),
    save(CHAPTER, TARGET, "all eleven files."),
]
