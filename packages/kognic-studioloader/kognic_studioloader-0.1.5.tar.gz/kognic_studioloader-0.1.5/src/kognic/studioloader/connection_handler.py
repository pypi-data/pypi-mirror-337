import asyncio
import logging

import kognic.studio.proto.messages_pb2 as PB
import websockets
from kognic.studioloader.interfaces.loader import Loader
from websockets.asyncio.client import ClientConnection

log = logging.getLogger(__name__)


class ConnectionHandler:

    def __init__(self, loader: Loader, websocket: ClientConnection) -> None:
        self.loader = loader
        self.websocket = websocket

    async def run(self):

        initial_frames = await self.send_initial_scene_information()

        await self.send_pre_annotation()

        await self.send_new_frames_resources(initial_frames)

        log.info("Entering steady state mode")
        while True:
            try:
                await self.run_steady_state()
            except KeyboardInterrupt:
                break
            except websockets.ConnectionClosed:
                log.info("Client disconnected, ending steady state mode")
                break

    async def send_new_frames_resources(
        self,
        frames_message: PB.Frames,
    ):
        frame_ids = [frame.frame_id for frame in frames_message.frames]
        await self.send_resources_for_frame_ids(frame_ids)

    async def send_resources_for_frame_ids(
        self,
        frame_ids: list[str],
    ):
        for frame_id in frame_ids:
            for resource in self.loader.get_resources_for_frame(frame_id):
                if isinstance(resource, PB.CameraImage):
                    message = PB.Message(camera_image=resource)
                else:
                    message = PB.Message(point_cloud=resource)
                await self.websocket.send(message.SerializeToString())
        log.info("Upload of scene resource data complete")

    async def send_initial_scene_information(
        self,
    ) -> PB.Frames:
        frames_message = self.loader.get_frames()
        message = PB.Message(frames=frames_message)
        await self.websocket.send(message.SerializeToString())

        sensor_spec_message = self.loader.get_sensor_spec()
        message = PB.Message(sensor_spec=sensor_spec_message)
        await self.websocket.send(message.SerializeToString())

        for calibration_message in self.loader.get_calibrations():
            message = PB.Message(calibration=calibration_message)
            await self.websocket.send(message.SerializeToString())

        return frames_message

    async def send_pre_annotation(self):
        openlabel_message = self.loader.get_openlabel()
        message = PB.Message(open_label=openlabel_message)
        await self.websocket.send(message.SerializeToString())

    async def handle_save_openlabel_message(self, openlabel: PB.OpenLabel):
        return self.loader.save_openlabel(openlabel)

    async def run_steady_state(self):
        for calibration_message in self.loader.poll_calibrations():
            log.info("Calibration changed, uploading")
            message = PB.Message(calibration=calibration_message)
            await self.websocket.send(message.SerializeToString())

        try:
            raw_message = await asyncio.wait_for(self.websocket.recv(), 1)
            message = PB.Message()
            message.ParseFromString(raw_message)
            message_type = message.WhichOneof("data")
            if message_type == "open_label":
                log.info(f"Got to save openlabel")
                await self.handle_save_openlabel_message(message.open_label)

        except asyncio.TimeoutError:
            log.debug("No message")

        await self.websocket.pong()
