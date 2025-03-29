import logging
import os
from pathlib import Path
from typing import Generator, List, Union

import kognic.studio.proto.messages_pb2 as PB
from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.protobuf import (
    construct_calibration_message,
    construct_image_message,
    construct_point_cloud_message,
)
from kognic.studioloader.resource_parser import load_calibrations, load_poses

log = logging.getLogger(__name__)


def get_file_timestamp(file: Path) -> float:
    return os.stat(file).st_mtime


def convert_from_nano_to_milliseconds(timestamp: int) -> int:
    return timestamp / 1e6


class POCDataLoader(Loader):
    def __init__(self, scene_path: Path) -> None:
        self.scene_path = scene_path
        self.scene_name = scene_path.stem

        log.info(f"Initializing scene {self.scene_name}")

        self.camera_resources = {
            dir.name: sorted(list(dir.glob("*")), key=lambda x: int(x.stem))
            for dir in self.cameras_path.glob("*")
            if dir.is_dir()
        }
        self.lidar_resources = {
            dir.name: sorted(list(dir.glob("*")), key=lambda x: int(x.stem))
            for dir in self.lidars_path.glob("*")
            if dir.is_dir()
        }
        self.calibration_path = self.scene_path / "calibrations.json"
        self.ego_pose_path = self.scene_path / "ego_poses.json"

        self._calibration_timestamp = get_file_timestamp(self.calibration_path)
        self._pointcloud_processor = construct_point_cloud_message
        self._image_processor = construct_image_message

        self.calibration = load_calibrations(self.calibration_path)
        self.ego_poses = load_poses(self.ego_pose_path)

    @property
    def cameras_path(self) -> Path:
        return self.scene_path / "cameras"

    @property
    def lidars_path(self) -> Path:
        return self.scene_path / "lidars"

    def get_frames(self) -> PB.Frames:
        log.info(f"Accessing frames for sequence {self.scene_name}")
        frames: List[PB.Frame] = []

        # Assume that lidar timestamps are the frame timestamps. We need to redo this a bit
        lidar_timestamps = sorted(
            [
                int(file.stem)
                for file in (self.lidars_path / list(self.lidar_resources.keys())[0]).glob("*")
            ]
        )
        relative_timestamp = 0
        previous_frame_timestamp = None
        for frame_id, frame_timestamp in enumerate(lidar_timestamps):
            frame_ego_pose = self.ego_poses[str(frame_id)]
            if previous_frame_timestamp:
                relative_timestamp += convert_from_nano_to_milliseconds(
                    frame_timestamp - previous_frame_timestamp
                )
            frames.append(
                PB.Frame(
                    frame_id=str(frame_id),
                    relative_timestamp=int(relative_timestamp),
                    pose=PB.Pose(
                        position=PB.Vector3(**frame_ego_pose.position.model_dump()),
                        orientation=PB.Quaternion(**frame_ego_pose.rotation.model_dump()),
                    ),
                )
            )
            previous_frame_timestamp = frame_timestamp

        return PB.Frames(frames=frames)

    def get_sensor_spec(self) -> PB.SensorSpec:
        return PB.SensorSpec(
            cameras=[
                PB.CameraSpec(
                    name=camera,
                    width=self.calibration[camera].image_width,
                    height=self.calibration[camera].image_height,
                )
                for camera in self.camera_resources.keys()
            ]
        )

    def get_calibrations(self) -> Generator[PB.Calibration, None, None]:
        for sensor, calibration in self.calibration.items():
            yield construct_calibration_message(sensor, calibration)

    def poll_calibrations(self) -> Generator[PB.Calibration, None, None]:
        new_timestamp = get_file_timestamp(self.calibration_path)
        if new_timestamp != self._calibration_timestamp:
            self._calibration_timestamp = new_timestamp
            yield from self.get_calibrations()

    def get_resources_for_frame(
        self, frame_id: str
    ) -> Generator[Union[PB.PointCloud, PB.CameraImage], None, None]:
        log.info(f"Uploading frame: {frame_id}")

        for camera_name, camera_resources in self.camera_resources.items():
            image = camera_resources[int(frame_id)]
            yield self._image_processor(camera_name, frame_id, image)

        for _, lidar_resources in self.lidar_resources.items():
            pointcloud = lidar_resources[int(frame_id)]
            yield self._pointcloud_processor(frame_id, str(pointcloud))
