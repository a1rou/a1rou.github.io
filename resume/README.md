# Resume source

- `resume.tex` — editable LaTeX source
- `Rodion_Islibaev_ML_Engineer_Resume.pdf` — compiled, public PDF used on the portfolio site

## Build

The document uses the Lato font and compiles with XeLaTeX or Tectonic.

```bash
tectonic --keep-logs --keep-intermediates resume.tex
cp resume.pdf Rodion_Islibaev_ML_Engineer_Resume.pdf
```

The PDF is intentionally a one-page, print-friendly technical resume. Contact links, the portfolio, GitHub, live demo, and project repositories are embedded as clickable links.
