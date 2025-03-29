import logging
from typing import Generator, List, Optional, Union

import numpy as np
import zod.data_classes as ZOD
from zod.constants import Camera, Lidar
from zod.zod_sequences import ZodSequence

import kognic.studio.proto.messages_pb2 as PB
from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.protobuf import (
    ELEMENT_FIELDS,
    FrameId,
    ResourceId,
    construct_image_message,
)

log = logging.getLogger(__name__)


def construct_point_cloud_message_from_npy(
    frame_id: FrameId, resource_id: ResourceId, field_mapping: Optional[dict[str, str]] = None
) -> PB.PointCloud:
    log.info(f"Constructing lidar message for: {resource_id} frame_id: {frame_id}")
    data = np.load(resource_id)

    if not field_mapping:
        return PB.PointCloud(frame_id=frame_id, fields=ELEMENT_FIELDS, data=data.tobytes())

    # Define dtype based on ELEMENT_FIELDS
    new_data = np.empty(
        len(data),
        dtype=np.dtype(
            [
                ("ts_gps", "<f8"),
                ("x", "<f8"),
                ("y", "<f8"),
                ("z", "<f8"),
                ("intensity", "u1"),
                ("sensor_id", "u1"),
            ]
        ),
    )

    for field in ELEMENT_FIELDS:
        source_field = field_mapping.get(field.name, field.name)
        if field.type == PB.PackedElementField.NumericType.FLOAT64:
            new_data[field.name] = data[source_field].astype("<f8")
        elif field.type == PB.PackedElementField.NumericType.UINT8:
            new_data[field.name] = data[source_field].astype("u1")

    return PB.PointCloud(frame_id=frame_id, fields=ELEMENT_FIELDS, data=new_data.tobytes())


class ZodLoader(Loader):
    def __init__(self, sequence: ZodSequence):
        self.sequence = sequence

        self.cameras = {
            camera_name.value: self.sequence.info.get_camera_frames(camera=camera_name)
            for camera_name in self._get_camera_names()
        }
        self.lidars = {
            lidar_name.value: self.sequence.info.get_lidar_frames(lidar=lidar_name)
            for lidar_name in self._get_lidar_names()
        }

        self._pointcloud_processor = construct_point_cloud_message_from_npy
        self._image_processor = construct_image_message
        self.pointcloud_field_mapping = {"ts_gps": "timestamp", "sensor_id": "diode_index"}

    @staticmethod
    def construct_frame_message(frame_id: int | str, relative_timestamp) -> PB.Frame:
        if isinstance(frame_id, int):
            frame_id = str(frame_id)
        return PB.Frame(frame_id=frame_id, relative_timestamp=relative_timestamp)

    @staticmethod
    def construct_camera_spec(
        camera_name: str, camera_frame: ZOD.sensor.CameraFrame
    ) -> PB.CameraSpec:
        return PB.CameraSpec(name=camera_name, width=camera_frame.width, height=camera_frame.height)

    @staticmethod
    def _construct_extrinsics_message(pose: ZOD.geometry.Pose) -> PB.ExtrinsicCalibration:
        return PB.ExtrinsicCalibration(
            position=PB.Vector3(
                x=pose.translation[0], y=pose.translation[1], z=pose.translation[2]
            ),
            rotation=PB.Quaternion(
                w=pose.rotation.w, x=pose.rotation.x, y=pose.rotation.y, z=pose.rotation.z
            ),
        )

    def construct_lidar_calibration(
        self, sensor_name: str, calibration: ZOD.calibration.LidarCalibration
    ) -> PB.Calibration:
        lidar_calibration = PB.LidarCalibration(
            extrinsics=self._construct_extrinsics_message(calibration.extrinsics)
        )
        return PB.Calibration(sensor_name=sensor_name, lidar=lidar_calibration)

    def construct_camera_calibration(
        self, sensor_name: str, calibration: ZOD.calibration.CameraCalibration
    ) -> PB.Calibration:
        extrinsics = self._construct_extrinsics_message(calibration.extrinsics)
        distortion_coefficients = PB.KannalaDistortionCoefficients(
            k1=calibration.distortion[0],
            k2=calibration.distortion[1],
            p1=calibration.distortion[2],
            p2=calibration.distortion[3],
        )
        undistortion_coefficients = PB.UndistortionCoefficients(
            l1=calibration.undistortion[0],
            l2=calibration.undistortion[1],
            l3=calibration.undistortion[2],
            l4=calibration.undistortion[3],
        )
        camera_matrix = PB.CameraMatrix(
            fx=calibration.intrinsics[0, 0],
            fy=calibration.intrinsics[1, 1],
            cx=calibration.intrinsics[0, 2],
            cy=calibration.intrinsics[1, 2],
        )
        kannala = PB.Kannala(
            distortion_coefficients=distortion_coefficients,
            undistortion_coefficients=undistortion_coefficients,
        )
        camera_calibration = PB.CameraCalibration(
            extrinsics=extrinsics,
            camera_matrix=camera_matrix,
            width=calibration.image_dimensions[0],
            height=calibration.image_dimensions[1],
            kannala=kannala,
        )
        return PB.Calibration(sensor_name=sensor_name, camera=camera_calibration)

    def _get_camera_names(self):
        return [Camera.FRONT]

    def _get_lidar_names(self):
        return [Lidar.VELODYNE]

    def get_frames(self) -> PB.Frames:
        def _get_milliseconds_difference(time: float, ref: float) -> int:
            return int((time - ref) * 1000)

        log.info(f"Accessing frames for sequence {self.sequence.info.id}")
        time_ref = None
        frames: List[PB.Frame] = []
        for frame_id, frame in enumerate(
            self.sequence.info.get_camera_lidar_map(lidar=Lidar.VELODYNE)
        ):
            lidar_frame = next(f for f in frame if isinstance(f, ZOD.sensor.LidarFrame))
            if time_ref is None:
                time_ref = lidar_frame.time.timestamp()
            frames.append(
                self.construct_frame_message(
                    frame_id,
                    _get_milliseconds_difference(lidar_frame.time.timestamp() + frame_id, time_ref),
                )
            )
        return PB.Frames(frames=frames)

    def get_sensor_spec(self) -> PB.SensorSpec:
        log.info(f"Constructing sensor spec for sequence {self.sequence.info.id}")
        cameras = [
            self.construct_camera_spec(camera_name, camera_frames[0])
            for camera_name, camera_frames in self.cameras.items()
        ]
        return PB.SensorSpec(cameras=cameras)

    def get_calibrations(self) -> Generator[PB.Calibration, None, None]:
        for sensor_name, lidar_calibration in self.sequence.calibration.lidars.items():
            yield self.construct_lidar_calibration(sensor_name.value, lidar_calibration)

        for sensor_name, camera_calibration in self.sequence.calibration.cameras.items():
            yield self.construct_camera_calibration(sensor_name.value, camera_calibration)

    def get_resources_for_frame(
        self, frame_id: str
    ) -> Generator[Union[PB.PointCloud, PB.CameraImage], None, None]:
        log.info(f"Uploading frame: {frame_id}")

        for camera_name, camera_resources in self.cameras.items():
            try:
                image = camera_resources[int(frame_id)]
                yield self._image_processor(camera_name, frame_id, image.filepath)
            except IndexError:
                continue

        for _, lidar_resources in self.lidars.items():
            try:
                pointcloud = lidar_resources[int(frame_id)]
                yield self._pointcloud_processor(
                    frame_id,
                    pointcloud.filepath,
                    field_mapping=self.pointcloud_field_mapping,
                )
            except IndexError:
                continue
