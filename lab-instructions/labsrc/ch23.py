from engine import *
from common import *

BASE, TARGET, CHAPTER = "v3.2", "v3.3", 23
M = "main.cpp"
BH, BC = "gradebook.h", "gradebook.cpp"


def line(ver, f, text):
    return seg(ver, f, text, text)


ITEMS = [
    header("Add Generic Statistics and an ID Index", "v3.3",
           "Your committed Chapter 22 v3.2 program (eleven files)."),
    Md("""
#### What you will build

In this lab you put the Standard Template Library to work and write a class
template of your own. By the end you will have:

1. **`Statistics<T>`**, a header-only class template that computes count,
   mean, median, lowest, highest, and standard deviation for any numeric type.
2. An **ID index** — a `std::map<int, std::size_t>` from student ID to roster
   position — that `Gradebook` keeps up to date, and a `findById` member that
   uses it.
3. A **letter-grade distribution** counted with a `std::map<char, int>`.
4. `sortByPercentage` rewritten with a **lambda** that states the ordering
   right where the sort happens.
5. Two new menu options: **Statistics** and **Find by ID**. Quit moves to
   option 8.

#### Files in this checkpoint

| File | What you do to it |
|---|---|
| `statistics.h` | Create (Step 1) — a header only; there is no `statistics.cpp` |
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 2–5) |
| `main.cpp` | Edit (Step 6) |
| All other files | **No change** — keep them open |

When you are finished your project has **twelve files**.
"""),
    HOW_TO_READ,
    Md("""
#### Build it: step by step

##### Step 1 — Write the `Statistics<T>` class template
"""),
    Create("statistics.h", sol(TARGET, "statistics.h"),
           intro="Create a new file named `statistics.h` and enter this code:"),
    Md("""
- `template <typename T>` makes `Statistics` a **blueprint**. When you write
  `Statistics<double>`, the compiler generates a version of the class with
  every `T` replaced by `double`.
- The entire template is in the header. The compiler needs the full
  definition at the point where `Statistics<double>` is used, so a class
  template normally has **no `.cpp` file**.
- `T{}` is a value-initialized `T` — `0.0` for a `double` — and is returned
  when there is no data.
- `median()` **copies** the values before sorting, so asking for the median
  does not rearrange the caller's data.
- `std::min_element` and `std::max_element` from `<algorithm>` return
  iterators; the `*` in front reads the value they point to.

##### Step 2 — Declare the new `Gradebook` members (`gradebook.h`)
"""),
    Replace(BH, line(BASE, BH, "// gradebook.h"), line(TARGET, BH, "// gradebook.h"),
            intro="In `gradebook.h`, find the first line:"),
    InsertAfter(BH, "#include <iosfwd>\n", "#include <map>\n",
                intro="Find the standard-library include:"),
    InsertAfter(BH, "    void sortByPercentage();\n",
                lines(TARGET, BH, 51, 59),
                intro="Find the declaration of `sortByPercentage`:"),
    InsertAfter(BH, "    std::vector<Student> roster_;\n", lines(TARGET, BH, 64, 68),
                intro="In the `private:` section, find:"),
    Md("""
- `findById` returns a **pointer** to the student, or `nullptr` if there is no
  such ID. A pointer can say "nothing found"; a reference cannot.
- `letterDistribution` returns a `std::map<char, int>`: each letter grade
  mapped to how many students earned it.
- `printStatistics` writes to whatever `std::ostream` it is given — the
  screen today, a file tomorrow.
- `idIndex_` maps an ID (the **key**) to the student's position in `roster_`
  (the **value**). A `std::map` keeps its keys sorted and finds a key in
  logarithmic time — the job Chapter 17's binary search did, without needing
  a sorted copy of the roster.

##### Step 3 — Keep the index current, and look students up (`gradebook.cpp`)
"""),
    Replace(BC, line(BASE, BC, "// gradebook.cpp"), line(TARGET, BC, "// gradebook.cpp"),
            intro="In `gradebook.cpp`, find the first line:"),
    Replace(BC, '#include "gradebook.h"\n\n#include <algorithm>\n',
            '#include "gradebook.h"\n\n#include "statistics.h"\n\n#include <algorithm>\n#include <map>\n',
            intro="Find the first includes:"),
    Replace(BC, seg(BASE, BC, "void Gradebook::addStudent(const Student& s) {", "}"),
            seg(TARGET, BC, "void Gradebook::addStudent(const Student& s) {", "return &roster_[it->second];") + "}\n",
            intro="Find `addStudent`:"),
    Md("""
- In `addStudent`, the new student was just pushed onto the end of the
  roster, so its position is `roster_.size() - 1`. That position is stored in
  the index under the student's ID.
- `idIndex_.find(id)` returns an **iterator**. If it equals `idIndex_.end()`,
  the ID is not in the map. Otherwise `it->second` is the stored position.
  `auto` lets the compiler spell out the long iterator type for you.
"""),
    Run("Open `statistics.h` along with the other files and click **Run**. The "
        "program should compile cleanly and behave exactly like v3.2. "
        "`letterDistribution` and `printStatistics` are declared but not yet "
        "defined; that is allowed as long as nothing calls them, and nothing "
        "does yet."),
    Md("""
##### Step 4 — Count letter grades and compute statistics (`gradebook.cpp`)
"""),
    InsertAfter(BC, "    return &roster_[it->second];\n}\n",
                "\n" + seg(TARGET, BC, "std::map<char, int> Gradebook::letterDistribution() const {",
                           'out << "\\n";') + "}\n",
                intro="Directly below the `findById` function you just added — after this code:"),
    Md("""
(The first line in the box is blank on purpose: leave one blank line between
`findById` and the new code.)

- `++counts[letter]` is the standard **counting idiom** for a map. If `letter`
  is not in the map yet, `operator[]` inserts it with the value `0`, and `++`
  makes it `1`. Because a `std::map` is sorted by key, the counts come back in
  letter order.
- `printStatistics` fills a `Statistics<double>` with every student's course
  percentage, then prints the results. It uses `percentageFor`, so the
  statistics follow the chosen grading scheme.
- `for (const auto& entry : letterDistribution())` walks the map;
  `entry.first` is the letter and `entry.second` is the count.

##### Step 5 — Sort with a lambda, and rebuild the index (`gradebook.cpp`)
"""),
    Replace(BC, line(BASE, BC, "std::sort(roster_.begin(), roster_.end());"),
            seg(TARGET, BC, "// A lambda states the ordering", "idIndex_[roster_[i].id()] = i;") + "    }\n",
            intro="In `sortByPercentage`, find:"),
    Md("""
- The **lambda** `[self](const Student& a, const Student& b) { ... }` is the
  comparison, written right where it is used. You no longer have to go read
  `Student::operator<` to find out what order the sort produces.
- The lambda needs `percentageFor`, a `Gradebook` member, so it **captures** a
  pointer to the gradebook, `self`, by listing it in the square brackets.
- **An index is derived data, and derived data goes stale.** Sorting moves
  every student to a new position, so every position stored in `idIndex_` is
  now wrong. The loop clears the index and rebuilds it from the sorted roster.
  Forget this, and *Find by ID* silently returns the wrong student.

##### Step 6 — Add *Statistics* and *Find by ID* to the menu (`main.cpp`)
"""),
    Replace(M, seg(BASE, M, "//  Grade Calculator  v3.2", "rerun: v3.1 now leaks"),
            seg(TARGET, M, "//  Grade Calculator  v3.3", "Sorting is expressed with a lambda"),
            intro="At the top of `main.cpp`, find these lines of the header comment:"),
    Replace(M, line(BASE, M, "=== GRADE CALCULATOR v3.2"), line(TARGET, M, "=== GRADE CALCULATOR v3.3"),
            intro="At the start of `main`, find the banner line:"),
    Replace(M, seg(BASE, M, 'std::cout << "\\n1) Add student', "6) Quit"),
            seg(TARGET, M, 'std::cout << "\\n1) Add student', "8) Quit"),
            intro="Find the menu prompt:"),
    Replace(M, seg(BASE, M, "} else if (c == '6') {", "Please enter 1-6."),
            seg(TARGET, M, "} else if (c == '6') {", "Please enter 1-8."),
            intro="Near the end of the menu loop, find:"),
    Md("""
- **Statistics** (option 6) passes `std::cout` to `printStatistics`.
- **Find by ID** (option 7) converts the typed ID with `std::stoi`, catching
  bad input, then asks `book.findById(id)`. Always compare the result with
  `nullptr` before using it — dereferencing a null pointer crashes the
  program.
- **Quit** moves to option 8.
"""),
    Run("Make sure all twelve files are open and click **Run**. The program "
        "should compile with no errors and no warnings and show the "
        "eight-option menu."),
    Md("""
#### Check your work

Choose `1` (Points-based). Add three students, each with one assignment
(category: press Enter):

| Student | Assignment | Earned | Possible | Bonus |
|---|---|---|---|---|
| `Ana` | `Test` | 95 | 100 | 0 |
| `Ben` | `Test` | 75 | 100 | 0 |
| `Cy` | `Test` | 55 | 100 | 0 |

1. Choose `6` (Statistics). You should see:

   ```text
   --- Class statistics ---
     Students : 3
     Mean     : 75.0%
     Median   : 75.0%
     Range    : 55.0% to 95.0%
     Std dev  : 16.3
     Grades   : A=1  C=1  F=1
   ```

   Check the standard deviation by hand: the deviations from the mean are
   +20, 0, −20; their squares average 800 ÷ 3 ≈ 266.67; √266.67 ≈ 16.3.
2. Choose `7` and enter `1002`. You should see `Ben: 75.0%`.
3. Choose `7` and enter `99`. You should see `No student with ID 99.`
4. Choose `3` (Sort), then `7` with `1002` again. It must still find `Ben` —
   proof that the index was rebuilt after sorting.
5. Choose `8` (Quit).

Then confirm:

- [ ] The program compiles with no errors and no warnings.
- [ ] `statistics.h` has an include guard and there is no `statistics.cpp`.
- [ ] `addStudent` updates `idIndex_`, and `sortByPercentage` rebuilds it.
- [ ] Every use of `findById` checks for `nullptr`.
"""),
    workflow("all eleven project files to open them. You will create "
             "`statistics.h` during the lab.",
             "Work through Steps 1–6 above in StudySite's internal editor, in "
             "order, clicking **Run** at each ▶ Run checkpoint."),
    save(CHAPTER, TARGET, "all twelve files, including the new `statistics.h`."),
]
