# Chapter 15 Lab — Save and Load the Gradebook

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.2
- **Starting point:** The working Chapter 14 v2.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add a `Gradebook` struct that bundles the scale, assignments, and roster
   together, and give it up to `saveGradebook`/`loadGradebook`.
2. Add file-stream support that saves the grade scale, assignments, and
   students to `gradebook.csv`.
3. Load `gradebook.csv` at startup when it exists; parse into a temporary
   `Gradebook` and replace the active one only after the whole file is valid.
4. Replace the single batch-entry pass from v2.1 with a menu loop: add
   assignment, add student, print report, save, quit.
5. Create `gradebook-format.md` documenting every record tag, its field
   order, and the restriction on commas in text fields.

This checkpoint also **retires two Chapter 14 features**: drop-lowest, and
the interactive custom-grade-scale prompt (`readGradeScale`). Persistence and
the menu loop are the point of this chapter; either could return later as its
own addition, but neither is part of v2.2. A saved file can still carry a
custom scale — `loadGradebook` reads whatever `TIER` rows are in the file —
there's just no more interactive prompt to define one from a blank slate.

## Build it: step by step

Each step below shows the actual code for that piece. Type it in as you go —
don't wait until the end to test. Where a step **replaces** something from
v2.1, the old code is named so you know what to remove.

### Step 1 — New includes, constants, and the `Gradebook` struct

Add `<fstream>` and `<sstream>` to your includes, add `DEFAULT_FILE`, and add
a `Gradebook` struct that owns everything `main` used to hold in separate
local variables.

```cpp
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <string>
#include <vector>

const bool CAP_AT_100 = true;
const std::string DEFAULT_FILE = "gradebook.csv";

struct Assignment { std::string name; double pointsPossible = 0.0; };
struct Score      { double pointsEarned = 0.0; double bonusPoints = 0.0; };
struct Student    { std::string name; int id = 0; std::vector<Score> scores; };
struct GradeTier  { double cutoff = 0.0; char letter = 'F'; };

struct Gradebook {
    std::vector<Assignment> assignments;
    std::vector<Student>    roster;
    std::vector<GradeTier>  scale;
    int nextId = 1001;
};
```

`Score`, `Assignment`, `Student`, and `GradeTier` are unchanged from Chapter
14. `Gradebook` is new — it's the one thing you'll save, load, and pass
around instead of three separate vectors and an `int nextId`.

Delete four functions carried over from Chapter 14 that nothing in v2.2
calls: `readYesNo`, `defaultScale`, `readGradeScale`, and `computePercentage`.
`readYesNo` supported the old yes/no prompts, which the menu loop replaces.
`defaultScale` and `readGradeScale` supported the interactive custom-scale
prompt, which v2.2 drops (see above). `computePercentage` is folded directly
into the new `percentageOf` in Step 5. Keep `readNonNegative` and `readLine`
exactly as they were in v2.1 — both are still used.

### Step 2 — A CSV line splitter

Every load needs to turn one text line back into fields. Add this above the
save/load functions:

```cpp
/** Splits one CSV line on commas. Fields containing commas are not supported;
 *  the format documentation states this restriction explicitly. */
std::vector<std::string> splitCsv(const std::string& line) {
    std::vector<std::string> fields;
    std::istringstream in(line);
    std::string field;
    while (std::getline(in, field, ',')) { fields.push_back(field); }
    return fields;
}
```

### Step 3 — `saveGradebook`

Writes the whole `Gradebook` as tagged CSV rows: one `NEXTID` line, one
`TIER` line per grade tier, one `ASSIGNMENT` line per assignment, one
`STUDENT` line per student (with that student's scores trailing on the same
line).

```cpp
bool saveGradebook(const Gradebook& book, const std::string& filename) {
    std::ofstream out(filename);
    if (!out) { return false; }

    out << "# Grade Calculator gradebook file, version 1\n";
    out << "# Section tags allow new record types to be added later.\n";
    out << "NEXTID," << book.nextId << "\n";
    for (const GradeTier& t : book.scale) {
        out << "TIER," << t.cutoff << "," << t.letter << "\n";
    }
    for (const Assignment& a : book.assignments) {
        out << "ASSIGNMENT," << a.name << "," << a.pointsPossible << "\n";
    }
    for (const Student& s : book.roster) {
        out << "STUDENT," << s.id << "," << s.name;
        for (const Score& sc : s.scores) {
            out << "," << sc.pointsEarned << "," << sc.bonusPoints;
        }
        out << "\n";
    }
    return out.good();
}
```

### Step 4 — `loadGradebook`

This is the step most students under-build: it reads into a **local**
`Gradebook loaded`, not directly into `book`. Only if the whole file parses
does `book = loaded;` run at the end. A bad line partway through a bad file
must never leave `book` half-overwritten.

```cpp
/** Loads a gradebook. Returns false and leaves book untouched on failure. */
bool loadGradebook(Gradebook& book, const std::string& filename, std::string& message) {
    std::ifstream in(filename);
    if (!in) {
        message = "No file named '" + filename + "' was found.";
        return false;
    }

    Gradebook loaded;
    std::string line;
    int lineNumber = 0;
    while (std::getline(in, line)) {
        ++lineNumber;
        if (line.empty() || line[0] == '#') { continue; }
        std::vector<std::string> f = splitCsv(line);
        if (f.empty()) { continue; }

        try {
            if (f[0] == "NEXTID" && f.size() >= 2) {
                loaded.nextId = std::stoi(f[1]);
            } else if (f[0] == "TIER" && f.size() >= 3) {
                loaded.scale.push_back({std::stod(f[1]), f[2].empty() ? '?' : f[2][0]});
            } else if (f[0] == "ASSIGNMENT" && f.size() >= 3) {
                loaded.assignments.push_back({f[1], std::stod(f[2])});
            } else if (f[0] == "STUDENT" && f.size() >= 3) {
                Student s;
                s.id = std::stoi(f[1]);
                s.name = f[2];
                for (std::size_t i = 3; i + 1 < f.size(); i += 2) {
                    s.scores.push_back({std::stod(f[i]), std::stod(f[i + 1])});
                }
                loaded.roster.push_back(s);
            } else {
                message = "Unrecognized record on line " + std::to_string(lineNumber)
                        + "; the rest of the file was still loaded.";
            }
        } catch (...) {
            message = "Malformed number on line " + std::to_string(lineNumber)
                    + "; that record was skipped.";
        }
    }

    if (loaded.scale.empty()) {
        loaded.scale = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };
        message = "File had no grade scale; the default scale was used.";
    }
    book = loaded;
    if (message.empty()) { message = "Loaded " + filename + "."; }
    return true;
}
```

### Step 5 — Grading functions, carried over and trimmed

`letterFor` carries over from Chapter 14 with only its parameter names tidied
up (`percentage`→`pct`, `tier`→`t`) — the logic is unchanged. `studentPercentage`
from v2.1 becomes `percentageOf`: the same earned/possible math, now computing
the rounded percentage inline instead of calling the `computePercentage`
helper you deleted in Step 1, and with its `dropLowest` parameter and the
worst-assignment search removed, because drop-lowest isn't part of v2.2.
`printReport` is new: it's the class-report loop pulled out of `main` so the
menu's `3) Report` option can call it on demand instead of it running once at
the end of the program.

```cpp
char letterFor(double pct, const std::vector<GradeTier>& scale) {
    for (const GradeTier& t : scale) { if (pct >= t.cutoff) { return t.letter; } }
    return '?';
}

double percentageOf(const Student& s, const std::vector<Assignment>& as) {
    double earned = 0.0;
    double possible = 0.0;
    for (std::size_t a = 0; a < as.size() && a < s.scores.size(); ++a) {
        earned   += s.scores[a].pointsEarned + s.scores[a].bonusPoints;
        possible += as[a].pointsPossible;
    }
    if (possible <= 0.0) { return 0.0; }
    double raw = earned / possible * 100.0;
    return std::round((CAP_AT_100 ? std::min(raw, 100.0) : raw) * 10.0) / 10.0;
}

void printReport(const Gradebook& book) {
    std::cout << "\n=====================================\n  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);
    if (book.roster.empty()) { std::cout << "No students on the roster.\n\n"; return; }
    for (const Student& s : book.roster) {
        double pct = percentageOf(s, book.assignments);
        std::cout << std::left << std::setw(6) << s.id << std::setw(20) << s.name
                  << std::right << std::setw(8) << pct << "%   "
                  << letterFor(pct, book.scale) << "\n";
    }
    std::cout << "\n";
}
```

### Step 6 — Rewrite `main` as a menu loop

This is the biggest structural change in the chapter. Delete the entire body
of your v2.1 `main` — the custom-grade-scale prompt, the assignment-entry
loop, the student-entry loop, the drop-lowest prompt, and the final report —
and replace it with this:

```cpp
int main() {
    std::cout << "=== GRADE CALCULATOR v2.2 (persistent) ===\n\n";

    Gradebook book;
    book.scale = { {90.0,'A'}, {80.0,'B'}, {70.0,'C'}, {60.0,'D'}, {0.0,'F'} };

    std::string message;
    if (loadGradebook(book, DEFAULT_FILE, message)) {
        std::cout << message << "\n\n";
    } else {
        std::cout << message << " Starting a new gradebook.\n\n";
    }

    bool running = true;
    while (running) {
        std::cout << "1) Add assignment  2) Add student  3) Report  "
                     "4) Save  5) Quit\nChoice: ";
        std::string line;
        if (!std::getline(std::cin, line)) { break; }
        char choice = line.empty() ? '?' : line[0];

        if (choice == '1') {
            Assignment a;
            a.name = readLine("  Assignment name: ");
            if (a.name.empty()) { continue; }
            a.pointsPossible = readNonNegative("  Points possible: ");
            book.assignments.push_back(a);
            for (Student& s : book.roster) { s.scores.push_back({0.0, 0.0}); }
            std::cout << "  Added.\n\n";
        } else if (choice == '2') {
            Student s;
            s.name = readLine("  Student name: ");
            if (s.name.empty()) { continue; }
            s.id = book.nextId++;
            for (const Assignment& a : book.assignments) {
                Score sc;
                sc.pointsEarned = readNonNegative("  " + a.name + " points earned: ");
                sc.bonusPoints  = readNonNegative("  " + a.name + " bonus: ");
                s.scores.push_back(sc);
            }
            book.roster.push_back(s);
            std::cout << "  Added as ID " << s.id << ".\n\n";
        } else if (choice == '3') {
            printReport(book);
        } else if (choice == '4') {
            std::cout << (saveGradebook(book, DEFAULT_FILE)
                          ? "  Saved to " + DEFAULT_FILE + ".\n\n"
                          : "  Could not write " + DEFAULT_FILE + ".\n\n");
        } else if (choice == '5') {
            running = false;
        } else {
            std::cout << "  Please enter 1-5.\n\n";
        }
    }

    if (saveGradebook(book, DEFAULT_FILE)) {
        std::cout << "Gradebook saved. Goodbye.\n";
    } else {
        std::cout << "Warning: could not save. Goodbye.\n";
    }
    return 0;
}
```

Notice the program now **loads on startup and saves on exit automatically**,
in addition to the explicit `4) Save` option — so a student who forgets to
save before quitting doesn't lose the session.

### Step 7 — Write `gradebook-format.md`

Document the file format your code just implemented: the `NEXTID`, `TIER`,
`ASSIGNMENT`, and `STUDENT` tags, the field order for each, and the rule that
comma-containing text fields aren't supported. Base it on what `saveGradebook`
actually writes — don't describe a format your code doesn't produce.

## Verification

- A save-then-load round trip reproduces the same gradebook.
- A missing file is handled without a crash (a first run with no
  `gradebook.csv` starts a new, empty gradebook).
- A nonnumeric field, truncated student row, unknown tag, and missing grade
  tiers are each rejected or repaired without crashing.
- A failed load does not destroy the active in-memory data.
- Quitting from the menu, and letting the program exit any other way, both
  leave a valid `gradebook.csv` behind.

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
4. Work through Steps 1–7 above in StudySite's internal editor, in order.
   Click **Run** after Steps 1–4 (once you have `Gradebook`, `splitCsv`,
   `saveGradebook`, and `loadGradebook` in place) even though `main` hasn't
   changed yet — the file should still compile. Then apply Steps 5 and 6
   together, since `main` calls `printReport`.
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
   editor, including `gradebook-format.md`. **Save to GitHub includes every
   open editor file**, so close scratch files and accidental `_imported`
   duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 15 Grade Calculator v2.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 15
  checkpoint, including `gradebook-format.md`.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
