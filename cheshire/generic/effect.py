from enum import Enum

class Effect(Enum):
    """Generic effects which may be interpreted differently or not at all
    by different devices"""
    NONE = -1
    JUMP_7 = 0
    JUMP_3 = 1
    FADE_7 = 2
    FADE_3 = 3
    FLASH  = 4
    AUTO   = 5
    # Slowly fades through colors. Noise increases speed.
    FADE_7_FAST_ON_NOISE = 600
    # Slowly pulses each color twice. Noise increases speed.
    TWO_FADE_FAST_ON_NOISE = 700
    # Solid color. Noise quickly cycles through colors.
    JUMP_ON_NOISE_PAUSE_QUIET = 800
    # Off. Noise turns on lights and quickly cycles through colors.
    JUMP_ON_NOISE_OFF_QUIET = 900