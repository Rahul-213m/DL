#!/usr/bin/env python3
"""Smoke-test the local cloud + operator integration.

This script exists to make the integration path operational and repeatable.
It checks the project config, starts the API and UI locally, and waits for the
expected HTTP responses on the configured ports.
"""

from __future__ import annotations

import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV = os.environ.copy()
ENV["PYTHONUNBUFFERED"] = "1"


def run_command(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=str(cwd or ROOT), env=ENV, text=True, capture_output=True)


def wait_for_http(url: str, timeout: float = 30.0) -> int:
    deadline = time.monotonic() + timeout
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                return int(response.getcode())
        except Exception as exc:  # pragma: no cover - smoke path only
            last_error = exc
            time.sleep(0.5)
    if last_error is not None:
        raise RuntimeError(f"Timed out waiting for {url}: {last_error}")
    raise RuntimeError(f"Timed out waiting for {url}")


def main() -> int:
    print("[1/3] configuration check")
    result = run_command([sys.executable, "-m", "app.cli", "doctor"])
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        print("doctor check failed")
        return result.returncode

    print("[2/3] API smoke check")
    api = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=str(ROOT),
        env=ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        status = wait_for_http("http://127.0.0.1:8000/docs")
        print(f"API docs status: {status}")
        if status != 200:
            return 1
    finally:
        if api.poll() is None:
            api.send_signal(signal.SIGINT)
            api.wait(timeout=10)

    print("[3/3] UI smoke check")
    ui = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "ui/app.py",
            "--server.address",
            "127.0.0.1",
            "--server.port",
            "8501",
            "--server.headless",
            "true",
        ],
        cwd=str(ROOT),
        env=ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        status = wait_for_http("http://127.0.0.1:8501")
        print(f"UI status: {status}")
        if status != 200:
            return 1
    finally:
        if ui.poll() is None:
            ui.send_signal(signal.SIGINT)
            ui.wait(timeout=10)

    print("integration smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
