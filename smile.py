import asyncio
from bleak import BleakScanner, BleakClient
import bleak as b

import pdb

from cheshire.hal.compilers.ks03_new.constants import KS03NewScene


dev_name = "KS03~"

def hex_byte(i: int):
    return hex(i).lstrip('0x').zfill(2)

def rgb_new(red: int, green: int, blue: int, white: int = 0, brightness: int = 0xff):
    prefix = "5a00"
    is_rgb = "01"
    rgb_hex = f"{hex_byte(red)}{hex_byte(green)}{hex_byte(blue)}"
    white = hex_byte(white)
    brightness = hex_byte(brightness)
    speed = "00"
    suffix = "a5"

    return prefix + is_rgb + rgb_hex + white + brightness + speed + suffix

def scene(scene_num: int):
    # return "7E0503" + ByteConvertor.toByte16(sceneNum + 128) + "03FFFF00EF"
    # Looks like toByte16 isn't actually 16bits, but just zero pads out to 2 chars
    return "7E0503" + hex_byte(scene_num + 128) + "03FFFF00EF"

def scene_new(scene_num: int, speed: int, brightness: int):
    # return "7E0503" + ByteConvertor.toByte16(sceneNum + 128) + "03FFFF00EF"
    return "5C00" + hex_byte(scene_num + 128) + hex_byte(speed) + hex_byte(brightness) + "00C5"

def white_new(ww: int, cw: int, brightness: int):
    return "5A02" + hex_byte(ww) + hex_byte(cw) + hex_byte(brightness) + "00A5"

async def main():
    # devices: [] = await BleakScanner.discover()
    # # pdb.set_trace()
    # [d] = [d for d in devices if d.name == dev_name]

    # d = await BleakScanner.find_device_by_name(dev_name)
    d = await BleakScanner.find_device_by_filter(lambda dev, ad: dev and dev.name and dev.name.startswith(dev_name))
    if d is None:
        raise ConnectionError("Didn't find BLE device")
    
    async with BleakClient(d) as c:
        tch = None
        for s in c.services:
            print(s.uuid)
            for ch in s.characteristics:
                print(ch.uuid)
                print(ch.description)
                # if ch.uuid[4:8] == "fff3":
                if ch.uuid[4:8] == "afd1":
                    # print(await c.write_gatt_char(ch, bytes.fromhex("5a0001ff0000000f00a5"), True))
                    # print(await c.write_gatt_char(ch, bytes.fromhex("5a000100ff00000f00a5"), True))
                    print(await c.write_gatt_char(ch, bytes.fromhex("5a00010000ff000f00a5"), True))
                    # print(await c.write_gatt_char(ch, bytes.fromhex(white_new(0, 128, 128)), True))
                    # print("sent")
                    # for scene_num in range(0, 1):
                    #     print(await c.write_gatt_char(ch, bytes.fromhex(scene_new(KS03NewScene.FLASH, 0, 80)), True))
                    #     print(f"sent scene: {scene_num}")
                    #     await asyncio.sleep(5)
                    #     print(f"slept")


            print()
        # await c.write_gatt_char("fff3", bytes.fromhex(""))
    
    


    # pdb.set_trace()
    # for d in devices:
        # print(dir(d))

asyncio.run(main())