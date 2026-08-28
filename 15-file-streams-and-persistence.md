# Chapter 15 — File Streams and Persistent Data

## Learning Objectives

When you finish this chapter you will be able to:

- Explain what a stream abstracts, and why files and the console share an interface. *(SLO 2.1)*
- Write to a file with `std::ofstream` and read from one with `std::ifstream`. *(SLO 2.6)*
- Check stream state and handle a file that is missing or malformed. *(SLO 2.1)*
- Read a file line by line and split each line into fields. *(SLO 2.6)*
- Convert text to numbers safely with `std::stod` and `std::stoi`. *(SLO 2.6)*
- Use `std::stringstream` to build and parse text in memory. *(SLO 2.6)*
- Design a documented file format, and judge whether it can accommodate future data. *(SLO 2.1, 2.4)*
- Build Grade Calculator v2.2 — a gradebook that survives being closed.

---

## 15.1 Streams as an Abstraction

Chapter 1 Section 1.2 said main memory is **volatile**: when your program ends, everything it held is gone. Every version of the Grade Calculator so far has thrown away the entire roster on exit.

Files fix that, and this chapter is item three on your Chapter 13 backlog — *perfective* maintenance, adding capability users want.

A **stream** is a sequence of data flowing to or from somewhere. You have used two since Chapter 2:

```cpp
std::cout << "text";     // a stream to the screen
std::cin >> value;       // a stream from the keyboard
```

File streams use the **same operators**:

```cpp
std::ofstream out("gradebook.csv");
out << "text";                        // a stream to a file

std::ifstream in("gradebook.csv");
in >> value;                          // a stream from a file
```

That sameness is the point of the abstraction. Code written against a stream does not care what is on the other end, which means the reporting code you already have could write to a file with almost no change. Chapter 19 exploits this properly with `operator<<`.

| Type | Header | Direction |
|---|---|---|
| `std::ofstream` | `<fstream>` | output — write to a file |
| `std::ifstream` | `<fstream>` | input — read from a file |
| `std::ostringstream` | `<sstream>` | output — build a string in memory |
| `std::istringstream` | `<sstream>` | input — read from a string in memory |

---

## 15.2 Writing to a File

```cpp
#include <fstream>

std::ofstream out("gradebook.csv");
out << "STUDENT,1001,Ada Lovelace\n";
out << "WORK,1001,Midterm,84,100,5\n";
```

The file is created if it does not exist and **emptied if it does**. That second behavior deserves respect — opening for output destroys the previous contents immediately, before you write anything.

The file closes automatically when the stream goes out of scope. You may close it explicitly with `out.close()`, and it is worth doing when you need to reopen the file for reading in the same function.

Everything from Chapter 4 works: `std::fixed`, `std::setprecision`, `std::setw` all apply to file streams exactly as to `std::cout`.

---

## 15.3 Reading from a File

```cpp
std::ifstream in("gradebook.csv");

std::string line;
while (std::getline(in, line)) {
    // process one line
}
```

`std::getline(in, line)` reads one line and returns the stream, which converts to `false` when there is nothing more. That makes it the standard idiom for reading a whole file — and it is Chapter 7's sentinel loop, with end-of-file as the sentinel.

---

## 15.4 Checking Stream State

**A file may not open.** It may not exist, or you may lack permission. Always check:

```cpp
std::ifstream in("gradebook.csv");
if (!in) {
    std::cout << "No file named 'gradebook.csv' was found.\n";
    return;
}
```

```text
opened nope.csv? false
!missing evaluates to true
```

A stream converts to `false` when something has gone wrong. `!in` is the idiomatic test.

| Test | True when |
|---|---|
| `in.is_open()` | the file opened successfully |
| `in.eof()` | reading reached end of file |
| `in.fail()` | an operation failed, such as reading text into a number |
| `in.good()` | nothing has gone wrong |
| `!in` | the stream is in a failed or ended state |

**Failing to check is the most common file-handling defect**, and the symptom is misleading: a program that reads a missing file simply sees no data and reports an empty gradebook, exactly as though the file were empty. The user concludes their work was lost.

---

## 15.5 Parsing a Line into Fields

Reading a line gives you text. Splitting it is the next step, and `std::istringstream` makes it straightforward:

```cpp
#include <sstream>

std::vector<std::string> splitCsv(const std::string& line) {
    std::vector<std::string> fields;
    std::istringstream in(line);
    std::string field;
    while (std::getline(in, field, ',')) {
        fields.push_back(field);
    }
    return fields;
}
```

The third argument to `getline` is the **delimiter** — the character that ends each piece. Reading a string as though it were a stream is a genuinely useful trick, and it appears again whenever text needs structure.

```text
1: (skipped comment)
2: tag=STUDENT fields=3
3: tag=WORK fields=6
```

> **This simple splitter does not handle fields containing commas.** A student named `Lovelace, Ada` would split into two fields and corrupt the record. Real CSV handles this with quoting. This book's format documentation states the restriction explicitly, which is the honest alternative to pretending the problem does not exist.

---

## 15.6 Converting Text to Numbers

Fields arrive as text. Converting is a place where bad data becomes a crash if you are careless:

| Function | Converts to |
|---|---|
| `std::stod(s)` | `double` |
| `std::stoi(s)` | `int` |

```cpp
double points = std::stod("84.5");     // 84.5
```

```text
stod("abc") threw invalid_argument
stod("84.5") = 84.5
```

**These throw when the text is not a number.** `std::stod("abc")` raises `std::invalid_argument`; a number too large raises `std::out_of_range`. An unhandled exception terminates the program.

Catch them:

```cpp
try {
    points = std::stod(field);
} catch (const std::invalid_argument&) {
    std::cout << "Line " << lineNumber << ": expected a number.\n";
}
```

Chapter 24 covers exceptions properly. What you need here is the shape — `try`, then `catch` — and the reason: **a file is outside your program, so nothing guarantees its contents are what you expect.** That is Chapter 11's lesson about validating external data, arriving in a new form.

---

## 15.7 Building Text in Memory

`std::ostringstream` builds a string using stream operators:

```cpp
#include <sstream>

std::ostringstream out;
out << std::fixed << std::setprecision(1) << percentage << "%";
std::string text = out.str();
```

This is how `formatGrade` was implemented in Chapter 10 without explanation. It is the clean way to produce formatted text when you need a `std::string` rather than immediate output.

---

## 15.8 Designing a File Format

This is the design work of the chapter, and it is more consequential than the code.

### Requirements for a gradebook format

**Human-readable.** You should be able to open it and see what is wrong. Binary formats are compact and useless when something breaks.

**Line-oriented.** One record per line, so a corrupt line damages one record rather than everything.

**Self-describing.** A reader should be able to tell what each line is without counting positions.

**Extensible.** New kinds of record should be addable without invalidating existing files.

### A format that meets them

```text
# Grade Calculator gradebook file, version 1
# Section tags allow new record types to be added later.
NEXTID,1002
TIER,90,A
TIER,80,B
TIER,0,F
ASSIGNMENT,Homework 1,10
STUDENT,1001,Ada,9,1
```

Each line begins with a **tag** naming the record type. Lines beginning with `#` are comments and are skipped. A reader dispatches on the tag and ignores tags it does not recognize.

That last property is what makes the format extensible. Adding a `CATEGORY` record later does not break a reader that has never heard of one — it skips the line and carries on.

### The question you cannot answer yet

Your Chapter 13 maintenance plan analyzed weighted grading. Weighted grading needs category names and weights stored somewhere.

**Can this format hold them?** Think about it before reading on, and write down your answer.

The tag design says yes: add `CATEGORY,Exam,50` lines, and old readers skip them while new readers use them. If instead you had chosen a fixed-column format — "field 4 is always points possible" — adding data would mean changing every position and invalidating every existing file.

**You will find out in Chapter 21 whether your format actually was extensible.** That is a real test of a design decision made twelve chapters earlier, and it is worth making deliberately rather than by luck.

### Documenting the format

Write it down, in a file beside your code:

```text
GRADEBOOK FILE FORMAT, version 1
--------------------------------
Plain text, one record per line, fields separated by commas.
Lines beginning with # are comments. Blank lines are ignored.
Unrecognized tags are skipped, so new record types may be added.

RESTRICTION: fields may not contain commas.

NEXTID,<n>                      the next student ID to assign
TIER,<cutoff>,<letter>          one grade scale tier, highest first
ASSIGNMENT,<name>,<possible>    one assignment
STUDENT,<id>,<name>,<e1>,<b1>,<e2>,<b2>,...
                                one student, then earned/bonus pairs
```

Appendix D Section D.3 asks you to document decisions. **A file format is a promise to every future version of your program**, and an undocumented one is a promise nobody can keep.

---

## 15.9 Robust File Handling

Four rules, each from a real failure mode.

**Check that the file opened.** Report it clearly if not.

**Report the line number on any error.** `"Cannot read 'gradebook.csv' at line 14: expected a number."` is actionable. `"parse error"` is not.

**Decide what a malformed line means, and be consistent.** Two defensible policies: skip the bad line and carry on, or refuse the whole file. v2.2 skips and warns; Chapter 24's release build refuses, because a partly-loaded gradebook is worse than none.

**Never destroy existing data on a failed load.** Build the new gradebook in a separate variable and install it only on success. Loading a corrupt file should leave you with what you had, not with nothing.

---

## Common Errors and Warnings

| What you see or observe | Cause | Fix |
|---|---|---|
| The program reports an empty gradebook | The file did not open and nobody checked | Test `if (!in)` |
| `error: 'ifstream' was not declared` | Missing `#include <fstream>` | Add the header |
| Previous data vanished | Opening for output truncates | Check before overwriting |
| `terminate called after throwing 'std::invalid_argument'` | `stod` on non-numeric text | Wrap in `try`/`catch` |
| Only the first field is read | Used `>>` instead of `getline` with a delimiter | `std::getline(ss, field, ',')` |
| A name with a comma splits into two fields | Format restriction | Document it, or quote fields |
| Reading gets one extra empty record | Trailing newline at end of file | Skip empty lines |
| The file is written but is empty | Stream not flushed or closed | Let it go out of scope, or `close()` |
| `error: 'stod' was not declared` | Missing `#include <string>` | Add the header |

---

## Design Notes

**Check every file operation.** The failure mode is silence, which is worse than a crash.

**Report the line number.** Users cannot fix what they cannot find.

**Design formats to be readable and extensible.** Tags over positions.

**Build the replacement, then install it.** A failed load must leave the previous state untouched.

**Document the format, including its restrictions.** The commas-in-fields limitation is real; saying so is the honest choice.

---

## Grade Calculator v2.2 — Save and Load

### What v2.2 does

Everything v2.1 did, plus: the roster, the assignments, and the custom grade scale all persist to `gradebook.csv` and load automatically at startup. A menu-driven loop replaces the run-once flow.

**An instructor's custom grading scale now survives between sessions**, which is the feature that makes the calculator usable as an actual tool rather than a demonstration.

### Saving

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

### Loading

```cpp
bool loadGradebook(Gradebook& book, const std::string& filename, std::string& message) {
    std::ifstream in(filename);
    if (!in) {
        message = "No file named '" + filename + "' was found.";
        return false;
    }

    Gradebook loaded;              // build separately; install only on success
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
    book = loaded;                 // install, now that it is known good
    if (message.empty()) { message = "Loaded " + filename + "."; }
    return true;
}
```

### A saved file

```text
# Grade Calculator gradebook file, version 1
# Section tags allow new record types to be added later.
NEXTID,1002
TIER,90,A
TIER,80,B
TIER,70,C
TIER,60,D
TIER,0,F
ASSIGNMENT,Homework 1,10
STUDENT,1001,Ada,9,1
```

### Expected behavior

Add an assignment and a student, save, quit, and restart:

```text
=== GRADE CALCULATOR v2.2 (persistent) ===

Loaded gradebook.csv.

1) Add assignment  2) Add student  3) Report  4) Save  5) Quit
```

The report shows the student entered in the previous session.

### What to notice

**`Gradebook loaded;` then `book = loaded;`** — the whole reason for the temporary. A file that fails partway leaves `book` untouched. Assigning directly into `book` as you parse would leave a half-loaded gradebook if line 14 were malformed.

**Every record type is checked for field count** before its fields are used. `f.size() >= 3` before touching `f[2]` prevents an out-of-range access on a truncated line — Chapter 11's bounds lesson, applied to data from outside the program.

**Unrecognized tags produce a warning, not a failure.** That is what makes the format extensible, and it is the property Chapter 21 will test.

**A missing grade scale is repaired with the default.** A gradebook with no scale cannot assign letters at all, so a sensible default beats an unusable file — and the message says what happened.

**`catch (...)` catches everything.** That is a blunt instrument, appropriate here because any conversion failure means the same thing. Chapter 24 replaces it with specific exception types and better messages.

**Adding an assignment gives every existing student a zero score for it**, keeping `scores` the same length as `assignments`. That correspondence is exactly what Chapter 18's `Student` class will enforce rather than maintain by hand.

### Your StudySite Lab — Save and Load the Gradebook

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.2
- **Starting point:** The working Chapter 14 v2.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

#### Required work

1. Add file-stream support that saves the grade scale, assignments, and students to `gradebook.csv`.
2. Load `gradebook.csv` at startup when it exists.
3. Parse into temporary data and replace the active gradebook only after the complete file is valid.
4. Create `file-format.md` documenting every record type, field order, and the restriction on commas in text fields.
5. Add a menu option that saves to a different filename.


#### Verification

- A save-then-load round trip reproduces the same gradebook.
- A missing file is handled without a crash.
- A nonnumeric field, truncated student row, unknown tag, and missing grade tiers are each rejected.
- A failed load does not destroy the active in-memory data.

#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This avoids
   creating files with names such as `_imported` when the same path is already
   open.
3. Click **Load from GitHub**, select **grade-calculator-1437**, and click each source, header,
   or documentation file needed for this chapter. Confirm the editor shows the
   expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. For a
   multi-file program, keep every source and header file needed by the build
   open in the editor.
5. Click **Run**. Read compiler messages and program output in the embedded
   Terminal, and type program input there when prompted.
6. Fix every compiler error and warning, then complete the verification list.
7. Use the Tutor with the current code or Terminal output when you need help.

#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the editor.
   **Save to GitHub includes every open editor file**, so close scratch files
   and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **grade-calculator-1437** and the existing **main** branch.
4. Enter the commit message **Complete Chapter 15 Grade Calculator v2.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the new
   commit and expected files are present before leaving StudySite.

#### Complete when

- The verification list passes.
- **grade-calculator-1437** contains the Chapter 15 checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.


---

## Try It Yourself

### 1. Write and read a file

```cpp
#include <fstream>
#include <iostream>
#include <string>

int main() {
    {
        std::ofstream out("demo.txt");
        out << "first line\n";
        out << "second line\n";
    }   // the stream closes here

    std::ifstream in("demo.txt");
    if (!in) {
        std::cout << "could not open demo.txt\n";
        return 1;
    }
    std::string line;
    while (std::getline(in, line)) {
        std::cout << "read: " << line << "\n";
    }
    return 0;
}
```

**Expected output:**

```text
read: first line
read: second line
```

*Try:* Change the filename in the `ifstream` to something that does not exist. Confirm the check fires. Then remove the check and see what the program reports instead — that silence is the failure mode from Section 15.4.

### 2. Splitting a line into fields

```cpp
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

std::vector<std::string> splitCsv(const std::string& line) {
    std::vector<std::string> fields;
    std::istringstream in(line);
    std::string field;
    while (std::getline(in, field, ',')) { fields.push_back(field); }
    return fields;
}

int main() {
    std::vector<std::string> f = splitCsv("STUDENT,1001,Ada Lovelace,84,5");
    std::cout << "fields: " << f.size() << "\n";
    for (const std::string& s : f) { std::cout << "[" << s << "]\n"; }
    return 0;
}
```

**Expected output:**

```text
fields: 5
[STUDENT]
[1001]
[Ada Lovelace]
[84]
[5]
```

*Try:* Split `"STUDENT,1001,Lovelace, Ada,84"`. How many fields now? This is the restriction from Section 15.5 — see it happen.

### 3. Converting text safely

```cpp
#include <iostream>
#include <stdexcept>
#include <string>

int main() {
    std::cout << "stod(\"84.5\") = " << std::stod("84.5") << "\n";
    try {
        std::cout << std::stod("abc") << "\n";
    } catch (const std::invalid_argument&) {
        std::cout << "stod(\"abc\") threw invalid_argument\n";
    }
    return 0;
}
```

**Expected output:**

```text
stod("84.5") = 84.5
stod("abc") threw invalid_argument
```

*Try:* Remove the `try`/`catch` and rerun. The program terminates — that is an unhandled exception, and Chapter 24 explains what happened.

### 4. Building text in memory

```cpp
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

std::string formatGrade(double percentage) {
    std::ostringstream out;
    out << std::fixed << std::setprecision(1) << percentage << "%";
    return out.str();
}

int main() {
    std::cout << formatGrade(89.666) << "\n";
    std::cout << "[" << formatGrade(100.0) << "]\n";
    return 0;
}
```

**Expected output:**

```text
89.7%
[100.0%]
```

*Try:* Change it to pad the result to eight characters using `std::setw`.

### 5. A round trip

Write a program that saves three names and scores to a file, then reads them back and prints them. Confirm what comes out matches what went in.

Then, deliberately: edit the file by hand to remove a comma from one line. What does your program do? Make it report the line number rather than crashing or silently skipping.

### 6. Judge a format

Which of these gradebook formats is more extensible, and why? What breaks in the weaker one if a category and weight must be added to each assignment?

```text
Format A:
Ada,1001,84,100,5
Grace,1002,91,100,0

Format B:
STUDENT,1001,Ada
WORK,1001,Midterm,84,100,5
STUDENT,1002,Grace
WORK,1002,Midterm,91,100,0
```

### 7. Reason about files

- Why must you check whether a file opened, when a missing file produces no error message?
- Why build the loaded data in a temporary and assign it at the end?
- What is the advantage of a tag at the start of each line over fixed field positions?
- Why report the line number in a parse error?
- Your program writes `gradebook.csv` and a user opens it in a spreadsheet, edits it, and saves. What could go wrong, and what does that suggest about documenting the format?

---

## Summary

- A **stream** is a sequence of data flowing to or from somewhere. File streams use the same `<<` and `>>` as the console, which is what makes the abstraction valuable.
- `std::ofstream` writes; `std::ifstream` reads; both need `<fstream>`. **Opening for output empties the file immediately.**
- `while (std::getline(in, line))` is the standard idiom for reading a whole file.
- **Always check that a file opened.** The failure mode is silence — an empty result indistinguishable from an empty file.
- Split a line into fields with `std::istringstream` and `std::getline` with a **delimiter**.
- `std::stod` and `std::stoi` convert text to numbers and **throw** on bad input. A file is outside your program, so its contents must be validated.
- `std::ostringstream` builds formatted text in memory.
- Design formats to be **human-readable**, **line-oriented**, **self-describing**, and **extensible**. Tags beat fixed positions because unknown tags can be skipped.
- **Document the format, including its restrictions.**
- Build loaded data separately and install it only on success, so a failed load never destroys what you had.

---

## Key Terms

**delimiter** — the character separating fields in a line of text.

**file stream** — a stream connected to a file.

**ifstream** — an input file stream.

**ofstream** — an output file stream.

**parsing** — extracting structured values from text.

**persistence** — storing data so it survives after a program ends.

**stream state** — the flags recording whether a stream has failed or reached its end.

**stringstream** — a stream reading from or writing to a string in memory.

**tag** — a leading field identifying what kind of record a line holds.

**truncate** — to empty a file when opening it for output.

---

**Next:** Chapter 16 promotes debugging to a first-class skill. You will learn the symbolic debugger — breakpoints, stepping, watches, and the call stack — and then use it on a broken build of the Grade Calculator containing three seeded defects that are invisible on ordinary input. Grade Calculator v2.3.
