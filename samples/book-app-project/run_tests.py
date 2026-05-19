from pathlib import Path
import subprocess
import sys


def main() -> int:
    project_dir = Path(__file__).resolve().parent
    command = [sys.executable, "-m", "pytest", "tests", "-q"]
    completed = subprocess.run(command, cwd=project_dir)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())