# User Guide

## Discover

To connect to a light and start controlling it, use the `connect_to_ble_device` method
from cheshire.hal.devices on a `BLEDevice`` discovered by bleak.

If the device is supported, and the connection succeeds, you will get back a `Connection`
and if not, `None`.

```python
# Discover Bluetooth LE devices
device = await BleakScanner.find_device_by_name(name='KS03~AAABBB')

# Connect to this device if it's supported
if connection := await connect_to_ble_device(bleak_device):
    print(f"Connected to {bleak_device.name}")
```

Assuming the connection succeeded, you now have a `Connection` object which you can use
to push a certain desired state to the light.

## LightState

In Cheshire, you describe your desired state (color, brightness, special effects, etc.)
as a `LightState` which you can then apply to a connected device.

```python
from cheshire.compiler.state import LightState

# Update desired light state
state = LightState()
```

The state is updated with commands which may or may not be supported by your target device
e.g. some devices only output white light and don't support RGB. Unsupported commands are
simply ignored.

```python
from cheshire.generic.command import *

state.update(SwitchCommand(on=True))
state.update(BrightnessCommand(0x30))
state.update(RGBCommand(0x0e, 0x0, 0xaa))
```

## Commands

### List

Commands are defined in [/cheshire/generic/command.py](/cheshire/generic/command.py) which is
copied below verbatim.

```python
@dataclass
class SwitchCommand(Command):
    on: bool

@dataclass
class BrightnessCommand(Command):
    brightness: int

@dataclass
class ColorTemperatureCommand(Command):
    ww: int
    cw: int

@dataclass
class RGBCommand(Command):
    red: int
    green: int
    blue: int

@dataclass
class WhiteCommand(Command):
    white: int

@dataclass
class EffectCommand(Command):
    effect: Effect

@dataclass
class SpeedCommand(Command):
    speed: int
```

### Query Device Support

To check explicitly whether a given device supports a command, you can check it's `DeviceProfile`.

```python
from cheshire.hal.devices import device_profile_from_ble_device

# BLEDevice from Bleak
device: BLEDevice

profile = device_profile_from_ble_device(device)

# Only connect if this device supports changing the color temperature
if ColorTemperatureCommand in profile.supported_commands:

    # You can optionally connect using the device profile
    connection = profile.connect(device)
```

## Controlling the Light

With a `LightState` and a `Connection`, all that's left is to call `apply(state: LightState)`

```python
# Connected device from above
connection: Connection

# LightState configured above
state: LightState

await connection.apply(state)
```