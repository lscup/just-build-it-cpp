#!/bin/bash
# Build a single PDF of Just Build It! C++ from the markdown sources.
# Requires: pandoc + xelatex (TinyTeX). Installs nothing.
set -e
SRC="$1"; OUT="$2"; FILES="$3"; META="${4:-build/meta.yaml}"
HERE="$(cd "$(dirname "$0")" && pwd)"

python3 - "$SRC" "$FILES" <<'PY'
import pathlib,re,sys
src=pathlib.Path(sys.argv[1]); names=pathlib.Path(sys.argv[2]).read_text().split()
out=[]
for n in names:
    t=(src/n).read_text()
    t=re.sub(r'(\!\[[^\]]*\]\(figures/[^)]+?)\.svg\)', r'\1.png)', t)   # LaTeX can't read SVG here
    # Palatino lacks U+2192; use a math arrow in prose (never inside code fences)
    parts=re.split(r'(?m)(^\s*```.*$)', t); infence=False; fixed=[]
    for p in parts:
        if re.match(r'^\s*```', p or ''): infence=not infence; fixed.append(p); continue
        fixed.append(p if infence else (p or '').replace('→', r'$\rightarrow$'))
    out.append("".join(fixed).rstrip()+"\n")
pathlib.Path(sys.argv[0]) # noop
open("build/book.md","w").write("\n\n".join(out))
PY

pandoc "$META" build/book.md -f markdown-raw_html -s -o build/book.tex \
  --toc --toc-depth=2 --top-level-division=chapter \
  --include-in-header=build/header.tex --highlight-style=build/a11y.theme \
  -V mainfont="Palatino" -V monofont="Menlo"
# pandoc 3.5 emits \usepackage{bookmark}; this TinyTeX lacks it, and it is what loads hyperref
sed -i '' 's/^\\usepackage{bookmark}$/\\usepackage{hyperref}/' build/book.tex
ln -sfn "../$SRC/figures" build/figures
cd build
xelatex -interaction=nonstopmode book.tex >p1.log 2>&1
xelatex -interaction=nonstopmode book.tex >p2.log 2>&1
mv book.pdf "$OUT"
echo "pages: $(grep -oE 'on book.pdf \([0-9]+ pages' p2.log | grep -oE '[0-9]+')"
echo "missing glyphs: $(grep -c 'Missing character' p2.log)"
