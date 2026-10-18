# Chapter 22 Lab — Replace Manual Ownership with Smart Pointers

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.2
- **Starting point:** Your committed Chapter 21 v3.1 program (eleven files).

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## What you will build

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

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `gradebook.h`, `gradebook.cpp` | Edit (Steps 2–3) |
| `gradingscheme.h` | Edit — comments only (Step 4) |
| `main.cpp` | Edit (Steps 5–6) |
| All other files | **No change** — keep them open |

## How to use these steps

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

## Build it: step by step

### Step 1 (try it, then undo it) — See why manual ownership is fragile

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

### Step 2 — Own the scheme with `std::unique_ptr` (`gradebook.h`)

In `gradebook.h`, find the first line:

```cpp
// gradebook.h - Grade Calculator v3.1 - Chapter 21
```

Replace it with:

```cpp
// gradebook.h - Grade Calculator v3.2 - Chapter 22
```

Find the standard-library include:

```cpp
#include <iosfwd>
```

Directly below it, add:

```cpp
#include <memory>
```

Inside the class, find the constructor, destructor, deleted copy operations, and `setScheme`:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");
    ~Gradebook();

    // Copying is disabled: Gradebook owns a raw pointer, and a default copy
    // would leave two objects deleting the same scheme. Chapter 22 replaces
    // this restriction with smart-pointer ownership.
    Gradebook(const Gradebook&) = delete;
    Gradebook& operator=(const Gradebook&) = delete;

    /**
     * Installs a grading scheme. The Gradebook takes ownership.
     * Can be called at any time; every grade is recomputed on the next report.
     */
    void setScheme(GradingScheme* scheme);
```

Replace it with:

```cpp
    explicit Gradebook(const std::string& courseName = "Untitled Course");

    // No destructor is needed now. unique_ptr releases the scheme when the
    // Gradebook is destroyed, and again whenever the scheme is replaced.
    // The compiler-generated destructor is correct, so we do not write one.

    /**
     * Installs a grading scheme. Ownership transfers to the Gradebook.
     * The unique_ptr parameter makes that transfer visible at every call site:
     * a caller must std::move into it, so ownership is never ambiguous.
     */
    void setScheme(std::unique_ptr<GradingScheme> scheme);
```

At the bottom of the class, find:

```cpp
    // One pointer to an abstract base. Which concrete scheme it refers to is
    // not this class's concern - that is what polymorphism buys.
    GradingScheme* scheme_ = nullptr;
```

Replace it with:

```cpp
    // An owning smart pointer to an abstract base. Polymorphism is unchanged;
    // only the ownership question is answered differently.
    std::unique_ptr<GradingScheme> scheme_;
```

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

### Step 3 — Simplify the implementation (`gradebook.cpp`)

In `gradebook.cpp`, find the first line:

```cpp
// gradebook.cpp - Grade Calculator v3.1 - Chapter 21
```

Replace it with:

```cpp
// gradebook.cpp - Grade Calculator v3.2 - Chapter 22
```

Find:

```cpp
#include <algorithm>
```

Directly below it, add:

```cpp
#include <memory>
#include <utility>
```

Find the constructor, the destructor, and `setScheme`:

```cpp
Gradebook::Gradebook(const std::string& courseName)
    : courseName_(courseName), scheme_(new PointsBased()) {}

Gradebook::~Gradebook() {
    delete scheme_;
}

void Gradebook::setScheme(GradingScheme* scheme) {
    if (scheme == nullptr || scheme == scheme_) { return; }
    delete scheme_;          // release the previous scheme before replacing it
    scheme_ = scheme;
}
```

Replace it with:

```cpp
Gradebook::Gradebook(const std::string& courseName)
    : courseName_(courseName), scheme_(std::make_unique<PointsBased>()) {}

void Gradebook::setScheme(std::unique_ptr<GradingScheme> scheme) {
    if (!scheme) { return; }
    // Assigning to a unique_ptr destroys whatever it held first. This one line
    // replaces v3.1's manual delete, and the destructor and deleted copy
    // operations that had to accompany it.
    scheme_ = std::move(scheme);
}
```

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

### Step 4 — Update the ownership note (`gradingscheme.h`)

The comment above `class GradingScheme` still describes v3.1's hand-written
ownership. Make it describe the code you now have.

In `gradingscheme.h`, find the first line:

```cpp
// gradingscheme.h - Grade Calculator v3.1 - Chapter 21
```

Replace it with:

```cpp
// gradingscheme.h - Grade Calculator v3.2 - Chapter 22
```

Then find the ownership note in the comment block:

```cpp
 * OWNERSHIP NOTE (revisited in Chapter 22): Gradebook owns a raw pointer.
 * That is correct here, but only because Gradebook also writes a destructor,
 * deletes the old scheme before replacing it, and disables copying. Miss any
 * one of those three and the program leaks or double-frees. Chapter 22 shows
 * how to get the same behavior with none of that hand-written ceremony.
```

Replace it with:

```cpp
 * OWNERSHIP NOTE (Chapter 22): Gradebook owns its scheme through a
 * std::unique_ptr, so a scheme is released automatically when it is replaced
 * and when the Gradebook is destroyed. No hand-written destructor, delete, or
 * deleted copy operations are needed.
```

Comments are part of the code. A comment that describes code that no longer
exists is a defect, even though the compiler never notices it.

### Step 5 — Update the header comment and includes in `main.cpp`

At the top of `main.cpp`, find the header comment:

```cpp
// =============================================================================
//  Grade Calculator  v3.1                                          Chapter 21
// -----------------------------------------------------------------------------
//  Change  : GradingScheme is now abstract with a pure virtual computePercentage
//            and a virtual destructor. Gradebook holds a GradingScheme* and
//            never asks which scheme it has - the v3.0 branch is gone.
//            The scheme can be switched MID-SESSION and every grade recomputes.
//            A third scheme (WeightedDropLowest) was added without changing
//            Gradebook, Student, GradeScale, Assignment, or the report code.
//  Cost    : correct raw-pointer ownership needs three pieces of hand-written
//            bookkeeping in Gradebook - a destructor, a delete inside
//            setScheme, and deleted copy operations. This build has all three
//            and does not leak. Chapter 22 removes the need for any of them.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

Replace it with:

```cpp
// =============================================================================
//  Grade Calculator  v3.2                                          Chapter 22
// -----------------------------------------------------------------------------
//  Change  : Ownership. The raw GradingScheme* becomes std::unique_ptr.
//            Gradebook loses its destructor, its manual delete, and its
//            deleted copy operations - 8 lines of bookkeeping for 0.
//            Behavior is identical to v3.1; both builds are leak-free.
//  Point   : v3.1 is correct because its author remembered three separate
//            things. v3.2 is correct because there is nothing to remember.
//  Verify  : build both with -fsanitize=address, switch schemes, exit.
//            Neither leaks. Then delete Gradebook::~Gradebook from v3.1 and
//            rerun: v3.1 now leaks, v3.2 cannot be broken the same way.
//  Build   : g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp
//            student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
// =============================================================================
```

Below it, find:

```cpp
#include <iostream>
```

Directly below it, add:

```cpp
#include <memory>
#include <utility>
```

### Step 6 — Create schemes with `std::make_unique`

In `chooseScheme`, find the three `setScheme` calls:

```cpp
    if (!c.empty() && c[0] == '2')      { book.setScheme(new Weighted()); }
    else if (!c.empty() && c[0] == '3') { book.setScheme(new WeightedDropLowest()); }
    else                                { book.setScheme(new PointsBased()); }
```

Replace it with:

```cpp
    if (!c.empty() && c[0] == '2') {
        book.setScheme(std::make_unique<Weighted>());
    } else if (!c.empty() && c[0] == '3') {
        book.setScheme(std::make_unique<WeightedDropLowest>());
    } else {
        book.setScheme(std::make_unique<PointsBased>());
    }
```

At the start of `main`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.1 (switchable schemes) ===\n\n";
```

Replace it with:

```cpp
    std::cout << "=== GRADE CALCULATOR v3.2 (leak-free) ===\n\n";
```

`std::make_unique<Weighted>()` returns a temporary `unique_ptr<Weighted>`,
which converts to the `unique_ptr<GradingScheme>` parameter and moves straight
into the `Gradebook`. There is no moment when a raw, unowned pointer exists.

Nothing else in `main` changes.

> **▶ Run checkpoint:** Make sure all eleven files are open and click **Run**. The program should compile with no errors and no warnings and show the `v3.2 (leak-free)` banner.

## Check your work

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

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click all eleven project files to open them.
   Confirm the editor shows the expected file paths before editing.
4. Do the Step 1 experiment and undo it, then work through Steps 2–6 above in StudySite's internal editor, in order, and click **Run** at the ▶ Run checkpoint.
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
> clang++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc
> ./gradecalc
> ```
>
> **Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):
>
> ```powershell
> g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp student.cpp gradingscheme.cpp gradebook.cpp -o gradecalc.exe
> .\gradecalc.exe
> ```

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — all eleven files. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 22 Grade Calculator v3.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 22
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
