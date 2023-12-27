from enum import Enum

class Effect(Enum):
    """Generic effects which may be interpreted differently or not at all
    by different devices"""
    NONE = "None"
    JUMP_7 = "Jump 7"
    JUMP_3 = "Jump 3"
    FADE_7 = "Fade 7"
    FADE_3 = "Fade 3"
    FLASH  = "Flash"
    AUTO   = "Auto"
    # Slowly fades through colors. Noise increases speed.
    FADE_7_FAST_ON_NOISE = "Fade 7 Volume Controls Speed"
    # Slowly pulses each color twice. Noise increases speed.
    TWO_FADE_FAST_ON_NOISE = "Two Fade Volume Controls Speed"
    # Solid color. Noise quickly cycles through colors.
    JUMP_ON_NOISE_PAUSE_QUIET = "Cycle Colors When Loud"
    # Off. Noise turns on lights and quickly cycles through colors.
    JUMP_ON_NOISE_OFF_QUIET = "Light and Cycle Colors When Loud"