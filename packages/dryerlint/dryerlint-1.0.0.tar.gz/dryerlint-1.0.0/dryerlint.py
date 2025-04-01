import subprocess
import os
import shutil
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

TARGET_DIRS = ['.', 'src', 'tests']
EXCLUDED_DIRS = ['venv', '.venv', 'node_modules', '.git', '__pycache__', '.mypy_cache', '.pytest_cache']
TIMEOUT = 30

def find_python_files(dirs, excluded):
    python_files = []
    for directory in dirs:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                if any(excl in root for excl in excluded):
                    continue
                for file in files:
                    if file.endswith(".py"):
                        python_files.append(os.path.join(root, file))
    return python_files

def run_command(description, command, timeout=TIMEOUT):
    print(f"\n{Fore.CYAN}=== {description} ==={Style.RESET_ALL}")
    try:
        result = subprocess.run(command, shell=True, text=True, capture_output=True, timeout=timeout)
        success = result.returncode == 0
        output = result.stdout + result.stderr
        timed_out = False
    except subprocess.TimeoutExpired:
        success = False
        output = f"{description} timed out after {timeout} seconds."
        timed_out = True
    except FileNotFoundError:
        success = False
        output = f"{description} failed — command not found."
        timed_out = False
    return {
        "description": description,
        "success": success,
        "output": output.strip(),
        "timed_out": timed_out
    }

def main():
    parser = argparse.ArgumentParser(description="🧺 DryerLint — Remove the Fuzz.")
    parser.add_argument('--fix-only', action='store_true', help="Only run auto-fixers (black, isort, ruff)")
    parser.add_argument('--check-only', action='store_true', help="Only run checkers (pylint, mypy, etc.)")
    parser.add_argument('--summary-only', action='store_true', help="Only show summary report")
    args = parser.parse_args()

    py_files = find_python_files(TARGET_DIRS, EXCLUDED_DIRS)
    formatted_targets = " ".join(f'"{file}"' for file in py_files)
    exclude_str = "|".join(EXCLUDED_DIRS)
    exclude_csv = ",".join(EXCLUDED_DIRS)

    results = []

    if not args.check_only:
        fix_commands = [
            ("Black (auto-formatting)", f"black {formatted_targets}"),
            ("Isort (auto-import-sorting)", f"isort {formatted_targets}"),
            ("Ruff (auto-lint-fix)", f"ruff check . --fix --exclude {exclude_csv}")
        ]
        for desc, cmd in fix_commands:
            results.append(run_command(desc, cmd))

    if not args.fix_only:
        check_commands = [
            ("Pylint (linting)", f"pylint {formatted_targets}"),
            ("Mypy (type checking)", f"mypy {formatted_targets} --exclude '{exclude_str}'"),
            ("Pyright (static analysis)", f"pyright {formatted_targets} --ignore={exclude_str}"),
            ("Bandit (security check)", f"bandit -r . -x {exclude_csv}"),
            ("Ruff (linting verification)", f"ruff check . --exclude {exclude_csv}"),
            ("Flake8 (style linting)", f"flake8 {formatted_targets} --exclude={exclude_csv}"),
            ("Pydocstyle (docstring checker)", f"pydocstyle {' '.join(formatted_targets.split())}")
        ]
        for desc, cmd in check_commands:
            results.append(run_command(desc, cmd))

    if not args.summary_only:
        for result in results:
            print(result["output"])

    # Summary report
    print(f"\n{Fore.CYAN}=== SUMMARY REPORT ==={Style.RESET_ALL}")
    score = 0
    max_score = 100
    points_per_check = max_score // len(results)

    for result in results:
        if result["timed_out"]:
            status = f"{Fore.YELLOW}⚠️ TIMED OUT"
        elif "not found" in result["output"].lower():
            status = f"{Fore.YELLOW}⚠️ NOT INSTALLED"
        else:
            status = f"{Fore.GREEN}✅ SUCCESS" if result["success"] else f"{Fore.RED}❌ FAILED"
        if result["success"]:
            score += points_per_check
        print(f"- {result['description']}: {status}{Style.RESET_ALL}")

    print(f"\n{Fore.MAGENTA}Overall Code Quality Score: {score}/100{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}=== ERROR DETAILS ==={Style.RESET_ALL}")
    for result in results:
        if not result["success"]:
            print(f"\n{Fore.RED}--- {result['description']} ---{Style.RESET_ALL}")
            print(result["output"])

if __name__ == "__main__":
    main()