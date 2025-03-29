import logging
from typing import ByteString

import kognic.studio.proto.messages_pb2 as PB
from kognic.studioloader.connection_handler import ConnectionHandler
from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.interfaces.warehouse import Warehouse
from websockets.asyncio.client import ClientConnection


log = logging.getLogger(__name__)


class ServerHandler:

    def __init__(self, warehouse: Warehouse) -> None:
        self.warehouse = warehouse

    async def handle(self, websocket: ClientConnection):
        log.info(f"Got connection: {websocket}")
        await self.init_connection(websocket)

        loader = await self.initialize_loader(websocket)
        connection_handler = ConnectionHandler(loader, websocket)
        await connection_handler.run()

    async def init_connection(self, websocket: ClientConnection):
        scenes = self.warehouse.get_available_scenes()
        log.info(f"Available scenes: {scenes}")
        await websocket.send(
            PB.Message(
                initial_server_message=PB.InitialServerMessage(available_scenes=scenes)
            ).SerializeToString()
        )

    async def initialize_loader(self, websocket) -> Loader:
        recv_message: ByteString = await websocket.recv()
        message = PB.Message()
        message.ParseFromString(recv_message)
        message_type = message.WhichOneof("data")

        if message_type != "initialize_scene":
            fields = message.ListFields()
            fields = [field[0].name for field in fields]
            log.error(f"Unexpected initialize_scene message: {fields}")
            raise Exception(f"Unexpected initialize_scene message: {fields}")

        scene_to_load = message.initialize_scene.scene
        loader = self.warehouse.initialize_scene(scene_to_load)
        log.info("Initialized loader")
        return loader
