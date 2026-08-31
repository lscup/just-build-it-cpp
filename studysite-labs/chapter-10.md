# Chapter 10 Lab — Organize Reusable Functions

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v1.1
- **Starting point:** The working Chapter 9 program.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## Required work

1. Move reusable declarations to `gradelib.h` and definitions to `gradelib.cpp`; keep application flow in `main.cpp`.
2. Add an include guard to `gradelib.h`.
3. Add validated numeric input that recovers after invalid text.
4. Pass output values by reference where a function must update the caller.
5. Add `readInRange` and use it to keep points possible between `0` and `1000`.


## Verification

- All source files build together.
- Typing `abc` for a number does not trap the program in a loop or crash it.
- The existing menu and grade calculations still work.

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
4. Enter the commit message **Complete Chapter 10 Grade Calculator v1.1**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

## Complete when

- The verification list passes.
- **COSC1436F26-Grade-Calculator-YourLastName** contains the Chapter 10
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
