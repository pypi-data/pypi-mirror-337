import asyncio
import logging

from kognic.studioloader.interfaces.warehouse import Warehouse
from kognic.studioloader.logging_utils import setup_logging
from kognic.studioloader.server_handler import ServerHandler
from websockets.asyncio.server import serve

from kognic.studioloader.warehouse.zod_warehouse import ZodWarehouse

log = logging.getLogger(__name__)
setup_logging()


async def run(warehouse: Warehouse):
    log.info("Starting websocket server")
    server_handler = ServerHandler(warehouse)
    async with serve(
        server_handler.handle,
        "localhost",
        8765,
    ):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    warehouse = ZodWarehouse(bootstrap=True)
    asyncio.run(run(warehouse))
