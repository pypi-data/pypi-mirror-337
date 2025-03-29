import json
import logging
from pathlib import Path


from kognic.io.model.calibration.calib import BaseCalibration, SensorCalibrationEntry
from kognic.io.model.ego import EgoVehiclePose

log = logging.getLogger(__name__)


def get_image_bytes(image_path: Path) -> bytes:
    log.debug(f"Loading image bytes from {image_path}")
    with open(image_path, "rb") as fp:
        return fp.read()


def load_calibrations(path: Path) -> dict[str, BaseCalibration]:
    with open(path) as fp:
        raw_calibrations = json.load(fp)
    calibrations = {}
    for sensor_name, raw_calibration in raw_calibrations.items():
        calibrations[sensor_name] = SensorCalibrationEntry._parse_calibration(raw_calibration)
    return calibrations


def load_poses(path: Path) -> dict[str, EgoVehiclePose]:
    with open(path) as fp:
        raw_poses = json.load(fp)
    poses = {}
    for frame_id, raw_pose in raw_poses.items():
        poses[frame_id] = EgoVehiclePose.model_validate(raw_pose)
    return poses


def load_json(path: Path) -> dict:
    with open(path, "r") as fp:
        return json.load(fp)
