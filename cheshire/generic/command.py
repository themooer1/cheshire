from dataclasses import dataclass

from .effect import Effect

@dataclass
class Command:
    """Generic meta-command which maps to one or more device commands."""
    def get_type(self):
        return type(self).__name__

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
