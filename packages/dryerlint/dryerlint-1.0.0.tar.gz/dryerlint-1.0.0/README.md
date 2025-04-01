# 🧺 DryerLint

> Remove the Fuzz.

DryerLint is a Python-powered code quality tool that:
- 🧼 Cleans up formatting with `black`, `isort`, and `ruff`
- 🧐 Runs deep linting, static analysis, type checks, and security scans
- 🎯 Outputs a color-coded summary with an overall code quality score
- 🚫 Ignores your `venv`, `.git`, and all the other gunk

## 💻 Installation

1. Clone this repo or download the script
2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
3. Install the tools:
```bash
pip install -r editor_requirements.txt
```

## ▶️ Usage

```bash
python run_code_quality_checks.py
```

You’ll get:
- Auto-fixes (black, isort, ruff)
- Lint & security checks (pylint, mypy, pyright, bandit, flake8, pydocstyle)
- A color-coded terminal report
- An overall code quality score out of 100

## 📁 Included Tools

| Tool        | Purpose           | Auto-fix? |
|-------------|-------------------|-----------|
| `black`     | Code formatter    | ✅ Yes     |
| `isort`     | Import sorter     | ✅ Yes     |
| `ruff`      | Fast linter       | ✅ Yes     |
| `pylint`    | Style + logic     | ❌ No      |
| `flake8`    | Linting           | ❌ No      |
| `mypy`      | Type checker      | ❌ No      |
| `pyright`   | Static analysis   | ❌ No      |
| `bandit`    | Security scanner  | ❌ No      |
| `pydocstyle`| Docstring checker | ❌ No      |

## 🤝 License

MIT — free to use, modify, and share.