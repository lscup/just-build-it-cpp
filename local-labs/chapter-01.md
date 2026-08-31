# Chapter 01 Lab — Create the COSC 1436 Base Repository

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.0
- **Starting point:** No prior project files.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Use the private `COSC1436F26-Grade-Calculator-YourLastName` repository your instructor created for you and invited you to. Do not create your own repository. Use this one repository for every chapter through Chapter 12.
2. Create `README.md` from the supplied template. Replace only `[Your name]`.
3. Create `requirements.md` by copying the supplied requirements exactly. These are the approved project requirements; do not invent or rewrite them.
4. Commit both documents as the first checkpoint. C++ coding begins in Chapter 2.

## Supplied `README.md`

Copy this text and replace only `[Your name]`:

```markdown
# Grade Calculator

A cumulative C++ project for COSC 1436.

## Student

[Your name]

## Course

COSC 1436 — Programming Fundamentals

## Project plan

This single repository contains my Grade Calculator work for Chapters 1–12.
The Chapter 12 code checkpoint will be the foundation for the separately
assigned COSC 1436 final project.
```

## Supplied `requirements.md`

Copy this complete requirements document. Do not rewrite it.

```markdown
# Grade Calculator Requirements

## Purpose

The Grade Calculator is a console application that calculates and reports
points-based course grades for a class roster.

## Inputs

The program accepts:

- the student's name;
- a user-defined letter-grade scale;
- any number of assignments;
- each assignment's name and points possible;
- each student's points earned for every assignment, including bonus points;
- a choice to drop or keep each student's lowest assignment.

## Processing

The program:

1. totals each student's earned points and possible points;
2. adds bonus points to points earned, but not to points possible;
3. optionally removes both the earned and possible points for the student's
   lowest assignment;
4. calculates the percentage using floating-point division;
5. caps the reported percentage at 100%;
6. rounds the reported percentage to one decimal place;
7. assigns a letter grade using the scale entered by the user; and
8. calculates the class average.

## Output

The program displays:

- a Grade Calculator heading;
- the active letter-grade scale;
- each student's name, percentage to one decimal place, and letter grade;
- labeled totals where required; and
- the class average.

Output must be readable, consistently aligned, and understandable without
reading the source code.

## Validation and edge cases

The program must:

- reject nonnumeric input where a number is required;
- reject negative point values;
- avoid division by zero;
- handle an empty assignment list or roster without crashing;
- reject grade-scale cutoffs that are not entered from highest to lowest; and
- ensure the scale reaches a lowest tier at 0%.

## COSC 1436 scope

This calculator uses total points only.

**Out of scope for COSC 1436:** weighted-category grading, in which categories
such as exams and homework carry different percentages of the final grade.
Weighted grading is deferred to COSC 1437.

## Storage estimate

One assignment record contains:

- assignment name: 30 characters × 1 byte = 30 bytes;
- points earned: 8 bytes;
- points possible: 8 bytes; and
- bonus points: 8 bytes.

Estimated size of one assignment record:

30 + 8 + 8 + 8 = **54 bytes**

Estimated size for 30 students with 12 assignments each:

30 × 12 × 54 = **19,440 bytes**
```


## Verification

- StudySite can load from and save to the connected `COSC1436F26-Grade-Calculator-YourLastName` repository.
- `README.md` and `requirements.md` are both present.
- There is no `main.cpp` yet.

## Optional local workflow

1. Accept the GitHub invitation your instructor emailed you. It gives you
   access to **COSC1436F26-Grade-Calculator-YourLastName**, the private
   repository already created for you in the **lscup** organization, where
   *YourLastName* is your own last name. Do not create your own repository.
2. Copy the repository URL from GitHub and clone it in your own development
   environment:

   ```bash
   git clone <your-repository-url> COSC1436F26-Grade-Calculator-YourLastName
   cd COSC1436F26-Grade-Calculator-YourLastName
   ```

3. Create the two supplied documents in your local editor. Chapter 1 has no
   compile or run step.

## Save this checkpoint

```bash
git add .
git commit -m "Create COSC 1436 Grade Calculator base repository"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- The verification list passes in your local environment.
- The correct cumulative repository contains the Chapter 1 checkpoint.
- The commit is pushed to GitHub.
