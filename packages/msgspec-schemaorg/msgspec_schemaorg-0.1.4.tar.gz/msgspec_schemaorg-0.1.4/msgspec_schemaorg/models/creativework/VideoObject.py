from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MediaObject import MediaObject
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class VideoObject(MediaObject):
    """A video file."""
    type: str = field(default_factory=lambda: "VideoObject", name="@type")
    videoFrameSize: str | None = None
    embeddedTextCaption: str | None = None
    actors: 'Person' | None = None
    caption: str | 'MediaObject' | None = None
    videoQuality: str | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    transcript: str | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    director: 'Person' | None = None