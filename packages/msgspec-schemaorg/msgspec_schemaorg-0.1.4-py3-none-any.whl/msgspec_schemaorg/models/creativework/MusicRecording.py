from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicAlbum import MusicAlbum
    from msgspec_schemaorg.models.creativework.MusicComposition import MusicComposition
    from msgspec_schemaorg.models.creativework.MusicPlaylist import MusicPlaylist
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicRecording(CreativeWork):
    """A music recording (track), usually a single song."""
    type: str = field(default_factory=lambda: "MusicRecording", name="@type")
    recordingOf: 'MusicComposition' | None = None
    isrcCode: str | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None
    inAlbum: 'MusicAlbum' | None = None
    inPlaylist: 'MusicPlaylist' | None = None
    byArtist: 'MusicGroup' | 'Person' | None = None