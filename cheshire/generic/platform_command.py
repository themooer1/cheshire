from dataclasses import dataclass

@dataclass
class PlatformCommand:
    """Low level command which maps directly to a device command"""
    def get_type(self):
        return type(self)

    def get_bytes(self) -> bytes:
        return self._bytes
