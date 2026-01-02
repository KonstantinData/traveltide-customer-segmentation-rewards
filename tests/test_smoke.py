import subprocess
import sys


def test_cli_help_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "traveltide", "--help"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0


def test_cli_run_placeholder_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "traveltide", "run"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
