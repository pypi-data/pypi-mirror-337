import json
import logging
from pathlib import Path

import kognic.studio.proto.messages_pb2 as PB
import numpy as np
from kognic.studioloader.resource_parser import get_image_bytes
from kognic.io.model.calibration import CustomCameraCalibration
from kognic.io.model.calibration.calib import (
    BaseCalibration,
    CalibrationType,
    KannalaCalibration,
    LidarCalibration,
    PinholeCalibration,
    PrincipalPointDistortionCalibration,
)
from kognic.io.model.calibration.camera.common import CameraMatrix
from kognic.io.model.calibration.common import Position, RotationQuaternion
from kognic.io.tools.calibration.validation import validate_custom_camera_calibration

log = logging.getLogger(__name__)


ResourceId = str
FrameId = str
SensorName = str


def construct_image_message(
    camera_name: SensorName,
    frame_id: FrameId,
    resource_id: ResourceId,
) -> PB.CameraImage:
    log.info(f"Constructing image message for: camera: {camera_name} frame: {frame_id}")
    image = PB.CameraImage()
    image.format = "jpg"
    image.frame_id = frame_id
    image.data = get_image_bytes(Path(resource_id))
    image.camera = camera_name
    return image


ELEMENT_FIELDS = [
    PB.PackedElementField(name="ts_gps", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="x", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="y", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="z", type=PB.PackedElementField.NumericType.FLOAT64),
    PB.PackedElementField(name="intensity", type=PB.PackedElementField.NumericType.UINT8),
    PB.PackedElementField(name="sensor_id", type=PB.PackedElementField.NumericType.UINT8),
]


def construct_point_cloud_message(
    frame_id: FrameId,
    resource_id: ResourceId,
) -> PB.PointCloud:
    log.info(f"Constructing lidar message for: {resource_id} frame_id: {frame_id}")

    if resource_id.endswith("metadata.json"):
        data = load_potree_data(resource_id)
    else:
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
                ("sensor_id", "uint8"),
            ],
        )
    return PB.PointCloud(frame_id=frame_id, fields=ELEMENT_FIELDS, data=data.tobytes())


def construct_calibration_message(sensor_name: str, calibration: BaseCalibration) -> PB.Calibration:
    if calibration.calibration_type == CalibrationType.LIDAR:
        return construct_lidar_calibration_message(sensor_name, calibration)
    if calibration.calibration_type == CalibrationType.KANNALA:
        return construct_kannala_calibration_message(sensor_name, calibration)
    if calibration.calibration_type == CalibrationType.PINHOLE:
        return construct_pinhole_calibration_message(sensor_name, calibration)
    if calibration.calibration_type == CalibrationType.CUSTOM:
        return construct_custom_calibration_message(sensor_name, calibration)
    if calibration.calibration_type == CalibrationType.PRINCIPALPOINTDIST:
        return construct_principal_point_dist_calibration_message(sensor_name, calibration)

    raise


def construct_lidar_calibration_message(
    sensor_name: SensorName,
    calibration: LidarCalibration,
) -> PB.Calibration:
    log.info(f"Constructing lidar calibration message for sensor: {sensor_name}")
    extrinsics = construct_extrinsics_message(calibration.position, calibration.rotation_quaternion)
    lidar_calibration = PB.LidarCalibration(extrinsics=extrinsics)
    return PB.Calibration(sensor_name=sensor_name, lidar=lidar_calibration)


def construct_kannala_calibration_message(
    sensor_name: SensorName,
    calibration: KannalaCalibration,
) -> PB.Calibration:
    log.info(f"Constructing kannala calibration message for sensor: {sensor_name}")
    extrinsics = construct_extrinsics_message(calibration.position, calibration.rotation_quaternion)

    kannala_distortion_coefficients = PB.KannalaDistortionCoefficients(
        k1=calibration.distortion_coefficients.k1,
        k2=calibration.distortion_coefficients.k2,
        p1=calibration.distortion_coefficients.p1,
        p2=calibration.distortion_coefficients.p2,
    )
    undistortion_coefficients = PB.UndistortionCoefficients(
        l1=calibration.undistortion_coefficients.l1,
        l2=calibration.undistortion_coefficients.l2,
        l3=calibration.undistortion_coefficients.l3,
        l4=calibration.undistortion_coefficients.l4,
    )

    kannala = PB.Kannala(
        distortion_coefficients=kannala_distortion_coefficients,
        undistortion_coefficients=undistortion_coefficients,
    )

    camera_matrix = construct_camera_matrix_message(calibration.camera_matrix)

    camera_calibration = PB.CameraCalibration(
        extrinsics=extrinsics,
        camera_matrix=camera_matrix,
        width=calibration.image_width,
        height=calibration.image_height,
        kannala=kannala,
    )

    return PB.Calibration(sensor_name=sensor_name, camera=camera_calibration)


def construct_pinhole_calibration_message(
    sensor_name: SensorName,
    calibration: PinholeCalibration,
) -> PB.Calibration:
    log.info(f"Constructing pinhole calibration message for sensor: {sensor_name}")
    extrinsics = construct_extrinsics_message(calibration.position, calibration.rotation_quaternion)

    distortion_coefficients = PB.DistortionCoefficients(
        k1=calibration.distortion_coefficients.k1,
        k2=calibration.distortion_coefficients.k2,
        p1=calibration.distortion_coefficients.p1,
        p2=calibration.distortion_coefficients.p2,
        k3=calibration.distortion_coefficients.k3,
    )

    camera_matrix = construct_camera_matrix_message(calibration.camera_matrix)

    pinhole = PB.Pinhole(distortion_coefficients=distortion_coefficients)
    camera_calibration = PB.CameraCalibration(
        extrinsics=extrinsics,
        camera_matrix=camera_matrix,
        width=calibration.image_width,
        height=calibration.image_height,
        pinhole=pinhole,
    )

    return PB.Calibration(sensor_name=sensor_name, camera=camera_calibration)


def construct_extrinsics_message(
    position: Position,
    rotation: RotationQuaternion,
) -> PB.ExtrinsicCalibration:
    position_message = construct_position_message(position)
    rotation_message = construct_rotation_message(rotation)
    return PB.ExtrinsicCalibration(position=position_message, rotation=rotation_message)


def construct_camera_matrix_message(camera_matrix: CameraMatrix) -> PB.CameraMatrix:
    return PB.CameraMatrix(
        fx=camera_matrix.fx,
        fy=camera_matrix.fy,
        cx=camera_matrix.cx,
        cy=camera_matrix.cy,
    )


def construct_position_message(position: Position) -> PB.Vector3:
    return PB.Vector3(
        x=position.x,
        y=position.y,
        z=position.z,
    )


def construct_rotation_message(rotation: RotationQuaternion) -> PB.Quaternion:
    return PB.Quaternion(
        x=rotation.x,
        y=rotation.y,
        z=rotation.z,
        w=rotation.w,
    )


def construct_custom_calibration_message(
    sensor_name: SensorName, calibration: CustomCameraCalibration
) -> PB.Calibration:
    log.info(f"Constructing custom calibration message for sensor {sensor_name}")
    validate_custom_camera_calibration(calibration)
    extrinsics = construct_extrinsics_message(calibration.position, calibration.rotation_quaternion)
    custom = PB.Wasm(wasm_base64=calibration.wasm_base64)
    camera = PB.CameraCalibration(
        extrinsics=extrinsics,
        width=calibration.image_width,
        height=calibration.image_height,
        wasm=custom,
    )
    return PB.Calibration(sensor_name=sensor_name, camera=camera)


def construct_principal_point_dist_calibration_message(
    sensor_name: SensorName, calibration: PrincipalPointDistortionCalibration
) -> PB.Calibration:
    log.info(f"Constructing principal point dist calibration message for sensor {sensor_name}")
    extrinsics = construct_extrinsics_message(calibration.position, calibration.rotation_quaternion)
    camera = PB.CameraCalibration(
        extrinsics=extrinsics,
        width=calibration.image_width,
        height=calibration.image_height,
        principal_point_dist=PB.PrincipalPointDistortion(
            principal_point=PB.PrincipalPoint(
                x=calibration.principal_point.x, y=calibration.principal_point.y
            ),
            distortion_center=PB.DistortionCenter(
                x=calibration.distortion_center.x, y=calibration.distortion_center.y
            ),
            lens_projection_coefficients=PB.LensProjectionCoefficients(
                c1=calibration.lens_projection_coefficients.c1,
                c2=calibration.lens_projection_coefficients.c2,
                c3=calibration.lens_projection_coefficients.c3,
                c4=calibration.lens_projection_coefficients.c4,
                c5=calibration.lens_projection_coefficients.c5,
                c6=calibration.lens_projection_coefficients.c6,
            ),
        ),
    )
    return PB.Calibration(
        sensor_name=sensor_name,
        camera=camera,
    )


def construct_openlabel_message(openlabel: dict) -> PB.OpenLabel:
    log.info("Constructing openlabel messeege")
    return PB.OpenLabel(open_label=json.dumps(openlabel))
