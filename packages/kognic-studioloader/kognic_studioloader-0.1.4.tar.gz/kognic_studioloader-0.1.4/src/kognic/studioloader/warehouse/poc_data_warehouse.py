import os
from pathlib import Path

from kognic.studioloader.interfaces.warehouse import Warehouse
from kognic.studioloader.loader.poc_data_loader import POCDataLoader


class POCDataWarehouse(Warehouse):
    def __init__(self, path: Path):
        self.path = path

    def get_available_scenes(self) -> list[str]:
        return os.listdir(self.path)

    def initialize_scene(self, scene: str) -> POCDataLoader:
        return POCDataLoader(self.path / scene)
