from dataclasses import dataclass
from bleak import BleakClient
from bleak.backends.device import BLEDevice

from communication.transmitter import Transmitter


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

    async def send_raw(self, raw_command: bytes):
        for service in self._client.services:
            # Match the short Bluetooth UUID
            # print(f"Service: {service}")
            # print(f"suuid: {service.uuid} expected: {self._gatt.write_service}")
            if service.uuid[4:8] == self._gatt.write_service:
                for characteristic in service.characteristics:
                    # print(f"Characteristic: {characteristic}")
                    # print(f"cuuid: {characteristic.uuid} expected: {self._gatt.write_characteristic}")
                    if characteristic.uuid[4:8] == self._gatt.write_characteristic:
                        # print(f"Writing {characteristic} = {raw_command.hex()}")
                        return await self._client.write_gatt_char(characteristic, raw_command, False)