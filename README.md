# Google-Docs-LaTeX-Substitutions

Allows you to import, export, and delete lists of automatic substitutions into Google Docs.
The file `latex_substitutions.csv` provides a list of substitutions from a symbol's LaTeX code into the corresponding Unicode character.

Since Google Docs is case-insensitive, for codes distinguished by only an uppercase or lowercase letter, the lowercase version uses two backslashes.

Examples:
```
\frac12 -> ½
\times -> ×
\mathbb{r} -> ℝ
\\mathbb{r} -> 𝕣
\pi -> π
```

Note: Google Docs doesn't support substitutions into capital letters (it gets automatically lowercased), so for capital Greek letters either use auto-capitalization at the beginning of a sentence or Format > Text > Capitalization > UPPERCASE.

## Setup

This uses [seleniumbase](https://github.com/seleniumbase/SeleniumBase/) on Google Chrome, so make sure you have Chrome installed.

```bash
pip install -r requirements.txt
```

Make a file called `.env`:

Fill these values to auto-login

```
email=your email here
password=your password here
```

## Usage
Importing the list:
```bash
python main.py import -f data/latex_substitutions.csv
```

Ignore duplicates (prevent overrriding the ones you already have):
```bash
python main.py import -f data/latex_substitutions.csv -d
```

Exporting your substitutions:
```bash
python main.py export -f output.csv
```

Deleting the substitutions
```bash
python main.py delete -f data/latex_substitutions.csv
```