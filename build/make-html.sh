#!/bin/bash
# Build a single self-contained, accessible HTML edition from the markdown sources.
# Requires: pandoc + python3. Installs nothing.
#   ./make-html.sh <source-dir> <out.html> <order.txt> "<title>"
set -e
SRC="$1"; OUT="$2"; FILES="$3"; TITLE="${4:-Just Build It!}"

python3 - "$SRC" "$FILES" <<'PY'
import pathlib,sys
src=pathlib.Path(sys.argv[1]); names=pathlib.Path(sys.argv[2]).read_text().split()
# HTML keeps the .svg figures and literal arrows; no LaTeX-specific rewriting
pathlib.Path("build/book-html.md").write_text(
    "\n\n".join((src/n).read_text().rstrip()+"\n" for n in names))
PY

pandoc build/book-html.md -f markdown-raw_html -t html5 -s --embed-resources \
  --toc --toc-depth=2 --shift-heading-level-by=1 \
  --highlight-style=build/a11y.theme --css=build/style.css \
  --resource-path="$SRC" --metadata title="$TITLE" --metadata lang=en-US -o "$OUT"

python3 - "$OUT" <<'PY'
import re,base64,sys
p=sys.argv[1]; h=open(p,encoding="utf-8").read()
def inline(m):
    tag=m.group(0)
    s=re.search(r'src="data:image/svg\+xml;base64,([^"]+)"',tag)
    if not s: return tag
    svg=base64.b64decode(s.group(1)).decode("utf-8")
    svg=re.sub(r'^<\?xml[^>]*\?>\s*','',svg)
    svg=re.sub(r'\swidth="[^"]*"\s*height="[^"]*"',' ',svg,count=1)  # let CSS size it
    if 'role=' not in svg[:400]: svg=svg.replace('<svg','<svg role="img"',1)
    return svg
# inline SVGs: keeps their own <title>/<desc>, renders reliably, and makes the
# diagram label text real DOM text (searchable, and visible to tutor retrieval)
h=re.sub(r'<img[^>]*src="data:image/svg\+xml;base64,[^"]*"[^>]*>',inline,h)
if 'class="skip"' not in h:
    h=h.replace('<body>','<body>\n<a class="skip" href="#TOC">Skip to table of contents</a>',1)
h=h.replace('<pre class="sourceCode','<pre tabindex="0" class="sourceCode')  # keyboard-scrollable
open(p,"w",encoding="utf-8").write(h)
print(f"  inlined svg: {len(re.findall(r'<svg',h))}   remaining img: {len(re.findall(r'<img',h))}   size: {len(h)/1e6:.2f} MB")
PY
