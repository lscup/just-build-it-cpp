# Appendix C — Debugger Reference Card

A one-page reference for Chapter 16. The concepts are the same in every debugger; only the gestures differ.

---

## C.1 Before You Start

**Build with `-g`.** Without it, the debugger cannot show your variable names or line numbers.

```text
g++ -std=c++17 -Wall -Wextra -g *.cpp -o gradecalc
```

Never debug an optimized build. `-O2` rearranges code, so stepping jumps unpredictably and variables may appear "optimized out."

---

## C.2 Core Commands

| Action | VS Code | gdb | What it does |
|---|---|---|---|
| Start debugging | **F5** | `run` | Run until a breakpoint |
| Continue | **F5** | `continue` | Run to the next breakpoint |
| Step Over | **F10** | `next` | Execute this line, not entering calls |
| Step Into | **F11** | `step` | Execute this line, entering the first call |
| Step Out | **Shift+F11** | `finish` | Finish this function, return to caller |
| Restart | **Ctrl+Shift+F5** | `run` | Start again from the beginning |
| Stop | **Shift+F5** | `kill` | End the debugging session |

**Step Over versus Step Into** is the distinction that matters. Step *over* a call you trust; step *into* one you suspect.

---

## C.3 Breakpoints

| Action | VS Code | gdb |
|---|---|---|
| Set at a line | Click the gutter left of the line number | `break file.cpp:42` |
| Set at a function | — | `break functionName` |
| Remove | Click the red dot again | `delete N` |
| Disable temporarily | Right-click → Disable Breakpoint | `disable N` |
| List all | Breakpoints panel | `info breakpoints` |
| **Conditional** | Right-click → Edit Breakpoint, enter a condition | `break file.cpp:42 if i > 5` |

### Useful conditions

```text
student.id == 1042
percentage >= 89.0 && percentage <= 91.0
i >= scale.size()
name == "Ada"
```

**Break on the impossible.** A conditional breakpoint on something you believe cannot happen is free if you are right and decisive if you are wrong.

---

## C.4 Inspecting State

| Want | VS Code | gdb |
|---|---|---|
| A local variable | Variables panel, or hover over the name | `print x` |
| An expression | Watch panel → **+** | `print earned / possible` |
| A container's size | Watch `scale.size()` | `print scale.size()` |
| A vector element | Expand it in Variables | `print v[2]` |
| An object's members | Expand it in Variables | `print *this` |
| Change a value | Right-click in Variables → Set Value | `set var x = 5` |

**Watch expressions are the underused feature.** Watching the exact comparison you suspect — `pct >= 90.0` — and seeing it as `true` or `false` at each step is usually faster than reasoning about it.

---

## C.5 The Call Stack

| Want | VS Code | gdb |
|---|---|---|
| See how you got here | Call Stack panel | `backtrace` |
| Inspect a caller's locals | Click that frame | `frame N` then `info locals` |
| Move up one frame | Click the frame above | `up` |
| Move down one frame | Click the frame below | `down` |

**Read the call stack every time you pause.** When a crash lands inside library code, walk down to the first frame that is *your* code and look at what it passed.

---

## C.6 Watchpoints

A watchpoint fires when a **variable changes**, rather than when a line is reached. It answers "what changed this?"

| VS Code | gdb |
|---|---|
| Right-click a variable in Variables → **Break on Value Change** | `watch totalEarned` |

Useful when a value is wrong and you do not know which of many places wrote it.

---

## C.7 A Debugging Session, Start to Finish

Following Chapter 16 Section 16.2:

1. **Reproduce.** Find input that fails reliably. Save it to a file so it is repeatable.
2. **Narrow.** Find the smallest input that still fails.
3. **Hypothesize.** State specifically what you think is wrong.
4. **Set a breakpoint** where you can first observe it — not at the top of `main`.
5. **Predict** what you expect to see, before you look.
6. **Run.** Compare what you see with what you predicted.
7. **Step** — over to survey, into to investigate.
8. **Read the call stack** to understand how you arrived.
9. **Fix the cause**, not the symptom.
10. **Write a regression test** that would have caught it.

---

## C.8 Debugging Techniques by Symptom

| Symptom | Technique |
|---|---|
| Crash | Run under the debugger; it stops at the failing line with the stack intact |
| Wrong answer, no crash | **Bisect** between a known-good point and a known-bad one |
| Fails only for one input | Conditional breakpoint on that input |
| Fails on iteration 300 | Conditional breakpoint on the loop counter |
| A value changes and you cannot see where | Watchpoint |
| Crash inside library code | Walk down the call stack to your nearest frame |
| Works in debug, fails in release | Undefined behavior — run the sanitizers |
| Cannot reproduce it at all | Log inputs until you can; an unreproducible defect cannot be verified fixed |

---

## C.9 When Not to Use a Debugger

| Instead | When |
|---|---|
| **Read the compiler messages** | The program does not build. The compiler already told you |
| **Diagnostic output** | You need to see a pattern across many iterations |
| **Assertions** | You want a condition checked continuously, not once |
| **AddressSanitizer** | Memory leaks, use-after-free, buffer overruns |
| **UndefinedBehaviorSanitizer** | Overflow, bad casts, other undefined behavior |
| **A test harness** | You want to verify many cases at once, repeatably |

```text
g++ -std=c++17 -fsanitize=address -g *.cpp -o gradecalc
g++ -std=c++17 -fsanitize=undefined -g *.cpp -o gradecalc
```

---

## C.10 Common Debugger Problems

| Symptom | Cause | Fix |
|---|---|---|
| Breakpoints show as hollow circles | Built without `-g` | Add `-g`, rebuild |
| No variable names, only addresses | Built without `-g` | Add `-g`, rebuild |
| Stepping jumps around unpredictably | Optimized build | Remove `-O2` |
| "Variable optimized out" | Optimized build | Remove `-O2` |
| Breakpoint never fires | Line never reached, or condition never true | Check the condition; break earlier |
| Debugger will not start | No `launch.json` | Appendix A Section A.4 |
| Program exits immediately | It ran to completion before your breakpoint | Break earlier |
| Stack shows only `??` | Debug information missing from part of the build | Rebuild everything with `-g` |
