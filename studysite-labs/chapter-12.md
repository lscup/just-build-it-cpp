# Chapter 12 Lab — Complete the Dynamic Roster

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.3
- **Starting point:** The working Chapter 11 program and the Chapter 5 design document.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Replace fixed student, assignment, score, and grade-scale arrays with `std::vector`.
2. Allow any number of assignments and students.
3. Add the drop-lowest option. Remove both earned and possible points for the selected assignment.
4. Preserve validated input, custom grade scales, rounding, capping, and class reporting from the earlier checkpoints.
5. Keep the weighted-grading scope statement unchanged. Weighted grading belongs to COSC 1437.
6. Complete only the Chapter 12 code checkpoint here. Final-project documentation, finishing touches, and submission instructions will be provided separately.


## Verification

- The program handles more than 40 students.
- Drop-lowest arithmetic matches a hand calculation.
- No-student, no-assignment, zero-possible-points, invalid-scale, cutoff-boundary, bonus, and invalid-numeric-input cases behave correctly.
- The repository contains the complete working v1.3 code checkpoint and the project documents created in earlier chapters.

## StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1436F26-Grade-Calculator-YourLastName**, and click each source,
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
3. Select **COSC1436F26-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter 12 Grade Calculator v1.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1436F26-Grade-Calculator-YourLastName** contains the Chapter 12
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
