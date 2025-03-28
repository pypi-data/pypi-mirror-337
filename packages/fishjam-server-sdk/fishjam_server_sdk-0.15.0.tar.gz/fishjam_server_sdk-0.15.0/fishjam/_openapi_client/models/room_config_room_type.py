from enum import Enum


class RoomConfigRoomType(str, Enum):
    """The use-case of the room. If not provided, this defaults to full_feature."""

    AUDIO_ONLY = "audio_only"
    BROADCASTER = "broadcaster"
    FULL_FEATURE = "full_feature"

    def __str__(self) -> str:
        return str(self.value)
