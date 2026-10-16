# Chapter 03 Lab — Store an Assignment

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.2
- **Starting point:** Your committed Chapter 2 v0.1 program (one file, prints a banner).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Chapter 2's program could only talk. This one listens. You replace the fixed
banner with four prompts, store what the user types in **variables of the
right type**, and echo it back as a formatted summary. The two ideas that
matter here are choosing a type that fits the data, and knowing which input
function to use for which kind of value. By the end you will have:

1. A shorter one-line banner, so the program's output is dominated by its
   work rather than its decoration.
2. Two `std::string` variables read with `std::getline`, because names
   contain spaces.
3. Two `double` variables read with `std::cin >>`, because scores need
   partial credit.
4. A `--- Summary ---` block that echoes all four values with aligned
   labels.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-5) |

When you are finished your project still has **one** `.cpp` file.

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

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select **COSC1436xxx-Grade-Calculator-YourLastName**, and click `main.cpp`.
   Confirm the editor shows the expected file paths before editing.
4. Continue the existing program in StudySite's internal editor, finish the steps in order, then Run.
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Step 1 — Update the comment header and include `<string>`

In `main.cpp`, find the first two comment lines:

```cpp
// Grade Calculator v0.1 - Chapter 2
// Prints the application banner. Confirms the toolchain works end to end.
```

Replace it with:

```cpp
// Grade Calculator v0.2 - Chapter 3
// Reads one named assignment and echoes a formatted summary.
// New this version: typed variables, std::getline for names.
```

Now find the include line:

```cpp
#include <iostream>
```

Directly below it, add:

```cpp
#include <string>
```

**Why:** `std::string` is not built into the language the way `int` and
`double` are — it comes from the standard library, and `<string>` is the header
that declares it. Leaving the include out produces a confusing error about
`string` not naming a type, which is one of the most common errors beginners
hit. The comment header gains a "New this version" line so your file records
its own history as the project grows.

## Step 2 — Replace the banner with a single line

In `main.cpp`, find all five banner lines:

```cpp
    std::cout << "===================================\n";
    std::cout << "        GRADE CALCULATOR           \n";
    std::cout << "        Version 0.1                \n";
    std::cout << "===================================\n";
    std::cout << "Course: Programming Fundamentals\n";
```

Replace all five with this single line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.2 ===\n\n";
```

**Why:** The five-line box was useful when printing was all the program did.
Now that there is real output below it, a one-line header keeps the screen
readable. Note the `\n\n` at the end — the second newline leaves a blank line
between the header and the first prompt. Spacing is part of a usable interface,
not an afterthought.

> **▶ Run checkpoint:** Click **Run**. The program should print just the new one-line banner and exit. The prompts do not exist yet.

## Step 3 — Read the two names with `std::getline`

In `main.cpp`, find the banner line:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.2 ===\n\n";
```

Directly below it, add:

```cpp

    // Names may contain spaces, so getline is required here.
    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);

    std::string assignmentName;
    std::cout << "Assignment name: ";
    std::getline(std::cin, assignmentName);
```

**Why:** `std::getline(std::cin, variable)` reads an entire line, spaces
included, up to the point where the user pressed Enter. The alternative,
`std::cin >> variable`, stops at the first space — so "Ada Lovelace" would
store only "Ada" and leave "Lovelace" waiting in the input buffer to corrupt
the next read. Any value that can contain a space must be read with
`std::getline`. Declaring each variable immediately above the prompt that
fills it keeps the two together and makes the code read top to bottom.

## Step 4 — Read the two scores with `std::cin >>`

In `main.cpp`, find the line that reads the assignment name:

```cpp
    std::getline(std::cin, assignmentName);
```

Directly below it, add:

```cpp

    // Points are double, not int: partial credit such as 8.5 is common.
    double pointsEarned = 0.0;
    std::cout << "Points earned: ";
    std::cin >> pointsEarned;

    double pointsPossible = 0.0;
    std::cout << "Points possible: ";
    std::cin >> pointsPossible;
```

**Why:** These are numbers, so `std::cin >>` is correct: it skips leading
whitespace and converts the digits to a `double`. The type is `double` rather
than `int` because partial credit is normal — 8.5 out of 10 must be
representable. Initializing each variable to `0.0` at the point of declaration
means that if the read fails the variable still holds a defined value instead
of garbage, which is a habit that prevents a whole class of bugs later.

## Step 5 — Print the summary

In `main.cpp`, find the line that reads the points possible:

```cpp
    std::cin >> pointsPossible;
```

Directly below it, add:

```cpp

    std::cout << "\n--- Summary ---\n";
    std::cout << "Student:    " << studentName << "\n";
    std::cout << "Assignment: " << assignmentName << "\n";
    std::cout << "Score:      " << pointsEarned << " / " << pointsPossible << "\n";
```

**Why:** Echoing input back is how a user confirms the program understood
them. The labels are padded with spaces so the values line up in a column —
`"Student:    "` has four trailing spaces, `"Assignment: "` has one. Alignment
like this is done by hand for now; Chapter 5 replaces it with a proper
formatting approach.

> **▶ Run checkpoint:** Click **Run** and type the inputs below in the Terminal, pressing Enter after each. The summary should match the expected output.

## Expected output

With the inputs `Ada Lovelace`, `Analytical Engine Essay`, `8.5`, and `10`:

```text
=== GRADE CALCULATOR v0.2 ===

Student name: Ada Lovelace
Assignment name: Analytical Engine Essay
Points earned: 8.5
Points possible: 10

--- Summary ---
Student:    Ada Lovelace
Assignment: Analytical Engine Essay
Score:      8.5 / 10
```

Note that `10` prints as `10`, not `10.00`. A `double` prints only as many
decimals as it needs by default. Chapter 4 addresses that.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] A two-word student name is stored and echoed in full, not truncated
      at the space.
- [ ] A score of `8.5` is accepted and echoed as `8.5`.
- [ ] The four labels in the summary line up in a column.
- [ ] The program exits normally after printing the summary.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — for this chapter that is `main.cpp`. **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1436xxx-Grade-Calculator-YourLastName** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 3 Grade Calculator v0.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- Every item in **Check your work** passes.
- **COSC1436xxx-Grade-Calculator-YourLastName** contains the Chapter 3 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
