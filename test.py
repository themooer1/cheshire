import asyncio
from bleak import BleakScanner, BleakClient
from cheshire.compiler.state import LightState
from cheshire.generic.command import *
from cheshire.hal.devices import Connection, connect_to_ble_device

async def main():
    # Discover Bluetooth LE devices
    discover = await BleakScanner.discover()
    connections: list[Connection] = []

    # Connect to supported devices
    for bleak_device in discover:
        if bleak_device.name == None:
            continue

        # Get a device profile if it's supported
        if connection := await connect_to_ble_device(bleak_device):
            print(f"Connected to {bleak_device.name}")

            connections.append(connection)

    async def send_all(state: LightState):
        # Push light state to connected devices
        for c in connections:
            await c.apply(state)
            

    # Update desired light state
    state = LightState()
    state.update(SwitchCommand(on=True))
    state.update(BrightnessCommand(0x30))
    state.update(RGBCommand(0x0e, 0x0, 0xaa))
    # state.update(EffectCommand(Effect.JUMP_7))

    await send_all(state)


asyncio.run(main())