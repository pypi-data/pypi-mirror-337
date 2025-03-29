import os
from pathlib import Path
from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.interfaces.warehouse import Warehouse
from kognic.studioloader.warehouse.kognic_io_warehouse import KognicIoWarehouse
from kognic.studioloader.warehouse.zod_warehouse import ZodWarehouse

BASE_DIR = Path(os.path.abspath(__file__)).parent.parent.parent.parent.parent


class EverythingWarehouse(Warehouse):

    def __init__(self) -> None:
        self._kognic_warehouse = KognicIoWarehouse()
        self._zod_warehouse = ZodWarehouse(BASE_DIR / "zod")
        super().__init__()

    def get_available_scenes(self) -> list[str]:
        all_scenes = (
            self._zod_warehouse.get_available_scenes()
            + self._kognic_warehouse.get_available_scenes()
        )
        return all_scenes

    def initialize_scene(self, scene: str) -> Loader:
        if scene in self._zod_warehouse.get_available_scenes():
            return self._zod_warehouse.initialize_scene(scene)

        if scene in self._kognic_warehouse.get_available_scenes():
            return self._kognic_warehouse.initialize_scene(scene)

        raise
