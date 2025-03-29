from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
    from msgspec_schemaorg.models.creativework.MusicComposition import MusicComposition
    from msgspec_schemaorg.models.creativework.MusicRecording import MusicRecording
    from msgspec_schemaorg.models.event.Event import Event
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicComposition(CreativeWork):
    """A musical composition."""
    type: str = field(default_factory=lambda: "MusicComposition", name="@type")
    firstPerformance: 'Event' | None = None
    iswcCode: str | None = None
    composer: 'Person' | 'Organization' | None = None
    recordedAs: 'MusicRecording' | None = None
    lyricist: 'Person' | None = None
    musicArrangement: 'MusicComposition' | None = None
    lyrics: 'CreativeWork' | None = None
    includedComposition: 'MusicComposition' | None = None
    musicalKey: str | None = None
    musicCompositionForm: str | None = None