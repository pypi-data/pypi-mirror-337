from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.intangible.ItemList import ItemList
from typing import Optional, Union, Dict, List, Any


class MusicPlaylist(CreativeWork):
    """A collection of music tracks in playlist form."""
    type: str = field(default_factory=lambda: "MusicPlaylist", name="@type")
    numTracks: int | None = None
    track: 'MusicRecording' | 'ItemList' | None = None
    tracks: 'MusicRecording' | None = None