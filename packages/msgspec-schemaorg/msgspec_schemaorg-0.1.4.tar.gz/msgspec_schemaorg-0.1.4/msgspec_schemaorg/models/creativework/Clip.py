from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.Episode import Episode
    from msgspec_schemaorg.models.creativework.HyperTocEntry import HyperTocEntry
    from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Clip(CreativeWork):
    """A short TV or radio program or a segment/part of a program."""
    type: str = field(default_factory=lambda: "Clip", name="@type")
    clipNumber: int | str | None = None
    actors: 'Person' | None = None
    endOffset: int | float | 'HyperTocEntry' | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    partOfEpisode: 'Episode' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    partOfSeason: 'CreativeWorkSeason' | None = None
    partOfSeries: 'CreativeWorkSeries' | None = None
    startOffset: int | float | 'HyperTocEntry' | None = None
    director: 'Person' | None = None