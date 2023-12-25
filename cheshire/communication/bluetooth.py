from dataclasses import dataclass
from bleak import BleakClient
from bleak.backends.device import BLEDevice

from cheshire.communication.transmitter import Transmitter


@dataclass
class GattProfile:
    """
    Holds the BLE GATT service and characteristic paths to read write and notify
    """

    write_service: str
    write_characteristic: str
    notify_service: str
    notify_characteristic: str
    read_service: str
    read_characteristic: str

    @classmethod
    def new(cls, read_write_notify_service: str, write_characteristic: str, notify_characteristic: str, read_characteristic: str):
        return cls.new_ex(
            read_write_notify_service,
            write_characteristic,
            read_write_notify_service,
            notify_characteristic,
            read_write_notify_service,
            read_characteristic)

    @classmethod
    def new_ex(cls, write_service: str, write_characteristic: str, notify_service: str, notify_characteristic: str, read_service: str, read_characteristic: str) -> "GattProfile":
        return cls(
            write_service,
            write_characteristic,
            notify_service,
            notify_characteristic,
            read_service,
            read_characteristic)


class BLETransmitter(Transmitter):
    def __init__(self, client: BleakClient, gatt: GattProfile):
        self._client = client
        self._gatt = gatt
        self._characteristic = None
        for service in self._client.services:
            # Match the short Bluetooth UUID
            if service.uuid[4:8] == self._gatt.write_service:
                for characteristic in service.characteristics:
                    if characteristic.uuid[4:8] == self._gatt.write_characteristic:
                        self._characteristic = characteristic
                        return
        raise ConnectionError(f"Expected BLEClient to support a characteristic with UUID[4:8] == {self._gatt.write_characteristic}")

    async def close(self):
        await self.disconnect()

    async def disconnect(self):
        await self._client.disconnect()

    async def send_raw(self, raw_command: bytes):
        return await self._client.write_gatt_char(self._characteristic, raw_command, False)