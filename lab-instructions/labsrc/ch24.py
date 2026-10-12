from engine import *
from common import *

BASE, TARGET, CHAPTER = "v3.3", "v4.0", 24
M = "main.cpp"
SH, SC = "gradescale.h", "gradescale.cpp"
GH, GC = "gradingscheme.h", "gradingscheme.cpp"
BH = "gradebook.h"


def line(ver, f, text):
    return seg(ver, f, text, text)


ITEMS = [
    header("Add Release-Safe Error Handling", "v4.0",
           "Your committed Chapter 23 v3.3 program (twelve files)."),
    Md("""
#### What you will build

This is the release checkpoint. Until now, bad input was either quietly
repaired (an invalid grade scale) or quietly accepted (weights that do not
total 100). In this lab you make the program **refuse bad input with an
exception, explain why, and carry on**. By the end you will have:

1. An **exception hierarchy** in `gradebookerror.h`: a `GradebookError` base
   class derived from `std::runtime_error`, and three specific errors —
   `InvalidScaleError`, `WeightSumError`, and `FileFormatError`.
2. A `GradeScale` constructor that **throws** `InvalidScaleError` instead of
   repairing the tiers.
3. A `Weighted` constructor that **throws** `WeightSumError` when the
   weights do not total 100.
4. **Saving and loading** the gradebook to `gradebook.csv`: loaded at
   startup, saved from a new **Save** option, and saved again on Quit. A
   malformed file produces a `FileFormatError` that names the file and line.
5. `try`/`catch` blocks in `main` that report each error and keep the program
   running, plus the return of **custom category weights** when choosing a
   weighted scheme.

The menu grows to nine options: Add student, Report, Sort, **Edit scale**
(renamed), Change scheme, Statistics, Find by ID, **Save** (new), and Quit.

> **Scope:** Complete only the Chapter 24 code checkpoint here. Final-project
> documentation, finishing touches, and submission instructions will be
> provided separately.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradebookerror.h` | Create (Step 1) |
| `gradescale.h`, `gradescale.cpp` | Edit (Step 2) |
| `gradingscheme.h`, `gradingscheme.cpp` | Edit (Step 3) |
| `gradebook.h`, `gradebook.cpp` | Edit (Step 4) |
| `main.cpp` | Edit (Steps 5–10) |
| `assignment.*`, `student.*`, `statistics.h` | **No change** — keep them open |

When you are finished your project has **thirteen files**.
"""),
    HOW_TO_READ,
    Md("""
#### Build it: step by step

##### Step 1 — Write the exception hierarchy
"""),
    Create("gradebookerror.h", sol(TARGET, "gradebookerror.h"),
           intro="Create a new file named `gradebookerror.h` and enter this code:"),
    Md("""
- `GradebookError` **inherits from `std::runtime_error`**, so every error this
  program throws can be caught as a `GradebookError`, or more generally as a
  `std::exception`. The message passed to the constructor is what `what()`
  returns later.
- Each derived class adds a prefix or builds a more specific message.
  `WeightSumError` formats the actual total into its message and also keeps it
  in `actual()`. `FileFormatError` records the file name and line number.
- A thrown exception carries **data**, not just a message, so the code that
  catches it can decide what to do.

##### Step 2 — Make `GradeScale` refuse instead of repair
"""),
    Replace(SH, line(BASE, SH, "// gradescale.h"), line(TARGET, SH, "// gradescale.h"),
            intro="In `gradescale.h`, find the first line:"),
    Replace(SH, seg(BASE, SH, "    GradeScale();", "explicit GradeScale("),
            seg(TARGET, SH, "    GradeScale();", "explicit GradeScale("),
            intro="Inside the class, find the two constructor declarations:"),
    Replace(SC, seg(BASE, SC, "// gradescale.cpp", "#include <ostream>"),
            seg(TARGET, SC, "// gradescale.cpp", "#include <ostream>"),
            intro="In `gradescale.cpp`, find the first lines of the file:"),
    DeleteRange(SC, "GradeScale::GradeScale(const std::vector<Tier>& requested) {", "}",
                intro="Find the start of the constructor that takes tiers:",
                between="the body of that constructor",
                new=seg(TARGET, SC, "GradeScale::GradeScale(const std::vector<Tier>& requested) {",
                        "every percentage maps to a letter.") + "    }\n}\n",
                after="In its place, enter:"),
    Md("""
**The invariant did not change** — cutoffs still strictly descend and the
lowest tier is still 0. Only the response to a violation changed: instead of
skipping or patching a bad tier, the constructor **throws**. A constructor
that throws never finishes, so **no half-built `GradeScale` can exist**.

The doc comment in the header now says `@throws InvalidScaleError`, so anyone
calling the constructor knows to be ready for it.
"""),
    Run("Click **Run** with every file open, including `gradebookerror.h`. The "
        "program should compile cleanly. Do **not** test *Custom scale* yet — "
        "nothing catches the new exception until Step 9, so a bad scale would "
        "end the program."),
    Md("""
##### Step 3 — Make `Weighted` refuse weights that do not total 100
"""),
    Replace(GH, line(BASE, GH, "// gradingscheme.h"), line(TARGET, GH, "// gradingscheme.h"),
            intro="In `gradingscheme.h`, find the first line:"),
    Replace(GH, seg(BASE, GH, "    Weighted();", "explicit Weighted("),
            seg(TARGET, GH, "    Weighted();", "explicit Weighted("),
            intro="In `class Weighted`, find the two constructor declarations:"),
    Replace(GC, seg(BASE, GC, "// gradingscheme.cpp", '#include "gradingscheme.h"'),
            seg(TARGET, GC, "// gradingscheme.cpp", '#include "gradebookerror.h"'),
            intro="In `gradingscheme.cpp`, find the first two lines:"),
    Replace(GC, seg(BASE, GC, "Weighted::Weighted(const std::vector<CategoryWeight>& weights)", "weights_(weights) {}"),
            seg(TARGET, GC, "Weighted::Weighted(const std::vector<CategoryWeight>& weights)", "throw WeightSumError") + "    }\n}\n",
            intro="Find the `Weighted` constructor that takes weights:"),
    Md("""
In v3.0 weights that did not total 100 were scaled proportionally, with only
a note. Now the constructor uses its own `weightsValid()` check and throws a
`WeightSumError` carrying the actual total.

`WeightedDropLowest`'s weights-taking constructor calls this constructor, so
it gets the same check **for free** — you do not change `WeightedDropLowest`
at all.

##### Step 4 — Let a `Gradebook` be moved, and keep IDs unique

Loading a file will build a complete new `Gradebook` and then move it into
place. A `Gradebook` cannot be copied (it holds a `unique_ptr`), but it can be
**moved**.
"""),
    Replace(BH, line(BASE, BH, "// gradebook.h"), line(TARGET, BH, "// gradebook.h"),
            intro="In `gradebook.h`, find the first line:"),
    Replace(BH, lines(BASE, BH, 18, 20), lines(TARGET, BH, 18, 25),
            intro="Find the constructor and the comment below it:"),
    Md("""
`= default` asks the compiler to generate the move constructor and move
assignment operator. Each member is moved in turn — including the
`unique_ptr`, which hands over its scheme.

There is one more thing to fix before students can be loaded from a file. A
loaded student keeps the ID it was saved with, but the `Gradebook`'s next-ID
counter starts at 1001 every time the program runs. Without a fix, the first
student you add after a reload would get an ID that is already taken.
"""),
    Replace("gradebook.cpp", line(BASE, "gradebook.cpp", "// gradebook.cpp"),
            line(TARGET, "gradebook.cpp", "// gradebook.cpp"),
            intro="In `gradebook.cpp`, find the first line:"),
    InsertAfter("gradebook.cpp", seg(BASE, "gradebook.cpp", "roster_.push_back(s);", "idIndex_[s.id()] = roster_.size() - 1;"),
                seg(TARGET, "gradebook.cpp", "// A student loaded from a file", "nextId_ = s.id() + 1;"),
                intro="In `addStudent`, find:"),
    Md("""
`addStudent` is the one place every student enters the roster — typed in or
loaded — so this is the one place the counter has to be kept ahead of the
IDs already in use. **A class protects its own invariants**; here the
invariant is "every ID handed out is unused."

##### Step 5 — Update the header comment and includes in `main.cpp`
"""),
    Replace(M, seg(BASE, M, "// ====", "// ====", 2), seg(TARGET, M, "// ====", "// ====", 2),
            intro="At the top of `main.cpp`, find the header comment:"),
    Replace(M, seg(BASE, M, '#include "gradebook.h"', "#include <string>"),
            seg(TARGET, M, '#include "gradebook.h"', "DEFAULT_FILE"),
            intro="Below it, find the includes:"),
    Md("""
`<fstream>` and `<sstream>` are back for file input and output, and
`DEFAULT_FILE` names the file the gradebook is saved to.

##### Step 6 — Add `splitCsv` and `saveGradebook`
"""),
    InsertBefore(M, "/** Builds the scheme the user asked for. The only place that names the\n",
                 lines(TARGET, M, 54, 87) + "\n",
                 intro="Find the comment just above `chooseScheme` (below `readLine`):"),
    Md("""
- `splitCsv` is the same helper you wrote in Chapter 15.
- The file format is **version 2**: `TIER` lines for the scale, then a
  `STUDENT` line for each student, followed by one `WORK` line per assignment
  — including its **category**.
- `saveGradebook` returns nothing. If the file cannot be opened, or the
  writing fails partway through, it **throws** a `GradebookError` instead of
  returning `false` for a caller to forget to check.

##### Step 7 — Add `loadGradebook`, which builds a replacement first
"""),
    InsertBefore(M, "/** Builds the scheme the user asked for. The only place that names the\n",
                 lines(TARGET, M, 89, 157) + "\n",
                 intro="Find the same comment line again — it is now just below `saveGradebook`:"),
    Md("""
Read this function in two halves.

**Reading.** Every line is parsed into local variables — `tiers` and
`loaded` — never directly into `book`. Inside the loop:

- A record with too few fields, a `WORK` line for an unknown student, or an
  unrecognized record type throws a `FileFormatError` naming the line.
- `std::stod` and `std::stoi` throw `std::invalid_argument` on text that is
  not a number, and `std::out_of_range` on a number too large. The `catch`
  blocks **translate** those library exceptions into a `FileFormatError` that
  names the file and line the user can actually fix.

**Committing.** Only after the whole file has been read does the function
build a `fresh` gradebook, set its scale (which may throw
`InvalidScaleError`), add the students, and finally
`book = std::move(fresh);`. If anything throws before that last line, `book`
is **untouched** — the load either succeeds completely or changes nothing.
That is what the move operations from Step 4 make possible.

The `// ----` line at the end separates the persistence section from the
menu helpers below it.
"""),
    Run("Click **Run**. The program should compile cleanly; the new functions "
        "exist but are not called yet."),
    Md("""
##### Step 8 — Rewrite `chooseScheme` to accept custom weights safely
"""),
    DeleteRange(M, "/** Builds the scheme the user asked for. The only place that names the", "}",
                intro="Find the comment above `chooseScheme`:",
                between="the whole `chooseScheme` function",
                new=lines(TARGET, M, 159, 191),
                after="In its place, enter:"),
    Md("""
- Points-based grading is chosen as before.
- For either weighted scheme, the user may now enter their own categories
  and weights. If they enter none, the default weights are used.
- Creating the scheme sits inside a `try` block. If the weights do not total
  100, the `Weighted` constructor throws, the `catch` prints the error's
  message, and the function **returns early** — `setScheme` was never reached,
  so the previous scheme is still in effect.

##### Step 9 — Add `editScale`
"""),
    InsertBefore(M, "int main() {\n", lines(TARGET, M, 193, 209) + "\n",
                 intro="Find the first line of `main`:"),
    Md("""
This is the *Custom scale* code from `main`, moved into its own function and
protected by `try`/`catch`. Look at the comment in the `catch` block: because
`GradeScale(requested)` throws **before** `book.setScale(...)` runs, the old
scale is never replaced. The user sees why the scale was refused and keeps
the scale they had.

##### Step 10 — Rewrite `main`: load, catch, save
"""),
    DeleteRange(M, "int main() {", "}", last=True,
                intro="Find the start of `main`:",
                end_text="all the way to the final closing `}` at the very end of the file.",
                new=lines(TARGET, M, 211, 301),
                after="In its place, enter the new `main`:"),
    Md("""
- **Startup** tries to load `gradebook.csv`. If there is no file, or it is
  malformed, the error is printed and a new gradebook starts.
- **The whole menu body is inside one `try` block.** Any `GradebookError`
  raised by an option is caught at the bottom of the loop, its message is
  printed, and the loop continues. The `catch` names `GradebookError`, so it
  handles all three specific errors.
- **Edit scale** (option 4) calls `editScale`, and **Change scheme**
  (option 5) calls the new `chooseScheme`.
- **Save** (option 8) is new. **Quit** moves to option 9.
- **On exit** the gradebook is saved. If that fails, the program says so and
  returns `1` — a nonzero exit code tells the operating system something went
  wrong.
"""),
    Run("Make sure all thirteen files are open and click **Run**. The program "
        "should compile with no errors and no warnings. On the first run it "
        "prints `No file named 'gradebook.csv' was found.` and `Starting a new "
        "gradebook.` — that is correct."),
    Md("""
#### Check your work

Work through this test plan in the Terminal. A release is a claim that you
tested the whole program, not only the cases you happened to try while typing.

1. **Fresh start.** Choose `1` (Points-based). Add `Ada` with one assignment:
   `HW1`, earned `9`, possible `10`, bonus `0`, category Enter. Report with
   `2`: `1001  Ada                     90.0%   A`.
2. **An invalid scale is refused.** Choose `4` (Edit scale). Enter `A` with
   `80`, then `B` with `85`, then `done`. You should see:

   ```text
     Invalid grade scale: tier 'B' at 85 is not below the previous tier at 80.
     Your previous scale is still in effect.
   ```

   Report again: Ada is still an `A` under the default scale.
3. **A scale that does not reach 0 is refused.** Choose `4` and enter only `A`
   with `90`, then `done`. You should see a message that the lowest tier must
   have a cutoff of 0, and the previous scale stays in effect.
4. **Bad weights are refused.** Choose `5`, then `2`, answer `y`, and enter
   `Exam` `50` and `Homework` `30`, then `done`. You should see:

   ```text
     Category weights total 80.0 percent; they must total 100.
     The grading scheme was not changed.
   ```

5. **Save and reload.** Choose `8`. You should see
   `Saved to gradebook.csv.` Then choose `9` to quit; the program prints
   `Gradebook saved. Goodbye.` Click **Run** again: the program should print
   `Loaded gradebook.csv (1 students).` Choose a scheme, then report — Ada is
   back with 90.0%. Now add a new student, `Bo`, with no assignments
   (type `done` right away). The program should print `Added Bo as ID 1002.`
   — not 1001, which Ada already has.

Then confirm:

- [ ] All thirteen files build together with no errors and no warnings.
- [ ] No input you can type makes the program crash or stop unexpectedly.
- [ ] Every `throw` in the program throws a class derived from
      `GradebookError`, and every `catch` catches by **`const` reference**.
- [ ] `assignment.*`, `student.*`, and `statistics.h` are unchanged from
      Chapter 23.
"""),
    workflow("all twelve project files to open them. You will create "
             "`gradebookerror.h` during the lab.",
             "Work through Steps 1–10 above in StudySite's internal editor, in "
             "order, clicking **Run** at each ▶ Run checkpoint."),
    save(CHAPTER, TARGET, "all thirteen files, including the new `gradebookerror.h`. "
         "You do not need to commit `gradebook.csv`."),
]
