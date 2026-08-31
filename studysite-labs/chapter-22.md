# Chapter 22 Lab — Replace Manual Ownership with Smart Pointers

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** v3.2
- **Starting point:** The working Chapter 21 v3.1 program.

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.

## Required work

1. Confirm the correct v3.1 program switches schemes and exits normally.
2. Temporarily remove the manual delete in `setScheme` and observe the memory-safety failure using the available memory check; then restore it.
3. Replace the raw owning scheme pointer with `std::unique_ptr<GradingScheme>`.
4. Remove the manual destructor, manual delete, and explicitly deleted copy operations that unique ownership now handles.
5. Keep all grading behavior unchanged.


## Verification

- The intentional raw-pointer defect is detected by a memory-safety check.
- The final smart-pointer version reports no leak.
- Copying a Gradebook is rejected by the type system.
- All three grading schemes still produce the Chapter 21 results.

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

For Chapter 22, **Run** verifies normal program behavior. Use the optional
local-development instructions for the required AddressSanitizer check, then
return to this coding panel for the final edit, normal run, and GitHub commit.

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
4. Enter the commit message **Complete Chapter 22 Grade Calculator v3.2**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1437F26-Grade-Calculator-YourLastName** contains the Chapter 22
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
