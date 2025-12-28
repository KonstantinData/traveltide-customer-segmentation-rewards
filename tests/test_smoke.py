import os
import subprocess
import sys
from pathlib import Path


def test_cli_help_runs() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(Path.cwd() / "src")

    result = subprocess.run(
        [sys.executable, "-m", "traveltide", "--help"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0
