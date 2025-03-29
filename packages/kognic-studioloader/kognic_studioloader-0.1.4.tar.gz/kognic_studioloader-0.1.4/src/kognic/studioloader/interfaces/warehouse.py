from abc import ABC, abstractmethod

from kognic.studioloader.interfaces.loader import Loader


class Warehouse(ABC):

    @abstractmethod
    def get_available_scenes(self) -> list[str]:
        pass

    @abstractmethod
    def initialize_scene(self, scene: str) -> Loader:
        pass
