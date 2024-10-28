#!/usr/bin/env python3
import os
import sys
import time
import psutil
from pathlib import Path

PETO = Path(os.environ["PETO"])
PID_FILE = PETO / ".peto_service.pid"
RELOAD_SIGNAL_FILE = PETO / ".reload"

def is_pid_running():
    if PID_FILE.exists():
        try:
            with PID_FILE.open() as f:
                pid = int(f.read())
            return psutil.pid_exists(pid)
        except (ValueError, ProcessLookupError):
            return False
    return False

def write_pid_file():
    """Write the current process ID to the PID file."""
    with PID_FILE.open("w") as f:
        f.write(str(os.getpid()))


def remove_pid_file():
    """Remove the PID file when the service stops."""
    if PID_FILE.exists():
        PID_FILE.unlink()


def run_peto_service():
    """Run the PencManager service in the background, maintaining updates to pets."""
    if is_pid_running():
        return

    write_pid_file()
    try:
        manager = PencManager()
        while True:
            try:
                if RELOAD_SIGNAL_FILE.exists():
                    manager.load_persistent_state()
                    RELOAD_SIGNAL_FILE.unlink()
                manager.update_pets()
            except Exception as e:
                print(f"Error updating pets: {e}")
            time.sleep(60)
    finally:
        remove_pid_file()
        remove_pid_file()


if __name__ == "__main__":
    sys.path.append(str(PETO / "src"))
    from services.penc_manager import PencManager

    run_peto_service()
