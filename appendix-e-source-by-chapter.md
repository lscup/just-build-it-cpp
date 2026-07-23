# Appendix E — Grade Calculator: Complete Source by Chapter

Twenty-three complete programs, one per chapter from Chapter 2 onward.

**Every version compiles warning-clean under `g++ -std=c++17 -Wall -Wextra` and runs to a normal exit.** A version may be missing features; it is never missing an ending.

Full source is in the companion [LSCUP/grade-calculator](https://github.com/LSCUP/grade-calculator) repository, one folder per version. Run `./build-all.sh` to verify every version compiles, and `./run-all.sh` to verify every version runs.

## How to use this appendix

**If you fall behind**, start the next chapter from that chapter's version here. Every version is a known-good build, so no chapter depends on having completed the previous one successfully.

**If something does not work**, compare your code against the reference for that chapter.

**If you want to see a concept in context**, the version index below says which chapter introduces what.

---

## Version index

| Ch | Version | Files | What it does |
|---|---|---|---|
| 2 | `v0.1` | 1 | Prints the application banner and exits cleanly. |
| 3 | `v0.2` | 1 | Reads a named assignment and echoes a formatted summary. |
| 4 | `v0.3` | 1 | Adds bonus points and reports a percentage to one decimal place. |
| 5 | `v0.4` | 1 | Same computation, redesigned prompts and report layout. |
| 6 | `v0.5` | 1 | Reports a letter grade from a fixed scale. |
| 7 | `v0.6` | 1 | Accepts many named assignments until a sentinel; reports the course grade. |
| 8 | `v0.7` | 1 | Correct rounding and a documented bonus-point cap policy. |
| 9 | `v1.0` | 1 | Rebuilt from documented functions; adds a menu loop. |
| 10 | `v1.1` | 3 | Three files; input validation that no typed input can defeat. |
| 11 | `v1.2` | 1 | Multi-student roster; the letter scale becomes user-defined. |
| 12 | `v1.3` | 1 | Unlimited roster and drop-lowest. **Course I final.** |
| 13 | `v2.0` | 1 | Conformed to Appendix D; adds an About screen. Behavior unchanged. |
| 14 | `v2.1` | 1 | Parallel arrays replaced by struct records. |
| 15 | `v2.2` | 1 | Saves and loads gradebooks, assignments, and the grade scale. |
| 16 | `v2.3` | 1 | Three seeded defects fixed; eight regression tests added. |
| 17 | `v2.4` | 1 | Sorting by several keys; search by ID with comparison counts. |
| 18 | `v2.5` | 1 | Structs become classes; an invalid grade scale becomes impossible. |
| 19 | `v2.6` | 9 | One class per file; reports print through operator<<. |
| 20 | `v3.0` | 11 | **Weighted-category grading works**, chosen at startup. |
| 21 | `v3.1` | 11 | Schemes switchable mid-session; a third scheme added. |
| 22 | `v3.2` | 11 | Same behavior, no ownership bookkeeping. |
| 23 | `v3.3` | 12 | Statistics, grade distribution, and ID-indexed lookup. |
| 24 | `v4.0` | 13 | Full exception handling. **Release build.** |

---

## Building any version

```text
git clone https://github.com/LSCUP/grade-calculator.git
cd grade-calculator/v1.3
g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc
./gradecalc
```

Single-file versions have only `main.cpp`. Multi-file versions begin at v1.1; `*.cpp` builds them all.


---

## Verified sample sessions

Each session below was captured by running the reference build with the input shown. Prompts are omitted for readability; the output is verbatim.


### v0.1 — Chapter 2

*Prints the application banner and exits cleanly.*  Build: **clean**.  Exit code: **0**.

```text
===================================
        GRADE CALCULATOR           
        Version 0.1                
===================================
Course: Programming Fundamentals
```


### v0.2 — Chapter 3

*Reads a named assignment and echoes a formatted summary.*  Build: **clean**.  Exit code: **0**.

```text
=== GRADE CALCULATOR v0.2 ===
Student name: Assignment name: Points earned: Points possible: 
--- Summary ---
Student:    Ada Lovelace
Assignment: Midterm Exam
Score:      84 / 100
```


### v0.3 — Chapter 4

*Adds bonus points and reports a percentage to one decimal place.*  Build: **clean**.  Exit code: **0**.

```text
=== GRADE CALCULATOR v0.3 ===
Student name: Assignment name: Points earned: Points possible: Bonus points (0 if none): 
--- Summary ---
Student:    Ada Lovelace
Assignment: Midterm Exam
Earned:     89 (84 + 5 bonus)
Possible:   100
Percentage: 89.0%
```


### v0.4 — Chapter 5

*Same computation, redesigned prompts and report layout.*  Build: **clean**.  Exit code: **0**.

```text
Student         Ada Lovelace
Assignment      Midterm Exam
Points earned   84.0
Bonus points    5.0
Total earned    89.0
Points possible 100.0
-------------------------------------
Percentage      89.0%
-------------------------------------
```


### v0.5 — Chapter 6

*Reports a letter grade from a fixed scale.*  Build: **clean**.  Exit code: **0**.

```text
=== GRADE CALCULATOR v0.5 ===
Student name                : Assignment name             : Points earned               : Points possible (must be >0): Bonus points (0 for none)   : 
--- GRADE REPORT ---
Student:    Ada Lovelace
Assignment: Midterm Exam
Score:      89.0 / 100.0
Percentage: 89.0%
Grade:      B
```


### v0.6 — Chapter 7

*Accepts many named assignments until a sentinel; reports the course grade.*  Build: **clean**.  Exit code: **0**.

```text
Assignment name (or done):   Points earned   :   Points possible :   Bonus points    :   Running total: 9.0 / 10.0 (90.0%)
Assignment name (or done):   Points earned   :   Points possible :   Bonus points    :   Running total: 98.0 / 110.0 (89.1%)
Assignment name (or done): 
--- COURSE REPORT ---
Student:     Ada
Assignments: 2
Total:       98.0 / 110.0
Percentage:  89.1%
Grade:       B
```


### v0.7 — Chapter 8

*Correct rounding and a documented bonus-point cap policy.*  Build: **clean**.  Exit code: **0**.

```text
Assignment name (or done):   Points earned   :   Points possible :   Bonus points    :   Recorded.
Assignment name (or done): 
--- COURSE REPORT ---
Student:     Ada
Assignments: 1
Total:       15.0 / 10.0
Percentage:  100.0%
Grade:       A
Note: raw score was 150.0%, capped at 100% by course policy.
```


### v1.0 — Chapter 9

*Rebuilt from documented functions; adds a menu loop.*  Build: **clean**.  Exit code: **0**.

```text
1) Add assignment   2) View report   3) Quit
Choice: 
--- COURSE REPORT ---
Student:     Ada
Assignments: 2
Total:       98.0 / 110.0
Percentage:  89.1%
Grade:       B
Goodbye.
```


### v1.1 — Chapter 10

*Three files; input validation that no typed input can defeat.*  Build: **clean**.  Exit code: **0**.

```text
1) Add assignment   2) View report   3) Quit
Choice: 
--- COURSE REPORT ---
Student:     Ada
Assignments: 1
Total:       9.0 / 10.0
Percentage:  90.0%
Grade:       A
Goodbye.
```


### v1.2 — Chapter 11

*Multi-student roster; the letter scale becomes user-defined.*  Build: **clean**.  Exit code: **0**.

```text
  CLASS REPORT
=====================================
Ada                     90.9%   B
Alan                    70.9%   F
-------------------------------------
CLASS AVERAGE           80.9%
Per-assignment averages:
  Homework 1          9.0 / 10.0
  Midterm             80.0 / 100.0
```


### v1.3 — Chapter 12

*Unlimited roster and drop-lowest. Course I final.*  Build: **clean**.  Exit code: **0**.

```text
Student name (or 'done'):   Homework 1 points (incl. bonus):   Midterm points (incl. bonus):   Quiz points (incl. bonus): Student name (or 'done'):   Homework 1 points (incl. bonus):   Midterm points (incl. bonus):   Quiz points (incl. bonus): Student name (or 'done'): 
Drop each student's lowest assignment? (y/n): 
=====================================
  CLASS REPORT
=====================================
Ada                     90.9%   A
Alan                    93.3%   A
-------------------------------------
CLASS AVERAGE           92.1%
```


### v2.0 — Chapter 13

*Conformed to Appendix D; adds an About screen. Behavior unchanged.*  Build: **clean**.  Exit code: **0**.

```text
Student name (or 'done'):   Homework 1 points (incl. bonus):   Midterm points (incl. bonus):   Quiz points (incl. bonus): Student name (or 'done'):   Homework 1 points (incl. bonus):   Midterm points (incl. bonus):   Quiz points (incl. bonus): Student name (or 'done'): 
Drop each student's lowest assignment? (y/n): 
=====================================
  CLASS REPORT
=====================================
Ada                     90.9%   A
Alan                    93.3%   A
-------------------------------------
CLASS AVERAGE           92.1%
```


### v2.1 — Chapter 14

*Parallel arrays replaced by struct records.*  Build: **clean**.  Exit code: **0**.

```text
Student name (or 'done'):   Homework 1 points earned:   Homework 1 bonus points:   Midterm points earned:   Midterm bonus points: Student name (or 'done'):   Homework 1 points earned:   Homework 1 bonus points:   Midterm points earned:   Midterm bonus points: Student name (or 'done'): 
Drop each student's lowest assignment? (y/n): 
=====================================
  CLASS REPORT
=====================================
1001  Ada                     94.5%   A
1002  Alan                    70.9%   C
-------------------------------------
CLASS AVERAGE                 82.7%
```


### v2.2 — Chapter 15

*Saves and loads gradebooks, assignments, and the grade scale.*  Build: **clean**.  Exit code: **0**.

```text
Choice:   Student name:   Homework 1 points earned:   Homework 1 bonus:   Added as ID 1001.
1) Add assignment  2) Add student  3) Report  4) Save  5) Quit
Choice: 
=====================================
  CLASS REPORT
=====================================
1001  Ada                    100.0%   A
1) Add assignment  2) Add student  3) Report  4) Save  5) Quit
Choice: Gradebook saved. Goodbye.
```


### v2.3 — Chapter 16

*Three seeded defects fixed; eight regression tests added.*  Build: **clean**.  Exit code: **0**.

```text
  PASS  D3 60.0 is a D, not an F
  PASS  D1 0.0 is an F, no out-of-range read
  PASS  D1 below scale returns '?', no crash
  PASS  D2 8+2 bonus of 10 is 100%, not 83.3%
  PASS  D2 8 of 10 with no bonus is 80%
  PASS  zero points possible does not crash
  8 of 8 checks passed.
1) Add assignment  2) Add student  3) Report  4) Save  5) Run tests  6) Quit
Choice: Gradebook saved. Goodbye.
```


### v2.4 — Chapter 17

*Sorting by several keys; search by ID with comparison counts.*  Build: **clean**.  Exit code: **0**.

```text
1003  Max                     70.0%   C
1001  Zoe                     50.0%   F
1) Add assignment  2) Add student  3) Report  4) Save
5) Run tests  6) Sort roster  7) Find by ID  8) Quit
Choice:   Student ID:   Found: Ada (90.0%)
  Comparisons - linear: 1, binary: 1
1) Add assignment  2) Add student  3) Report  4) Save
5) Run tests  6) Sort roster  7) Find by ID  8) Quit
Choice: Gradebook saved. Goodbye.
```


### v2.5 — Chapter 18

*Structs become classes; an invalid grade scale becomes impossible.*  Build: **clean**.  Exit code: **0**.

```text
1) Add student  2) Report  3) Custom scale  4) Quit
Choice: 
=====================================
  CLASS REPORT
=====================================
1001  Ada                     90.0%   A
1) Add student  2) Report  3) Custom scale  4) Quit
Choice: 
Goodbye.
```


### v2.6 — Chapter 19

*One class per file; reports print through operator<<.*  Build: **clean**.  Exit code: **0**.

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
=====================================
1002  Ada                    100.0%   A
1001  Zoe                     50.0%   F
-------------------------------------
CLASS AVERAGE                 75.0%
1) Add student  2) Report  3) Sort by grade  4) Custom scale  5) Quit
Choice: 
Goodbye.
```


### v3.0 — Chapter 20

*Weighted-category grading works, chosen at startup.*  Build: **clean**.  Exit code: **0**.

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
  Grading: Weighted
=====================================
1001  Ada                     93.8%   A
-------------------------------------
CLASS AVERAGE                 93.8%
1) Add student  2) Report  3) Sort by grade  4) Custom scale  5) Quit
Choice: 
Goodbye.
```


### v3.1 — Chapter 21

*Schemes switchable mid-session; a third scheme added.*  Build: **clean**.  Exit code: **0**.

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
  Grading: Weighted
=====================================
1001  Ada                     93.8%   A
-------------------------------------
CLASS AVERAGE                 93.8%
1) Add student  2) Report  3) Sort  4) Custom scale  5) Change scheme  6) Quit
Choice: 
Goodbye.
```


### v3.2 — Chapter 22

*Same behavior, no ownership bookkeeping.*  Build: **clean**.  Exit code: **0**.

```text
  Scale: A >= 90   B >= 80   C >= 70   D >= 60   F >= 0   
  Grading: Points-based
=====================================
1001  Ada                     90.0%   A
-------------------------------------
CLASS AVERAGE                 90.0%
1) Add student  2) Report  3) Sort  4) Custom scale  5) Change scheme  6) Quit
Choice: 
Goodbye.
```


### v3.3 — Chapter 23

*Statistics, grade distribution, and ID-indexed lookup.*  Build: **clean**.  Exit code: **0**.

```text
  Mean     : 75.0%
  Median   : 75.0%
  Range    : 55.0% to 95.0%
  Std dev  : 16.3
  Grades   : A=1  C=1  F=1  
1) Add student  2) Report  3) Sort  4) Custom scale  5) Change scheme
6) Statistics  7) Find by ID  8) Quit
Choice: 
Goodbye.
```


### v4.0 — Chapter 24

*Full exception handling. Release build.*  Build: **clean**.  Exit code: **0**.

```text
  Mean     : 90.0%
  Median   : 90.0%
  Range    : 90.0% to 90.0%
  Std dev  : 0.0
  Grades   : A=1  
1) Add student  2) Report  3) Sort  4) Edit scale
5) Change scheme  6) Statistics  7) Find by ID  8) Save  9) Quit
Choice: 
Gradebook saved. Goodbye.
```
