# Appendix A — Setting Up Your Development Environment

Every program in this book runs unchanged in either environment below. Neither requires anything to be purchased, and the first requires nothing to be installed.

**All instructions here are numbered text steps.** Where a screenshot would normally appear, the step names the menu, button, or command by its label instead, so the procedure can be followed by reading alone.

---

## A.1 What This Book Requires

| Requirement | Detail |
|---|---|
| Compiler | Any supporting **C++17** — g++ 9 or later, clang 10 or later |
| Libraries | **The standard library only.** Nothing to install |
| Build system | **None.** Every program builds with one command |
| Terminal | Needed for the debugger in Chapter 16 and the sanitizer in Chapter 22 |

The compile command used throughout:

```text
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
```

For multi-file versions, from Chapter 10 onward:

```text
g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
```

---

## A.2 Option 1 — The StudySite.ai Editor

The fastest way to work through the reading and the Try It Yourself examples. Nothing to install and nothing to configure.

1. Open the chapter you are working on in StudySite.
2. Open the code editor panel.
3. Type your program into the editor. **Type it rather than pasting it** — Chapter 2 Section 2.5 explains why this matters early on.
4. Run it using the editor's Run control. Compilation and execution happen together.
5. Type any input the program prompts for into the terminal panel.

**Suits:** reading, experimenting, the Try It Yourself examples, and every single-file program in Chapters 2 through 9.

**Does not suit:** the symbolic debugger in Chapter 16, or AddressSanitizer in Chapter 22. Both need a full toolchain — use Option 2 for those.

---

## A.3 Option 2 — GitHub Codespaces

A complete Linux machine running in your browser, with VS Code, g++, the debugger, and a real terminal. This is the environment Chapter 16 and Chapter 22 assume.

### First-time setup

1. Create a free account at `github.com` if you do not have one.
2. Create a new repository for your coursework. Name it something like `cpp-gradecalculator`. Tick **Add a README file** so the repository is not empty.
3. On the repository page, select the green **Code** button.
4. Choose the **Codespaces** tab, then **Create codespace on main**.
5. Wait for the codespace to build. The first time takes a few minutes; later starts are quick.

VS Code opens in your browser with a file explorer on the left, an editor in the centre, and a panel at the bottom for the terminal.

### Confirm the toolchain works

1. Open a terminal: **Terminal → New Terminal** from the menu bar.
2. Type:

   ```text
   g++ --version
   ```

3. You should see a version number. Anything from **g++ 9** onward supports everything in this book.

If that command reports "not found", the codespace has not finished building. Wait and try again.

### Create and run your first program

1. In the file explorer, select the **New File** icon and name the file `main.cpp`.
2. Type the program from Chapter 2 Section 2.1.
3. In the terminal:

   ```text
   g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
   ./gradecalc
   ```

4. **If compilation succeeded, nothing is printed.** Silence means success — Chapter 2 Section 2.5.

### Saving your work

Codespaces keeps your files, but commit regularly so the work is in your repository:

```text
git add .
git commit -m "Grade Calculator v0.1 - first running program"
git push
```

Chapter 13 Section 13.6 explains why the commit history matters, and the capstone in Chapter 24 asks for it.

---

## A.4 Setting Up the Debugger

Chapter 16 needs this. Do it once, in Codespaces.

### Install the C++ extension

1. Select the **Extensions** icon in the left sidebar.
2. Search for `C/C++`.
3. Install the extension published by Microsoft.

### Create a launch configuration

1. Select the **Run and Debug** icon in the left sidebar.
2. Select **create a launch.json file**.
3. Choose **C++ (GDB/LLDB)**, then **g++ - Build and debug active file**.

VS Code creates `.vscode/launch.json` and `.vscode/tasks.json`.

### Make the build include debug information

Open `.vscode/tasks.json` and confirm the `args` list includes `-g`, `-std=c++17`, `-Wall`, and `-Wextra`. Add any that are missing:

```text
"args": [
    "-fdiagnostics-color=always",
    "-g",
    "-std=c++17",
    "-Wall",
    "-Wextra",
    "${file}",
    "-o",
    "${fileDirname}/${fileBasenameNoExtension}"
]
```

**Without `-g` the debugger cannot show your variable names or line numbers** — Chapter 16 Section 16.3.

### For multi-file programs

From Chapter 10 onward your program has several `.cpp` files. Replace `"${file}"` in that list with:

```text
"${fileDirname}/*.cpp",
```

and change the output name to something fixed, such as `"${fileDirname}/gradecalc"`.

### Confirm the debugger works

1. Open `main.cpp`.
2. Click in the narrow gutter immediately left of a line number inside `main`. A red dot appears — that is a breakpoint.
3. Press **F5**.
4. The program builds, starts, and pauses at the red dot. The **Variables** panel on the left shows your local variables, and the **Call Stack** panel shows how execution reached that line.

If it pauses and shows your variables by name, you are set up for Chapter 16.

---

## A.5 Option 3 — VS Code on Your Own Computer

If you prefer to work offline. The debugger instructions in Chapter 16 apply identically, since Codespaces *is* VS Code.

### Windows

1. Install **VS Code** from `code.visualstudio.com`.
2. Install a compiler. The simplest route is **MSYS2** from `msys2.org`. After installing, open the MSYS2 terminal and run:

   ```text
   pacman -S mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-gdb
   ```

3. Add the compiler to your PATH. The directory is typically `C:\msys64\ucrt64\bin`.
4. Open a new terminal and confirm with `g++ --version`.

### macOS

1. Install VS Code from `code.visualstudio.com`.
2. Install the command line tools by running:

   ```text
   xcode-select --install
   ```

3. Confirm with `g++ --version`. On macOS this reports clang, which is fine — it supports C++17 fully.

### Linux

1. Install VS Code from your distribution's package manager or `code.visualstudio.com`.
2. Install the compiler and debugger:

   ```text
   sudo apt install g++ gdb          # Debian, Ubuntu
   sudo dnf install gcc-c++ gdb      # Fedora
   ```

3. Confirm with `g++ --version`.

### Then, on any platform

Install the Microsoft **C/C++** extension and follow Section A.4 from "Create a launch configuration" onward.

---

## A.6 Verifying Your Setup

Whichever environment you chose, this program confirms everything works. If it builds clean and prints the expected output, you are ready for Chapter 2.

```cpp
// setup-check.cpp - confirms the toolchain is working
// Build: g++ -std=c++17 -Wall -Wextra setup-check.cpp -o setup-check

#include <iostream>
#include <string>
#include <vector>

int main() {
    std::cout << "=== Setup Check ===\n";
    std::cout << "C++ standard: " << __cplusplus << "\n";

    std::vector<std::string> names = {"Ada", "Grace", "Alan"};
    for (const std::string& n : names) {
        std::cout << "  " << n << "\n";
    }

    std::cout << "If you see three names above, your setup is working.\n";
    return 0;
}
```

**Expected output:**

```text
=== Setup Check ===
C++ standard: 201703
  Ada
  Grace
  Alan
If you see three names above, your setup is working.
```

**The number `201703` confirms C++17.** A smaller number means the `-std=c++17` flag is not reaching the compiler — check your command or your `tasks.json`.

---

## A.7 When Setup Goes Wrong

| Symptom | Cause | Fix |
|---|---|---|
| `g++: command not found` | Compiler not installed or not on PATH | Section A.5 for your platform |
| `__cplusplus` is not `201703` | `-std=c++17` missing | Add it to your command or `tasks.json` |
| `bash: ./gradecalc: No such file` | Compilation failed, so no executable exists | Read the compiler messages above |
| `Permission denied` running the program | Executable bit not set | `chmod +x gradecalc` |
| Debugger starts but shows no variable names | Built without `-g` | Add `-g` to `tasks.json` |
| Breakpoints appear as hollow circles | The build did not include debug information | Add `-g`; rebuild |
| `undefined reference to ...` | A `.cpp` was left off the build | List every `.cpp`, or use `*.cpp` |
| Program cannot find `gradebook.csv` | Terminal is in a different directory | `cd` to the directory containing your program |
| Codespace will not start | Free monthly hours exhausted | Use the StudySite editor, or a local install |

---

## A.8 Which Environment for Which Chapter

| Chapters | Environment | Why |
|---|---|---|
| 1 | Neither — no code | |
| 2–9 | StudySite editor or Codespaces | Single-file programs |
| 10–15 | Either | Multi-file builds work in both |
| **16** | **Codespaces** | The symbolic debugger is required |
| 17–21 | Either | |
| **22** | **Codespaces** | AddressSanitizer is required |
| 23–24 | Either; Codespaces for the release build | |

**Use the StudySite editor for reading and experimenting; use Codespaces when a chapter needs the toolchain.** Nothing prevents you from using Codespaces throughout, and many students do.
