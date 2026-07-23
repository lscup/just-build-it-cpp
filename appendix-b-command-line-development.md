# Appendix B — Command Line Development

Chapter 2 introduced one command and Chapter 24 explained the four stages it performs. This appendix collects everything you need to build, run, and inspect C++ programs from a terminal.

Everything here works in GitHub Codespaces, macOS, Linux, and Windows with MSYS2.

---

## B.1 Moving Around

Before compiling, you must be in the directory containing your source.

| Command | Does |
|---|---|
| `pwd` | print the current directory |
| `ls` | list files here |
| `ls -l` | list with sizes and dates |
| `cd foldername` | move into a directory |
| `cd ..` | move up one level |
| `cd` | return to your home directory |
| `mkdir foldername` | create a directory |

```text
cd cpp-gradecalculator/v1.3
ls
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
./gradecalc
```

**The `./` in `./gradecalc` means "in the current directory."** Without it, the shell searches its usual locations and reports "command not found."

---

## B.2 The Compile Command

```text
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
```

| Part | Meaning |
|---|---|
| `g++` | the compiler |
| `-std=c++17` | use the C++17 standard |
| `-Wall` | report all common warnings |
| `-Wextra` | report additional warnings |
| `main.cpp` | the source file |
| `-o gradecalc` | name the executable |

**Silence means success.** A compiler with nothing to report says nothing.

### Multi-file programs

List every `.cpp`. Never list a header.

```text
g++ -std=c++17 -Wall -Wextra main.cpp assignment.cpp gradescale.cpp \
    student.cpp gradebook.cpp -o gradecalc
```

Or let the shell expand them:

```text
g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
```

**Omitting a `.cpp` produces an `undefined reference` error from the linker** — Chapter 24 Section 24.8.

### Useful additional flags

| Flag | Does | Used in |
|---|---|---|
| `-g` | include debug information | Chapter 16 |
| `-O2` | optimize | Chapter 24 release build |
| `-DNDEBUG` | remove assertions | Chapter 24 release build |
| `-fsanitize=address` | detect memory errors | Chapter 22 |
| `-Werror` | treat every warning as an error | optional discipline |

### The three builds this book uses

```text
# Ordinary development
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc

# Debugging (Chapter 16)
g++ -std=c++17 -Wall -Wextra -g main.cpp -o gradecalc

# Release (Chapter 24)
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG main.cpp -o gradecalc
```

---

## B.3 Stopping After Each Stage

Chapter 2 Section 2.2 described four stages. Each can be run alone, which makes the pipeline something you can inspect rather than take on trust.

| Command | Stops after | Produces |
|---|---|---|
| `g++ -E main.cpp -o main.ii` | preprocessing | the expanded translation unit |
| `g++ -S main.cpp -o main.s` | compilation | assembly |
| `g++ -c main.cpp -o main.o` | assembly | an object file |
| `g++ main.cpp -o gradecalc` | linking | the executable |

Worth doing once:

```text
g++ -std=c++17 -E main.cpp -o main.ii
wc -l main.ii
```

A six-line program expands past 32,000 lines. Chapter 2 measured exactly this.

### Compiling separately, then linking

Large projects compile each file once and relink:

```text
g++ -std=c++17 -c student.cpp -o student.o
g++ -std=c++17 -c gradebook.cpp -o gradebook.o
g++ -std=c++17 -c main.cpp -o main.o
g++ student.o gradebook.o main.o -o gradecalc
```

Change one `.cpp` and only that file needs recompiling. **Change a header and every file that includes it must be rebuilt** — which is why Chapter 19 Section 19.3 asks you to keep headers small.

---

## B.4 Running Programs

```text
./gradecalc
```

### Feeding input from a file

Instead of typing the same input repeatedly while testing:

```text
printf 'Ada\n1\nHomework 1\n9\n10\n0\n2\n3\n' > testinput.txt
./gradecalc < testinput.txt
```

The `<` redirects the file into the program's standard input, exactly as if you had typed it.

### Capturing output

```text
./gradecalc < testinput.txt > output.txt
./gradecalc < testinput.txt 2> errors.txt      # error output only
./gradecalc < testinput.txt > all.txt 2>&1     # both together
```

### Comparing two versions

This is the verification procedure from Chapter 13 Section 13.6:

```text
./gradecalc13 < testinput.txt | tail -9 > out13.txt
./gradecalc20 < testinput.txt | tail -9 > out20.txt
diff out13.txt out20.txt
```

**`diff` printing nothing means the files match.** That silence is your evidence that a refactor changed no behavior.

### The exit code

```text
./gradecalc
echo $?
```

`0` means success, anything else means failure — Chapter 2 Section 2.1, and Chapter 24's release build returns 1 when it cannot save.

### Stopping a runaway program

**Ctrl+C.** Useful when Chapter 7's infinite loops arrive.

---

## B.5 Debugging from the Command Line

Chapter 16 uses the VS Code debugger. The same debugger is available directly as `gdb`, and knowing a few commands is useful when no editor is available.

```text
g++ -std=c++17 -Wall -Wextra -g main.cpp -o gradecalc
gdb ./gradecalc
```

| Command | Does |
|---|---|
| `break main` | breakpoint at the start of `main` |
| `break main.cpp:42` | breakpoint at line 42 |
| `run` | start the program |
| `next` | execute one line, stepping over calls |
| `step` | execute one line, stepping into calls |
| `finish` | run until the current function returns |
| `print x` | show the value of `x` |
| `backtrace` | show the call stack |
| `continue` | run to the next breakpoint |
| `quit` | leave gdb |

The concepts are identical to Chapter 16's — `next` is Step Over, `step` is Step Into, `backtrace` is the Call Stack panel.

---

## B.6 Finding Memory Errors

Chapter 22's tool:

```text
g++ -std=c++17 -fsanitize=address -g *.cpp -o gradecalc
./gradecalc
```

The program runs normally and reports leaks, use-after-free, and buffer overruns as they occur:

```text
SUMMARY: AddressSanitizer: 264 byte(s) leaked in 4 allocation(s).
```

A related tool checks for undefined behavior:

```text
g++ -std=c++17 -fsanitize=undefined -g *.cpp -o gradecalc
```

This catches signed overflow, some out-of-bounds accesses, and other undefined behavior — including things Chapter 3 and Chapter 11 warned about but could not demonstrate reliably.

**Run both before considering a program finished.**

---

## B.7 Makefiles

Every program in this book builds with one command, so a makefile is a convenience rather than a requirement. Chapter 24 Section 24.8 shows one; here is a slightly fuller version.

Create a file named exactly `Makefile`:

```text
CXX      = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -g
SRCS     = main.cpp assignment.cpp gradescale.cpp student.cpp \
           gradingscheme.cpp gradebook.cpp
TARGET   = gradecalc

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) $(SRCS) -o $(TARGET)

release: $(SRCS)
	$(CXX) -std=c++17 -Wall -Wextra -O2 -DNDEBUG $(SRCS) -o $(TARGET)

asan: $(SRCS)
	$(CXX) $(CXXFLAGS) -fsanitize=address $(SRCS) -o $(TARGET)

clean:
	rm -f $(TARGET) *.o

.PHONY: release asan clean
```

Then:

```text
make            # ordinary build
make release    # optimized build
make asan       # sanitizer build
make clean      # remove build products
```

> **The indented lines in a makefile must begin with a real tab character, not spaces.** This is the single most common makefile error, and the message — `missing separator` — does not say so.

---

## B.8 Version Control

Chapter 13 Section 13.6 explains why this matters. The commands you need:

| Command | Does |
|---|---|
| `git init` | start tracking a directory |
| `git status` | what has changed |
| `git add .` | stage all changes |
| `git commit -m "message"` | record the staged changes |
| `git log --oneline` | list the history |
| `git diff` | show unstaged changes |
| `git checkout -- file` | discard changes to a file |

A typical cycle:

```text
git add .
git commit -m "v1.2: grade scale is now user-defined rather than hard-coded"
```

**Commit each Grade Calculator version separately**, with a message saying *why*. By Chapter 24 you will have twelve commits, each a working program — which is the version history the capstone asks for.

### Ignoring build products

Create a file named `.gitignore`:

```text
gradecalc
*.o
*.ii
*.s
gradebook.csv
```

Executables and object files are rebuilt from source and should not be committed.

---

## B.9 Command Reference

```text
# Build
g++ -std=c++17 -Wall -Wextra main.cpp -o gradecalc
g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
g++ -std=c++17 -Wall -Wextra -g *.cpp -o gradecalc              # debug
g++ -std=c++17 -Wall -Wextra -O2 -DNDEBUG *.cpp -o gradecalc    # release
g++ -std=c++17 -fsanitize=address -g *.cpp -o gradecalc         # memory check

# Inspect the pipeline
g++ -std=c++17 -E main.cpp -o main.ii     # after preprocessing
g++ -std=c++17 -S main.cpp -o main.s      # after compiling
g++ -std=c++17 -c main.cpp -o main.o      # after assembling

# Run
./gradecalc
./gradecalc < testinput.txt
./gradecalc < testinput.txt > output.txt
echo $?

# Compare
diff out13.txt out20.txt

# Debug
gdb ./gradecalc

# Version control
git add . && git commit -m "why this changed"
git log --oneline
```

---

## B.10 Common Command Line Problems

| Symptom | Cause | Fix |
|---|---|---|
| `command not found: g++` | Compiler not installed or not on PATH | Appendix A Section A.5 |
| `bash: ./gradecalc: No such file` | Build failed, so nothing was produced | Read the compiler output |
| `Permission denied` | Executable bit not set | `chmod +x gradecalc` |
| `undefined reference to ...` | A `.cpp` was omitted | List every `.cpp`, or use `*.cpp` |
| `No such file or directory: main.cpp` | Wrong directory | `pwd`, then `cd` |
| Program cannot find its data file | Terminal is elsewhere | `cd` to the program's directory |
| `make: *** missing separator` | Spaces instead of a tab in the makefile | Use a real tab |
| Program will not stop | Infinite loop | Ctrl+C |
| Nothing printed after compiling | Compilation succeeded | That is what success looks like |
