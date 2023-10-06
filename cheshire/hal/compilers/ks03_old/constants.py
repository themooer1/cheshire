from enum import IntEnum

class KS03OldScene(IntEnum):
    JUMP_7 = 0
    JUMP_3 = 1
    FADE_7 = 2
    FADE_3 = 3
    FLASH  = 4
    AUTO   = 5

class KS03OldMusicModel(IntEnum):
    # Slowly fades through colors. Noise increases speed.
    FADE_7_FAST_ON_NOISE = 0
    # Slowly pulses each color twice. Noise increases speed.
    TWO_FADE_FAST_ON_NOISE = 1
    # Solid color. Noise quickly cycles through colors.
    JUMP_ON_NOISE_PAUSE_QUIET = 2
    # Off. Noise turns on lights and quickly cycles through colors.
    JUMP_ON_NOISE_OFF_QUIET = 3

