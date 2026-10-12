"""Lab engine: one source drives both the rendered Markdown lab and a
mechanical replay that proves the steps turn version N-1 into version N."""
import os
import re

SOL = os.environ.get("GRADE_CALCULATOR", os.path.join(os.path.dirname(__file__), "..", "..", "..", "grade-calculator"))


def sol(ver, fname):
    with open(os.path.join(SOL, ver, fname)) as f:
        return f.read()


def seg(ver, fname, start, end, end_occurrence=1):
    """Lines from the first line containing `start` through the
    end_occurrence-th following line containing `end` (inclusive)."""
    lines = sol(ver, fname).splitlines(keepends=True)
    i = next(k for k, l in enumerate(lines) if start in l)
    count = 0
    for j in range(i, len(lines)):
        if end in lines[j]:
            count += 1
            if count == end_occurrence:
                return "".join(lines[i:j + 1])
    raise ValueError(f"end marker {end!r} not found in {ver}/{fname}")


def lines(ver, fname, a, b):
    """1-based inclusive line range."""
    ls = sol(ver, fname).splitlines(keepends=True)
    return "".join(ls[a - 1:b])


# ---------------------------------------------------------------- actions
class Md:
    def __init__(self, text):
        self.text = text.strip("\n") + "\n"


class Create:
    def __init__(self, fname, content, intro=None):
        self.fname, self.content, self.intro = fname, content, intro


class Replace:
    def __init__(self, fname, old, new, intro=None, after=None):
        self.fname, self.old, self.new, self.intro, self.after = fname, old, new, intro, after


class Delete:
    def __init__(self, fname, old, intro=None):
        self.fname, self.old, self.intro = fname, old, intro


class DeleteRange:
    """Delete from the line equal to `start` through the next line equal to `end`."""
    def __init__(self, fname, start, end, intro=None, between=None, new=None, after=None,
                 last=False, exclusive=False, end_text=None):
        self.fname, self.start, self.end = fname, start, end
        self.intro, self.between, self.new, self.after = intro, between, new, after
        self.last, self.exclusive, self.end_text = last, exclusive, end_text


class InsertAfter:
    def __init__(self, fname, anchor, new, intro=None):
        self.fname, self.anchor, self.new, self.intro = fname, anchor, new, intro


class InsertBefore:
    def __init__(self, fname, anchor, new, intro=None):
        self.fname, self.anchor, self.new, self.intro = fname, anchor, new, intro


class Append:
    """Add a blank line and then `new` at the very end of a file."""
    def __init__(self, fname, new, intro=None):
        self.fname, self.new, self.intro = fname, new, intro


class Run:
    def __init__(self, text):
        self.text = text


# ---------------------------------------------------------------- rendering
def code(text, lang="cpp"):
    return f"```{lang}\n{text.rstrip(chr(10))}\n```\n"


LOCAL_SUBS = []   # (old, new) pairs applied to Md text in local mode


def _first_sentence_dropped(text):
    """Drop the leading 'click Run' sentence of a Run checkpoint."""
    import re as _re
    parts = _re.split(r'(?<=\.)\s+', text, maxsplit=1)
    return parts[1] if len(parts) > 1 and "**Run**" in parts[0] else text


def render(items, mode="studysite", build_cmd="g++ -std=c++17 -Wall -Wextra *.cpp -o gradecalc"):
    out = []
    for it in items:
        if isinstance(it, Md):
            t = it.text
            if mode == "local":
                t = getattr(it, "local_text", None) or t
                for a, b in LOCAL_SUBS:
                    t = t.replace(a, b)
            out.append(t)
        elif isinstance(it, Create):
            out.append(it.intro or
                       f"Create a new file named `{it.fname}` and enter this code:")
            out.append(code(it.content))
        elif isinstance(it, Replace):
            out.append(it.intro or f"In `{it.fname}`, find this code:")
            out.append(code(it.old))
            out.append(it.after or "Replace it with:")
            out.append(code(it.new))
        elif isinstance(it, Delete):
            out.append(it.intro or f"In `{it.fname}`, find this code and delete it:")
            out.append(code(it.old))
        elif isinstance(it, DeleteRange):
            out.append(it.intro or f"In `{it.fname}`, find the line:")
            out.append(code(it.start))
            btw = f" ({it.between})" if it.between else ""
            if it.end_text:
                out.append(f"Delete that line and everything below it{btw}, {it.end_text}")
            elif it.exclusive:
                out.append(f"Delete that line and everything below it{btw}, stopping just "
                           "**above** this line, which you keep:")
                out.append(code(it.end))
            else:
                out.append(f"Delete that line and everything below it{btw}, down to and "
                           "including this line:")
                out.append(code(it.end))
            if it.new is not None:
                out.append(it.after or "In the space where that code was, enter:")
                out.append(code(it.new))
        elif isinstance(it, InsertAfter):
            out.append(it.intro or f"In `{it.fname}`, find this code:")
            out.append(code(it.anchor))
            out.append("Directly below it, add:")
            out.append(code(it.new))
        elif isinstance(it, InsertBefore):
            out.append(it.intro or f"In `{it.fname}`, find this code:")
            out.append(code(it.anchor))
            out.append("Directly above it, add:")
            out.append(code(it.new))
        elif isinstance(it, Append):
            out.append(it.intro or f"Go to the very end of `{it.fname}`. After the last "
                       "line, leave one blank line and add:")
            out.append(code(it.new))
        elif isinstance(it, Run):
            if mode == "local":
                rest = _first_sentence_dropped(it.text).replace(
                    "a `.cpp` file is not open", "a `.cpp` file is missing from the build")
                out.append("> **▶ Build checkpoint:** Rebuild and run the program:\n>\n"
                           f"> ```bash\n> {build_cmd}\n> ./gradecalc\n> ```\n>\n> {rest}\n")
            else:
                out.append(f"> **▶ Run checkpoint:** {it.text}\n")
        else:
            raise TypeError(it)
    return "\n".join(x if x.endswith("\n") else x + "\n" for x in out)


# ---------------------------------------------------------------- replay
class ReplayError(Exception):
    pass


def _once(text, needle, what):
    n = text.count(needle)
    if n != 1:
        raise ReplayError(f"{what}: expected exactly 1 match, found {n}:\n{needle[:200]}")
    return text.index(needle)


def _nl(s):
    return s if s.endswith("\n") else s + "\n"


def replay(base_files, items, checkpoints=None):
    files = dict(base_files)
    snapshots = []
    for it in items:
        if isinstance(it, Create):
            if it.fname in files:
                raise ReplayError(f"create: {it.fname} already exists")
            files[it.fname] = _nl(it.content)
        elif isinstance(it, Replace):
            t = files[it.fname]
            old, new = _nl(it.old), _nl(it.new)
            _once(t, old, f"replace in {it.fname}")
            files[it.fname] = t.replace(old, new, 1)
        elif isinstance(it, Delete):
            t = files[it.fname]
            old = _nl(it.old)
            _once(t, old, f"delete in {it.fname}")
            files[it.fname] = t.replace(old, "", 1)
        elif isinstance(it, DeleteRange):
            lines = files[it.fname].splitlines(keepends=True)
            starts = [k for k, l in enumerate(lines) if l.rstrip("\n") == it.start]
            if len(starts) != 1:
                raise ReplayError(f"range start in {it.fname}: {len(starts)} matches for {it.start!r}")
            s = starts[0]
            cand = [k for k in range(s, len(lines)) if lines[k].rstrip("\n") == it.end]
            if not cand:
                raise ReplayError(f"range end not found in {it.fname}: {it.end!r}")
            e = cand[-1] if it.last else cand[0]
            if it.exclusive:
                e -= 1
            new = [] if it.new is None else [_nl(it.new)]
            files[it.fname] = "".join(lines[:s] + new + lines[e + 1:])
        elif isinstance(it, InsertAfter):
            t = files[it.fname]
            a = _nl(it.anchor)
            i = _once(t, a, f"insert-after anchor in {it.fname}") + len(a)
            files[it.fname] = t[:i] + _nl(it.new) + t[i:]
        elif isinstance(it, InsertBefore):
            t = files[it.fname]
            a = _nl(it.anchor)
            i = _once(t, a, f"insert-before anchor in {it.fname}")
            files[it.fname] = t[:i] + _nl(it.new) + t[i:]
        elif isinstance(it, Append):
            files[it.fname] = _nl(files[it.fname]) + "\n" + _nl(it.new)
        elif isinstance(it, Run):
            snapshots.append(dict(files))
    return files, snapshots


def load_version(ver):
    d = os.path.join(SOL, ver)
    return {f: open(os.path.join(d, f)).read() for f in sorted(os.listdir(d))
            if f.endswith((".cpp", ".h"))}
