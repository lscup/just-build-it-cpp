# Just Build It! C++ — Chapter Outline

*Programming Fundamentals, One Working Program at a Time*

**24 chapters across a two-course sequence**
Inspired by *Programming Fundamentals* (Richard Halterman), restructured for the Student Learning Outcomes below and for WCAG-compliant publication in StudySite.ai.

---

## About This Outline

### Course structure

| Course | Chapters | Focus |
|---|---|---|
| Course I — Programming Fundamentals | 1–12 | Data representation, procedural programming, control structures, functions, arrays |
| Course II — Object-Oriented Programming | 13–24 | SDLC, structs and classes, inheritance, polymorphism, algorithms, debugging, memory |

### Student Learning Outcomes

**Course I (Chapters 1–12)**

| ID | Outcome |
|---|---|
| SLO 1.1 | Describe how data are represented, manipulated, and stored in a computer. |
| SLO 1.2 | Categorize different programming languages and their uses. |
| SLO 1.3 | Understand and use the fundamental concepts of data types, structured programming, algorithmic design, and user interface design. |
| SLO 1.4 | Demonstrate a fundamental understanding of software development methodologies, including modular design, pseudo code, flowcharting, structure charts, data types, control structures, functions, and arrays. |
| SLO 1.5 | Develop projects that utilize logical algorithms from specifications and requirements statements. |
| SLO 1.6 | Demonstrate appropriate design, coding, testing, and documenting of computer programs that implement project specifications and requirements. |
| SLO 1.7 | Apply computer programming concepts to new problems or situations. |

**Course II (Chapters 13–24)**

| ID | Outcome |
|---|---|
| SLO 2.1 | Identify and explain a programming development lifecycle, including planning, analysis, design, development, and maintenance. |
| SLO 2.2 | Demonstrate a basic understanding of object-oriented programming by using structs and classes in software projects. |
| SLO 2.3 | Use object-oriented programming techniques to develop executable programs that include elements such as inheritance and polymorphism. |
| SLO 2.4 | Document and format code in a consistent manner. |
| SLO 2.5 | Apply basic searching and sorting algorithms in software design. |
| SLO 2.6 | Apply single- and multi-dimensional arrays in software. |
| SLO 2.7 | Use a symbolic debugger to find and fix runtime and logical errors in software. |
| SLO 2.8 | Demonstrate a basic understanding of programming methodologies, including object-oriented, structured, and procedural programming. |
| SLO 2.9 | Describe the phases of program translation from source code to executable code. |

### The running project: Grade Calculator

Every chapter ends with a **Grade Calculator** section in which students extend one continuously evolving application.

### The completeness rule

**Every chapter's version compiles, runs to completion, and produces correct output for the features it has.** A version may be missing features. It is never missing an ending.

This is a hard constraint on how the book is written, and it rules out several habits common in textbooks:

- No chapter delivers a fragment, a function without a caller, or a class without a `main` that exercises it.
- No chapter leaves the project in a state that does not build. If a refactor spans two chapters, the first chapter completes a coherent subset and the second extends it — the seam falls between two working programs, never through the middle of one.
- No chapter introduces a feature it cannot finish. A capability arrives whole or waits for the chapter that can complete it.
- Every version handles its own input errors well enough not to crash on the input its own prompts invite.
- Every version ends with a clear, formatted result and a normal exit — never a silent return or an unhandled condition.

Practically, this means each chapter's version is a program a student could hand to an instructor and have it work. From Chapter 2 forward there are twenty-three of them, one per chapter, and Appendix E carries the complete source of all twenty-three.

**Reference-only content.** A few topics are worth explaining but not worth building into the project — command-line arguments in Section 11.10 are the clearest case. These are labeled *reference only* wherever they appear, in the section heading and in the chapter's key terms. The label is a promise in both directions: the book explains the topic and shows a short standalone example, and no exercise or project milestone will require it. Marking these explicitly is what keeps the completeness rule honest, since a concept taught but never used would otherwise read as a feature the project forgot to finish.

Two consequences worth noting. Design-heavy chapters (5, 13) still ship a running program — the design artifacts are additional deliverables, not substitutes, and each of those chapters includes a modest but real code change so students end the chapter with something they can run. And the "a"-suffixed sub-versions of earlier drafts are gone: one chapter, one version, one working build.

### Grading model by course

The grading model is deliberately staged. Course I builds a complete, genuinely useful points-based calculator. Course II generalizes it — and that generalization is the pedagogical payoff of the object-oriented material.

| Capability | Course I (Ch 1–12) | Course II (Ch 13–24) |
|---|---|---|
| Points-based grading (points earned ÷ points possible) | Yes — the only scheme | Yes — retained as one of two schemes |
| Weighted-category grading (categories with percentage weights) | No | Yes — added in Ch 20–21 |
| Scheme selectable at run time | No | Yes — polymorphic dispatch, Ch 21 |
| Custom letter grade scale (user-defined cutoffs and letters) | Yes — from Ch 11 | Yes — refined into a class |
| Assignment name input | Yes — from Ch 3 | Yes |
| Bonus points | Yes — from Ch 4 | Yes — per scheme |

Restricting Course I to a single scheme keeps procedural code honest: with one grading rule there is no reason to reach for abstraction students have not met. Course I therefore ends with a well-written procedural program that is genuinely appropriate for its requirements — not a straw man.

When Course II adds a second scheme, inheritance and polymorphism are presented immediately as the right tool for it. Chapter 20 opens with a short worked comparison — the book shows what a flag-and-branch version would look like and names its specific costs — and then teaches the inheritance-based design students will actually build. Students read the analysis; they do not spend a session implementing a version that will be discarded.

The three shared features — custom letter scales, assignment names, and bonus points — are present in both courses. They give Course I enough substance to be a real application, and they give Course II concrete material to encapsulate.

### Version by chapter

One version per chapter. Every entry below is a complete, running program.

| Ch | Version | What it does when you run it |
|---|---|---|
| 1 | — | *(No code yet — requirements document only)* |
| 2 | v0.1 | Prints the gradebook banner and course name, exits cleanly |
| 3 | v0.2 | Prompts for student name, assignment name, points earned and possible; echoes a formatted summary |
| 4 | v0.3 | Adds bonus points and reports a percentage to one decimal place |
| 5 | v0.4 | Same computation, redesigned prompts and report layout from the UI design work |
| 6 | v0.5 | Reports a letter grade from a fixed scale |
| 7 | v0.6 | Accepts many named assignments until a sentinel; reports course total and letter |
| 8 | v0.7 | Correct rounding and a documented bonus-point cap policy |
| 9 | v1.0 | Same behavior, rebuilt from documented functions; adds a menu |
| 10 | v1.1 | Same behavior across three files; validated input never crashes |
| 11 | v1.2 | Multi-student roster; user-defined letter scale replaces the fixed one |
| 12 | v1.3 | Unlimited roster and assignments; drop-lowest feature — **Course I complete** |
| 13 | v2.0 | Identical behavior, reformatted to the adopted coding standard; adds an About screen |
| 14 | v2.1 | Same behavior on `struct` records instead of parallel arrays |
| 15 | v2.2 | Saves and loads gradebooks, assignments, and the grade scale to CSV |
| 16 | v2.3 | Three defects fixed, regression tests added and passing |
| 17 | v2.4 | Sort the roster by several keys; search by student ID |
| 18 | v2.5 | Same behavior on `Student` and `GradeScale` classes; invalid scales now impossible |
| 19 | v2.6 | Reports print via `operator<<`; one header/implementation pair per class |
| 20 | v3.0 | Weighted-category grading works; scheme chosen at startup |
| 21 | v3.1 | Scheme switchable mid-session, all grades recomputed live |
| 22 | v3.2 | Same behavior, no memory leaks |
| 23 | v3.3 | Adds class statistics, grade distribution, ID-keyed lookup |
| 24 | v4.0 | Full error handling, release build, user guide — **Course II complete** |

### Technical decisions

| Decision | Choice | Consequence for the writing |
|---|---|---|
| Language standard | **C++17** | `auto`, range-based `for`, `std::vector`, `std::string_view`, structured bindings, and `std::optional` are all available. Compile line is `g++ -std=c++17 -Wall -Wextra`. |
| Primary environment | **StudySite.ai's built-in editor** | Every program must build and run with no project file, no build system, and no external libraries — standard library only. |
| Debugging environment | **GitHub Codespaces** (VS Code based) | Chapter 16 teaches the VS Code debugger UI, which students reach through Codespaces without installing anything locally. |
| Platform assumptions | **None** | No Windows-only or POSIX-only calls, no `system("pause")`, no `conio.h`, no ANSI escape codes for color. Output is plain text that renders identically everywhere. |
| I/O model | **Console only**, `std::cin` / `std::cout` | Keeps every version runnable in a browser editor and makes automated checking of student work straightforward. |
| Program interface | **Interactive and menu-driven** | Every program uses `int main()` and prompts for input. No program reads command-line arguments; `argc`/`argv` are explained in Section 11.10 as reference material only. |
| Diagrams | **Hand-authored SVG**, PNG beside each | Mermaid is not rendered by StudySite. Each figure lives in `figures/` with `role="img"`, `<title>`, `<desc>`, and `aria-labelledby`, plus a prose long description in the chapter body. A manifest lists every asset so import is mechanical. |
| Exercises | **Generated by StudySite's exercise builder** | The book supplies runnable examples with expected output, not authored exercise sets or solution keys. See "Exercises are generated, not authored" below. |
| Voice | **Second person** ("you write…") | Direct address throughout, suited to self-paced students working in the StudySite editor. |
| File I/O | **Relative paths, plain CSV** | Works identically in the StudySite editor and Codespaces. No absolute paths, no platform-specific separators. |

Two constraints follow from the browser-based editor and deserve stating plainly, because they shape every listing in the book. **All input is line-oriented and all output is plain text** — no cursor positioning, no screen clearing, no color. And **no program depends on being rebuilt a particular way**: single-file versions compile with one command, multi-file versions with one command listing the files. Nothing requires a makefile, though Chapter 24 shows one as an optional convenience.

Because Codespaces is VS Code, Chapter 16's debugger instruction transfers directly to a local VS Code installation for students who want one, and the concepts transfer to any symbolic debugger. The chapter teaches breakpoints, stepping, watches, and the call stack as ideas first, then shows the VS Code gestures that invoke them.

### Chapter template

Each chapter follows the same structure so the reading experience is predictable — a WCAG 3.2.3 (Consistent Navigation) and 3.2.4 (Consistent Identification) requirement.

1. Learning Objectives (mapped to SLOs)
2. Motivation — a problem the current toolkit cannot solve
3. Concept sections with worked, runnable listings
4. Common Errors and Warnings
5. Design Notes — style, formatting, documentation habits
6. **Grade Calculator** — apply the chapter to the running project
7. **Try It Yourself** — runnable examples with suggested variations
8. Summary
9. Key Terms with definitions

### Exercises are generated, not authored

StudySite.ai includes an exercise builder that generates exercises from the supplied chapter source, so **this book does not contain authored exercise sets or solution keys.** What it contains instead is the raw material that builder needs, and getting that material right is an authoring obligation rather than an afterthought.

Practically, every chapter carries a **Try It Yourself** section of short, complete, runnable programs — each one small enough to read in a sitting, each demonstrating exactly one idea, each accompanied by its expected output and two or three suggested variations ("change the cutoff to 85 and predict what happens before you run it"). Students can open any of them directly in the StudySite editor and terminal.

This shapes the prose in three ways worth stating up front:

- **Concepts are named explicitly, not just demonstrated.** A generator cannot build a question about an idea the text never names. Where a listing illustrates short-circuit evaluation, the prose says so in those words.
- **Expected output is always shown.** Every runnable example is paired with what it prints, which gives the generator a verifiable answer to build against and gives students a way to check themselves without a solution key.
- **Boundary and failure cases are called out in the text.** The interesting questions live at the edges — what happens at exactly 90.0, at zero points possible, at a bonus that pushes past 100. Naming those cases in the prose is what lets good exercises be generated from them.

The Grade Calculator milestone in each chapter is a natural exercise source too: it is a stated goal with a known-good implementation in Appendix E, so generated work can be checked against a reference.

### Accessibility conventions (WCAG 2.2 AA)

- **Headings** are strictly nested (no skipped levels); one `#` per chapter.
- **Code** uses fenced blocks with an explicit `cpp` language tag; every listing has a caption and is referenced by name in prose, never as "the code below."
- **Figures** — flowcharts, structure charts, memory diagrams — are authored as Mermaid or SVG with descriptive `alt` text plus a long-description paragraph conveying the same information in prose. No figure carries meaning available only visually.
- **Color** is never the sole carrier of meaning; syntax highlighting is decorative and all diagrams are labeled with text.
- **Tables** use real header rows with scope; no layout tables.
- **Console output** is shown in labeled blocks distinguishable from source code by caption, not styling alone.
- **Link text** is descriptive ("the operator precedence table in Chapter 4"), never "click here."
- **Math** is written in plain prose or MathML-compatible notation, not images.
- **Terminology** is consistent: one name per concept, defined in the chapter Key Terms and the book glossary.

---

# Course I — Programming Fundamentals

## Chapter 1 — Computing, Data, and the Software Landscape

**Objectives:** SLO 1.1, 1.2

Establishes what a computer actually stores and how programming languages differ, before any code is written.

**Sections**

1.1 What a Program Is
1.2 Hardware in Brief: CPU, Memory, Storage, I/O
1.3 Representing Data: Bits, Bytes, and Words
1.4 Numbers in Binary, Octal, and Hexadecimal
1.5 Representing Negative Numbers and Real Numbers
1.6 Representing Text: ASCII and Unicode
1.7 How Data Are Manipulated and Stored
1.8 Categories of Programming Languages
  1.8.1 Machine, Assembly, and High-Level Languages
  1.8.2 Compiled, Interpreted, and Hybrid Languages
  1.8.3 Paradigms: Procedural, Object-Oriented, Functional
  1.8.4 Choosing a Language for a Purpose
1.9 Where C++ Fits and Why This Book Uses It

**Grade Calculator v0.0 — Problem Statement.** Students write the plain-language requirements for a **points-based** grade calculator: it accepts named assignments with points earned, points possible, and optional bonus points, and reports a percentage and a letter grade against a scale the user defines. Weighted grading is explicitly listed as out of scope for Course I and noted as a planned future enhancement — students' first requirements document therefore includes a scope boundary, which they will revisit in Chapter 20. They also estimate the storage a single assignment record needs, applying Section 1.3.

**Key terms:** bit, byte, word, binary, hexadecimal, two's complement, ASCII, Unicode, machine language, assembler, compiler, interpreter, paradigm, source code, executable

**Accessibility notes:** Bit-pattern and memory-layout figures need long descriptions stating every value in prose. The number-base conversion table needs real header rows.

---

## Chapter 2 — From Source Code to Running Program

**Objectives:** SLO 1.2, 2.9 *(introduced here, revisited in Chapter 24)*

**Sections**

2.1 Anatomy of a Simple C++ Program
2.2 The Translation Pipeline
  2.2.1 Preprocessing
  2.2.2 Compilation to Assembly
  2.2.3 Assembly to Object Code
  2.2.4 Linking and Loading
2.3 Development Tools: Editors, Compilers, Debuggers, Build Systems
2.4 Setting Up Your Environment
2.5 Editing, Compiling, and Running Your First Program
2.6 Reading Compiler Messages
2.7 A Template for Simple C++ Programs
2.8 Source Formatting and Comments from Day One

**Grade Calculator v0.1 — Hello, Gradebook.** A compiling, running program that prints the application banner and the course name. Students confirm their toolchain works end to end and commit the first version.

**Key terms:** preprocessor, translation unit, object file, linker, loader, IDE, toolchain, `#include`, `main`, namespace, whitespace

**Accessibility notes:** The translation-pipeline figure is a Mermaid flowchart with each stage's inputs and outputs restated in prose.

---

## Chapter 3 — Values, Variables, and Data Types

**Objectives:** SLO 1.1, 1.3

**Sections**

3.1 Literal Values
3.2 Variables, Declaration, and Assignment
3.3 Identifiers and Naming Conventions
3.4 Integer Types and Their Ranges
3.5 Floating-Point Types and Precision
3.6 Characters and Text
3.7 Boolean Values
3.8 Constants and `const`
3.9 Enumerated Types
3.10 Type Inference with `auto`
3.11 Choosing the Right Type
3.12 Basic Console Input and Output

**Grade Calculator v0.2 — Naming and Storing an Assignment.** Declares typed variables for the student name, the **assignment name**, points earned, and points possible. Reading a name introduces `std::getline` and the distinction between extracting a word and reading a whole line — including the classic mixed `>>`/`getline` pitfall, met here where it is cheap to explain. Students justify each type choice in a comment block, including why points are floating-point and why a name cannot be a `char`.

**Key terms:** literal, variable, identifier, declaration, initialization, `int`, `double`, `char`, `bool`, `const`, enumeration, `auto`, overflow, precision, `std::cin`, `std::cout`, `std::getline`, text input

**Accessibility notes:** The type-range table must be a genuine data table. Precision-loss examples show exact console output in captioned blocks.

---

## Chapter 4 — Expressions, Arithmetic, and Errors

**Objectives:** SLO 1.1, 1.3, 1.6

**Sections**

4.1 Expressions and Operators
4.2 Integer vs. Floating-Point Arithmetic
4.3 Integer Division and Modulus
4.4 Mixed-Type Expressions and Conversion
4.5 Operator Precedence and Associativity
4.6 Compound Assignment, Increment, and Decrement
4.7 Formatting Numeric Output
4.8 Bitwise Operators
4.9 Kinds of Errors
  4.9.1 Compile-Time Errors
  4.9.2 Run-Time Errors
  4.9.3 Logic Errors
  4.9.4 Compiler Warnings and Why to Fix Them
4.10 Comments and Self-Documenting Code

**Grade Calculator v0.3 — Percentage and Bonus Points.** Calculates a percentage from points earned and points possible, formatted to one decimal place. **Bonus points** are added to points earned but not to points possible — which means a percentage above 100 is now possible. Students must decide, document, and justify whether their calculator caps the result at 100, and the two behaviors are compared against real grading policies. This is also where they deliberately introduce an integer-division bug, observe it, and fix it — their first logic error.

**Key terms:** operand, operator, precedence, associativity, implicit conversion, cast, modulus, compound assignment, compile-time error, run-time error, logic error, warning

**Accessibility notes:** The precedence table is long — split by category with a heading per group so screen-reader users can navigate it.

---

## Chapter 5 — Algorithmic Design and Program Documentation

**Objectives:** SLO 1.3, 1.4, 1.5, 1.6

A design chapter placed deliberately before control structures, so students plan in pseudocode before they can write branches and loops.

**Sections**

5.1 What Makes an Algorithm
5.2 From Requirements Statement to Specification
5.3 Writing Pseudocode
5.4 Flowcharting: Symbols and Conventions
5.5 Structure Charts and Top-Down Decomposition
5.6 Desk Checking and Trace Tables
5.7 Structured Programming: Sequence, Selection, Repetition
5.8 User Interface Design for Console Applications
  5.8.1 Prompts, Feedback, and Error Messages
  5.8.2 Designing a Readable Report
  5.8.3 Accessibility in Text-Based Interfaces
5.9 Documenting Your Design

**Grade Calculator v0.4 — Designed Interface.** Two deliverables, one of them running code.

*Design artifacts:* a written specification, pseudocode, a flowchart, and a structure chart for the full points-based application students will build over the term, covering assignment name entry, bonus points, the percentage calculation, and a user-defined letter scale. The specification states the points-based scope boundary explicitly and records weighted grading as a deferred requirement. This artifact is revised at each later chapter and formally reconciled in Chapter 24.

*Running program:* v0.4 computes exactly what v0.3 did, but students apply Section 5.8 to the parts they can already change — clearer prompts that state expected units and ranges, a report laid out in aligned labeled columns, and a plain-language message when points possible is zero instead of an unexplained result. The program still ends with a complete formatted report and a clean exit. Students run v0.3 and v0.4 side by side and note which changes improved comprehension, which is a design judgment rather than a coding one.

**Key terms:** algorithm, specification, pseudocode, flowchart, structure chart, desk check, trace table, sequence, selection, repetition, top-down design, decomposition, user interface

**Accessibility notes:** This chapter is figure-dense. Every flowchart and structure chart requires a prose long description that a reader could use to reconstruct the diagram. Flowchart symbols are described by name (decision diamond, process rectangle), never by shape alone.

---

## Chapter 6 — Conditional Execution

**Objectives:** SLO 1.3, 1.4, 1.7

**Sections**

6.1 The `bool` Type Revisited
6.2 Relational Operators and Boolean Expressions
6.3 The `if` Statement
6.4 Compound Statements and Scope
6.5 The `if/else` Statement
6.6 Logical Operators and Compound Conditions
6.7 Short-Circuit Evaluation
6.8 Nested Conditionals
6.9 Multi-way `if/else if` Chains
6.10 The `switch` Statement
6.11 The Conditional Operator
6.12 Common Errors in Conditional Logic

**Grade Calculator v0.5 — Letter Grades.** Converts a percentage to a letter grade with a multi-way chain, using a fixed 90/80/70/60 scale defined as named constants. Students trace boundary cases (89.95, 90.0) and document which behavior is correct and why, and confirm that a bonus-inflated percentage above 100 still maps to the top grade. The chapter closes by asking how the program would change if a user wanted a different scale — every cutoff is hard-coded in the conditional chain, which motivates the data-driven redesign in Chapter 11.

**Key terms:** relational operator, Boolean expression, `if`, `else`, block, scope, `&&`, `||`, `!`, short-circuit evaluation, nested conditional, `switch`, `case`, fall-through, conditional operator

**Accessibility notes:** Decision logic gets both a flowchart and an equivalent decision table in prose.

---

## Chapter 7 — Iteration

**Objectives:** SLO 1.3, 1.4, 1.7

**Sections**

7.1 The `while` Statement
7.2 Counter-Controlled vs. Sentinel-Controlled Loops
7.3 The `do/while` Statement
7.4 The `for` Statement
7.5 Choosing the Right Loop
7.6 Nested Loops
7.7 Altering Loop Flow: `break` and `continue`
7.8 Infinite Loops and How to Escape Them
7.9 Accumulators, Counters, and Running Totals
7.10 Loop Design and Off-by-One Errors

**Grade Calculator v0.6 — Multiple Assignments.** Loops to accept an arbitrary number of named assignments using a sentinel, accumulating total points earned (including bonus) and total points possible. Reports the running course percentage after each entry. Because points-based grading is simply a ratio of two running totals, the accumulator pattern from Section 7.9 *is* the grading algorithm — a point worth making explicitly, since it is exactly what will not generalize to weighted grading in Chapter 20.

**Key terms:** loop, iteration, `while`, `do/while`, `for`, loop control variable, sentinel, accumulator, counter, nested loop, `break`, `continue`, infinite loop, off-by-one error

**Accessibility notes:** Trace tables replace any animation of loop state. Every loop example includes a full iteration-by-iteration table.

---

## Chapter 8 — Using Library Functions

**Objectives:** SLO 1.3, 1.7

**Sections**

8.1 What a Function Is, from the Caller's View
8.2 Arguments, Parameters, and Return Values
8.3 Headers and the Standard Library
8.4 Mathematical Functions
8.5 Minimum, Maximum, and Rounding
8.6 Character Classification Functions
8.7 Random Numbers
8.8 Timing with `clock`
8.9 Reading Library Documentation

**Grade Calculator v0.7 — Rounding and Robustness.** Uses `std::round` to round the reported percentage correctly and `std::max`/`std::min` to implement the bonus-point cap policy chosen in Chapter 4 as a single clear expression. Students replace their hand-written rounding logic, compare results, and find at least one input where the two disagree.

**Key terms:** function call, argument, parameter, return value, header, library, `<cmath>`, `<cctype>`, `<random>`, side effect, documentation

**Accessibility notes:** Function-signature listings are captioned individually so they can be cited by name.

---

## Chapter 9 — Writing Functions

**Objectives:** SLO 1.4, 1.5, 1.6, 1.7

**Sections**

9.1 Defining a Function
9.2 Prototypes, Definitions, and Order
9.3 Parameters and Pass by Value
9.4 Return Values and `void` Functions
9.5 Local Variables and Scope
9.6 Modular Design in Practice
9.7 From Structure Chart to Function Set
9.8 Commenting and Documenting Functions
9.9 Testing Functions Individually
9.10 Worked Examples: Input Validation, Menu Handling, Report Formatting

**Grade Calculator v1.0 — Modular Rebuild.** The application is rebuilt from named functions derived directly from the Chapter 5 structure chart: `readAssignment`, `computePercentage`, `applyBonus`, `assignLetterGrade`, and `printReport`. Each gets a documentation comment stating purpose, parameters, return value, and preconditions, plus a hand-written test case including a bonus-point case and a zero-points-possible case.

Because functions now make it cheap, v1.0 also gains a **menu loop** — add an assignment, view the report, or quit — so the program no longer runs once and exits. This is the first version that behaves like an application rather than a script, and it remains the shell for every version that follows.

*Refactoring under the completeness rule:* the rebuild happens in one chapter, not spread across two. Section 9.6 walks students through it one function at a time, recompiling and rerunning after each extraction, so the program is working at every intermediate step and never enters a broken half-refactored state.

**Key terms:** function definition, prototype, signature, pass by value, return type, `void`, local variable, scope, lifetime, modular design, cohesion, stub, driver

**Accessibility notes:** Show the structure chart from Chapter 5 alongside the resulting function list, with the mapping stated in prose.

---

## Chapter 10 — Managing Functions and Data

**Objectives:** SLO 1.4, 1.6, 1.7

**Sections**

10.1 Global and Static Variables, and Why to Avoid Globals
10.2 Overloaded Functions
10.3 Default Arguments
10.4 Recursion
10.5 Introduction to Pointers
10.6 Reference Variables
10.7 Pass by Reference
  10.7.1 Via Pointers
  10.7.2 Via References
  10.7.3 `const` References
10.8 Splitting a Program Across Files
10.9 Making Functions Reusable

**Grade Calculator v1.1 — Multi-File and Reusable.** Split into `gradelib.h`, `gradelib.cpp`, and `main.cpp`. Input validation is rewritten to return a status flag by reference alongside the validated value. Students overload `formatGrade` for numeric and letter forms, and give `applyBonus` a default argument of zero so existing calls still compile — a concrete demonstration of extending an interface without breaking its callers.

**Key terms:** global variable, static variable, overloading, default argument, recursion, base case, pointer, address-of, dereference, reference, pass by reference, `const` reference, header guard, separate compilation

**Accessibility notes:** Pointer and memory diagrams need long descriptions naming each variable, its address, and its value.

---

## Chapter 11 — Arrays

**Objectives:** SLO 1.4, 1.7, 2.6

**Sections**

11.1 Why Collections Are Needed
11.2 Declaring and Initializing Arrays
11.3 Indexing and Bounds
11.4 Traversing an Array
11.5 Arrays and Functions
11.6 Parallel Arrays
11.7 Two-Dimensional Arrays
11.8 Multidimensional Arrays
11.9 C-Style Strings
11.10 Command-Line Arguments *(reference only — see note below)*
11.11 Common Array Errors

**Grade Calculator v1.2 — Class Roster and Custom Letter Scale.** Two features arrive together because both are fundamentally about replacing code with data.

Stores points for many students in a two-dimensional array (students × assignments), with parallel arrays of student names and assignment names. Computes per-student and per-assignment totals and percentages.

More importantly, the hard-coded grade cutoffs from Chapter 6 become **parallel arrays** of cutoff values and letters that the user enters at startup — so an instructor can define an A/B/C/D/F scale, a plus-minus scale, or a pass/fail scale without the program changing. `assignLetterGrade` becomes a short loop over those arrays instead of a conditional chain. Students explicitly compare the two versions and articulate why the table-driven one is shorter, more flexible, and easier to test. This is the chapter's central lesson — that data can replace control flow — and it recurs in Chapter 14 as a struct and Chapter 18 as a class.

Validation matters here: cutoffs must be entered in descending order and the scale must cover every possible percentage. Students write and test that validation.

**Note on Section 11.10.** Command-line arguments are covered because `argv` is an array of C strings and belongs to this chapter's material. They are **reference content only**: the Grade Calculator never reads them, and no exercise requires them. Every program in this book is menu-driven and takes its input interactively from `std::cin`. Section 11.10 explains what `argc` and `argv` are and shows a short standalone example, then says plainly that this book's programs do not use them and why.

**Key terms:** array, element, index, subscript, bounds, out-of-bounds, traversal, parallel arrays, two-dimensional array, row-major order, C string, `argc`, `argv` *(reference only)*

**Accessibility notes:** Two-dimensional array figures are presented as real tables with row and column headers, not as images of grids.

---

## Chapter 12 — Vectors and Standard Strings

**Objectives:** SLO 1.3, 1.7, 2.6

**Sections**

12.1 Limitations of Raw Arrays
12.2 Declaring and Using `std::vector`
12.3 Growing and Shrinking a Vector
12.4 Vector Member Functions
12.5 Range-Based `for` Loops
12.6 Vectors and Functions
12.7 Vectors of Vectors
12.8 `std::string` as a Sequence
12.9 String Operations and Parsing
12.10 Vectors vs. Arrays: When to Use Which

**Grade Calculator v1.3 — Dynamic Roster.** Replaces fixed arrays with `std::vector`, allowing any number of students, assignments, and grade-scale tiers. Student and assignment names become `std::string`, removing the fixed-length limits from Chapter 11. Adds a "drop lowest assignment" feature — which in a points-based scheme means removing both its earned and possible points, a subtlety students must reason through and test.

**Course I final feature set:** named assignments, bonus points, user-defined letter scale, multi-student roster, class statistics, sorting, and drop-lowest — all on a single points-based grading model.

**Key terms:** `std::vector`, dynamic sizing, `push_back`, `size`, `at`, range-based `for`, `std::string`, `substr`, `find`, container

**Accessibility notes:** Capacity-growth diagrams need prose descriptions of sizes before and after each operation.

**Course I capstone.** Students deliver Grade Calculator v1.3 — a complete points-based grading application with named assignments, bonus points, a user-defined letter scale, and a multi-student roster — together with its updated design document, function documentation, and a written test plan. Evidence for SLO 1.5 and 1.6. The application is genuinely usable at this point; nothing in Course II is required to make it work, only to make it general.

---

# Course II — Object-Oriented Programming

## Chapter 13 — The Software Development Lifecycle

**Objectives:** SLO 2.1, 2.4, 2.8

Opens Course II by framing everything that follows as a lifecycle activity rather than a coding trick.

**Sections**

13.1 Why Process Matters
13.2 Planning: Feasibility and Requirements Gathering
13.3 Analysis: Modeling the Problem Domain
13.4 Design: Architecture, Interfaces, and Data
13.5 Development: Implementation and Integration
13.6 Testing and Quality Assurance
13.7 Deployment and Maintenance
13.8 Lifecycle Models: Waterfall, Iterative, Agile
13.9 Programming Methodologies Compared
  13.9.1 Unstructured and Procedural
  13.9.2 Structured
  13.9.3 Object-Oriented
  13.9.4 Choosing a Methodology
13.10 Coding Standards, Formatting, and Documentation
13.11 Version Control Basics

**Grade Calculator v2.0 — Inherited Codebase.** Two deliverables, one of them running code.

*Design artifacts:* a maintenance and enhancement plan for the application inherited from Course I — what it does, what it lacks, and a prioritized backlog for the term. The headline item is the deferred requirement recorded in Chapter 1, **weighted-category grading**, now formally analyzed: what it means, how it differs from points-based grading, and what it will cost. Students produce this analysis before they know how they will implement it, which is the position a maintenance programmer normally occupies.

*Running program:* students adopt the written coding standard from Appendix D and bring the entire Course I codebase into conformance — naming, brace style, comment blocks, file headers. The program's behavior is deliberately **unchanged**, and students verify that by running the same test inputs against v1.3 and v2.0 and diffing the output. That exercise is the chapter's real lesson: a refactor that alters behavior is a defect, and the only way to know is to have tests. v2.0 also adds a small visible feature — an About screen reporting version, author, and build date — so students end the chapter with something new they can see, not only something tidier.

**Key terms:** lifecycle, requirements, analysis, design, implementation, integration, maintenance, waterfall, iterative, agile, coding standard, refactoring, version control, technical debt

**Accessibility notes:** Lifecycle diagrams are supplemented by an ordered list of phases with inputs and outputs, so the sequence is available without the figure.

---

## Chapter 14 — Structs: Grouping Related Data

**Objectives:** SLO 2.2, 2.6, 2.8

**Sections**

14.1 The Problem with Parallel Arrays
14.2 Declaring and Using a `struct`
14.3 Member Access
14.4 Structs and Functions
14.5 Arrays and Vectors of Structs
14.6 Nested Structs
14.7 Structs, References, and `const`
14.8 Designing Records from Requirements
14.9 Structs as a Bridge to Classes

**Grade Calculator v2.1 — Student Records.** Every parallel-array pair from Course I collapses into a struct: `Student` (name, ID, scores), `Assignment` (name, points earned, points possible, bonus points), and `GradeTier` (cutoff, letter) — the last replacing the parallel cutoff and letter arrays from Chapter 11 with a single `std::vector<GradeTier>`. The roster becomes `std::vector<Student>`. Students compare the before and after line counts and identify which classes of bug — mismatched array lengths, index drift between parallel arrays — have become structurally impossible rather than merely unlikely.

**Key terms:** `struct`, member, record, aggregate, member access operator, nested struct, aggregate initialization, plain old data

**Accessibility notes:** Record-layout figures are given as tables of member name, type, and purpose.

---

## Chapter 15 — File Streams and Persistent Data

**Objectives:** SLO 2.1, 2.4, 2.6

**Sections**

15.1 Streams as an Abstraction
15.2 Output File Streams
15.3 Input File Streams
15.4 Checking Stream State
15.5 Reading Line by Line and Parsing Fields
15.6 Delimited Text Formats
15.7 Formatting Output with Manipulators
15.8 String Streams
15.9 Designing a File Format
15.10 Robust File Handling

**Grade Calculator v2.2 — Save and Load.** Rosters, assignments, and the custom grade scale all persist to CSV and load on startup — so an instructor's letter-grade scheme survives between sessions. Students design and document the file format, decide how to represent bonus points in it, and handle missing or malformed files gracefully. The format must be forward-looking enough to accommodate weighted grading later; students discover in Chapter 21 whether their design actually was.

**Key terms:** stream, `ofstream`, `ifstream`, `fstream`, stream state, `eof`, `fail`, delimiter, parsing, manipulator, `stringstream`, serialization

**Accessibility notes:** Sample file contents appear in captioned blocks labeled as data, clearly distinguished from source listings.

---

## Chapter 16 — Debugging and Testing

**Objectives:** SLO 2.7, 2.4, 2.1

Placed early in Course II so the debugger is a tool students use for the rest of the book, not an appendix.

**Sections**

16.1 Categories of Defects Revisited
16.2 A Systematic Debugging Process
16.3 The Symbolic Debugger
  16.3.1 Breakpoints
  16.3.2 Stepping: Into, Over, and Out
  16.3.3 Inspecting Variables and Expressions
  16.3.4 The Call Stack
  16.3.5 Watchpoints and Conditional Breakpoints
16.4 Debugging Run-Time Errors
16.5 Debugging Logic Errors
16.6 Diagnostic Output and Assertions
16.7 Writing Test Cases
16.8 Boundary and Edge Case Testing
16.9 Regression Testing
16.10 Documenting Defects and Fixes

**Grade Calculator v2.3 — Defect Hunt.** Students are given an intentionally broken build of the Grade Calculator and must locate three seeded defects using breakpoints and the call stack: an out-of-range access when the grade scale does not cover a percentage, a bonus-point value added to points possible as well as points earned, and an off-by-one in the tier loop that returns the wrong letter exactly at a cutoff. Each is invisible on typical input and obvious on boundary input — which is the lesson. Students write a defect report and a regression test for each.

**Key terms:** debugger, breakpoint, watchpoint, step into, step over, call stack, stack frame, watch expression, assertion, test case, boundary value, regression test, defect report

**Accessibility notes:** Debugger instruction is written as numbered keyboard-and-menu steps, not screenshots alone. Every screenshot is accompanied by an equivalent textual procedure.

---

## Chapter 17 — Searching and Sorting

**Objectives:** SLO 2.5, 2.6, 2.8

**Sections**

17.1 Why Algorithm Choice Matters
17.2 Linear Search
17.3 Binary Search and the Sorted Precondition
17.4 Comparing Search Performance
17.5 Selection Sort
17.6 Insertion Sort
17.7 Bubble Sort and Its Reputation
17.8 Merge Sort: Divide and Conquer
17.9 Introducing Algorithm Efficiency
17.10 Sorting by Different Criteria
17.11 Library Sorting and Searching

**Grade Calculator v2.4 — Rankings.** Sorts the roster by name, by course percentage, and by letter grade, using a comparison function selected at run time. Adds a search-by-ID feature, implemented first linearly, then with binary search on a sorted roster; students measure and report the difference. The grade-scale lookup from Chapter 11 is revisited as a search problem — a linear scan over tiers is fine for five tiers and worth binary search for fifty, which grounds the efficiency discussion in the students' own code.

**Key terms:** linear search, binary search, precondition, selection sort, insertion sort, bubble sort, merge sort, divide and conquer, comparison function, stability, efficiency, `std::sort`, `std::find`

**Accessibility notes:** Each sort is traced as a table of array states per pass, so the algorithm is followable without animation.

---

## Chapter 18 — Classes and Objects

**Objectives:** SLO 2.2, 2.3, 2.8

**Sections**

18.1 From Struct to Class
18.2 Objects, State, and Behavior
18.3 Instance Variables
18.4 Member Functions
18.5 Access Specifiers and Encapsulation
18.6 Constructors
18.7 Default and Parameterized Constructors
18.8 Accessors and Mutators
18.9 The Destructor
18.10 Object Lifetime
18.11 Identifying Classes from Requirements

**Grade Calculator v2.5 — Student and GradeScale Classes.** The `Student` struct becomes a class with private data, a constructor, accessors, and behavior — `addAssignment`, `totalPointsEarned`, `percentage`. The `GradeTier` vector becomes a `GradeScale` class that owns its tiers and enforces its own invariants in the constructor: cutoffs descending, no gaps, full coverage of 0 to 100 and above. The validation students wrote as loose free functions in Chapter 11 now lives where it cannot be bypassed, and an invalid `GradeScale` object simply cannot be constructed. Students identify each Course I bug that this makes unreachable.

**Key terms:** class, object, instance, instance variable, member function, method, `public`, `private`, encapsulation, information hiding, constructor, destructor, accessor, mutator, invariant, lifetime

**Accessibility notes:** UML-style class diagrams are paired with a members table listing name, visibility, type, and purpose.

---

## Chapter 19 — Refining Classes

**Objectives:** SLO 2.2, 2.3, 2.4

**Sections**

19.1 Passing Objects to Functions
19.2 Returning Objects
19.3 The `this` Pointer
19.4 `const` Member Functions
19.5 Separating Declaration from Definition
19.6 Header Guards and Multiple Inclusion
19.7 Operator Overloading
  19.7.1 Operator Functions
  19.7.2 Operator Methods
  19.7.3 Overloading Stream Operators
19.8 Static Members
19.9 Friends
19.10 Classes vs. Structs
19.11 The Copy Constructor and Assignment

**Grade Calculator v2.6 — Gradebook Class.** A `Gradebook` class owns the roster and the `GradeScale` and exposes the operations. `operator<<` prints a formatted report for a `Student` and for the whole `Gradebook`; `operator[]` retrieves a student by index; `operator<` on `Student` enables sorting by percentage. Each class moves into its own header and implementation file pair with guards, and the accessors that never mutate — `percentage`, `letterFor`, `size` — are marked `const`.

**Key terms:** `this`, `const` method, header guard, `#pragma once`, operator overloading, operator method, `friend`, static member, copy constructor, assignment operator, interface, implementation

**Accessibility notes:** File-organization diagrams are restated as a directory listing with a purpose column.

---

## Chapter 20 — Inheritance

**Objectives:** SLO 2.3, 2.8

**Sections**

20.1 A New Requirement: Weighted Grading
20.2 Two Designs Compared: Flags and Branches vs. a Class Hierarchy
20.3 Modeling "Is-A" Relationships
20.4 Base and Derived Classes
20.5 Inheritance Mechanics and Syntax
20.6 Constructors Under Inheritance
20.7 `protected` Members
20.8 Overriding Member Functions
20.9 Multilevel Hierarchies
20.10 Composition as an Alternative
20.11 Designing a Hierarchy from Requirements
20.12 When Not to Inherit

**Grade Calculator v3.0 — Weighted Grading.** Section 20.1 introduces the requirement: Exams count 50%, Homework 30%, Participation 20%, with each category's percentage computed separately before being combined.

Section 20.2 then shows two designs side by side, both written by the book. The first threads a scheme flag through `Gradebook` and branches inside every calculation; the second uses a small class hierarchy. Roughly thirty lines of each are printed together, and the costs of the flag version are named concretely — every future scheme touches every function, the branches cannot be tested independently, and adding a third scheme means editing code that already works. Students read and analyze this comparison; they are not asked to build the version the book is arguing against.

They then implement the hierarchy directly. Assignments gain a `Category` (name and weight). A `GradingScheme` base class is defined with `PointsBased` and `Weighted` derived classes, each computing a course percentage from the same `std::vector<Assignment>` by its own rule. Bonus points and the `GradeScale` are shared and require no changes at all — the return on the encapsulation work from Chapter 18, and something students can verify by diffing their own files.

*Complete at the end of this chapter:* v3.0 asks the user which scheme to use at startup, constructs the matching object once, and runs to completion with it. Weighted grading genuinely works — category weights are entered, validated to total 100%, and applied. What v3.0 cannot yet do is switch schemes without restarting, because the selection lives in a single `if` at construction rather than in the type system. That limitation is stated in the chapter and in the code, and Chapter 21 removes it. The program is feature-limited, not unfinished.

**Key terms:** inheritance, base class, derived class, superclass, subclass, `protected`, override, is-a, has-a, composition, hierarchy, initializer list

**Accessibility notes:** Hierarchy diagrams are paired with a nested list showing the same parent-child structure.

---

## Chapter 21 — Polymorphism

**Objectives:** SLO 2.3, 2.8

**Sections**

21.1 The Problem Polymorphism Solves
21.2 Virtual Functions
21.3 Dynamic Binding
21.4 Base Class Pointers and References
21.5 Abstract Classes and Pure Virtual Functions
21.6 Virtual Destructors
21.7 Polymorphic Collections
21.8 Runtime Type Information
21.9 I/O Streams as an Inheritance Case Study
21.10 Design Patterns in Brief: Adapter and Strategy
21.11 Costs and Trade-offs of Polymorphism

**Grade Calculator v3.1 — Two Schemes, Chosen at Run Time.** `GradingScheme` becomes an abstract base class with a pure virtual `computePercentage(const std::vector<Assignment>&) const` and a virtual destructor. `Gradebook` holds a `GradingScheme*` and never asks which scheme it has — the branching from the flag design in Section 20.2 is gone entirely, replaced by dynamic dispatch.

The user now selects points-based or weighted at startup, or switches mid-session and sees every student's grade recomputed. Students then prove the design by adding a third scheme — weighted-with-lowest-dropped-per-category — and confirming that `Gradebook`, `Student`, `GradeScale`, and the report code compile unchanged. They also return to their Chapter 15 file format and determine whether it can store category weights, or whether it must be revised; either outcome is a legitimate lesson in interface design.

Both schemes honor bonus points, custom letter scales, and named assignments — the features carried the whole way from Course I.

**Key terms:** polymorphism, `virtual`, dynamic binding, static binding, vtable, abstract class, pure virtual function, virtual destructor, slicing, upcast, downcast, design pattern

**Accessibility notes:** Dispatch diagrams are accompanied by a prose walkthrough naming the object type, the called function, and the resolved implementation for each case.

---

## Chapter 22 — Memory Management and Smart Pointers

**Objectives:** SLO 2.1, 2.7, 2.8

**Sections**

22.1 Memory Regions: Stack, Heap, Static, Code
22.2 Automatic vs. Dynamic Storage
22.3 `new` and `delete`
22.4 Memory Leaks and Dangling Pointers
22.5 Building a Linked List
22.6 Resource Management and RAII
22.7 The Rule of Three
22.8 Move Semantics in Brief
22.9 Smart Pointers: `unique_ptr` and `shared_ptr`
22.10 Debugging Memory Errors

**Grade Calculator v3.2 — Safe Ownership.** The raw `GradingScheme*` held by `Gradebook` is replaced with `std::unique_ptr<GradingScheme>`.

The framing matters here, because the obvious version of this lesson is dishonest. **v3.1 does not leak.** Its raw-pointer ownership is correct — but only because `Gradebook` also writes a destructor, deletes the old scheme inside `setScheme`, and disables copying. Three separate pieces of hand-written bookkeeping, each of which must be remembered.

So the chapter does not ask students to find a leak the book planted in their own code. It asks them to *delete one of those three lines* from a copy of v3.1 and rerun under AddressSanitizer, which reports the leak immediately. Then they convert to `unique_ptr` and find that all three lines can be removed at once, because there is nothing left to remember. The lesson lands as *v3.1 is correct because its author was careful; v3.2 is correct because it cannot be written wrong* — which is the actual argument for RAII, and a stronger one than "here is a bug we gave you."

Behavior is identical between the two versions, and both are leak-free as shipped.

**Key terms:** stack, heap, dynamic allocation, `new`, `delete`, memory leak, dangling pointer, linked list, node, RAII, rule of three, move semantics, `unique_ptr`, `shared_ptr`, ownership

**Accessibility notes:** Stack and heap diagrams need long descriptions listing each allocation, its region, and its lifetime.

---

## Chapter 23 — Templates and the Standard Template Library

**Objectives:** SLO 2.5, 2.6, 2.8

**Sections**

23.1 The Case for Generic Code
23.2 Function Templates
23.3 Class Templates
23.4 STL Containers Overview
23.5 Iterators and Iterator Ranges
23.6 `std::map` and `std::set`
23.7 Standard Algorithms
23.8 Lambda Functions
23.9 Namespaces
23.10 Choosing the Right Container

**Grade Calculator v3.3 — Generic and Indexed.** A `Statistics<T>` template computes mean, median, and standard deviation for any numeric type. Student lookup moves to `std::map<int, Student>` keyed by ID. Assignments are grouped by category with `std::map<std::string, std::vector<Assignment>>`, which simplifies the weighted scheme considerably. Custom sorts are rewritten as lambdas passed to `std::sort`, and the letter-grade distribution across the class is computed with a counting map.

**Key terms:** template, type parameter, instantiation, generic programming, container, iterator, iterator range, `std::map`, `std::set`, algorithm, lambda, capture, namespace

**Accessibility notes:** The container-comparison table is a real data table with a header row naming each performance characteristic.

---

## Chapter 24 — Exceptions, Release, and the Road Ahead

**Objectives:** SLO 2.1, 2.4, 2.9

Closes the book by revisiting translation from Chapter 2 with full understanding, and shipping the project.

**Sections**

24.1 Why Return Codes Are Not Enough
24.2 `throw`, `try`, and `catch`
24.3 Standard Exception Types
24.4 Custom Exception Classes
24.5 Catching Multiple Exceptions
24.6 Exception Safety and Cleanup
24.7 When to Use Exceptions
24.8 Program Translation Revisited
  24.8.1 Preprocessing, Compilation, Assembly, Linking
  24.8.2 Separate Compilation and Build Systems
  24.8.3 Static and Dynamic Libraries
  24.8.4 Debug vs. Release Builds
24.9 Preparing a Release: Documentation and User Guide
24.10 Maintenance and Future Enhancement
24.11 Where to Go Next

**Grade Calculator v4.0 — Release.** Input, file, and range errors are converted to exceptions with a custom `GradebookError` hierarchy — `InvalidScaleError` for a malformed letter scale, `WeightSumError` when category weights do not total 100%, `FileFormatError` for a corrupt gradebook file.

Students produce a release build, a README, a user guide covering both grading schemes, and a final design document reconciled against the Chapter 5 original. That reconciliation is the capstone deliverable: the Chapter 5 specification explicitly deferred weighted grading, and students now account for how that deferred requirement was analyzed in Chapter 13, attempted procedurally in Chapter 20, and solved polymorphically in Chapter 21 — a documented, traceable requirement followed across two courses and twenty-four chapters.

**Key terms:** exception, `throw`, `try`, `catch`, `std::exception`, exception safety, stack unwinding, static library, dynamic library, debug build, release build, user documentation, maintenance

**Accessibility notes:** The exception-propagation figure needs a prose description of the call stack at throw and at each catch level.

---

## Appendices

**Appendix A — Setting Up Your Development Environment.** Per-platform setup for a modern compiler, editor, and debugger, written as numbered text procedures with screenshots as supplements, never as the sole instruction.

**Appendix B — Command-Line Development.** Compiling, linking, and running from a terminal; introduction to build files.

**Appendix C — Debugger Reference Card.** Common commands and shortcuts across the major debuggers, presented as a table.

**Appendix D — Coding Standard and Style Guide.** The formatting and documentation conventions used throughout the book, supporting SLO 2.4.

**Appendix E — Grade Calculator: Complete Source by Chapter.** Full compilable listings for all twenty-three versions (v0.1 through v4.0), each with the sample session it produces. Because every version runs, a student who falls behind can rejoin at the start of any chapter with a known-good build, and an instructor can assign any chapter without requiring the previous one to have been completed successfully. Each listing is accompanied by its test inputs and expected output so correctness can be checked without reading the code.

**Appendix F — Glossary.** All key terms, alphabetized, cross-linked to their defining chapters.

**Appendix G — SLO-to-Chapter Coverage Matrix.** A grid mapping every outcome to the chapters, project milestones, and Try It Yourself examples that address it, for accreditation reporting. Because exercises are generated rather than authored, this matrix points to the source material each outcome is taught from, and the generated exercise sets inherit that mapping.

---

## Coverage Verification

**Course I outcomes**

| Outcome | Primary chapters | Assessed in |
|---|---|---|
| SLO 1.1 Data representation | 1, 3, 4 | Ch 1 Try It Yourself; Ch 3 type-justification writeup |
| SLO 1.2 Language categories | 1, 2 | Ch 1 comparison essay |
| SLO 1.3 Types, structured programming, algorithmic and UI design | 3, 4, 5, 6, 7, 12 | Ch 5 design document; Ch 6–7 projects |
| SLO 1.4 Methodologies, pseudocode, flowcharts, structure charts, control structures, functions, arrays | 5, 6, 7, 9, 10, 11 | Ch 5 and Ch 9 milestone deliverables |
| SLO 1.5 Projects from specifications | 5, 9, 11, 12 | Grade Calculator v1.0 and v1.3 |
| SLO 1.6 Design, code, test, document | 4, 5, 9, 10 | Ch 9 test plan; Ch 12 capstone |
| SLO 1.7 Apply concepts to new problems | 6, 7, 8, 9, 10, 11, 12 | Try It Yourself variations; Grade Calculator milestones |

**Course II outcomes**

| Outcome | Primary chapters | Assessed in |
|---|---|---|
| SLO 2.1 Development lifecycle | 13, 15, 22, 24 | Ch 13 lifecycle plan; Ch 24 final reconciliation |
| SLO 2.2 Structs and classes | 14, 18, 19 | Grade Calculator v2.1 and v2.5 |
| SLO 2.3 Inheritance and polymorphism | 18, 20, 21 | Grade Calculator v3.0 and v3.1 |
| SLO 2.4 Consistent documentation and formatting | 13, 16, 19, 24 | Style audit at each milestone |
| SLO 2.5 Searching and sorting | 17, 23 | Ch 17 rankings feature |
| SLO 2.6 Single- and multi-dimensional arrays | 11, 12, 14, 15, 23 | Ch 11 roster; Ch 14 records |
| SLO 2.7 Symbolic debugger | 16, 22 | Ch 16 defect hunt; Ch 22 leak investigation |
| SLO 2.8 Programming methodologies | 13, 14, 17, 18, 20, 21, 23 | Ch 13 comparison; Ch 21 refactor |
| SLO 2.9 Program translation phases | 2, 24 | Ch 2 pipeline walkthrough; Ch 24 build lab |

---

## Notes on Departures from Halterman

- **New Chapter 1** covers data representation and language categorization, which Halterman treats only briefly. SLO 1.1 and 1.2 require it.
- **New Chapter 5** front-loads pseudocode, flowcharting, and structure charts before control structures. Halterman has no equivalent; SLO 1.4 names all three explicitly.
- **New Chapter 13** on the SDLC opens Course II. SLO 2.1 requires it and it gives the second course a coherent frame.
- **New Chapter 16** on debugging and testing is promoted to a full chapter. Halterman scatters this material; SLO 2.7 requires deliberate instruction in a symbolic debugger.
- **Structs get their own Chapter 14**, before classes. SLO 2.2 names structs alongside classes, and they are the natural bridge from Course I records to Course II objects.
- **Arrays precede vectors** (Ch 11 before Ch 12), reversing Halterman, because SLO 2.6 requires explicit competence with single- and multi-dimensional arrays.
- **Halterman's Chapters 6 and 7** (iteration; other conditional and iterative statements) are merged into Chapters 6 and 7 here, grouping all selection together and all repetition together.
- **File streams move earlier** (Ch 15) to enable persistence in the running project well before the OO material.
- **STL and associative containers** are consolidated into Chapter 23 rather than spread across three chapters, keeping the total at 24.

---

## Design Rationale: Why One Grading Scheme in Course I

Halterman's running examples are self-contained per chapter. A single project spanning two courses needs something his structure does not supply: a reason for the object-oriented material to exist.

Restricting Course I to points-based grading supplies it. The argument:

**Procedural code should be allowed to look good.** If Course I already handled two grading schemes, students would meet flags, branches, and duplicated logic while still calling that "how programming works." A single scheme lets procedural design be genuinely appropriate for the problem — which is honest, because it is.

**The second scheme is a real requirement, not a contrivance.** Weighted grading is how most actual courses work. Students are not asked to accept an artificial extension; they are asked to handle the requirement their own institution uses.

**The requirement is planted early and tracked.** It appears as an explicit out-of-scope note in the Chapter 1 requirements statement, is carried in the Chapter 5 design document, is formally analyzed in the Chapter 13 lifecycle plan, and is designed and built in Chapters 20 and 21. That trail is itself the evidence for SLO 2.1 — students do not read about requirements traceability, they produce a two-course example of it.

**Motivation comes from reading, not from failing.** Every student-written version of the project is one they keep and build on. Where the book needs to argue for a design, it prints the alternative itself and analyzes it (Section 20.2) rather than assigning students to write code that will be thrown away. Students get the comparison without spending a session on a dead end, and no milestone deliverable is ever discarded work.

**Shared features prove encapsulation pays.** Custom letter scales, assignment names, and bonus points exist in both courses. When the grading scheme is generalized in Chapter 21, those components — properly encapsulated in Chapters 18 and 19 — require no changes at all. Students see directly that good boundaries absorb change, which is a claim usually asserted rather than demonstrated.

**Known limitations are disclosed, not hidden.** Where a chapter teaches something a later chapter improves — raw-pointer ownership in Chapter 21, superseded by smart pointers in Chapter 22; startup-only scheme selection in Chapter 20, made dynamic in Chapter 21 — the book says so at the time and explains why the simpler form comes first. Students are never surprised to learn that code they were taught was quietly wrong.

**No version ships a defect the book planted.** Every version in Appendix E is correct for the features it has, including the ones a later chapter improves. Where a chapter needs students to *see* a failure, they induce it themselves by removing something from a working build — as in Chapter 22, where deleting one line from the correct v3.1 produces an immediate, observable leak. The one exception is Chapter 16's `broken.cpp`, which is clearly labeled as a debugging lab, distributed separately from the student's own project, and never something they built.

**Missing features, never missing endings.** The completeness rule stated above is what makes staged development safe. Because every chapter's version runs, "not yet implemented" is always a visible, documented gap in a working program rather than a build that does not compile. Students can always demonstrate what they have, instructors can always grade it, and a student who struggles with one chapter starts the next from a known-good build in Appendix E instead of falling permanently behind.
