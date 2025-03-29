from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.interfaces.warehouse import Warehouse
from kognic.studioloader.loader.kognic_io_loader import KognicIoLoader


class KognicIoWarehouse(Warehouse):

    def __init__(self) -> None:
        super().__init__()

    def get_available_scenes(self) -> list[str]:
        return ["kognic io scene"]

    def initialize_scene(self, scene: str) -> Loader:
        return KognicIoLoader(scene)
