import asyncio
from bleak import BleakScanner

async def scan_ble(timeout=5):
    devices = await BleakScanner.discover(timeout=timeout)
    result = []

    for d in devices:
        result.append({
            "name": d.name,
            "address": d.address,
            "rssi": getattr(d, "rssi", None)
        })

    return result

def scan_ble_sync(timeout=5):
    return asyncio.run(scan_ble(timeout))