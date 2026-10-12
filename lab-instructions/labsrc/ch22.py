from engine import *
from common import *

BASE, TARGET, CHAPTER = "v3.1", "v3.2", 22
M = "main.cpp"
BH, BC = "gradebook.h", "gradebook.cpp"


def line(ver, f, text):
    return seg(ver, f, text, text)


ITEMS = [
    header("Replace Manual Ownership with Smart Pointers", "v3.2",
           "Your committed Chapter 21 v3.1 program (eleven files)."),
    Md("""
#### What you will build

v3.1 is correct: its `Gradebook` owns a raw `GradingScheme*` and does three
separate things by hand to avoid leaks and double deletes — a destructor, a
`delete` inside `setScheme`, and deleted copy operations. In this lab you
replace that hand-written bookkeeping with **`std::unique_ptr`**. By the end:

1. `Gradebook` holds a `std::unique_ptr<GradingScheme>`.
2. `Gradebook` has **no destructor**, **no `delete`**, and **no deleted copy
   operations** — `unique_ptr` handles all of it.
3. `setScheme` takes a `std::unique_ptr<GradingScheme>`, so every caller must
   visibly hand over ownership.
4. `chooseScheme` creates schemes with **`std::make_unique`** instead of
   `new`.

The program's **behavior does not change at all** — same menu, same grades.
What changes is that its correctness no longer depends on anyone remembering
three things.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 2–3) |
| `gradingscheme.h` | Edit — comments only (Step 4) |
| `main.cpp` | Edit (Steps 5–6) |
| All other files | **No change** — keep them open |
"""),
    HOW_TO_READ,
    Md("""
#### Build it: step by step

##### Step 1 (try it, then undo it) — See why manual ownership is fragile

Before you change anything, see how easy it is to break v3.1.

1. In `gradebook.cpp`, find this line inside `Gradebook::setScheme`:

   ```cpp
       delete scheme_;          // release the previous scheme before replacing it
   ```

2. Turn it into a comment by typing `//` at the start of the line.
3. Click **Run**. Choose a scheme, then use **Change scheme** (option 5) two or
   three times, report, and quit.

The program still prints correct grades and exits normally. But every scheme
you replaced was never deleted — the program **leaked** that memory. Nothing
in the output tells you, which is why leaks are called *silent*.

> **Note — this is the one check StudySite's Run cannot make for you.** A leak
> is invisible from the program's output. If you have a local C++ toolchain,
> build the program with `-fsanitize=address -g` and repeat the experiment:
> AddressSanitizer reports the leaked allocations when the program exits.
> Otherwise, ask your instructor which memory check to use.

4. **Remove the `//` you added** so the line is restored exactly as it was.
   Steps 2–6 assume the original v3.1 code.

##### Step 2 — Own the scheme with `std::unique_ptr` (`gradebook.h`)
"""),
    Replace(BH, line(BASE, BH, "// gradebook.h"), line(TARGET, BH, "// gradebook.h"),
            intro="In `gradebook.h`, find the first line:"),
    InsertAfter(BH, "#include <iosfwd>\n", "#include <memory>\n",
                intro="Find the standard-library include:"),
    Replace(BH, seg(BASE, BH, "explicit Gradebook(", "void setScheme(GradingScheme* scheme);"),
            seg(TARGET, BH, "explicit Gradebook(", "void setScheme(std::unique_ptr<GradingScheme> scheme);"),
            intro="Inside the class, find the constructor, destructor, deleted copy operations, and `setScheme`:"),
    Replace(BH, seg(BASE, BH, "// One pointer to an abstract base.", "GradingScheme* scheme_ = nullptr;"),
            seg(TARGET, BH, "// An owning smart pointer", "std::unique_ptr<GradingScheme> scheme_;"),
            intro="At the bottom of the class, find:"),
    Md("""
- **`std::unique_ptr<GradingScheme>`** is an *owning* pointer from
  `<memory>`. When the `unique_ptr` is destroyed or given a new object, it
  deletes the object it held. So the `Gradebook`'s compiler-generated
  destructor is now correct — you do not write one.
- A `unique_ptr` **cannot be copied**, only moved. That makes `Gradebook`
  non-copyable automatically, so the two `= delete` lines are no longer needed.
- `setScheme` now takes its parameter **by value as a `unique_ptr`**. A caller
  cannot pass one without giving up ownership, so who owns the scheme is
  never in doubt.
- **The polymorphism is untouched.** `scheme_` still points to the abstract
  base, and calls through it still dispatch to the right scheme.

##### Step 3 — Simplify the implementation (`gradebook.cpp`)
"""),
    Replace(BC, line(BASE, BC, "// gradebook.cpp"), line(TARGET, BC, "// gradebook.cpp"),
            intro="In `gradebook.cpp`, find the first line:"),
    InsertAfter(BC, "#include <algorithm>\n", "#include <memory>\n#include <utility>\n",
                intro="Find:"),
    Replace(BC, seg(BASE, BC, "Gradebook::Gradebook(const std::string& courseName)", "scheme_ = scheme;") + "}\n",
            seg(TARGET, BC, "Gradebook::Gradebook(const std::string& courseName)", "scheme_ = std::move(scheme);") + "}\n",
            intro="Find the constructor, the destructor, and `setScheme`:"),
    Md("""
- `std::make_unique<PointsBased>()` creates the starting scheme and wraps it in
  a `unique_ptr` in one step — no `new` appears anywhere.
- The destructor is **gone**.
- In `setScheme`, `scheme_ = std::move(scheme);` transfers ownership from the
  parameter into the member. Assigning to a `unique_ptr` **first deletes
  whatever it held**, so this one line replaces v3.1's manual `delete`.
  `std::move` (from `<utility>`) is required because a `unique_ptr` cannot be
  copied.

> **Heads-up:** `main.cpp` still calls `setScheme(new ...)`, and a raw pointer
> does not convert to a `unique_ptr` automatically. The program will not
> compile until the end of Step 6.

##### Step 4 — Update the ownership note (`gradingscheme.h`)

The comment above `class GradingScheme` still describes v3.1's hand-written
ownership. Make it describe the code you now have.
"""),
    Replace("gradingscheme.h", line(BASE, "gradingscheme.h", "// gradingscheme.h"),
            line(TARGET, "gradingscheme.h", "// gradingscheme.h"),
            intro="In `gradingscheme.h`, find the first line:"),
    Replace("gradingscheme.h", seg(BASE, "gradingscheme.h", " * OWNERSHIP NOTE", "hand-written ceremony."),
            seg(TARGET, "gradingscheme.h", " * OWNERSHIP NOTE", "deleted copy operations are needed."),
            intro="Then find the ownership note in the comment block:"),
    Md("""
Comments are part of the code. A comment that describes code that no longer
exists is a defect, even though the compiler never notices it.

##### Step 5 — Update the header comment and includes in `main.cpp`
"""),
    Replace(M, seg(BASE, M, "// ====", "// ====", 2), seg(TARGET, M, "// ====", "// ====", 2),
            intro="At the top of `main.cpp`, find the header comment:"),
    InsertAfter(M, "#include <iostream>\n", "#include <memory>\n#include <utility>\n",
                intro="Below it, find:"),
    Md("""
##### Step 6 — Create schemes with `std::make_unique`
"""),
    Replace(M, seg(BASE, M, "if (!c.empty() && c[0] == '2')", "else                                {"),
            seg(TARGET, M, "if (!c.empty() && c[0] == '2') {", "book.setScheme(std::make_unique<PointsBased>());") + "    }\n",
            intro="In `chooseScheme`, find the three `setScheme` calls:"),
    Replace(M, line(BASE, M, "=== GRADE CALCULATOR v3.1"), line(TARGET, M, "=== GRADE CALCULATOR v3.2"),
            intro="At the start of `main`, find the banner line:"),
    Md("""
`std::make_unique<Weighted>()` returns a temporary `unique_ptr<Weighted>`,
which converts to the `unique_ptr<GradingScheme>` parameter and moves straight
into the `Gradebook`. There is no moment when a raw, unowned pointer exists.

Nothing else in `main` changes.
"""),
    Run("Make sure all eleven files are open and click **Run**. The program "
        "should compile with no errors and no warnings and show the "
        "`v3.2 (leak-free)` banner."),
    Md("""
#### Check your work

Repeat the Chapter 21 test — it must produce **exactly the same results**.
Choose `1` (Points-based) and add `Ada` with `Exam 1` (90/100, bonus 0,
`Exam`), `HW1` (10/10, bonus 0, `Homework`), and `HW2` (5/10, bonus 0,
`Homework`). Report after each scheme:

| Scheme (option 5, then) | Report line |
|---|---|
| `1` Points-based | `1001  Ada                     87.5%   B` |
| `2` Weighted | `1001  Ada                     84.4%   B` |
| `3` Weighted, lowest dropped | `1001  Ada                     93.8%   A` |

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] Searching your project for `delete` and for `new ` finds nothing in
      `gradebook.cpp` or `main.cpp`.
- [ ] `Gradebook` declares no destructor and no `= delete` copy operations.
- [ ] Switching schemes several times and quitting works normally. (If you
      have a local toolchain, an AddressSanitizer build reports no leaks.)

| | v3.1 | v3.2 |
|---|---|---|
| Destructor | hand-written | **not needed** |
| `delete` in `setScheme` | required | **not needed** |
| Deleted copy operations | required | **not needed** |
| Behavior | identical | identical |
"""),
    workflow("all eleven project files to open them.",
             "Do the Step 1 experiment and undo it, then work through Steps 2–6 "
             "above in StudySite's internal editor, in order, and click **Run** "
             "at the ▶ Run checkpoint."),
    save(CHAPTER, TARGET, "all eleven files."),
]
