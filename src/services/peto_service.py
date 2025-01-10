#!/usr/bin/env python3
import os
import signal
import sys
import time

from services.penc_manager import PencManager
from utils.utils import get_tmp, setup_logger

TMP_DIR = get_tmp()
PID_FILE = TMP_DIR / ".peto_service.pid"
RELOAD_SIGNAL_FILE = TMP_DIR / ".reload"

logger = setup_logger()

def write_pid_file():
    """Write the current process ID to the PID file."""
    pid = str(os.getpid())
    with PID_FILE.open("w") as f:
        f.write(pid)
    logger.info(f"Writing services PID: {pid}")


def is_pid_running(pid: str) -> bool:
    """Check if the process with the given PID is running."""
    try:
        os.kill(int(pid), 0)
        return True
    except ProcessLookupError:
        return False
    except ValueError:
        return False


def check_and_handle_pid_file():
    """Check the PID file for a valid running process."""
    if PID_FILE.exists():
        with PID_FILE.open("r") as f:
            pid = f.read().strip()
        if is_pid_running(pid):
            logger.info(f"Service is already running with PID {pid}. Exiting.")
            return True
        else:
            logger.warning("Stale PID file found. Removing and continuing.")
            remove_pid_file()
    return False


def remove_pid_file():
    """Remove the PID file when the service stops."""
    if PID_FILE.exists():
        PID_FILE.unlink()


def handle_signal(signum, frame):
    """Handle termination signals (e.g., SIGTERM, SIGINT)."""
    logger.info(f"Received signal {signum}. Cleaning up...")
    remove_pid_file()
    sys.exit(0)


def run_peto_service():
    """Run the PencManager service in the background, maintaining updates to pets."""
    if check_and_handle_pid_file():
        return

    logger.info("Starting peto service")
    write_pid_file()

    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)

    try:
        manager = PencManager()
        while True:
            if RELOAD_SIGNAL_FILE.exists():
                manager.load_persistent_state()
                RELOAD_SIGNAL_FILE.unlink()

            logger.info("Updating pets")
            manager.update_pets()
            time.sleep(60)
    except Exception as e:
        logger.error(f"An error occurred while updating pets: {e}", exc_info=True)
        time.sleep(5)
    finally:
        logger.info("Exiting")
        remove_pid_file()


if __name__ == "__main__":
    run_peto_service()
