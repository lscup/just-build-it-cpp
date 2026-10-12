# Chapter 18–24 lab sources

Each `chNN.py` describes one Grade Calculator lab as a list of steps. Every
code step is an explicit action — *create this file*, *find this code and
replace it with this*, *insert this below that* — whose code is taken
directly from the solution files in `lscup/grade-calculator`.

`build.py` does two things:

1. **Verifies** each lab (`check.py`): it starts from the previous version's
   solution, applies every step exactly as a student would, and requires the
   result to match the next version's solution file for file. It also
   compiles the program at every ▶ Run checkpoint with
   `g++ -std=c++17 -Wall -Wextra` and requires zero warnings.
2. **Writes** the verified labs into the chapter markdown, `studysite-labs/`,
   `local-labs/`, and the Chapter 18–24 entries of
   `lab-instructions/chapters.json`. Nothing is written if verification fails.

```bash
GRADE_CALCULATOR=/path/to/grade-calculator python3 lab-instructions/labsrc/build.py
```

Edit the `chNN.py` files, not the generated markdown. After a solution
changes, run `build.py`; a failed replay names the step that no longer
matches.
