from .constants import KS03NewScene
from cheshire.generic.platform_command import PlatformCommand
from struct import Struct

# TODO: Not all of these are KS03New
# Notably the warm white + color temp methods are KS11
# Move them to proper platform support modules

class KS03NewSwitchCommand(PlatformCommand):
    def __init__(self, on: bool):
        on_off = b"\xF0" if on else b"\x0F"
        self._bytes = b"\x5B" + on_off + b"\x00\xB5"

class KS03NewRGBWBrightnessSpeedCommand(PlatformCommand):
    _color_struct = Struct("BBBBBB")

    def __init__(self, red: int, green: int, blue: int, white: int, brightness: int, speed: int, is_rgb: bool):
        is_rgb_hex = b"\x01" if is_rgb else b"\x02"
        white = 0 if is_rgb else white
        self._bytes = b"\x5A\x00" + is_rgb_hex + self._color_struct.pack(red, green, blue, white, brightness, speed) + b"\xA5"

class KS03NewSceneCommand(PlatformCommand):
    _scene_struct = Struct("BBB")

    def __init__(self, scene_num: KS03NewScene, speed: int, brightness: int):
        self._bytes = b"\x5C\x00" + self._scene_struct.pack(scene_num + 128, speed, brightness) + b"\x00\xC5"

class KS03NewMusicModelCommand(PlatformCommand):
    _music_model_struct = Struct("B")
    _speed_struct = Struct("B")

    def __init__(self, music_model: int, speed: int):
        self._bytes = b"\x5A\x0A\xF0" + self._music_model_struct.pack(music_model) + self._speed_struct.pack(8 - speed) + b"\xA5"



class KS03NewLightColorCeilingRGB_CCTCommand(PlatformCommand):
    _color_struct = Struct("BBBBBB")

    def __init__(self, red: int, green: int, blue: int, warm: int, bright: int, speed: int):
        self._bytes = b"\x5A\x00\x00" + self._color_struct.pack(red, green, blue, warm, bright, speed) + b"\xA5"

class KS03NewMusicRBGBrightnessCommand(PlatformCommand):
    _RGB_struct = Struct("BBB")
    _brightness_struct = Struct("B")

    def __init__(self, red: int, green: int, blue:int, brightness: int):
        self._bytes = b"\x5A\x00\x01" + self._RGB_struct(red, green, blue) + b"\x00" + self._brightness_struct(brightness) + b"\x00\xA5"

class KS03NewMusicRGBWBrigtnessCommand(PlatformCommand):
    _music_RGBW_brightness_struct = Struct("BBBBB")

    def __init__(self, red: int, green: int, blue:int, white: int, brightness: int):
        self._bytes = b"\x5A\x00\x00" + self._music_RGBW_brightness_struct.pack(red, green, blue, white, brightness) + b"\x00\xA5"

class KS03NewWWCWCommand(PlatformCommand):
    _wwcw_struct = Struct("BBB")

    def __init__(self, ww: int, cw: int, brightness: int):
        self._bytes = b"\x5A\x02" + self._wwcw_struct.pack(ww, cw, brightness) + b"\x00\xA5"
