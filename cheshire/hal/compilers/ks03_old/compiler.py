from cheshire.compiler.compiler import StateCompiler
from cheshire.compiler.state import LightState
from cheshire.generic.command import SwitchCommand, BrightnessCommand, RGBCommand, EffectCommand, SpeedCommand
from cheshire.generic.effect import Effect
from .platform_commands import *
from .constants import *

effect_to_scene_mapping = {
    # Effect.NONE: None,
    Effect.JUMP_7: KS03OldScene.JUMP_7,
    Effect.JUMP_3: KS03OldScene.JUMP_3,
    Effect.FADE_7: KS03OldScene.FADE_7,
    Effect.FADE_3: KS03OldScene.FADE_3,
    Effect.FLASH: KS03OldScene.FLASH,
    Effect.AUTO: KS03OldScene.AUTO,
}

effect_to_music_model_mapping = {
    # Effect.NONE: None,
    Effect.FADE_7_FAST_ON_NOISE: KS03OldMusicModel.FADE_7_FAST_ON_NOISE,
    Effect.TWO_FADE_FAST_ON_NOISE: KS03OldMusicModel.TWO_FADE_FAST_ON_NOISE,
    Effect.JUMP_ON_NOISE_PAUSE_QUIET: KS03OldMusicModel.JUMP_ON_NOISE_PAUSE_QUIET,
    Effect.JUMP_ON_NOISE_OFF_QUIET: KS03OldMusicModel.JUMP_ON_NOISE_OFF_QUIET,
}

class KS03OldCompiler(StateCompiler):
    def compile(self, state: LightState):
        platform_commands: list[PlatformCommand] = []

        # Set on/off state first
        if cmd := state.state.get('SwitchCommand'):
            platform_commands.append(
                KS03OldSwitchCommand(cmd.on)
            )

    
        # Set scene / music mode
        # (I think this needs to be set, then speed, then brightness
        # possibly with 100ms delays between commands)
        if cmd := state.state.get('EffectCommand'):
            if cmd.effect == Effect.NONE:
                # Set a solid color
                if cmd := state.state.get('RGBCommand'):
                    platform_commands.append(
                        KS03OldRGBCommand(
                            int((cmd.red * 100) / 255),
                            int((cmd.green * 100) / 255),
                            int((cmd.blue * 100) / 255)
                        )
                    )
            else:
                scene = effect_to_scene_mapping.get(cmd.effect)
                music_model = effect_to_music_model_mapping.get(cmd.effect)
                # TODO support music mode
                if music_model is not None:
                    speed = 0
                    if speed_cmd := state.state.get('SpeedCommand'):
                        speed = speed_cmd.speed
                    platform_commands.append(
                        KS03OldMusicModelCommand(music_model, speed)
                    )
                if scene is not None:
                    platform_commands.append(
                        KS03OldSceneCommand(
                            scene
                        )
                    )

        # Set speed
        if cmd := state.state.get('SpeedCommand'):
            platform_commands.append(
                KS03OldSpeedCommand(
                    cmd.speed
                )
            )

        # Set brightness
        if cmd := state.state.get('BrightnessCommand'):
            platform_commands.append(
                KS03OldBrightnessCommand(int((cmd.brightness * 100) / 255))
            )

        return platform_commands
