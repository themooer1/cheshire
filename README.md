![Cheshire Cat](./docs/assets/img/cheshire.png)
# Cheshire

API for Keepsmile and related Bluetooth LE lights.


## Usage

TODO update with simplified usage as package

```python
import asyncio
from bleak import BleakScanner, BleakClient
from compiler.state import LightState
from generic.command import *
from hal.devices import device_from_prefix

async def main():
    # Discover Bluetooth LE devices
    discover = await BleakScanner.discover()
    senders = []

    # Connect to supported devices
    for dev in discover:
        if dev.name == None:
            continue

        # Get a device profile if it's supported
        if profile := device_from_prefix(dev.name[:5]):
            print(f"Found {dev.name}")

            # Get device command compiler
            compiler = profile.compiler()

            # Connect
            client = BleakClient(dev)
            await client.connect()

            print(f"Connecting to {dev.name}")
            await client.connect()

            # Wrap BleakClient in a command transmitter
            transmitter = profile.get_transmitter(client)

            async def send_state(state: LightState):
                await transmitter.send_all(
                    compiler.compile(state)
                )

            senders.append(send_state)

    # Update desired light state
    state = LightState()
    state.update(SwitchCommand(on=True))
    state.update(BrightnessCommand(0x10))
    state.update(RGBCommand(0xfe, 0x0, 0x0))

    # Push light state to devices
    for s in senders:
        await s(state)

asyncio.run(main())
```

## Supported Devices
| Device | Bluetooth Name | Support |
|-|-|-|
| Keepsmile Led Strip Lights | KS03-XXXX | Yes |
| Keepsmile Led Strip Lights (New) | KS03~XXXX | Yes |
| Keepsmile Double Side Lighting Led Floor Lamp | ? | Unknown |
| luckystyle Floor Lamp | KS01-XXXX | Untested |