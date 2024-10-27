import json
import os
from pathlib import Path

from services.penc import Penc


class PencManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PencManager, cls).__new__(cls)
            cls._instance.penc_list = []
            cls._instance.data_file = Path(os.environ["PETO"]) / ".penc_data.json"
            cls._instance.load_persistent_state()
        return cls._instance

    def add_penc(self, penc: Penc):
        """Register a new penc and save to persistent state."""
        self.penc_list.append(penc)
        self.save_persistent_state()

    def remove_penc(self, penc: Penc):
        """Remove a penc from updates and save state."""
        if penc in self.penc_list:
            self.penc_list.remove(penc)
            self.save_persistent_state()

    def update_pets(self):
        """Run updates for all pets in registered pencs."""
        for penc in self.penc_list:
            penc.update_all_pets()

    def load_persistent_state(self):
        """Load saved penc directories."""
        if self.data_file.exists():
            with self.data_file.open("r") as f:
                penc_directories = json.load(f)
                self.penc_list = [Penc(directory) for directory in penc_directories]

    def save_persistent_state(self):
        """Save the list of penc directories."""
        penc_directories = [penc.directory for penc in self.penc_list]
        with self.data_file.open("w") as f:
            json.dump(penc_directories, f)
