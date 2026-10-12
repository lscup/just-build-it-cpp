from engine import *
from common import *

BASE, TARGET, CHAPTER = "v2.4", "v2.5", 18
F = "main.cpp"

old_header = seg(BASE, F, "// ====", "// ====", 2)
new_header = seg(TARGET, F, "// ====", "// ====", 2)
old_includes = seg(BASE, F, "#include <cmath>", "DEFAULT_FILE")
new_includes = seg(TARGET, F, "#include <algorithm>", "CAP_AT_100")
assignment_cls = lines(TARGET, F, 22, 49)
gradescale_cls = lines(TARGET, F, 51, 106)
student_cls = lines(TARGET, F, 108, 147)
new_banner = lines(TARGET, F, 149, 151)
new_main = lines(TARGET, F, 177, 242)

ITEMS = [
    header("Introduce Classes and Invariants", "v2.5",
           "Your committed Chapter 17 v2.4 program (`main.cpp`)."),
    Md("""
#### What you will build

In this lab you rebuild the Grade Calculator's data around **classes** instead
of structs. By the end you will have:

1. An `Assignment` class that holds one graded item — its name, points earned,
   points possible, and bonus — behind `private` data and `const` accessors.
   The old `Score` struct is folded into it.
2. A `GradeScale` class whose constructor **enforces an invariant**: cutoffs
   strictly descend and the lowest tier is 0. Whatever tiers a user types, the
   constructor repairs them into a usable scale, so no other code ever has to
   check.
3. A `Student` class that **owns its own assignments** and computes its own
   percentage with a `percentage()` member that needs no parameters.
4. A smaller, cleaner `main` with four menu options: **Add student**,
   **Report**, **Custom scale**, and **Quit**.

#### What is different about v2.5

v2.5 is a *rebuild*, not an add-on, so a few things from Chapter 17 change on
purpose. Read this before you start so nothing surprises you.

- **Assignments are entered per student.** In v2.4 you added assignments once
  for the whole course, and each student held a list of scores that lined up
  with that list by position. In v2.5 each `Student` owns its own `Assignment`
  objects, so you enter a student's assignments right after the student's
  name. The separate *Add assignment* menu option goes away.
- **The `Gradebook` struct goes away.** `main` holds a `GradeScale`, a
  `std::vector<Student>`, and a next-ID counter directly. (Chapter 19 brings
  back a `Gradebook` — as a real class.)
- **v2.5 starts from a smaller core.** Saving and loading (Chapter 15), the
  regression tests (Chapter 16), and sort and find (Chapter 17) are set aside
  in this checkpoint so you can concentrate on classes. They are not lost:
  your Chapter 17 commit keeps them in your repository's history. Sorting
  returns in Chapter 19, Find by ID in Chapter 23, and saving and loading in
  Chapter 24 — each rebuilt on top of the classes you write today.
- **The grading math does not change.** The same scores still produce the
  same percentage and letter grade.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit. Everything in this lab happens in this one file. |
"""),
    HOW_TO_READ,
    Md("""
> **Heads-up:** Steps 2 through 7 take the program apart before Step 8 puts
> `main` back together, so the program will **not** compile again until the
> end of Step 8. That is expected. Do not try to fix compiler errors in the
> middle — finish the steps in order, then Run.

#### Build it: step by step

##### Step 1 — Update the header comment

Every version of the program opens with a comment block that says what
changed. Update it so the file describes v2.5.
"""),
    Replace(F, old_header, new_header,
            intro="At the very top of `main.cpp`, find the header comment:"),
    Md("""
*Why:* the header is the first thing a reader (including future you) sees. It
should describe the code that is actually in the file.

##### Step 2 — Update the `#include` list and constants

v2.5 no longer reads or writes files, so it no longer needs `<fstream>`,
`<sstream>`, or the `DEFAULT_FILE` constant. It does need `<algorithm>`,
because `Student::percentage()` will call `std::min`.
"""),
    Replace(F, old_includes, new_includes,
            intro="Just below the header comment, find the `#include` lines and the two constants:"),
    Md("""
*Why:* include what you use, and only what you use (Appendix D, Section D.4).
`CAP_AT_100` stays — the course still caps a reported percentage at 100.

##### Step 3 — Replace the structs with an `Assignment` class

Chapter 17's data lived in five structs: `Assignment` (a name and points
possible), `Score` (points earned and bonus), `Student` (which held a list of
`Score`s), `GradeTier`, and `Gradebook`. In v2.5 an assignment belongs to
exactly one student, so it can hold *everything* about itself — and `Score`
is no longer needed.
"""),
    DeleteRange(F, "struct Assignment { std::string name; double pointsPossible = 0.0; };",
                "};",
                intro="Find the first struct, just below `CAP_AT_100`:",
                between="the `Score`, `Student`, `GradeTier`, and `Gradebook` structs",
                new=assignment_cls,
                after="In the space where the five structs were, enter the `Assignment` class:"),
    Md("""
Look at what changed:

- The data members are **`private`** and end in an underscore (`name_`,
  `pointsEarned_`) — the naming convention from Appendix D that marks a member
  variable. Code outside the class can no longer change them directly.
- The **constructor** uses a member initializer list to set all four values
  at once. `bonus` has a default of `0.0`, so a caller can leave it out.
- Every accessor ends in **`const`**, which promises the compiler it does not
  change the object.
- `totalEarned()` and `ratio()` are **behavior that lives with the data**.
  Bonus is added to points earned, never to points possible — the D2 rule from
  Chapter 16, now written once in the class that owns the numbers.

##### Step 4 — Add the `GradeScale` class and its invariant

In v2.4 the scale was a plain `std::vector<GradeTier>`, and nothing stopped
the program from holding a broken one (tiers out of order, no 0 tier). The
`GradeScale` class makes a broken scale impossible to build.
"""),
    InsertBefore(F, "// ---------- input helpers ----------\n", gradescale_cls + "\n",
                 intro="Find the comment line that now sits just below the `Assignment` class:"),
    Md("""
Study the second constructor — it is the heart of this chapter:

- `GradeScale()` with no arguments builds the default A/B/C/D/F scale.
- `explicit GradeScale(const std::vector<Tier>& requested)` walks the tiers
  the user asked for and **keeps only the ones that preserve the invariant**:
  a negative cutoff is skipped, and a cutoff that is not lower than the
  previous kept tier is skipped. If the result does not reach 0, an `F` tier
  at 0 is added.
- Because *every* `GradeScale` passes through one of these constructors, the
  invariant is always true. That is why `letterFor` has no error handling: it
  cannot be handed a bad scale.
- `Tier` is a small struct **nested inside** the class, so its full name is
  `GradeScale::Tier`. It replaces the old `GradeTier` struct.
- `describe()` prints the scale on one line, so `main` does not need to know
  how a scale is stored.

##### Step 5 — Add the `Student` class

A `Student` now owns a `std::vector<Assignment>`. Everything needed to compute
a grade is inside the object.
"""),
    InsertBefore(F, "// ---------- input helpers ----------\n", student_cls + "\n",
                 intro="Find the same comment line again — it is now just below the `GradeScale` class:"),
    Md("""
Compare `percentage()` with Chapter 17's `percentageOf(student, assignments)`.
The old function needed the course-wide assignment list passed in, because a
student only held scores. The new member function takes **no parameters** —
the student has everything it needs. It still applies the same course policy:
skip a zero total to avoid dividing by zero, cap at 100 when `CAP_AT_100` is
`true`, and round to one decimal place.

`addAssignment` is the **only** way to put work into a student, so there is
exactly one place to look if a student's work ever looks wrong.

##### Step 6 — Update the input-helpers banner

Your `readNonNegative` and `readLine` functions do not change. Only the
comment above them changes, to match the banner style of the classes above it.
"""),
    Replace(F, "// ---------- input helpers ----------\n", new_banner,
            intro="Find the comment line:"),
    Md("""
##### Step 7 — Remove the code that v2.5 sets aside

Everything between `readLine` and `main` belonged to the struct-based design:
the CSV helpers and `saveGradebook`/`loadGradebook` (Chapter 15), the free
functions `letterFor`, `percentageOf`, and `printReport`, the regression tests
(Chapter 16), and the sort and search functions (Chapter 17). The classes now
do the grading work, and the other features are set aside for this checkpoint
(see *What is different about v2.5*).
"""),
    DeleteRange(F, "// ---------- CSV helpers ----------", "int main() {",
                intro="Find the line just below the end of `readLine`:",
                between="all the CSV, persistence, grading, test, sorting, and searching code",
                exclusive=True),
    Md("""
When you are done, the closing `}` of `readLine` should be followed by one
blank line and then `int main() {`.

*Why:* in Chapter 17 this code worked on `Student::scores` and the shared
`book.assignments` list. Neither exists any more, so keeping it would only
produce compiler errors. Your Chapter 17 commit still has every line of it if
you want to look back.

##### Step 8 — Rewrite `main` around the new classes

`main` gets simpler: three local variables replace the `Gradebook` struct, and
the menu has four options.
"""),
    DeleteRange(F, "int main() {", "}", last=True,
                intro="Find the start of `main`:",
                end_text="all the way to the final closing `}` at the very end of the file.",
                new=new_main,
                after="In its place, enter the new `main`:"),
    Md("""
Walk through what each part does:

- **Startup.** `GradeScale scale;` builds the default scale — valid by
  construction. `scale.describe()` prints it so the user can see it.
- **Option 1 — Add student.** After reading the name, `Student s(name,
  nextId++)` creates the student with the next ID. The inner loop reads one
  assignment at a time (name, points earned, points possible, bonus) until the
  user types `done` or presses Enter on an empty name, adding each one with
  `s.addAssignment(...)`. Only then is the finished student added to the
  roster.
- **Option 2 — Report.** Each row calls `s.id()`, `s.name()`, and
  `s.percentage()` — accessors, not data members — and
  `scale.letterFor(...)` for the letter.
- **Option 3 — Custom scale.** The loop collects tiers into a
  `std::vector<GradeScale::Tier>` without checking them, then
  `scale = GradeScale(requested);` builds a new scale. **The constructor does
  the repairing** — this code contains no validation at all.
- **Option 4 — Quit** ends the loop. Because there is no file to save in
  v2.5, the program simply says goodbye.
"""),
    Run("Click **Run**. The program should compile with no errors and no "
        "warnings and show the v2.5 banner, the default scale, and the "
        "four-option menu. If you see errors, the message names a line — "
        "compare that area with the code boxes above."),
    Md("""
#### Check your work

Run the program and type the inputs below in the Terminal. Your output should
match.

1. Choose `1` (Add student). Enter the name `Ada`. Add two assignments:
   `HW1` with points earned `9`, points possible `10`, bonus `1`; and
   `Midterm` with `84`, `100`, bonus `5`. Type `done`. The program should
   print `Added Ada as ID 1001.`
2. Choose `2` (Report). You should see:

   ```text
   =====================================
     CLASS REPORT
   =====================================
   1001  Ada                     90.0%   A
   ```

   Check it by hand: (9 + 1 + 84 + 5) ÷ (10 + 100) = 99 ÷ 110 = 90.0%.
3. Choose `3` (Custom scale). Enter `A` with `93`, `B` with `85`, and then
   `ZZZ` with `99`. Type `done`. You should see:

   ```text
     Scale accepted.
     Scale: A >= 93   B >= 85   F >= 0
   ```

   The `ZZZ` tier was dropped because 99 is not below 85, and an `F` tier at
   0 was added because your scale did not reach 0. The constructor repaired
   the input — no error, no crash.
4. Choose `2` again. Ada's 90.0% is now a `B` under the stricter scale. The
   data did not change; only the scale did.
5. Choose `4` (Quit). The program prints `Goodbye.` and ends normally.

Then confirm:

- [ ] The program compiles with no errors **and no warnings**.
- [ ] `Assignment`, `GradeScale`, and `Student` have only `private` data
      members; `main` reaches their data only through member functions.
- [ ] Every accessor that does not change its object is marked `const`.
- [ ] The structs `Score`, `GradeTier`, and `Gradebook` no longer appear
      anywhere in `main.cpp`.
- [ ] The menu shows exactly four options: Add student, Report, Custom scale,
      Quit.
"""),
    workflow("`main.cpp` to open it.",
             "Work through Steps 1–8 above in StudySite's internal editor, in "
             "order. Click **Run** at the ▶ Run checkpoint at the end of Step 8."),
    save(CHAPTER, TARGET, "for this chapter that is just `main.cpp`."),
]
