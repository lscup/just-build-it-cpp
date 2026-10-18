# Chapter 02 Lab — Hello, Gradebook

- **Course:** COSC 1436 — Programming Fundamentals
- **Project checkpoint:** v0.1
- **Starting point:** Your Chapter 1 repository, containing `README.md` and `requirements.md` and no C++ code yet.

> **One-repository rule:** Continue in the same COSC 1436 Grade Calculator
> repository through Chapter 12. Do not create a chapter folder or a new
> repository. Each chapter replaces or extends the current working program.

## What you will build

This is the first code checkpoint. The program you write here does one thing —
it prints the Grade Calculator banner and exits — and that is the point. Before
any grading logic exists, you confirm that the whole toolchain works end to
end: you can create a source file, the compiler accepts it, the program runs,
and you can commit the result to GitHub. Every later chapter adds to this same
file. By the end you will have:

1. A new file `main.cpp` containing a complete, minimal C++ program: a
   comment header, `#include <iostream>`, an `int main()` function, and
   `return 0;`.
2. A five-line banner printed with `std::cout`, naming the application, its
   version, and the course.
3. A program that compiles with no errors and no warnings, and exits normally.

## Files in this checkpoint

| File | What you do to it |
|---|---|
| `main.cpp` | Create (Steps 1-3) |
| `README.md`, `requirements.md` | **No change** — keep them in the repository |

When you are finished your project has **one** `.cpp` file.

## How to use these steps

This lab is a guided exercise, not a test. Each step tells you **which file**
to open, shows the **exact code to find**, and shows the **exact code to put in
its place**. Work through the steps in order and copy the code from the boxes
rather than retyping it where you can.

- A **find** box shows code exactly as it appears in your program at the end
  of the previous chapter. Use the editor's search to locate it. If you cannot
  find it, your program differs from the previous checkpoint — compare it with
  your last commit on GitHub before going further.
- A **▶ Build checkpoint** marks a point where the program should build and run
  again. Between checkpoints the program may not compile; that is expected.
- Each step ends with a short explanation of *why*. Read it — it is the
  chapter's concept, applied to your own program.

## Optional local workflow

Build and run this chapter's program with the command for your platform:

**macOS** (Terminal, with the Xcode command-line tools — Appendix A.5):

```bash
clang++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
./gradecalc
```

**Windows** (PowerShell, with MSYS2's `g++` on your PATH — Appendix A.5):

```powershell
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc.exe
.\gradecalc.exe
```

The ▶ Build checkpoints below use `g++ -std=c++17 -Wall -Wextra *.cpp -o
gradecalc`, which works as written on macOS, Linux, and WSL. On Windows, use
the Windows command above instead.

1. Open your existing local clone and synchronize it:

   ```bash
   git pull --ff-only
   ```

2. Create the new file in your local editor, finish the steps in order, then build.
3. Fix every compiler error and warning before moving past a Build
   checkpoint.
4. Run the program and complete the **Check your work** list:

   ```bash
   ./gradecalc
   ```

## Step 1 — Create `main.cpp` with the program skeleton

> **How to create a file:** create each new file in the same folder as
> `main.cpp`, with the exact name shown (spelling and lowercase matter,
> because `#include` lines refer to these names).

Create a new file named `main.cpp` and enter this code:

```cpp
// Grade Calculator v0.1 - Chapter 2
// Prints the application banner. Confirms the toolchain works end to end.
// Build: g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc

#include <iostream>

int main() {
    return 0;
}
```

**Why:** Every C++ program needs exactly one `main` function — that is where
execution begins. `#include <iostream>` brings in the output facilities you
need in the next step; without it the compiler does not know what `std::cout`
is. `return 0;` tells the operating system the program finished normally. The
comment header at the top records what this version of the program does and
how to build it, and you will update it in every chapter.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should compile and exit immediately without printing anything. An empty result is the correct result here — it proves the toolchain works before any output exists to distract you. If you get a compiler error, re-check the braces and the semicolon after `return 0`.

## Step 2 — Print the banner

In `main.cpp`, find this line:

```cpp
int main() {
```

Directly below it, add:

```cpp
    std::cout << "===================================\n";
    std::cout << "        GRADE CALCULATOR           \n";
    std::cout << "        Version 0.1                \n";
    std::cout << "===================================\n";
```

**Why:** `std::cout` is the standard output stream, and `<<` sends each value
to it in turn. The `\n` at the end of each string is the newline character; it
moves output to the next line. Without it every line would run together. Note
that the banner lines are printed in the order you write them — output is
sequential, top to bottom, which is the single most important thing to
internalize about how a program executes.

## Step 3 — Add the course line

In `main.cpp`, find these two lines — the version line and the closing rule below it:

```cpp
    std::cout << "        Version 0.1                \n";
    std::cout << "===================================\n";
```

Directly below it, add:

```cpp
    std::cout << "Course: Programming Fundamentals\n";
```

**Why:** This line sits after the closing rule rather than inside the banner
box, so the box stays a fixed five lines wide while the text below it can grow
in later chapters. Keeping decoration and content separate is a habit worth
starting now.

> **▶ Build checkpoint:** Rebuild and run the program:
>
> ```bash
> g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
> ./gradecalc
> ```
>
> The program should print the full banner followed by the course line, then exit. Compare your output character by character with the expected output below — the `=` rules are 35 characters wide.

## Expected output

```text
===================================
        GRADE CALCULATOR
        Version 0.1
===================================
Course: Programming Fundamentals
```

The two centred lines are padded with spaces inside the string literal, so
they sit under the middle of the rules. If your banner looks ragged, count the
spaces in the find boxes above.

## Check your work

Then confirm:

- [ ] `main.cpp` compiles with no errors and **no warnings**.
- [ ] The program prints exactly five banner lines and one course line.
- [ ] The two rule lines are the same length as each other.
- [ ] The program exits normally, with no input required.
- [ ] `README.md` and `requirements.md` are still in the repository,
      unchanged.

## Save this checkpoint

```bash
git add .
git commit -m "Complete Chapter 2 Grade Calculator v0.1"
git push
```

Confirm the new commit appears in the correct repository on GitHub.

## Complete when

- Every item in **Check your work** passes in your local environment.
- The correct cumulative repository contains the Chapter 2 checkpoint.
- The commit is pushed to GitHub.
