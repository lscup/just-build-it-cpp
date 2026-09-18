# Chapter 17 Lab — Sort and Search the Roster

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.4
- **Starting point:** The working Chapter 16 v2.3 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Add a `StudentComparer` function-pointer type and three comparator
   functions — `byName`, `byId`, and `byPercentageDescending` — so one sort
   routine can serve every ordering the menu offers.
2. Add `selectionSort`, a selection-sort routine that sorts a
   `std::vector<Student>` in place using whichever comparator is passed to
   it.
3. Add `linearSearchById` and `binarySearchById`. Both search by student ID
   and both count their own comparisons through an `int&` output parameter,
   so the two techniques can be measured, not just trusted.
4. Add two new menu options and renumber `Quit`:
   - `6) Sort roster` — asks which key to sort by (name, percentage, or ID)
     and calls `selectionSort` with the matching comparator.
   - `7) Find by ID` — runs `linearSearchById` on the roster as it stands,
     then runs `binarySearchById` on a **sorted copy** of the roster (never
     the live one), and prints both comparison counts.
   - `Quit` moves from choice `6` to choice `8`.

Nothing from v2.3 is retired, renamed, or changed behaviorally — this
checkpoint is purely additive. The only things a returning user will notice
are the two-line menu (it no longer fits on one line) and that `Quit` is now
`8` instead of `6`.

## Build it: step by step

Each step below shows the actual code for that piece. Type it in as you go —
don't wait until the end to test. All of it goes after `runTests()` and
before `main()`.

### Step 1 — The comparator type and three comparator functions

A comparison function pointer lets one sort routine serve every ordering
instead of writing `sortByName`, `sortById`, and `sortByPercentage` as three
separate copies of the same loop.

```cpp
// A comparison function pointer lets one sort routine serve every ordering.
typedef bool (*StudentComparer)(const Student&, const Student&,
                               const std::vector<Assignment>&);

bool byName(const Student& a, const Student& b, const std::vector<Assignment>&) {
    return a.name < b.name;
}

bool byId(const Student& a, const Student& b, const std::vector<Assignment>&) {
    return a.id < b.id;
}

bool byPercentageDescending(const Student& a, const Student& b,
                            const std::vector<Assignment>& as) {
    return percentageOf(a, as) > percentageOf(b, as);
}
```

Each comparator answers one question: "does `a` come before `b`?" `byName`
and `byId` ignore the assignment list entirely (hence the unnamed third
parameter) because a name or an ID needs no calculation. `byPercentageDescending`
uses it, because a percentage has to be computed from scores — and it uses
`>` rather than `<` so that the *highest* percentage sorts first, matching
how a ranked list is normally read.

### Step 2 — `selectionSort`

```cpp
/**
 * Selection sort: repeatedly find the smallest remaining element and swap it
 * into place. Simple to trace by hand, which is why Chapter 17 starts here.
 * Comparisons: n(n-1)/2 regardless of the input order.
 */
void selectionSort(std::vector<Student>& roster,
                   const std::vector<Assignment>& as,
                   StudentComparer comesFirst) {
    for (std::size_t i = 0; i + 1 < roster.size(); ++i) {
        std::size_t best = i;
        for (std::size_t j = i + 1; j < roster.size(); ++j) {
            if (comesFirst(roster[j], roster[best], as)) { best = j; }
        }
        if (best != i) { std::swap(roster[i], roster[best]); }
    }
}
```

The outer loop fixes one position at a time; the inner loop scans everything
still unsorted to find what belongs there. That inner scan runs for every
position regardless of how the data already looked, so selection sort always
does the same amount of work: `n(n-1)/2` comparisons for `n` students, best
case and worst case alike — O(n²). It is never the fastest sort, but it is
the easiest to trace by hand, which is exactly why it is the one to learn
first. Passing in `comesFirst` is what lets the same function sort by name
one moment and by percentage the next — the sort logic never changes, only
which comparator it's handed.

### Step 3 — `linearSearchById` and `binarySearchById`

```cpp
/** Linear search: works on any order, examines up to n elements. */
int linearSearchById(const std::vector<Student>& roster, int id, int& comparisons) {
    comparisons = 0;
    for (std::size_t i = 0; i < roster.size(); ++i) {
        ++comparisons;
        if (roster[i].id == id) { return static_cast<int>(i); }
    }
    return -1;
}

/**
 * Binary search: requires the roster to be sorted by ID first.
 * That precondition is the whole trade-off - it is far faster, but only
 * if someone has paid the cost of sorting.
 */
int binarySearchById(const std::vector<Student>& roster, int id, int& comparisons) {
    comparisons = 0;
    int low = 0;
    int high = static_cast<int>(roster.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        ++comparisons;
        if (roster[mid].id == id)      { return mid; }
        else if (roster[mid].id < id)  { low = mid + 1; }
        else                           { high = mid - 1; }
    }
    return -1;
}
```

Linear search makes no assumption about ordering, so it can run on the
roster exactly as the user left it — worst case, it examines every student.
Binary search is faster (worst case around log₂n comparisons instead of n),
but only because it throws away half the remaining range on every step, and
that trick only works if the range is sorted by the field being searched.
Hand it unsorted data and it will confidently return the wrong answer, or
none at all. That precondition — sorted first, searched second — is the
entire trade-off this step is teaching, not just "a second way to search."

### Step 4 — Two new menu options, and `Quit` moves to `8`

The menu prompt grows to two lines and gains two entries before `Quit`:

```cpp
std::cout << "1) Add assignment  2) Add student  3) Report  4) Save\n"
             "5) Run tests  6) Sort roster  7) Find by ID  8) Quit\nChoice: ";
```

Insert these two branches immediately before the old `Quit` branch, and
renumber that branch from `'6'` to `'8'`:

```cpp
} else if (choice == '6') {
    std::cout << "  Sort by: 1) name  2) percentage  3) ID\n  Choice: ";
    std::string s;
    std::getline(std::cin, s);
    StudentComparer cmp = byName;
    if (!s.empty() && s[0] == '2')      { cmp = byPercentageDescending; }
    else if (!s.empty() && s[0] == '3') { cmp = byId; }
    selectionSort(book.roster, book.assignments, cmp);
    std::cout << "  Roster sorted.\n\n";
} else if (choice == '7') {
    std::cout << "  Student ID: ";
    std::string s;
    std::getline(std::cin, s);
    int id = 0;
    try { id = std::stoi(s); }
    catch (...) { std::cout << "  Not a valid ID.\n\n"; continue; }

    int linearCost = 0;
    int found = linearSearchById(book.roster, id, linearCost);

    // Binary search needs sorted data, so sort a copy first.
    std::vector<Student> sorted = book.roster;
    selectionSort(sorted, book.assignments, byId);
    int binaryCost = 0;
    binarySearchById(sorted, id, binaryCost);

    if (found >= 0) {
        std::cout << "  Found: " << book.roster[found].name << " ("
                  << percentageOf(book.roster[found], book.assignments) << "%)\n";
    } else {
        std::cout << "  No student with ID " << id << ".\n";
    }
    std::cout << "  Comparisons - linear: " << linearCost
              << ", binary: " << binaryCost << "\n\n";
} else if (choice == '8') {
    running = false;
```

Look closely at option `7`: it builds `std::vector<Student> sorted = book.roster;`
and sorts *that copy* by ID, leaving `book.roster` exactly as the user left
it. This is deliberate. If binary search sorted the live roster as a side
effect, "Find by ID" would silently reorder the class list every time it
ran — a search should never rearrange the thing it searches. Copying first
means the roster the user sees in the next report is unaffected by whatever
order they last searched in, and it lets the linear search (on the original
order) and the binary search (on the sorted copy) be timed fairly against
each other on the same underlying data. Finally, update the fallback error
message from `"  Please enter 1-6.\n\n"` to `"  Please enter 1-8.\n\n"` to
match the new range of choices.

## Verification

- Sorting by name, by percentage, and by ID each produce a correctly ordered
  roster — check at least five students per order.
- Searching for an ID that exists on the roster finds the right student by
  both linear and binary search; searching for an ID that does not exist
  reports "not found" from both.
- The printed comparison counts are sane: binary search's count should
  generally be lower than linear search's on a roster of any real size, and
  binary search must never report *more* comparisons than linear search's
  worst case for the same target.
- After a sort-then-search round trip, `3) Report` still shows every
  student's correct percentage and letter grade — sorting rearranges the
  roster, it must never corrupt or drop a student's data.

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
4. Work through Steps 1–4 above in StudySite's internal editor, in order.
   Add Steps 1–3 first and click **Run** — the file should still compile
   even though `main` hasn't changed yet. Then apply Step 4 and click
   **Run** again.
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
   editor. **Save to GitHub includes every open editor file**, so close
   scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 17 Grade Calculator v2.4**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter 17
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
