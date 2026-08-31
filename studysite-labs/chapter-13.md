# Chapter 13 Lab — Establish the COSC 1437 Baseline

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v2.0
- **Starting point:** The private `COSC1437F26-Grade-Calculator-YourLastName` repository your instructor created for you in the `lscup` organization and invited you to, and the complete Chapter 12 v1.3 solution supplied in this lab.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Create `main.cpp` with the complete supplied Chapter 12 starter code before making Chapter 13 changes.
2. Run the starter unchanged and confirm the complete points-based Grade Calculator works.
3. Create `maintenance-plan.md` identifying the coding-standard cleanup, behavior-preservation plan, test evidence, and weighted-grading requirement deferred to Chapters 20–21.
4. Bring the code into conformance with the Appendix D coding standard without changing its existing grade calculations.
5. Add an About menu option that identifies the application, version, course, and author.
6. Keep all Chapter 13–24 work in this same COSC 1437 repository.


## Complete Chapter 12 starter code

Create `main.cpp` in the StudySite coding panel with the complete code below. Run this starter unchanged before beginning the Chapter 13 changes.

```cpp
// Grade Calculator v1.3 - Chapter 12 - COURSE I FINAL
// Unlimited roster, assignments, and grade tiers using std::vector.
// New this version: std::vector replaces fixed arrays, drop-lowest feature.
//
// Complete Course I feature set: named assignments, bonus points, custom
// letter scale, multi-student roster, class statistics, drop lowest.
// Grading model: points-based only. Weighted grading arrives in Chapter 20.
//
// Run: click Run in StudySite and use the embedded Terminal.

#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

const bool CAP_AT_100 = true;

// ---------- input helpers ----------

double readNonNegative(const std::string& prompt) {
    double value = 0.0;
    while (true) {
        std::cout << prompt;
        if (!(std::cin >> value)) {
            if (std::cin.eof()) { return 0.0; }
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cout << "  That is not a number. Please try again.\n";
            continue;
        }
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        if (value < 0.0) {
            std::cout << "  Value cannot be negative. Please try again.\n";
            continue;
        }
        return value;
    }
}

std::string readLine(const std::string& prompt) {
    std::cout << prompt;
    std::string line;
    std::getline(std::cin, line);
    return line;
}

bool readYesNo(const std::string& prompt) {
    std::string answer = readLine(prompt);
    return !answer.empty() && (answer[0] == 'y' || answer[0] == 'Y');
}

// ---------- grade scale ----------

std::vector<double> gradeCutoffs;
std::vector<char> gradeLetters;

void useDefaultScale() {
    gradeCutoffs = {90.0, 80.0, 70.0, 60.0, 0.0};
    gradeLetters = {'A', 'B', 'C', 'D', 'F'};
}

void readGradeScale() {
    gradeCutoffs.clear();
    gradeLetters.clear();
    std::cout << "\n--- Define your grade scale ---\n";
    std::cout << "Enter tiers highest first. Type 'done' to finish.\n\n";

    while (true) {
        std::string letterText = readLine("Tier letter (or 'done'): ");
        if (letterText == "done" || letterText.empty()) { break; }
        double cutoff = readNonNegative("  Minimum percentage: ");
        if (!gradeCutoffs.empty() && cutoff >= gradeCutoffs.back()) {
            std::cout << "  Cutoff must be lower than " << gradeCutoffs.back()
                      << ". Tier not added.\n";
            continue;
        }
        gradeLetters.push_back(letterText[0]);
        gradeCutoffs.push_back(cutoff);
    }

    if (gradeCutoffs.empty() || gradeCutoffs.back() > 0.0) {
        std::cout << "Note: scale did not reach 0, so an 'F' at 0 was added.\n";
        gradeLetters.push_back('F');
        gradeCutoffs.push_back(0.0);
    }
}

char letterFor(double percentage) {
    for (std::size_t i = 0; i < gradeCutoffs.size(); ++i) {
        if (percentage >= gradeCutoffs[i]) { return gradeLetters[i]; }
    }
    return '?';
}

double computePercentage(double earned, double possible) {
    if (possible <= 0.0) { return 0.0; }
    double raw = earned / possible * 100.0;
    double reported = CAP_AT_100 ? std::min(raw, 100.0) : raw;
    return std::round(reported * 10.0) / 10.0;
}

int main() {
    std::cout << "=== GRADE CALCULATOR v1.3 ===\n";
    std::cout << "    Course I final version\n\n";

    if (readYesNo("Define a custom grade scale? (y/n): ")) {
        readGradeScale();
    } else {
        useDefaultScale();
        std::cout << "Using default scale: A 90, B 80, C 70, D 60, F 0.\n";
    }

    // Assignments: name and points possible, any number of them.
    std::vector<std::string> assignmentNames;
    std::vector<double> pointsPossible;

    std::cout << "\n--- Enter assignments ---\n";
    while (true) {
        std::string name = readLine("Assignment name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        assignmentNames.push_back(name);
        pointsPossible.push_back(readNonNegative("  Points possible: "));
    }

    // Students: name plus one earned-points entry per assignment.
    std::vector<std::string> studentNames;
    std::vector<std::vector<double>> earned;

    std::cout << "\n--- Enter students ---\n";
    while (true) {
        std::string name = readLine("Student name (or 'done'): ");
        if (name == "done" || name.empty()) { break; }
        studentNames.push_back(name);

        std::vector<double> row;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            row.push_back(readNonNegative("  " + assignmentNames[a] + " points (incl. bonus): "));
        }
        earned.push_back(row);
    }

    bool dropLowest = false;
    if (assignmentNames.size() > 1) {
        dropLowest = readYesNo("\nDrop each student's lowest assignment? (y/n): ");
    }

    std::cout << "\n=====================================\n";
    std::cout << "  CLASS REPORT\n";
    std::cout << "=====================================\n";
    std::cout << std::fixed << std::setprecision(1);

    double classTotal = 0.0;
    for (std::size_t s = 0; s < studentNames.size(); ++s) {
        double totalEarned = 0.0;
        double totalPossible = 0.0;
        for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
            totalEarned += earned[s][a];
            totalPossible += pointsPossible[a];
        }

        // Dropping in a points-based scheme removes BOTH the earned points and
        // the possible points. Removing only one would distort the result.
        if (dropLowest && !assignmentNames.empty()) {
            std::size_t worst = 0;
            double worstRatio = 2.0;
            for (std::size_t a = 0; a < assignmentNames.size(); ++a) {
                if (pointsPossible[a] <= 0.0) { continue; }
                double ratio = earned[s][a] / pointsPossible[a];
                if (ratio < worstRatio) { worstRatio = ratio; worst = a; }
            }
            if (worstRatio <= 1.0) {
                totalEarned -= earned[s][worst];
                totalPossible -= pointsPossible[worst];
            }
        }

        double pct = computePercentage(totalEarned, totalPossible);
        classTotal += pct;
        std::cout << std::left << std::setw(20) << studentNames[s]
                  << std::right << std::setw(8) << pct << "%   "
                  << letterFor(pct) << "\n";
    }

    if (!studentNames.empty()) {
        std::cout << "-------------------------------------\n";
        std::cout << std::left << std::setw(20) << "CLASS AVERAGE"
                  << std::right << std::setw(8)
                  << classTotal / studentNames.size() << "%\n";
    } else {
        std::cout << "No students entered.\n";
    }
    return 0;
}
```


## Verification

- The supplied v1.3 starter runs before refactoring.
- The same input produces the same grade before and after the coding-standard pass.
- The About option works and returns to the menu.
- `maintenance-plan.md` includes the deferred weighted-grading analysis.

## StudySite workflow

1. Accept the GitHub invitation your instructor emailed you. It gives you
   access to **COSC1437F26-Grade-Calculator-YourLastName**, the private
   repository already created for you in the **lscup** organization, where
   *YourLastName* is your own last name. Do not create your own repository,
   and do not continue Chapter 13 in the COSC 1436 repository.
2. In StudySite, open this chapter's **coding panel on the main stage**.
3. Click **Load from GitHub**. Connect GitHub if prompted, select
   **COSC1437F26-Grade-Calculator-YourLastName**, and click `README.md` to
   load it into the editor.
4. Create `main.cpp` with the complete Chapter 12 starter code supplied in
   this lab. Click **Run**, read the output in the embedded Terminal, and
   confirm the unchanged v1.3 program works.
5. Save this untouched baseline first: click **Save to GitHub**, select
   **COSC1437F26-Grade-Calculator-YourLastName** and **main**, enter **Add
   Chapter 12 starter for COSC 1437**, and click **Commit**. Confirm the
   commit succeeds.
6. Complete the Chapter 13 changes in the same coding panel. Keep every
   source, header, and documentation file needed for this checkpoint open.
7. Click **Run** again. Fix every compiler error and warning, then complete
   the verification list.
8. Use the Tutor with the current code or Terminal output when you need
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
3. Select **COSC1437F26-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 13 Grade Calculator v2.0**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437F26-Grade-Calculator-YourLastName** contains the Chapter 13
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
