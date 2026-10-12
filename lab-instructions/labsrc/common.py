from engine import Md, LOCAL_SUBS


def header(title, version, start):
    return Md(f"""
### Your StudySite Lab — {title}

- **Course:** COSC 1437 — Object-Oriented Programming
- **Project checkpoint:** {version}
- **Starting point:** {start}

> **One-repository rule:** Continue in the same COSC 1437 Grade Calculator
> repository from Chapter 13 through Chapter 24. Do not create a chapter folder
> or a new repository. The supplied Chapter 12 solution is the foundation;
> your COSC 1437 work is what you add in Chapters 13–24.
""")


HOW_TO_READ = Md("""
#### How to use these steps

This lab is a guided exercise, not a test. Each step tells you **which file**
to open, shows the **exact code to find**, and shows the **exact code to put in
its place**. Work through the steps in order and copy the code from the boxes
rather than retyping it where you can.

- A **find** box shows code exactly as it appears in your program at the end
  of the previous chapter. Use the editor's search to locate it. If you cannot
  find it, your program differs from the previous checkpoint — compare it with
  your last commit on GitHub, or ask the Tutor to help you line it up, before
  going further.
- A **▶ Run checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.
""")


def workflow(files_sentence, steps_sentence):
    return Md(f"""
#### StudySite workflow

1. Confirm that your previous chapter is committed on GitHub, then open this
   chapter's **coding panel on the StudySite main stage**.
2. Close stale project tabs from an earlier session before loading. This
   avoids creating files with names such as `_imported` when the same path
   is already open.
3. Click **Load from GitHub**, select
   **COSC1437xxx-Grade-Calculator-YourLastName**, and click {files_sentence}
   Confirm the editor shows the expected file paths before editing.
4. {steps_sentence}
5. Read compiler messages and program output in the embedded Terminal, and
   type program input there when prompted. Fix every compiler error and
   warning before moving past a Run checkpoint.
6. Complete the **Check your work** list.
7. Use the Tutor with the current code or Terminal output when you need
   help.
""")


def save(chapter, version, files_note):
    return Md(f"""
#### Save this checkpoint

> **IMPORTANT — commit to save your work:** StudySite autosaves editor tabs
> locally on this device, but local autosave is not a durable GitHub backup.
> Your work is not safely saved in your repository until **Save to GitHub**
> finishes a successful **Commit**.

1. Keep every project file that belongs in this checkpoint open in the
   editor — {files_note} **Save to GitHub includes every open editor file**,
   so close scratch files and accidental `_imported` duplicates first.
2. Click **Save to GitHub**.
3. Select **COSC1437xxx-Grade-Calculator-YourLastName** and the existing
   **main** branch.
4. Enter the commit message **Complete Chapter {chapter} Grade Calculator {version}**.
5. Click **Commit** and wait for StudySite's confirmation.
6. Open the commit link, or open the repository on GitHub, and confirm the
   new commit and expected files are present before leaving StudySite.

#### Complete when

- Every item in **Check your work** passes.
- **COSC1437xxx-Grade-Calculator-YourLastName** contains the Chapter {chapter}
  checkpoint.
- The GitHub commit is visible; StudySite's local autosave alone is not
  completion.
""")


HOW_TO_READ.local_text = HOW_TO_READ.text.replace(
    "your last commit on GitHub, or ask the Tutor to help you line it up, before\n  going further.",
    "your last commit on GitHub before going further.").replace(
    "**▶ Run checkpoint**", "**▶ Build checkpoint**")

_workflow_studysite = workflow


def workflow(files_sentence, steps_sentence):
    m = _workflow_studysite(files_sentence, steps_sentence)
    local_steps = (steps_sentence.replace("StudySite's internal editor", "your local editor")
                   .replace("click **Run** at the ▶ Run checkpoint", "build and run at the ▶ Build checkpoint")
                   .replace("clicking **Run** at each ▶ Run checkpoint", "building and running at each ▶ Build checkpoint")
                   .replace("Click **Run** at the ▶ Run checkpoint", "Build and run at the ▶ Build checkpoint")
                   .replace("Keep every file open, and click **Run** at the ▶ Run checkpoint",
                            "Build and run at the ▶ Build checkpoint"))
    m.local_text = f"""
#### Optional local workflow

These commands assume macOS, Linux, or WSL with a C++17-capable `g++`
toolchain. An equivalent local C++17 environment is acceptable.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. {local_steps}
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```
""".strip("\n") + "\n"
    return m


_save_studysite = save


def save(chapter, version, files_note):
    m = _save_studysite(chapter, version, files_note)
    m.local_text = f"""
#### Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter {chapter} Grade Calculator {version}"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

#### Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter {chapter} checkpoint.
- The commit is pushed to GitHub.
""".strip("\n") + "\n"
    return m


LOCAL_SUBS.extend([
    ("finish the steps in order, then Run.", "finish the steps in order, then build."),
    ("Do **not** click Run until the checkpoint", "Do **not** build until the checkpoint"),
    ("type the inputs below in the Terminal", "type the inputs below in your terminal"),
    ("Work through this test plan in the Terminal.", "Work through this test plan in your terminal."),
    ("Click **Run** again: the program should print", "Run `./gradecalc` again: the program should print"),
    ("3. Click **Run**. Choose a scheme", "3. Rebuild and run the program. Choose a scheme"),
    ("""> **Note — this is the one check StudySite's Run cannot make for you.** A leak
> is invisible from the program's output. If you have a local C++ toolchain,
> build the program with `-fsanitize=address -g` and repeat the experiment:
> AddressSanitizer reports the leaked allocations when the program exits.
> Otherwise, ask your instructor which memory check to use.""",
     """> **Note — a leak is invisible from the program's output.** Build the
> program with `-fsanitize=address -g` and repeat the experiment:
> AddressSanitizer reports the leaked allocations when the program exits.
>
> ```bash
> g++ -std=c++17 -Wall -Wextra -fsanitize=address -g *.cpp -o gradecalc
> ```"""),
    ("""Every one of them must
be open in the StudySite editor when you click **Run** — a `.cpp` file that is
not open is not compiled, and the linker error you get names the missing
function, not the missing tab.""",
     """Every `.cpp` file must be
part of the build; the `*.cpp` in the build command takes care of that."""),
    ("""> **How to create a file:** in the StudySite editor, create a new file with
> the exact name shown (spelling and lowercase matter, because `#include`
> lines refer to these names). Keep each new file open after you create it.""",
     """> **How to create a file:** create each new file in the same folder as
> `main.cpp`, with the exact name shown (spelling and lowercase matter,
> because `#include` lines refer to these names)."""),
    (""", and all of them must
be open in the editor when you click **Run**.""", "."),
])
