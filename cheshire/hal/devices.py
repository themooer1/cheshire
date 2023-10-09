from dataclasses import dataclass
from enum import Enum
from typing import Callable

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from cheshire.communication.bluetooth import BLETransmitter, GattProfile
from cheshire.communication.transmitter import Transmitter
from cheshire.compiler.compiler import StateCompiler
from cheshire.compiler.state import LightState
from cheshire.generic.command import *

from cheshire.generic.command import Command
from .compilers.ks03_old.compiler import KS03OldCompiler
from .compilers.ks03_new.compiler import KS03NewCompiler

class DeviceNamePrefix(Enum):
    """
    Device types are determined from the Bluetooth device name prefix.
    """
    KS01 = "KS01-"
    KS02 = "KS02-"
    KS03 = "KS03-"
    KS03_New = "KS03~"
    KS04 = "KS04-"
    KS04_New = "KS04~"
    KS05 = "KS05-"
    KS07 = "KS07-"
    KS08 = "KS08-"
    KS09 = "KS09-"
    KS10 = "KS10-"
    KS11 = "KS11-" # Seems to have white led in addition to RGB
    KS12 = "KS12-"
    KS13 = "KS13-"

        
def gatt_from_prefix(prefix: DeviceNamePrefix) -> GattProfile | None:
    gatt_profile_by_prefix = {
        DeviceNamePrefix.KS01: GattProfile.new("ae00", "ae01", "ae02", "ae01"),
        DeviceNamePrefix.KS03: GattProfile.new("fff0", "fff3", "fff3", "fff3"),
        DeviceNamePrefix.KS03_New: GattProfile.new("afd0", "afd1", "afd2", "afd3"),
        DeviceNamePrefix.KS04: GattProfile.new("fff0", "fff3", "fff3", "fff3"),
        DeviceNamePrefix.KS04_New: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS05: GattProfile.new_ex("ae00", "ae01", "ae00", "ae02", "ff00", "ff02"),
        DeviceNamePrefix.KS05: GattProfile.new("ae00", "ae01", "ae02", "ff02"),
        DeviceNamePrefix.KS07: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS08: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS09: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS10: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS11: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS12: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        DeviceNamePrefix.KS13: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
    }

    return gatt_profile_by_prefix.get(prefix)

def transmitter_from_prefix(prefix: DeviceNamePrefix, client: BleakClient) -> Transmitter | None:
    return BLETransmitter(client, gatt_from_prefix(prefix))

class Connection:
    def __init__(self, compiler: StateCompiler, transmitter: Transmitter):
        self._transmitter = transmitter
        self._compiler = compiler

    async def apply(self, state: LightState):
        await self._transmitter.send_all(
            self._compiler.compile(state)
        )

    async def disconnect(self):
        await self._transmitter.close()

@dataclass
class DeviceProfile:
    supported_commands: list[type[Command]]
    compiler: StateCompiler
    get_transmitter: Callable[[BleakClient], Transmitter] 

    async def connect(self, device: BLEDevice):
        # Instantiate device command compiler
        compiler = self.compiler()

        # Connect
        client = BleakClient(device)
        await client.connect()

        # Wrap BleakClient in a command transmitter
        transmitter = self.get_transmitter(client)

        return Connection(compiler, transmitter)

def make_transmitter_fetcher(prefix: DeviceNamePrefix):
    def fetcher(client: BleakClient):
        return transmitter_from_prefix(
            prefix,
            client
        )

    return fetcher

devices_by_prefix = {
        # DeviceNamePrefix.KS01: GattProfile.new("ae00", "ae01", "ae02", "ae01"),
        DeviceNamePrefix.KS03: DeviceProfile(
            supported_commands=[
                SwitchCommand,
                BrightnessCommand,
                RGBCommand,
                EffectCommand,
                SpeedCommand
            ],
            compiler=KS03OldCompiler,
            get_transmitter=make_transmitter_fetcher(DeviceNamePrefix.KS03),
        ),
        DeviceNamePrefix.KS03_New: DeviceProfile(
            supported_commands=[
                SwitchCommand,
                BrightnessCommand,
                RGBCommand,
                EffectCommand,
                SpeedCommand
            ],
            compiler=KS03NewCompiler,
            get_transmitter=make_transmitter_fetcher(DeviceNamePrefix.KS03_New),
        ),
        # DeviceNamePrefix.KS03_New: GattProfile.new("afd0", "afd1", "afd2", "afd3"),
        # # DeviceNamePrefix.KS04: GattProfile.new("fff0", "fff3", "fff3", "fff3"),
        # # DeviceNamePrefix.KS04_New: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS05: GattProfile.new_ex("ae00", "ae01", "ae00", "ae02", "ff00", "ff02"),
        # # DeviceNamePrefix.KS05: GattProfile.new("ae00", "ae01", "ae02", "ff02"),
        # # DeviceNamePrefix.KS07: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS08: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS09: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS10: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS11: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS12: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
        # # DeviceNamePrefix.KS13: GattProfile.new("ae00", "ae01", "ae02", "ae10"),
    }

def device_from_prefix(prefix: DeviceNamePrefix | str) -> DeviceProfile | None:
    if isinstance(prefix, str):
        try:
            prefix = DeviceNamePrefix(prefix)
        except ValueError:
            return None

    return devices_by_prefix.get(prefix)

def device_profile_from_ble_device(bleak_device: BLEDevice) -> DeviceProfile | None:
# Fetch device based on first 5 characters of its name
    if bleak_device.name:
        return device_from_prefix(bleak_device.name[:5])

async def connect_to_ble_device(bleak_device: BLEDevice) -> Connection | None:
    # Fetch device based on first 5 characters of its name
    if device := device_profile_from_ble_device(bleak_device):
        return await device.connect(bleak_device)