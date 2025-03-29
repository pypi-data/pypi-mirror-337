import asyncio
from kognic.studioloader.server import run
from kognic.studioloader.warehouse.everything_warehouse import EverythingWarehouse


def main():
    warehouse = EverythingWarehouse()
    asyncio.run(run(warehouse))

