# Chapter 21 Lab — Select Schemes with Polymorphism

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.1
- **Starting point:** The working Chapter 20 v3.0 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Make `GradingScheme::computePercentage` pure virtual and add a virtual destructor.
2. Have `Gradebook` own a base-class scheme pointer and delegate calculations through it.
3. Allow the user to switch schemes without restarting or re-entering data.
4. Add `WeightedDropLowest` as a third scheme without editing Student, Assignment, GradeScale, or report formatting.
5. Extend the Chapter 15 file format so category names and weights persist.


## Verification

- With Exam 1 at 90/100, Homework 1 at 10/10, Homework 2 at 5/10, and category weights of 50 and 30, the three schemes report 87.5%, 84.4%, and 93.8%.
- Switching schemes immediately recomputes reports.
- The grade calculation contains no type-selection branch.
- Saving and loading preserves categories and weights.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437F26-Grade-Calculator-YourLastName**, and click each source,
   header, or documentation file needed for this chapter. Confirm the editor
   shows the expected file paths before editing.
4. Continue the existing project in StudySite's internal editor. For a
   multi-file program, keep every source and header file needed by the build
   open in the editor.
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
3. Select **COSC1437F26-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 21 Grade Calculator v3.1**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437F26-Grade-Calculator-YourLastName** contains the Chapter 21
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
