from .constants import KS03OldScene
from cheshire.generic.platform_command import PlatformCommand
from struct import Struct

class KS03OldSwitchCommand(PlatformCommand):
    def __init__(self, on: bool):
        if on:
            self._bytes = b"\x7e\x04\x04\xf0\x01\x01\xff\x00\xef"
        else:
            self._bytes = b"\x7e\x04\x04\x10\x01\x00\xff\x00\xef"

class KS03OldBrightnessCommand(PlatformCommand):
    _brightness_struct = Struct("B")

    def __init__(self, brightness: int):
        self._bytes = b"\x7E\x04\x01" + self._brightness_struct.pack(brightness) + b"\xFF\xFF\xFF\x00\xEF"

class KS03OldRGBCommand(PlatformCommand):
    _rgb_struct = Struct("BBB")

    def __init__(self, red: int, green: int, blue: int):
        self._bytes = b"\x7E\x07\x05\x03" + self._rgb_struct.pack(red, green, blue) + b"\x00\xEF"
    
class KS03OldSpeedCommand(PlatformCommand):
    _speed_struct = Struct("B")

    def __init__(self, speed: int):
        self._bytes = b"\x7E\x04\x02" + self._speed_struct.pack(speed) + b"\xFF\xFF\xFF\x00\xEF"

class KS03OldSceneCommand(PlatformCommand):
    _scene_struct = Struct("B")

    def __init__(self, scene: KS03OldScene):
        self._bytes = b"\x7E\x05\x03" + self._scene_struct.pack(scene + 128) + b"\x03\xFF\xFF\x00\xEF"

class KS03OldMusicModelCommand(PlatformCommand):
    _music_model_struct = Struct("B")
    _speed_struct = Struct("B")

    def __init__(self, music_model: int, speed: int):
        self._bytes = b"\x7E\x0A" + self._music_model_struct.pack(music_model) + self._speed_struct.pack(8 - speed) + b"\xA5"


        # for kind, cmd in state.state.values():
        #     if isinstance(cmd, SwitchCommand):
        #         kstate.on = cmd.on
        #     if isinstance(cmd, BrightnessCommand):
        #         kstate.brightness
        #     if isinstance(cmd, RGBCommand):
        #         kstate.red = cmd.red
        #         kstate.green = cmd.green
        #         kstate.blue = cmd.blue
        #     if isinstance(cmd, EffectCommand):
        #         scene = effect_to_scene_mapping[cmd.effect]
        #         music_model= effect_to_music_model_mapping[cmd.effect]

        #         if scene:
        #             kstate.scene = scene.value
        #         if music_model
        #             kstate.music = music_modelvalue
        #     if isinstance(cmd, SpeedCommand):
        #         kstate.speed = cmd.speed
