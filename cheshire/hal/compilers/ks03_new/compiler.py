from cheshire.compiler.compiler import StateCompiler
from cheshire.compiler.state import LightState
from cheshire.generic.command import *
from cheshire.generic.effect import Effect
from .constants import *
from .platform_commands import *


effect_to_scene_mapping = {
    # Effect.NONE: None,
    Effect.JUMP_7: KS03NewScene.JUMP_7,
    Effect.JUMP_3: KS03NewScene.JUMP_3,
    Effect.FADE_7: KS03NewScene.FADE_7,
    Effect.FADE_3: KS03NewScene.FADE_3,
    Effect.FLASH: KS03NewScene.FLASH,
    Effect.AUTO: KS03NewScene.AUTO,
}

effect_to_music_model_mapping = {
    # Effect.NONE: None,
    Effect.FADE_7_FAST_ON_NOISE: KS03NewMusicModel.FADE_7_FAST_ON_NOISE,
    Effect.TWO_FADE_FAST_ON_NOISE: KS03NewMusicModel.TWO_FADE_FAST_ON_NOISE,
    Effect.JUMP_ON_NOISE_PAUSE_QUIET: KS03NewMusicModel.JUMP_ON_NOISE_PAUSE_QUIET,
    Effect.JUMP_ON_NOISE_OFF_QUIET: KS03NewMusicModel.JUMP_ON_NOISE_OFF_QUIET,
}

class KS03NewCompiler(StateCompiler):
    def compile(self, state: LightState):
        platform_commands: list[PlatformCommand] = []

        # Set on/off state first
        if cmd := state.state.get('SwitchCommand'):
            platform_commands.append(
                KS03NewSwitchCommand(cmd.on)
            )

        # Extract brightness used in other commands
        brightness = 254
        if cmd := state.state.get('BrightnessCommand'):
            brightness = cmd.brightness

        # Extract speed used in other commands
        speed = 0
        if speed_cmd := state.state.get('SpeedCommand'):
            speed = speed_cmd.speed
        
        # KS03New uses different commands for setting color brightness etc.
        # for music and scene modes than in simple light mode
        if cmd := state.state.get('EffectCommand'):
            if cmd.effect != Effect.NONE:
                music_model= effect_to_music_model_mapping.get(cmd.effect)
                scene = effect_to_scene_mapping.get(cmd.effect)

                if music_model:
                    platform_commands.append(
                        KS03NewMusicModelCommand(music_model, speed)
                    )
                    
                if scene:
                    platform_commands.append(
                        KS03NewSceneCommand(scene, speed, brightness)
                    )

                return platform_commands
                
        
        r = 100
        g = 100
        b = 100

        if rgb_cmd := state.state.get('RGBCommand'):
            r = int((rgb_cmd.red * 100) / 255)
            g = int((rgb_cmd.green * 100) / 255)
            b = int((rgb_cmd.blue * 100) / 255)

        platform_commands.append(
            KS03NewRGBWBrightnessSpeedCommand(
                red=r, 
                green=g,
                blue=b,
                white=0, # KS03New doesn't support warm white
                brightness=brightness,
                speed=speed,
                is_rgb=True # Double-disables warm white :)
            )
        )

        return platform_commands