import os
import subprocess
from pathlib import Path
from utils.utils import get_tmp, setup_logger

logger = setup_logger()

def start_service():
    peto = Path(os.environ["PETO"])
    service_pid_file = get_tmp() / ".peto_service.pid"
    if service_pid_file.exists():
        with service_pid_file.open("r") as f:
            pid = int(f.read().strip())
            if not (Path("/proc") / f"{pid}").exists():
                service_pid_file.unlink()

    env = os.environ.copy()
    src = peto / "src"
    env["PYTHONPATH"] = str(src)

    subprocess.Popen(
        [str(src / "services/peto_service.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
        env=env,
    )
