import difflib
import importlib
import os
import subprocess
import sys
import tempfile

from engine import load_version, replay, render

def compile_files(files):
    with tempfile.TemporaryDirectory() as d:
        for n, t in files.items():
            open(os.path.join(d, n), "w").write(t)
        cpps = [n for n in files if n.endswith(".cpp")]
        r = subprocess.run(["g++", "-std=c++17", "-Wall", "-Wextra", *cpps, "-o", "a.out"],
                           cwd=d, capture_output=True, text=True)
        return r.returncode == 0 and not r.stderr.strip(), r.stderr

ok_all = True
for name in sys.argv[1:]:
    m = importlib.import_module(name)
    base = load_version(m.BASE)
    target = load_version(m.TARGET)
    final, snaps = replay(base, m.ITEMS)
    ok = True
    for f in sorted(set(final) | set(target)):
        if f in getattr(m, 'IGNORE', set()):
            print(f'[{name}] (ignored by design: {f})'); continue
        a, b = final.get(f), target.get(f)
        if a != b:
            ok = False
            print(f"[{name}] MISMATCH {f}")
            if a is not None and b is not None:
                sys.stdout.writelines(list(difflib.unified_diff(
                    a.splitlines(True), b.splitlines(True), "replayed", "solution"))[:60])
            else:
                print("   present in", "replay" if a else "solution", "only")
    for i, s in enumerate(snaps):
        c, err = compile_files(s)
        print(f"[{name}] run checkpoint {i+1}: {'compiles clean' if c else 'FAILS'}")
        if not c:
            ok = False
            print(err[:1500])
    md = render(m.ITEMS)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", f"{name}.md"), "w").write(md)
    print(f"[{name}] {'OK - replay matches ' + m.TARGET if ok else 'PROBLEMS'}  ({len(md.splitlines())} lines)")
    ok_all &= ok
sys.exit(0 if ok_all else 1)
