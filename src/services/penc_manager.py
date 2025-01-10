import json
from pathlib import Path

from services.penc import Penc
from utils.utils import get_tmp, setup_logger

logger = setup_logger()

class PencManager:
    _instance = None
    data_file = get_tmp() / ".penc_data.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PencManager, cls).__new__(cls)
            cls._instance.penc_list = []
            cls._instance.load_persistent_state()
        return cls._instance

    def add_penc(self, penc: Penc):
        """Register a new penc and save to persistent state."""
        logger.info(f"Adding penc: {penc.directory}")
        self.penc_list.append(penc)
        self.save_persistent_state()
        logger.info(f"Successfully added penc: {penc.directory}")

    def remove_penc(self, penc: Penc):
        """Remove a penc from updates and save state."""
        if penc in self.penc_list:
                self.penc_list.remove(penc)
                self.save_persistent_state()
                logger.info(f"Successfully removed penc: {penc.directory}")
        else:
            logger.warning(f"Attempted to remove a non-existent penc: {penc.directory}")

    def update_pets(self):
        """Run updates for all pets in registered pencs."""
        for penc in self.penc_list:
            logger.info(f"Updating pets in {penc.directory}")
            penc.update_all_pets()

    def load_persistent_state(self):
        """Load saved penc directories."""
        try:
            if self.data_file.exists():
                with self.data_file.open("r") as f:
                    penc_directories = json.load(f)
                    self.penc_list = [
                        Penc(Path(directory)) for directory in penc_directories
                    ]
            else:
                logger.warning(f"Persistent state file {self.data_file} does not exist.")
        except Exception as e:
            logger.error(f"Failed to load persistent state: {e}")
            self.penc_list = []


    def save_persistent_state(self):
        """Save the list of penc directories."""
        penc_directories = [str(penc.directory) for penc in self.penc_list]
        with self.data_file.open("w") as f:
            json.dump(penc_directories, f)
