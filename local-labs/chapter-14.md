# Chapter 14 Lab — Replace Parallel Arrays with Structs

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.1
- **Starting point:** The working Chapter 13 v2.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add `Assignment`, `Score`, `Student`, and `GradeTier` structs.
2. Replace the parallel `gradeCutoffs`/`gradeLetters` vectors with
   `defaultScale()` and `readGradeScale()` functions that build and return a
   `std::vector<GradeTier>` instead of writing to globals.
3. Change `letterFor` to take a `const std::vector<GradeTier>& scale`
   parameter instead of reading the (now-deleted) global scale vectors.
4. Replace the parallel `assignmentNames`/`pointsPossible` vectors with a
   `std::vector<Assignment>`, and the parallel `studentNames`/`earned`
   vectors with a `std::vector<Student>`, each carrying an auto-assigned
   `id` and a `std::vector<Score>`.
5. Extract the drop-lowest earned/possible math that lived inline in
   `main`'s report loop into a new `studentPercentage(const Student&, const
   std::vector<Assignment>&, bool dropLowest)` function.

This checkpoint also **retires the `showAbout()` About screen** — the
startup banner becomes a single line, `=== GRADE CALCULATOR v2.1 (struct
records) ===`. Two behaviors change along with the structs, not just their
internal representation, so name them rather than assuming "preserve
behavior": each student's score entry is now **two** prompts per
assignment — "points earned" then "bonus points" — instead of v2.0's one
combined "points (incl. bonus)" prompt, and the class report gains a new
left column showing each student's auto-assigned ID (starting at 1001)
before the name. `readYesNo`, `readNonNegative`, `readLine`, and
`computePercentage` all carry over unchanged.

## Build it: step by step

Each step below shows the actual code for that piece. Type it in as you go —
don't wait until the end to test. Where a step **replaces** something from
v2.0, the old code is named so you know what to remove.

### Step 1 — The four structs

Add these right after `const bool CAP_AT_100 = true;`, before the input
helpers.

```cpp
struct Assignment {
    std::string name;
    double pointsPossible = 0.0;
};

struct Score {
    double pointsEarned = 0.0;
    double bonusPoints  = 0.0;
};

struct Student {
    std::string name;
    int id = 0;
    std::vector<Score> scores;   // one entry per assignment, same order
};

struct GradeTier {
    double cutoff = 0.0;
    char   letter = 'F';
};
```

`Score` is new — v2.0 had no record for one assignment's result, only a bare
`double` sitting in a parallel `earned` vector. The other three replace a
pair of parallel containers each. Give every member a default value, as
shown — Appendix D's initialization rule applies to struct members exactly
as it does to variables.

### Step 2 — Grade scale functions return a vector instead of writing globals

Delete the two global vectors and rewrite `useDefaultScale`/`readGradeScale`
so each **returns** a `std::vector<GradeTier>` instead of mutating shared
state:

```cpp
// DELETE these two globals:
// std::vector<double> gradeCutoffs;
// std::vector<char> gradeLetters;

std::vector<GradeTier> defaultScale() {
    return { {90.0, 'A'}, {80.0, 'B'}, {70.0, 'C'}, {60.0, 'D'}, {0.0, 'F'} };
}

std::vector<GradeTier> readGradeScale() {
    std::vector<GradeTier> scale;
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers highest first. Type 'done' to finish.\n\n";

    while (true) {
        std::string letterText = readLine("Tier letter (or 'done'): ");
        if (letterText == "done" || letterText.empty()) { break; }
        double cutoff = readNonNegative("  Minimum percentage: ");
        if (!scale.empty() && cutoff >= scale.back().cutoff) {
            std::cout << "  Cutoff must be lower than " << scale.back().cutoff
                      << ". Tier not added.\n";
            continue;
        }
        scale.push_back({cutoff, letterText[0]});
    }
    if (scale.empty() || scale.back().cutoff > 0.0) {
        std::cout << "Note: scale did not reach 0, so an 'F' at 0 was added.\n";
        scale.push_back({0.0, 'F'});
    }
    return scale;
}
```

Renamed: `useDefaultScale` (void, wrote to globals) becomes `defaultScale`
(returns a value). `readGradeScale` keeps its name but changes from `void`
to a function returning `std::vector<GradeTier>`.

### Step 3 — `letterFor` takes the scale as a parameter

```cpp
char letterFor(double percentage, const std::vector<GradeTier>& scale) {
    for (const GradeTier& tier : scale) {
        if (percentage >= tier.cutoff) { return tier.letter; }
    }
    return '?';
}
```

Compare with v2.0's version, which read the two now-deleted globals by name
and indexed them in lockstep: `for (std::size_t i = 0; i < gradeCutoffs.size();
++i) { if (percentage >= gradeCutoffs[i]) { return gradeLetters[i]; } }`.
The new version cannot desynchronize a cutoff from its letter — there is
only one thing to index into.

### Step 4 — `studentPercentage`: pull the drop-lowest math out of `main`

`computePercentage` carries over unchanged and is now called from inside
this new function instead of directly from `main`.

```cpp
double studentPercentage(const Student& student,
                         const std::vector<Assignment>& assignments,
                         bool dropLowest) {
    double earned = 0.0;
    double possible = 0.0;
    for (std::size_t a = 0; a < assignments.size() && a < student.scores.size(); ++a) {
        earned   += student.scores[a].pointsEarned + student.scores[a].bonusPoints;
        possible += assignments[a].pointsPossible;
    }
    if (dropLowest && assignments.size() > 1) {
        std::size_t worst = 0;
        double worstRatio = 2.0;
        for (std::size_t a = 0; a < assignments.size() && a < student.scores.size(); ++a) {
            if (assignments[a].pointsPossible <= 0.0) { continue; }
            double ratio = (student.scores[a].pointsEarned + student.scores[a].bonusPoints)
                         / assignments[a].pointsPossible;
            if (ratio < worstRatio) { worstRatio = ratio; worst = a; }
        }
        if (worstRatio <= 1.0) {
            earned   -= student.scores[worst].pointsEarned + student.scores[worst].bonusPoints;
            possible -= assignments[worst].pointsPossible;
        }
    }
    return computePercentage(earned, possible);
}
```

This is the same earned/possible loop and worst-assignment search that used
to live directly inside `main`'s report `for` loop, indexed into the
`earned`/`pointsPossible` parallel containers. Nothing about the arithmetic
changes — only where it lives and what it reads.

### Step 5 — Delete `showAbout`

Delete the whole `showAbout()` function. In `main`, replace the
`showAbout();` call with one line:

```cpp
std::cout << "=== GRADE CALCULATOR v2.1 (struct records) ===\n";
```

The About screen — version, course, build date/time, scheme — is gone.
There is no struct-based replacement for it in v2.1; it is simply retired.

### Step 6 — Rewrite the assignment and student entry loops in `main`

Replace the parallel-vector declarations and both entry loops with:

```cpp
std::vector<Assignment> assignments;
std::cout << "\n--- Enter assignments ---\n";
while (true) {
    std::string name = readLine("Assignment name (or 'done'): ");
    if (name == "done" || name.empty()) { break; }
    Assignment a;
    a.name = name;
    a.pointsPossible = readNonNegative("  Points possible: ");
    assignments.push_back(a);
}

std::vector<Student> roster;
int nextId = 1001;
std::cout << "\n--- Enter students ---\n";
while (true) {
    std::string name = readLine("Student name (or 'done'): ");
    if (name == "done" || name.empty()) { break; }
    Student s;
    s.name = name;
    s.id = nextId++;
    for (const Assignment& a : assignments) {
        Score sc;
        sc.pointsEarned = readNonNegative("  " + a.name + " points earned: ");
        sc.bonusPoints  = readNonNegative("  " + a.name + " bonus points: ");
        s.scores.push_back(sc);
    }
    roster.push_back(s);
}
```

Gone: `std::vector<std::string> assignmentNames`, `std::vector<double>
pointsPossible`, `std::vector<std::string> studentNames`, and
`std::vector<std::vector<double>> earned`. Notice the single combined
"points (incl. bonus)" prompt from v2.0 is now two prompts per assignment,
one per `Score` member, and each student gets an `id` the moment they're
added. The `dropLowest` line right after the student loop is unchanged from
v2.0 except that it now tests `assignments.size()` instead of
`assignmentNames.size()`.

### Step 7 — Rewrite the report loop

```cpp
double classTotal = 0.0;
for (const Student& s : roster) {
    double pct = studentPercentage(s, assignments, dropLowest);
    classTotal += pct;
    std::cout << std::left << std::setw(6) << s.id
              << std::setw(20) << s.name
              << std::right << std::setw(8) << pct << "%   "
              << letterFor(pct, scale) << "\n";
}
if (!roster.empty()) {
    std::cout << "-------------------------------------\n";
    std::cout << std::left << std::setw(26) << "CLASS AVERAGE"
              << std::right << std::setw(8) << classTotal / roster.size() << "%\n";
} else {
    std::cout << "No students entered.\n";
}
```

The report no longer computes earned/possible totals inline — it calls
`studentPercentage`. `letterFor` now takes `scale` as its second argument.
The new `std::setw(6) << s.id` column pushes the name and total further
right, which is why `"CLASS AVERAGE"` widens from `setw(20)` to `setw(26)`
to keep the divider and the average aligned under the report above it.

## Verification

- Student names cannot be reordered separately from their scores.
- A grade letter cannot exist without its cutoff.
- Given the same assignment points, student scores, and drop-lowest choice,
  v2.1 computes the same percentages and letters as v2.0 — remember that the
  score-entry prompts themselves changed (earned and bonus are now entered
  separately, so re-derive equivalent totals when comparing runs).
- Each student is assigned a unique ID starting at 1001, in entry order.
- The program builds without warnings.

## Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Work through Steps 1–5 above in your local editor, in order. After Step 5
   (once you have the four structs, the scale functions returning a vector,
   the parameterized `letterFor`, `studentPercentage` in place, and
   `showAbout` deleted), rebuild even though `main`'s entry loops haven't
   changed yet — the file should still compile:

   ```bash
   g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
   ```

3. Apply Steps 6 and 7 together, since the rewritten report loop calls
   `studentPercentage` and the new `letterFor`. Rebuild again:

   ```bash
   g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
   ```

4. Fix every compiler error and warning.
5. Run the program and complete the verification list:

   ```bash
   ./gradecalc
   ```

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 14 Grade Calculator v2.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 14 checkpoint.
- The commit is pushed to GitHub.
