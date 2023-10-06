from abc import ABC, abstractmethod

from compiler.state import LightState
from generic.platform_command import PlatformCommand


class StateCompiler(ABC):
    """Turns a light state into a list of platform commands which will achieve that state."""
    @abstractmethod
    def compile(self, state: LightState) -> list[PlatformCommand]:
        # Match on supported commands here. Ignore unsupported ones
        pass