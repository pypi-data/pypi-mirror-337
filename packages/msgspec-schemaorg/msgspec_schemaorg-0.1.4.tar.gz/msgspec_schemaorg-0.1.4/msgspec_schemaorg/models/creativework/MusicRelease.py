from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.MusicPlaylist import MusicPlaylist
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.MusicAlbum import MusicAlbum
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.MusicReleaseFormatType import MusicReleaseFormatType
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class MusicRelease(MusicPlaylist):
    """A MusicRelease is a specific release of a music album."""
    type: str = field(default_factory=lambda: "MusicRelease", name="@type")
    releaseOf: 'MusicAlbum' | None = None
    musicReleaseFormat: 'MusicReleaseFormatType' | None = None
    recordLabel: 'Organization' | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None
    catalogNumber: str | None = None
    creditedTo: 'Person' | 'Organization' | None = None