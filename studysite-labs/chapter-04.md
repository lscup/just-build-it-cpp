# Chapter 04 Lab — Calculate Percentage and Bonus

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.3
- **Starting point:** The working Chapter 3 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Calculate `(points earned + bonus points) / points possible * 100.0` using floating-point arithmetic.
2. Guard against points possible being zero before dividing.
3. Display the percentage to one decimal place.
4. Keep the percentage uncapped in this checkpoint and document that policy in a comment.


## Verification

- `84 / 100` with `5` bonus reports `89.0%`.
- `10 / 10` with `5` bonus reports `150.0%`.
- Zero points possible produces an explanation instead of a division error.

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
4. Enter the commit message **Complete Chapter 4 Grade Calculator v0.3**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1436F26-Grade-Calculator-YourLastName** contains the Chapter 4
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
