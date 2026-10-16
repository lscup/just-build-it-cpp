# Chapter 09 Lab — Rebuild with Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.0
- **Starting point:** Your committed Chapter 8 v0.7 program (one file, one long `main`).

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

Your `main` has grown to seventy lines and does five unrelated jobs. This
chapter rebuilds the same behavior out of six small functions, each with one
job and a documentation comment stating what it takes, what it returns, and
what it assumes. Then it adds the thing functions make possible: a **menu
loop**, so the program keeps running and the user chooses what to do next
instead of answering a fixed sequence of questions once.

Nothing about the grading changes. The output for the same inputs is
identical. What changes is that the program becomes something you can read a
piece at a time. By the end you will have:

1. `applyBonus`, `computePercentage`, and `assignLetterGrade` — three pure
   calculations that take values and return values.
2. `readAssignment` — reads one assignment and updates the running totals
   through **reference parameters**.
3. `printReport` and `readMenuChoice` — one prints, one asks.
4. A `main` of about thirty lines: set up, loop on a menu with a `switch`,
   print a final report, exit.

> **Note:** individual assignments are still not stored — there are no arrays
> until Chapter 11 — so the program keeps running totals only. Adding an
> assignment and viewing the report many times is now possible; listing the
> assignments is not, yet.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Edit (Steps 1-9) |

When you are finished your project still has **one** `.cpp` file.

## How to use these steps

This lab is a guided exercise, not a test. Each step tells you **which file**
to open, shows the **exact code to find**, and shows the **exact code to put in
its place**. Work through the steps in order and copy the code from the boxes
rather than retyping it where you can.

- A **find** box shows code exactly as it appears in your program at the end
  of the previous chapter. Use the editor's search to locate it. If you cannot
  find it, your program differs from the previous checkpoint — compare it with
  your last commit on GitHub before going further.
- A **▶ Build checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.

## Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Continue the existing program in your local editor, finish the steps in order, then build.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Step 1 — Update the comment header

In `main.cpp`, find the eight header comment lines above the `Build:` line:

```cpp
// Grade Calculator v0.7 - Chapter 8
// Correct rounding and a documented bonus-point cap policy.
// New this version: std::round, std::min, library functions replace hand-rolled logic.
//
// POLICY DECISION (documented per Chapter 4): this gradebook CAPS the reported
// percentage at 100. Bonus points can rescue a low score but cannot produce a
// grade above the maximum. Set CAP_AT_100 to false for uncapped reporting.
//
```

Replace it with:

```cpp
// Grade Calculator v1.0 - Chapter 9
// Same behavior as v0.7, rebuilt from documented functions, plus a menu loop.
// New this version: user-defined functions, a menu that keeps the program running.
// Note: individual assignments are not stored yet (no arrays until Chapter 11),
// so the program keeps running totals only.
```

**Why:** The policy block moves out of the header because the policy is about
to live inside `computePercentage`, documented on the function that implements
it. A comment belongs as close as possible to the code it describes. What
replaces it is the new limitation worth recording: no storage of individual
assignments yet.

## Step 2 — Write `applyBonus`

> **Where these go:** each function in Steps 2-7 is added **above** `int main()`
> and below the constants. Add them in order, so each new one appears directly
> above `int main()` and below the one you added before it. A function must be
> declared before the code that calls it, and `main` calls all of them.

In `main.cpp`, find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Adds bonus points to a raw score.
 * @param  pointsEarned  raw points earned, must be >= 0
 * @param  bonusPoints   bonus to add, must be >= 0
 * @return the combined total
 */
double applyBonus(double pointsEarned, double bonusPoints) {
    return pointsEarned + bonusPoints;
}
```

**Why:** This is the smallest useful function in the program — one line of
arithmetic — and it is worth writing precisely because it is small. The name
says what the operation *means*, where `pointsEarned + bonusPoints` only says
what it does. If the bonus policy ever changes, there is now exactly one place
to change it.

Read the documentation comment carefully, because every function from here on
has one. `@param` describes each input and any constraint on it; `@return`
describes what comes back. Writing this before the body forces you to decide
what the function is responsible for, which is most of the work of designing
one.

## Step 3 — Write `computePercentage`

Again find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Converts points to a percentage, capped by course policy.
 * @param  earned    total points earned including bonus
 * @param  possible  total points possible, must be > 0
 * @return percentage rounded to one decimal place
 * @pre    possible > 0; the caller must check this first
 */
double computePercentage(double earned, double possible) {
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}
```

**Why:** The cap and the rounding from Chapter 8 move in here, unchanged. Now
there is one place in the program that knows how a percentage is produced, and
the policy constant is read at exactly one site.

Note the `@pre` line — a **precondition**. This function divides by
`possible`, so it requires `possible > 0`, and it states that the *caller* must
check. That is a real design decision: the alternative is for the function to
check and return some sentinel value, which pushes the problem to every caller
instead. Either is defensible; what matters is writing down which one you
chose, because a caller cannot guess.

## Step 4 — Write `assignLetterGrade`

Find the start of `main` once more:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Maps a percentage to a letter grade on the fixed course scale.
 * @param  percentage  a value from 0 upward
 * @return one of A, B, C, D, F
 */
char assignLetterGrade(double percentage) {
    if (percentage >= A_CUTOFF) { return 'A'; }
    if (percentage >= B_CUTOFF) { return 'B'; }
    if (percentage >= C_CUTOFF) { return 'C'; }
    if (percentage >= D_CUTOFF) { return 'D'; }
    return 'F';
}
```

**Why:** Compare this to the `if`/`else if` chain it replaces. There is no
`else if` and no `letter` variable — each test simply **returns** when it
matches. `return` exits the function immediately, so reaching the second `if`
already proves the first was false. The `else` is implied by control flow.

This is the clearest form this logic can take, and it is only available because
the code is in a function. Inside `main` you had to assign to a variable and
carry it along; here the answer leaves the moment it is known. The final
`return 'F';` is the default, reached only when all four tests fail.

## Step 5 — Write `readAssignment`

Find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Prompts for and reads one assignment, updating the running totals.
 * @param  totalEarned    running total, updated in place
 * @param  totalPossible  running total, updated in place
 * @param  count          assignment count, updated in place
 */
void readAssignment(double& totalEarned, double& totalPossible, int& count) {
    std::string assignmentName;
    std::cout << "  Assignment name : ";
    std::getline(std::cin, assignmentName);

    double pointsEarned = 0.0;
    std::cout << "  Points earned   : ";
    std::cin >> pointsEarned;

    double pointsPossible = 0.0;
    std::cout << "  Points possible : ";
    std::cin >> pointsPossible;

    double bonusPoints = 0.0;
    std::cout << "  Bonus points    : ";
    std::cin >> bonusPoints;
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');

    totalEarned += applyBonus(pointsEarned, bonusPoints);
    totalPossible += pointsPossible;
    ++count;
    std::cout << "  Recorded: " << assignmentName << "\n\n";
}
```

**Why:** This is the chapter's most important new idea: the `&` in
`double& totalEarned`. That is a **reference parameter**, and it means the
function receives the caller's actual variable rather than a copy of its value.
`totalEarned += ...` inside this function changes `main`'s `totalEarned`.

Without references this function could not work. A normal parameter is a copy;
adding to the copy would update something that ceases to exist when the
function returns, and `main`'s totals would stay at zero. The three
accumulators must be references because updating them *is* the function's job.

Notice also that this function calls `applyBonus` rather than adding the bonus
itself, and that the prompts and the `std::cin.ignore` call moved in here
wholesale. Everything about reading one assignment now lives in one place.

## Step 6 — Write `printReport`

Find the start of `main`:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Prints the full course report for the current totals.
 */
void printReport(const std::string& student, double earned, double possible, int count) {
    std::cout << "\n--- COURSE REPORT ---\n";
    std::cout << "Student:     " << student << "\n";
    std::cout << "Assignments: " << count << "\n";
    std::cout << std::fixed << std::setprecision(1);
    std::cout << "Total:       " << earned << " / " << possible << "\n";

    if (count == 0 || possible <= 0.0) {
        std::cout << "No course grade is available yet.\n\n";
        return;
    }
    double percentage = computePercentage(earned, possible);
    std::cout << "Percentage:  " << percentage << "%\n";
    std::cout << "Grade:       " << assignLetterGrade(percentage) << "\n\n";
}
```

**Why:** `const std::string& student` is a reference too, but for the opposite
reason. Copying a string means copying its characters, which is wasted work;
passing a reference avoids that. The `const` then promises the function will
not modify it — so the reference is purely an efficiency measure, with no
change in meaning. **`const` reference for input you only read, plain reference
for values you intend to change** is the convention worth internalizing.

The guard clause from Chapter 8 survives as an early `return` from this
function, and the function calls `computePercentage` and `assignLetterGrade`
rather than repeating their logic. This is what the rebuild buys: the report
reads like a description of itself.

## Step 7 — Write `readMenuChoice`

Find the start of `main` for the last time:

```cpp
int main() {
```

Directly above it, add:

```cpp
/**
 * Displays the menu and returns the user's choice as a character.
 */
char readMenuChoice() {
    std::cout << "1) Add assignment   2) View report   3) Quit\n";
    std::cout << "Choice: ";
    std::string line;
    std::getline(std::cin, line);
    return line.empty() ? '?' : line[0];
}
```

**Why:** This reads a whole line with `getline` and returns only its first
character. Reading the line — rather than a single `char` with `>>` — is what
keeps the input buffer clean, so the `getline` inside `readAssignment` is not
derailed by a leftover newline. It is the Chapter 7 lesson applied
structurally: handle input a line at a time and the buffer problem stops
recurring.

`line.empty() ? '?' : line[0]` guards the case where the user just presses
Enter. Reading `line[0]` of an empty string is undefined behavior — it might
appear to work, which is worse than crashing. Returning `'?'` sends it to the
`default` branch and the program asks again.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should behave exactly as it did in Chapter 8 — the six new functions are defined but nothing calls them yet. This checkpoint proves all six compile before you rewrite `main` around them.

## Step 8 — Rebuild `main` around the menu

In `main.cpp`, find the first line inside `main`:

```cpp
    std::cout << "=== GRADE CALCULATOR v0.7 ===\n\n";
```

Delete that line and everything below it (about seventy lines), down to and including this line:

```cpp
    return 0;
```

In the space where that code was, enter this — the whole of the new `main`:

```cpp
    std::cout << "=== GRADE CALCULATOR v1.0 ===\n\n";

    std::string studentName;
    std::cout << "Student name: ";
    std::getline(std::cin, studentName);
    std::cout << "\n";

    double totalEarned = 0.0;
    double totalPossible = 0.0;
    int assignmentCount = 0;
    bool running = true;

    while (running) {
        char choice = readMenuChoice();
        switch (choice) {
            case '1':
                readAssignment(totalEarned, totalPossible, assignmentCount);
                break;
            case '2':
                printReport(studentName, totalEarned, totalPossible, assignmentCount);
                break;
            case '3':
                running = false;
                break;
            default:
                std::cout << "Please enter 1, 2, or 3.\n\n";
                break;
        }
    }

    printReport(studentName, totalEarned, totalPossible, assignmentCount);
    std::cout << "Goodbye.\n";
    return 0;
```

**Why:** `main` is now a description of the program rather than the program
itself: greet, set up the totals, loop until the user quits, print a final
report. Every line of detail lives in a function with a name.

The **menu loop** is the new behavior. `while (running)` keeps going until
something sets `running` to `false`, and the `switch` dispatches on the
character returned by `readMenuChoice`. A `switch` is the natural fit when you
are choosing among a fixed set of discrete values; it reads better than four
chained `if`s comparing the same variable.

Two details that matter. Every `case` ends with `break` — without it, control
**falls through** into the next case and runs its code too, which is a classic
bug and the reason `break` is not optional here. And `default` catches
everything unmatched, so an unexpected keystroke produces a helpful message
rather than silence.

The final `printReport` call after the loop means the student always sees their
grade on the way out, whether or not they chose option 2.

## Step 9 — Remove the now-unused sentinel

In `main.cpp`, find the `SENTINEL` constant and delete it:

```cpp
const std::string SENTINEL = "done";
```

**Why:** The menu replaced the sentinel: the user now chooses `3` to quit
instead of typing `done` as an assignment name. A constant nothing references
is dead weight that invites the next reader to wonder what it is for. Deleting
code that has stopped being used is part of finishing a change, not an
afterthought.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> Click **Run** and work through the test plan below in the Terminal.

## Test plan

**1. The menu works.** Enter student `Ada Lovelace`. You should see the menu.
Choose `2` straight away: the report shows `Assignments: 0` and
`No course grade is available yet.` Then choose `3`: the report prints once
more, followed by `Goodbye.`

**2. Add, view, add, view.** Restart and choose `1`, entering `Essay`, `45`,
`50`, `0`. Choose `2` — total `45.0 / 50.0`, percentage `90.0%`, grade `A`.
Choose `1` again with `Quiz`, `10`, `50`, `0`. Choose `2` — total
`55.0 / 100.0`, `55.0%`, grade `F`. Being able to view a report *between*
entries is the new capability this chapter unlocked.

**3. Invalid input.** At the menu, type `x` and press Enter: `Please enter 1,
2, or 3.` and the menu returns. Then press Enter on its own with no text: the
same message, via the `'?'` from `readMenuChoice`. Neither should crash or
skip a prompt.

**4. Multi-word names still work.** Choose `1` and enter `Final Research
Paper` as the assignment name. It must be stored in full and echoed by the
`Recorded:` line.

**5. Identical results.** Run the same inputs you used in Chapter 8 and
confirm the percentage and grade are the same. This chapter restructured the
program; it must not have changed its answers.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] `main` is about thirty lines and contains no arithmetic.
- [ ] Each of the six functions has a documentation comment.
- [ ] The three accumulator parameters of `readAssignment` are references
      (`double&`, `int&`), and the totals in `main` actually change.
- [ ] `printReport` takes the student name as a `const std::string&`.
- [ ] Every `case` in the `switch` ends with `break`.
- [ ] Choosing `3` prints the report and then `Goodbye.`
- [ ] `SENTINEL` no longer appears anywhere in the file.
- [ ] The same inputs produce the same grade as your Chapter 8 program.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 9 Grade Calculator v1.0"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 9 checkpoint.
- The commit is pushed to GitHub.
