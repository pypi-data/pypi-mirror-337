from abc import ABC, abstractmethod
from typing import Callable, Generator, Optional, Union

import kognic.studio.proto.messages_pb2 as PB
from kognic.studioloader.protobuf import ResourceId, FrameId, SensorName


class Loader(ABC):

    @abstractmethod
    def __init__(
        self,
        scene_uuid: str,
        pointcloud_processor: Optional[Callable[[FrameId, ResourceId], PB.PointCloud]] = None,
        image_processor: Optional[
            Callable[[SensorName, FrameId, ResourceId], PB.CameraImage]
        ] = None,
    ) -> None:
        self._scene_uuid = scene_uuid
        self._pointcloud_processor = pointcloud_processor or unit_pointcloud_processor
        self._image_processor = image_processor or unit_image_processor

    def get_frames(self) -> PB.Frames:
        return PB.Frames(frames=[])

    def get_sensor_spec(self) -> PB.SensorSpec:
        return PB.SensorSpec(cameras=[])

    def get_calibrations(self) -> Generator[PB.Calibration, None, None]:
        yield from ()

    def poll_calibrations(self) -> Generator[PB.Calibration, None, None]:
        yield from ()

    def get_resources_for_frame(
        self,
        frame_id: str,
    ) -> Generator[Union[PB.PointCloud, PB.CameraImage], None, None]:
        _ = frame_id
        yield from ()

    def get_openlabel(self) -> PB.OpenLabel:
        return PB.OpenLabel(open_label='{"openlabel: {}}')

    def save_openlabel(self, openlabel: PB.OpenLabel):
        return None


def unit_pointcloud_processor(frame_id: FrameId, resource_id: ResourceId) -> PB.PointCloud:
    return PB.PointCloud()


def unit_image_processor(
    sensor_name: SensorName,
    frame_id: FrameId,
    resource_id: ResourceId,
) -> PB.CameraImage:
    return PB.CameraImage()
