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
    videoFrameSize: Union[List[str], str, None] = None
    embeddedTextCaption: Union[List[str], str, None] = None
    actors: Union[List['Person'], 'Person', None] = None
    caption: Union[List[Union[str, 'MediaObject']], Union[str, 'MediaObject'], None] = None
    videoQuality: Union[List[str], str, None] = None
    musicBy: Union[List[Union['Person', 'MusicGroup']], Union['Person', 'MusicGroup'], None] = None
    transcript: Union[List[str], str, None] = None
    actor: Union[List[Union['Person', 'PerformingGroup']], Union['Person', 'PerformingGroup'], None] = None
    directors: Union[List['Person'], 'Person', None] = None
    director: Union[List['Person'], 'Person', None] = None