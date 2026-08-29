# Building the book

Two single-file editions are generated from the markdown sources in the
repository root and committed alongside them:

| File | What it is |
|---|---|
| `../Just-Build-It-Cpp.pdf` | Print/download edition — 476 pages, XeLaTeX |
| `../Just-Build-It-Cpp.html` | Accessible web edition — one self-contained file, no external resources |

## Regenerate

Run from the repository root:

```bash
./build/make-pdf.sh  . Just-Build-It-Cpp.pdf  build/order.txt
./build/make-html.sh . Just-Build-It-Cpp.html build/order.txt "Just Build It! — A Complete Two-Course C++ Programming Textbook"
```

Requires `pandoc` and `xelatex`. Neither script installs anything.

## Files here

| File | Purpose |
|---|---|
| `order.txt` | The files that make up the book, in order |
| `meta.yaml` | Title, paper size, margins, fonts |
| `header.tex` | LaTeX preamble — code sizing, tables, spacing |
| `style.css` | HTML styling, print rules included |
| `a11y.theme` | Syntax colors, all at or above WCAG AA 4.5:1 on the code background |

## Notes for anyone editing these

- **The PDF build rewrites `.svg` figure references to `.png`.** This TinyTeX
  has no `rsvg-convert`, so LaTeX cannot read SVG. Every figure ships as both.
- **The PDF build replaces `→` with a math arrow.** Palatino has no U+2192 and
  XeLaTeX drops it silently. The build reports `missing glyphs`; it must be 0.
- **pandoc emits `\usepackage{bookmark}`**, which this TinyTeX lacks — and that
  package is also what loads `hyperref`. The script substitutes `hyperref`
  rather than deleting the line.
- **The HTML build inlines the SVGs** instead of embedding them as base64. That
  keeps each figure's own `<title>`/`<desc>` for screen readers, and makes the
  diagram label text real DOM text — searchable, and visible to tools that index
  the file.
