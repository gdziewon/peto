#!/usr/bin/env python3
import os
from pathlib import Path
import logging
import logging.config


def get_tmp() -> Path:
    peto_path = Path(os.environ["PETO"])
    tmp_dir = peto_path / "tmp"

    tmp_dir.mkdir(exist_ok=True)
    return tmp_dir

def setup_logger(log_file="peto.log", level=logging.DEBUG):
    log_dir = get_tmp()

    log_format = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        filename=log_dir / log_file,
        level=level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    return logging.getLogger()
