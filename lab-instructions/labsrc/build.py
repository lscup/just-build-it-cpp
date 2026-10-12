#!/usr/bin/env python3
"""Verify the Chapter 18-24 labs against the solutions, then write them into
the textbook: the embedded chapter labs, studysite-labs/, local-labs/, and the
Chapter 18-24 entries of lab-instructions/chapters.json.

    GRADE_CALCULATOR=/path/to/grade-calculator python3 build.py
"""
import importlib, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from engine import render

CHAPTERS = range(18, 25)
mods = [f"ch{n}" for n in CHAPTERS]
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
if subprocess.run([sys.executable, os.path.join(HERE, "check.py"), *mods], cwd=HERE).returncode:
    sys.exit("verification failed - nothing written")

def standalone(md, n):
    out = []
    for l in md.splitlines():
        m = re.match(r"^(#{3,6}) (.*)", l)
        if m:
            l = (f"# Chapter {n} Lab — " + l[len("### Your StudySite Lab — "):]
                 if l.startswith("### Your StudySite Lab — ") else m.group(1)[2:] + " " + m.group(2))
        out.append(l)
    return "\n".join(out).rstrip() + "\n"

def items_after(md, heading):
    seg = md[md.index(heading) + len(heading):]
    m = re.search(r"^#### ", seg, re.M)
    seg = seg[:m.start()] if m else seg
    out, cur = [], None
    for l in seg.splitlines():
        mm = re.match(r"^(\d+\.|- \[ \]) (.*)", l)
        if mm:
            cur = [mm.group(2)]; out.append(cur)
        elif cur is not None and l.startswith("   "):
            cur.append(l.strip())
        elif not l.strip():
            cur = None
    return [" ".join(x) for x in out]

enc = lambda s: s.replace("`", "@@BT@@")
manifest_path = os.path.join(BOOK, "lab-instructions", "chapters.json")
manifest = json.load(open(manifest_path))
for n in CHAPTERS:
    mod = importlib.import_module(f"ch{n}")
    lab = render(mod.ITEMS)
    chapter = next(f for f in os.listdir(BOOK) if re.match(rf"{n}-.*\.md$", f))
    path = os.path.join(BOOK, chapter)
    text = open(path).read()
    s = text.index("### Your StudySite Lab")
    e = re.compile(r"\n---\n\n## ").search(text, s).start()
    open(path, "w").write(text[:s] + lab.rstrip("\n") + "\n\n" + text[e:])
    open(os.path.join(BOOK, "studysite-labs", f"chapter-{n}.md"), "w").write(standalone(lab, n))
    open(os.path.join(BOOK, "local-labs", f"chapter-{n}.md"), "w").write(
        standalone(render(mod.ITEMS, mode="local"), n))
    entry = next(c for c in manifest if c["chapter"] == n)
    req = items_after(lab, "#### What you will build")
    if n == 24:
        req.append("Complete only the Chapter 24 code checkpoint here. Final-project documentation, "
                   "finishing touches, and submission instructions will be provided separately.")
    entry.update(
        title=enc(re.search(r"### Your StudySite Lab — (.*)", lab).group(1)),
        start=enc(re.search(r"\*\*Starting point:\*\* (.*)", lab).group(1)),
        requirements=[enc(x) for x in req],
        verify=[enc(x) for x in items_after(lab, "Then confirm:")],
        commit=f"Complete Chapter {n} Grade Calculator {mod.TARGET}")
    print(f"wrote Chapter {n}")
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
    f.write("\n")
