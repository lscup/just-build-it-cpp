# Chapter 16 Lab — Debug and Add Regression Tests

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.3
- **Starting point:** The working Chapter 15 v2.2 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Seed the same three defects described below into a copy of your own
   working v2.2 code, so you observe each failure before you fix it.
2. Find and fix **Defect 1 (D1)**, an off-by-one loop bound, and
   **Defect 3 (D3)**, a `>` used where `>=` is required — both in `letterFor`.
3. Find and fix **Defect 2 (D2)**, bonus points wrongly added to points
   possible as well as points earned, in `percentageOf`.
4. Add a `check`/`runTests` regression-test harness that exercises all three
   defects plus the zero-points-possible boundary, and wire a new
   `5) Run tests` menu option to call it.
5. Renumber the menu so `6) Quit` replaces the old `5) Quit`, and update the
   invalid-choice prompt to `1-6`.
6. Create `defect-reports.md` recording the symptom, reproduction steps,
   cause, correction, and regression test for each of the three defects.

Nothing from v2.2 is **retired** this chapter, but two things change that are
easy to miss. First, the menu grows a line — quitting moves from choice `5`
to choice `6`, and `5` now runs the tests — so if you type the menu loop by
hand rather than copying it, don't leave a stray `else if (choice == '5')
{ running = false; }` behind. Second, the reference solution's own header
comment says "Run the tests from menu option 6" — that line in the reference
file is wrong about its own code. The code beneath it wires `'5'` to
`runTests()` and `'6'` to quitting. Write your own header comment to say it
correctly: **5 runs the tests, 6 quits.**

## Build it: step by step

Each step below shows the actual broken code to type in and watch fail, then
the fix. Build with `-g` so the debugger has your names and line numbers, and
rebuild after each step — don't wait until the end to test.

### Step 1 — Reproduce and fix D1 and D3 in `letterFor`

Temporarily change your working `letterFor` to this broken version:

```cpp
char letterFor(double pct, const std::vector<GradeTier>& scale) {
    for (std::size_t i = 0; i <= scale.size(); ++i) {
        if (pct > scale[i].cutoff) { return scale[i].letter; }
    }
    return '?';
}
```

Rebuild, run, and reproduce **D3** first: add one assignment worth 10 points,
add a student who earns exactly 9 points with no bonus (90.0%), and print the
report. You should see an A; the broken build prints a B. Set a breakpoint
on the `if (pct > scale[i].cutoff)` line, watch `pct` and `scale[i].cutoff`
in the Watch panel, and step through with F10. When `i` is 0 (the
90.0-cutoff tier), `pct` and `scale[i].cutoff` are both `90.0` — and
`pct > scale[i].cutoff` evaluates `false`, because they are *equal*, not
greater. The loop falls through to the B tier instead of stopping here. That
confirms D3: the comparison needs `>=`.

Now reproduce **D1** without changing anything back yet: add a student who
earns 0 points on that same assignment (0.0%). The default scale's lowest
tier is `{0.0, 'F'}`, so the same `>` bug means `pct > scale[i].cutoff` is
`false` for that tier too — the loop never returns inside the vector and
walks off the end. Move your breakpoint's watch to `i` and `scale.size()`
instead, and step through with F10: `i` climbs 0, 1, 2, 3, 4, and the loop
condition `i <= scale.size()` still lets it run once more at `i == 5`, which
equals `scale.size()`. At that point `scale[i]` reads past the end of the
vector — undefined behavior. Depending on what happens to be in memory
there, you might see a crash, a garbage letter, or by chance a plausible one;
none of those outcomes is correct, and none is guaranteed to repeat.

Fix both defects at once by restoring the range-for loop with `>=`:

```cpp
char letterFor(double pct, const std::vector<GradeTier>& scale) {
    for (const GradeTier& t : scale) { if (pct >= t.cutoff) { return t.letter; } }
    return '?';
}
```

Rebuild and repeat both inputs: 9/10 should now report A, and 0/10 should
report F, every time.

### Step 2 — Reproduce and fix D2 in `percentageOf`

Temporarily change `percentageOf`'s accumulation line so bonus points count
toward `possible` as well as `earned`:

```cpp
double percentageOf(const Student& s, const std::vector<Assignment>& as) {
    double earned = 0.0;
    double possible = 0.0;
    for (std::size_t a = 0; a < as.size() && a < s.scores.size(); ++a) {
        earned   += s.scores[a].pointsEarned + s.scores[a].bonusPoints;
        possible += as[a].pointsPossible + s.scores[a].bonusPoints;
    }
    if (possible <= 0.0) { return 0.0; }
    double raw = earned / possible * 100.0;
    return std::round((CAP_AT_100 ? std::min(raw, 100.0) : raw) * 10.0) / 10.0;
}
```

Reproduce: one assignment worth 10 points, a student who earns 8 points with
2 bonus. By hand, 8 + 2 earned out of 10 possible should cap at 100%. The
broken build reports 83.3% instead. Set a breakpoint on the
`possible += ...` line inside the loop, and watch `possible` and
`s.scores[a].bonusPoints`. Step over the line once with F10: `possible`
jumps from `0.0` to `12.0`, not `10.0` — the bonus leaked into the
denominator. That confirms D2.

Fix it by dropping the bonus term from the `possible` accumulation — bonus
only ever helps `earned`:

```cpp
possible += as[a].pointsPossible;
```

Rebuild and repeat 8+2-out-of-10; you should now see exactly 100.0%.

### Step 3 — Add the regression-test harness

Above `main`, add the `check` helper and a `runTests` function that
exercises all three defects plus one extra boundary — an assignment worth
zero points, which must not divide by zero:

```cpp
int checksRun = 0;
int checksFailed = 0;

void check(bool condition, const std::string& label) {
    ++checksRun;
    if (condition) {
        std::cout << "  PASS  " << label << "\n";
    } else {
        ++checksFailed;
        std::cout << "  FAIL  " << label << "\n";
    }
}

void runTests() {
    std::cout << "\n--- Regression tests ---\n";
    std::vector<GradeTier> scale = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };

    // D3: exactly at a cutoff must take the higher grade.
    check(letterFor(90.0, scale) == 'A', "D3 90.0 is an A, not a B");
    check(letterFor(80.0, scale) == 'B', "D3 80.0 is a B, not a C");
    check(letterFor(60.0, scale) == 'D', "D3 60.0 is a D, not an F");

    // D1: a percentage below every cutoff must not read past the end.
    check(letterFor(0.0, scale)  == 'F', "D1 0.0 is an F, no out-of-range read");
    check(letterFor(-5.0, scale) == '?', "D1 below scale returns '?', no crash");

    // D2: bonus raises earned points only, never points possible.
    std::vector<Assignment> as = { {"HW1", 10.0} };
    Student withBonus;
    withBonus.scores.push_back({8.0, 2.0});     // 8 earned + 2 bonus out of 10
    check(percentageOf(withBonus, as) == 100.0, "D2 8+2 bonus of 10 is 100%, not 83.3%");

    Student noBonus;
    noBonus.scores.push_back({8.0, 0.0});
    check(percentageOf(noBonus, as) == 80.0,    "D2 8 of 10 with no bonus is 80%");

    // Boundary: an assignment worth zero points must not divide by zero.
    std::vector<Assignment> zero = { {"Ungraded", 0.0} };
    Student s2;
    s2.scores.push_back({0.0, 0.0});
    check(percentageOf(s2, zero) == 0.0, "zero points possible does not crash");

    std::cout << "  " << (checksRun - checksFailed) << " of " << checksRun
              << " checks passed.\n\n";
    checksRun = 0;
    checksFailed = 0;
}
```

If you run this with either defect still in place, one or more lines print
`FAIL` instead of `PASS` — that is the point of a regression test: it fails
before the fix and passes after. Once both fixes from Steps 1 and 2 are in
place, every line should print `PASS`.

### Step 4 — Rewire the menu: 5 runs tests, 6 quits

Change the menu prompt, add a `'5'` branch that calls `runTests()`, move
quitting to `'6'`, and update the invalid-input message:

```cpp
std::cout << "1) Add assignment  2) Add student  3) Report  "
             "4) Save  5) Run tests  6) Quit\nChoice: ";
...
} else if (choice == '5') {
    runTests();
} else if (choice == '6') {
    running = false;
} else {
    std::cout << "  Please enter 1-6.\n\n";
}
```

If you are working from a printed or reference copy of `main.cpp`, note that
its own header comment claims "Run the tests from menu option 6." That
comment is wrong about its own code. The code beneath it wires `'5'` to
`runTests()` and `'6'` to quitting — write your own header comment
correctly.

## Verification

- Before you apply the fixes, each seeded defect makes at least one
  `runTests()` check print `FAIL`: D3 fails the exact-cutoff checks, D1
  fails (or crashes on) the `0.0` and below-scale checks, and D2 fails the
  bonus check.
- After both fixes, choosing `5) Run tests` prints `8 of 8 checks passed.`
  with no `FAIL` lines.
- A student scoring exactly at a cutoff (e.g., 90.0%) receives the higher
  letter grade, not the lower one.
- A student scoring at or below the lowest cutoff (0.0%) still returns `F`,
  and a percentage below the whole scale returns `?` — neither reads past
  the end of the scale vector.
- A bonus that brings a student exactly to an assignment's points possible
  caps the percentage at 100%, never inflating the denominator.
- Choosing `5` runs the tests and `6` quits; there is no longer a `5) Quit`
  option.
- The normal Grade Calculator menu (add assignment, add student, report,
  save) still works.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click each source,
   header, or documentation file needed for this chapter. Confirm the editor
   shows the expected file paths before editing.
4. Work through Steps 1–4 above in StudySite's internal editor, in order:
   seed and fix D1/D3 in `letterFor` first and confirm both test inputs
   behave correctly; then seed and fix D2 in `percentageOf` and confirm the
   bonus case; then add the `check`/`runTests` harness; then rewire the
   menu, since the new `5) Run tests` line depends on `runTests` already
   existing. Click **Run** after each step.
5. Click **Run**. Read compiler messages and program output in the embedded
   Terminal, and type program input there when prompted.
6. Fix every compiler error and warning, then complete the verification
   list.
7. Use the Tutor with the current code or Terminal output when you need
   help.

## Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor, including `defect-reports.md`. **Save to GitHub includes every
   open editor file**, so close scratch files and accidental `_imported`
   duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 16 Grade Calculator v2.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 16
  checkpoint, including `defect-reports.md`.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
