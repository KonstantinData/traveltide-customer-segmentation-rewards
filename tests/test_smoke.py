import subprocess
import sys

def test_cli_help_runs() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "traveltide", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
