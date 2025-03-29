from __future__ import annotations
from msgspec import Struct, field
from msgspec_schemaorg.models.creativework.CreativeWork import CreativeWork
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from msgspec_schemaorg.models.creativework.CreativeWorkSeason import CreativeWorkSeason
    from msgspec_schemaorg.models.creativework.VideoObject import VideoObject
    from msgspec_schemaorg.models.intangible.CreativeWorkSeries import CreativeWorkSeries
    from msgspec_schemaorg.models.intangible.Duration import Duration
    from msgspec_schemaorg.models.intangible.QuantitativeValue import QuantitativeValue
    from msgspec_schemaorg.models.organization.MusicGroup import MusicGroup
    from msgspec_schemaorg.models.organization.Organization import Organization
    from msgspec_schemaorg.models.organization.PerformingGroup import PerformingGroup
    from msgspec_schemaorg.models.person.Person import Person
from typing import Optional, Union, Dict, List, Any


class Episode(CreativeWork):
    """A media episode (e.g. TV, radio, video game) which can be part of a series or season."""
    type: str = field(default_factory=lambda: "Episode", name="@type")
    actors: 'Person' | None = None
    trailer: 'VideoObject' | None = None
    episodeNumber: int | str | None = None
    musicBy: 'Person' | 'MusicGroup' | None = None
    duration: 'QuantitativeValue' | 'Duration' | None = None
    actor: 'Person' | 'PerformingGroup' | None = None
    directors: 'Person' | None = None
    partOfSeason: 'CreativeWorkSeason' | None = None
    partOfSeries: 'CreativeWorkSeries' | None = None
    productionCompany: 'Organization' | None = None
    director: 'Person' | None = None