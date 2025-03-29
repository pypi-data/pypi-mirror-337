import logging
import numpy as np
from typing import Optional, Callable, Generator, Tuple, Union, List
from datetime import datetime

from kognic.io.model.calibration.camera.common import BaseCameraCalibration

from kognic.studioloader.interfaces.loader import Loader
from kognic.io.model.calibration.camera.pinhole_calibration import PinholeCalibration
from kognic.io.model.calibration.common import Position, RotationQuaternion
from kognic.io.model.calibration.lidar.lidar_calibration import LidarCalibration, LidarFieldOfView
from kognic.io.model.scene.resources import Image, PointCloud

import kognic.studio.proto.messages_pb2 as PB
import kognic.io.model.calibration as CalibrationModel
import kognic.io.model.scene.lidars_and_cameras_sequence as LCSM

from kognic.studioloader.protobuf import (
    FrameId,
    ResourceId,
    SensorName,
    construct_calibration_message,
    construct_image_message,
    construct_point_cloud_message,
)

log = logging.getLogger(__name__)

ELEMENT_FIELDS = [
    PB.PackedElementField(name="ts_gps", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="x", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="y", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="z", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="intensity", type=PB.PackedElementField.NumericType.UINT8),
]


def construct_point_cloud_message(
    frame_id: FrameId,
    resource_id: ResourceId,
) -> PB.PointCloud:
    log.info(f"Constructing lidar message for: {resource_id} frame_id: {frame_id}")
    data = np.genfromtxt(
        resource_id,
        delimiter=",",
        names=True,
        dtype=[
            ("ts_gps", "<f8"),
            ("x", "<f8"),
            ("y", "<f8"),
            ("z", "<f8"),
            ("intensity", "uint8"),
        ],
    )
    return PB.PointCloud(frame_id=frame_id, fields=ELEMENT_FIELDS, data=data.tobytes())


class KognicIoLoader(Loader):

    def __init__(
        self,
        scene_uuid: str,
        pointcloud_processor: Optional[Callable[[FrameId, ResourceId], PB.PointCloud]] = None,
        image_processor: Optional[
            Callable[[SensorName, FrameId, ResourceId], PB.CameraImage]
        ] = None,
    ) -> None:
        self.scene, self.calibrations = get_da_data()
        self.scene.frames.sort(key=lambda x: x.relative_timestamp)
        log.info([frame.relative_timestamp for frame in self.scene.frames])
        super().__init__(
            scene_uuid,
            pointcloud_processor or construct_point_cloud_message,
            image_processor or construct_image_message,
        )

    def get_frames(self) -> PB.Frames:
        frames = []
        for frame in self.scene.frames:
            frames.append(
                PB.Frame(
                    frame_id=frame.frame_id,
                    relative_timestamp=frame.relative_timestamp,
                    pose=None,
                )
            )

        return PB.Frames(frames=frames)

    def get_sensor_spec(self) -> PB.SensorSpec:
        camera_calibrations = [
            camera_calibration_to_spec(calib, name)
            for name, calib in self.calibrations.calibration.items()
            if isinstance(calib, BaseCameraCalibration)
        ]

        return PB.SensorSpec(cameras=camera_calibrations)

    def get_calibrations(self) -> Generator[PB.Calibration, None, None]:
        for name, calibration in self.calibrations.calibration.items():
            yield construct_calibration_message(name, calibration)

    def get_resources_for_frame(
        self,
        frame_id: str,
    ) -> Generator[Union[PB.PointCloud, PB.CameraImage], None, None]:
        for frame in self.scene.frames:
            if frame.frame_id != frame_id:
                continue

            for image in frame.images:
                assert image.resource_id is not None
                yield self._image_processor(image.sensor_name, frame_id, image.resource_id)

            for pointcloud in frame.point_clouds:
                assert pointcloud.resource_id is not None
                yield self._pointcloud_processor(frame_id, pointcloud.resource_id)

    def get_openlabel(self) -> PB.OpenLabel:
        return PB.OpenLabel(open_label='{"openlabel: {}}')

    def save_openlabel(self, openlabel: PB.OpenLabel):
        return None


def camera_calibration_to_spec(calibration: PinholeCalibration, camera_name: str) -> PB.CameraSpec:
    return PB.CameraSpec(
        name=camera_name,
        width=calibration.image_width,
        height=calibration.image_height,
    )


def get_da_data() -> Tuple[LCSM.LidarsAndCamerasSequence, CalibrationModel.SensorCalibration]:
    lidar_sensor1 = "RFL01"
    cam_sensor1 = "RFC01"
    cam_sensor2 = "RFC02"

    examples_path = "/home/alex/kognic/repos/kognic-io-python/examples"
    calibration_spec = create_sensor_calibration(
        f"Collection {datetime.now()}",
        [lidar_sensor1],
        [cam_sensor1, cam_sensor2],
    )

    return (
        LCSM.LidarsAndCamerasSequence(
            external_id=f"LCS-with-pre-annotation",
            frames=[
                LCSM.Frame(
                    frame_id="1",
                    relative_timestamp=0,
                    point_clouds=[
                        PointCloud(
                            filename=examples_path + "/resources/point_cloud_RFL01.csv",
                            sensor_name=lidar_sensor1,
                            client_filename=None,
                        )
                    ],
                    images=[
                        Image(
                            filename=examples_path + "/resources/img_RFC01.jpg",
                            sensor_name=cam_sensor1,
                            client_filename=None,
                        ),
                        Image(
                            filename=examples_path + "/resources/img_RFC02.jpg",
                            sensor_name=cam_sensor2,
                            client_filename=None,
                        ),
                    ],
                ),
                LCSM.Frame(
                    frame_id="2",
                    relative_timestamp=4,
                    point_clouds=[
                        PointCloud(
                            filename=examples_path + "/resources/point_cloud_RFL11.csv",
                            sensor_name=lidar_sensor1,
                            client_filename=None,
                        )
                    ],
                    images=[
                        Image(
                            filename=examples_path + "/resources/img_RFC11.jpg",
                            sensor_name=cam_sensor1,
                            client_filename=None,
                        ),
                        Image(
                            filename=examples_path + "/resources/img_RFC12.jpg",
                            sensor_name=cam_sensor2,
                            client_filename=None,
                        ),
                    ],
                ),
            ],
            calibration_id="calibration_id",
        ),
        calibration_spec,
    )


def create_sensor_calibration(
    external_id,
    lidar_sources: Optional[List[str]] = None,
    camera_sources: Optional[List[str]] = None,
):
    if lidar_sources is None:
        lidar_sources = []

    if camera_sources is None:
        camera_sources = []

    camera_calibrations = [
        unity_pinhole_calibration(),
        unity_pinhole_calibration(),
    ]
    calibration_dict = {
        **{lidar_source: unity_lidar_calibration() for lidar_source in lidar_sources},
        **{camera_source: camera_calibrations.pop() for camera_source in camera_sources},
    }
    calibration_external_id = external_id
    sensor_calibration = CalibrationModel.SensorCalibration(
        external_id=calibration_external_id,
        calibration=calibration_dict,
    )

    return sensor_calibration


def unity_pinhole_calibration():
    camera_position = Position(x=0.0, y=0.0, z=0.0)
    camera_rotation = RotationQuaternion(w=1.0, x=0.0, y=0.0, z=0.0)
    camera_camera_matrix = CalibrationModel.CameraMatrix(fx=3450, fy=3250, cx=622, cy=400)
    camera_distortion_coefficients = CalibrationModel.DistortionCoefficients(
        k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=1.0
    )
    return PinholeCalibration(
        position=camera_position,
        rotation_quaternion=camera_rotation,
        camera_matrix=camera_camera_matrix,
        distortion_coefficients=camera_distortion_coefficients,
        image_height=1080,
        image_width=1920,
        field_of_view=190.0,
    )


def unity_lidar_calibration():
    lidar_position = Position(x=0.0, y=0.0, z=0.0)
    lidar_rotation = RotationQuaternion(w=1.0, x=0.0, y=0.0, z=0.0)
    lidar_fov = LidarFieldOfView(start_angle_deg=315, stop_angle_deg=45, depth=200)
    return LidarCalibration(
        position=lidar_position,
        rotation_quaternion=lidar_rotation,
        field_of_view=lidar_fov,
    )
